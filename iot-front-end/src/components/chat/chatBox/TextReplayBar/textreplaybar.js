import React, { createRef } from 'react';
import { Button } from 'antd';
import './textreplaybar.css';
import 'antd/dist/antd.css';

const TextReplayBar = ({chatId, onSend})=> {
    const message = createRef();
    
    const handleKeyPress = (e)=> {
        if (e.key.toLowerCase() === "enter") {
            sendMessage();
        }
    }

    const sendMessage = ()=> {
        onSend(chatId, message.current.value);
        message.current.value = "";
    }

    return (
        <div className="replyBar">			
			<input ref={message} type="text" className="textArea" onKeyPress={handleKeyPress} placeholder="Type your message..." cols="40" rows="5" />
            <Button className="sendButton" type="primary" onClick={sendMessage}>Send</Button>
		</div>
    )
}

export default TextReplayBar;