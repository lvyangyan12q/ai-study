import urllib.request, re, ssl
ctx = ssl.create_default_context()
UA = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}
def page(r):
    req = urllib.request.Request("https://github.com/"+r, headers=UA)
    return urllib.request.urlopen(req, timeout=25, context=ctx).read(700000).decode("utf-8","ignore")

repos = ["microsoft/ai-agents-for-beginners","datawhalechina/hello-agents","huggingface/agents-course",
"NirDiamant/GenAI_Agents","NirDiamant/agents-towards-production","skyming/awesome-ai-agent",
"microsoft/autogen","langchain-ai/langgraph","crewAIInc/crewAI","openai/openai-agents-python",
"geekan/MetaGPT","run-llama/llama_index","mem0ai/mem0","modelscope/agentscope","camel-ai/camel",
"e2b-dev/E2B","browser-use/browser-use","All-Hands-AI/OpenHands","langflow-ai/langflow",
"FlowiseAI/Flowise","dair-ai/Prompt-Engineering-Guide","rasbt/LLMs-from-scratch","punkpeye/awesome-mcp-servers",
"modelcontextprotocol/servers","datawhalechina/handy-multi-agent","datawhalechina/llm-universe",
"humanlayer/12-factor-agents","e2b-dev/awesome-ai-agents","kyrolabs/awesome-langchain",
"microsoft/generative-ai-for-beginners","AnthropicAI/anthropic-cookbook","anthropics/claude-cookbooks",
"wandb/wandb","langgenius/dify","infiniflow/ragflow","1Panel-dev/MaxKB","josephmisiti/awesome-machine-learning",
"anthropics/prompt-eng-interactive-tutorial","cfortuner/awesome-ai-agents","swyxio/ai-notes"]
seen=set()
for r in repos:
    if r in seen: continue
    seen.add(r)
    try:
        h = page(r)
        s = re.search(r'"stargazerCount":(\d+)', h)
        f = re.search(r'"forksCount":(\d+)', h)
        d = re.search(r'<meta property="og:description" content="([^"]*)"', h)
        print(f"{r}\t★{s.group(1) if s else '?'}\tF{f.group(1) if f else '?'}\t{(d.group(1) if d else '')[:130]}")
    except Exception as e:
        print(f"{r}\tERR\t{e}")