#!/usr/bin/env python3
"""
唐家三少全系 + 绿茵巨星 全文深度感官扫描
提取：足部/腿部/胸部/臀部/亲密动作/暧昧反应/服饰 的全部例句
"""

import os, re, json
from collections import defaultdict

# ========== 配置 ==========
TARGETS = {
    # 唐家三少
    '斗罗大陆': 'novel-txts/斗罗大陆.txt',
    '斗罗大陆II绝世唐门': 'novel-txts/斗罗大陆II绝世唐门.txt',
    '斗罗大陆III龙王传说': 'novel-txts/斗罗大陆III龙王传说.txt',
    '狂神': 'novel-txts/狂神.txt',
    '天珠变': 'novel-txts/天珠变.txt',
    '琴帝': 'novel-txts/琴帝.txt',
    '神印王座': 'novel-txts/神印王座.txt',
    '空速星痕': 'novel-txts/空速星痕.txt',
    '酒神': 'novel-txts/酒神.txt',
    # 绿茵系列
    '绿茵巨星': 'novel-txts/绿茵巨星.txt',
    '绿茵峥嵘': 'novel-txts/绿茵峥嵘.txt',
    '绿茵教父': 'novel-txts/绿茵教父.txt',
    '足球豪门': 'novel-txts/足球豪门.txt',
    # 对照组（高密度绅士）
    '太阳王之证': 'novel-txts/太阳王之证.txt',
    '斗破苍穹': 'novel-txts/斗破苍穹.txt',
    '龙族': 'novel-txts/龙族.txt',
}

SENSORY_KEYWORDS = {
    '足部': [
        '丝袜', '连裤袜', '美足', '玉足', '脚踝', '脚趾', '脚底', '脚掌',
        '足弓', '赤足', '赤脚', '光脚', '嫩足', '粉足', '莲足', '纤足',
        '丝足', '小脚', '秀足', '脚丫', '脚背', '脚跟',
    ],
    '腿部': [
        '美腿', '玉腿', '大腿', '小腿', '长腿', '纤腿', '白腿', '粉腿',
        '修长.*腿', '笔直.*腿', '玉柱', '腿根', '腿间', '热裤', '短裤',
    ],
    '胸部': [
        '酥胸', '玉峰', '双峰', '胸脯', '蓓蕾', '丰满', '饱满', '浑圆',
        '高耸', '挺拔', '胸口', '胸前', '乳', '峰峦',
    ],
    '臀部': [
        '翘臀', '蜜桃臀', '臀部', '丰臀', '臀线', '圆润', '翘起', '浑圆',
        '臀', '翘', '屁股',
    ],
    '服饰': [
        '高跟鞋', '高跟', '短裙', '超短裙', '低胸', '露背', '抹胸', '开衩',
        '束腰', '紧身衣', '蕾丝', '吊带', '丝袜', '连裤袜', '热裤', '比基尼',
        '丁字裤', '内衣', '胸罩', '文胸', '睡袍', '睡衣', '旗袍', '制服',
        '校服', '女仆', '护士装',
    ],
    '亲密动作': [
        '搂住', '挽住', '抚摸', '抚过', '摩挲', '亲吻', '吻住', '拥入怀',
        '抱住', '贴近', '依偎', '揽住', '环住', '缠绕', '盘绕', '蹭',
        '捏', '揉', '摸', '触碰', '握住', '抓紧', '贴紧',
    ],
    '暧昧反应': [
        '脸红', '羞红', '娇嗔', '嗔怪', '娇羞', '含羞', '面红耳赤',
        '双颊绯红', '耳根.*红', '脸烫', '霞飞', '心如鹿撞', '小鹿乱撞',
        '心跳加速', '呼吸急促', '喘息', '呻吟', '嘤咛', '呢喃',
    ],
    '身体曲线': [
        '曲线', '腰肢', '纤腰', '蛮腰', '柳腰', '身材', '身段',
        '玲珑', '婀娜', '曼妙', '窈窕', '凹凸有致', '前凸后翘',
    ],
}

def read_novel(filepath):
    """全文读取，尝试多种编码"""
    for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=enc, errors='strict') as f:
                return f.read()
        except:
            continue
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except:
        return ""

def extract_sentences(text, keywords, max_per_kw=3):
    """提取包含关键词的句子"""
    # 按句号/感叹号/省略号/换行分句
    sentences = re.split(r'[。！？\n]+', text)
    
    results = defaultdict(list)
    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 8 or len(sent) > 120:
            continue
        for kw in keywords:
            if re.search(kw, sent):
                if len(results[kw]) < max_per_kw:
                    results[kw].append(sent)
    return results

def main():
    all_results = {}
    
    for name, filepath in TARGETS.items():
        if not os.path.exists(filepath):
            print(f"❌ {name} - 文件不存在")
            continue
        
        fsize = os.path.getsize(filepath)
        text = read_novel(filepath)
        if not text or len(text) < 1000:
            print(f"❌ {name} - 读取失败")
            continue
        
        char_count = len(text)
        print(f"\n{'='*60}")
        print(f"## {name} ({char_count//10000}万字)")
        print(f"{'='*60}")
        
        novel_data = {
            'char_count': char_count,
            'categories': {},
        }
        
        for cat, kws in SENSORY_KEYWORDS.items():
            # 统计总命中
            total_hits = 0
            kw_hits = {}
            for kw in kws:
                count = len(re.findall(kw, text))
                if count > 0:
                    kw_hits[kw] = count
                    total_hits += count
            
            if total_hits == 0:
                continue
            
            density = total_hits / (char_count / 10000)
            novel_data['categories'][cat] = {
                'total': total_hits,
                'density': round(density, 2),
                'keywords': kw_hits,
            }
            
            # 提取例句
            examples = extract_sentences(text, [k for k, v in kw_hits.items() if v >= 2])
            novel_data['categories'][cat]['examples'] = {
                kw: sents for kw, sents in examples.items()
            }
            
            # 输出
            top_kws = sorted(kw_hits.items(), key=lambda x: -x[1])[:8]
            kw_str = ', '.join(f'{k}({v})' for k, v in top_kws)
            print(f"\n### {cat} ({total_hits}次, {density:.1f}/万字)")
            print(f"  关键词: {kw_str}")
            
            # 展示例句（每个高频词1条）
            shown = 0
            for kw, sents in sorted(examples.items(), key=lambda x: -kw_hits.get(x[0], 0)):
                if sents and shown < 5:
                    print(f"  [{kw}] {sents[0][:80]}")
                    shown += 1
        
        all_results[name] = novel_data
    
    # 保存JSON
    output_path = 'novel-corpus-analysis/tjss-sensory-deep-scan.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n\n详细数据已保存至 {output_path}")

if __name__ == '__main__':
    main()
