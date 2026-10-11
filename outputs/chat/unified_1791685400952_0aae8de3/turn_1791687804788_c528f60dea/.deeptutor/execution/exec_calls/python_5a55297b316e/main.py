import os
print("cwd:", os.getcwd())
root = os.environ.get("DEEPTUTOR_WORKSPACE_ROOT")
print("root set:", bool(root))
if root:
    print("cwd rel to root:", os.path.relpath(os.getcwd(), root))
    print("root listing:", os.listdir(root)[:20])
target = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687804788_c528f60dea")
print("target exists:", os.path.isdir(target))
print(os.listdir(target) if os.path.isdir(target) else "-")