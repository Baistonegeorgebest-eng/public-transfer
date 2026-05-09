#!/usr/bin/env python3
"""
补齐所有 deep 分析报告的"作者：未知"：
1. 从 fingerprint-results.json 提取已知作者 → 匹配 deep 报告
2. 从译本目录文件名提取内嵌作者 → 补齐译本合集
3. 从 novel-txts 文件名提取内嵌作者（少量合集在 novel-txts 名下）
4. 剩下的手动联网搜补
5. 更新 deep-analysis-v2.py 中的 KNOWN_AUTHORS 字典
"""
import os, re, json, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FP_FILE = os.path.join(BASE, 'scripts', 'fingerprint-results.json')
NOVEL_TXT_DIR = os.path.join(BASE, 'novel-txts')
TRANSLATION_DIR = os.path.join(BASE, '译本')
DEEP_DIR = os.path.join(BASE, 'novel-corpus-analysis')
SCRIPT_FILE = os.path.join(BASE, 'scripts', 'deep-analysis-v2.py')

# ============================================================
# Step 1: 加载所有已知作者来源
# ============================================================

# 1a. fingerprint-results.json
with open(FP_FILE) as f:
    fp_data = json.load(f)
fp_authors = {d['name'].strip(): d.get('author', '').strip() for d in fp_data}
print(f"[1a] fingerprint-results.json: {len(fp_authors)} 本, 未知: {sum(1 for a in fp_authors.values() if not a or a == '未知')}")

# 1b. 译本目录文件名 → 书名 -> 作者
def extract_author_from_filename(filename):
    """从译本目录的文件名提取作者，返回 (书名, 作者) 或 None"""
    name = filename.replace('.txt', '')
    # 先试括号作者： (作者名) (Z-Library)
    m = re.search(r'\(([^()]+?)\)\s*\(Z-Library\)\s*$', name)
    if m:
        author = m.group(1).strip()
        return name, author
    # 再试 作者：xxx
    m = re.search(r'作者[：:]\s*([^，。；]+?)(?:\)|$)', name)
    if m:
        author = m.group(1).strip()
        return name, author
    return name, None

translation_authors = {}
for f in os.listdir(TRANSLATION_DIR):
    if not f.endswith('.txt') or f.startswith('.'):
        continue
    fn = f.replace('.txt', '')
    # 提取作者
    author = None
    m = re.search(r'\(([^()]+?)\)\s*\(Z-Library\)', fn)
    if not m:
        m = re.search(r'作者[：:]\s*([^(（]+)', fn)
    if not m:
        # 试试纯数字 作者：xxx
        m = re.search(r'[（(]?作者[：:]?\s*([^)）]+?)[)）]', fn)
    if m:
        author = m.group(1).strip()
    
    # 从文件名提取短书名
    short_name = fn.split('(')[0].split('（')[0].strip()
    # 去掉开头的《》等
    short_name = short_name.strip('《》')
    if short_name:
        translation_authors[short_name] = author or '未知'

print(f"[1b] 译本目录: {len(os.listdir(TRANSLATION_DIR))} 文件, {len(translation_authors)} 本有作者")

# 1c. novel-txts 目录（部分文件有内嵌作者）
txt_authors = {}
for f in os.listdir(NOVEL_TXT_DIR):
    if not f.endswith('.txt') or f.startswith('.'):
        continue
    # 尝试匹配 《书名》作者：xxx
    m = re.search(r'作者[：:]\s*(.+?)\.txt$', f)
    if m:
        # 从书名提取短名
        short = f.split('.txt')[0]
        # 去掉编号前缀
        short = re.sub(r'^\d+[\.\-_]?\s*', '', short)
        # 清理多余内容
        for tag in ['（精校版全本）', '（校对版全本）', '（精校版全本+番外）', '（校对版全本+番外）', 
                     '(精校版全本)', '(校对版全本)', '(整理未校对精校版全本)', '(整理校对版全本)',
                     '（整理未校对精校版全本）', '（整理校对版全本）', '(实体封面全本)',
                     '（实体版1-3部全本）', '(实体版1-3全本)']:
            short = short.replace(tag, '').replace(tag, '')
        # 去除（校对版全本+番外）模式
        short = re.sub(r'[（(][^）)]*[）)]', '', short)
        # 去除剩余括号
        short = short.split('(')[0].split('（')[0]
        author = m.group(1).strip()
        short = short.strip()
        if short:
            txt_authors[short] = author

print(f"[1c] novel-txts内嵌作者: {len(txt_authors)} 本")

# ============================================================
# Step 2: 合并所有已知作者
# ============================================================
MASTER_AUTHORS = {}
MASTER_AUTHORS.update(fp_authors)
MASTER_AUTHORS.update(translation_authors)
MASTER_AUTHORS.update(txt_authors)
# 去掉值为'未知'或空
MASTER_AUTHORS = {k: v for k, v in MASTER_AUTHORS.items() if v and v != '未知'}
print(f"[2] 主作者表去重后: {len(MASTER_AUTHORS)} 条")

# ============================================================
# Step 3: 扫描所有 deep 报告，标注未匹配的和已修复的
# ============================================================
reports = glob.glob(os.path.join(DEEP_DIR, '*-deep.md'))
skip_reports = {'全库跨作品分析', '极端值纪录', '翻译作品对照', '体育文三作者', '游戏文进化', '修正后小样本作者'}
matched = 0
fixed = 0
still_unknown = []

for f in sorted(reports):
    fname = os.path.basename(f)
    report_name = fname.replace('analysis-', '').replace('-deep.md', '')
    
    # 跳过非单本
    if report_name in skip_reports or report_name.endswith('进化') or report_name.endswith('对比'):
        continue
    
    with open(f, 'r+', encoding='utf-8') as fh:
        content = fh.read()
        first_line = content.split('\n')[0]
        
        # 当前标注的作者
        author_current = None
        m = re.search(r'>\s*作者[：:]\s*(\S+)', content)
        if m:
            author_current = m.group(1).strip()
        
        if author_current and author_current != '未知':
            matched += 1
            continue
        
        # 查找作者
        found_author = None
        
        # 精确匹配
        if report_name in MASTER_AUTHORS:
            found_author = MASTER_AUTHORS[report_name]
        else:
            # 部分匹配
            for master_name, master_author in MASTER_AUTHORS.items():
                if report_name in master_name or master_name in report_name:
                    found_author = master_author
                    break
        
        if found_author and found_author != '未知':
            # 替换报告头
            new_content = re.sub(
                r'(>\s*作者[：:])[^\n|]*(?:\|.*)?',
                f'\\1 {found_author} |',
                content
            )
            # 如果上面没匹配到竖线格式
            if new_content == content:
                new_content = re.sub(
                    r'(>\s*作者[：:])[^\n]*',
                    f'\\1 {found_author}',
                    content
                )
            
            fh.seek(0)
            fh.write(new_content)
            fh.truncate()
            fixed += 1
            print(f"  [FIX] {report_name}: 未知 → {found_author}")
        else:
            still_unknown.append(report_name)

print(f"\n[3] 已匹配: {matched}, 已修复: {fixed}, 仍未知: {len(still_unknown)}")

if still_unknown:
    print("\n=== 仍未知作者（需要联网搜索）===")
    for s in sorted(still_unknown):
        # 看看novel-txts里有没有同名文件
        txt_matches = [f for f in os.listdir(NOVEL_TXT_DIR) if s in f or f.replace('.txt','') in s]
        trans_matches = [f for f in os.listdir(TRANSLATION_DIR) if s in f]
        info = ""
        if txt_matches:
            info += f" [txt: {txt_matches[0]}]"
        if trans_matches:
            info += f" [译: {trans_matches[0]}]"
        print(f"  {s}{info}")

# ============================================================
# Step 4: 更新 deep-analysis-v2.py 中的 KNOWN_AUTHORS 字典
# ============================================================
print("\n\n[4] 更新 KNOWN_AUTHORS 字典...")

# 读取脚本
with open(SCRIPT_FILE, 'r', encoding='utf-8') as f:
    script_content = f.read()

# 找到 KNOWN_AUTHORS 的起始和结束
start_marker = 'KNOWN_AUTHORS = {'
end_marker = '\ndef load_author_map'
start_idx = script_content.find(start_marker)
end_idx = script_content.find(end_marker, start_idx)

# 只包含fingerprint里的作者（deep报告能匹配上的）
# 以及需要补的新作者
relevant_authors = {}
for report_name in glob.glob(os.path.join(DEEP_DIR, '*-deep.md')):
    rname = os.path.basename(report_name).replace('analysis-', '').replace('-deep.md', '')
    if rname in skip_reports or rname.endswith('进化') or rname.endswith('对比'):
        continue
    if rname in MASTER_AUTHORS and MASTER_AUTHORS[rname] and MASTER_AUTHORS[rname] != '未知':
        relevant_authors[rname] = MASTER_AUTHORS[rname]
    else:
        for mn, ma in MASTER_AUTHORS.items():
            if rname in mn or mn in rname:
                relevant_authors[rname] = ma
                break

# 也包含 fingerprint 中有但还没 deep 报告的作者（用于进化分析等）
for name, author in fp_authors.items():
    if author and author != '未知' and name not in relevant_authors:
        relevant_authors[name] = author

# 生成 Python 字典字符串
lines = ['KNOWN_AUTHORS = {']
for name in sorted(relevant_authors.keys()):
    author = relevant_authors[name]
    lines.append(f"    '{name}': '{author}',")
lines.append('}')
new_dict = '\n'.join(lines)

# 替换
new_script = script_content[:start_idx] + new_dict + script_content[end_idx:]

with open(SCRIPT_FILE, 'w', encoding='utf-8') as f:
    f.write(new_script)

print(f"[4] KNOWN_AUTHORS 更新: {len(relevant_authors)} 条 (原来110条)")

print("\n✅ 全部完成")
