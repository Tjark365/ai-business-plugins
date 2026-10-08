import json,sys
NAME="Tender Finder"
def run(r,pro=False):
 if not isinstance(r,dict): raise ValueError("request must be an object")
 if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Enter sector, geography, CPV/category, contract size and deadline preferences."},"pro_required":True}
 tenders=r.get("tenders",[])
 if not isinstance(tenders,list): raise ValueError("tenders must be a list")
 out=[]
 for t in tenders:
  if not isinstance(t,dict): continue
  score=0
  score+=30 if t.get("sector_fit") else 0; score+=25 if t.get("geography_fit") else 0; score+=20 if t.get("requirements_fit") else 0; score+=15 if t.get("budget_fit") else 0; score+=10 if t.get("deadline") else 0
  out.append({"title":t.get("title","Unknown"),"score":score,"deadline":t.get("deadline"),"buyer":t.get("buyer"),"source":t.get("source")})
 out.sort(key=lambda x:x["score"],reverse=True)
 return {"mode":"pro","tool":NAME,"result":{"ranking":out,"method":"Sector 30 / geography 25 / requirements 20 / budget 15 / deadline evidence 10","next_actions":["Verify the official notice","Check mandatory requirements","Confirm deadline and submission route"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))