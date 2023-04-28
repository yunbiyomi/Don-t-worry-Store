import http from "http";
import WebSocket from "ws";
import express from "express";
import { log } from "console";

const app = express();

app.set("view engine", "pug");
app.set("views", __dirname + "/views");
app.use("/public", express.static(__dirname + "/public")); // 폴더를 유저에게 공개
app.get("/", (req, res) => res.render("home")); // 홈페이지로 이동 시 사용될 템플릿을 렌더

const handleListen = () => console.log('listening on http://localhost:3000');

const server = http.createServer(app);
const wss = new WebSocket.Server({server}); // HTTP 서버, webSoket 서버 둘다 가능

const sockets = [];

wss.on("connection", (socket) => {
    sockets.push(socket);
    console.log("브라우저에 연결되었습니다.");
    socket.on("close", () => console.log("브라우저와의 연결이 끊어졌습니다."));
    socket.on("message", (message) => {
        sockets.forEach(aSocket => aSocket.send(message.toString("utf-8")));
    })
})

server.listen(3000, handleListen);