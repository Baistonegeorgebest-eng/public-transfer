#!/usr/bin/env python3
"""
从 999 份分析报告中提取结构化数据
输出：CSV + JSON（全量指纹表）

区分三类文件：
  - 普通分析（analysis-*.md）
  - 深度分析（analysis-*-deep.md）→ 额外提取感官/福利/句式
  - 批次汇总（analysis-batch-*.md）→ 跳过（已含在单本分析中）

排除非小说文件（P.D.詹姆斯等英文名作者）
"""

import os
import re
import json
import csv
import sys
from pathlib import Path
from typing import Optional

# ── 路径 ──
BASE = Path(__file__).resolve().parent.parent / "analysis"
OUT_DIR = Path(__file__).resolve().parent.parent / "extract"
OUT_DIR.mkdir(exist_ok=True)

# ── 非小说文件过滤 ──
NON_NOVEL_PATTERNS = [
    r"analysis-batch-",  # 批次汇总已含在单本分析中，跳过
]


def is_novel_file(fname: str) -> bool:
    for pat in NON_NOVEL_PATTERNS:
        if re.search(pat, fname):
            return False
    return True


def parse_number(s: str) -> Optional[float]:
    """安全解析数字，处理 **粗体**、逗号、百分号等"""
    if not s:
        return None
    s = s.strip().strip("*").strip("%").replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def extract_punctuation_fingerprint(text: str) -> dict:
    """提取标点指纹表（一、标点指纹）或 header fingerprint 行"""
    data = {}

    # ── 方式1：header fingerprint 行（如 zhttty 系列）──
    # > **fingerprint**：句号5.7 | 感叹2.76 | 省略5.38 | 均句65.3字 | 段均100.2字 | 长句率62.1% | grey=9
    fp_line = re.search(r"[>＞].*?fingerprint.*?[：:](.+?)(?:\n|$)", text, re.IGNORECASE)
    if fp_line:
        fp_text = fp_line.group(1)
        # 句号5.7 / 感叹2.76 / 省略5.38
        for m in re.finditer(r"(句号|感叹|省略|逗号|问号)\s*([0-9.]+)", fp_text):
            key = m.group(1)
            data[key] = float(m.group(2))
        # 均句65.3字
        m = re.search(r"均句\s*([0-9.]+)\s*字", fp_text)
        if m:
            data["均句"] = float(m.group(1))
        # 段均100.2字
        m = re.search(r"段均\s*([0-9.]+)\s*字", fp_text)
        if m:
            data["段均"] = float(m.group(1))
        # 长句率62.1%
        m = re.search(r"长句率\s*([0-9.]+)\s*%", fp_text)
        if m:
            data["长句(>30字)%"] = float(m.group(1))

    # ── 方式2：标准表格 ──
    # 匹配 | 指标 | 本作/数值 | ... 格式，兼容多种列名
    pattern = r"\|\s*(逗号|句号|感叹|省略|问号|均句|中位句|句长变异|长句|超长句|短句|对话占比|段均|情绪密度|感叹号|省略号|逗号/千字|句号/千字|感叹号/千字|省略号/千字|问号/千字|均句长|感叹号（！）|省略号（……）|句号（。）|逗号（，）|问号（？）)\s*\|[^|]*\|\s*[~≈]?\s*([0-9.]+)"
    for m in re.finditer(pattern, text):
        key = m.group(1).strip()
        val = parse_number(m.group(2))
        if val is not None:
            # 统一键名
            if "感叹" in key:
                key = "感叹"
            elif "省略" in key:
                key = "省略"
            elif "逗号" in key:
                key = "逗号"
            elif "句号" in key:
                key = "句号"
            elif "问号" in key:
                key = "问号"
            elif "均句" in key:
                key = "均句"
            data[key] = val

    # ── 方式3：逐行扫描（兼容不同表格列数）──
    valid_keys = ("逗号", "句号", "感叹", "省略", "问号",
                  "均句", "中位句", "句长变异系数",
                  "长句(>30字)%", "超长句(>50字)%",
                  "短句(≤10字)%", "对话占比", "段均", "情绪密度")
    if len(data) < 3:
        for line in text.split("\n"):
            if "|" not in line:
                continue
            cells = [c.strip().strip("*") for c in line.split("|")]
            if len(cells) < 3:
                continue
            key = cells[1]
            # 统一键名
            norm_key = key
            if "感叹" in norm_key:
                norm_key = "感叹"
            elif "省略" in norm_key:
                norm_key = "省略"
            elif "逗号" in norm_key:
                norm_key = "逗号"
            elif "句号" in norm_key:
                norm_key = "句号"
            elif "问号" in norm_key:
                norm_key = "问号"
            elif "均句" in norm_key:
                norm_key = "均句"
            # 找第一个是数字的列
            for cell in cells[2:]:
                val = parse_number(cell)
                if val is not None and norm_key in valid_keys:
                    data[norm_key] = val
                    break

    # ── 方式4：正文中散落的数值 ──
    # 感叹号密度仅0.34/千字 / 感叹号密度0.34/千字 / 感叹号密度：0.34/千字
    if "感叹" not in data:
        for pat in [
            r"感叹.*?密度[仅是达为]?\s*([0-9.]+)/千字",
            r"感叹号[仅是达为]?\s*([0-9.]+)/千字",
            r"感叹.*?([0-9.]+)\s*/\s*千字",
        ]:
            m = re.search(pat, text)
            if m:
                data["感叹"] = float(m.group(1))
                break
    if "省略" not in data:
        for pat in [
            r"省略.*?密度[仅是达为]?\s*([0-9.]+)/千字",
            r"省略号[仅是达为]?\s*([0-9.]+)/千字",
            r"省略.*?([0-9.]+)\s*/\s*千字",
        ]:
            m = re.search(pat, text)
            if m:
                data["省略"] = float(m.group(1))
                break
    if "逗号" not in data:
        m = re.search(r"逗号.*?密度[仅是达为]?\s*([0-9.]+)/千字", text)
        if m:
            data["逗号"] = float(m.group(1))
    if "句号" not in data:
        m = re.search(r"句号.*?密度[仅是达为]?\s*([0-9.]+)/千字", text)
        if m:
            data["句号"] = float(m.group(1))
    if "均句" not in data:
        for pat in [
            r"均句[长长]?\s*[：:为是]\s*([0-9.]+)\s*字",
            r"平均句长[：:为是]?\s*([0-9.]+)\s*字",
            r"句长.*?([0-9.]+)\s*字",
        ]:
            m = re.search(pat, text)
            if m:
                val = float(m.group(1))
                if 5 < val < 200:  # 合理范围
                    data["均句"] = val
                    break

    # ── 方式5：表格中的"均句长"行（如 "均句长 | **39.4字**"）──
    if "均句" not in data:
        m = re.search(r"\|\s*均句[长长]?\s*\|[^|]*\|\s*\*?\*?([0-9.]+)\s*字?", text)
        if m:
            data["均句"] = float(m.group(1))

    return data


def extract_sentence_analysis(text: str) -> dict:
    """提取句式分析表（deep文件才有）"""
    data = {}
    # 在"二、句式分析"段落中找
    m = re.search(r"## 二、句式分析(.*?)(?=## |\Z)", text, re.DOTALL)
    if not m:
        return data
    section = m.group(1)
    pattern = r"\|\s*(总句数|均句长|中位句长|句长变异系数|长句.*?%|超长句.*?%|短句.*?%|对话占比)\s*\|[^|]*\|\s*([0-9.,*]+)"
    for pm in re.finditer(pattern, section):
        key = pm.group(1).strip()
        val = parse_number(pm.group(2))
        if val is not None:
            data[key] = val
    return data


def extract_emotion_curve(text: str) -> list:
    """提取情绪密度曲线（10段数值）"""
    # 匹配感叹号密度/千字的10段数据
    m = re.search(r"(?:感叹号|情绪).*?密度.*?千字.*?按.*?分段", text)
    if not m:
        # 尝试匹配数值行
        pass

    # 找柱状图前的数值行
    lines = text.split("\n")
    for i, line in enumerate(lines):
        # 匹配包含多个数字的行，如 "  0.2    0.2    0.8    1.8 ..."
        nums = re.findall(r"\d+\.\d+", line)
        if len(nums) >= 8:  # 至少8个数值点
            # 检查上下文是否在情绪曲线区域
            context = "\n".join(lines[max(0, i-3):i+1])
            if any(kw in context for kw in ["情绪", "感叹", "密度", "分段", "曲线"]):
                return [float(n) for n in nums[:10]]

    # 备用：找包含柱状图的区域
    for i, line in enumerate(lines):
        if "█" in line and i > 0:
            # 往上找数值行
            for j in range(i-1, max(0, i-5), -1):
                nums = re.findall(r"\d+\.\d+", lines[j])
                if len(nums) >= 8:
                    return [float(n) for n in nums[:10]]
    return []


def extract_style_tags(text: str) -> str:
    """提取风格标签"""
    m = re.search(r"## (?:四|三)、风格标签\s*\n+([^\n#]+)", text)
    if m:
        return m.group(1).strip().strip("*").strip()
    return ""


def extract_narrative_features(text: str) -> dict:
    """提取叙事特征（突然/似乎/也许等词频）"""
    data = {}
    pattern = r"\*\*(突然|似乎|好像|仿佛|也许|或许|可能)\*\*\s*出现\s*(\d+)\s*次.*?(\d+\.?\d*)\s*次/万字"
    for m in re.finditer(pattern, text):
        data[m.group(1)] = {
            "count": int(m.group(2)),
            "per_10k": float(m.group(3))
        }
    return data


def extract_opening_features(text: str) -> dict:
    """提取开局特征"""
    data = {}
    m = re.search(r"## .*开局特征.*?\n(.*?)(?=## |\Z)", text, re.DOTALL)
    if not m:
        return data
    section = m.group(1)
    cm = re.search(r"章节数[：:]\s*(\d+)", section)
    if cm:
        data["chapters"] = int(cm.group(1))
    data["has_hook"] = "✅" in section and "悬念" in section
    data["has_dialogue"] = "✅" in section and "对话" in section
    return data


def extract_sensory(text: str) -> dict:
    """提取感官描写密度（deep文件才有）"""
    data = {}
    m = re.search(r"## .*感官描写密度.*?\n(.*?)(?=## |\Z)", text, re.DOTALL)
    if not m:
        return data
    section = m.group(1)
    for row in re.finditer(r"\|\s*(视觉|听觉|触觉|嗅觉|味觉)\s*\|\s*(\d+)\s*\|\s*([0-9.]+)\s*\|", section):
        sense = row.group(1)
        data[sense] = {
            "count": int(row.group(2)),
            "per_10k": float(row.group(3))
        }
    return data


def extract_welfare(text: str) -> dict:
    """提取福利内容扫描L1-L7（deep文件才有）"""
    data = {}
    m = re.search(r"## .*福利.*?扫描.*?\n(.*?)(?=## |\Z|\n---)", text, re.DOTALL)
    if not m:
        return data
    section = m.group(1)
    levels = {"L1": "身体部位", "L2": "服饰", "L3": "亲密动作",
              "L4": "暧昧反应", "L5": "暧昧氛围", "L6": "暗示对话", "L7": "事后暗示"}
    for row in re.finditer(r"\|\s*(L\d)\s*\S*\s*\|\s*(\d+)\s*\|\s*([0-9.]+)\s*\|", section):
        level = row.group(1)
        data[level] = {
            "count": int(row.group(2)),
            "per_10k": float(row.group(3))
        }
    # 总计
    total_row = re.search(r"\|\s*\*\*总计\*\*\s*\|\s*(\d+)\s*\|\s*([0-9.]+)\s*\|", section)
    if total_row:
        data["total"] = {
            "count": int(total_row.group(1)),
            "per_10k": float(total_row.group(2))
        }
    return data


def extract_exclamation_types(text: str) -> dict:
    """提取感叹号使用类型（deep文件才有）"""
    data = {}
    m = re.search(r"感叹号使用类型.*?\n(.*?)(?=## |\Z)", text, re.DOTALL)
    if not m:
        return data
    section = m.group(1)
    for row in re.finditer(r"-\s*(情绪爆发|节奏标记|系统/设定)[：:]\s*([0-9.]+)%", section):
        data[row.group(1)] = float(row.group(2))
    return data


def extract_metadata(text: str, fname: str) -> dict:
    """提取元数据（作者/字数/章节）"""
    data = {"filename": fname}
    # 书名
    title_m = re.search(r"[#《「]([^》」]+)[》」]", text)
    if title_m:
        raw = title_m.group(1).strip()
        # 去掉"翻译文学叙事深度分析"等后缀
        raw = re.sub(r"翻译文学.*", "", raw).strip()
        raw = re.sub(r"叙事.*分析.*", "", raw).strip()
        raw = re.sub(r"深度分析", "", raw).strip()
        data["title"] = raw if raw else fname
    else:
        name_m = re.search(r"analysis-.*?[.．](.+?)(?:-deep)?\.md", fname)
        data["title"] = name_m.group(1) if name_m else fname

    # 作者
    author_m = re.search(r"作者[：:]\s*([^\s|*]+)", text)
    if author_m:
        data["author"] = author_m.group(1).strip()

    # 字数（万字）
    wordcount_m = re.search(r"字数[：:]\s*([0-9.]+)\s*万", text)
    if not wordcount_m:
        wordcount_m = re.search(r"([0-9.]+)\s*万字", text)
    if wordcount_m:
        data["wordcount_wan"] = float(wordcount_m.group(1))

    # 章节
    chapter_m = re.search(r"(?:约|共)?\s*(\d+)\s*章", text)
    if chapter_m:
        data["chapters"] = int(chapter_m.group(1))

    # 品类
    genre_m = re.search(r"品类[：:]\s*([^\s|*]+)", text)
    if genre_m:
        data["genre"] = genre_m.group(1).strip()

    # 是否译本
    if "翻译" in text or "译本" in text or "TCI" in text:
        data["is_translated"] = True

    return data


def parse_file(filepath: Path) -> Optional[dict]:
    """解析单个分析文件"""
    fname = filepath.name
    if not is_novel_file(fname):
        return None

    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  ⚠️ 读取失败: {fname}: {e}", file=sys.stderr)
        return None

    is_deep = "-deep" in fname

    record = {}

    # 元数据
    meta = extract_metadata(text, fname)
    record.update(meta)
    record["is_deep"] = is_deep
    record["file_size_kb"] = round(filepath.stat().st_size / 1024, 1)

    # 标点指纹（普通+深度都有）
    pf = extract_punctuation_fingerprint(text)
    for k, v in pf.items():
        record[f"punct_{k}"] = v

    # 情绪曲线
    curve = extract_emotion_curve(text)
    if curve:
        record["emotion_curve"] = curve

    # 风格标签
    tags = extract_style_tags(text)
    if tags:
        record["style_tags"] = tags

    # 叙事特征
    nf = extract_narrative_features(text)
    if nf:
        record["narrative_features"] = nf

    # 开局特征
    ofeats = extract_opening_features(text)
    if ofeats:
        record["opening"] = ofeats

    # 仅深度分析
    if is_deep:
        sa = extract_sentence_analysis(text)
        for k, v in sa.items():
            record[f"sentence_{k}"] = v

        sensory = extract_sensory(text)
        if sensory:
            record["sensory"] = sensory

        welfare = extract_welfare(text)
        if welfare:
            record["welfare"] = welfare

        ex_types = extract_exclamation_types(text)
        if ex_types:
            record["exclamation_types"] = ex_types

    return record


def main():
    files = sorted(BASE.glob("analysis-*.md"))
    print(f"📂 扫描目录: {BASE}")
    print(f"📄 总文件数: {len(files)}")

    records = []
    skipped = 0
    errors = 0

    for f in files:
        rec = parse_file(f)
        if rec is None:
            skipped += 1
            continue
        records.append(rec)

    print(f"\n✅ 成功解析: {len(records)}")
    print(f"⏭️  跳过(batch): {skipped}")

    # 统计
    deep_count = sum(1 for r in records if r.get("is_deep"))
    normal_count = len(records) - deep_count
    print(f"📊 普通分析: {normal_count} | 深度分析: {deep_count}")

    has_punct = sum(1 for r in records if any(k.startswith("punct_") for k in r))
    has_sensory = sum(1 for r in records if "sensory" in r)
    has_welfare = sum(1 for r in records if "welfare" in r)
    print(f"📊 有标点数据: {has_punct} | 有感官数据: {has_sensory} | 有福利数据: {has_welfare}")

    # ── 输出 JSON（全量，含嵌套结构）──
    json_path = OUT_DIR / "fingerprint-all.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"\n💾 JSON: {json_path} ({json_path.stat().st_size / 1024:.0f}KB)")

    # ── 输出 CSV（扁平化，标点指纹核心字段）──
    csv_path = OUT_DIR / "fingerprint-all.csv"
    csv_fields = [
        "title", "author", "genre", "wordcount_wan", "chapters", "is_deep", "is_translated", "file_size_kb",
        # 标点指纹
        "punct_逗号", "punct_句号", "punct_感叹", "punct_省略", "punct_问号",
        "punct_均句", "punct_中位句", "punct_句长变异系数",
        "punct_长句(>30字)%", "punct_超长句(>50字)%", "punct_短句(≤10字)%",
        "punct_对话占比", "punct_段均", "punct_情绪密度",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
        writer.writeheader()
        for rec in records:
            writer.writerow(rec)
    print(f"💾 CSV: {csv_path} ({csv_path.stat().st_size / 1024:.0f}KB)")

    # ── 输出风格标签汇总 ──
    tags_path = OUT_DIR / "style-tags.json"
    tags_data = {r["title"]: r.get("style_tags", "") for r in records if r.get("style_tags")}
    with open(tags_path, "w", encoding="utf-8") as f:
        json.dump(tags_data, f, ensure_ascii=False, indent=2)
    print(f"💾 风格标签: {tags_path} ({len(tags_data)}本)")

    # ── 输出感官数据汇总（仅deep）──
    sensory_path = OUT_DIR / "sensory-data.json"
    sensory_data = {r["title"]: r.get("sensory", {}) for r in records if r.get("sensory")}
    with open(sensory_path, "w", encoding="utf-8") as f:
        json.dump(sensory_data, f, ensure_ascii=False, indent=2)
    print(f"💾 感官数据: {sensory_path} ({len(sensory_data)}本)")

    # ── 输出福利数据汇总（仅deep）──
    welfare_path = OUT_DIR / "welfare-data.json"
    welfare_data = {r["title"]: r.get("welfare", {}) for r in records if r.get("welfare")}
    with open(welfare_path, "w", encoding="utf-8") as f:
        json.dump(welfare_data, f, ensure_ascii=False, indent=2)
    print(f"💾 福利数据: {welfare_path} ({len(welfare_data)}本)")

    # ── 质量分级报告 ──
    print("\n" + "="*50)
    print("📊 质量分级")
    print("="*50)
    tiers = {"🏆≥25KB": 0, "🔵≥15KB": 0, "✅≥10KB": 0, "🟡5-10KB": 0, "⬜<5KB": 0}
    for r in records:
        sz = r.get("file_size_kb", 0)
        if sz >= 25:
            tiers["🏆≥25KB"] += 1
        elif sz >= 15:
            tiers["🔵≥15KB"] += 1
        elif sz >= 10:
            tiers["✅≥10KB"] += 1
        elif sz >= 5:
            tiers["🟡5-10KB"] += 1
        else:
            tiers["⬜<5KB"] += 1
    for k, v in tiers.items():
        print(f"  {k}: {v}本")

    # ── 缺失数据统计 ──
    print("\n📊 数据完整度")
    missing_punct = sum(1 for r in records if not any(k.startswith("punct_") for k in r))
    missing_curve = sum(1 for r in records if "emotion_curve" not in r)
    missing_tags = sum(1 for r in records if "style_tags" not in r or not r["style_tags"])
    print(f"  缺标点数据: {missing_punct}")
    print(f"  缺情绪曲线: {missing_curve}")
    print(f"  缺风格标签: {missing_tags}")


if __name__ == "__main__":
    main()
