import React from 'react';
import { Button } from 'antd';
import './buttonsreplaybar.css';

const ButtonsReplayBar = ({chatId, onSend, buttonReplyes})=> {
    const renderButton = (buttonText, indice)=> {
        return <Button key={indice} onClick={() => onSend(chatId, buttonText)} type="primary">{buttonText}</Button>
    }

    return (
        <div className="replyBar">
            <div className="buttonsPanel">
                {buttonReplyes !== undefined && buttonReplyes.map((buttonText, indice) => renderButton(buttonText, indice))}
            </div>
        </div>
    )
}

export default ButtonsReplayBar;