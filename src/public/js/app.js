const socket = io();

const myFace = document.getElementById("myFace");
const muteBtn = document.getElementById("mute");
const cameraBtn = document.getElementById("camera");

let myStream;
let muted = false;
let cameraOff = false;

async function getMedia() {
    try {
        myStream = await navigator.mediaDevices.getUserMedia({
            audio: true,
            video: true,
        });
        myFace.srcObject = myStream;
    } catch (error) {
        console.log(error);
    }
}

getMedia();

function handleMuteClick() {
    myStream
    .getAudioTracks()
    .forEach((track) => (track.enable = !track.enabled));
    if (!muted) {
        muteBtn.textContent = "음소거 해제";
        muted = true;
    }
    else {
        muteBtn.textContent = "음소거";
        muted = false;
    }
}

function handleCameraClick() {
    console.log(myStream.getVideoTracks());
    if(cameraOff) {
        cameraBtn.textContent = "카메라 끄기";
        cameraOff = false;
    }
    else {
        cameraBtn.textContent = "카메라 켜기";
        cameraOff = true;
    }
}

muteBtn.addEventListener("click", handleMuteClick);
cameraBtn.addEventListener("click", handleCameraClick);