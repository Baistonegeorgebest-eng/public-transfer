#!/usr/bin/env python3
"""
感官词库提取脚本
从307本小说中提取五感描写句子，按题材分类，输出高频词和典型例句
"""

import os
import re
import json
from collections import defaultdict
from pathlib import Path

NOVEL_DIR = "novel-txts"
OUTPUT_DIR = "novel-corpus-analysis"

# ========== 题材分类 ==========
GENRE_MAP = {
    # 美食
    "美食": ["美食供应商", "异世界的美食家", "美食大帝", "小世界的小食堂"],
    # 美食末世
    "美食末世": ["末世之全能大师", "末世调教"],
    # 末世
    "末世": ["末世之黑暗召唤师", "末世重生之归来", "末世之植物掌控者", "我的末日避难所",
             "末世天灾：我收了贝利亚一行", "末世超级系统", "末世之随机宝箱"],
    # 仙侠
    "仙侠": ["一品修仙", "仙逆", "凡人修仙传", "遮天", "完美世界", "圣墟", "长生界",
             "仙葫", "仙箓", "神墓", "深空彼岸", "一念永恒", "三寸人间", "我欲封天",
             "道君", "星辰变", "盘龙", "莽荒纪", "沧元图", "飞剑问道", "雪鹰领主",
             "不朽", "神游", "灵境行者", "修真聊天群", "修真四万年", "一世之尊",
             "丹武至尊", "丹药修改器", "不死武皇", "不败战神", "五行天", "九鼎记",
             "寸芒", "飞升之后", "十方武圣", "极道天魔", "神秘之旅", "万千之心",
             "隐秘死角", "我的属性修行人生", "帝御山河", "人道崛起", "传奇族长",
             "我真是族长", "人皇纪", "大周皇族", "飞升之后", "史上第一祖师爷",
             "史上最强师兄", "我师兄实在太稳健了", "大荒蛮神", "星峰传说",
             "佛本是道", "龙蛇演义", "拳镇山河", "圣王", "星河大帝", "龙族",
             "亵渎", "一剑斩破九重天", "丹武至尊", "三界血歌", "光明纪元",
             "偷天", "开天录", "邪龙道", "法师传奇", "升龙道", "苟在妖武",
             "点道为止", "阳神", "永生", "万族之劫", "不灭金丹", "蛊惑魔王",
             "巫师之旅", "巫师世界", "永恒剑主", "中古战锤的五行法师"],
    # 都市
    "都市": ["大奉打更人", "明克街13号", "异常生物见闻录", "深空彼岸", "夜的命名术"],
    # 玄幻
    "玄幻": ["斗破苍穹", "武动乾坤", "大主宰", "元尊", "斗罗大陆", "斗罗大陆IV终极斗罗",
             "神印王座", "酒神", "天珠变", "冰火魔厨", "狂神", "惟我独仙",
             "万相之王", "暗影神座", "暴风法神", "超凡黎明", "香火成神道",
             "逍遥梦路", "主神崛起", "网游之纵横天下", "网游之修罗传说",
             "网游之天下无双", "网游之近战法师", "重生之最强剑神",
             "从零开始", "网游之虚空万界"],
    # 西幻
    "西幻": ["亵渎", "盘龙", "星辰变", "雪鹰领主", "沧元图", "飞剑问道",
             "黄龙真人异界游", "无限之电影杀戮", "漫威里的德鲁伊"],
    # 科幻
    "科幻": ["三体", "银河帝国", "银河界区", "流浪地球"],
    # 恐怖
    "恐怖": ["克苏鲁", "诡秘之主", "明克街13号"],
    # 历史
    "历史": ["秦吏", "唐砖", "绍宋", "神话版三国", "带着仓库到大明", "明天下"],
    # 同人
    "同人": ["霍格沃茨之血脉巫师", "霍格沃茨的毒鸡蛋", "霍格沃茨的白魔王",
             "无限恐怖", "无限曙光", "无限未来", "大宇宙时代"],
    # 言情/女频
    "言情": ["好色小姨"],
}

# 反向映射：小说名 -> 题材
NOVEL_TO_GENRE = {}
for genre, novels in GENRE_MAP.items():
    for novel in novels:
        NOVEL_TO_GENRE[novel] = genre

# ========== 感官关键词 ==========
SENSORY_PATTERNS = {
    "嗅觉": {
        "keywords": [
            "闻到", "闻着", "闻了", "嗅到", "嗅着", "气味", "味道", "香味", "香气",
            "臭味", "臭气", "腥味", "血腥味", "血腥气", "烟味", "焦味", "焦臭",
            "霉味", "腐臭", "酸臭", "恶臭", "清香", "幽香", "暗香", "浓香",
            "芳香", "芬芳", "刺鼻", "呛人", "腥甜", "腥臭", "铜腥", "铁锈味",
            "泥土味", "草木味", "花香", "果香", "肉香", "饭香", "菜香",
            "消毒水", "药味", "汗味", "体香", "香水味", "烟草味",
            "焚香", "檀香", "沉香", "龙涎", "麝香", "艾草",
            "松脂", "油脂", "油烟", "焦糊", "糊味",
        ],
        "patterns": [
            r"一股.*味", r"一阵.*香", r"弥漫着.*气",
            r"空气中.*闻", r"鼻尖.*嗅", r"鼻腔里",
            r"闻起来", r"闻上去", r"气味.*弥漫",
            r"味道.*飘来", r"味道.*散发",
        ],
    },
    "味觉": {
        "keywords": [
            "尝到", "尝了", "尝着", "品尝", "品味", "味道", "口味",
            "甜味", "苦味", "酸味", "辣味", "咸味", "鲜味", "涩味",
            "甘甜", "苦涩", "酸涩", "辛辣", "咸涩", "鲜美",
            "入口", "入喉", "入腹", "舌尖", "舌面", "舌根",
            "咀嚼", "吞咽", "咽下", "吞下", "嚼着",
            "美味", "可口", "好吃", "难吃", "好吃到",
            "回味", "回甘", "余味", "齿颊留香",
            "麻辣", "香辣", "酸辣", "甜腻", "油腻",
            "果汁", "茶香", "酒香", "汤汁", "汤鲜",
        ],
        "patterns": [
            r"吃起来", r"喝起来", r"尝起来",
            r"味道.*鲜", r"味道.*美", r"味道.*好",
            r"舌尖.*感", r"嘴里.*味",
            r"咬了一口", r"喝了一口", r"吃了一口",
        ],
    },
    "触觉": {
        "keywords": [
            "触感", "触碰", "触摸", "抚摸", "抚过", "摩挲",
            "柔软", "坚硬", "粗糙", "光滑", "细腻", "温润",
            "冰凉", "冰冷", "滚烫", "灼热", "温热", "微凉",
            "刺痛", "灼痛", "酸痛", "胀痛", "隐隐作痛",
            "鸡皮疙瘩", "汗毛", "毛孔", "起了一层",
            "指尖", "掌心", "手心", "指腹", "指节",
            "握住", "捏住", "抓住", "攥住", "松开",
            "黏腻", "黏稠", "湿滑", "干燥", "潮湿",
            "弹性", "紧致", "绵软", "硬邦邦", "软绵绵",
            "颤抖", "发抖", "哆嗦", "战栗", "打颤",
            "风刮", "风吹", "雨打", "雨淋", "日晒",
            "寒冷", "炎热", "闷热", "凉爽", "刺骨",
        ],
        "patterns": [
            r"手.*触到", r"指尖.*感", r"掌心.*触",
            r"皮肤.*感", r"身上.*感", r"脸上.*感",
            r"摸起来", r"摸上去", r"触感.*如",
            r"感觉到.*温", r"感觉到.*凉",
        ],
    },
    "听觉": {
        "keywords": [
            "听到", "听见", "听着", "声响", "声音", "声响",
            "轰鸣", "嗡鸣", "震颤", "震响", "回响",
            "脚步声", "心跳声", "呼吸声", "风声", "雨声",
            "鸟鸣", "虫鸣", "蛙声", "蝉鸣", "鸦啼",
            "剑鸣", "刀鸣", "枪响", "炮声", "爆炸声",
            "低语", "呢喃", "嘀咕", "呐喊", "咆哮", "嘶吼",
            "寂静", "安静", "喧闹", "嘈杂", "喧嚣",
            "咔哒", "噼啪", "叮当", "咣当", "砰", "嘭",
            "沙沙", "簌簌", "潺潺", "淙淙", "哗哗",
            "叮咚", "咕噜", "咯吱", "嘎吱",
        ],
        "patterns": [
            r"耳边.*响", r"耳中.*听", r"耳畔",
            r"声音.*传来", r"响声.*传来",
            r"听到.*声", r"听见.*声",
        ],
    },
    "视觉": {
        "keywords": [
            "看到", "看见", "望着", "盯着", "注视", "凝视",
            "目光", "视线", "眼中", "眼里", "眼底",
            "光芒", "光亮", "光辉", "闪烁", "闪耀", "耀眼",
            "黑暗", "漆黑", "昏暗", "灰暗", "阴暗",
            "红色", "蓝色", "绿色", "金色", "银色", "紫色",
            "碧绿", "湛蓝", "雪白", "漆黑", "赤红", "金黄",
            "晶莹", "剔透", "透明", "半透明", "朦胧",
            "轮廓", "身影", "身姿", "容貌", "面目",
            "天际", "地平线", "远处", "近处", "眼前",
        ],
        "patterns": [
            r"眼中.*映", r"视线.*落", r"目光.*停",
            r"看到.*色", r"看见.*影",
        ],
    },
}

# ========== 题材推断（从文件名） ==========
def guess_genre(filename):
    """从文件名推断题材"""
    name = Path(filename).stem
    if name in NOVEL_TO_GENRE:
        return NOVEL_TO_GENRE[name]

    # 关键词推断
    genre_keywords = {
        "末世": ["末世", "末日", "废土", "丧尸", "僵尸"],
        "仙侠": ["修仙", "修真", "仙", "道", "武", "剑", "丹", "龙", "神", "圣", "帝", "皇",
                 "功", "诀", "经", "录", "图", "记", "传", "录", "世界", "天", "元", "灵"],
        "美食": ["美食", "厨", "烹饪", "食", "菜", "料理"],
        "都市": ["都市", "城市", "校园", "校花", "总裁", "重生"],
        "玄幻": ["网游", "游戏", "系统", "穿越", "重生", "异界", "大陆"],
        "科幻": ["科幻", "机甲", "星际", "太空"],
        "恐怖": ["恐怖", "诡异", "鬼", "灵异"],
        "历史": ["三国", "唐朝", "宋朝", "明朝", "秦", "汉", "清"],
        "同人": ["同人", "漫威", "火影", "海贼", "龙珠", "霍格沃茨"],
    }
    for genre, kws in genre_keywords.items():
        for kw in kws:
            if kw in name:
                return genre

    return "未分类"


def extract_sentences(text, sensory_type):
    """从文本中提取某类感官的句子"""
    config = SENSORY_PATTERNS[sensory_type]
    keywords = config["keywords"]
    patterns = config["patterns"]

    results = []

    # 按句号/感叹号/省略号分句
    sentences = re.split(r'[。！？…]+', text)

    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 5 or len(sent) > 200:
            continue

        # 检查关键词
        matched_kw = None
        for kw in keywords:
            if kw in sent:
                matched_kw = kw
                break

        # 检查正则
        matched_pattern = None
        if not matched_kw:
            for pat in patterns:
                if re.search(pat, sent):
                    matched_pattern = pat
                    break

        if matched_kw or matched_pattern:
            results.append({
                "sentence": sent,
                "keyword": matched_kw or matched_pattern,
            })

    return results


def main():
    novel_dir = Path(NOVEL_DIR)
    if not novel_dir.exists():
        print(f"错误：{NOVEL_DIR} 目录不存在")
        return

    txt_files = sorted(novel_dir.glob("*.txt"))
    print(f"找到 {len(txt_files)} 个小说文件")

    # 按题材收集感官句子
    genre_sensory = defaultdict(lambda: defaultdict(list))
    # 按小说收集感官句子（用于统计）
    novel_stats = {}

    for i, txt_file in enumerate(txt_files):
        name = txt_file.stem
        genre = guess_genre(txt_file.name)

        try:
            text = txt_file.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"  跳过 {name}: {e}")
            continue

        text_len = len(text)
        novel_stats[name] = {"genre": genre, "char_count": text_len, "sensory": {}}

        for sensory_type in SENSORY_PATTERNS:
            sentences = extract_sentences(text, sensory_type)
            novel_stats[name]["sensory"][sensory_type] = len(sentences)

            for item in sentences:
                item["novel"] = name
                item["genre"] = genre
                genre_sensory[genre][sensory_type].append(item)

        if (i + 1) % 50 == 0:
            print(f"  已处理 {i+1}/{len(txt_files)}")

    print(f"\n处理完成。共 {len(novel_stats)} 本小说。")

    # ========== 输出结果 ==========
    output = []

    # 按题材输出每个感官类别的高频关键词和例句
    for genre in sorted(genre_sensory.keys()):
        output.append(f"\n{'='*60}")
        output.append(f"## 题材：{genre}")
        output.append(f"{'='*60}")

        for sensory_type in ["嗅觉", "味觉", "触觉", "听觉", "视觉"]:
            items = genre_sensory[genre].get(sensory_type, [])
            if not items:
                continue

            # 统计关键词频率
            kw_count = defaultdict(int)
            for item in items:
                kw_count[item["keyword"]] += 1

            # 按频率排序
            sorted_kws = sorted(kw_count.items(), key=lambda x: -x[1])

            output.append(f"\n### {sensory_type}（{len(items)} 条提取）")

            # 高频关键词
            output.append(f"高频关键词：")
            top_kws = sorted_kws[:20]
            for kw, count in top_kws:
                output.append(f"  {kw}: {count}")

            # 典型例句（每个关键词取1-2个）
            output.append(f"\n典型例句：")
            seen_kws = set()
            for item in items:
                kw = item["keyword"]
                if kw in seen_kws:
                    continue
                seen_kws.add(kw)
                if len(seen_kws) > 15:
                    break
                # 截取句子，去掉首尾空白
                sent = item["sentence"][:100]
                output.append(f"  [{kw}] {sent}")

    # ========== 按感官类别输出全库汇总 ==========
    output.append(f"\n{'='*60}")
    output.append(f"## 全库汇总（按感官类别）")
    output.append(f"{'='*60}")

    for sensory_type in ["嗅觉", "味觉", "触觉", "听觉", "视觉"]:
        all_items = []
        for genre in genre_sensory:
            all_items.extend(genre_sensory[genre].get(sensory_type, []))

        if not all_items:
            continue

        kw_count = defaultdict(int)
        for item in all_items:
            kw_count[item["keyword"]] += 1

        sorted_kws = sorted(kw_count.items(), key=lambda x: -x[1])

        output.append(f"\n### {sensory_type} 全库高频词（共 {len(all_items)} 条）")
        for kw, count in sorted_kws[:30]:
            output.append(f"  {kw}: {count}")

    # ========== 感官密度统计 ==========
    output.append(f"\n{'='*60}")
    output.append(f"## 感官密度统计（每万字感官句数）")
    output.append(f"{'='*60}")

    output.append(f"\n| 小说 | 题材 | 字数 | 嗅觉 | 味觉 | 触觉 | 听觉 | 视觉 | 感官总计 |")
    output.append(f"|------|------|------|------|------|------|------|------|---------|")

    # 按感官总计排序
    ranked = []
    for name, stats in novel_stats.items():
        total = sum(stats["sensory"].values())
        char_count = stats["char_count"]
        if char_count > 100000:  # 只统计10万字以上的
            ranked.append((name, stats, total))

    ranked.sort(key=lambda x: -x[2])

    for name, stats, total in ranked[:50]:
        cc = stats["char_count"]
        sens = stats["sensory"]
        per_wan = lambda n: f"{n / (cc/10000):.1f}" if cc > 0 else "0"
        output.append(f"| {name} | {stats['genre']} | {cc//10000}万 | "
                     f"{per_wan(sens.get('嗅觉',0))} | {per_wan(sens.get('味觉',0))} | "
                     f"{per_wan(sens.get('触觉',0))} | {per_wan(sens.get('听觉',0))} | "
                     f"{per_wan(sens.get('视觉',0))} | {per_wan(total)} |")

    # ========== 写入文件 ==========
    result_text = "\n".join(output)
    output_file = Path(OUTPUT_DIR) / "感官库提取结果.md"
    output_file.write_text(result_text, encoding="utf-8")
    print(f"\n结果已写入 {output_file}")

    # 同时保存JSON格式的详细数据
    json_data = {
        "genre_sensory": {
            genre: {
                stype: items[:100]  # 每类最多保存100条
                for stype, items in sdata.items()
            }
            for genre, sdata in genre_sensory.items()
        },
        "novel_stats": novel_stats,
    }
    json_file = Path(OUTPUT_DIR) / "sensory-extraction-data.json"
    json_file.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"详细数据已写入 {json_file}")


if __name__ == "__main__":
    main()
