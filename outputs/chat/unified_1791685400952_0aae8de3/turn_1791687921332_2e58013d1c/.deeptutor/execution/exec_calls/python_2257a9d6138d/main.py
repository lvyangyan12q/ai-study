import os, subprocess, shutil
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687921332_2e58013d1c")
SRC = os.path.join(NEW, "learning-space/sources")
print("sources:", os.listdir(SRC) if os.path.isdir(SRC) else "-")
for n in ["12-factor-agents", "openai-agents-python"]:
    d = os.path.join(SRC, n)
    print(n, "exists:", os.path.isdir(d), os.listdir(d)[:10] if os.path.isdir(d) else "-")