---
name: expert-dependency-map
description: Skill依赖图谱与学习路径。Use when 用户问"哪个skill先学""学习路径怎么走""skill之间什么关系""推荐哪些skill"、需要查找具体skill的依赖关系或联动推荐时触发。
  - onboarding
  - meta
  - 番茄小说
  - 起点中文网
  - 晋江文学城
---

# Skill依赖图谱与学习路径（expert-dependency-map）

## 目录

- [第一章 体系概览](#第一章-体系概览)
- [第二章 全局依赖关系图谱](#第二章-全局依赖关系图谱)
- [第三章 功能分类详解](#第三章-功能分类详解)
- [第四章 三阶段学习路径](#第四章-三阶段学习路径)
- [第五章 前置依赖与联动推荐](#第五章-前置依赖与联动推荐)
- [第六章 题材×平台组合推荐](#第六章-题材平台组合推荐)
- [第七章 场景触发指南](#第七章-场景触发指南)
- [第八章 快速查找索引](#第八章-快速查找索引)
- [第九章 经典技法补全与自检清单](#第九章-经典技法补全与自检清单)

---

## 第一章 体系概览

### 1.1 本文件的定位

本文件是整个novel skill体系的**说明书和导航图**。它回答三个核心问题：

1. **有哪些skill可用？** → 全局图谱
2. **应该按什么顺序学？** → 学习路径
3. **我现在需要哪个skill？** → 场景触发索引

**推荐阅读顺序：** expert-quickstart → 本文件（expert-dependency-map）→ 按需深入各skill

### 1.2 Skill体系总览

整个novel skill体系包含44个skill，分为五大类：

| 分类 | 数量 | 核心价值 |
|------|------|---------|
| 技法类 | 15个 | 提升写作技术 |
| 题材类 | 10个 | 适配特定题材 |
| 平台类 | 7个 | 适配发布平台 |
| 运营类 | 6个 | 连载运营策略 |
| 工具类 | 5个 | 辅助工具链 |

### 1.3 依赖关系的三种类型

- **前置依赖（Prerequisite）：** 学A之前必须先学B，否则A的内容你理解不了
- **联动推荐（Companion）：** 学A的时候建议同步参考B，能互相补充
- **进阶路径（Progression）：** 学完A之后推荐学B，形成递进关系

---

## 第二章 全局依赖关系图谱

### 2.1 技法类Skill图谱（15个）

```
novel-writing-expert (总入口)
  ├── expert-hook (开篇钩子)
  │     └── expert-title-outro (标题与结尾)
  ├── expert-pacing (叙事节奏)
  │     ├── expert-plot-shuangdian (爽点设计)
  │     └── expert-suspense (悬疑推理)
  ├── expert-dialogue (对白写作)
  │     └── expert-character (人物塑造)
  ├── expert-emotion (情感共鸣)
  │     ├── expert-emotion-death (发刀子/悲情)
  │     └── expert-revision (改稿自审)
  ├── expert-combat (战斗场面)
  │     └── expert-weapons (武器装备)
  ├── expert-logic (逻辑自洽)
  │     └── expert-memory (全局记忆)
  ├── expert-worldbuilding (世界观架构)
  │     ├── expert-skill-system (技能体系)
  │     └── expert-guoxue (国学文化)
  ├── expert-footprint (创作足迹)
  ├── expert-quality-gate (质量门禁)
  └── expert-revision (改稿自审)
        └── expert-anti-ai-taste (去AI味)
```

**核心依赖链：**
- `novel-writing-expert` → 所有技法skill的总入口，必须先读
- `expert-pacing` 是节奏控制的基础 → `expert-plot-shuangdian`和`suspense`依赖它
- `expert-character` 是人物塑造的基础 → `expert-dialogue`和`expert-emotion`依赖它
- `expert-logic` + `expert-memory` 是自洽性的保障 → 长篇创作必须掌握

### 2.2 题材类Skill图谱（10个）

```
题材选择
  ├── 东方玄幻 → expert-xuanhuan
  │     └── + expert-skill-system + expert-combat
  ├── 西方奇幻 → expert-xihuan
  │     └── + expert-worldbuilding + expert-writing-style-western
  ├── 都市题材 → expert-urban
  │     └── + expert-dialogue + expert-emotion
  ├── 科幻题材 → expert-sci-fi
  │     └── + expert-worldbuilding + expert-logic
  ├── 悬疑推理 → expert-suspense
  │     └── + expert-logic + expert-pacing
  ├── 重生穿越 → expert-rebirth
  │     └── + expert-plot-shuangdian + expert-hook
  ├── 系统流 → expert-system-design
  │     └── + expert-skill-system + expert-xuanhuan
  ├── 种田经营 → expert-farming
  │     └── + expert-pacing + expert-worldbuilding
  ├── 同人创作 → expert-fanfic-universal / expert-acg-fanfic
  │     └── + expert-character (OOC防控)
  └── 女频创作 → expert-fanqie-female
        └── + expert-emotion + expert-hook
```

### 2.3 平台类Skill图谱（7个）

```
平台适配
  ├── 番茄小说
  │     ├── expert-fanqie-novel (长篇)
  │     ├── expert-fanqie-short (短篇)
  │     └── expert-platform-metrics (算法规则)
  │     └── expert-bookstatus (项目状态)
  ├── 起点中文网
  │     ├── expert-qidian (平台规则)
  │     ├── expert-qidian-long (长篇爆款)
  │     └── expert-platform-metrics
  └── 晋江文学城
        ├── expert-jjwxc (平台规则)
        └── expert-platform-metrics
```

### 2.4 运营类Skill图谱（6个）

```
运营体系
  ├── expert-serialization-ops (连载运营)
  │     ├── expert-title-outro (标题断章)
  │     └── expert-hook (开篇钩子)
  ├── expert-collaboration-protocol (多Expert协同)
  ├── expert-memory (全局记忆管理)
  ├── expert-footprint (文风一致性)
  ├── expert-endurance (写作体能)
  └── expert-anti-ai-taste (去AI味)
```

### 2.5 工具类Skill图谱（5个）

```
工具链
  ├── expert-quickstart (新手快速上手)
  ├── expert-dependency-map (本文件/导航图)
  ├── expert-writing-style (大神文风研究)
  ├── expert-writing-style-western (西方文风)
  └── expert-ip-adaptation (IP改编)
```

---

## 第三章 功能分类详解

### 3.1 技法类（15个）——提升写作技术

| Skill | 核心功能 | 适用阶段 | 难度 |
|-------|---------|---------|------|
| novel-writing-expert | 总入口/全链路指导 | 全程 | ★☆☆ |
| expert-hook | 开篇300字抓人 | 初稿 | ★★★ |
| expert-pacing | 节奏控制/张力曲线 | 初稿+改稿 | ★★★ |
| expert-dialogue | 自然有个性的对白 | 初稿 | ★★☆ |
| expert-character | 人物塑造/OOC防控 | 大纲+初稿 | ★★★ |
| expert-emotion | 情感共鸣/哭点笑点 | 初稿 | ★★★ |
| expert-emotion-death | 悲情/死亡场景 | 初稿 | ★★★★ |
| expert-combat | 战斗场面设计 | 初稿 | ★★★ |
| expert-sensory-prose | 五感描写专项（视觉/听觉/嗅觉/味觉/触感链/织袜） | 大纲+初稿 | ★★★ |
| expert-weapons | 武器装备设计 | 设定阶段 | ★★☆ |
| expert-plot-shuangdian | 打脸/逆袭爽点 | 大纲+初稿 | ★★★ |
| expert-logic | 逻辑自洽审查 | 改稿 | ★★☆ |
| expert-worldbuilding | 世界观架构 | 设定阶段 | ★★★★ |
| expert-skill-system | 技能体系设计 | 设定阶段 | ★★★ |
| expert-cosmology-physics | 世界观科学锚点（防气体人） | 设定阶段（①②③） | ★★★ |
| expert-guoxue | 国学文化融入 | 设定+初稿 | ★★★ |
| expert-revision | 改稿五层递进法 | 改稿 | ★★★ |
| expert-footprint | 文风一致性追踪 | 连载中 | ★★☆ |
| expert-quality-gate | 写入后质量门禁验证 | 成稿阶段 | ★★★ |
| expert-anti-ai-taste | 去除AI痕迹 | 改稿 | ★★☆ |
| expert-title-outro | 标题/结尾设计 | 初稿+改稿 | ★★☆ |
| expert-suspense | 悬疑推理技法 | 大纲+初稿 | ★★★★ |

### 3.2 题材类（10个）——适配特定类型

| Skill | 题材 | 核心价值 |
|-------|------|---------|
| expert-xuanhuan | 东方玄幻 | 修炼体系/宗门势力/升级路线 |
| expert-xihuan | 西方奇幻 | 种族/魔法/史诗战争 |
| expert-urban | 都市题材 | 异能体系/蝴蝶效应/言情模板 |
| expert-sci-fi | 科幻 | 科技树/世界观框架/赛博朋克 |
| expert-suspense | 悬疑推理 | 诡计设计/悬念构建 |
| expert-rebirth | 重生穿越 | 蝴蝶效应/先知优势 |
| expert-system-design | 系统流 | 系统设计/任务架构 |
| expert-farming | 种田经营 | 慢热节奏/经营逻辑 |
| expert-fanfic-universal | 泛同人 | OOC防控/AU设计 |
| expert-acg-fanfic | ACG同人 | 原著还原/跨媒介改编 |

### 3.3 平台类（7个）——适配发布渠道

| Skill | 平台 | 关注点 |
|-------|------|--------|
| expert-fanqie-novel | 番茄长篇 | 推荐算法/签约策略/百万字连载 |
| expert-fanqie-short | 番茄短篇 | 1.5-3万字/付费节点/听读适配 |
| expert-fanqie-female | 番茄女频 | 追妻火葬场/真假千金/年代重生 |
| expert-qidian | 起点通用 | 平台规则/追读率/本章说 |
| expert-qidian-long | 起点长篇 | PK机制/仙侠/历史/西幻 |
| expert-jjwxc | 晋江 | 积分/收藏/榜单机制 |
| expert-platform-metrics | 通用 | 2026年算法指标/达标门槛 |
| expert-bookstatus | 项目状态管理 | 章节索引+进度追踪+文件关联 |
| novel-volume-workflow | 卷级全流程编排 | 一键推进全链路 |
| expert-revise-loop | 修正循环 | 3轮迭代+剧情推进校验 |
| expert-reader-tracker | 数据追踪 | 预警阈值+章节级关联诊断 |
| short-story-workflow | 短故事全流程 | 15章流水线+质检链 |

### 3.4 运营类（6个）——连载运营策略

| Skill | 功能 | 何时用 |
|-------|------|--------|
| expert-serialization-ops | 连载运营总指南 | 上架/冲榜/请假 |
| expert-collaboration-protocol | 多Expert协同调度 | 复杂创作任务 |
| expert-memory | 全局记忆管理 | 长篇50章以上 |
| expert-footprint | 文风一致性 | 连载30章以上 |
| expert-quality-gate | 写入验证 | 每次章节写入后 |
| expert-endurance | 写作体能管理 | 日更阶段 |
| expert-anti-ai-taste | 去AI味 | AI辅助写作后 |

### 3.5 工具类（5个）——辅助工具链

| Skill | 功能 | 何时用 |
|-------|------|--------|
| expert-quickstart | 新手快速上手 | 第一次使用 |
| novel-project-starter | 小说项目一键启动 | 用户说"想写小说"时自动触发 |
| novel-memory-3layer | 三层记忆管理架构（短期/中期/长期） | 连载中 | ★★☆ |
| novel-experience-db | 创作经验数据库（技法积累/案例检索） | 全程 | ★☆☆ |
| novel-expert-system | 全流程调度中枢 | 启动任何创作项目时（必调用） |
| novel-expert-system-techniques | 经典技法补全 | 选题评估/素材积累/防崩指南（novel-expert-system子模块） |
| novel-expert-system-agent-qc | 多Agent质控 | 批量写作质检/评审/润色（novel-expert-system子模块） |
| novel-expert-system-crossover | 联动创作规范 | 影视/动漫/游戏联动专项（novel-expert-system子模块） |
| skill-deployment-protocol | Skill部署集成规范 | 安装/批量导入/升级/删除skill后（强制） |
| expert-dependency-map | 导航图/说明书 | 找不到用哪个skill时 |
| expert-writing-style | 男频大神文风 | 想模仿大神风格 |
| expert-style-learner | 个性化风格学习 | 用过多次生成/用户有修改习惯后 |
| expert-writing-style-western | 西方经典文风 | 西幻/文学向创作 |
| expert-literary-prose | 文学质感锻造 | 江南文青/译本质感/意象氛围/出版向 |
| expert-acg-short | ACG短故事 | 番茄短故事/5000-3万字/ACG同人短篇 |
| expert-data-driven | 数据驱动创作 | 追读率/完读率/收藏转化/A/B测试 |
| expert-ensemble | 男频群像戏 | POV群像/小队群像/势力群像/战争群像 |
| expert-horror | 恐怖/怪谈 | 规则怪谈/无限流恐怖/民俗恐怖/克苏鲁 |
| expert-reader-psychology | 读者心理学 | 成瘾机制/弃读心理/平台读者画像 |
| expert-writing-safety | 避坑自检 | 格式合规/算法适配/内容质量终检 |
| expert-ip-adaptation | IP改编 | 小说→剧本/动漫 |

---

## 第四章 三阶段学习路径

### 4.1 新手路径（10个核心skill，2周速成）

**目标：** 掌握网文写作的基础技术，能写出合格的商业网文。

**第1天-第2天：基础认知**
1. **expert-quickstart** — 快速了解整个体系（30分钟）
2. **expert-dependency-map** — 本文件，了解全局（30分钟）
3. **novel-writing-expert** — 小说创作总指南（2小时）

**第3天-第4天：开篇技术**
4. **expert-hook** — 开篇钩子设计（1小时）
5. **expert-pacing** — 叙事节奏基础（1小时）

**第5天-第6天：核心技法**
6. **expert-dialogue** — 对白写作（1小时）
7. **expert-character** — 人物塑造（1小时）

**第7天-第8天：平台适配**
8. **expert-platform-metrics** — 平台算法规则（1小时）
9. 根据目标平台选一个：expert-fanqie-novel 或 expert-qidian（1小时）

**第9天-第10天：实战+改稿**
10. **expert-revision** — 改稿方法论（1小时）

**第11天-第14天：实战练习**
- 写一个5000字短篇
- 用expert-revision的方法改一遍
- 发布到目标平台

### 4.2 进阶路径（按题材选配，1-2月）

**前提：** 已完成新手路径

**核心进阶模块（所有人必学）：**
- expert-plot-shuangdian — 爽点设计（2小时）
- expert-emotion — 情感共鸣（2小时）
- expert-logic — 逻辑自洽（1小时）
- expert-memory — 全局记忆管理（1小时）

**按题材选配模块（选一个方向深入）：**

**玄幻方向（3-4周）：**
- expert-xuanhuan → expert-skill-system → expert-combat → expert-weapons
- 联动参考：expert-worldbuilding, expert-guoxue

**都市方向（3-4周）：**
- expert-urban → expert-dialogue（深入） → expert-emotion（深入）
- 联动参考：expert-rebirth（如果写都市重生）

**科幻方向（3-4周）：**
- expert-sci-fi → expert-worldbuilding → expert-logic（深入）
- 联动参考：expert-writing-style-western

**悬疑方向（3-4周）：**
- expert-suspense → expert-pacing（深入） → expert-logic（深入）
- 联动参考：expert-hook

**女频方向（3-4周）：**
- expert-fanqie-female → expert-emotion（深入） → expert-title-outro
- 联动参考：expert-rebirth

### 4.3 高手路径（全体系打通，持续）

**前提：** 已完成进阶路径，有至少一部30万字以上的完本作品

**第一阶段：深化技术（1-2月）**
- expert-emotion-death — 悲情场景专精
- expert-writing-style — 大神文风研究
- expert-literary-prose — 文学质感锻造（江南文青/译本质感/意象系统）
- expert-style-learner — 个性化风格学习（从修改中提取偏好，越用越像自己）
- expert-footprint — 文风一致性管理
- expert-suspense — 悬疑技法（跨题材运用）

**第二阶段：运营能力（持续）**
- expert-serialization-ops — 连载运营
- expert-title-outro — 标题断章优化
- expert-endurance — 写作体能管理
- 对应平台的深度skill

**第三阶段：体系化（持续）**
- expert-collaboration-protocol — 多Expert协同
- expert-ip-adaptation — IP改编
- expert-writing-style-western — 跨文化写作
- expert-literary-prose + writing-style-western — 西幻文学质感体系化
- 自定义skill组合和工作流

---

## 第五章 前置依赖与联动推荐

### 5.1 完整前置依赖表

| Skill | 必须先学（前置） | 建议同步（联动） |
|-------|----------------|----------------|
| novel-writing-expert | 无 | expert-quickstart |
| expert-quickstart | 无 | expert-dependency-map |
| novel-project-starter | 无 | expert-quickstart, novel-expert-system |
| expert-hook | novel-writing-expert | expert-pacing |
| expert-pacing | novel-writing-expert | expert-hook, expert-plot-shuangdian |
| expert-dialogue | novel-writing-expert | expert-character |
| expert-character | novel-writing-expert | expert-dialogue, expert-emotion |
| expert-emotion | expert-character | expert-dialogue, expert-emotion-death |
| expert-emotion-death | expert-emotion | expert-pacing, expert-dialogue |
| expert-combat | expert-pacing | expert-weapons, expert-xuanhuan |
| expert-weapons | expert-worldbuilding | expert-combat, expert-skill-system |
| expert-plot-shuangdian | expert-pacing | expert-hook, expert-combat |
| expert-logic | novel-writing-expert | expert-memory, expert-worldbuilding |
| expert-worldbuilding | novel-writing-expert | expert-logic, expert-skill-system |
| expert-skill-system | expert-worldbuilding | expert-combat, expert-weapons |
| expert-guoxue | expert-worldbuilding | expert-xuanhuan, expert-xihuan |
| expert-revision | novel-writing-expert | expert-logic, expert-memory |
| expert-footprint | expert-revision | expert-memory |
| expert-anti-ai-taste | expert-revision | expert-writing-style |
| expert-style-learner | expert-writing-style | expert-revision, expert-anti-ai-taste |
| expert-title-outro | expert-hook | expert-pacing, expert-serialization-ops |
| expert-suspense | expert-pacing, expert-logic | expert-hook, expert-emotion |
| expert-xuanhuan | expert-worldbuilding | expert-skill-system, expert-combat |
| expert-xihuan | expert-worldbuilding | expert-guoxue, expert-writing-style-western |
| expert-urban | expert-character | expert-dialogue, expert-emotion |
| expert-sci-fi | expert-worldbuilding | expert-logic, expert-writing-style-western |
| expert-rebirth | expert-hook | expert-plot-shuangdian, expert-urban |
| expert-system-design | expert-skill-system | expert-xuanhuan, expert-plot-shuangdian |
| expert-farming | expert-pacing | expert-worldbuilding, expert-urban |
| expert-fanfic-universal | expert-character | expert-emotion, expert-worldbuilding |
| expert-acg-fanfic | expert-fanfic-universal | expert-character, expert-emotion |
| expert-fanqie-female | expert-emotion | expert-hook, expert-title-outro |
| expert-fanqie-novel | expert-platform-metrics | expert-pacing, expert-hook |
| expert-fanqie-short | expert-fanqie-novel | expert-hook, expert-title-outro |
| expert-qidian | expert-platform-metrics | expert-pacing, expert-hook |
| expert-qidian-long | expert-qidian | expert-serialization-ops, expert-memory |
| expert-jjwxc | expert-platform-metrics | expert-emotion, expert-character |
| expert-serialization-ops | novel-writing-expert | expert-title-outro, expert-endurance |
| expert-memory | novel-writing-expert | expert-logic, expert-footprint |
| expert-endurance | novel-writing-expert | expert-serialization-ops |
| expert-collaboration-protocol | novel-writing-expert | expert-memory |
| expert-writing-style | novel-writing-expert | expert-pacing, expert-dialogue |
| expert-sensory-prose | expert-character | expert-emotion, expert-combat |
| novel-memory-3layer | expert-memory | expert-footprint, expert-revision |
| novel-experience-db | expert-revision | expert-anti-ai-taste, expert-data-driven |
| expert-writing-style-western | expert-writing-style | expert-xihuan, expert-sci-fi |
| expert-ip-adaptation | novel-writing-expert | expert-character, expert-worldbuilding |

### 5.2 强依赖 vs 弱依赖

**强依赖（不学A就无法理解B的核心内容）：**
- expert-character → expert-dialogue（不懂人物塑造就写不好个性化对白）
- expert-pacing → expert-plot-shuangdian（不懂节奏就设计不好爽点分布）
- expert-emotion → expert-emotion-death（不懂基本情感共鸣就写不好悲情）
- expert-worldbuilding → expert-skill-system（不懂世界观就设计不好技能体系）

**弱依赖（学A有助于理解B，但不是必须）：**
- expert-hook → expert-title-outro（开篇和结尾有共通技术，但可以独立学习）
- expert-logic → expert-suspense（逻辑能力有助于悬疑，但悬疑有自己的逻辑体系）
- expert-pacing → expert-combat（节奏感有助于战斗场面，但战斗有自己的节奏规则）

---

---

## 📚 References（按需加载）

| 文件 | 内容 | 什么时候读 |
|------|------|-----------|
| references/genre-platform-combos.md | 题材×平台组合+场景触发+快速查找+自检清单 | 选题材+平台或需要组合推荐时 |
