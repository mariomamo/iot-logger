import React, { createRef } from 'react';
import { Button } from 'antd';
import './buttonsreplaybar.css';

const ButtonsReplayBar = ({chatId, onSend, buttonReplyes})=> {
    const message = createRef();

    const contentStyle = {
        background: '#364d79',
    };

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