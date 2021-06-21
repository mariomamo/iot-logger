import React, { useEffect } from 'react';
import { Input, message } from 'antd';
import 'antd/dist/antd.css';
import './chatbox.css';
import ReplayBar from './replayBar/replaybar';

const { Search } = Input;

const ChatBox = ({name, messages})=> {

    const renderMessage = (message, indice)=> {
        if (message !== undefined) {
            switch (message.type) {
                case "text": return renderTextMessage(message, indice);
            }
        }
    }

    const renderTextMessage = (message, indice)=> {
        if (message.isSended) {
            return renderSendedTextMessage(message, indice);
        } else {
            return renderReceivedTextMessage(message, indice);
        }
    }

    const renderSendedTextMessage = (message, indice)=> {
        return (
            <div key={indice} className="chatMessage sent">
                {message.message}
            </div>
        )
    }

    const renderReceivedTextMessage = (message, indice)=> {
        return (
            <div key={indice} className="chatMessage received">
                {message.message}
            </div>
        )
    }

    return (
        <div className='chatBox'>
            <div className='chatInfoHeader'>
                <div>
                    {name}
                </div>
            </div>
            <div className='messageContainer'>
            {messages !== undefined && messages.map((message, indice) => renderMessage(message, indice))}
            </div>
            <div className='inputBox'>
                <ReplayBar />
            </div>
        </div>
    )
}

export default ChatBox;