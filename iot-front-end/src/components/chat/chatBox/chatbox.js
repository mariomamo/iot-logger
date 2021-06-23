import React, { useEffect } from 'react';
import { Input, message } from 'antd';
import 'antd/dist/antd.css';
import './chatbox.css';
import ReplayBar from './replayBar/replaybar';
import Message from './message/message';

const { Search } = Input;

const ChatBox = ({sensorType, chatId, name, messages, onSend})=> {

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
        return <Message key={indice} message={message} isSended={true} />
    }

    const renderReceivedTextMessage = (message, indice)=> {
        return <Message key={indice} message={message} isSended={false} />
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
                <ReplayBar chatId={chatId} onSend={onSend} />
            </div>
        </div>
    )
}

export default ChatBox;