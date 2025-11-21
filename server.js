const express = require("express");
const bodyParser = require("body-parser");
const { spawn } = require("child_process");

const app = express();
app.use(bodyParser.json());

// Khởi động Python process một lần và giữ nó chạy
let pyProcess = null;
let pendingRequests = [];
let isModelReady = false;

function startPythonProcess() {
  console.log("Starting Python process...");
  pyProcess = spawn("python", ["classify_server.py"]);

  let buffer = "";
  pyProcess.stdout.on("data", (data) => {
    buffer += data.toString();
    const lines = buffer.split("\n");
    buffer = lines.pop(); // Giữ dòng chưa hoàn chỉnh

    lines.forEach((line) => {
      if (line.trim()) {
        try {
          const result = JSON.parse(line);
          // Lấy request đầu tiên trong hàng đợi
          const handler = pendingRequests.shift();
          if (handler) {
            handler(result);
          }
        } catch (e) {
          console.error("JSON parse error:", e);
        }
      }
    });
  });

  pyProcess.stderr.on("data", (data) => {
    const message = data.toString();
    console.log(`Python: ${message}`);

    // Kiểm tra xem model đã load xong chưa
    if (message.includes("Model loaded!")) {
      isModelReady = true;
      console.log("Model is ready!");
    }
  });

  pyProcess.on("close", (code) => {
    console.log(`Python process exited with code ${code}`);
    pyProcess = null;
    isModelReady = false;
  });
}

app.post("/classify", (req, res) => {
  const { text } = req.body;
  if (!text) return res.status(400).json({ error: "Missing text" });

  if (!pyProcess) {
    return res
      .status(503)
      .json({ error: "Model is starting, please retry in a few seconds" });
  }

  if (!isModelReady) {
    return res.status(503).json({ error: "Model is loading, please wait..." });
  }

  // Thêm handler vào hàng đợi
  pendingRequests.push((result) => {
    if (result.error) {
      res.status(500).json({ error: result.error });
    } else {
      res.json({ text, label: result.label });
    }
  });

  // Gửi text sang Python
  pyProcess.stdin.write(text + "\n");
});

app.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
  startPythonProcess();
});
