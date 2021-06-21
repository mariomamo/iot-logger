import React, { useState, useEffect} from 'react';
import ChatBox from './chatBox/chatbox';
import Sidebar from './sidebar/sidebar';
import socketio from "socket.io-client";
import './chat.css';

const Chat = ()=> {
    const [selectedChat, setSelectedChat] = useState({});
    const [chatsList, setChatsList] = useState([]);
    const [client, setClient] = useState(null);
    const [url] = useState("http://127.0.0.1");
    const [port] = useState(5000);

    useEffect(() => {
        console.log(chatsList);
    }, [chatsList])

    useEffect(()=> {
        if (client !== null) {
            client.on("connect", ()=> {
                console.log("Connected!");
            });

            client.on("message", (message)=> {
                message = JSON.parse(message);
                console.log(chatsList, "-", message.data.chatId);
                if (contains(chatsList, message.data.chatId)) {
                    let newMessage = getChatFromList(chatsList, message.data.chatId);
                    newMessage.messages.push(message.data.payload)
                } else {
                    chatsList.push(getTNewChatTemplate(message.data, false));
                }
                setChatsList([...chatsList]);
            });
        }
    }, [client]);

    useEffect(() => {
        setClient(socketio.connect(url + ":" + port));

        // setChatsList([
        //     {
        //         chatId: "1",
        //         name: "Mario Offertucci",
        //         lastMessage: "Ciao, come va?",
        //         ora: "20:00",
        //         selected: false,
        //         messages: [
        //             {
        //                 type: "text",
        //                 isSended: true,
        //                 message: "Turn on the lights",
        //                 ora: "20:00"
        //             },
        //             {
        //                 type: "text",
        //                 isSended: false,
        //                 message: "I turned on the lights",
        //                 ora: "20:00"
        //             }
        //         ]
        //     },
        //     {
        //         chatId: "2",
        //         name: "Francesco Totti",
        //         lastMessage: "Aridaje",
        //         ora: "20:30",
        //         selected: false,
        //         messages: [
        //             {
        //                 type: "text",
        //                 isSended: false,
        //                 message: "My battery is low!",
        //                 ora: "20:00"
        //             },
        //             {
        //                 type: "text",
        //                 isSended: true,
        //                 message: "Shutdown",
        //                 ora: "20:00"
        //             }
        //         ]
        //     },
        //     {
        //         chatId: "3",
        //         name: "Antonio Donnarumma",
        //         lastMessage: "Non sono il portiere del Milan",
        //         ora: "20:35",
        //         selected: false,
        //         messages: [
        //             {
        //                 type: "text",
        //                 isSended: false,
        //                 message: "Ma che vuoi",
        //                 ora: "20:00"
        //             }
        //         ]
        //     },
        //     {
        //         chatId: "4",
        //         name: "Tizio strano",
        //         lastMessage: "E da me che voi",
        //         ora: "20:35",
        //         selected: false
        //     }
        // ]);
    }, []);

    const getPayloadMessage = (type, isSended, message, ora) => {
        return {
            type: type,
            isSended: isSended,
            message: message,
            ora: ora
        }
    }

    const getTNewChatTemplate = (message, isSended) => {
        console.log("MSG: ", message);
        let payload = getPayloadMessage(message.payload.type, isSended, message.payload.message, message.ora);

        return {
            chatId: message.chatId.toString(),
            name: message.name,
            ora: message.ora,
            lastMessage: message.payload.message,
            selected: false,
            messages: [payload],
            img: message.img
        }
    }
    
    const contains = (list, element) => {
        return list.some(arrayElement => arrayElement.chatId == element)
    }

    const getChatFromList = (list, id) => {
        return list.filter(elemento => elemento.chatId == id)[0];
    }

    const handleClick = (chat)=> {
        setSelectedChat(chat);
    }

    const getMessageToSend = (chatId, msg, ora, type) => {
        return {
            chatId: chatId,
            ora: ora,
            payload: {
                type: type,
                message: msg
            }
        }
    }

    const onSend = (chatId, msg)=> {
        let currentChat = getChatFromList(chatsList, chatId);
        currentChat.messages.push(getPayloadMessage("text", true, msg, "00:59"));
        console.log("LOG: ", currentChat);
        setChatsList([...chatsList]);
        client.emit('message', getMessageToSend(chatId, msg, "00:59", "text"));
    }

    const renderElement = ()=> {
        if (selectedChat !== undefined && selectedChat.selected) {
            return <ChatBox onSend={onSend} chatId={selectedChat.chatId} name={selectedChat.name} messages={selectedChat.messages} />;
        } else {
            return <ChatBox onSend={onSend} chatId={selectedChat.chatId} name="Select a chat for read and send messages" />;
        }
    }

    return (
        <div className='chat'>
            <Sidebar chatsList={chatsList} onClick={handleClick}/>
            {renderElement()}
        </div>
    )
}

export default Chat;