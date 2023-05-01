import http from "http";
// import WebSocket from "ws";
import SocketIO from "socket.io"
import express from "express";

const app = express();

app.set("view engine", "pug");
app.set("views", __dirname + "/views");
app.use("/public", express.static(__dirname + "/public")); // 폴더를 유저에게 공개
app.get("/", (req, res) => res.render("home")); // 홈페이지로 이동 시 사용될 템플릿을 렌더

const httpServer = http.createServer(app);
const wsServer = SocketIO(httpServer);

wsServer.on("connection", (socket) => {
    console.log(socket);
})

// const wss = new WebSocket.Server({server}); // HTTP 서버, webSoket 서버 둘다 가능

// const sockets = [];

// wss.on("connection", (socket) => {
//     sockets.push(socket);
//     socket["nickname"] = "익명";
//     console.log("브라우저에 연결되었습니다.");
//     socket.on("close", () => console.log("브라우저와의 연결이 끊어졌습니다."));
//     socket.on("message", (msg) => {
//         const message = JSON.parse(msg);
//         switch (message.type) {
//             case "new_message":
//                 sockets.forEach((aSocket) =>
//                 aSocket.send(`${socket.nickname}: ${message.payload}`)
//                 );
//         case "nickname":
//             socket["nickname"] = message.payload;
//         }
//     });
// });

wsServer.on("connection", (socket) => {
    socket.on("join_room", (roomName) => {
        socket.join(roomName);
        socket.to(roomName).emit("welcome");
    });

    socket.on("offer", (offer, roomName) => {
        socket.to(roomName).emit("offer", offer);
    });
    socket.on("answer", (answer, roomName) => {
        socket.to(roomName).emit("answer", answer);
    })
    socket.on("ice", (ice, roomName) => {
        socket.to(roomName).emit("ice", ice);
    })
});

const handleListen = () => console.log('listening on http://localhost:3000');
httpServer.listen(3000, handleListen);