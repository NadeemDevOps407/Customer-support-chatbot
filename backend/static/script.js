async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  addMessage("You", message, "user");
  input.value = "";

  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  const data = await response.json();
  addMessage("Bot", data.reply, "bot");
}

function addMessage(sender, text, cls) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("p");
  msg.className = `message ${cls}`;
  msg.innerHTML = `<b>${sender}:</b> ${text}`;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const audioPlayer = document.getElementById("recorded-audio");

startBtn.onclick = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);

  mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
  mediaRecorder.start();

  startBtn.disabled = true;
  stopBtn.disabled = false;
  console.log("Recording started...");
};

stopBtn.onclick = () => {
  mediaRecorder.onstop = async () => {
    const blob = new Blob(audioChunks, { type: 'audio/wav' });
    audioChunks = [];

    // play audio locally
    const url = URL.createObjectURL(blob);
    audioPlayer.src = url;

    // send audio to backend
    const formData = new FormData();
    formData.append("audio", blob, "voice.wav");

    const response = await fetch("/voice", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    console.log("Backend reply:", data.reply);
    alert("Bot reply: " + data.reply);
  };

  mediaRecorder.stop();
  startBtn.disabled = false;
  stopBtn.disabled = true;
};