import React from 'react';
import { Input, Button } from 'antd';
import './replaybar.css';
import 'antd/dist/antd.css';

const ReplayBar = ()=> {
    return (
        <div className="replyBar">			
			<input type="text" className="textArea" placeholder="Type your message..." cols="40" rows="5" />
            <Button className="sendButton" type="primary">Send</Button>
		</div>
    )
}

export default ReplayBar;