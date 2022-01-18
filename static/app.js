
$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    
    socket.on('response', function(data) {
        console.log("Received data" + data.data);
            $("<p />", { text: data.data}).appendTo("#mydiv1");
            });
    

});