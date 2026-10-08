import json,sys
NAME="B2B Outreach Agent"
def run(r,pro=False):
 if not isinstance(r,dict): raise ValueError("request must be an object")
 if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Provide offer, prospect evidence and desired CTA for a personalized sequence."},"pro_required":True}
 prospects=r.get("prospects",[])
 out=[]
 for p in prospects if isinstance(prospects,list) else []:
  if not isinstance(p,dict): continue
  evidence=p.get("evidence") or p.get("signal") or "No verified signal supplied"
  out.append({"company":p.get("company","Unknown"),"evidence":evidence,"message_framework":["Relevant observed signal","Specific problem hypothesis","Credible proof/value","Low-friction CTA"],"cta":r.get("cta","15-minute fit check")})
 return {"mode":"pro","tool":NAME,"result":{"personalized_frameworks":out,"guardrails":["Do not invent facts","Respect opt-outs and applicable marketing rules","Keep volume controlled and relevant"],"next_actions":["Verify every personalization fact","Send only to appropriate business contacts","Measure positive replies and meetings, not raw volume"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))