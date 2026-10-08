import json,sys
NAME="Förderantrag Checker"
REQUIRED=["project_description","eligibility","budget","timeline","impact","evidence"]
def run(r,pro=False):
    if not isinstance(r,dict): raise ValueError("request must be an object")
    if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Paste your application data or checklist for a structured gap review."},"pro_required":True}
    missing=[k for k in REQUIRED if not r.get(k)]
    budget=r.get("budget",{})
    budget_ok=isinstance(budget,dict) and all(isinstance(v,(int,float)) and v>=0 for v in budget.values()) if budget else False
    score=max(0,100-len(missing)*12-(0 if budget_ok else 12))
    return {"mode":"pro","tool":NAME,"result":{"readiness_score":score,"missing_sections":missing,"budget_check":"pass" if budget_ok else "review required","risks":[f"Missing section: {x}" for x in missing]+([] if budget_ok else ["Budget structure missing or contains invalid values"]), "next_actions":["Map every claim to evidence","Reconcile budget totals with programme rules","Check eligibility against the current official call","Review scoring criteria before submission"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))