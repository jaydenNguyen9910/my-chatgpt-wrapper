// Copyright 2023 tringuyen
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import './style.css';
import React, { useState, useEffect, useRef } from "react";
import { Container, Navbar, Nav } from "react-bootstrap";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { useNavigate } from "react-router-dom";
import { logout } from "../login/LoginActions";
import axios from "axios";
import {  toastOnError } from "../../utils/Utils";


const Dashboard = (props) => {
    const navigate = useNavigate();
    const { user, isAuthenticated, token } = props.loginReducer;

    const [inputValue, setInputValue] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const chatBoxRef = useRef(null);

    const handleSendMessage = async () => {
        setIsLoading(true);
        const newMessage = { text: inputValue, isUser: true };
        setMessages([...messages, newMessage]);
        setInputValue('')

        axios.post("/chatgpt",
            {
                message: inputValue,
            },
            {
                "Accept": "text/event-stream",
                "Content-Type": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": `TOKEN ${token}`
            }
        ).then(response => {
            const data = response.data;
            const chatbotMessage = { text: data, isUser: false };
            setMessages([...messages, newMessage, chatbotMessage]);
        })
        .catch(error => {
            toastOnError(error);
            axios.post("/gpt3",
                {
                    message: inputValue,
                },
                {
                    "Accept": "text/event-stream",
                    "Content-Type": "application/json",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Authorization": `TOKEN ${token}`
                }
            ).then(response => {
                const data = response.data;
                const chatbotMessage = { text: data, isUser: false };
                setMessages([...messages, newMessage, chatbotMessage]);
            })
            .catch(error => toastOnError(error))
        })
        .finally(() => {
            setIsLoading(false);
        });

        // try {
        //     const response = await fetch('wrapper/', {
        //         method: 'POST',
        //         headers: {
        //         'Accept': 'text/event-stream',
        //         'Content-Type': 'application/json',
        //         'Accept-Language': 'en-US,en;q=0.9'
        //         },
        //         body: JSON.stringify({
        //         message: inputValue,
        //         conversation_id: conversationId,
        //         parent_message_id: parentMessageId
        //         })
        //     });
        //     const data = await response.json();
        //     const chatbotMessage = { text: data.message, isUser: false };

        //     setMessages([...messages, newMessage, chatbotMessage]);
        //     setConversationId(data.conversation_id);
        //     setParentMessageId(data.parent_message_id);
        // } catch (error) {
        //     console.error(error);
        // } finally {
        //     setIsLoading(false);
        // }
    };

    useEffect(() => {
        chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
      }, [messages]);

    useEffect(() => {
        if (!isAuthenticated) {
          navigate('/login');
        }
    }, [isAuthenticated]);

    return (
        <div>
            <Navbar style={{"background-color": "lightgray"}}>
                <Navbar.Text style={{"padding-left": 10}}>
                    User: <b>{user.username}</b>
                </Navbar.Text>
                <Navbar.Toggle />
                <Navbar.Collapse className="justify-content-end" style={{"padding-right": 10}}>
                    <Nav.Link onClick={props.logout}>Logout</Nav.Link>
                </Navbar.Collapse>
            </Navbar>
            <Container>
            <div className="chat-wrapper">
                <h1>Welcome to ChatGPT Wrapper!</h1>
                <div className="chat-box" ref={chatBoxRef}>
                    {messages.map((message, index) => (
                    <div key={index} className={`${message.isUser ? 'user' : 'chatgpt'}-message-container`}>
                        <div className={`${message.isUser ? 'user' : 'chatgpt'}-message`}>
                        {message.text}
                        </div>
                    </div>
                    ))}
                </div>
                <div className="chat-input">
                    <input
                        className="input-field"
                        type="text"
                        placeholder="Type your message here..."
                        value={inputValue}
                        onChange={e => setInputValue(e.target.value)}
                    />
                    <button className="send-button" onClick={handleSendMessage} disabled={isLoading}>
                        {isLoading ? 'Sending...' : 'Send'}
                    </button>
                </div>
                {isLoading && (
                    <div className="loading-spinner">
                    <div className="spinner"></div>
                    </div>
                )}
                </div>
            </Container>
        </div>
    );
};

Dashboard.propTypes = {
    loginReducer: PropTypes.object.isRequired,
    logout: PropTypes.func.isRequired
};

const mapStateToProps = state => ({
    loginReducer: state.loginReducer
});

function mapDispatchToProps(dispatch) {
    return {
      logout: () => dispatch(logout()),
    };
  }

export default connect(mapStateToProps, mapDispatchToProps)(Dashboard);