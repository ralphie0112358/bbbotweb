function getMotorUrl() {
    return window.location.protocol + "//" + window.location.host + "/motor";
}
function refreshState() {
    var url = getMotorUrl();
    var client = new XMLHttpRequest();

    client.open("GET", url, false);
    client.send();

    if (client.status == 200) {
        var obj = JSON.parse(client.response);
        document.getElementById("robot_state").innerHTML = obj.state.bold();
    }
    else {
        alert("FAIL: " + client.status + " " + client.statusText + ".");
    }
}
window.onload = refreshState;
function myFunction() {

    var url = getMotorUrl();
    var client = new XMLHttpRequest();

    client.open("POST", url, false);
    client.send();

    if (client.status == 200) {
        var obj = JSON.parse(client.response);
        document.getElementById("robot_state").innerHTML = obj.state.bold();
    }
    else {
        alert("FAIL: " + client.status + " " + client.statusText + ".");
    }
}
