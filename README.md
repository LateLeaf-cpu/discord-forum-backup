# Discord 论坛频道备份工具

此工具用于备份 Discord 论坛频道的所有帖子（线程）。它通过以下步骤工作：

1. 使用 Discord Bot 获取论坛频道的所有线程ID
2. 使用 DiscordChatExporter 导出每个线程的内容
3. 将所有线程内容合并为一个文件

## 准备工作

### 1. 创建 Discord Bot
1. 访问 [Discord 开发者门户](https://discord.com/developers/applications)
2. 创建新应用
3. 转到 "Bot" 标签页：
   - 创建 Bot
   - 启用 **SERVER MEMBERS INTENT** 和 **MESSAGE CONTENT INTENT**
   - 复制 Bot Token（保密！）

### 2. 邀请 Bot 到服务器
1. 在 "OAuth2" > "URL Generator" 中：
   - 勾选 `bot` 范围
   - 勾选权限：`View Channels`, `Read Message History`
2. 使用生成的链接邀请 Bot 到你的服务器

### 3. 获取频道 ID
1. 在 Discord 中打开开发者模式（设置 > 高级）
2. 右键点击论坛频道 > 复制 ID

### 4. 下载 DiscordChatExporter
1. 从 [GitHub 发布页](https://github.com/Tyrrrz/DiscordChatExporter/releases) 下载最新 CLI 版本
2. 解压到合适位置

## 配置

1. 复制 `config.example.json` 为 `config.json`
2. 编辑 `config.json`：
   - `bot_token`: 你的 Bot Token
   - `channel_id`: 论坛频道 ID
   - `dce_path`: DiscordChatExporter.Cli.exe 的完整路径
   - `output_thread_ids`: 线程ID保存文件（默认：thread_ids.txt）
   - `output_dir`: 导出数据目录（默认：forum_backup）
   - `delay_seconds`: 导出间隔（秒，防止速率限制）
   - `proxy`: 代理地址（可选）
   - `token_type`: Token 类型（默认 Bot，可选 User）

## 使用

### 1. 安装依赖
```bash
pip install -r requirements.txt
