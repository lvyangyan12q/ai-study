import urllib.request, json, ssl
repos = ["microsoft/ai-agents-for-beginners","datawhalechina/hello-agents","huggingface/agents-course",
"NirDiamant/GenAI_Agents","skyming/awesome-ai-agent","microsoft/autogen","langchain-ai/langgraph",
"crewAIInc/crewAI","openai/openai-agents-python","geekan/MetaGPT","AntonOsika/gpt-engineer",
"TransformerOptimus/SuperAGI","run-llama/llama_index","deepset-ai/haystack","mem0ai/mem0",
"datawhalechina/handy-multi-agent","modelscope/agentscope","camel-ai/camel","OpenBMB/AgentVerse",
"e2b-dev/E2B","livekit/agents","browser-use/browser-use","All-Hands-AI/OpenHands"]
ctx = ssl.create_default_context()
for r in repos:
    try:
        req = urllib.request.Request("https://api.github.com/repos/"+r, headers={"User-Agent":"x"})
        d = json.load(urllib.request.urlopen(req, timeout=15, context=ctx))
        print(f"{d['full_name']}\t★{d['stargazers_count']}\tforks {d['forks_count']}\tlang {d.get('language')}\tupdated {d['pushed_at'][:10]}\t{(d.get('description') or '')[:120]}")
    except Exception as e:
        print(r, "ERR", e)