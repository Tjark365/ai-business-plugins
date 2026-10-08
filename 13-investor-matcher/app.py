import json,sys
NAME="Investor Matcher"
def run(r,pro=False):
 if not isinstance(r,dict): raise ValueError("request must be an object")
 if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Provide stage, sector, geography, round size and investor candidates."},"pro_required":True}
 inv=r.get("investors",[])
 out=[]
 for x in inv if isinstance(inv,list) else []:
  if not isinstance(x,dict): continue
  score=sum([25 if x.get("stage_fit") else 0,25 if x.get("sector_fit") else 0,20 if x.get("ticket_fit") else 0,15 if x.get("geography_fit") else 0,15 if x.get("thesis_evidence") else 0])
  out.append({"investor":x.get("name","Unknown"),"score":score,"thesis":x.get("thesis"),"source":x.get("source")})
 out.sort(key=lambda z:z["score"],reverse=True)
 return {"mode":"pro","tool":NAME,"result":{"ranking":out,"method":"Stage 25 / sector 25 / ticket 20 / geography 15 / current thesis evidence 15","next_actions":["Verify current investment thesis","Check portfolio conflicts","Prepare a tailored investment rationale"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))