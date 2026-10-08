import json,sys
NAME="Immobilien Deal Analyzer"
def n(r,k): 
    try:return float(r.get(k,0))
    except:return 0
def run(r,pro=False):
    if not isinstance(r,dict): raise ValueError("request must be an object")
    if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Enter purchase price, rent, costs, equity and financing terms."},"pro_required":True}
    price=n(r,"purchase_price"); rent=n(r,"annual_rent"); op=n(r,"annual_operating_costs"); equity=n(r,"equity"); loan=n(r,"loan_amount"); rate=n(r,"interest_rate_pct")
    noi=rent-op; gross=rent/price*100 if price else None; net=noi/price*100 if price else None; interest=loan*rate/100
    cashflow=noi-interest
    coc=cashflow/equity*100 if equity else None
    return {"mode":"pro","tool":NAME,"result":{"noi":round(noi,2),"gross_yield_pct":round(gross,2) if gross is not None else None,"net_yield_pct":round(net,2) if net is not None else None,"annual_interest":round(interest,2),"pre_tax_cashflow":round(cashflow,2),"cash_on_cash_pct":round(coc,2) if coc is not None else None,"sensitivity":{"interest_rate_plus_1pp_cashflow":round(noi-loan*(rate+1)/100,2)},"next_actions":["Add vacancy, maintenance, taxes and transaction costs","Stress-test rent and financing","Verify all property and financing assumptions"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))