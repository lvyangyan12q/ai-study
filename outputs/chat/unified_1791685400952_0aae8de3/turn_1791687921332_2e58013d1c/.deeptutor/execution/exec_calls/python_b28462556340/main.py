import os
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687921332_2e58013d1c")
R = os.path.join(NEW, "learning-space/sources/ai-agent-book")
for rel in ["docs/zh-CN/LEARNING.md", "docs/EXPERIMENT_STATUS.md"]:
    fp = os.path.join(R, rel)
    print("="*20, rel, "exists:", os.path.exists(fp))
    if os.path.exists(fp):
        t = open(fp, encoding="utf-8", errors="ignore").read()
        print("chars:", len(t))
        print(t[:4200])