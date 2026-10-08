import json,sys
NAME="Funding Finder"
DESC="Match projects to current non-repayable grants using official sources and explicit eligibility checks."
def run(request,pro=False):
 if not isinstance(request,dict): raise ValueError("request must be an object")
 if not pro: return {"mode":"free","tool":NAME,"preview":{"summary":DESC,"score":50},"pro_required":True}
 t=json.dumps(request,ensure_ascii=False).lower(); sig=("budget","deadline","procurement","contract","authority","requirement","grant","funding","innovation","research","investment","sme","eligibility")
 return {"mode":"pro","tool":NAME,"result":{"summary":DESC,"score":min(100,35+5*sum(x in t for x in sig)),"verified_facts":[],"inferences":["Preliminary fit score; current primary-source evidence must be validated."],"sources":[],"next_actions":["Collect primary-source evidence","Check eligibility and deadline","Rank by fit, evidence and timing"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))
