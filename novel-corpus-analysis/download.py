#!/usr/bin/env python3
"""Download new novels for punctuation fingerprint analysis."""
import urllib.request, os, threading

D = "/root/.openclaw/workspace/novel-corpus"
os.makedirs(D, exist_ok=True)

novels = {
    # Batch 2 - new
    "佛本是道": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/佛本是道-df12d74fe4f1fdd1f702f721babd8e2b.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241907656&Signature=+rSRQZ6eXOHkZILGD9JICc2aYc8=",
    "苟在妖武乱世修仙": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/苟在妖武乱世修仙%20(1)-2390c4eab3fee497fafc44b70478f7da.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241906238&Signature=d5L/IDJT7Mp0+oPBW/MesHy5UOI=",
    "诡秘如风常伴吾身": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/诡秘如风，常伴吾身-37ed61c79c9355d2a3b45593d318e93d.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241905780&Signature=/OCbSTXC/ifNkLAMwNKhcy/gYmQ=",
    "汉阙": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/汉阙-db99f5475bd01ad752f5f2133faf277f.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241905903&Signature=/coSiS/cKGAoZA5suku/UmSV784=",
    "极道天魔": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/极道天魔-f388891ab67780b264fce7b991e537e8.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241906526&Signature=wjtzYusMou0ZtywE+kSXVBhAlXc=",
    "轮回大劫主": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/轮回大劫主-54109f8fa84df3b6a75aefc99d8f569a.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241906854&Signature=ZP/feuaqXIcEEMVsc9s2TYPRWV0=",
    "美漫法神": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/美漫法神-ff52f25857ece08119821c2af86f0813.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241909172&Signature=yhBJDHhHearn0Ev5ZyeKb9K1pSE=",
    "明克街13号": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/明克街13号-4586a0259dd1c984dbcf345c0bdcb71c.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241907570&Signature=HKjiBn7ezV85Wz8GjA7gcl4DCds=",
    "秦吏": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/秦吏-30c5828679de5f5b6b43dfb1d479b6ed.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241907224&Signature=LObqEZYGaA2pHeuqM8u9Ygqm9NI=",
    # Batch 1 - new
    "光明纪元": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/cab54b4e-4cc4-490b-9452-2191bb80d17c.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241766942&Signature=z+o8vf1CAuO79+0vXWd6mFyzO44=",
    "开天录": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/《开天录》作者：血红-6a1c21dcd13b4bf6ae586b6c7416b90e.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241766236&Signature=Ol++lGPOCzUTBsWMU+DlTcq4/u4=",
    "逆龙道": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/《逆龙道》作者：血红-2e3273cbc93d16507fa32be1bf18b77b.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241765753&Signature=fNQnPQlQb5h8e2dnBSbNyn+KPHc=",
    "偷天": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/《偷天》作者：血红-0f42055d87299affa19ace04f81fffb5.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241766099&Signature=bYGgo2m0hKfKBwDt4Mwy5JMievM=",
    "邪龙道": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/《邪龙道》作者：血红-5cbf3be85b261f1a8d074278e009731f.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241768377&Signature=FrMYBvLSmG+bKiiYcqzticUfd/c=",
    "斗破苍穹": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/斗破苍穹-d5344f05e45c0959fd36f33a33d392eb.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241768802&Signature=UQRnTkDToqaDejsQx4tbo7QyjqI=",
}

def dl(name, url):
    out = os.path.join(D, f"{name}.txt")
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print(f"EXISTS: {name}")
        return
    try:
        urllib.request.urlretrieve(url, out)
        sz = os.path.getsize(out)
        print(f"OK: {name} ({sz/1024/1024:.1f}MB)")
    except Exception as e:
        print(f"FAIL: {name} - {e}")

threads = []
for name, url in novels.items():
    t = threading.Thread(target=dl, args=(name, url))
    t.start()
    threads.append(t)
for t in threads:
    t.join()

print("\n--- Downloaded ---")
total = 0
for f in sorted(os.listdir(D)):
    if f.endswith('.txt'):
        sz = os.path.getsize(os.path.join(D, f))
        total += sz
        print(f"  {f}: {sz/1024/1024:.1f}MB")
print(f"Total: {total/1024/1024:.1f}MB")
