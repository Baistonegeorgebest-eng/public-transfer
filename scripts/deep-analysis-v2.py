#!/usr/bin/env python3
"""
deep-analysis-v2.py — 四合一深度分析脚本
功能：
  1. 单本深度分析 (single)   → analysis-{name}-deep.md
  2. 作者进化分析 (evolution) → analysis-{author}进化-deep.md
  3. 感官库提取   (sensory)   → sensory-extraction-{genre}.md
  4. 福利感官扫描 (welfare)   → welfare-scan-results.md

用法：
  python3 deep-analysis-v2.py single <小说名>        # 单本深度
  python3 deep-analysis-v2.py single --all           # 全量单本深度
  python3 deep-analysis-v2.py evolution <作者名>     # 作者进化
  python3 deep-analysis-v2.py evolution --all        # 全量作者进化
  python3 deep-analysis-v2.py sensory <小说名>       # 单本感官提取
  python3 deep-analysis-v2.py sensory --all          # 全量感官提取
  python3 deep-analysis-v2.py welfare <小说名>       # 单本福利扫描
  python3 deep-analysis-v2.py welfare --all          # 全量福利扫描
  python3 deep-analysis-v2.py batch                  # 全量四合一
"""

import os, re, sys, json, statistics
from collections import defaultdict, Counter
from datetime import datetime

# ============================================================
# 配置
# ============================================================
NOVEL_DIR = "/root/public-transfer/novel-txts"
OUTPUT_DIR = "/root/public-transfer/novel-corpus-analysis"
AUTHOR_MAP_FILE = os.path.join(OUTPUT_DIR, "author-map.json")

# 全库均值基线（来自 fingerprint-table-v4.4）
BASELINE = dict(
    ck=60, pk=25, ek=3.0, lk=1.5, qk=4.0, dk=2.0,
    avg_sent=30, long30=40, short10=15, avg_para=60
)

# ============================================================
# 工具函数
# ============================================================

def read_file(filepath):
    """读取小说文件，自动检测编码（含BOM检测）"""
    # 先读取原始字节检测BOM
    with open(filepath, 'rb') as f:
        raw_head = f.read(4)
    
    # BOM检测
    if raw_head[:2] == b'\xff\xfe':
        enc_order = ['utf-16-le']
    elif raw_head[:2] == b'\xfe\xff':
        enc_order = ['utf-16-be']
    elif raw_head[:3] == b'\xef\xbb\xbf':
        enc_order = ['utf-8-sig']
    else:
        enc_order = ['utf-8', 'gbk', 'gb18030', 'gb2312', 'utf-16-le', 'utf-16-be', 'latin-1']
    
    for enc in enc_order:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                text = f.read()
            # 验证是否成功解码出中文（严格检查）
            sample = text[:3000]
            cn_count = sum(1 for c in sample if '\u4e00' <= c <= '\u9fff')
            # 至少5%是中文字符才算有效
            if cn_count > len(sample) * 0.05:
                return text
        except:
            continue
    
    # 最后兜底：errors=replace
    for enc in ['utf-8', 'gbk', 'gb18030']:
        try:
            with open(filepath, 'r', encoding=enc, errors='replace') as f:
                text = f.read()
            if len(text) > 1000:
                return text
        except:
            continue
    return None


def extract_novel_name(filename):
    """从文件名提取小说名（去掉编号前缀和.txt后缀）"""
    name = filename.replace('.txt', '')
    name = re.sub(r'^\d+[\.\-_]?\s*', '', name)
    return name


def get_chapters(text):
    """提取章节列表（起始位置）"""
    pattern = r'第[一二三四五六七八九十百千\d]+[章回节]'
    matches = list(re.finditer(pattern, text))
    if len(matches) < 2:
        step = 3000
        return [(i, i+step) for i in range(0, len(text), step)]
    chapters = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        chapters.append((start, end))
    return chapters


# ============================================================
# 核心分析引擎
# ============================================================

def punctuation_fingerprint(text, total_chars):
    """标点指纹提取"""
    k = total_chars / 1000
    return dict(
        ck=round((text.count('，') + text.count(',')) / k, 1),
        pk=round((text.count('。') + text.count('.')) / k, 1),
        ek=round((text.count('！') + text.count('!')) / k, 2),
        lk=round(text.count('……') / k, 2),
        qk=round((text.count('？') + text.count('?')) / k, 1),
        dk=round(text.count('——') / k, 1),
    )


def sentence_analysis(text):
    """句长分析"""
    sentences = [s.strip() for s in re.split(r'[。！？…]+', text) if len(re.sub(r'\s', '', s)) > 5]
    if not sentences:
        return dict(avg_sent=0, med_sent=0, cov=0, long30=0, long50=0, short10=0, sent_count=0)
    lengths = [len(re.sub(r'\s', '', s)) for s in sentences]
    avg = sum(lengths) / len(lengths)
    med = statistics.median(lengths)
    std = statistics.stdev(lengths) if len(lengths) > 1 else 0
    cov = std / avg if avg > 0 else 0
    return dict(
        avg_sent=round(avg, 1),
        med_sent=round(med, 1),
        cov=round(cov, 3),
        long30=round(sum(1 for l in lengths if l > 30) / len(lengths) * 100, 1),
        long50=round(sum(1 for l in lengths if l > 50) / len(lengths) * 100, 1),
        short10=round(sum(1 for l in lengths if l <= 10) / len(lengths) * 100, 1),
        sent_count=len(lengths),
    )


def paragraph_analysis(text):
    """段落分析"""
    paras = [p.strip() for p in text.split('\n') if len(re.sub(r'\s', '', p)) > 10]
    if not paras:
        return dict(avg_para=0, para_count=0)
    lengths = [len(re.sub(r'\s', '', p)) for p in paras]
    avg = sum(lengths) / len(lengths)
    # 安全上限：段均超过5000字大概率是编码/切分问题
    if avg > 5000:
        return dict(avg_para=0, para_count=0)
    return dict(
        avg_para=round(avg, 1),
        para_count=len(paras),
    )


def emotion_curve(text, total_chars, segments=10):
    """情绪密度曲线（感叹号按百分比分段）"""
    step = len(text) // segments
    densities = []
    for i in range(segments):
        start = i * step
        end = (i + 1) * step if i < segments - 1 else len(text)
        chunk = text[start:end]
        chunk_chars = len(re.sub(r'\s', '', chunk))
        if chunk_chars < 100:
            densities.append(0)
            continue
        excl = chunk.count('！') + chunk.count('!')
        densities.append(round(excl / (chunk_chars / 1000), 1))
    return densities


def narrative_features(text, total_chars):
    """叙事特征词频"""
    k10 = total_chars / 10000
    return dict(
        suddenly=round(text.count('突然') / k10, 1),
        seem=round((text.count('似乎') + text.count('好像') + text.count('仿佛')) / k10, 1),
        maybe=round((text.count('可能') + text.count('也许') + text.count('或许')) / k10, 1),
        grey=text.count('灰色') + text.count('灰色的'),
        stuff=text.count('什么东西'),
    )


def dialogue_estimation(text, para_count):
    """对话占比估算"""
    cn_quote = text.count('「') + text.count('『') + text.count('"') + text.count('\u201c')
    dialogue_lines = cn_quote // 2
    pct = min(95, dialogue_lines / max(1, para_count) * 100)
    return round(min(65, pct), 1)


def opening_analysis(text, total_chars):
    """开局分析（前5000字）"""
    chunk = text[:min(5000, len(text))]
    chapters = get_chapters(chunk)
    has_dialogue = bool(re.search(r'["\u201c\u300c\u300e]', chunk[:2000]))
    hook_words = ['忽然', '突然', '难道', '竟然', '没想到', '秘密', '真相', '不为人知',
                  '背后', '隐藏', '诡异', '奇怪', '不可思议', '离奇', '蹊跷']
    has_hook = any(w in chunk for w in hook_words)
    return dict(chapters=len(chapters), has_dialogue=has_dialogue, has_hook=has_hook)


def style_tags(pf, sa, pa, nf):
    """风格标签生成"""
    tags = []
    if sa['avg_sent'] > 40: tags.append('长句型')
    elif sa['avg_sent'] > 28: tags.append('中句型')
    else: tags.append('短句型')
    if pf['ek'] > 10: tags.append('高感叹')
    elif pf['ek'] > 5: tags.append('中感叹')
    else: tags.append('低感叹')
    if pf['lk'] > 3: tags.append('高省略')
    elif pf['lk'] < 0.5: tags.append('低省略')
    if pf['ck'] > 65: tags.append('高逗号')
    if sa['long30'] > 50: tags.append('长句密集')
    if sa['short10'] > 25: tags.append('碎片化')
    if nf['seem'] > 5: tags.append('模糊表达多')
    if nf['suddenly'] > 3: tags.append('节奏突变多')
    return ' / '.join(tags)


def classify_exclamation_usage(text, sample_size=5000):
    """分析感叹号使用类型（采样含感叹号的片段）"""
    # 找到第一个包含感叹号的片段
    chunk = ''
    for i in range(0, len(text), 3000):
        candidate = text[i:i+sample_size]
        if '！' in candidate or '!' in candidate:
            chunk = candidate
            break
    if not chunk:
        chunk = text[:sample_size]
    # 提取包含感叹号的完整句子
    excl_sentences = re.findall(r'[^。！？\n]*[！!][^。！？\n]*', chunk)
    excl_sentences = [s.strip() for s in excl_sentences if s.strip()]
    types = {'emotion': 0, 'rhythm': 0, 'system': 0}
    for s in excl_sentences:
        s = s.strip()
        if not s: continue
        if any(w in s for w in ['系统', '提示', '恭喜', '获得', '升级', '突破', '境界', '功法']):
            types['system'] += 1
        elif any(w in s for w in ['怒', '笑', '哭', '喊', '吼', '喝', '骂', '"', '\u300c']):
            types['emotion'] += 1
        else:
            types['rhythm'] += 1
    total = sum(types.values()) or 1
    return {k: round(v / total * 100, 1) for k, v in types.items()}


# ============================================================
# 感官库提取
# ============================================================

SENSORY_KEYWORDS = {
    '嗅觉': {
        'high': ['香气', '香味', '清香', '气味', '芬芳', '幽香', '浓香', '淡香', '花香', '药味',
                 '腥味', '血腥', '恶臭', '臭味', '汗味', '刺鼻', '腥臭', '臭气'],
        'mid': ['闻到', '闻着', '闻了', '嗅到', '闻起来', '弥漫', '散发', '飘来', '扑面'],
        'patterns': [r'一股.*味', r'一阵.*香', r'弥漫着.*气'],
    },
    '味觉': {
        'high': ['苦涩', '甜美', '甘甜', '酸甜', '辛辣', '鲜美', '美味', '可口', '甘美',
                 '苦味', '甜味', '咸味', '酸味', '辣味', '酒香', '鲜味'],
        'mid': ['入口', '吞下', '咽下', '咀嚼', '品尝', '品味', '味道', '好吃', '吞咽',
                '嚼着', '回味', '尝到', '喝了一口', '吃了一口', '入腹', '舌尖'],
        'patterns': [r'入口.*化', r'满口.*味'],
    },
    '触觉': {
        'high': ['温暖', '冰凉', '滚烫', '寒冷', '冰冷', '炙热', '灼热', '炽热', '温热',
                 '光滑', '粗糙', '柔软', '坚硬', '湿润', '干燥', '细腻', '僵硬', '酥麻',
                 '酸痛', '刺痛', '剧痛', '疼痛', '麻痹', '战栗', '颤抖', '哆嗦', '发抖',
                 '汗毛', '鸡皮疙瘩'],
        'mid': ['抚摸', '触碰', '抓住', '握住', '松开', '指尖', '手指', '手掌', '触摸',
                '触感', '碰到', '摸到', '风吹', '起了一层'],
        'patterns': [r'一阵.*感', r'浑身.*痛'],
    },
    '听觉': {
        'high': ['轰鸣', '咆哮', '嘶吼', '怒吼', '尖叫', '惨叫', '惊呼', '呐喊',
                 '安静', '寂静', '寂然', '沉默', '悄然', '万籁俱寂',
                 '叮当', '砰', '嘭', '哗哗', '咯吱', '嗡鸣', '嘀嗒', '嘎吱'],
        'mid': ['声音', '听到', '听见', '听着', '声响', '低语', '呢喃', '喃喃',
                '嘀咕', '嘟囔', '风声', '脚步声', '震颤'],
        'patterns': [r'阵阵.*声', r'一声.*响'],
    },
    '视觉': {
        'high': ['金色', '银色', '红色', '蓝色', '紫色', '黑色', '白色', '绿色', '青色',
                 '光芒', '光辉', '闪烁', '闪耀', '耀眼', '璀璨', '暗淡', '漆黑', '黑暗',
                 '明亮', '昏暗', '朦胧', '模糊'],
        'mid': ['看到', '看见', '目光', '眼中', '眼前', '望着', '盯着', '注视', '凝视',
                '视线', '远处', '身影', '凝望', '端详', '打量'],
        'patterns': [r'一道.*光', r'一片.*色'],
    },
}

WELFARE_KEYWORDS = {
    'L1_身体部位': ['锁骨', '腰肢', '腰线', '美腿', '长腿', '玉腿', '纤腰', '翘臀',
                   '酥胸', '胸口', '胸前', '胸膛', '脊背', '脖颈', '粉颈', '玉足',
                   '小蛮腰', '马甲线', '人鱼线', '蝴蝶骨', '香肩', '削肩', '天鹅颈',
                   '脚踝', '手腕', '指尖', '大腿', '小腿', '腹部', '小腹'],
    'L2_服饰': ['丝袜', '黑丝', '肉丝', '白丝', '高跟', '高跟鞋', '包臀裙', '短裙',
               '吊带', '内衣', '文胸', '内裤', '蕾丝', '薄纱', '透视', '低胸',
               '紧身', '贴身', '制服', '旗袍', '比基尼', '泳装', '睡衣', '浴袍',
               '长裙', '纱裙', '罗袜', '绣花鞋'],
    'L3_亲密动作': ['搂住', '抱住', '拥入', '揽住', '依偎', '靠在', '挽住',
                   '亲吻', '吻住', '吻上', '唇齿', '舌尖',
                   '抚摸', '轻抚', '摩挲', '揉捏', '指尖划过',
                   '握住', '抓住', '十指相扣', '手心', '掌心'],
    'L4_暧昧反应': ['脸红', '羞红', '绯红', '酡红', '面红耳赤', '霞飞双颊',
                   '心跳加速', '心跳漏拍', '小鹿乱撞', '怦然心动',
                   '喘息', '娇喘', '气息不稳', '呼吸急促',
                   '颤抖', '发软', '酥软', '瘫软', '全身发烫',
                   '呢喃', '低吟', '娇嗔', '嗔怪', '娇羞', '惊呼'],
    'L5_暧昧氛围': ['卧室', '独处', '密室', '只有两人', '二人世界',
                   '温泉', '浴池', '沐浴', '泡澡', '浴缸',
                   '月光', '烛光', '昏暗', '暧昧', '朦胧',
                   '更衣', '换衣', '试衣间', '更衣室',
                   '摔倒', '扑倒', '压在', '不小心'],
    'L6_暗示对话': ['别在这里', '等一下', '别动', '别看', '闭上眼睛',
                   '你想要', '可以吗', '确定吗',
                   '你再这样', '快住手', '不害臊',
                   '忍不了', '就差一点', '好不好'],
    'L7_事后暗示': ['整理衣服', '整理头发', '裹着被子', '被子滑落',
                   '扣上扣子', '撩到耳后', '小跑着离开',
                   '昨晚', '早上好', '清晨'],
}


def extract_sensory(text, total_chars, genre='未分类'):
    """从文本中提取五感描写句"""
    results = {}
    k10 = total_chars / 10000
    for sense, kw in SENSORY_KEYWORDS.items():
        sentences = []
        sents = re.split(r'[。！？\n]', text)
        for s in sents:
            s = s.strip()
            if len(s) < 10 or len(s) > 200:
                continue
            matched = False
            for word in kw['high']:
                if word in s:
                    sentences.append((word, s))
                    matched = True
                    break
            if not matched:
                for word in kw['mid']:
                    if word in s:
                        sentences.append((word, s))
                        matched = True
                        break
            if not matched:
                for pat in kw.get('patterns', []):
                    if re.search(pat, s):
                        sentences.append((pat, s))
                        matched = True
                        break
        word_counts = Counter()
        for word, _ in sentences:
            if word.startswith('.'):
                continue
            word_counts[word] += 1
        results[sense] = {
            'count': len(sentences),
            'density': round(len(sentences) / k10, 1) if k10 > 0 else 0,
            'top_words': word_counts.most_common(10),
            'examples': sentences[:5],
        }
    return results


def extract_welfare(text, total_chars):
    """福利内容扫描"""
    results = {}
    k10 = total_chars / 10000
    for layer, keywords in WELFARE_KEYWORDS.items():
        hits = []
        for kw in keywords:
            count = text.count(kw)
            if count > 0:
                hits.append((kw, count))
        total_hits = sum(c for _, c in hits)
        results[layer] = {
            'total': total_hits,
            'density': round(total_hits / k10, 1) if k10 > 0 else 0,
            'keywords': sorted(hits, key=lambda x: -x[1])[:10],
        }
    total_welfare = sum(r['total'] for r in results.values())
    return {
        'layers': results,
        'total': total_welfare,
        'density': round(total_welfare / k10, 1) if k10 > 0 else 0,
    }


# ============================================================
# 报告生成
# ============================================================

def generate_single_deep_report(name, text, author='未知', genre='未分类'):
    """生成单本深度分析报告"""
    total = len(re.sub(r'\s', '', text))
    if total < 10000:
        return None

    chapters = get_chapters(text)
    pf = punctuation_fingerprint(text, total)
    sa = sentence_analysis(text)
    pa = paragraph_analysis(text)
    ec = emotion_curve(text, total)
    nf = narrative_features(text, total)
    dl = dialogue_estimation(text, pa['para_count'])
    oa = opening_analysis(text, total)
    ex_types = classify_exclamation_usage(text)
    st = style_tags(pf, sa, pa, nf)
    sensory = extract_sensory(text, total, genre)
    welfare = extract_welfare(text, total)

    ch_count = len(chapters)
    words_per_ch = round(total / ch_count) if ch_count > 0 else 0

    def deviation(val, base):
        if base == 0: return '—'
        ratio = val / base
        if ratio > 1.15: return '↑↑' if ratio > 1.3 else '↑'
        elif ratio < 0.85: return '↓↓' if ratio < 0.7 else '↓'
        return '→'

    max_d = max(ec) if ec else 1
    curve_lines = []
    for d in ec:
        bar_len = int(d / max_d * 30) if max_d > 0 else 0
        curve_lines.append(f"  {d:>5.1f}  {'█' * bar_len}")
    curve_chart = '\n'.join(curve_lines)

    report = f"""# {name} 深度分析

> 作者：{author} | 字数：{total/10000:.0f}万 | 章节：{ch_count}章（约{words_per_ch}字/章）
> 分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 全本实测

---

## 一、标点指纹（确认值）

| 指标 | {name} | 全库均值 | 偏差 |
|------|--------|---------|------|
| 感叹 | {pf['ek']}/千字 | ~{BASELINE['ek']} | {deviation(pf['ek'], BASELINE['ek'])} |
| 省略 | {pf['lk']}/千字 | ~{BASELINE['lk']} | {deviation(pf['lk'], BASELINE['lk'])} |
| 逗号 | {pf['ck']}/千字 | ~{BASELINE['ck']} | {deviation(pf['ck'], BASELINE['ck'])} |
| 句号 | {pf['pk']}/千字 | ~{BASELINE['pk']} | {deviation(pf['pk'], BASELINE['pk'])} |
| 问号 | {pf['qk']}/千字 | ~{BASELINE['qk']} | {deviation(pf['qk'], BASELINE['qk'])} |
| 均句 | {sa['avg_sent']}字 | ~{BASELINE['avg_sent']}字 | {deviation(sa['avg_sent'], BASELINE['avg_sent'])} |
| 段均 | {pa['avg_para']}字 | ~{BASELINE['avg_para']}字 | {deviation(pa['avg_para'], BASELINE['avg_para'])} |
| 情绪密度 | {pf['ek']+pf['qk']:.1f} | ~{BASELINE['ek']+BASELINE['qk']:.1f} | {deviation(pf['ek']+pf['qk'], BASELINE['ek']+BASELINE['qk'])} |

## 二、句式分析

| 指标 | 值 |
|------|-----|
| 总句数 | {sa['sent_count']} |
| 均句长 | {sa['avg_sent']}字 |
| 中位句长 | {sa['med_sent']}字 |
| 句长变异系数 | {sa['cov']} |
| 长句(>30字) | {sa['long30']}% |
| 超长句(>50字) | {sa['long50']}% |
| 短句(≤10字) | {sa['short10']}% |
| 对话占比 | {dl}% |

## 三、情绪密度曲线（感叹号/千字，按10%分段）

```
{curve_chart}
```

感叹号使用类型（采样前3000字）：
- 情绪爆发：{ex_types['emotion']}%
- 节奏标记：{ex_types['rhythm']}%
- 系统/设定：{ex_types['system']}%

## 四、风格标签

**{st}**

## 五、叙事特征

- **突然** 出现 {text.count('突然')} 次（{nf['suddenly']}次/万字）
- **似乎/好像/仿佛** 出现 {text.count('似乎')+text.count('好像')+text.count('仿佛')} 次（{nf['seem']}次/万字）
- **可能/也许/或许** 出现 {text.count('可能')+text.count('也许')+text.count('或许')} 次（{nf['maybe']}次/万字）

## 六、开局特征（前5000字）

- 章节数：{oa['chapters']}
- 有悬念钩子：{'✅' if oa['has_hook'] else '❌'}
- 有对话：{'✅' if oa['has_dialogue'] else '❌'}

## 七、感官描写密度

| 感官 | 命中数 | 密度/万字 | 高频词 |
|------|--------|----------|--------|
| 视觉 | {sensory['视觉']['count']} | {sensory['视觉']['density']} | {', '.join(w for w,_ in sensory['视觉']['top_words'][:5])} |
| 听觉 | {sensory['听觉']['count']} | {sensory['听觉']['density']} | {', '.join(w for w,_ in sensory['听觉']['top_words'][:5])} |
| 触觉 | {sensory['触觉']['count']} | {sensory['触觉']['density']} | {', '.join(w for w,_ in sensory['触觉']['top_words'][:5])} |
| 嗅觉 | {sensory['嗅觉']['count']} | {sensory['嗅觉']['density']} | {', '.join(w for w,_ in sensory['嗅觉']['top_words'][:5])} |
| 味觉 | {sensory['味觉']['count']} | {sensory['味觉']['density']} | {', '.join(w for w,_ in sensory['味觉']['top_words'][:5])} |

## 八、福利内容扫描（L1-L7）

| 层级 | 命中数 | 密度/万字 | 主要关键词 |
|------|--------|----------|-----------|
| L1 身体部位 | {welfare['layers']['L1_身体部位']['total']} | {welfare['layers']['L1_身体部位']['density']} | {', '.join(w for w,_ in welfare['layers']['L1_身体部位']['keywords'][:5])} |
| L2 服饰 | {welfare['layers']['L2_服饰']['total']} | {welfare['layers']['L2_服饰']['density']} | {', '.join(w for w,_ in welfare['layers']['L2_服饰']['keywords'][:5])} |
| L3 亲密动作 | {welfare['layers']['L3_亲密动作']['total']} | {welfare['layers']['L3_亲密动作']['density']} | {', '.join(w for w,_ in welfare['layers']['L3_亲密动作']['keywords'][:5])} |
| L4 暧昧反应 | {welfare['layers']['L4_暧昧反应']['total']} | {welfare['layers']['L4_暧昧反应']['density']} | {', '.join(w for w,_ in welfare['layers']['L4_暧昧反应']['keywords'][:5])} |
| L5 暧昧氛围 | {welfare['layers']['L5_暧昧氛围']['total']} | {welfare['layers']['L5_暧昧氛围']['density']} | {', '.join(w for w,_ in welfare['layers']['L5_暧昧氛围']['keywords'][:5])} |
| L6 暗示对话 | {welfare['layers']['L6_暗示对话']['total']} | {welfare['layers']['L6_暗示对话']['density']} | {', '.join(w for w,_ in welfare['layers']['L6_暗示对话']['keywords'][:5])} |
| L7 事后暗示 | {welfare['layers']['L7_事后暗示']['total']} | {welfare['layers']['L7_事后暗示']['density']} | {', '.join(w for w,_ in welfare['layers']['L7_事后暗示']['keywords'][:5])} |
| **总计** | **{welfare['total']}** | **{welfare['density']}** | |

---
_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} GMT+8_
"""
    return report


def generate_evolution_report(author, novels_data):
    """生成作者进化分析报告"""
    if len(novels_data) < 2:
        return None

    novels_data.sort(key=lambda x: x[0])
    total_chars = sum(d[2] for d in novels_data)

    data_rows = []
    for name, text, total, pf, sa, pa, ec, nf, genre in novels_data:
        data_rows.append(dict(
            name=name, chars=total,
            ek=pf['ek'], lk=pf['lk'], ck=pf['ck'], pk=pf['pk'],
            qk=pf['qk'], avg_sent=sa['avg_sent'], long30=sa['long30'],
            avg_para=pa['avg_para'], genre=genre,
        ))

    ek_values = [r['ek'] for r in data_rows]
    lk_values = [r['lk'] for r in data_rows]
    ck_values = [r['ck'] for r in data_rows]
    pk_values = [r['pk'] for r in data_rows]

    def trend_desc(values):
        if len(values) < 2: return '—'
        first, last = values[0], values[-1]
        if last > first * 1.2: return f'↑ {first:.2f}→{last:.2f}'
        elif last < first * 0.8: return f'↓ {first:.2f}→{last:.2f}'
        return f'→ {first:.2f}~{last:.2f}'

    findings = []
    if max(ek_values) > 10:
        findings.append(f"感叹号峰值{max(ek_values):.1f}（{data_rows[ek_values.index(max(ek_values))]['name']}）")
    if min(ek_values) < 0.5:
        findings.append(f"感叹号谷值{min(ek_values):.2f}（{data_rows[ek_values.index(min(ek_values))]['name']}）")
    if max(lk_values) > 4:
        findings.append(f"省略号峰值{max(lk_values):.2f}（{data_rows[lk_values.index(max(lk_values))]['name']}）")
    if max(pk_values) - min(pk_values) > 20:
        findings.append(f"句号波动大：{min(pk_values):.1f}~{max(pk_values):.1f}")
    if max(ck_values) - min(ck_values) > 15:
        findings.append(f"逗号波动大：{min(ck_values):.1f}~{max(ck_values):.1f}")

    table_lines = []
    table_lines.append(f"| {'作品':<14} | {'字数':>5} | {'感叹':>6} | {'省略':>6} | {'逗号':>6} | {'句号':>6} | {'均句':>5} | {'长句%':>5} | {'段均':>5} | {'题材':<8} |")
    table_lines.append(f"|{'-'*16}|{'-'*7}|{'-'*8}|{'-'*8}|{'-'*8}|{'-'*8}|{'-'*7}|{'-'*7}|{'-'*7}|{'-'*10}|")
    for r in data_rows:
        table_lines.append(f"| {r['name']:<14} | {r['chars']/10000:>4.0f}万 | {r['ek']:>5.2f} | {r['lk']:>5.2f} | {r['ck']:>5.1f} | {r['pk']:>5.1f} | {r['avg_sent']:>4.0f}字 | {r['long30']:>4.1f} | {r['avg_para']:>4.0f} | {r['genre']:<8} |")
    data_table = '\n'.join(table_lines)

    ek_chart_lines = []
    max_ek = max(ek_values) if ek_values else 1
    for r, v in zip(data_rows, ek_values):
        bar_len = int(v / max_ek * 25) if max_ek > 0 else 0
        ek_chart_lines.append(f"  {r['name']:<12} {v:>5.2f}  {'█' * bar_len}")
    ek_chart = '\n'.join(ek_chart_lines)

    lk_chart_lines = []
    max_lk = max(lk_values) if lk_values else 1
    for r, v in zip(data_rows, lk_values):
        bar_len = int(v / max_lk * 25) if max_lk > 0 else 0
        lk_chart_lines.append(f"  {r['name']:<12} {v:>5.2f}  {'█' * bar_len}")
    lk_chart = '\n'.join(lk_chart_lines)

    report = f"""# {author} 进化线深度分析

> 作者：{author} | {len(novels_data)}本 | 总字数：{total_chars/10000:.0f}万字
> 分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 核心发现

{chr(10).join(f'- {f}' for f in findings) if findings else '- 风格整体稳定，无显著变化'}

---

## 一、全量数据

{data_table}

---

## 二、感叹号演变趋势

{ek_chart}

趋势：{trend_desc(ek_values)}

## 三、省略号演变趋势

{lk_chart}

趋势：{trend_desc(lk_values)}

## 四、逗号/句号演变

逗号趋势：{trend_desc(ck_values)}
句号趋势：{trend_desc(pk_values)}

## 五、各作品感官描写密度对比

| 作品 | 视觉/万字 | 听觉/万字 | 触觉/万字 | 嗅觉/万字 | 味觉/万字 |
|------|----------|----------|----------|----------|----------|
"""
    for name, text, total, pf, sa, pa, ec, nf, genre in novels_data:
        sensory = extract_sensory(text, total, genre)
        report += f"| {name} | {sensory['视觉']['density']} | {sensory['听觉']['density']} | {sensory['触觉']['density']} | {sensory['嗅觉']['density']} | {sensory['味觉']['density']} |\n"

    report += f"""
## 六、福利内容密度对比

| 作品 | L1身体 | L2服饰 | L3亲密 | L4反应 | L5氛围 | L6对话 | L7事后 | 总密度/万字 |
|------|--------|--------|--------|--------|--------|--------|--------|-----------|
"""
    for name, text, total, pf, sa, pa, ec, nf, genre in novels_data:
        welfare = extract_welfare(text, total)
        w = welfare['layers']
        report += f"| {name} | {w['L1_身体部位']['density']} | {w['L2_服饰']['density']} | {w['L3_亲密动作']['density']} | {w['L4_暧昧反应']['density']} | {w['L5_暧昧氛围']['density']} | {w['L6_暗示对话']['density']} | {w['L7_事后暗示']['density']} | {welfare['density']} |\n"

    report += f"""
---
_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} GMT+8_
"""
    return report


# ============================================================
# 作者映射
# ============================================================

KNOWN_AUTHORS = {
    '逆龙道': '血红', '偷天': '血红', '邪龙道': '血红',
    '光明纪元': '血红', '开天录': '血红', '升龙道': '血红',
    '邪风曲': '血红', '三界血歌': '血红', '巫颂': '血红',
    '法师传奇': '血红', '龙战星野': '血红', '逍行纪': '血红',
    '沧元图': '我吃西红柿', '寸芒': '我吃西红柿', '盘龙': '我吃西红柿',
    '星辰变': '我吃西红柿', '吞噬星空': '我吃西红柿', '莽荒纪': '我吃西红柿',
    '雪鹰领主': '我吃西红柿', '飞剑问道': '我吃西红柿', '仙逆': '耳根',
    '我欲封天': '耳根', '一念永恒': '耳根', '三寸人间': '耳根',
    '大主宰': '天蚕土豆', '斗破苍穹': '天蚕土豆', '武动乾坤': '天蚕土豆',
    '元尊': '天蚕土豆', '斗罗大陆': '唐家三少', '绝世唐门': '唐家三少',
    '天火大道': '唐家三少', '大奉打更人': '卖报小郎君',
    '诡秘之主': '爱潜水的乌贼', '一世之尊': '爱潜水的乌贼',
    '奥术神座': '爱潜水的乌贼', '宿命之环': '爱潜水的乌贼',
    '不死武皇': '妖月夜', '太阳王之证': '汉朝天子',
    '神话版三国': '坟土荒草', '儒道至圣': '永恒之火',
    '秦吏': '七月新番', '唐砖': '孑与2',
    '庆余年': '猫腻', '将夜': '猫腻', '间客': '猫腻',
    '大道朝天': '猫腻', '择天记': '猫腻',
    '万族之劫': '老鹰吃小鸡', '全球高武': '老鹰吃小鸡',
    '超凡黎明': '文抄公', '传奇族长': '孤独漂流',
    '无限恐怖': 'zhttty', '无限曙光': 'zhttty', '无限未来': 'zhttty',
    '死亡开端': 'zhttty', '大宇宙时代': 'zhttty',
    '无限之电影杀戮': '滚开', '神秘之旅': '滚开', '极道天魔': '滚开',
    '万千之心': '滚开', '十方武圣': '滚开', '隐秘死角': '滚开',
    '牧神记': '宅猪', '帝尊': '宅猪', '人道至尊': '宅猪',
    '圣墟': '辰东', '遮天': '辰东', '完美世界': '辰东',
    '神墓': '辰东', '长生界': '辰东', '深空彼岸': '辰东',
    '剑来': '烽火戏诸侯', '雪中悍刀行': '烽火戏诸侯',
    '陈二狗的妖孽人生': '烽火戏诸侯',
    '赘婿': '愤怒的香蕉', '隐杀': '愤怒的香蕉',
    '凡人修仙传': '忘语',
    '丹武至尊': '沉默的糕点', '圣王': '梦入神机',
    '龙蛇演义': '梦入神机', '佛本是道': '梦入神机', '永生': '梦入神机',
    '夜的命名术': '会说话的肘子', '大王饶命': '会说话的肘子', '第一序列': '会说话的肘子',
    '全职高手': '蝴蝶蓝', '网游之近战法师': '蝴蝶蓝',
    '惊悚乐园': '三天两觉', '贩罪': '三天两觉',
    '异常生物见闻录': '远瞳', '黎明之剑': '远瞳',
    '极品家丁': '禹岩',
    '回到明朝当王爷': '月关', '大争之世': '月关',
    '搜神记': '树下野狐', '蛮荒记': '树下野狐',
    '紫川': '老猪',
    '亵渎': '烟雨江南', '尘缘': '烟雨江南', '永夜君王': '烟雨江南',
    '道诡异仙': '狐尾的笔',
    '我有一座冒险屋': '我会修空调',
    '末世之黑暗召唤师': '晓夜圆舞曲',
    '异世之风流大法师': '么么',
    '花都猎人': '不乐无语',
    '好色小姨': '九月阳光',
    '我的美女总裁老婆': '霉干菜烧饼',
    '异兽迷城': '雨魔',
    '冰与火之歌': '乔治·R·R·马丁',
    '哈利波特': 'J·K·罗琳',
    '波西杰克逊': '雷克·莱尔顿',
    '三体': '刘慈欣',
    '银河帝国': '阿西莫夫',
}


def load_author_map():
    """加载作者映射"""
    if os.path.exists(AUTHOR_MAP_FILE):
        with open(AUTHOR_MAP_FILE, 'r', encoding='utf-8') as f:
            m = json.load(f)
        for k, v in KNOWN_AUTHORS.items():
            if k not in m:
                m[k] = v
        return m
    return dict(KNOWN_AUTHORS)


def save_author_map(amap):
    """保存作者映射"""
    with open(AUTHOR_MAP_FILE, 'w', encoding='utf-8') as f:
        json.dump(amap, f, ensure_ascii=False, indent=2)


# ============================================================
# 主流程
# ============================================================

def get_novel_list():
    """获取所有小说文件"""
    return sorted(f for f in os.listdir(NOVEL_DIR) if f.endswith('.txt'))


def analyze_single(name_pattern=None, do_all=False):
    """单本深度分析"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = get_novel_list()
    amap = load_author_map()

    if name_pattern and not do_all:
        files = [f for f in files if name_pattern in f]
        if not files:
            print(f"未找到匹配 '{name_pattern}' 的小说")
            return

    count = 0
    for f in files:
        name = extract_novel_name(f)
        filepath = os.path.join(NOVEL_DIR, f)
        text = read_file(filepath)
        if not text:
            print(f"X {name}: cannot read")
            continue

        author = amap.get(name, '未知')
        existing = os.path.join(OUTPUT_DIR, f"analysis-{name}.md")
        if os.path.exists(existing):
            with open(existing, 'r', encoding='utf-8') as ef:
                first_line = ef.readline()
                m = re.search(r'作者[：:]\s*(\S+)', first_line)
                if m and author == '未知':
                    author = m.group(1)

        report = generate_single_deep_report(name, text, author)
        if report:
            outpath = os.path.join(OUTPUT_DIR, f"analysis-{name}-deep.md")
            with open(outpath, 'w', encoding='utf-8') as out:
                out.write(report)
            count += 1
            print(f"OK {name} ({len(re.sub(r'\\s','',text))/10000:.0f}w)")
        else:
            print(f"X {name}: too short")

    print(f"\nSingle deep analysis done: {count} reports")


def analyze_evolution(author_name=None, do_all=False):
    """作者进化分析"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = get_novel_list()
    amap = load_author_map()

    author_books = defaultdict(list)
    for f in files:
        name = extract_novel_name(f)
        author = amap.get(name)
        if author and author != '未知':
            author_books[author].append((name, f))

    if author_name and not do_all:
        if author_name in author_books:
            target = {author_name: author_books[author_name]}
        else:
            print(f"Author '{author_name}' not found. Known: {', '.join(sorted(author_books.keys()))}")
            return
    else:
        target = {a: books for a, books in author_books.items() if len(books) >= 3}

    count = 0
    for author, books in target.items():
        print(f"\nAuthor: {author} ({len(books)} books)")
        novels_data = []
        for name, f in books:
            filepath = os.path.join(NOVEL_DIR, f)
            text = read_file(filepath)
            if not text:
                continue
            total = len(re.sub(r'\s', '', text))
            if total < 10000:
                continue
            pf = punctuation_fingerprint(text, total)
            sa = sentence_analysis(text)
            pa = paragraph_analysis(text)
            ec = emotion_curve(text, total)
            nf = narrative_features(text, total)
            genre = '未分类'
            existing = os.path.join(OUTPUT_DIR, f"analysis-{name}.md")
            if os.path.exists(existing):
                with open(existing, 'r', encoding='utf-8') as ef:
                    content = ef.read(500)
                    for g in ['仙侠', '玄幻', '都市', '历史', '科幻', '同人', '游戏', '末世', '恐怖', '西幻', '体育']:
                        if g in content:
                            genre = g
                            break
            novels_data.append((name, text, total, pf, sa, pa, ec, nf, genre))
            print(f"  OK {name} ({total/10000:.0f}w)")

        if len(novels_data) >= 2:
            report = generate_evolution_report(author, novels_data)
            if report:
                outpath = os.path.join(OUTPUT_DIR, f"analysis-{author}进化-deep.md")
                with open(outpath, 'w', encoding='utf-8') as out:
                    out.write(report)
                count += 1
                print(f"  -> {author}进化-deep.md")

    print(f"\nEvolution analysis done: {count} reports")


def analyze_sensory(name_pattern=None, do_all=False):
    """感官库提取"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = get_novel_list()

    if name_pattern and not do_all:
        files = [f for f in files if name_pattern in f]

    genre_data = defaultdict(lambda: defaultdict(lambda: {'total': 0, 'density_sum': 0, 'count': 0, 'examples': []}))

    count = 0
    for f in files:
        name = extract_novel_name(f)
        filepath = os.path.join(NOVEL_DIR, f)
        text = read_file(filepath)
        if not text:
            continue
        total = len(re.sub(r'\s', '', text))
        if total < 10000:
            continue

        genre = '未分类'
        existing = os.path.join(OUTPUT_DIR, f"analysis-{name}.md")
        if os.path.exists(existing):
            with open(existing, 'r', encoding='utf-8') as ef:
                content = ef.read(500)
                for g in ['仙侠', '玄幻', '都市', '历史', '科幻', '同人', '游戏', '末世', '恐怖', '西幻', '体育']:
                    if g in content:
                        genre = g
                        break

        sensory = extract_sensory(text, total, genre)
        for sense, data in sensory.items():
            genre_data[genre][sense]['total'] += data['count']
            genre_data[genre][sense]['density_sum'] += data['density']
            genre_data[genre][sense]['count'] += 1
            for word, cnt in data['top_words']:
                genre_data[genre][sense]['examples'].append((word, cnt))
        count += 1
        print(f"OK {name} ({genre})")

    for genre, senses in genre_data.items():
        report_lines = [f"# Sensory Extraction - {genre}\n"]
        report_lines.append(f"> Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report_lines.append(f"> Samples: {count}\n")

        for sense in ['嗅觉', '味觉', '触觉', '听觉', '视觉']:
            if sense not in senses:
                continue
            data = senses[sense]
            avg_density = round(data['density_sum'] / max(data['count'], 1), 1)
            word_counter = Counter()
            for word, cnt in data['examples']:
                word_counter[word] += cnt
            top = word_counter.most_common(20)
            report_lines.append(f"\n{'='*60}")
            report_lines.append(f"## {sense} ({data['total']} hits, avg {avg_density}/10k chars)")
            report_lines.append(f"{'='*60}\n")
            report_lines.append("Top keywords:")
            for word, cnt in top:
                report_lines.append(f"  {word}: {cnt}")
            report_lines.append("")

        outpath = os.path.join(OUTPUT_DIR, f"sensory-extraction-{genre}.md")
        with open(outpath, 'w', encoding='utf-8') as out:
            out.write('\n'.join(report_lines))
        print(f"-> sensory-extraction-{genre}.md")

    print(f"\nSensory extraction done: {count} books, {len(genre_data)} genres")


def analyze_welfare(name_pattern=None, do_all=False):
    """福利感官扫描"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = get_novel_list()

    if name_pattern and not do_all:
        files = [f for f in files if name_pattern in f]

    results = []
    amap = load_author_map()
    for f in files:
        name = extract_novel_name(f)
        filepath = os.path.join(NOVEL_DIR, f)
        text = read_file(filepath)
        if not text:
            continue
        total = len(re.sub(r'\s', '', text))
        if total < 10000:
            continue

        welfare = extract_welfare(text, total)
        author = amap.get(name, '未知')
        results.append(dict(
            name=name, author=author, chars=total,
            density=welfare['density'], total=welfare['total'],
            layers=welfare['layers'],
        ))
        print(f"OK {name} density={welfare['density']}/10k")

    results.sort(key=lambda x: -x['density'])

    report = f"""# Welfare Sensory Scan Results

> Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> Samples: {len(results)}

---

## Density Ranking TOP30

| # | Novel | Author | Chars | Density/10k | L1 Body | L2 Dress | L3 Intimacy | L4 Reaction | L5 Atmo | L6 Dialogue | L7 After |
|---|-------|--------|-------|-------------|---------|----------|-------------|-------------|---------|-------------|----------|
"""
    for i, r in enumerate(results[:30], 1):
        w = r['layers']
        report += f"| {i} | {r['name']} | {r['author']} | {r['chars']/10000:.0f}w | **{r['density']}** | {w['L1_身体部位']['density']} | {w['L2_服饰']['density']} | {w['L3_亲密动作']['density']} | {w['L4_暧昧反应']['density']} | {w['L5_暧昧氛围']['density']} | {w['L6_暗示对话']['density']} | {w['L7_事后暗示']['density']} |\n"

    report += f"""
---

## Layer Statistics

| Layer | Total Hits | Avg Density/10k |
|-------|-----------|-----------------|
"""
    layer_totals = defaultdict(int)
    for r in results:
        for layer, data in r['layers'].items():
            layer_totals[layer] += data['total']

    for layer in ['L1_身体部位', 'L2_服饰', 'L3_亲密动作', 'L4_暧昧反应', 'L5_暧昧氛围', 'L6_暗示对话', 'L7_事后暗示']:
        total = layer_totals[layer]
        avg = round(total / max(len(results), 1), 1)
        report += f"| {layer} | {total} | {avg} |\n"

    outpath = os.path.join(OUTPUT_DIR, "welfare-scan-results.md")
    with open(outpath, 'w', encoding='utf-8') as out:
        out.write(report)
    print(f"\nWelfare scan done: {len(results)} books -> welfare-scan-results.md")


def batch_all():
    """全量四合一分析"""
    print("=" * 60)
    print("Full batch analysis (4-in-1)")
    print("=" * 60)
    print("\n[1/4] Single deep analysis...")
    analyze_single(do_all=True)
    print("\n[2/4] Author evolution analysis...")
    analyze_evolution(do_all=True)
    print("\n[3/4] Sensory extraction...")
    analyze_sensory(do_all=True)
    print("\n[4/4] Welfare scan...")
    analyze_welfare(do_all=True)
    print("\n" + "=" * 60)
    print("All done!")


# ============================================================
# CLI
# ============================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == 'single':
        if len(sys.argv) > 2 and sys.argv[2] == '--all':
            analyze_single(do_all=True)
        elif len(sys.argv) > 2:
            analyze_single(sys.argv[2])
        else:
            print("Usage: python3 deep-analysis-v2.py single <name> or single --all")

    elif cmd == 'evolution':
        if len(sys.argv) > 2 and sys.argv[2] == '--all':
            analyze_evolution(do_all=True)
        elif len(sys.argv) > 2:
            analyze_evolution(sys.argv[2])
        else:
            print("Usage: python3 deep-analysis-v2.py evolution <author> or evolution --all")

    elif cmd == 'sensory':
        if len(sys.argv) > 2 and sys.argv[2] == '--all':
            analyze_sensory(do_all=True)
        elif len(sys.argv) > 2:
            analyze_sensory(sys.argv[2])
        else:
            print("Usage: python3 deep-analysis-v2.py sensory <name> or sensory --all")

    elif cmd == 'welfare':
        if len(sys.argv) > 2 and sys.argv[2] == '--all':
            analyze_welfare(do_all=True)
        elif len(sys.argv) > 2:
            analyze_welfare(sys.argv[2])
        else:
            print("Usage: python3 deep-analysis-v2.py welfare <name> or welfare --all")

    elif cmd == 'batch':
        batch_all()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == '__main__':
    main()
