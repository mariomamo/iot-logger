import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCheck } from '@fortawesome/free-solid-svg-icons'
import './message.css';


const Message = ({message, isSended})=> {
    if (isSended) {
        return (
            <div className={"chatRow sentDiv"}>
                <div className="chatMessage">
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
            </div>
        )
    } else {
        return (
            <div className={"chatRow receivedDiv"}>
                <div className="chatMessage">
                <div>
                    {message.message}
                </div>
                <div className="hour-box">
                    <div className="hour">
                        {message.hour}
                    </div>
                </div>
                </div>
            </div>
        )
    }
}

export default Message;