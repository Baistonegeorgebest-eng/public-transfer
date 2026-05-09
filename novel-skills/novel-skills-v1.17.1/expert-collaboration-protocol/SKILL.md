---
name: expert-collaboration-protocol
description: 多Expert协同协议。Use when 需要调度多个Expert协同工作、遇到Expert冲突需要仲裁、需要Token节省规范、或用户问"怎么让多个skill配合""Expert之间怎么协调"时触发。
---

# 专家联动协议 v2.0

> 版本：2.0.0（全面重构）
> 定位：多Expert协同写作系统的"宪法"
> 依赖：novel-expert-system（含72条路由表）、expert-writing-safety（质检层）
> 来源：MiMoClaw交叉引用矩阵 × Claude Code架构研究 × OpenClaw实践
> 更新：2026-04-02（新增Token节省规范 / 6大框架Skill联动 / 三级响应机制）

---

## 一、系统全貌（v2.0更新）

### 1.1 全部Skill索引（33个）

| # | Skill | 角色 | 优先级 |
|---|-------|------|--------|
| 1 | novel-expert-system | **主入口** | 唯一 |
| 2 | novel-writing-expert | 创作哲学（辅入口） | 高 |
| 3 | expert-fanqie-short | 番茄短篇 | P0 |
| 4 | expert-fanqie-novel | 番茄长篇 | P0 |
| 5 | expert-fanqie-female | 番茄女频 | P0 |
| 6 | expert-qidian | 起点通用 | P0 |
| 7 | expert-qidian-long | 起点长篇 | P0 |
| 8 | expert-acg-short | ACG短篇 | P1 |
| 9 | expert-acg-fanfic | ACG同人 | P1 |
| 10 | expert-xuanhuan | 东方玄幻 | P1 |
| 11 | expert-xihuan | 西幻 | P1 |
| 12 | expert-guoxue | 国学/仙侠 | P1 |
| 13 | expert-writing-safety | **质检（强制）** | 唯一 |
| 14 | expert-character | 人物塑造 | 辅 |
| 15 | expert-combat | 战斗场面 | 辅 |
| 16 | expert-dialogue | 对白写作 | 辅 |
| 17 | expert-emotion | 情感共鸣 | 辅 |
| 18 | expert-hook | 开篇钩子 | 辅 |
| 19 | expert-pacing | 叙事节奏 | 辅 |
| 20 | expert-plot-shuangdian | 爽点设计 | 辅 |
| 21 | expert-skill-system | 技能体系 | 辅 |
| 22b | expert-cosmology-physics | 世界观科学锚点 | 辅 |
| 22 | expert-weapons | 武器装备 | 辅 |
| 23 | expert-worldbuilding | 世界观 | 辅 |
| 24 | expert-memory | 全局记忆 | 辅 |
| 25 | expert-logic | 逻辑自洽 | 辅 |
| 26 | expert-title-outro | 标题结尾 | 辅 |
| 27 | expert-writing-style | 大神风格 | 辅 |
| 27b | expert-platform-metrics | 平台算法标准 | 引用 |
| 27c | expert-bookstatus | 项目状态管理 | 引用 |
| 27d | novel-volume-workflow | 卷级全流程编排 | 入口 |
| 27e | expert-revise-loop | 修正循环 | 辅 |
| 27f | expert-reader-tracker | 数据追踪 | 辅 |
| 27g | short-story-workflow | 短故事全流程 | 入口 |
| 27h | expert-sensory-prose | 五感描写专项 | 辅 |
| 27i | expert-suspense | 悬疑推理 | 辅 |
| 27j | expert-ensemble | 男频群像戏 | 辅 |
| 27k | expert-horror | 恐怖/怪谈 | 辅 |
| 27l | expert-rebirth | 重生穿越 | 辅 |
| 27m | expert-farming | 种田经营 | 辅 |
| 27n | expert-urban | 都市题材 | P1 |
| 27o | expert-sci-fi | 科幻题材 | P1 |
| 27p | expert-system-design | 系统流设计 | P1 |
| 27q | expert-fanfic-universal | 泛同人 | P1 |
| 27r | expert-jjwxc | 晋江平台 | P1 |
| 27s | expert-ip-adaptation | IP改编 | 辅 |
| 27t | expert-emotion-death | 悲情/死亡场景 | 辅 |
| 27u | expert-anti-ai-taste | 去AI味 | 辅 |
| 27v | expert-literary-prose | 文学质感锻造 | 辅 |
| 27w | expert-writing-style-western | 西方文风 | 辅 |
| 27x | expert-style-learner | 风格学习 | 辅 |
| 27y | expert-revision | 改稿自审 | 辅 |
| 27z | expert-footprint | 文风一致性 | 辅 |
| 27aa | expert-quality-gate | 质量门禁 | 辅 |
| 27ab | expert-serialization-ops | 连载运营 | 辅 |
| 27ac | expert-endurance | 写作体能 | 辅 |
| 27ad | expert-data-driven | 数据驱动 | 辅 |
| 27ae | expert-reader-psychology | 读者心理学 | 辅 |
| 27af | expert-quickstart | 新手指南 | 引用 |
| 27ag | expert-dependency-map | 依赖图谱 | 引用 |
| 27ah | novel-project-starter | 项目启动器 | 入口 |
| 27ai | novel-memory-3layer | 三层记忆管理 | 辅 |
| 27aj | novel-experience-db | 经验数据库 | 引用 |
| 27ak | novel-expert-system-agent-qc | 多Agent质控 | 辅 |
| 27al | novel-expert-system-crossover | 联动创作 | 辅 |
| 27am | novel-expert-system-techniques | 经典技法补全 | 辅 |
| 28 | session-compactor | **会话压缩** | 隔离 |
| 27h | expert-sensory-prose | 五感描写专项 | 辅 |
| 27i | expert-suspense | 悬疑推理 | 辅 |
| 27j | expert-ensemble | 男频群像戏 | 辅 |
| 27k | expert-horror | 恐怖/怪谈 | 辅 |
| 27l | expert-rebirth | 重生穿越 | 辅 |
| 27m | expert-farming | 种田经营 | 辅 |
| 27n | expert-urban | 都市题材 | P1 |
| 27o | expert-sci-fi | 科幻题材 | P1 |
| 27p | expert-system-design | 系统流设计 | P1 |
| 27q | expert-fanfic-universal | 泛同人 | P1 |
| 27r | expert-jjwxc | 晋江平台 | P1 |
| 27s | expert-ip-adaptation | IP改编 | 辅 |
| 27t | expert-emotion-death | 悲情/死亡场景 | 辅 |
| 27u | expert-anti-ai-taste | 去AI味 | 辅 |
| 27v | expert-literary-prose | 文学质感锻造 | 辅 |
| 27w | expert-writing-style-western | 西方文风 | 辅 |
| 27x | expert-style-learner | 风格学习 | 辅 |
| 27y | expert-revision | 改稿自审 | 辅 |
| 27z | expert-footprint | 文风一致性 | 辅 |
| 27aa | expert-quality-gate | 质量门禁 | 辅 |
| 27ab | expert-serialization-ops | 连载运营 | 辅 |
| 27ac | expert-endurance | 写作体能 | 辅 |
| 27ad | expert-data-driven | 数据驱动 | 辅 |
| 27ae | expert-reader-psychology | 读者心理学 | 辅 |
| 27af | expert-quickstart | 新手指南 | 引用 |
| 27ag | expert-dependency-map | 依赖图谱 | 引用 |
| 27ah | novel-project-starter | 项目启动器 | 入口 |
| 27ai | novel-memory-3layer | 三层记忆管理 | 辅 |
| 27aj | novel-experience-db | 经验数据库 | 引用 |
| 27ak | novel-expert-system-agent-qc | 多Agent质控 | 辅 |
| 27al | novel-expert-system-crossover | 联动创作 | 辅 |
| 27am | novel-expert-system-techniques | 经典技法补全 | 辅 |
| 29 | agent-engineering-guide | **12层架构** | 隔离 |
| 30 | claude-code-deep-dive | **源码研究** | 隔离 |
| 31 | model-optimization-mimo | MiMo优化 | 隔离 |
| 32 | model-optimization-gemini | Gemini优化 | 隔离 |

**角色分类：**
- **主入口**（1个）：novel-expert-system 唯一入口
- **平台专家**（6个）：#3-#7 + #9
- **质检专家**（1个）：#13（强制调用）
- **技能专家**（13个）：#14-#27
- **框架专家**（5个）：#28-#32（独立运行，不参与创作联动）

---

## 二、Token节省规范（v2.0新增）

> **核心原则：Skill不是加载，是检索。**

### 2.1 Skill分层加载规则（强制）

```
Layer 1（始终加载）：
  → novel-expert-system 的路由索引（附录七）
  → 仅含：Expert名字 + 1行功能描述 + 触发关键词
  → Token消耗：< 500字

Layer 2（按需加载）：
  → 路由命中后才加载对应Expert的完整SKILL.md
  → 加载后仅读取相关章节，不是全文
  → Token消耗：按需读取章节（< 3KB/次）

Layer 3（禁止全量加载）：
  ❌ 一次加载所有26个Expert全文
  ❌ 在system prompt里写入所有Skill内容
  ❌ 读取与当前任务无关的Expert
```

### 2.2 Skill描述规范（强制，v2.0新规）

| 标准 | 旧版 | v2.0规范 |
|------|------|---------|
| description字段 | 150-200字 | **≤100字** |
| 触发关键词 | 模糊 | **精准，3-5个** |
| 禁止 | 无限制 | 禁止写操作步骤，只写功能 |

**描述精简示例：**

```
❌ expert-combat旧版（186字）：
"战斗场面设计专家。专门负责设计精彩、紧张、有画面感的战斗场景。
适用场景：设计一场精彩的打斗、设计越阶战斗、设计战斗中的反转、
设计战斗中的技能组合......"

✅ expert-combat v2.0（73字）：
"战斗场面设计专家。提供：攻守转换节奏/五感描写词库/越阶战斗三
公式/群战三原则/战斗代价五类型。配合expert-weapons使用。"
```

### 2.3 单任务Token预算

```
简单任务（单Expert）：
  主入口路由：< 1k tokens
  Expert读取：< 3k tokens
  输出：< 5k tokens
  合计：< 10k tokens ✅

中等任务（主+1辅）：
  主入口路由：< 1k tokens
  主Expert：< 5k tokens
  辅Expert（1个）：< 3k tokens
  整合输出：< 8k tokens
  合计：< 18k tokens ✅

复杂任务（主+2辅+质检）：
  主入口路由：< 1k tokens
  主Expert：< 8k tokens
  辅Expert（2个）：< 6k tokens
  质检：< 3k tokens
  整合输出：< 10k tokens
  合计：< 30k tokens ⚠️（需监控）
```

**超标处理：**
```
> 20k tokens/单任务 → 启用session-compactor
> 50k tokens/累积 → 强制压缩
> 100k tokens/累积 → 停止接单，写快照，恢复后继续
```

---

## 三、联动触发规则（v2.0强化）

### 3.1 路由查询顺序（强制）

```
Step 1：精确匹配（novel-expert-system 附录七）
        → 用户query中有明确的平台/题材关键词
        → 直接激活对应Expert，跳过Step 2-3

Step 2：模糊匹配（题材→技能联动矩阵）
        → 无精确关键词，但有题材语境
        → 题材Expert + 技能Expert联动

Step 3：单Expert兜底
        → novel-expert-system 直接处理

Step 4：创作输出 → expert-writing-safety 强制质检
```

### 3.2 三级响应机制（v2.0新增）

```
A级响应（< 5k tokens，< 30秒）：
  → 单Expert直接响应
  → 无需路由表查询
  → 触发：简单问题/单章修改/单一技能咨询

B级响应（5-20k tokens，5-15分钟）：
  → 主+1辅协同
  → 主Expert调度，辅Expert输出
  → 触发：标准创作任务

C级响应（> 20k tokens，> 15分钟）：
  → 主+2辅+质检
  → 需制定执行计划
  → 触发：长篇章节/多平台联动/大纲设计
  → 必须先输出计划，用户确认后再执行
```

### 3.3 同时活跃Expert上限（强化）

```
A級任务：1个Expert ✅
B级任务：2个Expert（主+辅）✅
C级任务：3个Expert（主+辅+辅）⚠️上限
❌ 禁止：4个及以上Expert同时活跃
```

---

## 四、主辅协同标准流程

### 4.1 B级任务标准流程

```
用户需求
  ↓
novel-expert-system 路由判定（B级）
  ↓
主Expert生成"辅Expert调用指令"（格式见4.2）
  ↓
辅Expert一次性完整输出（不解释、不重复）
  ↓
主Expert整合（引用所有辅Expert成果）
  ↓
expert-writing-safety 强制质检
  ↓
输出给用户
  ↓
session-compactor 评估（>20k则压缩）
```

### 4.2 辅Expert调用指令格式（强制）

```
## 辅Expert调用

**目标：** [Expert名称]
**任务：** [≤50字的任务描述]
**上下文：** [角色名/已确定设定/已发生事件，≤100字]
**输出要求：** [具体输出内容，≤200字]
**字数：** [X~X字]
**禁止：** [敏感内容/已确定的设定]

---
[Expert名称] 输出完毕。
```

### 4.3 C级任务计划确认流程（v2.0新增）

```
Step 1：主Expert输出计划（不经用户确认不执行）
  - 涉及哪些Expert？
  - 执行顺序？
  - 预计Token消耗？
  - 有哪些风险点？

Step 2：用户确认（或修改计划）

Step 3：按计划执行

Step 4：expert-writing-safety质检

Step 5：结果交付 + session-compactor评估
```

---

## 五、Expert分类调用规则

### 5.1 平台专家联动表

| 用户意图 | 主Expert | 必选辅Expert | 可选辅Expert | 质检 |
|---------|---------|------------|------------|------|
| 番茄短篇（1.5-3万字） | expert-fanqie-short | expert-hook | expert-plot-shuangdian | ✅ |
| 番茄长篇（20万字+） | expert-fanqie-novel | expert-pacing, expert-memory | expert-logic | ✅ |
| 番茄女频 | expert-fanqie-female | expert-emotion | expert-character | ✅ |
| 起点通用 | expert-qidian | expert-guoxue | expert-logic | ✅ |
| 起点长篇 | expert-qidian-long | expert-guoxue, expert-logic | expert-memory | ✅ |
| ACG短篇 | expert-acg-short | expert-character | expert-plot-shuangdian | ✅ |
| ACG同人（长篇） | expert-acg-fanfic | expert-character | expert-combat | ✅ |

### 5.2 题材专家联动表

| 题材 | 主Expert | 必选辅Expert | 说明 |
|------|---------|------------|------|
| 东方玄幻/仙侠 | expert-xuanhuan | expert-guoxue, expert-skill-system | 修炼体系+五行设定 |
| 西幻/RPG | expert-xihuan | expert-weapons, expert-worldbuilding | 种族+魔法+政治 |
| 国学/历史 | expert-guoxue | expert-worldbuilding | 周易八卦+中医+神话 |
| 战斗升级流 | expert-combat | expert-skill-system, expert-weapons | 攻守节奏+技能树 |
| 世界观物理锚定 | expert-cosmology-physics | expert-worldbuilding, expert-skill-system | 能量守恒+地理生态+防气体人 |
| 情感/甜宠 | expert-emotion | expert-dialogue | 五感写作+情感锚点 |
| 大神风格模仿 | expert-writing-style | expert-pacing | 扩充字数+爽点密度 |

### 5.3 技能专家独立使用规则

以下Expert可被用户**直接调用**，无需经过主Expert：

| Expert | 触发条件 | 调用方式 |
|--------|---------|---------|
| expert-hook | 用户问"开头怎么写"/"标题" | 直接读取SKILL.md |
| expert-logic | 用户问"逻辑问题"/"战力崩坏" | 直接读取SKILL.md |
| expert-title-outro | 用户问"章节标题" | 直接读取SKILL.md |
| expert-memory | 用户问"之前设定是什么" | 直接读MEMORY.md |

---

## 六、禁止行为清单（v2.0扩充）

| 禁止 | 正确做法 | 违规后果 |
|------|---------|---------|
| 多个Expert同时输出 | 主Expert统一整合 | 内容打架 |
| 辅Expert直接输出给用户 | 全部经过主Expert中转 | 碎片化 |
| 加载与任务无关的Expert | 只加载路由命中的Expert | Token浪费 |
| Skill全文加载到system prompt | 只读取相关章节 | Token爆炸 |
| 同一Expert响应超过2次/任务 | 一次性完整输出 | 上下文膨胀 |
| 跳过expert-writing-safety | 所有创作输出必须质检 | 合规风险 |
| 超过30k tokens不触发压缩 | >20k开始警告，>30k强制压缩 | OOM风险 |

---

---

## 📚 References（按需加载）

| 文件 | 内容 | 什么时候读 |
|------|------|-----------|
| references/expert-catalog.md | 全部Skill索引+分类+调用规则表 | 查找具体Expert时 |
| references/context-management.md | Session上下文管理+Token警戒线+快照规则 | 管理长session时 |
| references/classic-techniques.md | 协作触发矩阵+冲突解决+上下文传递模板 | 深度协作问题时 |
