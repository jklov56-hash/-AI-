from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import requests
import json
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = 'personal-ai-assistant-key'

# 模拟用户数据
fake_users = {
    'admin': 'admin123',
    'user1': 'password123',
    'guest': 'guest123'
}

# 聊天历史存储
chat_history = {}

# 用户个人数据存储
user_data = {}

# 个人AI助手配置
class PersonalAIAssistant:
    def __init__(self):
        self.api_key = ''
        self.api_url = 'https://api.deepseek.com/chat/completions'
    
    def inference_chat_deepseek(self, chat, token):
        """DeepSeek API调用函数"""
        url = "https://api.deepseek.com/chat/completions"

        data = {
            "messages": [],
            "model": "deepseek-chat",
            "frequency_penalty": 0,
            "max_tokens": 4096,
            "presence_penalty": 0,
            "response_format": {
                "type": "text"
            },
            "stop": None,
            "stream": False,
            "stream_options": None,
            "temperature": 0.7,
            "top_p": 1,
            "tools": None,
            "tool_choice": "none",
            "logprobs": False,
            "top_logprobs": None
        }

        for role, content in chat:
            data["messages"].append({"role": role, "content": content})

        payload = json.dumps(data)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        try:
            res = requests.request("POST", url, headers=headers, data=payload)
            res_json = json.loads(res.text)
            res_content = res_json["choices"][0]["message"]["content"]
            return res_content
        except Exception as e:
            print(f"DeepSeek API调用失败: {e}")
            return None
    
    def get_response(self, message, context="", username=""):
        """获取AI回复"""
        try:
            # 构建个性化系统提示词
            system_prompt = self._build_personalized_prompt(username)
            
            # 构建对话历史
            chat_history = [("system", system_prompt)]
            
            # 如果有上下文，添加到对话历史
            if context:
                chat_history.append(("user", context))
            
            # 添加当前用户消息
            chat_history.append(("user", message))
            
            # 调用DeepSeek API
            response = self.inference_chat_deepseek(chat_history, self.api_key)
            
            if response:
                return response
            else:
                # 如果API调用失败，返回备用回复
                return self.get_fallback_response(message, username)
                
        except Exception as e:
            print(f"AI回复生成失败: {e}")
            return self.get_fallback_response(message, username)
    
    def _build_personalized_prompt(self, username):
        """构建个性化提示词"""
        base_prompt = """你是一个贴心的个人AI生活助手，专注于帮助用户解决日常生活、学习成长和时间管理方面的问题。

核心功能：
1. 生活助手：帮助规划日常生活，提供生活建议，解决日常问题
2. 学习成长：提供学习建议，推荐学习资源，制定学习计划
3. 时间管理：帮助制定日程安排，提醒重要事项，优化时间利用

你的特点：
- 温暖贴心：像朋友一样关心用户的生活和成长
- 个性化：根据用户的具体情况提供定制化建议
- 实用性强：提供具体可行的解决方案
- 鼓励支持：在用户遇到困难时给予鼓励和支持
- 持续跟进：关注用户的长期发展

请用中文回答，语气自然亲切，避免过于机械。根据用户的具体需求提供有针对性的帮助。"""
        
        # 如果有用户数据，可以进一步个性化
        if username and username in user_data:
            user_info = user_data[username]
            if 'interests' in user_info:
                base_prompt += f"\n\n用户兴趣：{', '.join(user_info['interests'])}"
            if 'goals' in user_info:
                base_prompt += f"\n用户目标：{', '.join(user_info['goals'])}"
        
        return base_prompt
    
    def get_fallback_response(self, message, username=""):
        """备用回复（当API调用失败时使用）"""
        # 根据消息内容分类提供个性化回复
        if any(word in message.lower() for word in ['你好', '您好', 'hi', 'hello']):
            return self._get_greeting_response(username)
        elif any(word in message.lower() for word in ['学习', '读书', '课程', '知识']):
            return self._get_learning_response(message)
        elif any(word in message.lower() for word in ['时间', '计划', '日程', '安排']):
            return self._get_time_management_response(message)
        elif any(word in message.lower() for word in ['习惯', '坚持', '养成']):
            return self._get_habit_response(message)
        elif any(word in message.lower() for word in ['情绪', '心情', '压力', '焦虑']):
            return self._get_emotional_response(message)
        elif any(word in message.lower() for word in ['目标', '梦想', '未来']):
            return self._get_goal_response(message)
        else:
            return self._get_general_response(message)
    
    def _get_greeting_response(self, username):
        """问候回复"""
        greetings = [
            f"你好{username}！我是你的个人AI生活助手，很高兴为你服务！今天有什么需要我帮助的吗？",
            f"欢迎回来{username}！我一直在等你呢，今天想聊些什么？",
            f"嗨{username}！看到你真开心，今天过得怎么样？有什么我可以帮你的吗？",
            f"{username}你好！我是你的专属AI助手，专注于生活、学习和时间管理，随时为你提供帮助！"
        ]
        return random.choice(greetings)
    
    def _get_learning_response(self, message):
        """学习相关回复"""
        responses = [
            "学习是一个持续的过程！我建议你可以先明确学习目标，然后制定一个合理的学习计划。每天坚持学习30分钟，效果会比偶尔学几个小时更好哦！",
            "关于学习，我建议采用番茄工作法：25分钟专注学习，然后休息5分钟。这样既能保持专注，又不会太累。",
            "学习最重要的是找到适合自己的方法。你可以尝试不同的学习方式，比如看视频、读书、做练习，找到最适合你的那一种。",
            "我建议把大目标分解成小任务，每天完成一点点。这样既不会感到压力太大，又能看到持续的进步。"
        ]
        return random.choice(responses)
    
    def _get_time_management_response(self, message):
        """时间管理回复"""
        responses = [
            "时间管理的关键是优先级排序。我建议使用四象限法则：重要且紧急 > 重要不紧急 > 紧急不重要 > 不重要不紧急。",
            "试试时间块管理法：把一天分成几个时间段，每个时间段专注做一件事。这样效率会更高！",
            "我推荐使用番茄钟工作法，25分钟工作+5分钟休息的循环，可以有效提高专注力。",
            "制定日程时记得留出缓冲时间，应对突发情况。另外，每天安排一些自我提升的时间也很重要。"
        ]
        return random.choice(responses)
    
    def _get_habit_response(self, message):
        """习惯养成回复"""
        responses = [
            "习惯养成需要21天！我建议从小习惯开始，比如每天阅读10分钟，或者每天锻炼15分钟。坚持最重要！",
            "建立新习惯时，可以把它和已有的习惯绑定。比如刷牙后立即阅读，这样更容易记住。",
            "习惯追踪很有帮助！你可以用日历记录每天的完成情况，看到连续打卡会很有成就感。",
            "不要追求完美，完成比完美更重要。即使某天没有完全做到，也不要放弃，第二天继续就好。"
        ]
        return random.choice(responses)
    
    def _get_emotional_response(self, message):
        """情绪支持回复"""
        responses = [
            "我理解你的感受。每个人都会有情绪波动的时候，这是很正常的。试着深呼吸，给自己一些空间。",
            "情绪就像天气，有晴天也有雨天。重要的是学会与各种情绪相处，接纳它们的存在。",
            "当你感到压力时，可以试试写情绪日记，把感受写下来。这有助于理清思绪，释放压力。",
            "记住要对自己温柔一些。成长是一个过程，允许自己有不完美的时候。"
        ]
        return random.choice(responses)
    
    def _get_goal_response(self, message):
        """目标规划回复"""
        responses = [
            "设定目标时，建议使用SMART原则：具体的、可衡量的、可达成的、相关的、有时限的。",
            "把大目标分解成小里程碑，每完成一个就庆祝一下。这样能保持动力！",
            "目标要既有挑战性又现实可行。太容易会无聊，太难会挫败，找到平衡点很重要。",
            "定期回顾和调整目标也很重要。随着成长，你的目标可能会发生变化，这是很正常的。"
        ]
        return random.choice(responses)
    
    def _get_general_response(self, message):
        """通用回复"""
        responses = [
            "我理解你的需求。作为你的个人AI助手，我会尽力为你提供有用的建议和支持。",
            "这个问题很有意思！让我从生活助手的角度为你分析一下...",
            "我注意到你在思考这个问题，这很棒！持续反思是成长的重要部分。",
            "基于我的理解，我建议你可以从这几个方面考虑...",
            "每个人都有自己的节奏和方式，找到最适合你的方法才是最重要的。"
        ]
        return random.choice(responses)

# 初始化AI模型
ai_model = PersonalAIAssistant()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in fake_users and fake_users[username] == password:
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            flash('用户名或密码错误，请重试')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'])

@app.route('/api/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({'error': '未登录'}), 401
    
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'error': '消息不能为空'}), 400
    
    username = session['username']
    
    # 获取用户聊天历史
    if username not in chat_history:
        chat_history[username] = []
    
    # 添加用户消息
    user_message = {
        'type': 'user',
        'content': message,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    chat_history[username].append(user_message)
    
    # 获取AI回复
    context = ""
    if len(chat_history[username]) > 2:
        # 获取最近几条消息作为上下文
        recent_messages = chat_history[username][-4:-1]
        context = "\n".join([f"{msg['type']}: {msg['content']}" for msg in recent_messages])
    
    ai_response = ai_model.get_response(message, context, username)
    
    # 添加AI回复
    ai_message = {
        'type': 'ai',
        'content': ai_response,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    chat_history[username].append(ai_message)
    
    return jsonify({
        'user_message': user_message,
        'ai_message': ai_message
    })

@app.route('/api/chat_history')
def get_chat_history():
    if 'username' not in session:
        return jsonify({'error': '未登录'}), 401
    
    username = session['username']
    return jsonify(chat_history.get(username, []))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)


