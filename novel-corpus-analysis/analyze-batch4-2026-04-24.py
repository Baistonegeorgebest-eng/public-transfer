#!/usr/bin/env python3
"""Batch 4 analysis for 8 novels."""
import os, re, json, sys

NOVEL_DIR = "/root/.openclaw/workspace/public-transfer/novel-txts"

novels = {
    "无限之凡人的智慧": "春秋散人",
    "武极天下": "蚕茧里的牛",
    "仙葫": "流浪的蛤蟆",
    "现代平民宗师传奇": "神医的名",
    "御剑乘风": "未确认",
    "阵法宗师异界纵横": "神医的名",
    "重生之足球神话": "冰魂46",
    "足球修改器": "乱世狂刀01",
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
    seem = (text.count('似乎') + text.count('好像') + text.count('仿佛')) / k
    maybe = (text.count('可能') + text.count('也许') + text.count('或许')) / k
    return {
        'chars': total, 'chapters': chapters,
        'comma_per_k': round(comma/k, 2), 'period_per_k': round(period/k, 2),
        'excl_per_k': round(excl/k, 2), 'ellipsis_per_k': round(ellipsis/k, 2),
        'quest_per_k': round(quest/k, 2),
        'excl_per_ch': round(excl/max(chapters,1), 2), 'ell_per_ch': round(ellipsis/max(chapters,1), 2),
        'avg_sent': round(avg_sent, 1), 'long_pct': round(long_pct, 1),
        'seem_per_10k': round(seem, 2), 'maybe_per_10k': round(maybe, 2),
    }

def sensory_scan(text):
    total = len(re.sub(r'\s', '', text))
    wan = total / 10000
    l1 = sum(text.count(w) for w in ['锁骨','腰肢','腰线','香肩','玉颈','酥胸','美腿','长腿','玉腿','纤腰','翘臀','丰臀','大腿','臀部','屁股','胸部','双峰','玉兔','乳','胸脯','肌肤','皮肤','胴体','玉体','娇躯','身体','身材','曲线','玲珑','婀娜','窈窕','身段'])
    l2 = sum(text.count(w) for w in ['丝袜','高跟','裙摆','内衣','薄纱','轻纱','薄衫','睡衣','浴袍','肚兜','亵衣','罗衫','纱裙','短裙','迷你裙','吊带','蕾丝','透明','若隐若现','薄如蝉翼'])
    l3 = sum(text.count(w) for w in ['搂住','抱住','拥入','依偎','靠在','贴近','偎依','揽住','抚摸','抚摩','摩挲','轻抚','揉捏','爱抚','亲吻','吻住','吻上','深吻','热吻','吮吸','舔舐'])
    l4 = sum(text.count(w) for w in ['脸红','面红','红晕','绯红','潮红','心跳','喘息','娇喘','气喘','酥软','颤抖','战栗','呻吟','娇吟','低吟','嘤咛','呢喃','娇嗔','撒娇'])
    l5 = sum(text.count(w) for w in ['独处','月光','烛光','温泉','浴池','浴室','卧室','床上','床笫','帷幔','春宵','良宵','夜深人静'])
    l6 = sum(text.count(w) for w in ['别在这里','你想要','闭上眼睛','别动','轻点','慢点','你好坏','讨厌'])
    l7 = sum(text.count(w) for w in ['整理衣服','裹着被子','清晨醒来','事后','云雨之后','鱼水之欢','巫山云雨','春风一度'])
    vip = sum(text.count(w) for w in ['一丝不挂','赤身裸体','光着身子','全身赤裸','高潮','快感','浪叫','娇喘连连','欲仙欲死','进入','插入','顶入','抽插','私处','下体','花心','蜜穴','春药','催情','强奸','强暴','蹂躏'])
    total_w = l1 + l2 + l3 + l4 + l5 + l6 + l7
    return {'total_welfare': total_w, 'welfare_density': round(total_w / wan, 2), 'vip_keywords': vip, 'vip_density': round(vip / wan, 2)}

results = {}
for name, author in novels.items():
    filepath = os.path.join(NOVEL_DIR, f"{name}.txt")
    if not os.path.exists(filepath): continue
    text = read_file(filepath)
    if not text: continue
    fp = fingerprint(text)
    ss = sensory_scan(text)
    if fp and ss:
        results[name] = {'author': author, 'fingerprint': fp, 'sensory': ss}
        print(f"[OK] {name} ({author}) {fp['chars']/10000:.0f}万 感叹{fp['excl_per_k']:.2f} 福利{ss['welfare_density']:.1f} VIP{ss['vip_density']:.2f}", file=sys.stderr)

print(json.dumps(results, ensure_ascii=False, indent=2))
