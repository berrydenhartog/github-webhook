import asyncio
import contextlib
import logging
import re
from collections.abc import Awaitable, Callable
from typing import Any

import jq
from fastapi import HTTPException, status

from .constants import FilterType, PermissionType
from .exporter import BaseExporter

logger = logging.getLogger(__name__)


def is_regex(value: str) -> bool:
    try:
        re.compile(value)
    except re.error:
        return False
    return True


def filter_event(filters: dict[PermissionType, list[dict[FilterType, Any]]], data: dict[str, Any]) -> bool:  # noqa: C901
    allow_filter = filters.get("ALLOW", [])
    deny_filter = filters.get("DENY", [])

    for filter in allow_filter:
        jq_filter = filter.get("FILTER")
        value = filter.get("VALUE")
        with contextlib.suppress(Exception):
            result = jq.compile(jq_filter).input(data).first()  # type: ignore
            if isinstance(value, str) and is_regex(value):
                if re.match(rf"{value}", result):  # type: ignore
                    return False
            else:
                if result == value:
                    return False

    for filter in deny_filter:
        jq_filter = filter.get("FILTER")
        value = filter.get("VALUE")
        with contextlib.suppress(Exception):
            result = jq.compile(jq_filter).input(data).first()  # type: ignore
            if isinstance(value, str) and is_regex(value):
                if re.match(value, result):  # type: ignore
                    return True
            else:
                if result == value:
                    return True

    return False


async def handle_filter_event_type(event_type: str, filters: dict[PermissionType, list[str]]) -> bool:
    allow_filter = filters.get("ALLOW", [])
    deny_filter = filters.get("DENY", [])

    if event_type in allow_filter:
        return False

    if len(allow_filter) > 0:
        return True

    return event_type in deny_filter


async def handle_filter_event(
    event_type: str,
    filters: dict[PermissionType, list[dict[FilterType, int | str | bool | float]]],
    data: dict[str, str | object],
) -> bool:
    return filter_event(filters, data)


async def handle_format_event(event_type: str, event_formats: dict[str, str], data: dict[str, str | object]) -> str:
    template = event_formats.get(event_type)

    logger.debug(f"Event {event_type} template: {template}")

    try:
        msg = template.format(**data) if template else str(data)
    except KeyError as e:
        logger.warning(f"Missing data for event {event_type}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing data for event {event_type}: {e}"
        ) from e

    return msg


async def handle_generic_event(event_type: str, exporters: list[BaseExporter], data: str) -> None:
    logger.debug(f"Event {event_type} parsed mesage: {data}")

    tasks = [exporter.handle_event(event_type, data) for exporter in exporters]
    await asyncio.gather(*tasks)


async def handle_unknown_event(event: str, exporters: list[BaseExporter], data: str) -> None:
    logger.warning(f"Unknown event {event}: {data}")

    await handle_generic_event(event, exporters, data)


DEFAULT_EVENT_HANDLERS: dict[str, Callable[[str, list[BaseExporter], str], Awaitable[None]]] = {
    "branch_protection_configuration": handle_generic_event,
    "branch_protection_rule": handle_generic_event,
    "check_run": handle_generic_event,
    "check_suite": handle_generic_event,
    "code_scanning_alert": handle_generic_event,
    "commit_comment": handle_generic_event,
    "create": handle_generic_event,
    "custom_property": handle_generic_event,
    "custom_property_values": handle_generic_event,
    "delete": handle_generic_event,
    "dependabot_alert": handle_generic_event,
    "deploy_key": handle_generic_event,
    "deployment": handle_generic_event,
    "deployment_protection_rule": handle_generic_event,
    "deployment_review": handle_generic_event,
    "deployment_status": handle_generic_event,
    "discussion": handle_generic_event,
    "discussion_comment": handle_generic_event,
    "fork": handle_generic_event,
    "github_app_authorization": handle_generic_event,
    "gollum": handle_generic_event,
    "installation": handle_generic_event,
    "installation_repositories": handle_generic_event,
    "installation_target": handle_generic_event,
    "issue_comment": handle_generic_event,
    "issues": handle_generic_event,
    "label": handle_generic_event,
    "marketplace_purchase": handle_generic_event,
    "member": handle_generic_event,
    "membership": handle_generic_event,
    "merge_group": handle_generic_event,
    "meta": handle_generic_event,
    "milestone": handle_generic_event,
    "org_block": handle_generic_event,
    "organization": handle_generic_event,
    "package": handle_generic_event,
    "page_build": handle_generic_event,
    "personal_access_token_request": handle_generic_event,
    "ping": handle_generic_event,
    "project_card": handle_generic_event,
    "project": handle_generic_event,
    "project_column": handle_generic_event,
    "projects_v2": handle_generic_event,
    "projects_v2_item": handle_generic_event,
    "projects_v2_status_update": handle_generic_event,
    "public": handle_generic_event,
    "pull_request": handle_generic_event,
    "pull_request_review_comment": handle_generic_event,
    "pull_request_review": handle_generic_event,
    "pull_request_review_thread": handle_generic_event,
    "push": handle_generic_event,
    "registry_package": handle_generic_event,
    "release": handle_generic_event,
    "repository_advisory": handle_generic_event,
    "repository": handle_generic_event,
    "repository_dispatch": handle_generic_event,
    "repository_import": handle_generic_event,
    "repository_ruleset": handle_generic_event,
    "repository_vulnerability_alert": handle_generic_event,
    "secret_scanning_alert": handle_generic_event,
    "secret_scanning_alert_location": handle_generic_event,
    "security_advisory": handle_generic_event,
    "security_and_analysis": handle_generic_event,
    "sponsorship": handle_generic_event,
    "star": handle_generic_event,
    "status": handle_generic_event,
    "sub_issues": handle_generic_event,
    "team_add": handle_generic_event,
    "team": handle_generic_event,
    "watch": handle_generic_event,
    "workflow_dispatch": handle_generic_event,
    "workflow_job": handle_generic_event,
    "workflow_run": handle_generic_event,
}
