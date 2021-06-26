import React, { createRef, useEffect } from 'react';
import 'antd/dist/antd.css';
import './chatbox.css';
import Message from './Message/message';
import ButtonsReplayBar from './ButtonsReplayBar/buttonsreplaybar';

const ChatBox = ({sensorType, chatId, name, messages, onSend})=> {
    const ref = createRef();

    useEffect(() => {
        scrollMessageBoxToBottom();
    }, [ref])

    const scrollMessageBoxToBottom = ()=> {
        var objDiv = document.getElementById("messageContainer");
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    const renderMessage = (message, indice)=> {
        if (message !== undefined) {
            switch (message.type) {
                case "text": return renderTextMessage(message, indice);
                default: return <div>NOT SUPPORTED</div>
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

    const getButtonsReplyTypes = ()=> {
        if (sensorType === "car") {
            return ["position", "engine on", "engine off", "status"]
        } else if (sensorType === "home") {
            return ["lights on", "lights off", "activate alarm", "deactivate alarm"]
        } else if (sensorType === "air-conditioner") {
            return ["set 20°", "set 22°", "set 24°", "set 26°", "set 28°", "set 30°", "status"]
        }
    }

    return (
        <div className='chatBox'>
            <div className='chatInfoHeader'>
                <div>
                    {name}
                </div>
            </div>
            <div id="messageContainer" ref={ref} className='messageContainer'>
                {messages !== undefined && messages.map((message, indice) => renderMessage(message, indice))}
            </div>
            <div className='inputBox'>
                <ButtonsReplayBar chatId={chatId} onSend={onSend} buttonReplyes={getButtonsReplyTypes()}/>
            </div>
        </div>
    )
}

export default ChatBox;