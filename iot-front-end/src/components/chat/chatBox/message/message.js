import React, { useEffect, useState } from 'react';
import './message.css';


const Message = ({message, isSended})=> {
    if (isSended) {
        return (
            <div className={"chatMessage sent"}>
                {message.message}
            </div>
        )
    } else {
        return (
            <div className={"chatMessage received"}>
                {message.message}
            </div>
        )
    }
}

export default Message;