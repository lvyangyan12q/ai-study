import os
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
D = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687804788_c528f60dea")
path = os.path.join(D, "ai-agent-curriculum.html")

part = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Agent 系统知识体系 · 进阶课程</title>
<style>
:root{
  --bg:#0b0f16; --bg2:#121826; --card:#141b28; --line:#24declared;
}
</style>
</head>
</html>
"""
print("placeholder")