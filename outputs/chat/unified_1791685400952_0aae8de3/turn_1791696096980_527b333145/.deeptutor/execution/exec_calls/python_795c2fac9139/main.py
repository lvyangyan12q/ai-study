import os, subprocess, time
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

def add(ch, timeout=140):
    t0=time.time()
    try:
        r = subprocess.run(["git","-c","http.version=HTTP/1.1","sparse-checkout","add",ch],
                           cwd=R, capture_output=True, text=True, timeout=timeout)
        return r.returncode, round(time.time()-t0,1), (r.stderr or "")[-160:].replace("\n"," ")
    except subprocess.TimeoutExpired:
        return "TIMEOUT", round(time.time()-t0,1), ""

t_start=time.time(); 
for i in [2,3,4,5]:
    ch=f"chapter{i}"
    if os.path.isdir(os.path.join(R,ch)):
        print(ch, "已存在，跳过"); continue
    if time.time()-t_start > 225:
        print("时间用尽，", ch, "留到下一批"); break
    rc, secs, err = add(ch)
    d=os.path.join(R,ch)
    print(f"{ch}: rc={rc} {secs}s 文件数={du(d)[0] if os.path.isdir(d) else 0} MB={du(d)[1] if os.path.isdir(d) else 0} {err[:110]}")
print("repo 总计:", du(R))