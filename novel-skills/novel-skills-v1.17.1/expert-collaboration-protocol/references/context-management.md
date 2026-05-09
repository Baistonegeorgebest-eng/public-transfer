# context-management（详细参考）

> 本文件为 expert-collaboration-protocol 的详细参考内容。

## 七、Session与上下文管理

### 7.1 Token警戒线（强制）

```
< 20k tokens：绿色 ✅ 正常
20k-50k tokens：黄色 ⚠️ 监控
50k-80k tokens：橙色 🔶 准备压缩
> 80k tokens：红色 🔴 立即压缩（session-compactor）
> 100k tokens：危险 ❌ 停止接单，写快照，重开session
```

### 7.2 快照写入规则（强制）

```
每完成以下节点，必须写快照到MEMORY.md：
  □ 每5章结束
  □ 每完成一个辅Expert输出
  □ 每次触发压缩前
  □ 每次暂停前（>10分钟无操作）

快照内容：
  ## [时间戳] 任务：[任务名]
  - 已完成：[具体内容]
  - 进行中：[任务名]（进行到X%）
  - 下一步：[具体操作]
  - Token用量：[Xk/100k]
```

---

## 八、异常处理（v2.0）

| 异常 | 处理方式 |
|------|---------|
| 辅Expert无法响应 | 主Expert代为补充，注明"主Expert代补充" |
| 辅Expert超时（>60秒） | 主Expert继续，不等待，注明"部分内容待补充" |
| 多个辅Expert输出冲突 | 主Expert裁定，保留更有依据的，删除矛盾的 |
| Token接近100k | 立即停止，写快照，重开session |
| 用户需求违规 | expert-writing-safety拦截，通知用户修改 |
| 用户绕过主Expert直接调用辅Expert | 我主动归拢到主Expert流程 |

---

*版本：2.0.0 | 2026-04-02*
*新增：Token节省规范/三级响应机制/快照规则/警戒线/最新Skill索引*

---

*本skill为多Expert协同协议，正文已覆盖调度规则和异常处理。*

---
