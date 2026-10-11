import urllib.request, re, ssl, json
ctx = ssl.create_default_context()
UA = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}
req = urllib.request.Request("https://github.com/microsoft/ai-agents-for-beginners", headers=UA)
h = urllib.request.urlopen(req, timeout=25, context=ctx).read(600000).decode("utf-8","ignore")
for kw in ["stargazerCount","stargazers_count","\"star\"","starsCount"]:
    idxs=[m.start() for m in re.finditer(re.escape(kw), h)][:3]
    print(kw, idxs)
    for i in idxs:
        print("   ", h[max(0,i-100):i+120].replace("\n"," "))
# try shields
try:
    req2 = urllib.request.Request("https://img.shields.io/github/stars/microsoft/ai-agents-for-beginners.json", headers=UA)
    print("shield:", urllib.request.urlopen(req2, timeout=20, context=ctx).read().decode())
except Exception as e:
    print("shield ERR", e)