import json,sys
NAME="Competitive Intelligence"
def run(r,pro=False):
 if not isinstance(r,dict): raise ValueError("request must be an object")
 if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Add competitor evidence for positioning, pricing, offers and strategic gaps."},"pro_required":True}
 comps=r.get("competitors",[])
 out=[]
 for c in comps if isinstance(comps,list) else []:
  if not isinstance(c,dict): continue
  strengths=c.get("strengths",[]); weaknesses=c.get("weaknesses",[])
  out.append({"competitor":c.get("name","Unknown"),"price":c.get("price"),"positioning":c.get("positioning"),"strength_count":len(strengths),"weakness_count":len(weaknesses),"source":c.get("source")})
 return {"mode":"pro","tool":NAME,"result":{"competitors":out,"gap_candidates":[x["competitor"] for x in out if x["weakness_count"]>x["strength_count"]],"next_actions":["Verify pricing and offer dates","Separate observed facts from interpretation","Test differentiated positioning with customers"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))