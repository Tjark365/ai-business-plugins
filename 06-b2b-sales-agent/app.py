import json,sys
NAME="B2B Sales Agent"
def run(r,pro=False):
 if not isinstance(r,dict): raise ValueError("request must be an object")
 if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Enter offer, ICP, sales cycle and common objections for a measurable playbook."},"pro_required":True}
 offer=r.get("offer",""); icp=r.get("icp",""); objections=r.get("objections",[])
 stages=[{"stage":"Qualification","goal":"Confirm problem, authority, budget and timing","metric":"qualified rate"},{"stage":"Discovery","goal":"Quantify impact and current process","metric":"discovery-to-proposal"},{"stage":"Proposal","goal":"Tie scope to measurable ROI","metric":"proposal-to-close"},{"stage":"Close","goal":"Resolve risk and agree next step","metric":"win rate"}]
 return {"mode":"pro","tool":NAME,"result":{"offer":offer,"icp":icp,"objection_handling":[{"objection":x,"response_framework":"Acknowledge → clarify → evidence → next step"} for x in objections],"stages":stages,"next_actions":["Define qualification thresholds","Track stage conversion","Use evidence-backed ROI claims only"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))