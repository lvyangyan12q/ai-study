import os
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791696096980_527b333145")
R = os.path.join(NEW, "learning-space/sources/ai-agent-book")
print("已检出:", sorted(d for d in os.listdir(R) if d.startswith("chapter")))
def du(p):
    total=0; files=0
    for dp,dn,fn in os.walk(p):
        if os.sep+".git" in dp: continue
        for f in fn:
            try: total+=os.path.getsize(os.path.join(dp,f)); files+=1
            except: pass
    return files, round(total/1024/1024,1)
for d in sorted(x for x in os.listdir(R) if x.startswith("chapter")) + ["book"]:
    print(" ", d, du(os.path.join(R,d)))
import glob
print("残锁:", glob.glob(os.path.join(R,".git","**","*.lock"), recursive=True))