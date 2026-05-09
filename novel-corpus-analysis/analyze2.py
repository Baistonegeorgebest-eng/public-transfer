#!/usr/bin/env python3
"""Punctuation fingerprint - handles GBK/UTF-8 encoding."""
import os, re

D = "/root/.openclaw/workspace/novel-corpus"

def read_file(filepath):
    for enc in ['utf-8', 'gbk', 'gb18030', 'gb2312']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                text = f.read()
            # Sanity check: should have common Chinese chars
            if '的' in text[:1000] or '章' in text[:2000]:
                return text
        except:
            continue
    return None

def analyze(text):
    total_chars = len(re.sub(r'\s', '', text))
    if total_chars < 1000:
        return None
    
    # Punctuation (full-width Chinese + half-width)
    comma = text.count('，') + text.count(',')
    period = text.count('。') + text.count('.')
    exclamation = text.count('！') + text.count('!')
    ellipsis = text.count('……')  # Count double-ellipsis as one unit
    ellipsis_single = text.count('…')
    question = text.count('？') + text.count('?')
    
    k = total_chars / 1000
    
    # Dialogue detection
    dialogue_chars = 0
    for op, cl in [('「', '」'), ('\u300c', '\u300d'), ('"', '"'), ('"', '"')]:
        stack = 0
        for ch in text:
            if ch == op:
                stack += 1
            elif ch == cl and stack > 0:
                stack -= 1
                dialogue_chars += 1  # rough: count close brackets as dialogue marker
    # Better: measure text between Chinese quotes
    dq = len(re.findall(r'「[^」]{2,}」', text)) + len(re.findall(r'「[^」]{2,}」', text))
    dq_chars = sum(len(m) for m in re.findall(r'「[^」]+」', text))
    dialogue_pct = (dq_chars / total_chars * 100) if total_chars > 0 else 0
    
    # Chapter count
    chapters = len(re.findall(r'第[一二三四五六七八九十百千\d]+[章回节]', text))
    if chapters == 0:
        chapters = len(re.findall(r'(?m)^chapter\s*\d+', text, re.IGNORECASE))
    if chapters < 2:
        chapters = max(1, total_chars // 3000)
    
    # Sentence length
    sentences = re.split(r'[。！？…]+', text)
    sentences = [s.strip() for s in sentences if len(re.sub(r'\s', '', s)) > 5]
    if sentences:
        lengths = [len(re.sub(r'\s', '', s)) for s in sentences]
        avg_sent = sum(lengths) / len(lengths)
        long_pct = sum(1 for l in lengths if l > 30) / len(lengths) * 100
        median_sent = sorted(lengths)[len(lengths)//2]
    else:
        avg_sent = long_pct = median_sent = 0
    
    # Uncertainty words
    seem = text.count('似乎') + text.count('好像') + text.count('仿佛')
    maybe = text.count('可能') + text.count('也许') + text.count('或许')
    tenk = total_chars / 10000
    
    return {
        'chars': total_chars, 'chapters': chapters,
        'comma_k': comma/k, 'period_k': period/k,
        'excl_k': exclamation/k, 'ellipsis_k': ellipsis/k,
        'quest_k': question/k,
        'excl_ch': exclamation/max(chapters,1),
        'ell_ch': ellipsis/max(chapters,1),
        'dialogue_pct': dialogue_pct,
        'avg_sent': avg_sent, 'long_pct': long_pct, 'median_sent': median_sent,
        'seem': seem/tenk, 'maybe': maybe/tenk,
    }

# Process all files
results = {}
for f in sorted(os.listdir(D)):
    if not f.endswith('.txt'):
        continue
    path = os.path.join(D, f)
    name = f.replace('.txt', '')
    text = read_file(path)
    if text:
        r = analyze(text)
        if r:
            results[name] = r
            print(f"OK: {name} ({r['chars']/10000:.0f}万字)")
    else:
        print(f"FAIL: {name}")

print()
print(f"{'小说':<18} {'字数':>5} {'逗号':>6} {'句号':>6} {'感叹':>6} {'省略':>6} {'问号':>6} {'对白%':>5} {'均句':>4} {'长句%':>5} {'!/章':>5} {'…/章':>5} {'似乎':>4} {'可能':>4}")
print("-" * 120)
for name in sorted(results.keys(), key=lambda x: results[x]['chars'], reverse=True):
    r = results[name]
    print(f"{name:<18} {r['chars']/10000:>4.0f}万 {r['comma_k']:>5.1f} {r['period_k']:>5.1f} {r['excl_k']:>5.2f} {r['ellipsis_k']:>5.1f} {r['quest_k']:>5.1f} {r['dialogue_pct']:>4.1f}% {r['avg_sent']:>3.0f} {r['long_pct']:>4.1f}% {r['excl_ch']:>4.1f} {r['ell_ch']:>4.1f} {r['seem']:>3.1f} {r['maybe']:>3.1f}")

print("\n=== PROTOCOL TABLE ROWS ===")
for name in sorted(results.keys(), key=lambda x: results[x]['chars'], reverse=True):
    r = results[name]
    # Determine author
    author_map = {
        '光明纪元': '血红', '开天录': '血红', '逆龙道': '血红', '偷天': '血红', '邪龙道': '血红',
        '斗破苍穹': '天蚕土豆', '佛本是道': '梦入神机', '龙蛇演义': '梦入神机',
        '苟在妖武乱世修仙': '文抄公', '诡秘如风常伴吾身': '文抄公', '超凡黎明': '文抄公',
        '轮回大劫主': '文抄公', '汉阙': '榴弹怕水', '秦吏': '榴弹怕水',
        '极道天魔': '滚开', '美漫法神': '梦入神机', '明克街13号': '纯洁滴小龙',
        '莽荒纪': '我吃西红柿', '盘龙': '我吃西红柿', '九鼎记': '我吃西红柿',
        '人道崛起': '孤独漂流', '人皇纪': '皇甫奇', '黄龙真人异界游': '梦入神机',
    }
    author = author_map.get(name, '待定')
    print(f"| {author}({name}) | {r['comma_k']:.1f} | {r['period_k']:.1f} | {r['excl_k']:.2f} | {r['ellipsis_k']:.2f} | {r['dialogue_pct']:.1f} | 待补充 |")
