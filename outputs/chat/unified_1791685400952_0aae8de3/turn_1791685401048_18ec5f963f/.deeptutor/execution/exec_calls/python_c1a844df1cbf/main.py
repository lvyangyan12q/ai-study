import urllib.request, re, ssl
ctx = ssl.create_default_context()
UA = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}
req = urllib.request.Request("https://github.com/microsoft/ai-agents-for-beginners", headers=UA)
h = urllib.request.urlopen(req, timeout=25, context=ctx).read(400000).decode("utf-8","ignore")
for kw in ["stargazers","starred","repo-stars","aria-label=\"1","og:description","social-count"]:
    for m in re.finditer(re.escape(kw), h):
        s=max(0,m.start()-120); print(kw,"|",h[s:m.start()+160].replace("\n"," "))
        break
print("=====")
# find all occurrences of 'stars'
print([m.start() for m in re.finditer("stars", h)][:10])
i = h.find('id="repo-stars-counter-star"')
print("idx",i, h[i-200:i+300] if i>0 else "")