import os, subprocess
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687921332_2e58013d1c")
SRC = os.path.join(NEW, "learning-space/sources")
os.makedirs(SRC, exist_ok=True)
targets = [
    ("https://github.com/humanlayer/12-factor-agents.git", "12-factor-agents"),
    ("https://github.com/openai/openai-agents-python.git", "openai-agents-python"),
]
for url, name in targets:
    d = os.path.join(SRC, name)
    if os.path.isdir(d):
        print(name, "already exists"); continue
    try:
        p = subprocess.run(["git","clone","--depth","1",url,name], cwd=SRC,
                           capture_output=True, text=True, timeout=240)
        print(name, "rc:", p.returncode, "| err tail:", (p.stderr or "")[-200:].replace("\n"," "))
    except Exception as e:
        print(name, "EXC", type(e).__name__, str(e)[:150])

def du(p):
    total=0; files=0
    for dp,dn,fn in os.walk(p):
        if ".git" in dp: continue
        for f in fn:
            try: total+=os.path.getsize(os.path.join(dp,f)); files+=1
            except: pass
    return files, round(total/1024/1024,2)
for _, name in targets:
    d = os.path.join(SRC, name)
    if os.path.isdir(d):
        print(name, du(d), sorted(os.listdir(d))[:14])