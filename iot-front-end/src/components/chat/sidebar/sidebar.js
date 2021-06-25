import React from 'react';
import MessageChatBox from './MessageChatBox/messagechatbox';
import SearchBar from './SearchBar/searchbar';
import './sidebar.css';

const Sidebar = ({onClick, chatsList})=> {
    const changeClick = (chatId)=> {
        let selectedMessage;
        chatsList.forEach(message => { 
            if (message.selected === true) {
                message.selected = false;
            } if (message.chatId === chatId) {
                message.selected = true;
                selectedMessage = message;
            }
        });
        onClick(selectedMessage);
    }

    return (
        <div className='sidebar'>
            <SearchBar />
            {chatsList !== undefined && chatsList.map((message, index) => <MessageChatBox onClick={changeClick} key={index} id={message.chatId} messages={message.messages} name={message.name} lastMessage={message.lastMessage} img={message.img} selected={message.selected}/>)}
        </div>
    )
}

export default Sidebar;