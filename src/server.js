import express from "express";

const app = express();

app.set("view engine", "pug");
app.set("views", __dirname + "/views");
app.use("/public", express.static(__dirname + "/public")); // 폴더를 유저에게 공개
app.get("/", (req, res) => res.render("home")); // 홈페이지로 이동 시 사용될 템플릿을 렌더

const handleListen = () => console.log('listening on http://localhost:3000');
app.listen(3000, handleListen);