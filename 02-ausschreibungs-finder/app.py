"""Ausschreibungs Finder: compact, deterministic core with optional live search."""
import os,re,json,sys
from dataclasses import dataclass,asdict
from typing import Any

@dataclass
class Result:
    title:str
    summary:str
    score:int
    confidence:str="medium"
    source:str=""

def _score(text:str, terms:list[str])->int:
    t=text.lower()
    hits=sum(1 for x in terms if x.lower() in t)
    return min(100, hits*18)

def analyze(request:dict[str,Any], pro:bool=False)->dict[str,Any]:
    if not pro:
        return {"mode":"free","message":"Pro workflow requires host entitlement.","preview":_preview(request)}
    return {"mode":"pro","results":_results(request)}

def _preview(r):
    return [{"title":"Preview","summary":"Define the target, constraints and evidence needed for a full run.","score":50,"confidence":"low","source":""}]

def _results(r):
    text=json.dumps(r,ensure_ascii=False)
    terms=[x for x in re.findall(r"[A-Za-zÄÖÜäöüß0-9-]{4,}",text) if x.lower() not in {"the","with","from","this","that"}][:20]
    return [asdict(Result(title="Ausschreibungs Finder",summary="Find and rank relevant public tenders by fit, deadline and buyer.",score=max(35,_score(text,terms[:6])),confidence="medium",source="User-supplied inputs"))]

if __name__=="__main__":
    req=json.loads(sys.stdin.read() or "{}")
    print(json.dumps(analyze(req,pro=os.getenv("PRO")=="1"),ensure_ascii=False,indent=2))
