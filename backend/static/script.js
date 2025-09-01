// async function sendMessage() {
//   const input = document.getElementById("user-input");
//   const message = input.value.trim();
//   if (!message) return;

//   addMessage("You", message, "user");
//   input.value = "";

//   const response = await fetch("/chat", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ message })
//   });

//   const data = await response.json();
//   addMessage("Bot", data.reply, "bot");
// }

// function addMessage(sender, text, cls) {
//   const chatBox = document.getElementById("chat-box");
//   const msg = document.createElement("p");
//   msg.className = `message ${cls}`;
//   msg.innerHTML = `<b>${sender}:</b> ${text}`;
//   chatBox.appendChild(msg);
//   chatBox.scrollTop = chatBox.scrollHeight;
// }

// let mediaRecorder;
// let audioChunks = [];

// const startBtn = document.getElementById("start-btn");
// const stopBtn = document.getElementById("stop-btn");
// const audioPlayer = document.getElementById("recorded-audio");

// startBtn.onclick = async () => {
//   const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//   mediaRecorder = new MediaRecorder(stream);

//   mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
//   mediaRecorder.start();

//   startBtn.disabled = true;
//   stopBtn.disabled = false;
//   console.log("Recording started...");
// };

// stopBtn.onclick = () => {
//   mediaRecorder.onstop = async () => {
//     const blob = new Blob(audioChunks, { type: 'audio/wav' });
//     audioChunks = [];

//     // play audio locally
//     const url = URL.createObjectURL(blob);
//     audioPlayer.src = url;

//     // send audio to backend
//     const formData = new FormData();
//     formData.append("audio", blob, "voice.wav");

//     const response = await fetch("/voice", {
//       method: "POST",
//       body: formData
//     });

//     const data = await response.json();
//     console.log("Backend reply:", data.reply);
//     alert("Bot reply: " + data.reply);
//   };

//   mediaRecorder.stop();
//   startBtn.disabled = false;
//   stopBtn.disabled = true;
// };

// Toggle chat visibility
// Toggle chat visibility
// document.getElementById("chat-toggle").onclick = () => {
//   document.getElementById("chat-box").classList.toggle("hidden");
// };

// document.getElementById("close-chat").onclick = () => {
//   document.getElementById("chat-box").classList.add("hidden");
// };

// // Append messages
// function appendMessage(sender, text) {
//   const chatMessages = document.getElementById("chat-messages");
//   const msg = document.createElement("div");
//   msg.classList.add("message", sender === "user" ? "user-message" : "bot-message");
//   msg.textContent = text;
//   chatMessages.appendChild(msg);
//   chatMessages.scrollTop = chatMessages.scrollHeight;
// }

// // Send message
// function sendMessage() {
//   const input = document.getElementById("user-input");
//   const text = input.value.trim();
//   if (!text) return;

//   appendMessage("user", text);
//   input.value = "";

//   // Fake bot reply
//   setTimeout(() => {
//     appendMessage("bot", "Hello! Thanks for reaching out. How can I help you today?");
//   }, 800);
// }


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

    const startBtn = document.getElementById("start-button");
    const stopBtn = document.getElementById("stop-button");
    const audioPlayer = document.getElementById("recorded-audio");

    startBtn.onclick = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = e => {
          if (e.data.size > 0) {
            audioChunks.push(e.data);
          }
        };
        
        mediaRecorder.onstop = async () => {
          const blob = new Blob(audioChunks, { type: 'audio/wav' });
          audioChunks = [];

          // send audio to backend
          const formData = new FormData();
          formData.append("audio", blob, "voice.wav");

          try {
            const response = await fetch("/voice", {
              method: "POST",
              body: formData
            });

            if (response.ok) {
              const audioBlob = await response.blob();
              const audioURL = URL.createObjectURL(audioBlob);
              audioPlayer.src = audioURL;
              audioPlayer.play();
            } else {
              console.error("Server error:", response.status);
              alert("Failed to get bot audio response.");
            }
          } catch (error) {
            console.error("Error sending audio:", error);
            alert("Failed to get bot audio response.");
          }
        };

        mediaRecorder.start();
        startBtn.disabled = true;
        stopBtn.disabled = false;
        console.log("Recording started...");
        
      } catch (error) {
        console.error("Error accessing microphone:", error);
        alert("Cannot access microphone. Please check permissions.");
      }
    };

    stopBtn.onclick = () => {
      if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        startBtn.disabled = false;
        stopBtn.disabled = true;
        console.log("Recording stopped...");
      }
    };

    // Optional: Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.key === ' ' && !startBtn.disabled) {
        e.preventDefault();
        startBtn.click();
      } else if (e.key === 'Escape' && !stopBtn.disabled) {
        stopBtn.click();
      }
    });

    // Function to send text message (you might already have this)
    function sendMessage() {
      const userInput = document.getElementById("user-input");
      const message = userInput.value.trim();
      
      if (message) {
        // Add your message sending logic here
        console.log("Sending message:", message);
        userInput.value = "";
      }
    }

    // Allow pressing Enter to send message
    document.getElementById("user-input").addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        sendMessage();
      }
    });

