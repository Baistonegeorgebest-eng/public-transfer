#!/usr/bin/env python3
"""Download batch 6."""
import urllib.request, urllib.parse, os, threading

D = "/root/.openclaw/workspace/novel-corpus"

novels = {
    "异常生物见闻录": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/异常生物见闻录-4f77cc94512d3daf1c27ab04dae842a3.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243258633&Signature=e1j5CgJdWPzyGvV331BehtjSLsI=",
    "战锤神印": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/战锤神印-78825e572c01dc07f32806d8c871f4d5.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243257612&Signature=BSXMBmLDHSErmKtiDd4mtBdhsKw=",
    "蛊惑魔王": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/蛊惑魔王-45fa2d85dc1a1d6e19bc12ce724d394d.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243257457&Signature=0aV7Vbb0Er3n9s/FVGA+JzilArI=",
    "巫师之旅": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/巫师之旅-bd743b5a52d4eba752a4bf57c957adb4.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243258920&Signature=qfnjfhnhdTrwTQLVLJYoh2Ia/ng=",
    "冒牌大英雄": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/冒牌大英雄-aec17efa213a811ea0bbe88db62b80e3.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243257818&Signature=Sdxq2VGfBI15SoHRScCDepESreE=",
    "武动乾坤": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/武动乾坤-d156fba8f4a8746912782a3b388deb6d.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243257942&Signature=kov7szopO3kuiqtAWXbih3O6QGo=",
    "大主宰": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/大主宰-64f2cc7502f597caf8e4817ea805d008.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243258230&Signature=6zr9ooJ02iAP7tVNlCnbji9uPYM=",
    "斗破苍穹2": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/斗破苍穹-07b259d1c70ba15637c75b8e637fb8a2.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243258400&Signature=7L89DyrKBdlsmBy7Eck4eq2UprY=",
    "元尊": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/元尊-30d6412cf6acd331cbaad9401ca8a348.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243258092&Signature=tuCDAfEUl4UrbV/eU53HsrYMqPY=",
    "魔兽剑圣异界纵横": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/魔兽剑圣异界纵横-23a7047040cca4246be1c6d07b55687f.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243257686&Signature=qh0akukDSZ2vooHJlzXA0KEzL68=",
    "哈利波特之学霸传奇": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/哈利波特之学霸传奇-33956544c5befe446306b4660a59d31b.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243257555&Signature=jE6VCFlvtVN/+wSIToUxAlHAwg4=",
    "剑来": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/剑来-1e7ba651a02b1ac0cfc8c1064429585f.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243259690&Signature=r6ByNo7VEePSJsYT/ZYgB+KxZMI=",
    "太阳王之证": "https://cnbj3-fusion.fds.api.xiaomi.com/chatbot-prod/multimedia/2234038896/9897c6b4-f3f6-4f52-9a6c-b49a3feddcb3.txt?GalaxyAccessKeyId=AKDFVGPIRVU2J5L22P&Expires=1808243296213&Signature=qCXTL2AhFsN6y9SCD6TZQVAhyqE=",
}

def encode_url(url):
    parts = url.split('?', 1)
    return urllib.parse.quote(parts[0], safe='/:@!$&\'()*+,;=-._~%') + ('?' + parts[1] if len(parts) > 1 else '')

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
total_mb = sum(os.path.getsize(os.path.join(D,f)) for f in os.listdir(D) if f.endswith('.txt'))/1024/1024
print(f"Corpus: {count} files, {total_mb:.0f}MB")
