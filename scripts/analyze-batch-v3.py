#!/usr/bin/env python3
"""Batch punctuation fingerprint analysis for all novels in novel-txts/"""
import os, re, json

D = "/root/.openclaw/workspace/novel-txts"

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

def analyze(text, name):
    total = len(re.sub(r'\s', '', text))
    if total < 10000:
        return None

    comma = text.count('，') + text.count(',')
    period = text.count('。') + text.count('.')
    excl = text.count('！') + text.count('!')
    ellipsis = text.count('……')
    quest = text.count('？') + text.count('?')
    dash = text.count('——')
    para = max(1, text.count('\n'))

    k = total / 1000
    chapters = len(re.findall(r'第[一二三四五六七八九十百千\d]+[章回节]', text))
    if chapters < 2:
        chapters = max(1, total // 3000)

    sentences = [s.strip() for s in re.split(r'[。！？…]+', text) if len(re.sub(r'\s','',s)) > 5]
    lengths = [len(re.sub(r'\s','',s)) for s in sentences]
    avg_sent = sum(lengths) / len(lengths) if lengths else 0

    import statistics
    med_sent = statistics.median(lengths) if lengths else 0
    std_sent = statistics.stdev(lengths) if len(lengths) > 1 else 0
    cov = std_sent / avg_sent if avg_sent > 0 else 0  # coefficient of variation

    long30 = sum(1 for l in lengths if l > 30) / len(lengths) * 100 if lengths else 0
    long50 = sum(1 for l in lengths if l > 50) / len(lengths) * 100 if lengths else 0
    short10 = sum(1 for l in lengths if l <= 10) / len(lengths) * 100 if lengths else 0

    # Dialogue estimation (lines with quotes)
    cn_quote = text.count('「') + text.count('『') + text.count('"')
    dialogue_lines = cn_quote // 2  # rough estimate
    dialogue_pct = min(95, dialogue_lines / max(1, para) * 100)

    # Specific words
    seem = (text.count('似乎') + text.count('好像') + text.count('仿佛')) / (total / 10000)
    maybe = (text.count('可能') + text.count('也许') + text.count('或许')) / (total / 10000)
    grey = text.count('灰色') + text.count('灰色的')
    stuff = text.count('什么东西')
    suddenly = text.count('突然')

    # Paragraph length
    paras = [p.strip() for p in text.split('\n') if len(re.sub(r'\s','',p)) > 10]
    para_lengths = [len(re.sub(r'\s','',p)) for p in paras]
    avg_para = sum(para_lengths) / len(para_lengths) if para_lengths else 0

    # Emotion density per 1000 chars
    emotion_density = (excl + quest) / k

    return dict(
        name=name, chars=total, chapters=chapters,
        ck=round(comma/k, 1), pk=round(period/k, 1),
        ek=round(excl/k, 2), lk=round(ellipsis/k, 2),
        qk=round(quest/k, 1), dk=round(dash/k, 1),
        ech=round(excl/max(chapters,1), 1), lch=round(ellipsis/max(chapters,1), 1),
        avg_sent=round(avg_sent, 1), med_sent=round(med_sent, 1),
        cov=round(cov, 3),
        long30=round(long30, 1), long50=round(long50, 1), short10=round(short10, 1),
        dialogue_pct=round(min(65, dialogue_pct), 1),
        seem=round(seem, 1), maybe=round(maybe, 1),
        grey=grey, stuff=stuff, suddenly=suddenly,
        avg_para=round(avg_para, 1),
        emotion_density=round(emotion_density, 1),
    )

author_map = {
    '逆龙道': '血红', '偷天': '血红', '邪龙道': '血红',
    '光明纪元': '血红', '开天录': '血红',
    '太阳王之证': '汉朝天子',
    '暗影神座': '游戏文', '暴风法神': '游戏文',
    '不死武皇': '妖月夜',
    '沧元图': '我吃西红柿',
    '超凡黎明': '文抄公',
    '传奇族长': '孤独漂流',
    '寸芒': '我吃西红柿',
    '大奉打更人': '卖报小郎君',
    '大荒蛮神': '更俗',
    '大周皇族': '皇甫奇',
    '大主宰': '天蚕土豆',
}

results = []
for f in sorted(os.listdir(D)):
    if not f.endswith('.txt'):
        continue
    name = f.replace('.txt', '')
    text = read_file(os.path.join(D, f))
    if text:
        r = analyze(text, name)
        if r:
            r['author'] = author_map.get(name, '？')
            results.append(r)
            print(f"✓ {name} ({r['chars']/10000:.0f}万字)")
        else:
            print(f"✗ {name}: too short or empty")
    else:
        print(f"✗ {name}: cannot read")

# Sort by chars desc
results.sort(key=lambda x: x['chars'], reverse=True)

# Print table
print(f"\n{'作者':<8} {'小说':<14} {'字数':>4} {'逗号':>6} {'句号':>6} {'感叹':>6} {'省略':>6} {'问号':>6} {'破折':>6} {'均句':>5} {'中位':>5} {'CoV':>5} {'长30':>5} {'长50':>5} {'短10':>5} {'!/章':>5} {'…/章':>5} {'似乎':>5} {'可能':>5} {'段均':>5} {'情绪':>5}")
print("-" * 140)
for r in results:
    print(f"{r['author']:<8} {r['name']:<14} {r['chars']/10000:>3.0f}万 {r['ck']:>5.1f} {r['pk']:>5.1f} {r['ek']:>5.2f} {r['lk']:>5.2f} {r['qk']:>5.1f} {r['dk']:>5.1f} {r['avg_sent']:>4.0f} {r['med_sent']:>4.0f} {r['cov']:>4.2f} {r['long30']:>4.1f}% {r['long50']:>4.1f}% {r['short10']:>4.1f}% {r['ech']:>4.1f} {r['lch']:>4.1f} {r['seem']:>4.1f} {r['maybe']:>4.1f} {r['avg_para']:>4.0f} {r['emotion_density']:>4.1f}")

# Save JSON
with open(os.path.join(D, 'fingerprint-results.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n总计分析 {len(results)} 本小说")
print(f"结果已保存到 {D}/fingerprint-results.json")
