import urllib.request, re, ssl, json
ctx = ssl.create_default_context()
UA = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
def get(url, n=400000, t=25):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=t, context=ctx).read(n).decode("utf-8","ignore")

repos = ["microsoft/ai-agents-for-beginners","datawhalechina/hello-agents","huggingface/agents-course",
"NirDiamant/GenAI_Agents","skyming/awesome-ai-agent","microsoft/autogen","langchain-ai/langgraph",
"crewAIInc/crewAI","openai/openai-agents-python","geekan/MetaGPT","run-llama/llama_index",
"mem0ai/mem0","modelscope/agentscope","camel-ai/camel","OpenBMB/AgentVerse","e2b-dev/E2B",
"browser-use/browser-use","All-Hands-AI/OpenHands","kortix-ai/suna","langflow-ai/langflow",
"FlowiseAI/Flowise","n8n-io/n8n","dair-ai/Prompt-Engineering-Guide","rasbt/LLMs-from-scratch",
"anthropics/anthropic-cookbook","openai/openai-cookbook","punkpeye/awesome-mcp-servers",
"modelcontextprotocol/servers","Anthropic Courses"]

out=[]
for r in repos:
    try:
        h = get("https://github.com/"+r)
        m = re.search(r'id="repo-stars-counter-star"[^>]*title="([\d,]+)"', h)
        stars = m.group(1) if m else "?"
        d = re.search(r'<meta name="description" content="([^"]*)"', h)
        desc = (d.group(1) if d else "")[:160]
        print(f"{r}\t★{stars}\t{desc}")
    except Exception as e:
        print(f"{r}\tERR\t{e}")