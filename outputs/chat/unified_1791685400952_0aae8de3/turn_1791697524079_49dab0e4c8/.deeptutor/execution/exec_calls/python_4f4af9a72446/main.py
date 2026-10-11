import os, subprocess, time, glob

root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
LS  = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791697524079_49dab0e4c8/learning-space")
R   = os.path.join(LS, "sources/ai-agent-book"); G = os.path.join(R, ".git")
LOGD= os.path.join(LS, "_logs")

# 先看清已下落的 chapter2/3 里是什么在占体积
def sz(d):
    return sum(os.path.getsize(os.path.join(dp,f)) for dp,_,fs in os.walk(d) for f in fs)
for ch in ["chapter2","chapter3"]:
    subs = [(sz(os.path.join(R,ch,s)), s) for s in os.listdir(os.path.join(R,ch)) if os.path.isdir(os.path.join(R,ch,s))]
    print(ch, "子目录体积 TOP5:", [(s, round(m/1e6,1)) for m,s in sorted(subs, reverse=True)[:5]])
big = sorted(((os.path.getsize(os.path.join(dp,f)), os.path.relpath(os.path.join(dp,f), R))
              for dp,_,fs in os.walk(R) for f in fs), reverse=True)[:6]
print("最大文件:", [(round(m/1e6,2), p[-60:]) for m,p in big])

# 规则：保留书/文档/skills/十章代码；剔除媒体、日志类大文件与已知超长路径
keep = ["/README.md","/README.en.md","/LICENSE","/mkdocs.yml","/pyproject.toml","/.gitignore",
        "/book/","/docs/","/skills/"] + [f"/chapter{i}/" for i in range(1,11)]
drop = ["!/**/*.mp4","!/**/*.mov","!/**/*.avi","!/**/*.webm","!/**/*.png","!/**/*.jpg","!/**/*.jpeg",
        "!/**/*.gif","!/**/*.webp","!/**/*.pdf","!/**/*.pptx","!/**/*.gz","!/**/*.zip","!/**/*.tar",
        "!/**/*.mp3","!/**/*.wav","!/**/*.m4a","!/**/*.jsonl","!/**/*.ndjson","!/**/*.csv",
        "!/**/*.log","!/**/*.parquet","!/**/*.db","!/**/*.sqlite","!/**/*.sqlite3",
        "!/**/runs/**","!/**/outputs/**","!/**/traces/**","!/**/checkpoints/**","!/**/__pycache__/**",
        "!/chapter10/book-translation/validation/**"]
open(os.path.join(G,"info","sparse-checkout"),"w",encoding="utf-8").write("\n".join(keep+drop)+"\n")
subprocess.run(["git","config","core.longpaths","true"], cwd=R, capture_output=True)

env = dict(os.environ); env["HTTPS_PROXY"] = env["HTTP_PROXY"] = "http://127.0.0.1:7897"
logpath = os.path.join(LOGD, "reapply2.log")
log = open(logpath,"w",encoding="utf-8",buffering=1)
p = subprocess.Popen(["git","-c","core.longpaths=true","-c","http.version=HTTP/1.1",
                      "-c","http.proxy=http://127.0.0.1:7897","-c","https.proxy=http://127.0.0.1:7897",
                      "sparse-checkout","reapply"],
                     cwd=R, env=env, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                     creationflags=0x00000008|0x00000200)
print("pid =", p.pid)
t0=time.time()
while time.time()-t0 < 215:
    time.sleep(20)
    alive = p.poll() is None
    n = sum(len(fs) for _,_,fs in os.walk(R)); mb = sz(R)/1e6
    tail = (open(logpath,encoding="utf-8",errors="replace").read().strip().splitlines() or [""])[-1]
    print(f"[{int(time.time()-t0):>3}s] {n:>5} 文件 {mb:7.1f} MB 运行中={alive} | {tail[:95]}")
    if not alive: break
print("退出码:", p.poll(), "耗时 %.0f s" % (time.time()-t0))
print("log:", open(logpath,encoding="utf-8",errors="replace").read()[:500])
for d in sorted(glob.glob(os.path.join(R,"chapter*"))):
    print(f"  {os.path.basename(d):<10} {sum(len(fs) for _,_,fs in os.walk(d)):>5} 文件 {sz(d)/1e6:7.1f} MB")