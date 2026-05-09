#!/usr/bin/env python3
"""Batch analysis for 14 new/replaced novels - fingerprint + sensory scan."""
import os, re, json, sys

NOVEL_DIR = "/root/.openclaw/workspace/public-transfer/novel-txts"

# All 14 novels to process
novels = {
    "回到明朝当王爷": "月关",
    "极品家丁": "禹岩",
    "小兵传奇": "玄雨",
    "邪风曲": "血红",
    "邪气凛然": "跳舞",
    "张三丰异界游": "写字板",
    "王牌进化": "卷土",
    "逍行纪": "血红",
    "中华仙魔录": "龙鳞道",
    "大汉帝国风云录": "猛子",
    "大争之世": "月关",
    "惟我独仙": "唐家三少",
    "召唤千军": "高森",
    "龙战星野": "血红",
}

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

def fingerprint(text):
    """Core punctuation fingerprint."""
    total = len(re.sub(r'\s', '', text))
    if total < 10000:
        return None
    k = total / 1000
    comma = text.count('，') + text.count(',')
    period = text.count('。') + text.count('.')
    excl = text.count('！') + text.count('!')
    ellipsis = text.count('……')
    quest = text.count('？') + text.count('?')
    chapters = len(re.findall(r'第[一二三四五六七八九十百千\d]+[章回节]', text))
    if chapters < 2:
        chapters = max(1, total // 3000)
    sentences = [s.strip() for s in re.split(r'[。！？…]+', text) if len(re.sub(r'\s','',s)) > 5]
    lengths = [len(re.sub(r'\s', '', s)) for s in sentences]
    avg_sent = sum(lengths) / len(lengths) if lengths else 0
    long_pct = sum(1 for l in lengths if l > 30) / len(lengths) * 100 if lengths else 0
    seem = (text.count('似乎') + text.count('好像') + text.count('仿佛')) / k
    maybe = (text.count('可能') + text.count('也许') + text.count('或许')) / k
    return {
        'chars': total, 'chapters': chapters,
        'comma_per_k': comma/k, 'period_per_k': period/k,
        'excl_per_k': excl/k, 'ellipsis_per_k': ellipsis/k,
        'quest_per_k': quest/k,
        'excl_per_ch': excl/max(chapters,1), 'ell_per_ch': ellipsis/max(chapters,1),
        'avg_sent': avg_sent, 'long_pct': long_pct,
        'seem_per_10k': seem, 'maybe_per_10k': maybe,
    }

def sensory_scan(text):
    """Scan for sensory/welfare content keywords."""
    total = len(re.sub(r'\s', '', text))
    k = total / 1000
    wan = total / 10000
    
    # v2 七层体系扫描
    # L1 身体部位
    l1_upper = sum(text.count(w) for w in ['锁骨','腰肢','腰线','香肩','玉颈','酥胸','美腿','长腿','玉腿','纤腰','翘臀','丰臀'])
    l1_lower = sum(text.count(w) for w in ['大腿','臀部','屁股','胸部','双峰','玉兔','乳','胸脯','翘臀','丰臀','美臀'])
    l1_body = sum(text.count(w) for w in ['肌肤','皮肤','胴体','玉体','娇躯','身体','身材','曲线','玲珑','婀娜','窈窕','身段'])
    
    # L2 服饰
    l2 = sum(text.count(w) for w in ['丝袜','高跟','裙摆','内衣','薄纱','轻纱','薄衫','睡衣','浴袍','肚兜','亵衣','罗衫','纱裙','短裙','迷你裙','吊带','蕾丝','透明','若隐若现','薄如蝉翼'])
    
    # L3 亲密动作
    l3_light = sum(text.count(w) for w in ['搂住','抱住','拥入','依偎','靠在','贴近','挨着','偎依','揽住','环住','勾住','攀住'])
    l3_mid = sum(text.count(w) for w in ['抚摸','抚摩','摩挲','轻抚','揉捏','摩弄','把玩','揉搓','搓揉','爱抚','抚弄'])
    l3_heavy = sum(text.count(w) for w in ['亲吻','吻住','吻上','亲吻','深吻','热吻','舌吻','吮吸','舔舐','啃咬','咬住','嘬'])
    
    # L4 暧昧反应
    l4_body = sum(text.count(w) for w in ['脸红','面红','红晕','绯红','潮红','发烫','发热','心跳','心如鹿撞','喘息','娇喘','气喘','呼吸急促','发软','酥软','发麻','战栗','颤抖','发抖','哆嗦','轻颤'])
    l4_voice = sum(text.count(w) for w in ['呻吟','娇吟','低吟','嘤咛','呢喃','轻哼','娇嗔','嗲声','撒娇','哼哼','嗯嗯','啊啊'])
    
    # L5 暧昧氛围
    l5 = sum(text.count(w) for w in ['独处','二人世界','月光','烛光','温泉','浴池','浴室','卧室','床上','床笫','被窝','被褥','帷幔','帐幔','纱帐','春宵','良宵','夜深人静'])
    
    # L6 暗示对话
    l6 = sum(text.count(w) for w in ['别在这里','你想要','闭上眼睛','别动','轻点','慢点','你好坏','坏人','讨厌','不要嘛','坏蛋','馋猫','小坏蛋'])
    
    # L7 事后暗示
    l7 = sum(text.count(w) for w in ['整理衣服','裹着被子','清晨醒来','第二天早上','事后','云雨之后','鱼水之欢','巫山云雨','春风一度','共赴巫山','颠鸾倒凤'])
    
    # 不能上架关键词（高确定性）
    vip_kw = sum(text.count(w) for w in [
        '一丝不挂','赤身裸体','光着身子','全身赤裸','脱光','脱得精光','脱个精光',
        '高潮','快感','呻吟声','浪叫','娇喘连连','欲仙欲死','欲死欲仙',
        '进入','插入','顶入','深入','抽插','挺动','耸动',
        '私处','下体','花心','蜜穴','玉门','桃源','幽谷',
        '春药','催情','迷药','蒙汗药','媚药',
        '强奸','轮奸','强暴','蹂躏','糟蹋',
    ])
    
    total_l1 = l1_upper + l1_lower + l1_body
    total_l3 = l3_light + l3_mid + l3_heavy
    total_l4 = l4_body + l4_voice
    total_welfare = total_l1 + l2 + total_l3 + total_l4 + l5 + l6 + l7
    
    return {
        'total_chars': total,
        'L1_body_upper': l1_upper, 'L1_body_lower': l1_lower, 'L1_body_general': l1_body,
        'L1_total': total_l1,
        'L2_clothing': l2,
        'L3_light': l3_light, 'L3_mid': l3_mid, 'L3_heavy': l3_heavy, 'L3_total': total_l3,
        'L4_body': l4_body, 'L4_voice': l4_voice, 'L4_total': total_l4,
        'L5_atmosphere': l5,
        'L6_dialogue': l6,
        'L7_aftermath': l7,
        'total_welfare': total_welfare,
        'welfare_density': total_welfare / wan,
        'vip_keywords': vip_kw,
        'vip_density': vip_kw / wan,
    }

# Main
results = {}
for name, author in novels.items():
    filepath = os.path.join(NOVEL_DIR, f"{name}.txt")
    if not os.path.exists(filepath):
        print(f"[SKIP] {name} - file not found", file=sys.stderr)
        continue
    
    text = read_file(filepath)
    if not text:
        print(f"[FAIL] {name} - cannot read", file=sys.stderr)
        continue
    
    fp = fingerprint(text)
    ss = sensory_scan(text)
    if fp and ss:
        results[name] = {'author': author, 'fingerprint': fp, 'sensory': ss}
        print(f"[OK]   {name} ({author}) - {fp['chars']/10000:.0f}万字, welfare={ss['welfare_density']:.1f}/万字, vip={ss['vip_density']:.2f}/万字", file=sys.stderr)
    else:
        print(f"[FAIL] {name} - analysis failed", file=sys.stderr)

# Output JSON
print(json.dumps(results, ensure_ascii=False, indent=2))
