#!/usr/bin/env python3
"""Final punctuation fingerprint v3 - all 62 novels."""
import os, re

D = "/root/.openclaw/workspace/novel-corpus"

def read_file(filepath):
    for enc in ['gbk', 'gb18030', 'utf-8', 'gb2312']:
        try:
            with open(filepath, 'r', encoding=enc, errors='replace') as f:
                text = f.read()
            if '的' in text[:1000] or '章' in text[:2000]:
                return text
        except:
            continue
    return None

def analyze(text):
    total = len(re.sub(r'\s', '', text))
    if total < 10000: return None
    comma = text.count('，') + text.count(',')
    period = text.count('。') + text.count('.')
    excl = text.count('！') + text.count('!')
    ellipsis = text.count('……')
    quest = text.count('？') + text.count('?')
    k = total / 1000
    chapters = len(re.findall(r'第[一二三四五六七八九十百千\d]+[章回节]', text))
    if chapters < 2: chapters = max(1, total // 3000)
    sentences = [s.strip() for s in re.split(r'[。！？…]+', text) if len(re.sub(r'\s','',s))>5]
    lengths = [len(re.sub(r'\s','',s)) for s in sentences]
    avg = sum(lengths)/len(lengths) if lengths else 0
    long_pct = sum(1 for l in lengths if l>30)/len(lengths)*100 if lengths else 0
    seem = (text.count('似乎')+text.count('好像')+text.count('仿佛')) / (total/10000)
    maybe = (text.count('可能')+text.count('也许')+text.count('或许')) / (total/10000)
    return dict(chars=total, ck=comma/k, pk=period/k, ek=excl/k, lk=ellipsis/k, qk=quest/k,
                avg=avg, long=long_pct, seem=seem, maybe=maybe)

author_map = {
    '光明纪元':'血红','开天录':'血红','逆龙道':'血红','偷天':'血红','邪龙道':'血红',
    '三界血歌':'血红','升龙道':'血红',
    '斗破苍穹':'天蚕土豆','斗破苍穹2':'天蚕土豆','武动乾坤':'天蚕土豆','大主宰':'天蚕土豆','元尊':'天蚕土豆','魔兽剑圣异界纵横':'天蚕土豆',
    '佛本是道':'梦入神机','美漫法神':'梦入神机','圣王':'梦入神机','星河大帝':'梦入神机','点道为止':'梦入神机','龙蛇演义':'梦入神机',
    '苟在妖武乱世修仙':'文抄公','诡秘如风常伴吾身':'文抄公','轮回大劫主':'文抄公','神秀之主':'文抄公','神秘之劫':'文抄公',
    '香火成神道':'文抄公','巫界术士':'文抄公','逍遥梦路':'文抄公','主神崛起':'文抄公','星空职业者':'文抄公',
    '汉阙':'榴弹怕水','秦吏':'榴弹怕水','绍宋':'榴弹怕水',
    '极道天魔':'滚开','十方武圣':'滚开','万千之心':'滚开','我的属性修行人生':'滚开','神秘之旅':'滚开','隐秘死角':'滚开',
    '万族之劫':'老鹰吃小鸡','圣王':'梦入神机','唐砖':'孑与2',
    '吞噬星空':'我吃西红柿','莽荒纪':'我吃西红柿','盘龙':'我吃西红柿','九鼎记':'我吃西红柿','星辰变':'我吃西红柿','雪鹰领主':'我吃西红柿','沧元图':'我吃西红柿','飞剑问道':'我吃西红柿','星峰传说':'我吃西红柿','星空职业者':'文抄公',
    '史上第一祖师爷':'八月飞鹰','史上最强师兄':'八月飞鹰',
    '我真是族长':'孤独漂流','传奇族长':'孤独漂流','人道崛起':'孤独漂流',
    '人皇纪':'皇甫奇','帝御山河':'皇甫奇','飞升之后':'皇甫奇','大周皇族':'皇甫奇',
    '明克街13号':'纯洁滴小龙',
    '夜的命名术':'肘子',
    '我师兄实在太稳健了':'言归正传',
    '玩家请自重':'熊狼狗',
    '巫颂':'血红',
    '异常生物见闻录':'远瞳','黎明之剑':'远瞳',
    '剑来':'烽火戏诸侯',
    '太阳王之证':'汉朝天子',
    '冒牌大英雄':'七十二编',
    '巫师之旅':'一行白鹭',
    '蛊惑魔王':'蛊惑',
    '战锤神印':'天子',
    '哈利波特之学霸传奇':'白开水',
    '大荒蛮神':'更俗',
    '诡秘之主':'乌贼',
    '黄龙真人异界游':'唐家三少',
}

results = {}
for f in sorted(os.listdir(D)):
    if not f.endswith('.txt') or 'fingerprint' in f or 'results' in f:
        continue
    name = f.replace('.txt', '')
    if name == '斗破苍穹2': name = '斗破苍穹'  # skip duplicate
    if name in results: continue
    text = read_file(os.path.join(D, f))
    if text:
        r = analyze(text)
        if r:
            author = author_map.get(name, '？')
            results[name] = (author, r)

sorted_r = sorted(results.items(), key=lambda x: x[1][1]['chars'], reverse=True)

print(f"{'作者':<8} {'小说':<16} {'字数':>4} {'逗号':>6} {'句号':>6} {'感叹':>6} {'省略':>6} {'问号':>6} {'均句':>4} {'长句%':>5} {'似乎':>4} {'可能':>4}")
print("-" * 100)
for name, (author, r) in sorted_r:
    print(f"{author:<8} {name:<16} {r['chars']/10000:>3.0f}万 {r['ck']:>5.1f} {r['pk']:>5.1f} {r['ek']:>5.2f} {r['lk']:>5.2f} {r['qk']:>5.1f} {r['avg']:>3.0f} {r['long']:>4.1f}% {r['seem']:>3.1f} {r['maybe']:>3.1f}")

# 天蚕土豆 evolution
print("\n\n=== 天蚕土豆进化 ===")
for name in ['魔兽剑圣异界纵横','斗破苍穹','武动乾坤','大主宰','元尊']:
    if name in results:
        _, r = results[name]
        print(f"  {name}: 感叹{r['ek']:.2f} 省略{r['lk']:.2f} 均句{r['avg']:.0f} 长句{r['long']:.1f}%")
