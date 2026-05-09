#!/usr/bin/env python3
"""Download batch 5."""
import urllib.request, urllib.parse, os, threading

D = "/root/.openclaw/workspace/novel-corpus"

novels = {
    "巫界术士": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/巫界术士-9453fcc09e83384fb7c0695702e434b5.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242464360&Signature=aypiPVf2xEasT6eCJzGMDhoCzYs=",
    "巫颂": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/巫颂-fc166b35e50e57ad2f425c190fd8d575.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242463660&Signature=9R8Q8I1bS8QEy9SRYk+qpZIFYaA=",
    "无限之电影杀戮": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/无限之电影杀戮-a07b85f633a31429eba0c909007a7285.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242463411&Signature=DiskhiRMnbnE6oIg5YzHm3bsQjI=",
    "香火成神道": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/香火成神道-499761b16dec550e9ea5fe76d4cb8048.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242463397&Signature=ceOeCn08k2EZb349kLcfVDb0H1g=",
    "逍遥梦路": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/逍遥梦路-9af1e4c991a4e2db8ba39552fda0bef1.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242464669&Signature=iIhyyEKT/6TlvhlaOuCRhdmwp7w=",
    "星辰变": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/星辰变-86098b88aa4e6bc08194e32cc20ebad5.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242464518&Signature=tL1DHcggpzvVHJWoifxrpmmPDhY=",
    "星峰传说": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/星峰传说-808adfad2ff096123aafa6f403d0673c.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242464268&Signature=/aBIKpxMiFPi1iKC6J+YYjNz1e8=",
    "星河大帝": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/星河大帝-246c0671435bd6352c2b04a84620ff53.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242463941&Signature=AjEGLpunNnhGeZMQ/rEoo+XQV+o=",
    "星空职业者": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/星空职业者-1f82977ffb9a27e8d7b9aeeedda616ff.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242464185&Signature=xLGIB6gIzUlApo4nYMzwJmcKfpo=",
    "虚空之主": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/虚空之主-730183e6d8e54ee0b15c9480ad6d9de5.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242464718&Signature=mkmvxpHMQxkd3UqTt8foHP2tU0E=",
    "雪鹰领主": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/雪鹰领主-f4537e6729016e2f29bc27046db7eed1.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242464043&Signature=kCDGQhXFVgMLfzF5kvDX+IRUAIM=",
    "阳神": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/阳神-0c292b05db2e5441e59a4cf26ea22b5d.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242464921&Signature=gyAqUnTMBRQAwX2gBo9xhcc3EQk=",
    "夜的命名术": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/夜的命名术-f8057a13f9a261342b47b5640eaa2525.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242465065&Signature=M954gfLaFx5bBwMOCiJip8ibSo4=",
    "隐秘死角": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/隐秘死角-69ccf8579f2779a6e72af1f98f44355d.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242464451&Signature=ABmwB71U7vFVFP4udEqvL139+Ig=",
    "主神崛起": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/主神崛起-37072fc8c499425d3a862d9463ed6458.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808242464736&Signature=ldHdv+YRB8amPr5jl39NeqAvsJw=",
}

def encode_url(url):
    parts = url.split('?', 1)
    path = parts[0]
    query = '?' + parts[1] if len(parts) > 1 else ''
    return urllib.parse.quote(path, safe='/:@!$&\'()*+,;=-._~%') + query

def dl(name, url):
    out = os.path.join(D, f"{name}.txt")
    if os.path.exists(out) and os.path.getsize(out) > 1000:
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

count = len([f for f in os.listdir(D) if f.endswith('.txt')])
print(f"Corpus: {count} files")
