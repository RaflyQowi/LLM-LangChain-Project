# Updated CSS
css = '''
<style>
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    border: 1px solid #d3d3d3; /* Add a subtle border */
}

.chat-message.user {
    background-color: #2b313e;
}

.chat-message.bot {
    background-color: #475063;
}

.chat-message .avatar {
    width: 15%; /* Adjust avatar size */
}

.chat-message .avatar img {
    max-width: 60px;
    max-height: 60px;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    width: 85%; /* Adjust message width */
    padding: 0.75rem;
    color: #fff;
}
</style>
'''

# Updated Templates
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/3pvQJ2B/bot-icon.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/HY8rRpL/human.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
