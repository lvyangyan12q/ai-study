import os, subprocess, time

root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
LS  = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791697524079_49dab0e4c8/learning-space")
R   = os.path.join(LS, "sources/ai-agent-book")
G   = os.path.join(R, ".git")
LOGD = os.path.join(LS, "_logs"); os.makedirs(LOGD, exist_ok=True)

# 1) 直接写 sparse 规则（只保留 书/文档/skills/十章代码，排除媒体与运行日志）
keep = ["/*.md","/*.sh","/*.txt","/LICENSE","/.gitignore","/.coderabbit.yaml",
        "/book/","/docs/","/skills/"] + [f"/chapter{i}/" for i in range(1,11)]
drop = ["!/**/*.mp4","!/**/*.mov","!/**/*.avi","!/**/*.webm","!/**/*.png","!/**/*.jpg",
        "!/**/*.jpeg","!/**/*.gif","!/**/*.webp","!/**/*.pdf","!/**/*.pptx","!/**/*.gz",
        "!/**/*.zip","!/**/*.mp3","!/**/*.wav","!/**/*.m4a","!/**/runs/**","!/**/outputs/**"]
open(os.path.join(G,"info","sparse-checkout"),"w",encoding="utf-8").write("\n".join(keep+drop)+"\n")
print("规则条数:", len(keep+drop))

# 2) 走代理后台下载（不受单次工具超时限制）
env = dict(os.environ)
env["HTTPS_PROXY"] = env["HTTP_PROXY"] = "http://127.0.0.1:7897"
logpath = os.path.join(LOGD, "fetch_proxy.log")
log = open(logpath, "w", encoding="utf-8", buffering=1)
p = subprocess.Popen(["git","-c","http.version=HTTP/1.1","-c","http.proxy=http://127.0.0.1:7897",
                      "-c","https.proxy=http://127.0.0.1:7897","checkout","HEAD","--","."],
                     cwd=R, env=env, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                     creationflags=0x00000008|0x00000200)
print("后台 pid =", p.pid); print("(下面每 30 秒报一次进度)")

# 3) 在同一次调用里守着它，看能不能一口气跑完
t0 = time.time()
while time.time()-t0 < 235:
    time.sleep(30)
    alive = p.poll() is None
    n = sum(len(fs) for _,_,fs in os.walk(R))
    mb = sum(os.path.getsize(os.path.join(dp,f)) for dp,_,fs in os.walk(R) for f in fs)/1e6
    tail = open(logpath,encoding="utf-8",errors="replace").read().strip().splitlines()[-1:] or [""]
    print(f"[{int(time.time()-t0):>3}s] 文件 {n:>5}  已落盘 {mb:6.1f} MB  运行中={alive}  log: {tail[0][:110]}")
    if not alive: break
print("最终退出码:", p.poll(), "| 耗时 %.0f s" % (time.time()-t0))
print("顶层目录:", sorted(d for d in os.listdir(R) if not d.startswith('.')))