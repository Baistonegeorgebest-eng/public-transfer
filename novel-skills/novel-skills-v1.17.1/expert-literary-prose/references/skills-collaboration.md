# 与其他Skills的协作关系

## 协作矩阵

| 配合 Skill | 协作方式 | 触发场景 |
|-----------|---------|---------|
| `expert-writing-style` | 提供网文大神的句式模板，本skill负责"文学化升级" | 从网文风格出发，追求更高质感时 |
| `expert-writing-style-western` | 共享西方文学技法，本skill侧重中文译本调性 | 西幻题材需要翻译腔/史诗感时 |
| `expert-anti-ai-taste` | 先用anti-ai去掉AI味，再用本skill注入文学味 | 生成内容有明显AI痕迹时 |
| `expert-xihuan` | expert-xihuan负责西幻设定，本skill负责西幻文风 | 西幻题材的完整创作流程 |
| `expert-character` | expert-character负责人物设计，本skill负责人物的文学性表达 | 写人物内心、出场、离场时 |
| `expert-emotion` | expert-emotion设计情感场景，本skill负责用文学手法表达 | 需要高质量情感场景时 |
| `expert-pacing` | expert-pacing控制节奏，本skill控制"安静段落"的文学浓度 | 在快节奏中插入文学性停顿时 |
| `expert-revision` | expert-revision做全面审稿，本skill做"文学质感专项审查" | 完稿后的质量提升阶段 |

## 调用规则

1. **独立使用**：当用户明确要求"写得文学一点""要有文学质感""像江南的风格"时，直接调用本skill
2. **协同使用**：当用户在其他skill的工作中需要提升文字质感时，本skill作为辅助skill提供文学性写法建议
3. **优先级**：本skill的建议优先级低于平台规则类skills（如expert-fanqie-novel的格式要求），但高于一般性写作建议
