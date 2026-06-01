# 项目索引

> 这个文档列出 X-valley.skill 合集下所有项目的状态、用途、和维护者。

## 当前项目

### 1. xiaoyuan-vault

- **路径**：`projects/xiaoyuan-vault/`
- **远程仓库**：https://github.com/wj89093/xiaoyuan-vault-free
- **状态**：✅ v1.3.0-free 已发布
- **类别**：桌面应用 (Electron)
- **License**：MIT
- **作用**：免费的本地知识库管理工具，支持 Markdown 编辑、知识图谱、多 vault 隔离、Schema、Lint
- **发布仓库**：[wj89093/xiaoyuan-vault-free](https://github.com/wj89093/xiaoyuan-vault-free)（开源版专用）
- **主开发仓库**：[wj89093/xiaoyuan-vault](https://github.com/wj89093/xiaoyuan-vault)（含 Pro 代码）
- **开源版 vs Pro**：
  - 开源版：vault 主功能 + Skill.md 插件（接用户自己的 Agent）
  - Pro 版：付费，含内置 AI Agent / 剪贴板浮窗 / AI Chat

### 2. skill-x-valley

- **路径**：`projects/skill-x-valley/`
- **状态**：✅ v1.0
- **类别**：Skill.md 文档
- **License**：MIT
- **作用**：金帝·新道蓝谷生命科学园招商助手，4 个飞书数据源
- **使用场景**：嵌入到支持 Skill 协议的 AI Agent（OpenClaw / Claude Code / 自建 LLM）

---

## 添加新项目

新项目应该：

1. **独立仓库**（不与合集混编）
2. **MIT 兼容 License**
3. **明确维护者**（至少 1 人）
4. **有 README + 入门指南**

添加流程：
```bash
# 1. 在 GitHub 上创建新仓库
# 2. 在 X-valley.skill 根目录执行
git submodule add <new-repo-url> projects/<name>

# 3. 更新顶层 README.md 把新项目加到表格

# 4. 提交
git add . && git commit -m "feat: add <name> submodule"
git push
```
