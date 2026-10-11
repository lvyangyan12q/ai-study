import os
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
D = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687804788_c528f60dea")
path = os.path.join(D, "ai-agent-curriculum.html")

body2 = r"""
<section id="path">
  <h2><span class="idx">02</span>推进路线：五个阶段</h2>
  <p class="sub">顺序不是随意的：先把"信息如何进入模型"搞懂（阶段一），你后面读任何框架源码都会快一个数量级；评估放在中途而不是最后，因为它本身就是调试工具。</p>
  <div id="pathList"></div>
</section>

<section id="pace">
  <h2><span class="idx">03</span>两周一个小节：节奏模板</h2>
  <p class="sub">每一小节都走同一个四步循环——这就是把"读过"变成"掌握"的机制。点开看每周具体做什么。</p>
  <div id="paceList"></div>
  <div class="note" style="margin-top:16px">
    <b>关于时间：</b>若每周只能投入 3 小时，把"读"和"实验"合并、跳过源码精读，总周期拉长到约 24 周即可，不要删掉阶段三（评估）——它是最容易被跳过、也最影响你判断力的一环。
  </div>
</section>

<section id="quiz">
  <h2><span class="idx">04</span>自测：12 道判断题</h2>
  <p class="sub">这些题故意设计成"凭直觉容易答错"。选完立刻给解析，答错不扣分，但请想清楚你原来为什么选错。</p>
  <div id="quizBox"></div>
  <div class="card" style="margin-top:18px;display:flex;gap:14px;align-items:center;flex-wrap:wrap">
    <button class="btn" id="quizReset">重做全部</button>
    <span id="quizScore" style="color:var(--mut);font-size:14.5px"></span>
  </div>
</section>

<section id="next">
  <h2><span class="idx">05</span>下一步</h2>
  <div class="grid g2">
    <div class="card">
      <b>① 去实验区把六个抽象概念玩一遍</b>
      <p style="color:var(--mut);font-size:14.5px">上下文预算、ReAct 循环、工具调用时序、RAG 召回、评估噪声、多 Agent 上下文模式，全部可交互。</p>
      <p style="margin:12px 0 0"><a class="btn" href="concept-lab.html" target="_blank">打开交互实验室 →</a></p>
    </div>
    <div class="card">
      <b>② 主线教材：按章精读 + 跑实验</b>
      <p style="color:var(--mut);font-size:14.5px">《深入理解 AI Agent：设计原理与工程实践》(<code>bojieli/ai-agent-book</code>)，10 章正文 + 109 个配套实验，中文原版免费，提供 PDF/EPUB。每章卡片里都有直达链接。</p>
      <p style="margin:12px 0 0"><a href="https://github.com/bojieli/ai-agent-book" target="_blank">github.com/bojieli/ai-agent-book ↗</a></p>
    </div>
  </div>
</section>

<div style="margin-top:60px;padding-top:20px;border-top:1px solid var(--line);color:var(--mut);font-size:13.5px">
  星标与仓库数据核对于 2026-10-11。文中实验为教学示意模型，用于建立直觉，不代表真实模型的精确数值行为。
</div>
</div>
"""
with open(path, "a", encoding="utf-8") as f:
    f.write(body2)
print("appended body2")