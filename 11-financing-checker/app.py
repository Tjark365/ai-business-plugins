import json,sys
NAME="Financing Checker"
def n(r,k): 
    try:return float(r.get(k,0))
    except:return 0
def run(r,pro=False):
    if not isinstance(r,dict): raise ValueError("request must be an object")
    if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Enter funding need, revenue, EBITDA, collateral and repayment capacity."},"pro_required":True}
    need=n(r,"funding_need"); rev=n(r,"revenue"); ebitda=n(r,"ebitda"); debt=n(r,"existing_debt"); cash=n(r,"cash")
    paths=[]
    if ebitda>0: paths.append(("bank_debt","Stronger fit when recurring cash flow supports debt service"))
    if need>0 and need<=500000: paths.append(("working_capital","Potential fit for smaller liquidity needs"))
    if need>0 and r.get("innovation"): paths.append(("grant_or_innovation_funding","Potential non-dilutive route; eligibility must be verified"))
    if r.get("equity"): paths.append(("equity","Potential fit when repayment capacity is limited"))
    readiness=0
    readiness+=25 if rev>0 else 0; readiness+=25 if ebitda>0 else 0; readiness+=15 if cash>0 else 0; readiness+=15 if debt>=0 else 0; readiness+=20 if need>0 else 0
    return {"mode":"pro","tool":NAME,"result":{"readiness_score":readiness,"funding_need":need,"existing_debt":debt,"candidate_paths":[{"type":a,"fit":b} for a,b in paths],"required_evidence":["Recent financial statements","Cash-flow forecast","Debt schedule","Use of funds","Collateral/equity information where relevant"],"warning":"This is a readiness assessment, not a financing approval."}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False))