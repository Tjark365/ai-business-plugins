import json,sys
NAME="Due-Diligence Analyzer"
AREAS=["commercial","financial","operational","legal","technology","people"]
def run(r,pro=False):
 if not isinstance(r,dict): raise ValueError("request must be an object")
 if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Provide company facts or diligence findings for a structured risk review."},"pro_required":True}
 findings=r.get("findings",{})
 if not isinstance(findings,dict): findings={}
 out={}
 for a in AREAS:
  x=findings.get(a,{}) or {}; status=x.get("status","unknown"); issues=x.get("issues",[])
  out[a]={"status":status,"issues":issues,"priority":"high" if status in ("red","critical") or issues else "review"}
 high=sum(1 for x in out.values() if x["priority"]=="high")
 return {"mode":"pro","tool":NAME,"result":{"areas":out,"high_priority_areas":high,"red_flags":[{"area":a,"issues":x["issues"]} for a,x in out.items() if x["priority"]=="high"],"next_actions":["Request primary documents for every material issue","Validate management claims independently","Escalate legal/accounting issues to qualified professionals"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))