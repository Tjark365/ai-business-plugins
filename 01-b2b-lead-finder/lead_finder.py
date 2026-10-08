"""B2B Lead Finder core logic.

The core is intentionally provider-agnostic. A host can inject a web/search
provider and an entitlement checker without changing the scoring logic.
"""

from dataclasses import dataclass, asdict
from typing import Any, Callable, Iterable


@dataclass
class Lead:
    company: str
    location: str
    fit_rationale: str
    current_signal: str
    source: str
    buyer_role: str
    opportunity_value: str
    score: int
    confidence: str
    next_action: str
    verified_facts: list[str]
    inferences: list[str]


def score_lead(
    *,
    icp_fit: int,
    buying_signal: int,
    ability_to_pay: int,
    problem_fit: int,
    timing: int,
    evidence: int,
) -> int:
    """Score a lead from 0-100 using the documented weighting."""
    parts = {
        "icp_fit": (icp_fit, 30),
        "buying_signal": (buying_signal, 25),
        "ability_to_pay": (ability_to_pay, 15),
        "problem_fit": (problem_fit, 15),
        "timing": (timing, 10),
        "evidence": (evidence, 5),
    }

    total = 0
    for value, weight in parts.values():
        if not 0 <= value <= 100:
            raise ValueError("Each scoring input must be between 0 and 100.")
        total += round(value * weight / 100)

    return min(100, max(0, total))


def rank_leads(leads: Iterable[Lead]) -> list[Lead]:
    """Return strongest leads first."""
    return sorted(leads, key=lambda lead: lead.score, reverse=True)


def free_preview(leads: Iterable[Lead]) -> list[dict[str, Any]]:
    """Free tier: maximum three lightweight preview leads."""
    ranked = rank_leads(leads)[:3]
    return [
        {
            "company": lead.company,
            "location": lead.location,
            "fit_rationale": lead.fit_rationale,
            "score": lead.score,
            "confidence": lead.confidence,
            "source": lead.source,
        }
        for lead in ranked
    ]


def pro_results(leads: Iterable[Lead]) -> list[dict[str, Any]]:
    """Pro tier: complete ranked lead records."""
    return [asdict(lead) for lead in rank_leads(leads)]


def search_and_rank(
    *,
    offer: str,
    icp: str,
    geography: str | None = None,
    industry: str | None = None,
    company_size: str | None = None,
    exclusions: list[str] | None = None,
    lead_count: int = 10,
    search_provider: Callable[..., Iterable[dict[str, Any]]],
    is_pro: bool = False,
) -> list[dict[str, Any]]:
    """Run provider-backed research and return Free or Pro results.

    The provider must return evidence-backed candidate dictionaries. This
    function does not invent contacts, revenue, buying signals, or sources.
    """
    if not offer.strip() or not icp.strip():
        raise ValueError("offer and icp are required")
    if not 1 <= lead_count <= 100:
        raise ValueError("lead_count must be between 1 and 100")

    candidates = search_provider(
        offer=offer,
        icp=icp,
        geography=geography,
        industry=industry,
        company_size=company_size,
        exclusions=exclusions or [],
        lead_count=lead_count,
    )

    leads: list[Lead] = []
    for item in candidates:
        lead = Lead(
            company=str(item["company"]),
            location=str(item.get("location", "Unknown")),
            fit_rationale=str(item.get("fit_rationale", "")),
            current_signal=str(item.get("current_signal", "")),
            source=str(item["source"]),
            buyer_role=str(item.get("buyer_role", "Unknown")),
            opportunity_value=str(item.get("opportunity_value", "Unknown")),
            score=score_lead(
                icp_fit=int(item.get("icp_fit", 0)),
                buying_signal=int(item.get("buying_signal", 0)),
                ability_to_pay=int(item.get("ability_to_pay", 0)),
                problem_fit=int(item.get("problem_fit", 0)),
                timing=int(item.get("timing", 0)),
                evidence=int(item.get("evidence", 0)),
            ),
            confidence=str(item.get("confidence", "Low")),
            next_action=str(item.get("next_action", "")),
            verified_facts=list(item.get("verified_facts", [])),
            inferences=list(item.get("inferences", [])),
        )
        leads.append(lead)

    if is_pro:
        return pro_results(leads)

    return free_preview(leads)
