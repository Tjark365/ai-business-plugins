"""HTTP API for the B2B Lead Finder."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from lead_finder import search_and_rank
from search_provider import live_candidates, SearchProviderError


app = FastAPI(title="B2B Lead Finder API", version="0.1.0")


class LeadRequest(BaseModel):
    offer: str
    icp: str
    geography: str | None = None
    industry: str | None = None
    company_size: str | None = None
    exclusions: list[str] = Field(default_factory=list)
    lead_count: int = Field(default=10, ge=1, le=50)
    pro: bool = False


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/leads")
def find_leads(request: LeadRequest):
    try:
        return {
            "mode": "pro" if request.pro else "free",
            "leads": search_and_rank(
                offer=request.offer,
                icp=request.icp,
                geography=request.geography,
                industry=request.industry,
                company_size=request.company_size,
                exclusions=request.exclusions,
                lead_count=request.lead_count,
                search_provider=live_candidates,
                is_pro=request.pro,
            ),
        }
    except SearchProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
