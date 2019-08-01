
var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/plot');
    socket.on('connect', function() {
        console.log("data sent to server");
        socket.emit('plotting'); // detec connecting to plot tab
        
    });

    socket.on('plotdata', function(data) {
        // $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        // $('#chat').scrollTop($('#chat')[0].scrollHeight);
        $("#Results").append('<li>'+ data.data +'</li>');
        //console.log("Received plot data")
        //window.alert("Received")
    });
});