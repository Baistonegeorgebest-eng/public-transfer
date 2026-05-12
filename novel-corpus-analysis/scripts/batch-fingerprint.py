#!/usr/bin/env python3
"""
批量指纹提取 + 分析报告生成
处理 14 本有 txt 无指纹的小说
"""
import os, re, json, math

NOVELS = [
    ("临渊行.txt", "临渊行", "宅猪"),
    ("丹武至尊.txt", "丹武至尊", "顽石"),
    ("丹药修改器.txt", "丹药修改器", "海千星河"),
    ("史上最强炼丹师.txt", "史上最强炼丹师", "丑八佰"),
    ("择日飞升.txt", "择日飞升", "宅猪"),
    ("浪迹在武侠世界的道士.txt", "浪迹在武侠世界的道士", "中原五百"),
    ("游方道士.txt", "游方道士", "小小小柠檬"),
    ("漫威蜘蛛侠：纵横宇宙.txt", "漫威蜘蛛侠：纵横宇宙", "子婴不当王"),
    ("猎魔人在霍格沃茨.txt", "猎魔人在霍格沃茨", "浅墨留香"),
    ("猎魔烹饪手册.txt", "猎魔烹饪手册", "颓废龙"),
    ("电影系统逍遥游.txt", "电影系统逍遥游", "渔歌飘渺"),
    ("霍格沃茨之巫师至上.txt", "霍格沃茨之巫师至上", "荆五"),
    ("霍格沃茨之血脉巫师.txt", "霍格沃茨之血脉巫师", "纯洁小天使"),
    ("牧神记.txt", "牧神记", "宅猪"),
]

TXT_DIR = "novel-txts"
OUT_DIR = "novel-corpus-analysis"

def read_novel(filepath):
    """Read novel with encoding detection."""
    for enc in ['utf-8', 'gbk', 'gb18030', 'gb2312']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                text = f.read()
            return text
        except:
            continue
    with open(filepath, 'rb') as f:
        raw = f.read()
    return raw.decode('gbk', errors='replace')

def analyze(filepath, name, author):
    """Full fingerprint analysis."""
    text = read_novel(filepath)
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Char count (no whitespace)
    chars = len(re.sub(r'\s', '', text))
    wan = round(chars / 10000, 0)

    # Punctuation counts
    comma = text.count('，')
    period = text.count('。')
    excl = text.count('！')
    ellipsis = text.count('……')
    question = text.count('？')

    # Per-1000-char rates
    ck = comma / chars * 1000 if chars else 0
    pk = period / chars * 1000 if chars else 0
    ek = excl / chars * 1000 if chars else 0
    lk = ellipsis / chars * 1000 if chars else 0
    qk = question / chars * 1000 if chars else 0

    # Sentence analysis
    sentences = re.split(r'[。！？]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 2]
    if sentences:
        sent_lengths = [len(re.sub(r'\s', '', s)) for s in sentences]
        avg_sent = sum(sent_lengths) / len(sent_lengths)
        med_sent = sorted(sent_lengths)[len(sent_lengths)//2]
        long30 = sum(1 for l in sent_lengths if l > 30) / len(sent_lengths) * 100
        short10 = sum(1 for l in sent_lengths if l < 10) / len(sent_lengths) * 100
    else:
        avg_sent = med_sent = long30 = short10 = 0
        sent_lengths = []

    # Paragraph analysis
    paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 10]
    if paragraphs:
        para_lengths = [len(re.sub(r'\s', '', p)) for p in paragraphs]
        avg_para = sum(para_lengths) / len(para_lengths)
    else:
        avg_para = 0

    # Chapter count
    chapters = len(re.findall(r'第[一二三四五六七八九十百千\d]+章', text))

    # Sentence length CoV
    if len(sent_lengths) > 1:
        mean_sl = avg_sent
        variance = sum((x - mean_sl)**2 for x in sent_lengths) / len(sent_lengths)
        cov = (variance ** 0.5) / mean_sl if mean_sl else 0
    else:
        cov = 0

    # Emotion density
    emotion_density = (excl + question + ellipsis) / max(len(paragraphs), 1) * 1000

    # Exclamation per chapter
    excl_per_chapter = excl / max(chapters, 1)
    ellipsis_per_chapter = ellipsis / max(chapters, 1)

    # Dialogue ratio (lines with quotes)
    dialogue_lines = len(re.findall(r'[""「」『』]', text))
    dialogue_density = dialogue_lines / chars * 1000 if chars else 0

    return {
        'name': name,
        'author': author,
        'chars': chars,
        'wan': int(wan),
        'chapters': chapters,
        'ck': round(ck, 1),
        'pk': round(pk, 1),
        'ek': round(ek, 2),
        'lk': round(lk, 2),
        'qk': round(qk, 1),
        'avg_sent': round(avg_sent, 1),
        'med_sent': round(med_sent, 1),
        'cov': round(cov, 3),
        'long30': round(long30, 1),
        'short10': round(short10, 1),
        'avg_para': round(avg_para, 1),
        'emotion_density': round(emotion_density, 1),
        'excl_per_chapter': round(excl_per_chapter, 1),
        'ellipsis_per_chapter': round(ellipsis_per_chapter, 1),
        'dialogue_density': round(dialogue_density, 1),
    }

def classify(val, thresholds):
    """Classify a value into low/medium/high etc."""
    for label, lo, hi in thresholds:
        if lo <= val < hi:
            return label
    return thresholds[-1][0]

def generate_report(r):
    """Generate analysis markdown report."""
    # Classifications
    excl_class = classify(r['ek'], [
        ("极低(0-2)", 0, 2), ("低(2-5)", 2, 5), ("中等(5-10)", 5, 10),
        ("高(10-15)", 10, 15), ("极高(>15)", 15, 100)
    ])
    sent_class = "偏长" if r['avg_sent'] > 35 else ("中等" if r['avg_sent'] > 25 else "偏短")
    long30_class = "高" if r['long30'] > 50 else ("中等" if r['long30'] > 30 else "低")
    ellipsis_class = classify(r['lk'], [
        ("极少(<1)", 0, 1), ("低(1-3)", 1, 3), ("中等(3-5)", 3, 5),
        ("高(5-8)", 5, 8), ("极高(>8)", 8, 100)
    ])

    md = f"""# {r['name']} 标点指纹分析

> 作者：{r['author']} | 字数：{r['wan']}万 | 全本实测
> 分析时间：2026-04-27

---

## 一、标点指纹

| 指标 | 本作 | 定位 |
|------|------|------|
| 逗号 | {r['ck']}/千字 | |
| 句号 | {r['pk']}/千字 | |
| 感叹 | {r['ek']}/千字 | {excl_class} |
| 省略 | {r['lk']}/千字 | {ellipsis_class} |
| 问号 | {r['qk']}/千字 | |
| 均句长 | {r['avg_sent']}字 | {sent_class} |
| 长句(>30) | {r['long30']}% | {long30_class} |
| 段均 | {r['avg_para']}字 | |
| 情绪密度 | {r['emotion_density']} | |
| 感叹/章 | {r['excl_per_chapter']} | |
| 省略/章 | {r['ellipsis_per_chapter']} | |

## 二、核心发现

- 逗号密度 {r['ck']}/千字，{'逗号主导型节奏' if r['ck'] > 60 else '逗号节奏适中' if r['ck'] > 40 else '逗号密度偏低'}
- 感叹号 {r['ek']}/千字，{excl_class}
- 均句长 {r['avg_sent']}字，{sent_class}
- 长句比例 {r['long30']}%，{long30_class}

## 三、对协议的启示

（待深度分析补充）
"""
    return md

def main():
    results = []
    table_rows = []

    for filename, name, author in NOVELS:
        filepath = os.path.join(TXT_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  [SKIP] {filepath} not found")
            continue

        print(f"  [PROCESSING] {name} ({author})...")
        r = analyze(filepath, name, author)
        results.append(r)

        # Generate analysis report
        report = generate_report(r)
        report_path = os.path.join(OUT_DIR, f"analysis-{name}.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"    -> Report: {report_path}")

        # Table row: # | author | name | wan万 | ck | pk | ek | lk | qk | avg_sent | long30% | welfare | vip
        table_rows.append(
            f"| {r['wan']}万 | {r['ck']} | {r['pk']} | {r['ek']} | {r['lk']} | {r['qk']} | {r['avg_sent']} | {r['long30']}% | 0.0 | 0.00 |"
        )

    # Save JSON
    json_path = os.path.join(TXT_DIR, "fingerprint-new-14.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n  [SAVED] {json_path}")

    # Print fingerprint table rows
    print("\n=== FINGERPRINT TABLE ROWS (to append to v4.3) ===")
    for i, (r, row) in enumerate(zip(results, table_rows), 1):
        print(f"| NEW{i} | {r['author']} | {r['name']} {row}")

    # Print summary
    print(f"\n=== SUMMARY ===")
    print(f"Processed: {len(results)} novels")
    for r in results:
        print(f"  {r['name']}: {r['wan']}万字, 逗号{r['ck']}, 句号{r['pk']}, 感叹{r['ek']}, 均句{r['avg_sent']}字, 长句{r['long30']}%")

if __name__ == "__main__":
    main()
