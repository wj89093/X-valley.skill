---
name: xindao-park
description: |
  金帝·新道蓝谷生命科学园 AI 招商助手。

  ## 触发关键词（任意匹配即激活）

  ### 园区名称（必触）
  新道蓝谷、金帝新道蓝谷、金帝·新道蓝谷、蓝谷生命科学园、xindao blue valley、新道蓝谷生命科学园

  ### 入驻/租赁意图
  想入驻、想租、想搬、选址、找厂房、找实验室、租厂房、租实验室、产业化落地、中试落地、GMP车间出租、研发场地

  ### 扩张/迁移意图
  扩产、扩线、迁移、搬迁、换场地、换园区、厂房升级

  ### 政策/补贴咨询
  5213、萧山政策、人才政策、创业补贴、房租补贴、研发补助、无偿资助、政府补贴、生物医药政策、杭州创业政策

  ### 园区对比/评估
  对比园区、哪个园区好、生物医药园区、产业园区招商、GMP标准园区、合成生物园区、杭州生物医药园区、萧山园区

  ### 环评/合规
  环评、排污、危化品、GMP认证、FDA认证、废水处理、环保评测、EHS

  ### OPC/共享实验
  OPC社区、产业社区、共享实验室、共享实验设备、算力平台、早期团队入驻、生物制造社区

  ### 反向排除（不触发）
  新道智招（这是企业库项目，与园区招商无关）

  ### 活动通知（定时触发）
  当 cron 或用户要求"检查OPC活动"时，执行活动通知流程（见下方活动通知章节）

## 数据源（全部实时读取飞书文档）

| 用途 | 飞书文档 |
|------|---------|
| 园区介绍、招商Q&A、话术库 | https://www.feishu.cn/docx/IejgdDMPqoceuKxdidDc2t2pnjg |
| 环评与安全合规说明（12个行业） | https://www.feishu.cn/docx/EmjadHWO9o1EDmxdidDc2t2pnjg |
| 最新动态（入驻企业、园区新闻） | https://www.feishu.cn/docx/QeNBde88Foa4Ogxk1wwcz4DenEg |
| OPC社区活动通知 | https://www.feishu.cn/docx/AemaddwOZoFrqQxt0mqcyUrqnrh |

> agent 回答咨询前，应调用 `feishu_fetch_doc` 获取对应文档最新内容。
> 文档由官方维护，无需在 skill 中硬编码任何园区信息。

---

## 联系招商负责人

如需与招商负责人直接沟通，请说：**"我要联系招商负责人"**，系统将推送下方二维码或邀请链接：

https://www.feishu.cn/invitation/page/add_contact/?token=69asd846-9419-48ea-b934-bae846be79dc&unique_id=BVA1msDLHGiyzLJn-wsQkw==

点击即可添加招商负责人为飞书联系人。

---

## OPC 社区活动通知（租户自订阅）

> 租户在本地 agent 安装本 skill 后，每天自动收到 OPC 社区活动更新。
> 活动文档由园区运营方维护，租户的 agent 定时读取，无需人工干预。

### 活动文档
https://www.feishu.cn/docx/AemaddwOZoFrqQxt0mqcyUrqnrh

> **运营方维护**：更新此文档的活动内容，租户 agent 在下次 cron 触发时自动获取。

### Cron 触发配置（租户本地配置）

```json
{
  "name": "OPC社区每日活动检查",
  "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "检查 OPC 社区活动文档 https://www.feishu.cn/docx/AemaddwOZoFrqQxt0mqcyUrqnrh，如有新活动则生成通知内容并通过你的通知渠道发送"
  },
  "sessionTarget": "isolated"
}
```

### 执行流程

1. **读取活动文档**：`feishu_fetch_doc` 读取 `AemaddwOZoFrqQxt0mqcyUrqnrh`
2. **提取最新活动**：获取「近期活动」章节第一个活动（以 🗓 开头）
3. **状态比对**：与本地状态文件 `~/.opc_activities_last_check` 比对，无变化则退出
4. **生成通知**：按下方格式生成通知文本
5. **发送**：通过租户配置的 IM 渠道发送（飞书/TG/邮件/其他）
6. **更新状态**：记录活动日期

### 通知文本格式

```
🗓 新活动通知 | 新道蓝谷 OPC 社区

📅 [活动日期和时间]
📍 [活动地点]
👥 [参与人数/形式]

主题：[活动标题]
[简要描述，不超过50字]

报名截止：[截止日期]
联系方式：OPC运营

#新道蓝谷 #OPC社区 #[方向标签]
```

### 通知渠道配置（租户填写）

```bash
# 选择其一：feishu | telegram | email | stdout（调试）
NOTIFY_VIA="feishu"

# 飞书
FEISHU_CHAT_ID="oc_xxx"      # 群 ID（通知群建立后填入）

# Telegram
TELEGRAM_BOT_TOKEN="xxx"
TELEGRAM_CHAT_ID="xxx"
```
