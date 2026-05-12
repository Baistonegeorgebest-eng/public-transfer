#!/usr/bin/env python3
"""
全文深挖扫描 v2 - 全面福利内容提取
标准更宽：不只丝袜高跟，而是所有能产生"福利感"的内容
分层：L1日常暧昧 → L2擦边 → L3明确暗示 → L4VIP级别
"""

import os, re, json
from collections import defaultdict

# ========== 全面福利关键词体系 v2 ==========
WELFARE_KEYWORDS = {
    # ===== 第一层：身体描写 =====
    '身体部位': {
        '上半身': [
            '锁骨', '香肩', '玉颈', '粉颈', '后颈', '耳垂', '耳根',
            '蝴蝶骨', '肩胛', '胸口', '胸前', '酥胸', '玉峰', '双峰',
            '胸脯', '蓓蕾', '饱满', '高耸', '挺拔', '浑圆.*胸', '丰满',
            '乳沟', '沟壑', '峰峦', '山峰', '玉兔',
        ],
        '腰腹': [
            '纤腰', '蛮腰', '柳腰', '小蛮腰', '腰肢', '水蛇腰',
            '腰线', '盈盈一握', '不盈一握', '小腹', '肚脐', '马甲线',
        ],
        '下半身': [
            '翘臀', '丰臀', '蜜桃臀', '臀部', '臀线', '浑圆.*臀',
            '翘起.*臀', '圆润.*臀', '屁股', '翘', '大腿', '美腿',
            '玉腿', '长腿', '修长.*腿', '笔直.*腿', '纤腿', '玉柱',
            '小腿', '腿根', '腿间', '热裤', '短裤',
        ],
        '足部': [
            '丝袜', '连裤袜', '美足', '玉足', '脚踝', '脚趾', '脚底',
            '脚掌', '足弓', '赤足', '赤脚', '光脚', '嫩足', '粉足',
            '莲足', '纤足', '丝足', '小脚', '秀足', '脚丫', '脚背',
            '脚跟', '玉趾', '金莲',
        ],
        '整体': [
            '曲线', '身材', '身段', '玲珑', '婀娜', '曼妙', '窈窕',
            '凹凸有致', '前凸后翘', '黄金比例', '魔鬼身材', '火辣',
            '性感', '丰满', '苗条', '高挑', '娇小',
        ],
    },

    # ===== 第二层：服饰描写 =====
    '服饰': {
        '丝袜高跟': [
            '丝袜', '连裤袜', '吊带袜', '长筒袜', '短袜', '棉袜',
            '高跟鞋', '高跟', '细跟', '粗跟', '尖头', '绑带',
            '玛丽珍', '短靴', '长靴', '过膝靴',
        ],
        '裙装': [
            '短裙', '超短裙', '迷你裙', '百褶裙', '包臀裙', 'A字裙',
            '长裙', '连衣裙', '吊带裙', '抹胸裙', '开衩裙', '旗袍',
            '晚礼服', '晚装', '套裙', '制服裙',
        ],
        '内衣/私密': [
            '内衣', '胸罩', '文胸', '内裤', '丁字裤', '蕾丝',
            '吊带', '吊带衫', '背心', '抹胸', '肚兜', '亵衣',
            '睡衣', '睡袍', '浴袍', '浴巾', '比基尼', '三点式',
        ],
        '特殊服饰': [
            '女仆装', '护士装', '校服', '制服', '旗袍', '紧身衣',
            '紧身', '露背', '低胸', '深V', '透视', '薄纱',
            '网纱', '镂空', '若隐若现',
        ],
    },

    # ===== 第三层：动作描写 =====
    '亲密动作': {
        '轻度': [
            '靠近', '贴近', '依偎', '并肩', '搀扶', '牵手',
            '挽住', '搭肩', '搂腰', '环住', '揽住',
        ],
        '中度': [
            '搂住', '抱住', '拥入怀', '贴紧', '缠绕', '盘绕',
            '抚摸', '抚过', '摩挲', '揉', '捏', '蹭',
            '握住', '抓紧', '触碰', '触摸',
        ],
        '重度': [
            '亲吻', '吻住', '吻上', '深吻', '热吻', '唇齿',
            '舌尖', '吮吸', '啃咬', '咬住嘴唇',
            '压在身下', '骑在', '跨坐', '缠绵',
        ],
    },

    # ===== 第四层：暧昧反应 =====
    '暧昧反应': {
        '面部': [
            '脸红', '羞红', '面红耳赤', '双颊绯红', '霞飞双颊',
            '耳根.*红', '耳根发烫', '脸烫', '面若桃花', '红晕',
            '酡红', '绯红', '飞红',
        ],
        '身体': [
            '心跳加速', '心如鹿撞', '小鹿乱撞', '心跳漏拍',
            '呼吸急促', '喘息', '气息不稳', '娇喘',
            '发抖', '颤抖', '战栗', '发软', '瘫软', '酥软',
            '全身发烫', '体温升高', '身体发热',
        ],
        '声音': [
            '呻吟', '嘤咛', '呢喃', '娇嗔', '嗔怪', '娇羞',
            '含羞', '嗲声', '撒娇', '呢喃', '低吟',
            '轻哼', '娇呼', '惊呼',
        ],
    },

    # ===== 第五层：环境/氛围 =====
    '暧昧氛围': {
        '场景': [
            '只有.*两人', '独处', '密室', '卧室', '床上', '浴池',
            '温泉', '更衣室', '换衣', '洗澡', '沐浴', '泡澡',
            '月光', '烛光', '昏暗', '暧昧', '私密',
        ],
        '意外': [
            '不小心', '无意中', '碰巧', '撞见', '偷看', '窥视',
            '走光', '走错房间', '摔倒', '扑倒', '压在',
            '衣服.*湿', '衣服.*破', '衣服.*掉', '走光',
        ],
    },

    # ===== 第六层：暗示性对话 =====
    '暗示对话': [
        '你昨晚有没有', '别在这里', '等一下', '别动',
        '你再这样', '快住手', '忍不了', '就差一点',
        '好不好', '别看', '不许看', '闭上眼睛',
        '你想要', '可以吗', '确定吗',
    ],

    # ===== 第七层：事后暗示 =====
    '事后暗示': [
        '扣上.*扣子', '整理.*衣服', '整理.*头发',
        '撩到耳后', '系好.*鞋带', '拉下.*裙摆',
        '裹紧.*被子', '脸红.*走了', '小跑.*离开',
        '早上好', '昨晚.*嗯', '没有继续说',
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

def scan_novel(name, filepath):
    """全文扫描一本小说"""
    text = read_novel(filepath)
    if not text or len(text) < 1000:
        return None

    char_count = len(text)
    results = {}

    for category, subcats in WELFARE_KEYWORDS.items():
        if isinstance(subcats, dict):
            for subcat, keywords in subcats.items():
                hits = {}
                total = 0
                for kw in keywords:
                    count = len(re.findall(kw, text))
                    if count > 0:
                        hits[kw] = count
                        total += count
                if total > 0:
                    key = f"{category}/{subcat}"
                    results[key] = {
                        'total': total,
                        'density': round(total / (char_count / 10000), 2),
                        'keywords': hits,
                    }
        else:
            keywords = subcats
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

    return {
        'char_count': char_count,
        'results': results,
    }


def main():
    novel_dir = 'novel-txts'

    # 先扫描太阳王之证做标杆
    target_novels = [
        '太阳王之证', '斗破苍穹', '龙族',
        '斗罗大陆', '狂神', '天珠变', '琴帝', '神印王座',
        '绿茵巨星', '绿茵教父', '绿茵峥嵘', '足球豪门',
        '好色小姨', '花都猎人', '我的美女总裁老婆',
        '异世之风流大法师', '搜神记', '雪中悍刀行',
        '大奉打更人', '诡秘之主', '冰与火之歌',
    ]

    all_data = {}

    for name in target_novels:
        filepath = f'{novel_dir}/{name}.txt'
        if not os.path.exists(filepath):
            # 模糊匹配
            matches = [f for f in os.listdir(novel_dir) if name in f and f.endswith('.txt')]
            if matches:
                filepath = f'{novel_dir}/{matches[0]}'
            else:
                print(f"❌ {name} - 未找到")
                continue

        print(f"扫描 {name}...", end=" ", flush=True)
        data = scan_novel(name, filepath)
        if data:
            all_data[name] = data
            # 计算总福利密度
            total_hits = sum(v['total'] for v in data['results'].values())
            density = round(total_hits / (data['char_count'] / 10000), 1)
            print(f"✅ {data['char_count']//10000}万字 总命中:{total_hits} 密度:{density}/万字")
        else:
            print("❌ 读取失败")

    # 保存JSON
    output_path = 'novel-corpus-analysis/welfare-deep-scan-v2.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"\n数据已保存至 {output_path}")

    # 输出太阳王之证的完整分析
    print("\n" + "="*80)
    print("## 太阳王之证 全文福利内容分析")
    print("="*80)

    if '太阳王之证' in all_data:
        data = all_data['太阳王之证']
        cc = data['char_count']
        print(f"全文 {cc//10000}万字\n")

        # 按总命中排序
        sorted_cats = sorted(data['results'].items(), key=lambda x: -x[1]['total'])

        for cat, info in sorted_cats:
            density = info['density']
            total = info['total']
            top_kws = sorted(info['keywords'].items(), key=lambda x: -x[1])[:10]
            kw_str = ', '.join(f'{k}({v})' for k, v in top_kws)
            print(f"\n### {cat} ({total}次, {density}/万字)")
            print(f"  {kw_str}")


if __name__ == '__main__':
    main()
