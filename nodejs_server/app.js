var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io')(server);
var request = require('request');

app.use(express.static(__dirname + '/bower_components'));

app.get('/', function(req, res){
    res.send("Hello world!");
});

io.on('connection', function(client) {
    console.log('Client connected...');
    // trying to access my Django backend to get all the channel names
    // TODO find a way to authenticate myself in order to get all the channel names from database
    request('http://localhost:8000/streamers/list/', function (error, response, body) {
        if (!error && response.statusCode == 200) {
            var channels = JSON.parse(body);
            console.log(channels);
        }
    });

    client.on('join', function(data) {
        console.log(data);
    });

});

server.listen(4200);
console.log("Server is listening on 4200");
