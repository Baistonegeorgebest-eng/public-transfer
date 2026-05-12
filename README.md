# public-transfer

小说语料库分析项目。

## ⚠️ 操作规范（必读）

### 推送铁律

1. **永远不要 `git push --force`**，除非你100%确定远程分支可以被覆盖
2. **只推送新增/修改的文件**，不要重新提交整个仓库
3. **推送前先 pull**：`git pull origin master --rebase`，解决冲突后再 push
4. **SSH 超时处理**：如果 SSH 连接超时，等待后重试，不要换方法 force push

### 标准工作流

```bash
# 1. 拉取最新代码
GIT_SSH_COMMAND="ssh -i ~/.ssh/.github_miclaw -o StrictHostKeyChecking=no -o ConnectTimeout=30 -o ServerAliveInterval=10" git pull origin master --rebase

# 2. 添加新文件（只add新增的，不要 git add -A）
git add novel-corpus-analysis/新文件.md

# 3. 提交
git commit -m "feat: 描述"

# 4. 推送
GIT_SSH_COMMAND="ssh -i ~/.ssh/.github_miclaw -o StrictHostKeyChecking=no -o ConnectTimeout=30 -o ServerAliveInterval=10" git push origin master
```

### SSH 密钥

- 路径：`~/.ssh/.github_miclaw`
- Git config：`bot@openclaw.ai` / `OpenClaw Bot`

### 分支说明

| 分支 | 内容 |
|------|------|
| master | 完整数据（小说txt + 分析报告 + 脚本 + 指纹表） |
| main | 分析报告 + 脚本（无txt） |

### 拉取方式对比

| 方式 | 命令 | 适用场景 |
|------|------|---------|
| SSH clone | `git clone git@github.com:Baistonegeorgebest-eng/public-transfer.git` | 完整克隆 |
| ghfast tarball | `curl -L -o repo.tar.gz "https://ghfast.top/https://github.com/...tar.gz"` | 快速下载 |

### 本地目录

- master: `/root/.openclaw/workspace/public-transfer-master-git`
- main: `/root/.openclaw/workspace/public-transfer-main-git`

---

## 项目内容

### 小说语料库

- **小说原文**：`novel-txts/*.txt`（356 本，已去重校验）
- **指纹表**：`novel-corpus-analysis/fingerprint-table-v4.4.md`（362 本）
- **人味协议**：`novel-corpus-analysis/human-flavor-protocol-v4.4.md`
- **分析报告**：`novel-corpus-analysis/analysis-*.md`（421+ 份）

### 深度分析（2026-04-28 新增）

- **Tier 1**（12本）：诡秘之主、大奉打更人、盘龙、凡人修仙传、阳神、完美世界、斗破苍穹、斗罗大陆、剑来、庆余年、万族之劫、我在精神病院学斩神
- **Tier 2**（15本）：冠军之心、我们是冠军、美食供应商、超神机械师、明朝败家子、官居一品、回到明朝当王爷、末世之黑暗召唤师、霍格沃茨之血脉巫师、猎魔人在霍格沃茨、漫威里的德鲁伊、某美漫的传奇人生、超凡黎明、奥术神座、大国重工
- **Tier 3**（17本）：牧神记、遮天、吞噬星空、武动乾坤、大主宰、仙逆、一念永恒、我欲封天、圣墟、深空彼岸、星门、雪中悍刀行、将夜、赘婿、天道图书馆、深海余烬、放开那个女巫

### 脚本

- `scripts/analyze-batch.py` - 批量标点分析
- `scripts/batch-generate-analysis.py` - 批量报告生成

---

_Last updated: 2026-04-28_

---

## ⚠️ 教训记录（2026-04-28）

### 事故回顾
上上个 session 把整个 workspace 文件夹（AGENTS.md、SOUL.md 等）连同项目文件一起推送到了 main 和 master 分支，导致：
- 两个分支根目录结构被污染
- main 分支膨胀到 1.3GB（正常 3.6MB）
- 嵌套了错误的子文件夹

### 操作规范（追加）

5. **禁止 `git add -A`** — 只 add 新增/修改的具体文件
6. **推送前 `git status` 确认** — 确保没有无关文件混入
7. **workspace 文件不入仓库** — AGENTS.md、SOUL.md 等是本地工作文件，不属于项目仓库
8. **新 session 先 pull 再操作** — 确认远程最新状态

### 推送命令模板
```bash
GIT_SSH_COMMAND="ssh -i ~/.ssh/.github_miclaw -o StrictHostKeyChecking=no -o ConnectTimeout=60 -o ServerAliveInterval=30" git push origin <branch>
```

_Updated: 2026-04-28 17:52 GMT+8_
