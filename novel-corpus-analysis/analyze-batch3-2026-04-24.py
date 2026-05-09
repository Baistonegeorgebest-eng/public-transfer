#!/usr/bin/env python3
"""Batch 3 (corrected) analysis for 19 NEW novels."""
import os, re, json, sys

NOVEL_DIR = "/root/.openclaw/workspace/public-transfer/novel-txts"

novels = {
    "无限斩杀": "娇蛮斩杀",
    "国破山河在": "华表",
    "洪荒不朽": "小七泡泡",
    "洪荒绝世散修": "吾心飞扬",
    "洪荒时辰": "静默节奏",
    "洪荒祖巫烛九阴传": "小小妖道",
    "皇气": "鸿蒙树",
    "剑极天下": "尸口巾",
    "抗日之血祭山河": "未确认",
    "雷罚": "没有灵魂的人",
    "秦皇纪": "殷扬",
    "人皇系统": "未确认",
    "随身带着地狱": "未确认",
    "随身装着一口泉": "未确认",
    "唐朝大宗师": "暖阳倾城",
    "无极魔道": "逆苍天",
    "无良皇帝": "傲无常",
    "无限的大冒险": "未确认",
    "不死冥王": "云天空",
}

def read_file(filepath):
    for enc in ['utf-8', 'gbk', 'gb18030']:
        try:
            with open(filepath, 'r', encoding=enc, errors='replace') as f:
                text = f.read()
            if '的' in text[:1000] or '章' in text[:2000]:
                return text
        except:
            continue
    return None

def fingerprint(text):
    total = len(re.sub(r'\s', '', text))
    if total < 10000: return None
    k = total / 1000
    comma = text.count('，') + text.count(',')
    period = text.count('。') + text.count('.')
    excl = text.count('！') + text.count('!')
    ellipsis = text.count('……')
    quest = text.count('？') + text.count('?')
    chapters = len(re.findall(r'第[一二三四五六七八九十百千\d]+[章回节]', text))
    if chapters < 2: chapters = max(1, total // 3000)
    sentences = [s.strip() for s in re.split(r'[。！？…]+', text) if len(re.sub(r'\s','',s)) > 5]
    lengths = [len(re.sub(r'\s', '', s)) for s in sentences]
    avg_sent = sum(lengths) / len(lengths) if lengths else 0
    long_pct = sum(1 for l in lengths if l > 30) / len(lengths) * 100 if lengths else 0
    return {
        'chars': total, 'chapters': chapters,
        'comma_per_k': round(comma/k, 2), 'period_per_k': round(period/k, 2),
        'excl_per_k': round(excl/k, 2), 'ellipsis_per_k': round(ellipsis/k, 2),
        'quest_per_k': round(quest/k, 2),
        'avg_sent': round(avg_sent, 1), 'long_pct': round(long_pct, 1),
    }

def sensory_scan(text):
    total = len(re.sub(r'\s', '', text))
    wan = total / 10000
    l1 = sum(text.count(w) for w in ['锁骨','腰肢','腰线','酥胸','美腿','大腿','臀部','胸部','双峰','肌肤','皮肤','胴体','玉体','娇躯','身体','身材','曲线','窈窕','身段'])
    l2 = sum(text.count(w) for w in ['丝袜','内衣','薄纱','睡衣','肚兜','亵衣','透明','若隐若现'])
    l3 = sum(text.count(w) for w in ['搂住','抱住','依偎','贴近','抚摸','摩挲','轻抚','爱抚','亲吻','吻住','深吻','吮吸'])
    l4 = sum(text.count(w) for w in ['脸红','红晕','潮红','心跳','喘息','娇喘','酥软','颤抖','呻吟','娇吟','嘤咛'])
    l5 = sum(text.count(w) for w in ['独处','月光','温泉','浴室','卧室','床上','帷幔','春宵'])
    l6 = sum(text.count(w) for w in ['别在这里','你想要','闭上眼睛','讨厌'])
    l7 = sum(text.count(w) for w in ['整理衣服','裹着被子','清晨醒来','事后','云雨'])
    vip = sum(text.count(w) for w in ['一丝不挂','赤身裸体','高潮','快感','浪叫','娇喘连连','进入','插入','抽插','私处','下体','花心','蜜穴','春药','催情','强奸','强暴'])
    total_w = l1 + l2 + l3 + l4 + l5 + l6 + l7
    return {'total_welfare': total_w, 'welfare_density': round(total_w / wan, 2), 'vip_keywords': vip, 'vip_density': round(vip / wan, 2)}

results = {}
for name, author in novels.items():
    filepath = os.path.join(NOVEL_DIR, f"{name}.txt")
    if not os.path.exists(filepath):
        print(f"[SKIP] {name}", file=sys.stderr)
        continue
    text = read_file(filepath)
    if not text:
        print(f"[FAIL] {name}", file=sys.stderr)
        continue
    fp = fingerprint(text)
    ss = sensory_scan(text)
    if fp and ss:
        results[name] = {'author': author, 'fingerprint': fp, 'sensory': ss}
        print(f"[OK] {name} ({author}) {fp['chars']/10000:.0f}万 感叹{fp['excl_per_k']:.2f} 福利{ss['welfare_density']:.1f} VIP{ss['vip_density']:.2f}", file=sys.stderr)

print(json.dumps(results, ensure_ascii=False, indent=2))
