import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCheck } from '@fortawesome/free-solid-svg-icons'
import './message.css';


const Message = ({message, isSended})=> {
    if (isSended) {
        return (
            <div className={"chatMessage sent"}>
                <div>
                    {message.message}
                </div>
                <div className="hour-box">
                    <div className="hour">
                        {message.hour}
                    </div>
                    <div className="check">
                        <FontAwesomeIcon icon={faCheck}/>
                    </div>
                </div>
            </div>
        )
    } else {
        return (
            <div className={"chatMessage received"}>
                <div>
                    {message.message}
                </div>
                <div className="hour-box">
                    <div className="hour">
                        {message.hour}
                    </div>
                </div>
            </div>
        )
    }
}

export default Message;