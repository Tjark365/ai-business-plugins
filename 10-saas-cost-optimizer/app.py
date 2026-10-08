import json,sys
NAME="SaaS Cost Optimizer"
def run(r,pro=False):
    if not isinstance(r,dict): raise ValueError("request must be an object")
    if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Provide software subscriptions with cost, seats and active users."},"pro_required":True}
    subs=r.get("subscriptions",[])
    if not isinstance(subs,list): raise ValueError("subscriptions must be a list")
    rows=[]; savings=0
    for x in subs:
        if not isinstance(x,dict): continue
        cost=float(x.get("monthly_cost",0) or 0); seats=float(x.get("seats",0) or 0); active=float(x.get("active_users",0) or 0)
        unused=max(0,seats-active); est=cost*(unused/seats) if seats else 0
        rows.append({"name":x.get("name","Unknown"),"monthly_cost":cost,"unused_seats":unused,"estimated_reclaimable":round(est,2)})
        savings+=est
    return {"mode":"pro","tool":NAME,"result":{"subscriptions":rows,"estimated_monthly_reclaimable":round(savings,2),"estimated_annual_reclaimable":round(savings*12,2),"assumptions":["Unused-seat savings are estimates; contracts and minimums must be checked."],"next_actions":["Cancel duplicate tools","Right-size seats at renewal","Negotiate based on actual utilization"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))