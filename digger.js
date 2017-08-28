var deadZone = 0.2;
var lastMessage;

function doConnect() {
    websocket = new WebSocket("ws://golddigger:8000");
    websocket.onopen = function(evt) {
        onOpen(evt)
    };
    websocket.onclose = function(evt) {
        onClose(evt)
    };
    websocket.onmessage = function(evt) {
        onMessage(evt)
    };
    websocket.onerror = function(evt) {
        onError(evt)
    };
}

function onOpen(evt) {
    console.log("connected");
}

function onClose(evt) {
    console.log("disconnected");
}

function onMessage(evt) {
    console.log("response: " + evt.data + '');
}

function onError(evt) {
    console.log('error: ' + evt.data + '');
    websocket.close();
}

function doSend(message) {
    if (message != lastMessage) {
        if (websocket.readyState == websocket.CONNECTING) {
            return false
        }
        if (websocket.readyState == websocket.CLOSED || websocket.readyState == websocket.CLOSING) {
            doConnect();
        }
        console.log("sent:", message);
        websocket.send(message);
        lastMessage = message;
    } else {
        return false;
    }
}
window.addEventListener("load", init, false);

function sendText() {
    doSend(document.myform.inputtext.value);
}

function clearText() {
    document.myform.outputtext.value = "";
}

function doDisconnect() {
    websocket.close();
}
var haveEvents = 'ongamepadconnected' in window;
var controllers = {};

function connecthandler(e) {
    addgamepad(e.gamepad);
}

function addgamepad(gamepad) {
    console.log("added gamepad", gamepad);
    controllers[gamepad.index] = gamepad;
}

function disconnecthandler(e) {
    removegamepad(e.gamepad);
}

function removegamepad(gamepad) {
    delete controllers[gamepad.index];
}

function updateStatus() {
    if (!haveEvents) {
        scangamepads();
    }
    var i = 0;
    var j;
    for (j in controllers) {
        var controller = controllers[j];
        var motionMessage;
        var turretMessage;
        for (i = 0; i < controller.buttons.length; i++) {
            //console.log("button " + i + ": " + controller.buttons[i]);
        }
        var axis = [];
        for (i = 0; i < controller.axes.length; i++) {
            //console.log("axis " + i + ": " + controller.axes[i].toFixed(4) + " value = " + ( controller.axes[i] + 1));
            axis[i] = controller.axes[i].toFixed(4);
        }
        if (axis[0] > -0.5 && axis[0] < 0.5 || axis[1] > -0.5 && axis[1] < 0.5) {
            motionMessage = 'stop 0';
        }
        if (axis[0] < deadZone * -1) {
            rate = Math.round(100 * Math.abs(axis[0]));
            motionMessage = 'left ' + rate.toString();
        } else if (axis[0] > deadZone) {
            rate = Math.round(100 * Math.abs(axis[0]));
            motionMessage = 'right ' + rate.toString();
        }
        if (axis[1] < deadZone * -1) {
            rate = Math.round(100 * Math.abs(axis[1]));
            motionMessage = 'forward ' + rate.toString();
        } else if (axis[1] > deadZone) {
            rate = Math.round(100 * Math.abs(axis[1]));
            motionMessage = 'backward ' + rate.toString();
        }
        if (axis[2] < deadZone && axis[2] > deadZone * -1) {
            turretMessage = 'stop 0';
        } else if (axis[2] < deadZone * -1) {
            rate = Math.round(100 * Math.abs(axis[2]));
            turretMessage = 'left' + ' ' + rate.toString();
        } else if (axis[2] > deadZone) {
            rate = Math.round(100 * Math.abs(axis[2]));
            turretMessage = 'right' + ' ' + rate.toString();
        }
        doSend('track_' + motionMessage + '\n' + 'turret_' + turretMessage);
    }
}

function scangamepads() {
    var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
    for (var i = 0; i < gamepads.length; i++) {
        if (gamepads[i]) {
            if (gamepads[i].index in controllers) {
                controllers[gamepads[i].index] = gamepads[i];
            } else {
                addgamepad(gamepads[i]);
            }
        }
    }
}

function init() {
    doConnect();
    setInterval(updateStatus, 100);
    //updateStatus();
}
window.addEventListener("gamepadconnected", connecthandler);
window.addEventListener("gamepaddisconnected", disconnecthandler);
