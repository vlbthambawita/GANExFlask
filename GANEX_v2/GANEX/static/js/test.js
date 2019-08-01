
var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        console.log("data sent to server");
        socket.emit('joined', {});
        
    });

    socket.on('status', function(data) {
        // $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        // $('#chat').scrollTop($('#chat')[0].scrollHeight);
        $("#Results").append('<li>'+ data.msg +'</li>');
        console.log("Received")
        //window.alert("Received")
    });

    socket.on('test', function(data) {
        // $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        // $('#chat').scrollTop($('#chat')[0].scrollHeight);
        $("#Results").append('<li>'+ data.msg +'</li>');
        console.log("Receiveddd test msg also")
        //window.alert("Received")
    });
    
});