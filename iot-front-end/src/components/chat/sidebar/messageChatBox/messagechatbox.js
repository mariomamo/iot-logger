import React, { useEffect, useState } from 'react';
import './messagechatbox.css';

const MessageChatBox = ({id, name, lastMessage, ora, img, selected, onClick})=> {
    const [chatboxClassName, setChatboxClassName] = useState("message");
    const [chatboxInfo, setChatboxInfo] = useState("messageinfo");
    const [oraStyle, setOraStyle] = useState("ora");

    useEffect(() => {
        if (selected) {
            setSelected();
        } else {
            setNotSelected();
        }
    });

    const setSelected = ()=> {
        setChatboxClassName("message selected");
        setChatboxInfo("messageinfo selected");
        setOraStyle("ora selected");
    }

    const setNotSelected = ()=> {
        setChatboxClassName("message");
        setChatboxInfo("messageinfo");
        setOraStyle("ora");
    }

    return (
        <div onClick={() => onClick(id)} className={chatboxClassName}>
            <div className='propic'>
                <img alt="not found" src={img}/>
            </div>
            <div className={chatboxInfo}>
                <div className='textname'>
                    {name}
                </div>
                <div className='messagepreview'>
                    {lastMessage}
                </div>
            </div>
            <div className={oraStyle}>
                {ora}
            </div>
        </div>
    )
}

export default MessageChatBox;