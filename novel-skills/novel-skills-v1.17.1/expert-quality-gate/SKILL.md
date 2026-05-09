---
name: expert-quality-gate
description: 章节写入质量门禁专家。Use when 章节写完需要Post-Write验证、检测AI模板/字数不足/节奏空洞/连续性错误，或用户说"质检""门禁验证"时触发。
  质量门禁专家。小说/长篇项目的强制写入后验证技能。每次文件修改后自动触发，
  同时具备Pre-Write（改前扫描）、Post-Write（改后验证）、Full Audit（全量审计）三种模式。
  追踪BOOK-STATUS.md，与expert-footprint/expert-logic/expert-revision联动。
  触发条件：修改前/修改后/用户声称已修复时/加载skill时。
  v1.2新增：节奏空洞检测、章节连续性校验、精确模板匹配、三级文件大小阈值、扩展模板库至20种。v1.3新增：文件内段落重复检测（J类）——Post-Write强制流程新增品类。v1.5新增：场景双版本语义检测（F类）——batch遗留项目全量审计强制品类。
---

# 质量门禁（expert-quality-gate）v1.3

> **版本：** 1.2（2026-04-04，节奏增强版）
> **来源：** v1.1合并版 + 实战审计反馈（第一部质量升级plus版）
> **定位：** 所有小说写入操作的强制验证技能。前置安全看 skill-safety-protocol，本技能管写入后正确。
>
> **核心原则（三条，不可跳过）：**
> 1. "已修改" ≠ "已正确"，只有验证通过才算完成
> 2. 验证必须独立于执行者（防自我确认偏差）
> 3. 前版本的"已清洁"标签不能阻断后续扫描

---

## 一、触发规则（强制门禁）

必须触发本技能的场景：

```
【场景A】修改任何章节文件之前  → Pre-Write 扫描
  目的：知道目标文件的当前状态，避免带病继续写
  操作：增量扫描 → 记录 BOOK-STATUS.md

【场景B】任何章节文件写入完成后  → Post-Write 验证 ⚠️ 最重要
  目的：确认问题真的消失了，没有引入新问题
  操作：增量扫描 → 对比写入前状态 → 更新 BOOK-STATUS.md

【场景C】用户说"已修复/已清理/已检查"之后
  目的：防止"说了就是改了"的情况
  操作：独立验证扫描 → 出具差距报告

【场景D】加载本技能时
  目的：获取当前真实状态（防日志与文件脱钩）
  操作：全量审计 → 重建 BOOK-STATUS.md
```

---

## 二、BOOK-STATUS.md 规范

### 2.1 存放位置

```
优先：项目根目录/BOOK-STATUS.md（便于全局查阅）
备选：与章节文件同目录/.quality-gate/BOOK-STATUS.md
原则：一个项目只保留一份，避免状态分裂
```

### 2.2 格式（双组件）

**组件A：章节状态表（快速查阅）**

```markdown
| 文件 | 章数 | 字数 | 填充数 | 游离段落 | 状态 | 最后验证 |
|------|------|------|--------|---------|------|---------|
| ch001_ch010.txt | 10 | 26343 | 5 | 8 | 🟡待修 | 2026-04-04 |
```

状态标记：
- ✅ 通过：脚本全过 + 人工抽查通过
- 🟡 待修：发现问题，尚未修复
- ❌ 阻断：严重问题，禁止继续操作
- 📋 监控：E类超阈值，需人工判断
- 🔍 验证中：正在进行Post-Write验证

**组件B：问题追踪清单（深度追踪）**

```markdown
## 已知问题清单（活动问题）

| # | 问题类型 | 章节 | 内容摘要 | 发现日期 | 状态 |
|---|---------|------|---------|---------|------|
| 1 | F类游离段落 | ch3 | "脐下气穴边缘黑色纹路"在分隔符后 | 2026-04-04 | 🟡待修 |

## 验证记录

| 日期 | 操作 | 结果 | 验证人 |
|------|------|------|--------|
| 2026-04-04 | Pre-Write全量审计 | 发现23处游离段落 | quality-gate |
```

### 2.3 更新规则

```
① 修改前：Pre-Write扫描 → 记录当前状态
② 修改后：Post-Write扫描 → 对比前后 → 更新状态
③ 问题修复后：标记🟡 → 脚本全过+人工抽查 → 改✅
④ 状态从实际文件生成，不从操作日志推导
```

---

## 三、门禁检查清单

### 3.1 Pre-Write 扫描（修改前）

```bash
# 增量四查：
# ① 章节标题数量是否正确
grep -c "^第.*章" target.txt

# ② 已知填充残留（精确匹配 -F，消除子串误报）
for pat in \
  "内心深处有一个声音在提醒他" \
  "脚步轻移，身体微微侧转" \
  "一种说不清的情绪涌上心头" \
  "阿尔弗在旁边挠了挠头" \
  "围观的人群中传来窃窃私语" \
  "他沉默了片刻，目光落在手中的茶杯" \
  "他微微皱眉，手指不自觉地在桌面上" \
  "夜色如墨，繁星点点" \
  "窗外的风带着一丝凉意" \
  "他深吸一口气，五禽戏的起手式"; do
  cnt=$(grep -c -F "$pat" target.txt 2>/dev/null)
  [ "$cnt" -gt 0 ] && echo "⚠️ 仍有[$pat]×$cnt"
done

# ③ 字数粗查（60字以下疑似损坏）
wc -m < target.txt | awk '{if($1<60000) print "⚠️ 字数" $1 "异常"; else print "✅ 字数正常"}'

# ④ 章节连续性校验（v1.2新增）
grep "^第.*章" target.txt | grep -oP '\d+' | awk 'NR>1{if($1!=prev+1) print "⚠️ 章节跳跃:"prev"→"$1} {prev=$1}'
```

### 3.2 Post-Write 扫描（修改后）

```bash
# 第一步：目标内容是否消失（精确匹配 -F）
grep -c -F "目标模板文本" target.txt

# 第二步：章节标题完整性
grep -n "^第.*章" target.txt | wc -l

# 第三步：双标题检测
grep "^第.*章" target.txt | sort | uniq -d

# 第四步：20种模板精确检测（v1.2扩展，-F固定字符串）
for pat in \
  "内心深处有一个声音在提醒他" \
  "脚步轻移，身体微微侧转" \
  "一种说不清的情绪涌上心头" \
  "阿尔弗在旁边挠了挠头" \
  "围观的人群中传来窃窃私语" \
  "他沉默了片刻，目光落在手中的茶杯" \
  "他微微皱眉，手指不自觉地在桌面上" \
  "夜色如墨，繁星点点" \
  "窗外的风带着一丝凉意" \
  "他深吸一口气，五禽戏的起手式" \
  "晨光从窗帘的缝隙" \
  "旁边一个年轻的侍从忍不住插嘴" \
  "壁炉里的余烬" \
  "月光如水" \
  "远山只剩剪影" \
  "炊烟袅袅" \
  "他的目光落在" \
  "嘴角微微上翘" \
  "身形猛然一动，速度快到在原地留下了一道残影" \
  "没有急着出手，而是缓缓调整呼吸"; do
  cnt=$(grep -c -F "$pat" target.txt 2>/dev/null)
  [ "$cnt" -gt 0 ] && echo "🔴 残留[$pat]×$cnt"
done

# 第五步：三级文件大小阈值（v1.2升级）
size=$(wc -c < target.txt)
if [ "$size" -gt 120000 ]; then
  echo "❌ 文件过大:${size}bytes — 强制拆分"
elif [ "$size" -gt 100000 ]; then
  echo "🔴 文件偏大:${size}bytes — 人工审查"
elif [ "$size" -gt 90000 ]; then
  echo "🟡 文件较大:${size}bytes — 监控"
fi

# 第六步：章节连续性校验（v1.2新增）
grep "^第.*章" target.txt | grep -oP '\d+' | awk '
  NR==1{first=$1; prev=$1; next}
  {if($1!=prev+1){for(i=prev+1;i<$1;i++) print "⚠️ 缺失:第"i"章"} prev=$1}
  END{print "✅ 章节范围:第"first"章-第"prev"章"}
'

# 第七步：字数检查（<2000字需报告）
python3 -c "
import re
with open('target.txt') as f:
    text = f.read()
chapters = re.split(r'(?m)^第\d+章', text)
for i, ch in enumerate(chapters[1:], 1):
    chars = len(re.sub(r'\s', '', ch))
    if 0 < chars < 2000:
        print(f'⚠️ 第{i}章仅{chars}字（<2000）')
"
```

### 3.3 语义连贯性人工抽查（修改处）

```
操作流程：
  1. 找到所有被修改的位置（grep行号）
  2. 读取每个位置前后各15行
  3. 检查：场景切换是否自然 / 人物行为是否合理 / 对话前后是否连贯
  4. 若发现断裂：标记🟡，停止放行
```

---

## 四、游离段落检测

### 4.1 检测脚本

```python
import re, os, glob

def find_stray_paragraphs(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    blocks = re.split(r'^---+\s*$', content, flags=re.MULTILINE)
    issues = []
    for i in range(len(blocks) - 1):
        block_lines = [l.strip() for l in blocks[i].split('\n') if l.strip()]
        next_block_lines = [l.strip() for l in blocks[i+1].split('\n')[:5] if l.strip()]
        next_is_chapter = any(re.match(r'^第.+章', l) for l in next_block_lines)
        if not next_is_chapter and len(block_lines) >= 3:
            issues.append({'position': f'块{i+1}', 'last_content': block_lines[-3:]})
    return issues

for fpath in sorted(glob.glob('ch*.txt')):
    issues = find_stray_paragraphs(fpath)
    name = os.path.basename(fpath)
    if issues:
        print(f'🔴 [{name}] {len(issues)}处游离段落')
    else:
        print(f'✅ [{name}] 无游离段落')
```

### 4.2 修复流程

```
① 判断游离段落是否有叙事价值
② 有价值 → 融入前章或后章合适位置
③ 无价值 → 直接删除
④ 有价值但不知融入哪里 → 标记🟡待修
⑤ 删除/融入后 → 重新执行Post-Write全量扫描
```

---

## 五、章节连续性校验（v1.2新增）

### 5.1 检测脚本

```bash
for f in ch*.txt; do
  echo "--- $f ---"
  grep "^第.*章" "$f" | grep -oP '\d+' | awk '
    NR==1{first=$1; prev=$1; next}
    {if($1!=prev+1){for(i=prev+1;i<$1;i++) print "⚠️ 缺失:第"i"章"} prev=$1}
    END{print "✅ 第"first"-"prev"章（共"prev-first+1"章）"}
  '
done
```

### 5.2 与预期对比

```bash
expected=10
actual=$(grep -c "^第.*章" ch001_ch010.txt)
[ "$actual" -ne "$expected" ] && echo "❌ 期望${expected}章，实际${actual}章"
```

---

## 六、节奏空洞检测（v1.2新增）

### 6.1 定义

```
节奏空洞 = 连续N章没有🟢（释放）或⭐（高燃）标记的区间
判定标准：
  · 连续≥5章全为🟡/🔴 → 🟡监控
  · 连续≥7章全为🟡/🔴 → 🔴告警（干烧区）
  · 连续≥10章全为🟡/🔴 → ❌阻断
```

### 6.2 检测方法

```bash
# 从PLOT-FRAMEWORK.md中提取爽点矩阵
grep -oP '[⭐🟢🟡🔴❓]' PLOT-FRAMEWORK.md | awk '
BEGIN{consec=0}
{
  if($1=="🟡" || $1=="🔴") {consec++; zone=zone" "$1}
  else {
    if(consec>=5) print "⚠️ 连续"consec"章无爽点:"zone
    if(consec>=7) print "🔴 干烧区:"zone
    consec=0; zone=""
  }
}
END{if(consec>=5) print "⚠️ 末尾连续"consec"章无爽点:"zone}
'
```

### 6.3 修复策略

```
发现干烧区后的修复优先级：
1. 在干烧区中心章节插入一个小爽点（🟢级）
2. 插入方式优先级：对话打脸 > 能力展示 > 认知逆袭 > 战斗小胜
3. 插入后必须通过Post-Write验证
4. 更新PLOT-FRAMEWORK.md中的爽点标记
```

---

## 七、问题分类体系（A-J十类·v1.3扩展）

```
A类：通用意象填充（月光/壁炉/炊烟/远山）
B类：场景描写模板（暮色场景/室内光影/户外夜景）
C类：万能结尾变体（夜色渐深/灯火阑珊/夜已深）
D类：角色动作填充（阿尔弗挠头/围观窃窃私语/沉默片刻）
E类：心理描写模板（内心深处声音/灵魂深处有什么）
F类：场景双版本（语义相同但措辞不同，跨章节出现——batch固有缺陷）← v1.5升级
G类：未分类模板（存在于文件中但不在已知20种模板库中）
H类：节奏空洞（连续≥5章无爽点）← v1.2新增
I类：章节跳跃（缺失章节号）← v1.2新增
J类：文件内段落重复（同文件中完全相同或高度相似的段落出现≥2次）← v1.3新增
```

---

---

## 七-B、J类检测：文件内段落重复（v1.3新增）

### 触发条件

每次 Post-Write 验证必须执行。清理/重写操作后尤其关键——旧版本未完全删除会导致新旧两版并存。

### 检测脚本

```python
import re, os, glob

def find_duplicate_paragraphs(filepath, min_length=30):
    """检测文件内完全相同或高度相似的段落"""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    paragraphs = re.split(r'

+', content)
    seen = {}
    duplicates = []
    for i, p in enumerate(paragraphs):
        p_clean = p.strip()
        if len(p_clean) < min_length:
            continue
        p_norm = re.sub(r's+', '', p_clean)
        if p_norm in seen:
            prev_idx = seen[p_norm]
            preview = p_clean[:60].replace('
', ' ')
            duplicates.append({'first': prev_idx, 'dup': i, 'preview': preview})
        else:
            seen[p_norm] = i
    return duplicates

for fpath in sorted(glob.glob('ch*.txt')):
    dups = find_duplicate_paragraphs(fpath)
    name = os.path.basename(fpath)
    if dups:
        print(f'🔴 [{name}] {len(dups)}个重复段落')
    else:
        print(f'✅ [{name}] 无重复段落')
```

### 修复流程

```
① 精确定位：运行检测脚本，获取所有重复段落
② 判断版本：对比两版，保留质量更高的版本
③ 精确删除：按段落删除多余版本
④ 字数检查：删除后验证字数是否达标
⑤ Post-Write：重新运行检测，确认 0 残留
⑥ 更新 BOOK-STATUS.md
```

### J类问题根因

清理/重写操作特有风险：旧版本未完全删除，新旧两版并存。
防护：任何"删除+重写"操作的 Post-Write 必须跑 J 类脚本。


---

---

## 📚 References（按需加载）

| 文件 | 内容 | 什么时候读 |
|------|------|-----------|
| references/detection-rules.md | 质检检测规则 | 按需加载 |
| references/post-write-flow.md | Post-Write验证流程+连续性校验 | 按需加载 |
| references/gate-standards.md | 门禁标准+自检清单 | 按需加载 |
