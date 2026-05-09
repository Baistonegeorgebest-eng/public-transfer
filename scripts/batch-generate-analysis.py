#!/usr/bin/env python3
"""批量生成小说标点指纹分析报告"""
import os, re, json, statistics, sys

NOVEL_DIR = "/root/.openclaw/workspace/public-transfer-master/novel-txts"
OUTPUT_DIR = "/root/.openclaw/workspace/public-transfer-master/novel-corpus-analysis"

def read_file(filepath):
    for enc in ['utf-8', 'gbk', 'gb18030', 'gb2312']:
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
    med_sent = statistics.median(lengths) if lengths else 0
    std_sent = statistics.stdev(lengths) if len(lengths) > 1 else 0
    cov = std_sent / avg_sent if avg_sent > 0 else 0

    long30 = sum(1 for l in lengths if l > 30) / len(lengths) * 100 if lengths else 0
    long50 = sum(1 for l in lengths if l > 50) / len(lengths) * 100 if lengths else 0
    short10 = sum(1 for l in lengths if l <= 10) / len(lengths) * 100 if lengths else 0

    cn_quote = text.count('「') + text.count('『') + text.count('"')
    dialogue_lines = cn_quote // 2
    dialogue_pct = min(95, dialogue_lines / max(1, para) * 100)

    seem = (text.count('似乎') + text.count('好像') + text.count('仿佛')) / (total / 10000)
    maybe = (text.count('可能') + text.count('也许') + text.count('或许')) / (total / 10000)
    suddenly = text.count('突然')

    paras = [p.strip() for p in text.split('\n') if len(re.sub(r'\s','',p)) > 10]
    para_lengths = [len(re.sub(r'\s','',p)) for p in paras]
    avg_para = sum(para_lengths) / len(para_lengths) if para_lengths else 0

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
        suddenly=suddenly,
        avg_para=round(avg_para, 1),
        emotion_density=round(emotion_density, 1),
    )

def classify_style(r):
    """根据指纹数据判断写作风格标签"""
    tags = []
    if r['avg_sent'] >= 40:
        tags.append('长句型')
    elif r['avg_sent'] <= 20:
        tags.append('短句型')
    else:
        tags.append('中句型')

    if r['ek'] >= 5:
        tags.append('高感叹')
    elif r['ek'] <= 1:
        tags.append('低感叹')

    if r['lk'] >= 3:
        tags.append('高省略')
    elif r['lk'] <= 0.5:
        tags.append('低省略')

    if r['long30'] >= 50:
        tags.append('长句密集')
    if r['short10'] >= 30:
        tags.append('短句密集')

    if r['dialogue_pct'] >= 40:
        tags.append('对话密集')
    elif r['dialogue_pct'] <= 15:
        tags.append('叙述为主')

    if r['emotion_density'] >= 8:
        tags.append('情绪饱满')
    elif r['emotion_density'] <= 3:
        tags.append('情绪克制')

    return tags

def position_metric(value, low, high):
    """定位指标在区间中的位置"""
    if value < low:
        return '低'
    elif value > high:
        return '高'
    else:
        return '中'

def generate_report(r):
    """生成 markdown 分析报告"""
    tags = classify_style(r)
    chars_wan = r['chars'] / 10000

    report = f"""# 《{r['name']}》标点指纹分析报告

**字数**：{chars_wan:.0f}万字  
**章节数**：约{r['chapters']}章  
**分析日期**：2026-04-27

---

## 一、标点指纹

| 指标 | 本作 | 定位 |
|------|------|------|
| 逗号 | {r['ck']}/千字 | {position_metric(r['ck'], 40, 80)} |
| 句号 | {r['pk']}/千字 | {position_metric(r['pk'], 10, 25)} |
| 感叹号 | {r['ek']}/千字 | {'高(>5)' if r['ek']>=5 else '甜点区间(2-5)' if r['ek']>=2 else '低(<2)'} |
| 省略号 | {r['lk']}/千字 | {'高(>3)' if r['lk']>=3 else '中(1-3)' if r['lk']>=1 else '低(<1)'} |
| 问号 | {r['qk']}/千字 | {position_metric(r['qk'], 3, 7)} |
| 破折号 | {r['dk']}/千字 | {position_metric(r['dk'], 1, 4)} |
| 均句长 | {r['avg_sent']}字 | {'偏长(>35)' if r['avg_sent']>35 else '适中(25-35)' if r['avg_sent']>25 else '偏短(<25)'} |
| 中位句长 | {r['med_sent']}字 | |
| 长句(>30字) | {r['long30']}% | {'高' if r['long30']>50 else '中' if r['long30']>30 else '低'} |
| 超长句(>50字) | {r['long50']}% | |
| 短句(≤10字) | {r['short10']}% | |
| 段均长度 | {r['avg_para']}字 | {'长段落' if r['avg_para']>80 else '中等(40-80)' if r['avg_para']>40 else '短段落'} |
| 情绪密度 | {r['emotion_density']} | {'高(>8)' if r['emotion_density']>8 else '中(5-8)' if r['emotion_density']>5 else '低(<5)'} |
| 感叹/章 | {r['ech']} | |
| 省略/章 | {r['lch']} | |
| 对话占比 | {r['dialogue_pct']}% | {'高' if r['dialogue_pct']>40 else '中' if r['dialogue_pct']>20 else '低'} |
| "似乎"类 | {r['seem']}/万字 | |
| "可能"类 | {r['maybe']}/万字 | |
| "突然" | {r['suddenly']}次 | |

## 二、风格标签

{' / '.join(tags)}

## 三、核心发现

- 句长特征：均句{r['avg_sent']}字，中位{r['med_sent']}字，句长变异系数{r['cov']}
- 情感表达：感叹号密度{r['ek']}/千字，情绪密度{r['emotion_density']}，{'情感表达较为克制' if r['emotion_density']<5 else '情感表达较为充沛' if r['emotion_density']>8 else '情感表达适中'}
- 节奏特征：{'短句为主，节奏明快' if r['avg_sent']<25 else '长句为主，节奏沉稳' if r['avg_sent']>35 else '句长适中，节奏均衡'}
- 对话风格：对话占比约{r['dialogue_pct']}%，{'以对话驱动叙事' if r['dialogue_pct']>40 else '以叙述为主' if r['dialogue_pct']<20 else '对话与叙述平衡'}

## 四、对标点协议的启示

（待与同类作品对比后补充）
"""
    return report

# ===== MAIN =====
# Check if we should only process missing ones
force = '--force' in sys.argv

results = []
processed = 0
skipped = 0
errors = []

novel_files = sorted([f for f in os.listdir(NOVEL_DIR) if f.endswith('.txt')])
print(f"共发现 {len(novel_files)} 个 txt 文件")

for f in novel_files:
    name = f.replace('.txt', '')
    output_path = os.path.join(OUTPUT_DIR, f"analysis-{name}.md")

    if not force and os.path.exists(output_path):
        skipped += 1
        continue

    text = read_file(os.path.join(NOVEL_DIR, f))
    if not text:
        errors.append(f"{name}: 无法读取")
        continue

    r = analyze(text, name)
    if not r:
        errors.append(f"{name}: 内容过短")
        continue

    report = generate_report(r)
    with open(output_path, 'w', encoding='utf-8') as fout:
        fout.write(report)

    results.append(r)
    processed += 1
    wan = r['chars'] / 10000
    print(f"✓ [{processed}] {name} ({wan:.0f}万字) → analysis-{name}.md")

print(f"\n===== 完成 =====")
print(f"新生成: {processed}")
print(f"已跳过: {skipped}")
print(f"失败: {len(errors)}")
if errors:
    for e in errors:
        print(f"  ✗ {e}")

# Save summary JSON
summary = {
    'generated': processed,
    'skipped': skipped,
    'errors': errors,
    'results': results
}
with open(os.path.join(OUTPUT_DIR, 'batch-analysis-summary.json'), 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print(f"\n摘要已保存到 batch-analysis-summary.json")
