"""Live web-search adapters.

Configure one provider with an environment variable:
- SERPER_API_KEY for Google results through Serper
- BRAVE_API_KEY for Brave Search

No key is bundled in the repository.
"""

import os
from typing import Any
import requests


class SearchProviderError(RuntimeError):
    pass


def _serper(query: str, num: int = 10) -> list[dict[str, Any]]:
    key = os.getenv("SERPER_API_KEY")
    if not key:
        raise SearchProviderError("SERPER_API_KEY is not configured")

    response = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": key, "Content-Type": "application/json"},
        json={"q": query, "num": min(num, 100)},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    return [
        {
            "title": item.get("title", ""),
            "url": item.get("link", ""),
            "snippet": item.get("snippet", ""),
        }
        for item in data.get("organic", [])
    ]


def _brave(query: str, num: int = 10) -> list[dict[str, Any]]:
    key = os.getenv("BRAVE_API_KEY")
    if not key:
        raise SearchProviderError("BRAVE_API_KEY is not configured")

    response = requests.get(
        "https://api.search.brave.com/res/v1/web/search",
        headers={"X-Subscription-Token": key, "Accept": "application/json"},
        params={"q": query, "count": min(num, 20)},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "snippet": item.get("description", ""),
        }
        for item in data.get("web", {}).get("results", [])
    ]


def web_search(query: str, num: int = 10) -> list[dict[str, Any]]:
    """Use configured live search provider."""
    if os.getenv("SERPER_API_KEY"):
        return _serper(query, num)
    if os.getenv("BRAVE_API_KEY"):
        return _brave(query, num)
    raise SearchProviderError(
        "No live search provider configured. Set SERPER_API_KEY or BRAVE_API_KEY."
    )


def build_queries(*, offer: str, icp: str, geography: str | None,
                  industry: str | None, company_size: str | None) -> list[str]:
    parts = [icp, offer]
    if geography:
        parts.append(geography)
    if industry:
        parts.append(industry)
    if company_size:
        parts.append(company_size)
    base = " ".join(parts)
    return [
        f'"{base}" companies',
        f'"{base}" expansion OR hiring OR funding',
        f'"{base}" partnership OR procurement OR investment',
    ]


def live_candidates(*, offer: str, icp: str, geography: str | None = None,
                    industry: str | None = None,
                    company_size: str | None = None,
                    exclusions: list[str] | None = None,
                    lead_count: int = 10) -> list[dict[str, Any]]:
    """Collect sourced search evidence for the scoring engine.

    This intentionally does not invent scores. A production host/model should
    evaluate the returned evidence and provide the six score components.
    """
    exclusions = exclusions or []
    results: list[dict[str, Any]] = []
    seen: set[str] = set()

    for query in build_queries(
        offer=offer, icp=icp, geography=geography,
        industry=industry, company_size=company_size
    ):
        for item in web_search(query, num=max(10, lead_count * 2)):
            url = item["url"]
            text = f'{item["title"]} {item["snippet"]}'.lower()
            if not url or url in seen:
                continue
            if any(ex.lower() in text for ex in exclusions):
                continue
            seen.add(url)
            results.append({
                "company": item["title"],
                "location": geography or "Unknown",
                "fit_rationale": item["snippet"],
                "current_signal": item["snippet"],
                "source": url,
                "buyer_role": "To be researched",
                "opportunity_value": "To be estimated",
                "confidence": "Research required",
                "next_action": "Verify company fit and current buying signal",
                "verified_facts": [item["snippet"]],
                "inferences": [],
                "icp_fit": 0,
                "buying_signal": 0,
                "ability_to_pay": 0,
                "problem_fit": 0,
                "timing": 0,
                "evidence": 50,
            })
            if len(results) >= lead_count:
                return results
    return results
