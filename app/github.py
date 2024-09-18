import logging
from collections.abc import Awaitable, Callable

from fastapi import HTTPException, status

from .clients import BaseClient
from .contants import DEFAULT_EVENT_DESCRIPTIONS

logger = logging.getLogger(__name__)


async def handle_generic_event(event: str, client: BaseClient, data: dict[str, str | object]) -> None:
    template = DEFAULT_EVENT_DESCRIPTIONS.get(event)

    logger.debug(f"Event {event} template: {template}")

    if not template:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unknown event type {event}")

    try:
        msg = template.format(**data)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing data for event {event}: {e}"
        ) from e

    logger.debug(f"Event {event} parsed mesage: {msg}")

    await client.handle_event(event, msg)


async def handle_unknown_event(event: str, _client: BaseClient, data: dict[str, str | object]) -> None:
    logger.warning(f"Unknown event {event}: {data}")


DEFAULT_EVENT_HANDLERS: dict[str, Callable[[str, BaseClient, dict[str, str | object]], Awaitable[None]]] = {
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
