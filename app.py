import json,sys
NAME="Funding Finder"
def run(r,pro=False):
 if not isinstance(r,dict): raise ValueError("request must be an object")
 if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Enter project, location, applicant type, investment and funding need."},"pro_required":True}
 programs=r.get("programs",[])
 if not isinstance(programs,list): raise ValueError("programs must be a list")
 out=[]
 for p in programs:
  if not isinstance(p,dict): continue
  score=sum([30 if p.get("eligibility") else 0,25 if p.get("project_fit") else 0,20 if p.get("funding_rate") else 0,15 if p.get("timing") else 0,10 if p.get("official_source") else 0])
  out.append({"program":p.get("name","Unknown"),"score":score,"funding_rate":p.get("funding_rate"),"deadline":p.get("deadline"),"source":p.get("source")})
 out.sort(key=lambda x:x["score"],reverse=True)
 return {"mode":"pro","tool":NAME,"result":{"ranking":out,"method":"Eligibility 30 / project fit 25 / funding rate 20 / timing 15 / official source 10","next_actions":["Verify current call on the official programme page","Check state aid and applicant eligibility","Reconcile eligible costs with the call"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))