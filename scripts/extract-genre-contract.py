#!/usr/bin/env python3
"""
从440篇手写叙事分析中提取品类级别叙事特征。
输出genre-contract.json供v5.0协议引用。
"""
import os, re, json, sys

ANALYSIS_DIR = '/Users/Saq/.qclaw/workspace/human-flavor/novel-corpus-analysis'
PLAN_FILE = '/Users/Saq/.qclaw/workspace/human-flavor/HANDOFF-narrative-analysis-plan-2026-05-08.md'
OUTPUT = '/Users/Saq/.qclaw/workspace/human-flavor/genre-contract.json'

# 品类→书籍列表的映射
# 从handoff提取：所有有品类标签的书
GENRE_MAP = {
    '仙侠/修真': [],    # 仙侠、修真、洪荒、修仙
    '玄幻/异界': [],    # 玄幻、异界、东方玄幻
    '历史/架空': [],    # 历史、架空历史
    '科幻/末世': [],    # 科幻、末世、末日、星际
    '都市/现实': [],    # 都市、现实、情感
    '竞技/体育': [],    # 竞技、网游、体育、电竞
    '恐怖/灵异': [],    # 恐怖、灵异、盗墓、克苏鲁
    '西方奇幻': [],     # 西方奇幻、奇幻、魔法
    '无限流': [],       # 无限流、综穿
    '游戏/电竞': [],    # 游戏虚拟（区别于竞技的网游）
    '二次元/同人': [],  # 同人作品
}

# 品类关键词→规范品类名
KW_TO_GENRE = {
    '仙侠': '仙侠/修真', '修真': '仙侠/修真', '修仙': '仙侠/修真',
    '洪荒': '仙侠/修真', '道': '仙侠/修真',
    '玄幻': '玄幻/异界', '异界': '玄幻/异界', '东方玄幻': '玄幻/异界',
    '历史': '历史/架空', '架空': '历史/架空', '架空历史': '历史/架空',
    '科幻': '科幻/末世', '末世': '科幻/末世', '末日': '科幻/末世',
    '星际': '科幻/末世',
    '都市': '都市/现实', '现实': '都市/现实', '情感': '都市/现实',
    '鉴宝': '都市/现实',
    '竞技': '竞技/体育', '网游': '竞技/体育', '体育': '竞技/体育',
    '足球': '竞技/体育', '电竞': '竞技/体育', '游戏': '竞技/体育',
    '恐怖': '恐怖/灵异', '灵异': '恐怖/灵异', '盗墓': '恐怖/灵异',
    '克苏鲁': '恐怖/灵异', '悬疑': '恐怖/灵异',
    '西方奇幻': '西方奇幻', '奇幻': '西方奇幻', '魔法': '西方奇幻',
    '西方': '西方奇幻', '巫师': '西方奇幻',
    '无限': '无限流', '无限流': '无限流', '综穿': '无限流',
    '同人': '二次元/同人', '二次元': '二次元/同人',
    '美食': '都市/现实',  # 美食供应商归都市
    '军事': '历史/架空',  # 军事历史归历史
    '种田': '都市/现实',  # 种田归都市/现实
    '科技': '科幻/末世', '工业': '科幻/末世',
    '武侠': '玄幻/异界',  # 武侠归玄幻
}

# 从handoff提取品类→书名映射
def parse_handoff():
    with open(PLAN_FILE) as f:
        text = f.read()
    
    result = {}  # {书名: 品类}
    
    # 匹配模式: [品类标签] 书名
    pattern = r'\[([^\]]+)\]\s+(.+?)(?:\s*—|$)'
    for m in re.finditer(pattern, text):
        tags = m.group(1).split('/')
        title = m.group(2).strip()
        if ':' in title:
            title = title.split(':')[0].strip()
        # 匹配所有已知品类
        for tag in tags:
            tag = tag.strip()
            if tag in KW_TO_GENRE:
                genre = KW_TO_GENRE[tag]
                if title not in result:
                    result[title] = genre
                break
    
    # 匹配"✅ 作者:书名 — 品类"模式
    pattern2 = r'✅\s+[^:]+:([^—\n—]+)'
    for m in re.finditer(pattern2, text):
        title = m.group(1).strip()
        # 这需要上下文，但先标记
        pass
    
    return result

# 从analysis文件提取叙事参数
def extract_from_analysis(filepath):
    try:
        with open(filepath) as f:
            text = f.read()
    except:
        return None
    
    data = {}
    
    # 书名
    m = re.search(r'#\s*《(.+?)》|^#\s*(.+?)(?:叙事|深度|分析)', text)
    if m:
        data['title'] = (m.group(1) or m.group(2)).strip()
    else:
        # 从文件名提取
        basename = os.path.basename(filepath)
        m = re.match(r'analysis-(.+?)\.md', basename)
        if m:
            raw = m.group(1)
            raw = re.sub(r'^\d+\.?', '', raw)
            data['title'] = raw.strip()
    
    # grey/品灰值
    m = re.search(r'(?:grey|品灰|灰值|灰色密度)\S*\s*[:：=]?\s*(\d+\.?\d*)', text, re.IGNORECASE)
    if m:
        data['grey'] = float(m.group(1))
    
    # 均句长
    m = re.search(r'均句长\S*\s*[:：=]?\s*(\d+\.?\d*)', text)
    if m:
        data['avg_sentence_len'] = float(m.group(1))
    
    # 感叹号
    m = re.search(r'(?:感叹号密度|!/千字|!密度)\S*\s*[:：=]?\s*(\d+\.?\d*)', text)
    if m:
        data['exclam_per_k'] = float(m.group(1))
    
    # 句号
    m = re.search(r'句号密度\S*\s*[:：=]?\s*(\d+\.?\d*)', text)
    if m:
        data['period_per_k'] = float(m.group(1))
    
    # 逗号
    m = re.search(r'逗号密度\S*\s*[:：=]?\s*(\d+\.?\d*)', text)
    if m:
        data['comma_per_k'] = float(m.group(1))
    
    # 省略号
    m = re.search(r'省略号密度\S*\s*[:：=]?\s*(\d+\.?\d*)', text)
    if m:
        data['ellipsis_per_k'] = float(m.group(1))
    
    # 问号
    m = re.search(r'问号密度\S*\s*[:：=]?\s*(\d+\.?\d*)', text)
    if m:
        data['question_per_k'] = float(m.group(1))
    
    # 对话率
    m = re.search(r'(?:对话率|引号密度)\S*\s*[:：=]?\s*(\d+\.?\d*\s*%?)', text)
    if m:
        val = m.group(1).replace('%', '').strip()
        try:
            data['dialogue_ratio'] = float(val)
        except:
            pass
    
    # 品类关键词搜索
    text_lower = text
    for kw, genre in KW_TO_GENRE.items():
        if kw in text_lower[:500] or kw in text_lower:
            # 太宽泛，只在前300字符搜索（标题/元数据区域）
            pass
    # 先从handoff判断，后从文件元数据判断
    
    # 定性判断
    qual_signals = []
    if '爽文' in text:
        qual_signals.append('fast_paced')
    if '文学' in text or '质感' in text:
        qual_signals.append('literary')
    if '经典' in text:
        qual_signals.append('classic')
    if '开山' in text or '鼻祖' in text:
        qual_signals.append('founder')
    data['signals'] = qual_signals
    
    return data

def main():
    # 1. 从handoff提取品类映射
    print("Parsing handoff...")
    handoff_genres = parse_handoff()
    print(f"  Found {len(handoff_genres)} books with genre tags")
    
    # 2. 从所有analysis文件提取数据
    all_data = []
    files = sorted([f for f in os.listdir(ANALYSIS_DIR) 
                    if f.startswith('analysis-') and f.endswith('.md') 
                    and 'deep' not in f and '进化' not in f 
                    and '对比' not in f and '全库' not in f 
                    and '品类' not in f and 'batch' not in f])
    
    print(f"Processing {len(files)} analysis files...")
    for f in files:
        path = os.path.join(ANALYSIS_DIR, f)
        data = extract_from_analysis(path)
        if data:
            # 尝试品类匹配
            title = data.get('title', '')
            # 从handoff匹配
            if title in handoff_genres:
                data['genre'] = handoff_genres[title]
            else:
                # 模糊匹配
                for ht, hg in handoff_genres.items():
                    if title and (title in ht or ht in title):
                        data['genre'] = hg
                        break
            
            if 'genre' in data:
                all_data.append(data)
    
    print(f"  {len(all_data)} books with genre assigned")
    
    # 3. 按品类聚合统计
    genre_stats = {g: {'grey': [], 'avg_sentence_len': [], 'exclam': [], 
                        'period': [], 'comma': [], 'ellipsis': [], 
                        'question': [], 'dialogue': [], 'books': []}
                   for g in GENRE_MAP}
    
    for d in all_data:
        g = d['genre']
        if g in genre_stats:
            genre_stats[g]['books'].append(d.get('title', '?'))
            for k in ['grey', 'avg_sentence_len', 'exclam', 'period', 
                       'comma', 'ellipsis', 'question', 'dialogue']:
                if k in d:
                    genre_stats[g][k].append(d[k])
    
    # 4. 计算统计
    result = {'metadata': {
        'source': '440 hand-written narrative analyses',
        'date': '2026-05-09',
        'books_matched': len(all_data)
    }}
    
    for g, stats in genre_stats.items():
        if len(stats['books']) == 0:
            continue
        entry = {'count': len(stats['books']), 'books': stats['books'][:30]}  # 最多30本列表
        for k in ['grey', 'avg_sentence_len', 'exclam', 'period', 'comma', 'ellipsis', 'question']:
            vals = [v for v in stats[k] if v > 0]
            if vals:
                entry[k] = {
                    'mean': round(sum(vals)/len(vals), 2),
                    'min': min(vals),
                    'max': max(vals),
                    'samples': len(vals)
                }
        if stats['dialogue']:
            vals = [v for v in stats['dialogue'] if v > 0]
            if vals:
                entry['dialogue_ratio'] = round(sum(vals)/len(vals), 2)
        result[g] = entry
    
    with open(OUTPUT, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {OUTPUT} ({os.path.getsize(OUTPUT)} bytes)")
    
    # 打印摘要
    for g in result:
        if g == 'metadata':
            continue
        e = result[g]
        grey_mean = e.get('grey', {}).get('mean', '?')
        exclam = e.get('exclam', {}).get('mean', '?')
        sent = e.get('avg_sentence_len', {}).get('mean', '?')
        print(f"  {g}: {e['count']}本, grey={grey_mean}, !={exclam}/k, 均句长={sent}")

if __name__ == '__main__':
    main()
