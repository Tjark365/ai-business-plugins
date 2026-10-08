import json,sys
NAME="Procurement Comparer"
def run(r,pro=False):
    if not isinstance(r,dict): raise ValueError("request must be an object")
    if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Add vendors with price, quality, delivery, risk and contract terms."},"pro_required":True}
    vendors=r.get("vendors",[])
    if not isinstance(vendors,list): raise ValueError("vendors must be a list")
    weights=r.get("weights",{"cost":.35,"quality":.25,"delivery":.15,"risk":.15,"terms":.10})
    out=[]
    for v in vendors:
        if not isinstance(v,dict): continue
        def g(k): 
            try:return float(v.get(k,0))
            except:return 0
        cost=g("cost"); quality=g("quality"); delivery=g("delivery"); risk=g("risk"); terms=g("terms")
        total=(1/(1+cost) if cost>=0 else 0)*weights.get("cost",.35)*100+quality*weights.get("quality",.25)+delivery*weights.get("delivery",.15)+risk*weights.get("risk",.15)+terms*weights.get("terms",.10)
        out.append({"vendor":v.get("name","Unknown"),"score":round(total,2),"cost":cost})
    out.sort(key=lambda x:x["score"],reverse=True)
    return {"mode":"pro","tool":NAME,"result":{"ranking":out,"scoring_note":"Quality/delivery/risk/terms are expected on a 0-100 scale; cost is normalized, so verify the weighting before a purchase decision.","next_actions":["Validate references and SLA","Compare total cost of ownership","Review termination, warranty and liability clauses"]}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))