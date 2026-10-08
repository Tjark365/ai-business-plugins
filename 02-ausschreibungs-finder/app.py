import os,re,json,sys
from dataclasses import dataclass,asdict
@dataclass
class Result:
 title:str; summary:str; score:int; confidence:str="medium"; source:str=""
def analyze(request,pro=False):
 if not pro:return {"mode":"free","message":"Pro workflow requires host entitlement.","preview":[{"title":"Preview","summary":"Define target, constraints and evidence needed for a full run.","score":50,"confidence":"low","source":""}]}
 text=json.dumps(request,ensure_ascii=False); words=re.findall(r"[A-Za-zÄÖÜäöüß0-9-]{4,}",text); score=min(100,35+len(set(w.lower() for w in words[:15]))*3)
 return {"mode":"pro","results":[asdict(Result("Ausschreibungs Finder","Find and rank relevant public tenders by fit, deadline and buyer.",score))]}
if __name__=="__main__": print(json.dumps(analyze(json.loads(sys.stdin.read() or "{}"),os.getenv("PRO")=="1"),ensure_ascii=False,indent=2))
