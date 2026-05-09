# 门禁标准+自检清单

> expert-quality-gate 的详细参考。按需加载。

## 七-C、F类检测：场景双版本（语义级）← v1.5新增

### 触发条件

**适用范围**：所有曾使用 batch（批量）模式生成的项目。单章模式项目可跳过此检测。
**触发时机**：Full Audit（全量审计）时强制执行，Post-Write 验证时对有 batch 历史的项目执行。

### 背景与根因

batch 模式下，模型分批次独立生成章节内容。当不同批次需要描写同一场景时（如战斗延续、场景切换回溯），模型会生成**措辞不同但语义完全相同**的段落。这类问题无法通过字符串去重（J类）检测，因为两次写法在字面上不同。

**实战数据（气功砍穿神魔一二部，2026-04-08）**：
- 字符串去重（J类）：发现 126 处
- 语义相似度检测（F类）：额外发现 **104 处**场景双版本
- 累计 **230 处** batch 残留
- 最严重：ch99 神庙探秘(9处)、ch14 铁证如山(5处)

**结论**：场景双版本是 batch 模式的固有缺陷，无法通过事后扫描根除。最根本的解决方案是采用**单章生成模式**。

### 检测方法

#### 方法一：段落级语义相似度（推荐）

```python
import re, os, glob
from difflib import SequenceMatcher

def find_scene_double_versions(filepath, threshold=0.75, min_len=50):
    """检测同一文件内语义相同但措辞不同的段落对"""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    # 按章节分隔
    chapters = re.split(r'(?m)^第\d+章.*$', content)
    all_paras = []
    for ci, ch in enumerate(chapters):
        paras = [p.strip() for p in re.split(r'\n{2,}', ch) if len(p.strip()) >= min_len]
        for pi, p in enumerate(paras):
            all_paras.append((ci, pi, p))
    
    issues = []
    checked = set()
    for i in range(len(all_paras)):
        for j in range(i+1, len(all_paras)):
            ci_i, pi_i, text_i = all_paras[i]
            ci_j, pi_j, text_j = all_paras[j]
            # 同一章节内跳过（那是J类的职责）
            if ci_i == ci_j:
                continue
            key = (i, j)
            if key in checked:
                continue
            checked.add(key)
            # 语义相似度：用 SequenceMatcher 对字符级比较
            ratio = SequenceMatcher(None, text_i, text_j).ratio()
            if ratio >= threshold:
                preview = text_i[:60].replace('\n', ' ')
                issues.append({
                    'ch1': ci_i, 'para1': pi_i,
                    'ch2': ci_j, 'para2': pi_j,
                    'similarity': f'{ratio:.0%}',
                    'preview': preview
                })
    return issues

for fpath in sorted(glob.glob('ch*.txt')):
    issues = find_scene_double_versions(fpath)
    name = os.path.basename(fpath)
    if issues:
        print(f'🔴 [{name}] {len(issues)}处场景双版本')
        for iss in issues:
            print(f'   Ch{iss["ch1"]}¶{iss["para1"]} ↔ Ch{iss["ch2"]}¶{iss["para2"]} (相似{iss["similarity"]}): {iss["preview"]}...')
    else:
        print(f'✅ [{name}] 无场景双版本')
```

#### 方法二：关键词重叠检测（快速筛查）

```bash
# 提取每段前20字作为指纹，统计跨章节重复
for f in ch*.txt; do
  echo "--- $f ---"
  python3 -c "
import re
with open('$f') as fh:
    content = fh.read()
chapters = re.split(r'(?m)^第\d+章.*$', content)
fingerprints = {}
for ci, ch in enumerate(chapters):
    paras = [p.strip()[:20] for p in re.split(r'\n{2,}', ch) if len(p.strip())>=30]
    for p in paras:
        if p in fingerprints:
            prev_ci = fingerprints[p]
            if prev_ci != ci:
                print(f'⚠️ Ch{prev_ci} ↔ Ch{ci}: \"{p}...\"')
        else:
            fingerprints[p] = ci
"
done
```

### 修复流程

```
① 运行检测脚本，获取所有场景双版本对
② 对比两版，保留质量更高/更完整的版本
③ 删除或重写较弱版本
④ 字数检查：删除后验证字数是否达标
⑤ 重新运行检测，确认 0 残留
⑥ 更新 BOOK-STATUS.md
```

### F类问题根因与预防

```
根因：batch 模式下，不同批次独立生成同一场景的不同版本
直接原因：所有扫描只做字符串去重，无法检测语义相同但措辞不同的段落
预防措施：
  ① 所有新项目强制采用单章生成模式（铁律）
  ② 有 batch 历史的旧项目，Full Audit 必须包含 F 类检测
  ③ F 类检测结果纳入 BOOK-STATUS.md 的问题追踪清单
```

### 与 J 类的关系

| 维度 | J类（v1.3） | F类（v1.5） |
|------|------------|------------|
| 检测范围 | 同文件内 | 同文件内 |
| 匹配方式 | 字符串精确/高度相似 | 语义相似度（阈值75%） |
| 根因 | 清理/重写残留 | batch 模式固有缺陷 |
| 检测成本 | 低（grep） | 中（Python） |
| 触发场景 | Post-Write 强制 | Full Audit 强制 / Post-Write（batch项目） |



## 八、红线规则（10条，不可跳过）

```
1  【Pre-Write强制】章节文件写入前必须先执行Pre-Write扫描
2  【Post-Write强制】章节文件写入后必须执行Post-Write验证
3  【未验证不放行】未通过Post-Write验证的文件，禁止继续操作
4  【日志≠状态】足迹记录的是操作日志，不等于当前状态
5  【已清洁不阻断】前版本的"已清洁"标签不能阻断后续扫描
6  【状态从实际生成】BOOK-STATUS.md必须从实际文件生成
7  【禁止带病放行】验证失败必须回滚或重新修改，不能带病放行
8  【新问题即更新】发现新类型问题，立即加入第七节分类体系
9  【精确匹配优先】模板检测使用-F固定字符串，消除子串误报 ← v1.2新增
10 【连续性必查】每次Post-Write必须执行章节连续性校验 ← v1.2新增
```

---

## 九、协作关系

```
skill-safety-protocol → 执行修改 → expert-quality-gate(Post-Write)
                                         ↓
                               验证通过？否 → 回滚
                               验证通过？是 → expert-footprint（记录）
                               验证通过？是 → expert-logic（逻辑抽查）
                               验证通过？是 → expert-revision（如需改写）

novel-expert-system → 写作流程 → expert-quality-gate（成稿门禁）
                                         ↓
                               门禁通过？否 → 停在当前章节
                               门禁通过？是 → 进入下一章

novel-framework-first → 框架先行 → novel-expert-system → expert-quality-gate
```

---

## 十、20种已知填充模板（v1.2扩展·精确匹配库）

```
# 使用方式：grep -F "模板文本" target.txt
# 注意：必须使用-F（固定字符串匹配），禁止正则子串匹配

1.  "内心深处有一个声音在提醒他"
2.  "脚步轻移，身体微微侧转"
3.  "一种说不清的情绪涌上心头"
4.  "阿尔弗在旁边挠了挠头"
5.  "围观的人群中传来窃窃私语"
6.  "他沉默了片刻，目光落在手中的茶杯"
7.  "他微微皱眉，手指不自觉地在桌面上"
8.  "夜色如墨，繁星点点"
9.  "窗外的风带着一丝凉意"
10. "他深吸一口气，五禽戏的起手式"
11. "晨光从窗帘的缝隙"
12. "旁边一个年轻的侍从忍不住插嘴"
13. "壁炉里的余烬"
14. "月光如水"
15. "远山只剩剪影"
16. "炊烟袅袅"
17. "他的目光落在"（D类高频动作）← v1.2新增
18. "嘴角微微上翘"（D类高频动作）← v1.2新增
19. "身形猛然一动，速度快到在原地留下了一道残影"
20. "没有急着出手，而是缓缓调整呼吸"
```

**误报判断标准（v1.2重要说明）：**
```
命中后人工判断：
  命中 + 有叙事功能 = 误报，放行
  命中 + 无叙事功能 = 真实残留，标记🔴

判断三个问题：
  · 该句是否推动了情节？
  · 该句是否揭示了角色状态？
  · 删除该句后上下文是否断裂？
  三个都答"否"→ 确认为填充残留
```

---

## 十一、三级文件大小阈值（v1.2升级）

| 阈值 | 标记 | 操作 |
|------|------|------|
| ≤90KB | ✅ 正常 | 无操作 |
| 90-100KB | 🟡 监控 | 记录，下次审计复查 |
| 100-120KB | 🔴 人工审查 | 检查重复段落、可拆分章节 |
| >120KB | ❌ 强制拆分 | 必须拆分为多个文件 |

---

## 十二、维护记录

```
v1.0 MiMoClaw原始版：2026-04-04
v1.0 自主修订版：2026-04-04
v1.1 合并版：2026-04-04
v1.2 节奏增强版：2026-04-04
  + 模板检测改为-F精确匹配，消除子串误报
  + 模板库扩展至20种（新增"他的目光落在""嘴角微微上翘"）
  + 新增节奏空洞检测（H类问题）
  + 新增章节连续性校验（I类问题）
  + 文件大小三级阈值（90🟡/100🔴/120❌）
  + 新增红线规则第9-10条
  + 问题分类扩展至A-I九类
  + BOOK-STATUS.md存放位置规范化
```

*v1.2 · 2026-04-04 · 节奏增强版 · 基于第一部质量升级plus版实战反馈*


---

## 十三、剧情推进校验集成（v1.4新增）

> 与 expert-revise-loop 的 Plot-Pace-Checker 联动。quality-gate 管"文本质量"，本节管"剧情节奏质量"。

### 13.1 K类检测：剧情推进偏差

| 编号 | 检测项 | 触发条件 | 严重度 |
|------|--------|---------|--------|
| K1 | 节奏过快 | 一章完成了规划中>=2章的内容 | 严重 |
| K2 | 剧情偏移 | 输出包含PLOT-FRAMEWORK中未规划的情节推进 | 中等 |
| K3 | 情感跳跃 | 角色关系在单章内跨>=2个亲密等级 | 中等 |
| K4 | 爽点过密 | 连续2章有爽点爆发（无铺垫间隔） | 轻微 |
| K5 | 设定过早揭示 | 出现了规划中后期才出现的世界观元素 | 严重 |
| K6 | 伏笔过早回收 | 回收了规划中后期才该回收的伏笔 | 中等 |
| K7 | 伏笔未记录 | 埋了新伏笔但未写入 bookstatus | 轻微 |

### 13.2 K类检测流程

```
Post-Write 验证时，额外执行：
1. 读取 PLOT-FRAMEWORK 中本章的规划
2. 逐条对比输出内容 vs 规划内容
3. 检测 K1-K7 偏差
4. 未通过 -> 标记为 K类问题，移交 expert-revise-loop
```

### 13.3 与 revise-loop 的联动

```
quality-gate 检测到 K类问题 ->
  输出问题清单（含 K类标记）->
  expert-revise-loop 接收 ->
  按 §3.3 节奏异常修正策略处理 ->
  修正后重新 quality-gate 全流程验证
```

---


---

## 十四、ERRORS.md 自动写入（v1.5新增）

### 14.1 触发条件

Post-Write 验证发现以下任一问题时，**自动写入项目 ERRORS.md**：

```
自动写入：
  ① J类（文件内段落重复）→ 写入
  ② F类（场景双版本）→ 写入
  ③ K类（剧情推进偏差）→ 写入
  ④ 三级阈值触发❌（文件>120KB强制拆分）→ 写入
  ⑤ 章节连续性断裂（I类）→ 写入

人工判断写入：
  ⑥ A-E类模板残留（需确认非误报后写入）
  ⑦ 节奏空洞（H类，需确认非刻意设计）
```

### 14.2 写入格式

```markdown
## [项目名-ERR-YYYYMMDD-XXX] [问题类别]

**章节**: 第XX章
**严重程度**: [low/medium/high/critical]
**问题描述**: [具体描述问题现象]
**检测方式**: [J类grep扫描 / F类语义对比 / K类剧情对比 / ...]
**影响范围**: [影响了哪些章节/角色/情节线]
**根因分析**: [为什么会发生——batch模式/清理残留/上下文丢失/...]
**修正方案**: [如何修复]
**预防措施**: [如何避免——加入禁止列表/改用单章模式/...]
```

### 14.3 执行流程

```
Post-Write 验证 → 发现问题
  ↓
判断是否触发 ERRORS.md 写入（14.1规则）
  ↓
是 → 生成 ERRORS.md 条目 → 追加到项目 ERRORS.md
  ↓
同时更新 expert-bookstatus 的变更日志
  ↓
继续标准 Post-Write 流程（修正/回滚/标记）
```

### 14.4 文件位置

```
项目根目录/ERRORS.md
与 .bookstatus.md / .footprint.md 同级
```



*v1.4 - 2026-04-06 追加§十三：K类剧情推进检测 + revise-loop联动*
