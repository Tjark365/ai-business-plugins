"""03-funding-finder structured plugin core."""
import json,sys
NAME="03-funding-finder"; DESC="Match projects to current non-repayable grants using official primary sources and explicit eligibility checks."
def run(request,pro=False):
    if not isinstance(request,dict): raise ValueError("request must be an object")
    if len(json.dumps(request,ensure_ascii=False))>50000: raise ValueError("request too large")
    if not pro: return {"mode":"free","tool":NAME,"preview":{"summary":DESC,"score":50,"confidence":"low"},"pro_required":True}
    t=json.dumps(request,ensure_ascii=False).lower()
    signals=("budget","deadline","funding","growth","hiring","expansion","procurement","investment","acquisition","risk","revenue","cost")
    score=min(100,35+4*sum(s in t for s in signals))
    return {"mode":"pro","tool":NAME,"result":{"summary":DESC,"score":score,"confidence":"medium","verified_facts":[],"inferences":["Preliminary score; external evidence must be validated before decisions."],"sources":[],"assumptions":list(request),"next_actions":["Collect primary-source evidence","Validate key assumptions","Rank by fit, evidence and timing"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False,indent=2))
