import json,sys
NAME="Cashflow Optimizer"
def n(r,k): 
    try:return float(r.get(k,0))
    except:return 0
def run(r,pro=False):
    if not isinstance(r,dict): raise ValueError("request must be an object")
    if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Enter receivables, payables, inventory, monthly burn and cash."},"pro_required":True}
    cash=n(r,"cash"); ar=n(r,"accounts_receivable"); ap=n(r,"accounts_payable"); inv=n(r,"inventory"); burn=n(r,"monthly_burn")
    dso=n(r,"dso_days"); dpo=n(r,"dpo_days"); invdays=n(r,"inventory_days")
    recommendations=[]
    if ar>0: recommendations.append({"action":"Accelerate receivables","potential_cash":round(ar*.10,2),"logic":"10% collection acceleration scenario"})
    if ap>0: recommendations.append({"action":"Optimize payment terms","potential_cash":round(ap*.10,2),"logic":"10% timing scenario"})
    if inv>0: recommendations.append({"action":"Reduce excess inventory","potential_cash":round(inv*.10,2),"logic":"10% inventory-release scenario"})
    runway=round(cash/burn,1) if burn>0 else None
    return {"mode":"pro","tool":NAME,"result":{"cash_runway_months":runway,"working_capital":{"receivables":ar,"payables":ap,"inventory":inv},"cycle_inputs":{"dso_days":dso,"dpo_days":dpo,"inventory_days":invdays},"recommendations":recommendations,"note":"Potential cash figures are scenarios, not guaranteed savings.","next_actions":["Validate customer collection history","Review supplier terms","Identify slow-moving inventory"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))