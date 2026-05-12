"""
deep_research — research_manager.py

Async orchestration engine for the deep research pipeline.
Ported from playground/deep_research/research_manager.py with:
  - YAML-driven prompt variants
  - Pydantic schema validation at every boundary
  - Resend notification (replaces SendGrid email_agent)
  - ArticleReportData output when variant='article'
"""
import asyncio
import logging
from typing import AsyncGenerator, Optional, Union

from agents import Runner, gen_trace_id, trace
from kk_utils.execution_trace import emit_trace

from kk_agent_skills.deep_research.agents._prompt_loader import (
    get_notification_config,
    get_planner_instruction,
)
from kk_agent_skills.deep_research.agents.notifier import send_research_report
from kk_agent_skills.deep_research.agents.planner_agent import make_planner_agent
from kk_agent_skills.deep_research.agents.search_agent import make_search_agent
from kk_agent_skills.deep_research.agents.writer_agent import make_writer_agent
from kk_agent_skills.deep_research.schemas import (
    ArticleReportData,
    ReportData,
    WebSearchItem,
    WebSearchPlan,
)

logger = logging.getLogger(__name__)


class ResearchManager:
    """
    Orchestrates the full multi-agent research pipeline.

    Pipeline:
        plan_searches → perform_searches (parallel) → write_report → [notify]

    Supports two output modes:
        - variant='article' → returns ArticleReportData
        - all other variants → returns ReportData
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    async def run(
        self,
        query: str,
        variant: str = "general",
        send_notification: bool = False,
        notification_recipient: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Run the full research pipeline, yielding status strings then the final output.

        The last yielded value is always the main content (markdown_report or markdown_content).

        Args:
            query: The research question or topic.
            variant: Prompt variant (general | technical | market | article).
            send_notification: Whether to email the report via Resend.
            notification_recipient: Override recipient email address.

        Yields:
            Status update strings during execution.
            Final yielded value: markdown report or article content.
        """
        trace_id = gen_trace_id()
        trace_url = f"https://platform.openai.com/traces/trace?trace_id={trace_id}"

        with trace("deep_research", trace_id=trace_id):
            logger.info(f"Deep research started: query='{query}' variant='{variant}' trace={trace_id}")
            emit_trace(f"deep_research start query={query!r} variant={variant!r} trace_id={trace_id}")
            yield f"Starting research (variant: {variant})..."
            yield f"Trace: {trace_url}"

            # Stage 1: Plan
            emit_trace(f"deep_research plan start query={query!r}")
            search_plan = await self._plan_searches(query, variant)
            emit_trace(f"deep_research plan done searches={len(search_plan.searches)}")
            yield f"Searches planned ({len(search_plan.searches)} queries), searching..."

            # Stage 2: Search (parallel)
            emit_trace("deep_research search stage start")
            search_results, queries_used = await self._perform_searches(search_plan, variant)
            emit_trace(f"deep_research search stage done results={len(search_results)}")
            yield f"Searches complete ({len(search_results)} results), writing report..."

            # Stage 3: Write
            emit_trace("deep_research write stage start")
            report = await self._write_report(query, search_results, variant)
            emit_trace("deep_research write stage done")
            yield "Report written."

            # Stage 4: Notify (optional)
            if send_notification:
                yield "Sending notification email..."
                emit_trace("deep_research notify stage start")
                try:
                    notif_config = get_notification_config(variant)
                    subject = notif_config.get("subject_template", "Research: {query}").format(
                        query=query[:80]
                    )
                    send_research_report(
                        markdown_report=self._get_report_markdown(report),
                        subject=subject,
                        recipient=notification_recipient,
                    )
                    emit_trace("deep_research notify stage done")
                    yield "Notification sent."
                except Exception as exc:
                    logger.warning(f"Notification failed (non-fatal): {exc}")
                    emit_trace(f"deep_research notify error: {exc}")
                    yield f"Notification skipped: {exc}"

            emit_trace("deep_research complete")
            yield "Research complete."
            # Final yield: the primary content
            yield self._get_report_markdown(report)

    def _get_report_markdown(self, report: Union[ReportData, ArticleReportData]) -> str:
        """Extract the main markdown content from either report type."""
        if isinstance(report, ArticleReportData):
            return report.markdown_content
        return report.markdown_report

    async def _plan_searches(self, query: str, variant: str) -> WebSearchPlan:
        planner = make_planner_agent(variant=variant, model=self.model)
        emit_trace(f"deep_research planner run variant={variant!r}")
        result = await Runner.run(planner, f"Query: {query}")
        plan = result.final_output_as(WebSearchPlan)
        logger.debug(f"Planned {len(plan.searches)} searches")
        return plan

    async def _perform_searches(
        self, search_plan: WebSearchPlan, variant: str
    ) -> tuple[list[str], list[str]]:
        """Execute all searches in parallel. Returns (results, queries_used)."""
        num_completed = 0
        emit_trace(f"deep_research parallel_search start count={len(search_plan.searches)} variant={variant!r}")
        tasks = [
            asyncio.create_task(self._search(item, variant))
            for item in search_plan.searches
        ]
        results: list[str] = []
        queries_used: list[str] = []

        for task in asyncio.as_completed(tasks):
            result, query_text = await task
            if result is not None:
                results.append(result)
                queries_used.append(query_text)
            num_completed += 1
            logger.debug(f"Search progress: {num_completed}/{len(tasks)}")
            emit_trace(f"deep_research parallel_search progress {num_completed}/{len(tasks)}")

        if not results:
            logger.warning("All searches returned empty results.")

        return results, queries_used

    async def _search(self, item: WebSearchItem, variant: str) -> tuple[Optional[str], str]:
        """Execute a single search. Returns (result_text_or_None, query_string)."""
        search_agent = make_search_agent(variant=variant, model=self.model)
        input_text = f"Search term: {item.query}\nReason for searching: {item.reason}"
        emit_trace(f"deep_research search query={item.query!r} variant={variant!r}")
        try:
            result = await Runner.run(search_agent, input_text)
            emit_trace(f"deep_research search done query={item.query!r}")
            return str(result.final_output), item.query
        except Exception as exc:
            logger.warning(f"Search failed for '{item.query}': {exc}")
            emit_trace(f"deep_research search error query={item.query!r}: {exc}")
            return None, item.query

    async def _write_report(
        self,
        query: str,
        search_results: list[str],
        variant: str,
    ) -> Union[ReportData, ArticleReportData]:
        """Write the final report using the writer agent."""
        writer = make_writer_agent(variant=variant, model=self.model)
        input_text = (
            f"Original query: {query}\n\n"
            f"Summarized search results:\n"
            + "\n\n---\n\n".join(search_results)
        )
        emit_trace(f"deep_research writer run variant={variant!r} inputs={len(search_results)}")
        result = await Runner.run(writer, input_text)

        # Select the correct output type based on variant
        if variant == "article":
            return result.final_output_as(ArticleReportData)
        return result.final_output_as(ReportData)
