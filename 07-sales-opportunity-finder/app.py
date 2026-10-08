import json,sys
NAME="Sales Opportunity Finder"
def run(r,pro=False):
 if not isinstance(r,dict): raise ValueError("request must be an object")
 if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Provide companies/signals to rank likely near-term sales opportunities."},"pro_required":True}
 leads=r.get("opportunities",[])
 out=[]
 for x in leads if isinstance(leads,list) else []:
  if not isinstance(x,dict): continue
  score=sum([30 if x.get("need_signal") else 0,25 if x.get("budget_signal") else 0,20 if x.get("timing_signal") else 0,15 if x.get("fit") else 0,10 if x.get("evidence") else 0])
  out.append({"company":x.get("company","Unknown"),"score":score,"signal":x.get("signal"),"source":x.get("source")})
 return {"mode":"pro","tool":NAME,"result":{"ranking":sorted(out,key=lambda z:z["score"],reverse=True),"method":"Need 30 / budget 25 / timing 20 / fit 15 / evidence 10","next_actions":["Verify the signal date","Confirm decision-maker role","Personalize outreach to the evidenced trigger"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))