const messageList = document.querySelector("ul");
const nickNameForm = document.querySelector("#nickName");
const messageForm = document.querySelector("#message");
const socket =  new WebSocket(`ws://${window.location.host}`);

function makeMessage(type, payload){
    const msg = {type, payload};
    return JSON.stringify(msg);
}

socket.addEventListener("open", () => {
    console.log("서버와 연결되었습니다.");
})

socket.addEventListener("message", (message) => {
    const li = document.createElement("li");
    li.textContent = message.data;
    messageList.append(li);
})

socket.addEventListener("close", () => {
    console.log("서버와의 연결이 끊어졌습니다.");d
})

function handleSubmit(event) {
    event.preventDefault();
    const input = messageForm.querySelector("input");
    socket.send(makeMessage("new_message", input.value));
    const li = document.createElement("li");
    li.textContent = `You: ${input.value}`;
    messageList.append(li);
    input.value = "";
}

function handleNickSubmit(event) {
    event.preventDefault();
    const input = nickNameForm.querySelector("input");
    socket.send(makeMessage("nickname", input.value));
    input.value = "";
}

messageForm.addEventListener("submit", handleSubmit);
nickNameForm.addEventListener("submit", handleNickSubmit);