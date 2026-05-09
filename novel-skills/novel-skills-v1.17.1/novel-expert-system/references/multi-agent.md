# multi-agent（详细参考）

> 本文件为 novel-expert-system 的详细参考内容。按需加载，不要全文读取。

## 第五步：多Agent协作写作流程（2026新增·实测验证版）

> 来源：agent-orchestrator 框架测试 + Claude Code 源码泄露启发
> 测试时间：2026-04-01｜平台：OpenClaw sessions_spawn API
> 结论：完整框架不可用，但"主读skill→生成精简指令→worker执行"模式有效

### 5.1 核心发现：sub-agent 的 token 陷阱

测试数据（2026-04-01）：
- expert-fanqie-short：504净行，加载消耗 36.9k prompt tokens
- sub-agent 超时：90秒内无法同时加载 skill + 执行任务
- 输出：366 tokens（什么都没写完）

结论：不要让 sub-agent 加载 skill。改用"主agent读skill → 生成精简指令 → sub-agent只执行"。

### 5.2 有效协作流程（双模式）

#### 模式一：单章节 worker（轻量任务）

```
主 Agent（执行方）
├── 读取目标 skill 文件（500行）
├── 提取：题材/字数/章节要求/核心禁忌
├── 生成：≤100字执行指令（不含 skill 内容）
├── spawn sub-agent（携带精简指令，不加载 skill）
│   └── sub-agent 直接执行，写完即结束
└── 主 agent 合并输出，更新进度
```

指令模板（主agent生成，注入给worker）：

```