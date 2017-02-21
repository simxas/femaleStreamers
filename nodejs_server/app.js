var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io')(server);
var request = require('request');

var apiURL = "https://api.twitch.tv/kraken/streams/";
var clientID = "xxxxxxxxxxxxxxx";

app.use(express.static(__dirname + '/bower_components'));

app.get('/', function(req, res){
    res.send('Hello world!');
});

io.on('connection', function(client) {
    console.log('Client connected...');
    // trying to access my Django backend to get all the channel names
    // TODO find a way to authenticate myself in order to get all the channel names from database
    client.on('join', function(data) {
        var djangoRequest = new Promise(function (resolve) {
            request('http://localhost:8888/streamers/list/foo/', function (error, response, body) {
                if (!error && response.statusCode == 200) {
                    var channels = JSON.parse(body);
                    console.log(channels.channels);
                    resolve(channels.channels);
                }else{
                    console.log(error);
                }
            });
        });

        djangoRequest.then(function (channels) {
            return Promise.all(channels.map(function (channel) {
                return new Promise(function (resolve) {
                    var options = {
                        url: apiURL + channel,
                        headers: {
                            'Client-ID': clientID
                        }
                    };

                    function callback(error, response, body) {
                        if (!error && response.statusCode == 200) {
                            var json = JSON.parse(body);
                            // console.log(json);
                            if (json.stream == null) {
                                resolve([ channel, { streams: null } ]);
                            } else { // channel online
                                resolve([ channel, { streams: 'something' } ]);
                            }
                        }
                    }

                    request(options, callback);
                })
            }))
        })
        .then(function (channelsData) {
            return channelsData
                .filter(function (channelData) {
                    console.log(channelData);
                    if(channelData[1].streams !== null) {
                        client.emit('channels', channelData[0]);
                    }
                    // return channelData[1].streams !== null;
                })
                .map(function (channelData) {
                    return channelData[0];
                });
        })
        .then(function (channels) {
            // this.channels = channels;
            // console.log('Online channels');
            // console.log(channels);
            // client.emit('channels', channels);
        });
    });

});

server.listen(4200);
console.log('Server is listening on 4200');
