# enforcement-rules（详细参考）

> 本文件为 novel-volume-workflow 的详细参考内容。按需加载。

## 九、强制 Skill 调用链（不可跳过）

> **最高优先级规则：任何创作输出和质检报告，都必须经过以下强制调用链。**
> **agent 凭"语感"判断"没问题"不算数，skill 的检查结果才算数。**

### 9.1 创作输出强制链

每次输出正文内容前（包括子代理回传的内容），必须执行：

```
Step 1：expert-writing-safety 强制检查
  → 无Markdown表格/敏感符号
  → 每段≤3行，单句≤20-25字
  → 无政治/色情/暴力违规
  → 未通过 → 不输出，修复

Step 2：expert-quality-gate Post-Write 验证
  → A-I类模板检测（16种已知模板零容忍）
  → J类文件内重复段落检测
  → 字数检查（窄口径≥2000字）
  → 文件大小检查（>90KB触发深度扫描）
  → 节奏空洞检测
  → 连续性校验
  → 未通过 → 不输出，修复

Step 3：expert-footprint 防重复扫描
  → 对照 .footprint.md 禁止列表
  → 跨章节重复检测
  → freshness 评级
  → 未通过 → 不输出，修改后重新扫描

Step 4：expert-logic 逻辑检查（条件触发）
  → 触发条件：涉及战力变化、境界突破、关键剧情转折
  → 战力无崩坏
  → 时间线无矛盾
  → 未通过 → 不输出，修复

Step 5：expert-character OOC检查（条件触发）
  → 触发条件：人物对话/行为/决策场景
  → 对照角色设定表
  → 未通过 → 不输出，修正

Step 6：更新 .bookstatus.md
  → 追加章节索引行
  → 更新进度概览

Step 7：更新 .footprint.md
  → 登记本章新元素

Step 8：输出内容
  → 只有全部通过才允许输出给用户
```

### 9.2 质检报告强制链

当 agent 报告"质检完成"或"检查没问题"时，必须实际执行以下操作并附上结果：

```
□ expert-quality-gate 的具体检测结果（不是"我觉得没问题"）
□ expert-writing-safety 的具体检测结果
□ expert-footprint 的扫描结果
□ expert-logic 的检测结果（如适用）
□ 字数统计（具体数字，不是"大概2000多字"）
□ 与 .bookstatus.md 的一致性确认

报告格式：
┌──────────────────────────────┐
│ 质检报告 ChXX                │
├──────────────────────────────┤
│ writing-safety: ✅通过 / ❌失败+具体问题 │
│ quality-gate:   ✅通过 / ❌失败+具体问题 │
│ footprint:      ✅通过 / ❌失败+具体问题 │
│ logic:          ✅通过 / ❌不适用       │
│ character:      ✅通过 / ❌不适用       │
│ 字数: 2,XXX字（窄口径）                │
│ bookstatus:     ✅已更新              │
└──────────────────────────────┘
```

### 9.3 子代理任务描述强制规则

spawn 子代理执行写作/质检任务时，任务描述必须包含：

```
1. 明确列出需要调用的 skills
2. 明确输出路径
3. 明确质检要求（必须附质检报告）
4. 明确 bookstatus 更新要求
5. 明确"未通过质检不得回传"

示例任务描述：
"写第75章，标题[XXX]，内容要点[XXX]。
 调用：expert-fanqie-novel（主）+ expert-hook + expert-pacing + expert-memory
 字数：窄口径2000-3000字
 写完后必须：
  1. 调用 expert-quality-gate Post-Write验证
  2. 调用 expert-writing-safety 合规检查
  3. 调用 expert-footprint 防重复扫描
  4. 未通过任何一项 → 修复后重新验证
  5. 通过后回传内容 + 质检报告
  6. 更新 .bookstatus.md 本章节索引
 输出路径：[项目目录]/第X卷/chXX.txt"
```

### 9.4 禁止行为清单

```
❌ 禁止：写完直接输出，不经过质检链
❌ 禁止：说"检查完毕没问题"但没有实际调用 skill
❌ 禁止：子代理回传未经质检的内容
❌ 禁止：跳过 bookstatus 更新
❌ 禁止：跳过 footprint 登记
❌ 禁止：质检未通过仍输出给用户
❌ 禁止：凭"语感"代替 skill 检查
```

---

## 十、与 AGENTS.md 的集成要求

在 AGENTS.md 或全局规则中应增加：

```
创作相关任务的强制规则：
1. 任何正文输出必须经过 §9.1 强制调用链
2. 任何质检报告必须包含 §9.2 的完整格式
3. 子代理任务描述必须遵循 §9.3 格式
4. 违反 §9.4 禁止行为清单的内容不得输出
5. 用户不需要手动要求调用 skills——这是强制流程
```

---

*v1.1 — 2026-04-06 追加 §9-10 强制 Skill 调用链规则*


---

## 十一、强制链更新：集成 revise-loop + reader-tracker（v1.2）

### 11.1 创作输出强制链（更新版）

```
初稿生成
  │
  ▼
Step 1: expert-writing-safety 合规检查
  │  -> 未通过 -> expert-revise-loop Round 1
  │
Step 2: expert-quality-gate Post-Write 验证
  │  -> 未通过 -> expert-revise-loop 按问题类型分配修正expert
  │
Step 3: expert-footprint 防重复扫描
  │  -> 未通过 -> expert-revise-loop Round 1
  │
Step 4: expert-revise-loop 剧情推进校验（Plot-Pace-Checker）
  │  对照 PLOT-FRAMEWORK 检查：
  │  - 情节推进速度是否过快
  │  - 是否包含未规划的内容
  │  - 情感节奏是否自然
  │  - 爽点密度是否合理
  │  - 世界观揭示是否过早
  │  -> 未通过 -> expert-revise-loop 修正（拆分/减速/补过渡）
  │
Step 5: expert-logic 逻辑检查（条件触发）
  │
Step 6: expert-character OOC检查（条件触发）
  │
Step 7: 更新 .bookstatus.md
  │
Step 8: 更新 .footprint.md
  │
Step 9: 输出 + 质检报告
```

### 11.2 定期数据检查（reader-tracker 集成）

```
每5-10章后自动触发（不需要用户提醒）：
  1. expert-reader-tracker 检查平台数据
  2. 对比上期数据，检测异常
  3. 如有异常 -> 生成数据诊断报告
  4. 诊断报告关联到具体章节
  5. 建议调用对应 expert 进行调整
  6. 写入 .bookstatus.md 变更日志
```

### 11.3 revise-loop 在 workflow 中的位置

```
Phase 3 逐章执行中：
  每章写完 -> 走 §9.1 强制链
  强制链第4步 = expert-revise-loop 剧情校验
  未通过 -> 进入 revise-loop 修正循环
  修正后重新走强制链
  最多3轮 -> 升级给用户
```

---

*v1.2 - 2026-04-06 集成 revise-loop + reader-tracker*


---
