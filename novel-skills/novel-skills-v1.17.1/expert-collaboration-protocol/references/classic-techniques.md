# classic-techniques（详细参考）

> 本文件为 expert-collaboration-protocol 的详细参考内容。

## 协同调度经典补全

### 多Expert调度的核心原则

```
① 主Expert负责框架 → 其他Expert填充内容
② 调度顺序决定质量 → 先题材后技能先质检
③ 不允许Expert之间矛盾 → 协议层强制一致性
④ 每个Expert有明确边界 → 不越权不推诿
```

### 异常处理标准流程

```
Expert返回错误 → 主入口记录错误 → 尝试下一个Expert → 3次失败→通知用户
```


---

## 经典技法补全

> 本章节补充可直接套用的经典技法模板，供创作者在实际写作中参考。

### 10.1 协作触发矩阵

多Expert协作的核心问题不是"怎么协作"，而是"什么时候触发哪个Expert"。协作触发矩阵为不同写作场景预定义最优的Expert调用组合。

```
触发矩阵模板：

场景类型          主Expert          协作Expert         调用顺序
开篇设计          expert-hook       expert-character   hook→character→pacing
战斗场景          expert-combat     expert-weapons     combat→weapons→pacing
情感高潮          expert-emotion    expert-dialogue    emotion→dialogue→pacing
世界观展开        expert-worldbuilding expert-logic       worldbuilding→logic→memory
升级突破          novel-expert-system expert-plot-shuangdian novel-system→plot-shuangdian→combat
悬疑推理          expert-suspense   expert-footprint   suspense→footprint→memory
日常/种田         expert-farming    expert-character   farming→character→pacing

触发规则：
① 每个场景最多同时调用3个Expert（超过会导致上下文冲突）
② 主Expert输出框架，协作Expert在框架内填充
③ 如果协作Expert的输出与主Expert冲突 → 以主Expert为准
④ 如果两个Expert的建议不兼容 → 启动冲突解决协议
```

### 10.2 冲突解决协议

当多个Expert的建议产生矛盾时，需要一套标准化的解决流程，避免陷入无限争论。

```
三级冲突解决机制：

第一级：规则仲裁（自动解决）
  → 有明确优先级规则的冲突
  → 规则：安全规范 > 平台规范 > 用户要求 > Expert建议
  → 例：expert-plot-shuangdian建议"主角碾压所有人"，但expert-logic指出"战力体系不允许"→ 以逻辑为准

第二级：上下文协商（需要更多上下文）
  → 冲突原因是因为各Expert看到的上下文不同
  → 解决方案：将冲突双方的完整上下文合并后重新判断
  → 例：expert-character建议"角色此时应该暴怒"，但expert-pacing建议"此处应该冷静"
  → 合并上下文后发现：这是角色性格弧线的"克制阶段"→ 应该"外表冷静但内心暴怒"

第三级：用户裁决（需要人工判断）
  → Expert之间无法达成一致的创意性冲突
  → 将双方的观点和理由整理后提交用户决定
  → 例：两个Expert对"结局是HE还是BE"有分歧 → 提交用户

冲突记录模板：
  冲突ID：[自增编号]
  冲突方：[ExpertA] vs [ExpertB]
  冲突内容：[一句话描述]
  解决方式：[仲裁/协商/用户裁决]
  解决结果：[采纳了谁的建议]
  → 每次冲突解决后记录，形成"冲突案例库"
```

### 10.3 上下文传递模板

Expert之间的信息传递是协作质量的关键。传递的信息太少，后续Expert无法做出正确判断；传递的信息太多，会造成上下文混乱。

```
上下文传递规范：

传递包结构：
{
  "scene_id": "场景编号",
  "primary_expert": "主Expert名称",
  "context_summary": "不超过200字的场景摘要",
  "character_states": [
    {"name": "角色名", "emotion": "当前情绪", "goal": "当前目标"}
  ],
  "world_state": "当前世界观的关键状态（50字内）",
  "constraints": ["约束1", "约束2"],
  "previous_outputs": ["前一个Expert的输出摘要"]
}

传递规则：
① 场景摘要必须包含：谁、在哪里、做什么、为什么
  → "林默在宗门大殿中向掌门汇报秘境探索结果，目的是获得进入内门的资格"

② 角色状态必须包含：情绪和目标
  → 情绪：当前的情感状态（愤怒/平静/兴奋/困惑）
  → 目标：角色在这个场景中想要达成什么

③ 约束条件必须明确列出
  → 例：["此场景不能出现暴力", "角色A不能暴露身份", "时间限制为1时辰内"]

④ 传递包总大小控制在500字以内
  → 太多信息会让后续Expert的上下文被淹没
  → 只传递"对后续决策有影响"的关键信息

禁忌：
  ❌ 传递完整的上一章内容（上下文爆炸）
  ❌ 只传递"写一个战斗场景"这样的模糊指令（信息不足）
  ❌ 传递不相关的角色信息（浪费上下文窗口）
  ❌ Expert之间互相引用对方的完整输出（重复传递）
```

### 10.4 自检清单

- [ ] 是否为当前写作场景选择了正确的主Expert？
- [ ] 协作Expert是否≤3个？
- [ ] 调用顺序是否符合触发矩阵的推荐？
- [ ] 如有Expert冲突，是否启动了冲突解决协议？
- [ ] 上下文传递包是否包含完整的场景摘要？
- [ ] 角色状态是否包含"情绪"和"目标"两个维度？
- [ ] 约束条件是否被明确列出和传递？
- [ ] 传递包总大小是否控制在500字以内？

### literary-prose 联动规则

- 触发条件：用户要求「文学质感」「文青风格」「译本质感」「像江南那样写」「出版向」
- 联动顺序：anti-ai-taste（去AI味）→ literary-prose（注入文学味）→ revision（审稿）
- 西幻联动：xihuan + literary-prose + writing-style-western（三位一体）
- 古风联动：xuanhuan + literary-prose + guoxue（意境优先）
- 浓度控制：由literary-prose根据题材自动选择文学浓度（第六章·题材×文学浓度搭配建议）

### 全量Expert协同规则（v3.3补全）

**【新增题材Expert联动】**
- expert-horror：恐怖/怪谈主Expert → 联动 suspense + pacing + hook + writing-safety
- expert-ensemble：男频群像主Expert → 联动 character + dialogue + combat + pacing + writing-safety
- expert-sci-fi：科幻题材主Expert → 联动 worldbuilding + logic + writing-style-western + writing-safety
- expert-farming：种田经营主Expert → 联动 worldbuilding + pacing + logic + writing-safety
- expert-rebirth：重生穿越主Expert → 联动 plot-shuangdian + pacing + character + logic + writing-safety
- expert-urban：都市题材主Expert → 联动 character + emotion + dialogue + logic + writing-safety
- expert-suspense：悬疑推理主Expert → 联动 logic + hook + pacing + writing-safety
- expert-system-design：系统流主Expert → 联动 plot-shuangdian + hook + pacing + writing-safety
- expert-acg-fanfic：ACG同人主Expert → 联动 character + plot-shuangdian + writing-safety
- expert-acg-short：ACG短故事主Expert → 联动 hook + emotion + title-outro + writing-safety
- expert-fanfic-universal：泛同人主Expert → 联动 character + worldbuilding + logic + writing-safety
- expert-fanqie-novel：番茄长篇主Expert → 联动 plot-shuangdian + pacing + hook + writing-safety

**【新增技能Expert联动】**
- expert-data-driven：数据复盘时调用 → 联动 reader-psychology + serialization-ops + 对应平台Expert
- expert-reader-psychology：分析读者行为时调用 → 联动 data-driven + emotion + hook
- expert-emotion-death：悲情场景专用 → 联动 emotion + pacing + dialogue（禁止单独使用）
- expert-endurance：日更倦怠/心态管理时调用 → 联动 serialization-ops
- expert-quickstart：新手入门首选 → 联动 dependency-map + writing-safety
- expert-revision：完稿后改稿阶段 → 联动 logic + writing-safety + anti-ai-taste
- expert-quality-gate：每次章节写入后 → 联动 logic + footprint + revision（Post-Write验证→问题定位→记录→如需改稿）
- expert-dependency-map：找不到skill时 → 联动 quickstart（新手）或 collaboration-protocol（进阶）
- expert-jjwxc：晋江平台专项 → 联动 character + emotion + pacing
- expert-platform-metrics：平台算法标准查询（被引用型） → 被 fanqie-short + fanqie-novel + fanqie-female + qidian + qidian-long + jjwxc 引用
- expert-bookstatus：项目状态文件创建与维护 → 被 novel-expert-system 初始化流程调用，联动 expert-memory + expert-footprint + expert-serialization-ops
- novel-volume-workflow：卷级全流程自动编排 → 入口级workflow，串联 bookstatus + memory + plot-shuangdian + pacing + quality-gate + footprint 全链路
- expert-revise-loop：质检不通过时的迭代修正 -> 联动 quality-gate + anti-ai-taste + pacing + logic + character + footprint
- expert-reader-tracker：平台数据动态追踪+诊断 -> 联动 platform-metrics + serialization-ops + data-driven + plot-shuangdian
- short-story-workflow：短故事全流程自动编排 -> 入口级workflow，串联 fanqie-short + acg-short + hook + plot-shuangdian + dialogue + quality-gate + revise-loop
- expert-ip-adaptation：IP改编时调用 → 联动 character + worldbuilding + dialogue
- expert-serialization-ops：连载运营阶段 → 联动 data-driven + endurance + title-outro
- expert-style-learner：用户修改生成内容后自动触发 → 联动 writing-style + anti-ai-taste + revision
- novel-project-starter：用户说"想写小说"时自动触发 → 联动 quickstart + dependency-map + novel-expert-system（启动项目初始化链）

**【新增风格Expert联动】**
- expert-writing-style-western：西幻文风 → 联动 xihuan + literary-prose + worldbuilding
- expert-anti-ai-taste：AI辅助写作后必调用 → 联动 literary-prose（先去后加）
- expert-literary-prose：追求文学质感时 → 联动 anti-ai-taste + writing-style + revision
- expert-style-learner：个性化风格学习 → 联动 writing-style（作为风格基线）+ anti-ai-taste（去AI味后提取真实偏好）+ revision（改稿数据来源）

**【协同协议自身说明】**
- expert-collaboration-protocol 为元协议，不参与路由调度
- 协议定义了所有Expert之间的联动规则和调度流程
- 新增Expert时必须同步更新本协议

**【元协议联动】**
- skill-safety-protocol + skill-deployment-protocol：每次skill操作前后必调用，先安全后集成
- skill-deployment-protocol → 联动 novel-expert-system + expert-dependency-map + expert-collaboration-protocol（框架三件套同步更新）
- novel-expert-system-crossover：novel-expert-system子模块 → 按需加载，联动 novel-expert-system
- novel-expert-system-agent-qc：novel-expert-system子模块 → 按需加载，联动 novel-expert-system
- novel-expert-system-techniques：novel-expert-system子模块 → 按需加载，联动 novel-expert-system
