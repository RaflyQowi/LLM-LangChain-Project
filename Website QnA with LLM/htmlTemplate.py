# Updated CSS
# CSS Styles
css = '''
<style>
    /* Styling for the body of the Streamlit app */
    body {
        background-color: #f2f7ff; /* Soft blue background */
        margin: 0; /* Remove default margin */
        padding: 0; /* Remove default padding */
    }

    /* Styling for the chat container */
    .chat-container {
        max-width: 600px; /* Adjust the maximum width as needed */
        margin: 0 auto; /* Center the chat container */
        background-color: #ffffff; /* White background */
        padding: 1rem; /* Add padding to the chat container */
        border-radius: 1rem; /* Rounded corners for the chat container */
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add a subtle box shadow */
    }

    /* Styling for the chat messages */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        border: 1px solid #d3d3d3; /* Add a subtle border */
    }

    /* Styling for user messages */
    .chat-message.user {
        background-color: #ffffff; /* White background for user messages */
    }

    /* Styling for bot messages */
    .chat-message.bot {
        background-color: #9dc8e5; /* Soft blue background for bot messages */
    }

    /* Styling for the avatar */
    .chat-message .avatar {
        width: 15%; /* Adjust avatar size */
    }

    /* Styling for the avatar image */
    .chat-message .avatar img {
        max-width: 60px;
        max-height: 60px;
        border-radius: 50%;
        object-fit: cover;
    }

    /* Styling for the message content */
    .chat-message .message {
        flex: 1; /* Allow the message to take up remaining space */
        padding: 0.75rem;
        color: #495057; /* Dark text color for better readability */
    }

    /* Styling for strong (name) in the message */
    .chat-message .message strong {
        margin-right: 0.25rem; /* Adjust the margin as needed */
    }
</style>
'''

# HTML Templates for Bot and User Messages
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/dp2yyWP/bot.jpg">
    </div>
    <div class="message">
        <strong>Doraemon:</strong> {{MSG}}
    </div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/JB2sps1/human.jpg">
    </div>    
    <div class="message">
        <strong>Nobita:</strong> {{MSG}}
    </div>
</div>
'''