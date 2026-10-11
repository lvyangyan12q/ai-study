import os
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791696096980_527b333145")
R = os.path.join(NEW, "learning-space/sources/ai-agent-book")
def du(p):
    total=0; files=0
    for dp,dn,fn in os.walk(p):
        if os.sep+".git" in dp: continue
        for f in fn:
            try: total+=os.path.getsize(os.path.join(dp,f)); files+=1
            except: pass
    return files, round(total/1024/1024,1)
chans = sorted(d for d in os.listdir(R) if d.startswith("chapter") and os.path.isdir(os.path.join(R,d)))
print("已存在章目录:", chans)
for c in chans:
    print("  ", c, du(os.path.join(R,c)))
print("repo 总计:", du(R))