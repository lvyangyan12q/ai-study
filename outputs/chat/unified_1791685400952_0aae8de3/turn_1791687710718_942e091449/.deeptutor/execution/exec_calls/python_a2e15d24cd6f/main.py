import urllib.request, re, ssl
ctx = ssl.create_default_context()
UA = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}
def get(u, n=700000, t=25):
    req = urllib.request.Request(u, headers=UA)
    return urllib.request.urlopen(req, timeout=t, context=ctx).read(n).decode("utf-8","ignore")

for r in ["bojieli/ai-agent-book"]:
    try:
        h = get("https://github.com/"+r)
        print("FINAL URL OK, len", len(h))
        s = re.search(r'"stargazerCount":(\d+)', h); f = re.search(r'"forksCount":(\d+)', h)
        d = re.search(r'<meta property="og:description" content="([^"]*)"', h)
        lic = re.search(r'"spdxId":"([^"]*)"', h)
        print(r, "★", s.group(1) if s else "?", "F", f.group(1) if f else "?", "license", lic.group(1) if lic else "?")
        print("DESC:", d.group(1) if d else "")
    except Exception as e:
        print(r, "ERR", e)

for branch in ["main","master"]:
    try:
        md = get(f"https://raw.githubusercontent.com/bojieli/ai-agent-book/{branch}/README.md", 40000)
        print("==== README", branch, "len", len(md))
        print(md[:3000])
        break
    except Exception as e:
        print("README", branch, "ERR", e)