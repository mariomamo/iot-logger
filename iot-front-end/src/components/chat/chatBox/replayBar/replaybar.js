import React, { createRef, useEffect, useState } from 'react';
import { Input, Button } from 'antd';
import './replaybar.css';
import 'antd/dist/antd.css';

const ReplayBar = ({chatId, onSend})=> {
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

export default ReplayBar;