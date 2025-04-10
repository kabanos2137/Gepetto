let createAssistantOwnImage = false;

class appSettingsBar {
    static logoffEventListener(event) {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        localStorage.removeItem("password");

        swup.navigate("/");
    }

    static expandEventListener(event) {
        document.getElementById("app-content").classList.toggle("blurred");
        document.getElementById("app-settings-bar").classList.toggle("expanded");
    }

    static addEventListeners() {
        document.getElementById("app-settings-bar-home").addEventListener("click", (event) => {
            swup.navigate("/app");
        });

        document.getElementById("app-settings-bar-logoff").addEventListener("click", (event) => {
            this.logoffEventListener(event);
        });

        document.getElementById("app-settings-bar-expand").addEventListener("click", (event) => {
            this.expandEventListener(event);
        })

        document.getElementById("app-settings-bar-logoff-p").addEventListener("click", (event) => {
            this.logoffEventListener(event);
        });
    }
}

class appPage {
    static getAssistants() {
        let appContent = document.getElementById("app-content");
        appContent.style.justifyContent = "center"
        fetch(`/api/assistant`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken,
                "Authorization": `Token ${localStorage.getItem("token")}`
            },
        })
            .then((res) => {
                if(res.ok === false){
                    res.json().then(res => {
                        handleError(res.action);
                    });
                }else{
                    return res.json();
                }
            })
            .then(res => {
                if(res.assistants && res.assistants.length > 0) {
                    let assistants = res.assistants;
                    appContent.style.justifyContent = "flex-start"

                    appContent.innerHTML = `
                        <h1>Your assistants</h1>
                    `;

                    assistants.forEach(assistant => {
                        appContent.innerHTML += `
                            <div class="app-content-assistant">
                                <img src="${assistant.profile_picture}">
                                <div>
                                    <h3 onclick="swup.navigate('/assistant?id=${assistant.id}')">${assistant.name}</h3>
                                    <h4>${assistant.description}</h4>
                                </div>
                            </div>
                        `
                    });

                    appContent.innerHTML += `<button id="app-content-create-new-conversation">Create new conversation</button>`

                    document.getElementById("app-content-create-new-conversation").addEventListener("click", (event) => {
                        this.contentCreateAssistantEventListener(event);
                    })
                } else {
                    appContent.style.justifyContent = "center"

                    appContent.innerHTML = `
                        <h1>Gepetto</h1>
                        <h2>Hmm, it's a bit empty here, isn't it? Maybe <u id="app-content-create-assistant">let's create your first assistant?</u></h2>
                    `;

                    document.getElementById("app-content-create-assistant").addEventListener("click", (event) => {
                        this.contentCreateAssistantEventListener(event);
                    })
                }
            })
    }

    static contentCreateAssistantEventListener(event) {
        swup.navigate("/create-assistant");
    }

    static addEventListeners() {
        this.getAssistants();
    }
}

class createAssistantPage {
    static nameEventListener(event) {
        if(!createAssistantOwnImage){
            const canvas = document.getElementById("create-assistant-form-profile-picture-generator");
            const ctx = canvas.getContext("2d");
            const diameter = 150;
            const letter = event.target.value ? event.target.value[0].toUpperCase() : "";

            ctx.beginPath();
            ctx.arc(diameter / 2, diameter / 2, diameter / 2, 0, Math.PI * 2);
            ctx.fillStyle = "#707070";
            ctx.fill();
            ctx.closePath();

            ctx.font = "70px Jura";
            ctx.fillStyle = "#D9D9D9";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(letter, diameter / 2, diameter / 2);

            document.getElementById("create-assistant-form-profile-picture").src = canvas.toDataURL("image/png");
        }
    }

    static errorDisplay(errorMSG) {
        let error = document.getElementById("create-assistant-error");

        error.innerHTML = errorMSG;
        error.className = "";
    }

    static createEventListener(event) {
        let form = new FormData(document.forms['create-assistant-form']);
        let canvas = document.getElementById("create-assistant-form-profile-picture-generator")

        let name = form.get("name");
        let description = form.get("description");
        let responseStyle = form.get("response-style");
        let tone = form.get("tone");
        let profilePicture = canvas.toDataURL("image/png");

        if(name === "" || description === "" || responseStyle === "" || tone === "") {
            this.errorDisplay("Please fill in all fields");
            return;
        }

        fetch("/api/assistant", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken,
                "Authorization": `Token ${localStorage.getItem("token")}`
            },
            body: JSON.stringify({
                assistant_name: name,
                description: description,
                response_style: responseStyle,
                tone: tone,
                profile_picture: profilePicture
            })
        })
            .then((res) => {
                if(res.ok === false){
                    res.json().then(res => {
                        handleError(res.action);
                    });
                }else{
                    return res.json();
                }
            })
            .then(res => {
                swup.navigate(`/assistant?id=${res.assistant_id}`);
            })
    }

    static addEventListeners() {
        createAssistantOwnImage = false;

        document.getElementById("create-assistant-form-name").addEventListener("input", (event) => {
            this.nameEventListener(event);
        });

        document.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                createAssistantPage.createEventListener(event);
            }
        });

        document.getElementById("create-assistant-submit").addEventListener("click", (event) => {
            this.createEventListener(event);
        })
    }
}

class assistantPage {
    static createConversationEventListener(event) {
        fetch("/api/conversation", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken,
                "Authorization": `Token ${localStorage.getItem("token")}`
            },
            body: JSON.stringify({
                conversation_name: "New conversation",
                assistant_id: new URLSearchParams(window.location.search).get("id"),
            })
        })
            .then(async (res) => {
                if(res.ok === false){
                    res.json().then(res => {
                        handleError(res.action);
                    });
                }else{
                    return res.json();
                }
            })
            .then(res => {
                swup.navigate(`/conversation?id=${res.conversation_id}`)
            })
    }

    static getAssistant() {
        const params = new URLSearchParams(window.location.search);

        let assistantID = params.get("id");

        let appContent = document.getElementById("app-content");
        appContent.style.justifyContent = "center"

        fetch(`/api/assistant?assistant_id=${assistantID}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken,
                "Authorization": `Token ${localStorage.getItem("token")}`
            },
        })
            .then((res) => {
                if(res.ok === false){
                    res.json().then(res => {
                        handleError(res.action);
                    });
                }else{
                    return res.json();
                }
            })
            .then(res => {
                appContent.style.justifyContent = "flex-start"

                appContent.innerHTML = `
                    <div id="assistant-header">
                        <img src="${res.profile_picture}">
                        <h1>${res.assistant_name}</h1>
                    </div>
                    <div id="assistant-info">
                        <h2>Description</h2>
                        <p>${res.description}</p>
                        <h2>Response style</h2>
                        <p>${res.response_style}</p>
                        <h2>Tone</h2>
                        <p>${res.tone}</p>
                    </div>
                    <div id="assistant-content">
                        <h1>Conversations</h1>
                        <p>Loading...</p>
                    </div>
                `

                fetch(`/api/conversation?assistant_id=${assistantID}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrftoken,
                        "Authorization": `Token ${localStorage.getItem("token")}`
                    }
                })
                    .then((res) => {
                        if(res.ok === false){
                            res.json().then(res => {
                                handleError(res.action);
                            });
                        }else{
                            return res.json();
                        }
                    })
                    .then(res => {
                        if(res.conversations.length === 0){
                            document.querySelector("#assistant-content > p").innerHTML = "You two haven't talked yet. <u id=\"assistant-content-create-conversation\">Maybe it's a good time to do it?</u>"
                            document.getElementById("assistant-content-create-conversation").addEventListener("click", (event) => {
                                this.createConversationEventListener(event);
                            });
                        }else{
                            document.querySelector("#assistant-content > p").remove();

                            let assistantContent = document.getElementById("assistant-content");

                            res.conversations.forEach(conversation => {
                                let date = new Date(conversation.date_of_creation)

                                const formatted = date.toLocaleString("en-GB", {
                                    day: "2-digit",
                                    month: "long",
                                    year: "numeric",
                                    hour: "2-digit",
                                    minute: "2-digit",
                                });

                                assistantContent.innerHTML += `
                                    <div class="assistant-content-conversation">
                                        <h1 onclick="swup.navigate('/conversation?id=${conversation.id}')">${conversation.name}</h1>
                                        <h3>${formatted}</h3>
                                    </div>
                                `
                            });

                            assistantContent.innerHTML += `<button id="assistant-content-create-new-conversation">Create new conversation</button>`

                            document.getElementById("assistant-content-create-new-conversation").addEventListener("click", (event) => {
                                this.createConversationEventListener();
                            })
                        }
                    })
            })
    }

    static addEventListeners() {
        this.getAssistant();
    }
}

class conversationPage {
    static sendMessageEvent(event) {
        const params = new URLSearchParams(window.location.search);

        let conversationID = params.get("id");

        let messageInput= document.getElementById("conversation-input-message");
        let message = messageInput.value;
        messageInput.value = "";

        let messageDiv = document.getElementById("conversation-messages");
        messageDiv.innerHTML = `
            <div class="inner-message">
                <p class="message-source">From: you</p>
                <p class="message-content">${message}</p>
            </div>
        ` + messageDiv.innerHTML

        fetch("/api/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken,
                "Authorization": `Token ${localStorage.getItem("token")}`
            },
            body: JSON.stringify({
                message: message,
                conversation_id: conversationID,
            })
        })
            .then(async (res) => {
                if(res.ok === false){
                    res.json().then(res => {
                        handleError(res.action);
                    });
                }else{
                    return res.json();
                }
            })
            .then(res => {
                messageDiv.innerHTML = `
                    <div class="outer-message">
                        <p class="message-source">From: assistant</p>
                        <p class="message-content">${res.message}</p>
                    </div>
                ` + messageDiv.innerHTML
            });
    }

    static loadConversation() {
        let appContent = document.getElementById("app-content");
        appContent.style.justifyContent = "center";

        const params = new URLSearchParams(window.location.search);

        let conversationID = params.get("id");

        fetch(`/api/conversation?conversation_id=${conversationID}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken,
                "Authorization": `Token ${localStorage.getItem("token")}`
            }
        })
            .then((res) => {
                if(res.ok === false){
                    res.json().then(res => {
                        handleError(res.action);
                    });
                }else{
                    return res.json();
                }
            })
            .then(res => {
                let date = new Date(res.date_of_creation)

                const formatted = date.toLocaleString("en-GB", {
                    day: "2-digit",
                    month: "long",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                });

                appContent.style.justifyContent = "space-between";
                appContent.innerHTML = `
                    <div id="conversation-header">
                        <h1>${res.conversation_name}</h1>
                        <h2 onclick="swup.navigate('/assistant?id=${res.assistant_id}')">${res.assistant_name}</h2>
                        <h3>${formatted}</h3>
                    </div>
                    <div id="conversation-messages">
                    </div>
                    <div id="conversation-input">
                        <input type="text" id="conversation-input-message"/>
                        <div id="conversation-input-message-send">
                            <i id="conversation-input-send" class="fa-solid fa-paper-plane"></i>
                        </div>
                    </div>
                `

                let messagesDiv = document.getElementById("conversation-messages");

                res.messages.forEach(message => {
                    if(message.sent_by === 0){
                        messagesDiv.innerHTML = `
                            <div class="outer-message">
                                <p class="message-source">From: assistant</p>
                                <p class="message-content">${message.message}</p>
                            </div>
                        ` + messagesDiv.innerHTML;
                    }else{
                        messagesDiv.innerHTML = `
                            <div class="inner-message">
                                <p class="message-source">From: you</p>
                                <p class="message-content">${message.message}</p>
                            </div>
                        ` + messagesDiv.innerHTML;
                    }
                })

                document.getElementById("conversation-input-send").addEventListener("click", (event) => {
                    this.sendMessageEvent(event)
                })

                document.getElementById("conversation-input-message").addEventListener('keypress', function(event) {
                    if (event.key === 'Enter') {
                        event.preventDefault();
                        conversationPage.sendMessageEvent(event);
                    }
                });
            });
    }

    static addEventListeners() {
        this.loadConversation();
    }
}