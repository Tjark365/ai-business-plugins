import json,sys
NAME="Price Optimizer"
def n(r,k): 
    try:return float(r.get(k,0))
    except:return 0
def run(r,pro=False):
    if not isinstance(r,dict): raise ValueError("request must be an object")
    if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Enter current price, unit cost, volume and target margin."},"pro_required":True}
    price=n(r,"current_price"); cost=n(r,"unit_cost"); volume=n(r,"volume"); target=n(r,"target_margin_pct")
    margin=(price-cost)/price*100 if price else None
    target_price=cost/(1-target/100) if target<100 else None
    tests=[round(price*x,2) for x in [.9,.95,1.05,1.1]] if price else []
    return {"mode":"pro","tool":NAME,"result":{"current_margin_pct":round(margin,2) if margin is not None else None,"target_price":round(target_price,2) if target_price else None,"test_prices":tests,"contribution_at_test_prices":[{"price":p,"unit_contribution":round(p-cost,2)} for p in tests],"warning":"Optimal pricing requires demand/elasticity evidence; this calculator does not infer willingness to pay.","next_actions":["Test a small price change","Measure conversion and contribution, not revenue alone","Segment prices only where customer value differs"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))