import urllib.request, re, ssl
ctx = ssl.create_default_context()
UA = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept-Language":"en-US,en;q=0.9"}
def get(url, n=400000):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=25, context=ctx).read(n).decode("utf-8","ignore")
for u in ["https://github.com/microsoft/ai-agents-for-beginners",
          "https://raw.githubusercontent.com/microsoft/ai-agents-for-beginners/main/README.md"]:
    try:
        h = get(u)
        print("OK", u, len(h))
        print(h[:600].replace("\n"," ")[:600])
        print("---")
    except Exception as e:
        print("ERR", u, e)