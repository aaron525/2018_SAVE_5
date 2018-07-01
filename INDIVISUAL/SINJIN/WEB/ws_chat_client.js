var clientSocket = null;

function connect() {
  clientSocket = new WebSocket("wss://echo.websocket.org");

  clientSocket.onopen = function() {
    document.getElementById("chatbox").innerHTML = "Connected!<br>";
  };

  clientSocket.onmessage = function(event) {
    var text = "";
    var msg = JSON.parse(event.data);
    var time = new Date(msg.date);
    var timeStr = time.toLocaleTimeString();

    switch (msg.type) {
      case "id":
        // TODO: will be implemented in another task
        break;
      case "username":
        // TODO: will be implemented in another task
        break;
      case "message":
        text = "(" + timeStr + ") <b>" + msg.name + "</b>: " + msg.text + "<br>";
        break;
      case "userlist":
        // TODO: will be implemented in another task
        break;
    }

    if (text.length) {
      document.getElementById("chatbox").innerHTML += text;
    }
  };
}

function sendText() {
  var msg = {
    type: "message",
    name: "anonymous",
    text: document.getElementById("text").value,
    date: Date.now()
  };

  clientSocket.send(JSON.stringify(msg));
  document.getElementById("text").value = "";
}

function clearText() {
  document.getElementById("chatbox").innerHTML = "";
}
