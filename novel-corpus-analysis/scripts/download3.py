#!/usr/bin/env python3
"""Download batch 3 novels."""
import urllib.request, urllib.parse, os, threading

D = "/root/.openclaw/workspace/novel-corpus"

novels = {
    "三界血歌": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/三界血歌-396fab6bda559a0e53f3c0df783a272a.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242000431&Signature=AtDipCY4LVutRPYUjgBgY6jypd8=",
    "绍宋": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/绍宋-80728dfc24ea3ade34d91c7af70c6a4f.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241997593&Signature=yG0BgnB42eExbI0FWLUa5VcRYDo=",
    "神秘之劫": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/神秘之劫-03a3fd00bb5212cddd8ace8c796237fb.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241999101&Signature=x/8gnk/Xw0QhQQ4Lv0/aBD6uBPI=",
    "神秘之旅": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/神秘之旅-d7f587b47e4beacefa94e5c86079816b.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241998251&Signature=maqK4H/UxQoPtnpNEDVZ79/snW0=",
    "神秀之主": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/神秀之主-bffdd1f252d5987dd3e26be97f72321d.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241997526&Signature=wma2hPp6Z0db2FJ5TcdDQMjs1kU=",
    "升龙道": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/升龙道-0bad303c1dfe695a6487963800c10504.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241998353&Signature=1iKeO8Nfu8hUH+e6dQkrgBVyN+w=",
    "圣王": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/圣王-24729c4abf816ebc6fff1fa421234840.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241998526&Signature=miR8HkYal0AUPLwTkaVSBP5fbwU=",
    "十方武圣": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/十方武圣-5c27f779c162da22415ce45c7bf32321.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241998426&Signature=oZ8WHfFniicXQvYX2vbc5eE9SCI=",
    "史上第一祖师爷": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/史上第一祖师爷-a96dbd9dd52c2d6ad20d6cd08bef1333.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242001029&Signature=eVJGsvkkrbxPMkdKPhOjWC3AE6s=",
    "史上最强师兄": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/史上最强师兄-14541d930a5a12b26a212f7977fd544f.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242000839&Signature=dOjBX2u/jeGwF7xSkZ99nXIZOQI=",
    "唐砖": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/唐砖-3dd41dce6845cf59786f6cf25eb95d1a.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242000254&Signature=T+aywg41+A94r0MjVezmHCFImTs=",
    "吞噬星空": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/吞噬星空-a44193de9a6658d24591a112599afa7c.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242001051&Signature=VINR1ygRcNB58bRLX5/o5FvLPnk=",
    "玩家请自重": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/玩家请自重-4d21be58c318b8557043807c72ef4b91.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241998532&Signature=vP/Dg3Wi6RwkMNueViFDMengk1k=",
    "万千之心": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/万千之心-dadf47ce58cf738c02e855edb055e87e.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241998531&Signature=nIrhs6Fs8L5Lc1NHlkdoHdVI6oQ=",
    "万族之劫": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/万族之劫-4d77be6449c0e212d936cfba64244fa1.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242001824&Signature=e1KRIQPx+4rlSFMA6b3SzmP29Nk=",
    "我的属性修行人生": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/我的属性修行人生-f4ab64a07e7acc4d0e8b3ea2e01caf70.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808241998594&Signature=47M3ijb8P0DZXS+P2N6QHCX7FPA=",
    "我师兄实在太稳健了": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/我师兄实在太稳健了-d563c46bb29c7c9e5888f4bff9484235.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242000537&Signature=d2U31IbIV8LCUuyU+416Oqz5umY=",
    "我真是族长": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/我真是族长（万古最强部落）-7bc5cea845cb7f445ccad83f2217f5d9.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242000692&Signature=sMB2Z5IeBgZQhauCcyJeokdz2NM=",
}

def encode_url(url):
    parts = url.split('?', 1)
    path = parts[0]
    query = '?' + parts[1] if len(parts) > 1 else ''
    return urllib.parse.quote(path, safe='/:@!$&\'()*+,;=-._~%') + query

def dl(name, url):
    out = os.path.join(D, f"{name}.txt")
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print(f"EXISTS: {name}")
        return
    try:
        urllib.request.urlretrieve(encode_url(url), out)
        print(f"OK: {name} ({os.path.getsize(out)/1024/1024:.1f}MB)")
    except Exception as e:
        print(f"FAIL: {name} - {e}")

threads = []
for name, url in novels.items():
    t = threading.Thread(target=dl, args=(name, url))
    t.start()
    threads.append(t)
for t in threads:
    t.join()
print("Done batch 3")
