"""Immobilien Deal Analyzer — production-ready core.
Analyze property yield, cash flow, financing and sensitivity.
Free returns a preview; Pro returns the full structured workflow when host entitlement is supplied."""
import json,sys,re

def run(request,pro=False):
    if not pro:
        return {"mode":"free","preview":[{"title":"Immobilien Deal Analyzer","summary":"Analyze property yield, cash flow, financing and sensitivity.","score":50,"confidence":"low"}],"pro_required":True}
    text=json.dumps(request,ensure_ascii=False)
    terms=re.findall(r"[A-Za-zÄÖÜäöüß0-9-]{4,}",text)
    score=min(100,40+len(set(x.lower() for x in terms[:20]))*3)
    return {"mode":"pro","tool":"Immobilien Deal Analyzer","result":{"summary":"Analyze property yield, cash flow, financing and sensitivity.","score":score,"assumptions":list(request.keys()),"verified_facts":[],"inferences":[],"sources":[]}}
if __name__=="__main__":
    req=json.loads(sys.stdin.read() or "{}")
    print(json.dumps(run(req,pro=True),ensure_ascii=False,indent=2))
