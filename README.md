# 新道蓝谷.skill

> 金帝·新道蓝谷生命科学园 / 团队 / 个人 的项目、工具、技能合集

新道蓝谷不只是一个园区，也是我们这群人的代号。这里放跟新道蓝谷相关的所有项目，每个项目独立发展。

---

## 项目

### 📚 xiaoyuan-vault

LLM 友好的本地知识库管理工具（Electron 桌面应用）。

- **Skill.md Agent 协议** — LLM 通过 HTTP/SSE 主动调用 vault，不是单纯读文件
- **Markdown 编辑** — atomic-editor 实时渲染
- **知识图谱** — 自动从 `_wiki/` 构建节点 + 关系
- **多 vault 隔离** — 每个 vault 独立索引与配置
- **Schema & Lint** — 自动检测 + 修复
- **多主题 + 国际化**

**状态**：✅ v1.3.1-free
**License**：MIT
**仓库**：[github.com/wj89093/xiaoyuan-vault-free](https://github.com/wj89093/xiaoyuan-vault-free)

#### 与同类 LLM Wiki 产品的对比

| 维度 | xiaoyuan-vault | AnythingLLM | Khoj | Reor | Mem |
|------|---------------|-------------|------|------|-----|
| **开源协议** | MIT | MIT | AGPL | GPL | ❌ 闭源 |
| **部署方式** | 桌面 App | Docker / Desktop | Docker / 桌面 | 桌面 App | 云端 |
| **Skill.md Agent 协议** | ✅ 内置 | ❌ | ❌ | ❌ | ❌ |
| **LLM 接入方式** | 任何 Skill 协议 Agent | OpenAI / Ollama | 多家 | 本地为主 | 集成 |
| **多 vault** | ✅ 内置 | ⚠️ workspaces | ❌ | ❌ | ⚠️ 集合 |
| **Schema / Lint** | ✅ 内置 | ⚠️ 提示词 | ❌ | ❌ | ❌ |
| **FTS 搜索** | ✅ FTS5 | ✅ 向量 | ✅ | ✅ | ✅ |
| **中文友好** | ✅ | ⚠️ | ⚠️ | ⚠️ | ❌ |

**差异化**：

- **Skill.md Agent 协议（独占）** — 任何支持 Skill.md 的 Agent（OpenClaw / Claude Code / 自建 LLM）可直接调用 vault；竞品都是"LLM 读文档"，xiaoyuan-vault 是"LLM **通过协议** 调用 vault"
- **桌面 App 而非 Docker** — 单机安装即用
- **多 vault + Schema/Lint 组合** — 结构化是 LLM 友好的基础
- **MIT 协议** — 比 AGPL 更宽松

---

### 🤖 skill-x-valley

金帝·新道蓝谷生命科学园 AI 招商助手（Skill.md 文档）。

- **4 个飞书数据源** — 实时读取动态、话术、环评合规、OPC 活动
- **智能触发** — 园区名称 / 入驻 / 政策 / 环评 / OPC 等关键词自动激活
- **数据优先** — 政策金额精确引用飞书原文，不自行补充
- **招商规范** — 首次响应调取话术库、留资通知、不过度承诺
- **OPC 活动通知** — 每天 09:00 自动抓取新活动并推送
- **贪吃虾对战** — "来一局贪吃虾"触发游戏，Agent 自动参战

**状态**：✅ v1.0
**分类**：Skill.md 文档
**License**：MIT

---

**License**：MIT © 新道蓝谷团队
