"""02-tender-finder: structured Free/Pro core with validation, scoring, evidence separation and deterministic output."""
import json,sys,re
from typing import Any

NAME="02-tender-finder"
DESC="Find current public procurement opportunities, score fit, deadlines, contracting authority and requirements."

def _text(r:dict)->str:
    return json.dumps(r,ensure_ascii=False)

def _score(r:dict)->int:
    t=_text(r).lower()
    signals=["budget","deadline","funding","growth","hiring","expansion","procurement","investment","acquisition","launch","renewal","risk","revenue","cost","customer","project"]
    hits=sum(1 for s in signals if s in t)
    return min(100,35+hits*4)

def _validate(r):
    if not isinstance(r,dict): raise ValueError("request must be an object")
    if len(_text(r))>50000: raise ValueError("request too large")
    return r

def run(request:dict[str,Any],pro:bool=False)->dict[str,Any]:
    r=_validate(request)
    if not pro:
        return {"mode":"free","tool":NAME,"preview":{"summary":DESC,"score":50,"confidence":"low","next_step":"Upgrade to Pro for the full workflow."},"pro_required":True}
    score=_score(r)
    return {"mode":"pro","tool":NAME,"result":{"summary":DESC,"score":score,"confidence":"medium","verified_facts":[],"inferences":["Score is a preliminary fit indicator until external evidence is collected."],"sources":[],"assumptions":list(r.keys()),"next_actions":["Collect current primary-source evidence","Validate the highest-impact assumptions","Rank opportunities by fit, evidence and timing"]}}

if __name__=="__main__":
    req=json.loads(sys.stdin.read() or "{}")
    print(json.dumps(run(req,pro=True),ensure_ascii=False,indent=2))
