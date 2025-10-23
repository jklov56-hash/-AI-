# AI智能客服系统

一个基于DeepSeek大模型的智能客服系统，提供现代化的Web界面和智能对话功能。

## 功能特点

- 🤖 **智能对话**: 集成DeepSeek大模型，提供自然流畅的对话体验
- 🎨 **现代化界面**: 美观的聊天界面，支持响应式设计
- 🔐 **用户认证**: 支持多用户登录系统
- 💬 **实时聊天**: 实时消息发送和接收
- 📱 **移动端适配**: 完美支持手机和平板设备
- 🛡️ **错误处理**: 完善的错误处理和备用回复机制

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

### 3. 访问系统

打开浏览器访问: http://localhost:5000

## 登录账号

系统提供以下测试账号：

| 用户名 | 密码 |
|--------|------|
| admin | admin123 |
| user1 | password123 |
| customer | customer123 |

## 技术架构

- **后端**: Flask (Python)
- **前端**: HTML5 + CSS3 + JavaScript
- **AI模型**: DeepSeek API
- **样式**: 现代化渐变设计 + Font Awesome图标

## 主要文件结构

```
界面/
├── app.py              # Flask主应用
├── requirements.txt    # Python依赖
├── README.md          # 项目说明
├── static/
│   ├── style.css      # 登录页面样式
│   ├── chat.css       # 聊天界面样式
│   └── chat.js        # 聊天功能JavaScript
└── templates/
    ├── login.html     # 登录页面
    └── chat.html      # 聊天界面
```

## API配置

系统使用DeepSeek API进行智能回复。如需更换API密钥，请修改 `app.py` 中的 `AIModel` 类：

```python
class AIModel:
    def __init__(self):
        self.api_key = 'your-deepseek-api-key'
        self.api_url = 'https://api.deepseek.com/chat/completions'
```

## 自定义配置

### 修改系统提示词

在 `app.py` 的 `get_response` 方法中修改 `system_prompt`：

```python
system_prompt = """你是一个专业的客服助手，请用友好、专业的态度回答用户的问题。
回答要简洁明了，如果遇到技术问题，请提供具体的解决方案。
如果用户询问产品信息，请提供详细的产品介绍。
始终保持礼貌和耐心。
请用中文回答，回答要自然流畅，不要过于机械。"""
```

### 调整AI参数

在 `inference_chat_deepseek` 方法中可以调整以下参数：

- `temperature`: 控制回复的随机性 (0.0-1.0)
- `max_tokens`: 最大回复长度
- `top_p`: 核采样参数

## 故障排除

### 1. API调用失败

如果DeepSeek API调用失败，系统会自动使用备用回复。检查：
- API密钥是否正确
- 网络连接是否正常
- API配额是否充足

### 2. 页面样式异常

确保所有CSS文件都正确加载，检查浏览器控制台是否有错误。

### 3. 消息发送失败

检查浏览器控制台的网络请求，确认后端服务正常运行。

## 扩展功能

### 添加数据库支持

可以集成SQLite、MySQL或PostgreSQL来持久化存储聊天记录和用户信息。

### 增加更多AI模型

可以添加对其他大模型API的支持，如OpenAI、讯飞等。

### 添加文件上传

支持图片、文档等文件的上传和AI分析。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！ 