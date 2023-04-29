const socket = io();

const myFace = document.getElementById("myFace");
const muteBtn = document.getElementById("mute");
const cameraBtn = document.getElementById("camera");
const camerasSelect = document.getElementById("cameras");

let myStream;
let muted = false;
let cameraOff = false;

async function getCameras() {
    try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const cameras = devices.filter(devices => devices.kind === "videoinput");
        const currentCamera = myStream.getVideoTracks() [0];
        cameras.forEach(camera => {
            const option = document.createElement("option");
            option.value = camera.deviceId;
            option.textContent = camera.label;
            if(currentCamera.lable === camera.label) {
                option.selected = true;
            }
            camerasSelect.appendChild(option);
        });
    } catch(error) {
        console.log(error);
    }
}

async function getMedia(deviceId) {
    const initialConstranins = {
        audio: true,
        video: { facinMode: "user" },
    };
    
    const cameraConstraints = {
        audio: true,
        video: { deviceId: { exact: deviceId } },
    };

    try {
        myStream = await navigator.mediaDevices.getUserMedia(
            deviceId ? cameraConstraints : initialConstranins
        );
        myFace.srcObject = myStream;
        if(!deviceId) {
            await getCameras();
        }
    } catch (error) {
        console.log(error);
    }
}

getMedia();

function handleMuteClick() {
    myStream
    .getAudioTracks()
    .forEach((track) => (track.enabled = !track.enabled));
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
    myStream
    .getVideoTracks()
    .forEach((track) => (track.enabled = !track.enabled));
    if(cameraOff) {
        cameraBtn.textContent = "카메라 끄기";
        cameraOff = false;
    }
    else {
        cameraBtn.textContent = "카메라 켜기";
        cameraOff = true;
    }
}

async function handleCameraChange() {
    await getMedia(camerasSelect.value);
}

muteBtn.addEventListener("click", handleMuteClick);
cameraBtn.addEventListener("click", handleCameraClick);
camerasSelect.addEventListener("input", handleCameraChange);