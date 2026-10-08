import json,sys
NAME="SEO Opportunity Finder"
def run(r,pro=False):
 if not isinstance(r,dict): raise ValueError("request must be an object")
 if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Provide keywords, pages and competitor observations to rank SEO opportunities."},"pro_required":True}
 kws=r.get("keywords",[])
 out=[]
 for k in kws if isinstance(kws,list) else []:
  if not isinstance(k,dict): continue
  vol=float(k.get("volume",0) or 0); diff=float(k.get("difficulty",100) or 100); intent=k.get("intent","unknown")
  score=round(max(0,min(100,(vol**0.5)*5 + max(0,100-diff)*.5 + (15 if intent in ("commercial","transactional") else 0))),2)
  out.append({"keyword":k.get("keyword",""),"opportunity_score":score,"volume":vol,"difficulty":diff,"intent":intent,"source":k.get("source")})
 out.sort(key=lambda x:x["opportunity_score"],reverse=True)
 return {"mode":"pro","tool":NAME,"result":{"ranking":out,"formula":"Demand signal + inverse difficulty + commercial intent bonus","next_actions":["Validate search intent manually","Check SERP competitors","Create the page only where topical authority and business value justify it"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))