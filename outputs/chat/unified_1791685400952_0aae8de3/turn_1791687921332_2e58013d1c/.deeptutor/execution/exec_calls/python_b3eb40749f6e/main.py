import os, subprocess, urllib.request, shutil
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]

# 1) 上一轮产物是否还在
old = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687804788_c528f60dea")
print("old dir exists:", os.path.isdir(old), os.listdir(old) if os.path.isdir(old) else "-")

# 2) 本轮可写目录
new = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687921332_2e58013d1c")
print("new dir exists:", os.path.isdir(new))
os.makedirs(new, exist_ok=True)

# 3) git / curl 可用性
for tool in ["git", "curl", "uv"]:
    print(tool, "->", shutil.which(tool))

# 4) 网络可达性
def probe(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            data = r.read(400)
            return "OK", r.status, r.headers.get("Content-Length"), len(data)
    except Exception as e:
        return "ERR", type(e).__name__, str(e)[:120], None

for u in [
    "https://raw.githubusercontent.com/bojieli/ai-agent-book/main/README.md",
    "https://raw.githubusercontent.com/bojieli/ai-agent-book/main/docs/zh-CN/LEARNING.md",
    "https://codeload.github.com/bojieli/ai-agent-book/tar.gz/refs/heads/main",
]:
    print(u.split("/")[-1], "=>", probe(u))