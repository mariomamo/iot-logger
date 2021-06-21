import React, { useEffect, useState } from 'react';
import MessageChatBox from './messageChatBox/messagechatbox';
import SearchBar from './searchBar/searchbar';
import './sidebar.css';

const Sidebar = ({onClick, chatsList})=> {
    const [messagesMap, setMessagesMap] = useState();
    
    useEffect(() => {
        // setChatsList(chatsList);
        // JSON.stringify(Array.from(chatMap.entries()))
        
        // let iterator = chatMap.keys();
        // let next;
        // let tempList = [];

        // console.log("M: ", chatMap);

        // for (let i = 0; i < chatMap.size; i++) {
        //     next = iterator.next();
        //     tempList.push(chatMap.get(next.value));
        //     console.log(tempList);
        //     console.log(next);
        //     console.log(chatMap.get(next.value));
        // }
    }, []);

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
            {/* {chatsList !== undefined && chatsList.map((message, index) => <MessageChatBox onClick={changeClick} key={index} id={message.chatId} messages={message.messages} name={message.name} lastMessage={message.lastMessage} ora={message.ora} selected={message.selected}/>)} */}
            {chatsList !== undefined && chatsList.map((message, index) => <MessageChatBox onClick={changeClick} key={index} id={message.chatId} messages={message.messages} name={message.name} lastMessage={message.lastMessage} ora={message.ora} selected={message.selected}/>)}
        </div>
    )
}

export default Sidebar;