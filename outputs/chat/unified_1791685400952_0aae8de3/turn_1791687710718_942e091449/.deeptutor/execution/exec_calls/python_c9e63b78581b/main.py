import urllib.request, re, ssl
ctx = ssl.create_default_context()
UA = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}
req = urllib.request.Request("https://raw.githubusercontent.com/bojieli/ai-agent-book/main/README.md", headers=UA)
md = urllib.request.urlopen(req, timeout=25, context=ctx).read(60000).decode("utf-8","ignore")
i = md.find("目录")
print(md[3000:9000])