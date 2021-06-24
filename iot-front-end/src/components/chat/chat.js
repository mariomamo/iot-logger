import React, { useState, useEffect} from 'react';
import ChatBox from './chatBox/chatbox';
import Sidebar from './sidebar/sidebar';
import socketio from "socket.io-client";
import './chat.css';
import SplashBox from './splashBox/splashbox';

const Chat = ()=> {
    const [selectedChat, setSelectedChat] = useState({});
    const [chatsList, setChatsList] = useState([]);
    const [client, setClient] = useState(null);
    const [url] = useState("http://127.0.0.1");
    const [port] = useState(5000);

    // useEffect(() => {
    //     console.log(chatsList);
    // }, [chatsList])

    useEffect(()=> {
        if (client !== null) {
            client.on("connect", ()=> {
                console.log("Connected!");
            });

            client.on("message", (message)=> {
                if (contains(chatsList, message.data.chatId)) {
                    updateExistingMessage(getChatFromList, chatsList, message);
                } else {
                    addNewMessage(message);
                }
                setChatsList([...chatsList]);
            });
        }
    }, [client]);

    useEffect(() => {
        setClient(socketio.connect(url + ":" + port));

        setChatsList([
            {
                sensorType: "car",
                chatId: "1",
                name: "Car",
                img: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Circle-icons-car.svg/1200px-Circle-icons-car.svg.png",
                lastMessage: {
                    hour: "20:00",
                    type: "text",
                    isSended: false,
                    message: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit, tenetur error, harum nesciunt ipsum debitis quas aliquid. Reprehenderit, quia. Quo neque error repudiandae fuga? Ipsa laudantium molestias eos sapiente officiis modi at sunt excepturi expedita sint? Sed quibusdam recusandae alias error harum maxime adipisci amet laborum. Perspiciatis minima nesciunt dolorem! Officiis iure rerum voluptates a cumque velit quibusdam sed amet tempora. Sit laborum ab, eius fugit doloribus tenetur fugiat, temporibus enim commodi iusto libero magni deleniti quod quam consequuntur! Commodi minima excepturi repudiandae velit hic maxime doloremque. Quaerat provident commodi consectetur veniam similique ad earum omnis ipsum saepe, voluptas, hic voluptates pariatur est explicabo fugiat, dolorum eligendi quam cupiditate excepturi mollitia maiores labore suscipit quas? Nulla, placeat. Voluptatem quaerat non architecto ab laudantium modi minima sunt esse temporibus sint culpa, recusandae aliquam numquam totam ratione voluptas quod exercitationem fuga. Possimus quis earum veniam quasi aliquam eligendi, placeat qui corporis!"
                },
                selected: false,
                messages: [
                    {
                        hour: "20:00",
                        type: "text",
                        isSended: true,
                        message: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit, tenetur error, harum nesciunt ipsum debitis quas aliquid. Reprehenderit, quia. Quo neque error repudiandae fuga? Ipsa laudantium molestias eos sapiente officiis modi at sunt excepturi expedita sint? Sed quibusdam recusandae alias error harum maxime adipisci amet laborum. Perspiciatis minima nesciunt dolorem! Officiis iure rerum voluptates a cumque velit quibusdam sed amet tempora. Sit laborum ab, eius fugit doloribus tenetur fugiat, temporibus enim commodi iusto libero magni deleniti quod quam consequuntur! Commodi minima excepturi repudiandae velit hic maxime doloremque. Quaerat provident commodi consectetur veniam similique ad earum omnis ipsum saepe, voluptas, hic voluptates pariatur est explicabo fugiat, dolorum eligendi quam cupiditate excepturi mollitia maiores labore suscipit quas? Nulla, placeat. Voluptatem quaerat non architecto ab laudantium modi minima sunt esse temporibus sint culpa, recusandae aliquam numquam totam ratione voluptas quod exercitationem fuga. Possimus quis earum veniam quasi aliquam eligendi, placeat qui corporis!"
                    },
                    {
                        hour: "20:00",
                        type: "text",
                        isSended: false,
                        message: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit, tenetur error, harum nesciunt ipsum debitis quas aliquid. Reprehenderit, quia. Quo neque error repudiandae fuga? Ipsa laudantium molestias eos sapiente officiis modi at sunt excepturi expedita sint? Sed quibusdam recusandae alias error harum maxime adipisci amet laborum. Perspiciatis minima nesciunt dolorem! Officiis iure rerum voluptates a cumque velit quibusdam sed amet tempora. Sit laborum ab, eius fugit doloribus tenetur fugiat, temporibus enim commodi iusto libero magni deleniti quod quam consequuntur! Commodi minima excepturi repudiandae velit hic maxime doloremque. Quaerat provident commodi consectetur veniam similique ad earum omnis ipsum saepe, voluptas, hic voluptates pariatur est explicabo fugiat, dolorum eligendi quam cupiditate excepturi mollitia maiores labore suscipit quas? Nulla, placeat. Voluptatem quaerat non architecto ab laudantium modi minima sunt esse temporibus sint culpa, recusandae aliquam numquam totam ratione voluptas quod exercitationem fuga. Possimus quis earum veniam quasi aliquam eligendi, placeat qui corporis!"
                    }
                ]
            }
        ]);
    }, []);

    const addNewMessage = (message)=> {
        chatsList.push(getTNewChatTemplate(message.data, false));
    }

    const updateExistingMessage = (getChatFromList, chatsList, message) => {
        let existingMessage = getChatFromList(chatsList, message.data.chatId);
        message.data.payload.isSended = false;
        existingMessage.lastMessage = message.data.payload;
        existingMessage.messages.push(message.data.payload);
    }

    const getPayloadMessage = (type, isSended, message, hour) => {
        return {
            hour: hour,
            type: type,
            isSended: isSended,
            message: message
        }
    }

    const getTNewChatTemplate = (message, isSended) => {
        let payload = getPayloadMessage(message.payload.type, isSended, message.payload.message, message.payload.hour);

        return {
            sensorType: message.sensorType,
            chatId: message.chatId.toString(),
            name: message.name,
            img: message.img,
            lastMessage: payload,
            selected: false,
            messages: [payload]
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

    const getMessageToSend = (chatId, msg, hour, type) => {
        return {
            chatId: chatId,
            payload: {
                hour: hour,
                type: type,
                message: msg
            }
        }
    }

    const onSend = (chatId, msg)=> {
        let currentChat = getChatFromList(chatsList, chatId);
        currentChat.messages.push(getPayloadMessage("text", true, msg, "00:59"));
        setChatsList([...chatsList]);
        client.emit('message', getMessageToSend(chatId, msg, "00:59", "text"));
    }

    const renderElement = ()=> {
        if (selectedChat !== undefined && selectedChat.selected) {
            return <ChatBox sensorType={selectedChat.sensorType} onSend={onSend} chatId={selectedChat.chatId} name={selectedChat.name} messages={selectedChat.messages} />;
        } else {
            return <SplashBox />
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