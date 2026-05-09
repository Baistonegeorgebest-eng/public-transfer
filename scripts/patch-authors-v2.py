#!/usr/bin/env python3
"""
补齐剩余36本"作者：未知"的deep报告 + fingerprint-results.json
"""
import os, re, json, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FP_FILE = os.path.join(BASE, 'scripts', 'fingerprint-results.json')
DEEP_DIR = os.path.join(BASE, 'novel-corpus-analysis')
NOVEL_TXT_DIR = os.path.join(BASE, 'novel-txts')

# ============================================================
# 全部缺失作者（联网搜索确认后） 
# ============================================================

# 网文类
WANGWEN = {
    '不灭金丹': '诸生浮屠',
    '临渊行': '宅猪',
    '丹药修改器': '海千星河',
    '史上最强炼丹师': '丑八佰',
    '我！最强反派，掠夺主角气运': '小猪',
    '择日飞升': '宅猪',
    '浪迹在武侠世界的道士': '中原五百',
    '游方道士': '小小小柠檬',
    '漫威蜘蛛侠：纵横宇宙': '子婴不当王',
    '猎魔人在霍格沃茨': '浅墨留香',
    '猎魔烹饪手册': '颓废龙',
    '电影系统逍遥游': '渔歌飘渺',
    '诡秘如风，常伴吾身': '余云飞',
    '霍格沃茨之巫师至上': '荆五',
    '霍格沃茨之血脉巫师': '纯洁小天使',
}

# 译本合集类（直接来自译本目录文件名或常识）
TRANSLATIONS = {
    'P.D.詹姆斯经典推理集（全5册）': 'P.D.詹姆斯',
    '丹·布朗作品系列（全7册）': '丹·布朗',
    '乔治·R.R.马丁经典奇幻系列（全22册）': '乔治·R.R.马丁',
    '凡尔纳经典科幻（全10册）': '儒勒·凡尔纳',
    '刺客信条（全14册）': '奥利弗·波登等',
    '哈利·波特全集': 'J.K.罗琳',
    '哈利·波特百科全书': '编委会',
    '哈利·波特终极典藏版': 'J.K.罗琳',
    '斯蒂芬·金惊悚套装（全17本）': '斯蒂芬·金',
    '江南作品合集（全25册）': '江南',
    '波西·杰克逊系列（全10册）': '雷克·莱尔顿',
    '星之继承者三部曲': '詹姆斯·P.霍根',
    '弗诺·文奇经典科幻（全5册）': '弗诺·文奇',
    '冰风谷三部曲': 'R.A.萨尔瓦多',
    '国家阴谋（五部）': '丹尼尔·席尔瓦',
    '克苏鲁神话（Ⅰ-Ⅲ卷）': 'H.P.洛夫克拉夫特',
    '冰与火之歌（全五卷）': '乔治·R.R.马丁',
    '龙族（实体版1-3部全本）': '江南',
    '龙族': '江南',  # 非deep报告版本
    '银河界区三部曲': '弗诺·文奇',
    '阿加莎·克里斯蒂侦探大全集（全85册）': '阿加莎·克里斯蒂',
    '纳尼亚传奇全集（全7册）': 'C.S.刘易斯',
    '空间三部曲（C.S.刘易斯）': 'C.S.刘易斯',
    '经典密室杀人推理小说合集': '多人合集',
    '钢铁是怎样炼成的': '尼古拉·奥斯特洛夫斯基',
    '银河帝国（阿西莫夫全17册）': '艾萨克·阿西莫夫',
    '肯·福莱特经典作品集（全11册）': '肯·福莱特',
    '魔兽世界官方作品全集（全26册）': '克里斯·梅森等',
    '黑豹红狼': '马龙·詹姆斯',
    '托尔金中洲三部曲': 'J.R.R.托尔金',
    '托尔金三部曲': 'J.R.R.托尔金',
}

# 合并
ALL_MISSING = {}
ALL_MISSING.update(WANGWEN)
ALL_MISSING.update(TRANSLATIONS)

print(f"总待补: {len(ALL_MISSING)} 本")

# ============================================================
# Step 1: 修复 deep 报告头
# ============================================================
fixed_reports = 0
for f in sorted(glob.glob(os.path.join(DEEP_DIR, '*-deep.md'))):
    fname = os.path.basename(f)
    report_name = fname.replace('analysis-', '').replace('-deep.md', '')
    
    # 先检查是否已经修复
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    m = re.search(r'>\s*作者[：:]\s*(\S+)', content)
    if m and m.group(1).strip() != '未知':
        continue  # 已修复
    
    # 查找作者
    author = None
    if report_name in ALL_MISSING:
        author = ALL_MISSING[report_name]
    else:
        # 分步部分匹配
        for missing_name, missing_author in ALL_MISSING.items():
            if report_name in missing_name or missing_name in report_name:
                author = missing_author
                break
    
    if author:
        # 替换
        new_content = re.sub(
            r'(>\s*作者[：:])[^\n]*',
            f'\\1 {author}',
            content
        )
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        fixed_reports += 1
        print(f"  [REPORT] {report_name}: 未知 → {author}")

print(f"\n[1] Deep报告修复: {fixed_reports} 份")

# ============================================================
# Step 2: 更新 fingerprint-results.json
# ============================================================
with open(FP_FILE, 'r', encoding='utf-8') as f:
    fp_data = json.load(f)

fp_name_to_idx = {d['name']: i for i, d in enumerate(fp_data)}

added = 0
for book_name, author in ALL_MISSING.items():
    # 检查是否在fingerprint中
    found = False
    for fp_name in fp_name_to_idx:
        if book_name == fp_name or book_name in fp_name or fp_name in book_name:
            idx = fp_name_to_idx[fp_name]
            old = fp_data[idx].get('author', '')
            if not old or old == '未知':
                fp_data[idx]['author'] = author
                added += 1
                print(f"  [FP] {fp_name}: {old or '空'} → {author}")
            found = True
            break
    
    if not found:
        print(f"  [SKIP] {book_name}: 不在fingerprint中")

# 再补novel-txts里可能漏的
txt_files = [f for f in os.listdir(NOVEL_TXT_DIR) if f.endswith('.txt') and not f.startswith('.')]
for f in txt_files:
    name = f.replace('.txt', '')
    name = re.sub(r'^\d+[\.\-_]?\s*', '', name)
    # 清理校对版本标记
    name = re.sub(r'[（(][^）)]*版[^）)]*[）)]', '', name)
    name = name.strip()
    
    if name not in fp_name_to_idx:
        # 可能是新书
        continue
    
    idx = fp_name_to_idx[name]
    entry = fp_data[idx]
    if entry.get('author', '') in ('', '未知'):
        # 从文件名提取
        m = re.search(r'作者[：:]\s*(.+?)\.txt$', f)
        if m:
            author = m.group(1).strip()
            entry['author'] = author
            print(f"  [FP_NEW] {name}: 空 → {author}")
            added += 1

with open(FP_FILE, 'w', encoding='utf-8') as f:
    json.dump(fp_data, f, ensure_ascii=False, indent=2)

print(f"[2] Fingerprint更新: {added} 条")

# ============================================================
# Step 3: 更新 deep-analysis-v2.py KNOWN_AUTHORS
# ============================================================
SCRIPT_FILE = os.path.join(BASE, 'scripts', 'deep-analysis-v2.py')

# 读取当前的KNOWN_AUTHORS
with open(SCRIPT_FILE, 'r', encoding='utf-8') as f:
    script_content = f.read()

start_marker = 'KNOWN_AUTHORS = {'
end_marker = '\ndef load_author_map'
start_idx = script_content.find(start_marker)
end_idx = script_content.find(end_marker, start_idx)

if start_idx == -1:
    print("[3] ❌ 找不到 KNOWN_AUTHORS 起始位置")
else:
    # 构建完整字典（旧entry + 新补的）
    # 先读出现有字典
    dict_block = script_content[start_idx + len('KNOWN_AUTHORS = {'):end_idx]
    existing = {}
    for line in dict_block.split('\n'):
        m = re.match(r"\s*'([^']+)':\s*'([^']+)',", line)
        if m:
            existing[m.group(1)] = m.group(2)
    
    print(f"[3] 现有 KNOWN_AUTHORS 条目: {len(existing)}")
    
    # 添加所有缺失
    for book_name, author in ALL_MISSING.items():
        existing[book_name] = author
    
    # 也加入fingerprint中未在KNOWN_AUTHORS里的（确保完整）
    fp_to_add = 0
    for d in fp_data:
        name = d['name']
        author = d.get('author', '')
        if author and author != '未知' and name not in existing:
            existing[name] = author
            fp_to_add += 1
    print(f"[3] 从fingerprint额外补充: {fp_to_add} 条")
    
    # 重新生成字典块
    dict_lines = ['KNOWN_AUTHORS = {']
    for name in sorted(existing.keys()):
        dict_lines.append(f"    '{name}': '{existing[name]}',")
    dict_lines.append('}')
    new_dict = '\n'.join(dict_lines)
    
    new_script = script_content[:start_idx] + new_dict + script_content[end_idx:]
    
    with open(SCRIPT_FILE, 'w', encoding='utf-8') as f:
        f.write(new_script)
    
    print(f"[3] KNOWN_AUTHORS 更新: {len(existing)} 条 (原110条)")

print("\n✅ 全部完成！")
