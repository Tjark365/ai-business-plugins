import json,sys
NAME="Unity Game Generator"
def run(r,pro=False):
    if not isinstance(r,dict): raise ValueError("request must be an object")
    if not pro:return {"mode":"free","tool":NAME,"preview":{"message":"Describe the game genre, core loop, platform and visual style."},"pro_required":True}
    idea=str(r.get("idea","")).strip() or "Arcade prototype"
    genre=r.get("genre","unspecified"); platform=r.get("platform","PC")
    return {"mode":"pro","tool":NAME,"result":{"game_concept":{"title":r.get("title","Generated Prototype"),"genre":genre,"platform":platform,"core_loop":idea},"scene_plan":[{"scene":"Bootstrap","purpose":"Initialize systems"},{"scene":"MainMenu","purpose":"Start/options"},{"scene":"Game","purpose":"Core gameplay"},{"scene":"Results","purpose":"Score/progression"}],"scripts":["GameManager.cs","PlayerController.cs","UIManager.cs","SaveSystem.cs"],"build_checklist":["Create Unity project","Add scenes in Build Settings","Implement input and gameplay loop","Add error handling and save/load","Test target platform build"],"note":"Generated code should be reviewed and tested inside the target Unity version."}}
if __name__=="__main__": print(json.dumps(run(json.loads(sys.stdin.read() or "{}"),True),ensure_ascii=False,indent=2))