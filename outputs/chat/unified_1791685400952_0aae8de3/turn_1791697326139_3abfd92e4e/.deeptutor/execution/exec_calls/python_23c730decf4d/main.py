import os, subprocess, time, glob, shutil, json

root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
BASE = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3")
PREV_LS = os.path.join(BASE, "turn_1791696096980_527b333145/learning-space")
NEW = os.path.join(BASE, "turn_1791697326139_3abfd92e4e")
os.makedirs(NEW, exist_ok=True)

# 1) 清掉上次被杀进程留下的 git 进程与锁
subprocess.run(["taskkill","/F","/IM","git.exe"], capture_output=True, text=True)
time.sleep(2)
LS = os.path.join(NEW, "learning-space")
R = os.path.join(LS, "sources/ai-agent-book")
if not os.path.isdir(LS) and os.path.isdir(PREV_LS):
    try:
        os.rename(PREV_LS, LS); print("学习空间已整体迁移到本轮目录（重命名，瞬间完成）")
    except OSError as e:
        print("rename 失败，改用复制:", e)
        shutil.copytree(PREV_LS, LS, symlinks=True)
G = os.path.join(R, ".git")
for l in glob.glob(os.path.join(G,"**","*.lock"), recursive=True):
    for attempt in range(3):
        try:
            os.remove(l); print("清锁成功:", os.path.basename(l)); break
        except Exception as e:
            time.sleep(1.5); print("清锁重试", attempt+1, os.path.basename(l), type(e).__name__)

# 2) 写 sparse 规则：只要 书/文档/skills/十章代码，排除媒体与大日志
keep = ["/book/", "/docs/", "/skills/"] + [f"/chapter{i}/" for i in range(1,11)]
drop = ["!/**/*.mp4","!/**/*.mov","!/**/*.avi","!/**/*.png","!/**/*.jpg","!/**/*.jpeg",
        "!/**/*.gif","!/**/*.webp","!/**/*.pdf","!/**/*.pptx","!/**/*.gz","!/**/*.zip",
        "!/**/*.mp3","!/**/*.wav","!/**/*.m4a","!/**/runs/**","!/**/outputs/**"]
patterns = keep + drop
subprocess.run(["git","sparse-checkout","set","--no-cone"]+patterns, cwd=R,
               capture_output=True, text=True)  # 先只登记规则（可能触发一次拉取，失败也无妨）

logdir = os.path.join(LS, "_logs"); os.makedirs(logdir, exist_ok=True)
log = open(os.path.join(logdir, "sparse_fetch.log"), "w", encoding="utf-8", buffering=1)
DETACHED = 0x00000008 | 0x00000200   # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
p = subprocess.Popen(["git","-c","http.version=HTTP/1.1","checkout","HEAD","--","."],
                     cwd=R, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                     creationflags=DETACHED)
print("后台下载已启动 pid=", p.pid)
time.sleep(20)
print("20 秒后 log 末尾:", open(os.path.join(logdir,'sparse_fetch.log'),encoding='utf-8',errors='replace').read()[-300:] or "(空)")
print("进程是否还在:", p.poll() is None)