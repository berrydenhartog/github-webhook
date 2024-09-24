import logging
from typing import Any

import httpx
from pydantic.networks import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from .baseenricher import BaseEnricher

logger = logging.getLogger(__name__)


class GithubenricherSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_file="github.env", yaml_file="github.yaml", env_prefix="GITHUB_"
    )

    TOKEN: str
    GRAPH_API: HttpUrl = "https://api.github.com/graphql"  # type: ignore


class GithubEnricher(BaseEnricher):
    def __init__(self, retries: int = 5, timeout: int = 1) -> None:
        self.settings = GithubenricherSettings()  # type: ignore
        self.transport = httpx.AsyncHTTPTransport(retries=retries)
        self.client = httpx.AsyncClient(transport=self.transport, timeout=timeout)

    async def handle_event(self, event: str, data: dict[str, Any]) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.settings.TOKEN}"}

        if event == "projects_v2_item":
            node_id = data["projects_v2_item"]["node_id"]
            query: str = """
                query ($id: ID!) {
                    node(id: $id) {
                        ... on ProjectV2Item{
                            type
                            content {
                                ... on Issue{
                                    title
                                }
                                ... on DraftIssue {
                                    title
                                }
                            }
                            project {
                                title
                            }
                        }
                    }
                }"""
            result = await self.client.post(
                str(self.settings.GRAPH_API), json={"query": query, "variables": {"id": node_id}}, headers=headers
            )

            if result.status_code != 200:
                logger.error(f"Failed to fetch data from Github: {result.status_code}")
                return data

            response = result.json()

            github_enricher: dict[str, object] = {
                "github_enricher": {
                    "project_title": response["data"]["node"]["project"]["title"],
                    "issue_title": response["data"]["node"]["content"]["title"],
                }
            }

            data.update(github_enricher)
        return data
