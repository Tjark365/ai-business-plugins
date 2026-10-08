import json,sys
NAME="Company Valuation"
def _n(r,k,d=0): 
    try:return float(r.get(k,d))
    except:return d
def run(request,pro=False):
    if not isinstance(request,dict): raise ValueError("request must be an object")
    if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Enter revenue, EBITDA, growth and net debt for a valuation range."},"pro_required":True}
    revenue=_n(request,"revenue"); ebitda=_n(request,"ebitda"); growth=_n(request,"growth_pct"); debt=_n(request,"net_debt"); multiple=_n(request,"ebitda_multiple",7)
    methods={}
    if ebitda>0: methods["ebitda_multiple"]=ebitda*multiple-debt
    if revenue>0: methods["revenue_multiple"]=revenue*_n(request,"revenue_multiple",1.5)-debt
    if revenue>0 and growth>-100: methods["growth_adjusted"]=revenue*max(.25,min(5,1+growth/100*2))-debt
    vals=[v for v in methods.values() if v>=0]
    return {"mode":"pro","tool":NAME,"result":{"valuation_range":([round(min(vals),2),round(max(vals),2)] if vals else None),"methods":{k:round(v,2) for k,v in methods.items()},"inputs":{"revenue":revenue,"ebitda":ebitda,"growth_pct":growth,"net_debt":debt},"assumptions":["Multiples are user-supplied or illustrative, not market quotes."],"confidence":"medium" if vals else "low","next_actions":["Replace illustrative multiples with current comparable-company evidence","Run downside/base/upside scenarios"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))