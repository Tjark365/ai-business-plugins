import json,sys
NAME="M&A Deal Finder"
def run(r,pro=False):
 if not isinstance(r,dict): raise ValueError("request must be an object")
 if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Enter target industry, geography, size, deal type and strategic rationale."},"pro_required":True}
 deals=r.get("deals",[])
 if not isinstance(deals,list): raise ValueError("deals must be a list")
 out=[]
 for d in deals:
  if not isinstance(d,dict): continue
  score=sum([25 if d.get("industry_fit") else 0,20 if d.get("size_fit") else 0,20 if d.get("geography_fit") else 0,20 if d.get("strategic_fit") else 0,15 if d.get("evidence") else 0])
  out.append({"target":d.get("target","Unknown"),"score":score,"deal_type":d.get("deal_type"),"source":d.get("source"),"status":d.get("status")})
 out.sort(key=lambda x:x["score"],reverse=True)
 return {"mode":"pro","tool":NAME,"result":{"ranking":out,"method":"Industry 25 / size 20 / geography 20 / strategic fit 20 / evidence 15","next_actions":["Verify transaction status","Check ownership and financial evidence","Prepare valuation and outreach rationale"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))