#!/usr/bin/env python3
"""Download batch 4 (re-upload, mostly for 神秘之劫)."""
import urllib.request, urllib.parse, os, threading

D = "/root/.openclaw/workspace/novel-corpus"

novels = {
    "神秘之劫": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/神秘之劫-c3dae05c6bd5f3d0c14225954fc545aa.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242203268&Signature=ol3JOLgNwYn/A5g70qDbXF2coGY=",
}

def encode_url(url):
    parts = url.split('?', 1)
    path = parts[0]
    query = '?' + parts[1] if len(parts) > 1 else ''
    return urllib.parse.quote(path, safe='/:@!$&\'()*+,;=-._~%') + query

for name, url in novels.items():
    out = os.path.join(D, f"{name}.txt")
    try:
        urllib.request.urlretrieve(encode_url(url), out)
        sz = os.path.getsize(out)
        print(f"OK: {name} ({sz/1024/1024:.1f}MB)")
    except Exception as e:
        print(f"FAIL: {name} - {e}")

# Check what we have now
total = 0
count = 0
for f in sorted(os.listdir(D)):
    if f.endswith('.txt'):
        sz = os.path.getsize(os.path.join(D, f))
        total += sz
        count += 1
print(f"\nCorpus: {count} files, {total/1024/1024:.0f}MB total")
