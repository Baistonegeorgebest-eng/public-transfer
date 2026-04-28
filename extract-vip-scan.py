#!/usr/bin/env python3
"""
"不能上架"内容扫描 - VIP/订阅福利级别
"""

import os, re, json
from collections import defaultdict

VIP_KEYWORDS = {
    '直接身体': [
        '裸', '赤裸', '一丝不挂', '不着寸缕', '光溜溜', '光着身子',
        '胴体', '娇躯', '玉体', '雪肌', '凝脂', '冰肌玉骨',
        '酥胸半露', '春光外泄', '呼之欲出',
        '沟壑深陷', '峰峦起伏', '玉峰挺立',
        '翘臀', '丰臀', '蜜桃', '翘起.*臀',
        '大腿.*叉开', '腿间', '腿根', '大腿内侧',
        '粉嫩', '娇嫩', '白嫩', '嫩滑', '吹弹可破',
    ],
    '性暗示': [
        '呻吟', '娇喘', '喘息.*急促', '喘息.*粗重',
        '缠绵', '云雨', '鱼水', '翻云覆雨', '春宵',
        '欲望', '情欲', '春情', '春心', '动情',
        '高潮', '巅峰', '极乐', '销魂', '蚀骨',
        '进入', '深入', '挺进', '冲击', '律动',
        '湿', '湿润', '泛滥', '泥泞', '蜜液',
        '硬', '坚挺', '膨胀', '火热', '灼热',
    ],
    '重度亲密': [
        '压在.*身上', '骑在.*身上', '跨坐', '盘在.*腰',
        '撕开.*衣服', '扯掉.*衣服', '脱掉.*衣服',
        '吻遍', '舔', '吮吸.*脖颈', '啃咬.*耳垂',
        '手伸进.*衣服', '手探入', '手指.*滑过.*肌肤',
        '身体.*摩擦', '紧密.*贴', '没有.*缝隙',
        '缠绕.*双腿', '双腿.*缠', '双腿.*夹',
    ],
    '直接对话': [
        '想要.*你', '给我.*你', '要了.*你',
        '别停', '继续.*用力', '轻点',
        '受不了', '快点.*还要',
        '舒服', '好舒服', '太舒服了',
    ],
    '事后直接': [
        '床上.*痕迹', '床单.*红', '落红', '初夜',
        '浑身.*痕迹', '身上.*印记', '吻痕',
        '腰酸', '腿软.*走不了', '下不了床',
        '回味.*昨晚', '昨夜.*疯狂', '一夜.*缠绵',
    ],
    '私密场景': [
        '浴室.*门', '洗澡.*门开', '沐浴.*被看到',
        '更衣.*被看到', '换衣服.*被看到',
        '泡澡.*一起', '温泉.*一起', '共浴',
        '水.*身体.*透明', '湿身.*衣服.*贴',
        '浴巾.*滑落', '浴袍.*敞开',
    ],
}

def read_novel(filepath):
    for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=enc, errors='strict') as f:
                return f.read()
        except:
            continue
    return ""

def scan_vip(name, filepath):
    text = read_novel(filepath)
    if not text or len(text) < 1000:
        return None
    char_count = len(text)
    results = {}
    for category, keywords in VIP_KEYWORDS.items():
        hits = {}
        total = 0
        for kw in keywords:
            count = len(re.findall(kw, text))
            if count > 0:
                hits[kw] = count
                total += count
        if total > 0:
            results[category] = {
                'total': total,
                'density': round(total / (char_count / 10000), 2),
                'keywords': hits,
            }
    total_hits = sum(v['total'] for v in results.values())
    return {
        'char_count': char_count,
        'results': results,
        'total_hits': total_hits,
        'density': round(total_hits / (char_count / 10000), 1) if char_count > 0 else 0,
    }

def main():
    novel_dir = 'novel-txts'
    all_data = {}
    files = sorted([f for f in os.listdir(novel_dir) if f.endswith('.txt')])
    print(f'扫描不能上架内容... {len(files)} 本')

    for i, fname in enumerate(files):
        name = fname[:-4]
        filepath = os.path.join(novel_dir, fname)
        fsize = os.path.getsize(filepath)
        if fsize < 50000:
            continue
        data = scan_vip(name, filepath)
        if data and data['total_hits'] > 0:
            all_data[name] = data
        if (i+1) % 50 == 0:
            print(f'  已处理 {i+1}/{len(files)}')

    with open('novel-corpus-analysis/welfare-vip-scan.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    ranked = sorted(all_data.items(), key=lambda x: -x[1]['density'])
    print(f'\n扫描完成。{len(all_data)} 本有"不能上架"内容。')
    print(f'\n=== 不能上架内容密度TOP30 ===')
    for rank, (name, data) in enumerate(ranked[:30], 1):
        cc = data['char_count']
        total = data['total_hits']
        density = data['density']
        cats = sorted(data['results'].items(), key=lambda x: -x[1]['total'])[:3]
        cat_str = ', '.join(f'{k}({v["total"]})' for k, v in cats)
        print(f'{rank:>2}. {name:<28} {cc//10000:>4}万 {total:>6} {density:>5.1f}/万字 | {cat_str}')

    # 对比上架TOP10
    print(f'\n=== 上架TOP10的"不能上架"密度 ===')
    top_pub = ['花都猎人','异世之风流大法师','我的美女总裁老婆','搜神记','好色小姨',
               '龙族','太阳王之证','大奉打更人','狂神','冰与火之歌']
    for name in top_pub:
        if name in all_data:
            d = all_data[name]
            print(f'  {name:<28} {d["density"]:>5.1f}/万字')
        else:
            print(f'  {name:<28}   0.0/万字 (纯上架)')

    # 按题材统计
    print(f'\n=== 按题材"不能上架"平均密度 ===')
    genre_map = {
        '都市后宫': ['好色小姨','花都猎人','我的美女总裁老婆','陈二狗的妖孽人生'],
        '西幻': ['异世之风流大法师','太阳王之证','亵渎','狂神'],
        '仙侠': ['搜神记','雪中悍刀行','剑来','一念永恒','我欲封天'],
        '玄幻': ['斗破苍穹','斗罗大陆','天珠变','琴帝','神印王座'],
        '都市': ['龙族','大奉打更人','夜的命名术','明克街13号'],
        '末世': ['末世之黑暗召唤师','末世调教，绝美女神变奴隶'],
        '体育': ['绿茵巨星','绿茵教父','绿茵峥嵘','足球豪门'],
    }
    for genre, novels in genre_map.items():
        densities = [all_data[n]['density'] for n in novels if n in all_data]
        if densities:
            avg = sum(densities) / len(densities)
            print(f'  {genre}: {avg:.1f}/万字 ({len(densities)}本)')

if __name__ == '__main__':
    main()
