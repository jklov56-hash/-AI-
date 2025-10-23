// 聊天界面JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    const loading = document.getElementById('loading');
    const charCount = document.querySelector('.char-count');
    const actionButtons = document.querySelectorAll('.action-btn');
    
    let isLoading = false;
    const maxLength = 500;
    
    // 快速操作按钮点击事件
    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.getAttribute('data-action');
            let message = '';
            
            switch(action) {
                case '学习计划':
                    message = '我想制定一个学习计划，你能帮我吗？';
                    break;
                case '时间管理':
                    message = '我需要一些时间管理的建议';
                    break;
                case '习惯养成':
                    message = '我想养成一些好习惯，有什么建议吗？';
                    break;
                case '情绪支持':
                    message = '我今天心情不太好，能给我一些支持吗？';
                    break;
            }
            
            if (message) {
                messageInput.value = message;
                updateCharCount();
                updateSendButton();
                sendMessage();
            }
        });
    });
    
    // 发送消息
    async function sendMessage() {
        const message = messageInput.value.trim();
        
        if (!message || isLoading) {
            return;
        }
        
        if (message.length > maxLength) {
            showError('消息长度不能超过500个字符');
            return;
        }
        
        isLoading = true;
        showLoading(true);
        updateSendButton();
        
        try {
            // 添加用户消息
            addMessageToUI('user', message);
            
            // 清空输入框
            messageInput.value = '';
            updateCharCount();
            
            // 发送到服务器
            const response = await fetch('/api/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // 添加AI回复
            if (data.ai_message) {
                addMessageToUI('ai', data.ai_message.content, data.ai_message.timestamp);
            }
            
        } catch (error) {
            console.error('发送消息失败:', error);
            showError('发送消息失败，请重试');
        } finally {
            isLoading = false;
            showLoading(false);
            updateSendButton();
        }
    }
    
    // 添加消息到界面
    function addMessageToUI(type, content, timestamp = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        
        const icon = document.createElement('i');
        icon.className = type === 'ai' ? 'fas fa-heart' : 'fas fa-user';
        avatar.appendChild(icon);
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        // 处理换行符，将\n转换为<br>
        const formattedContent = content.replace(/\n/g, '<br>');
        messageText.innerHTML = formattedContent;
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = timestamp || getCurrentTime();
        
        messageContent.appendChild(messageText);
        messageContent.appendChild(messageTime);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    // 更新字符计数
    function updateCharCount() {
        const currentLength = messageInput.value.length;
        charCount.textContent = `${currentLength}/${maxLength}`;
        
        if (currentLength > maxLength * 0.9) {
            charCount.style.color = '#dc3545';
        } else if (currentLength > maxLength * 0.7) {
            charCount.style.color = '#ffc107';
        } else {
            charCount.style.color = '#6c757d';
        }
    }
    
    // 更新发送按钮状态
    function updateSendButton() {
        const message = messageInput.value.trim();
        const isValid = message.length > 0 && message.length <= maxLength && !isLoading;
        
        sendButton.disabled = !isValid;
        sendButton.style.opacity = isValid ? '1' : '0.6';
    }
    
    // 显示/隐藏加载动画
    function showLoading(show) {
        loading.style.display = show ? 'flex' : 'none';
    }
    
    // 显示错误信息
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #dc3545;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            z-index: 1001;
        `;
        
        document.body.appendChild(errorDiv);
        
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 3000);
    }
    
    // 滚动到底部
    function scrollToBottom() {
        setTimeout(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 100);
    }
    
    // 获取当前时间
    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString('zh-CN', { 
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit' 
        });
    }
    
    // 绑定事件
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    messageInput.addEventListener('input', () => {
        updateCharCount();
        updateSendButton();
    });
    
    // 初始化
    updateCharCount();
    updateSendButton();
});
