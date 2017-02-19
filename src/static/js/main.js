var socket = io.connect('http://localhost:4200');
socket.on('connect', function(data) {
    socket.emit('join', 'Hello World from client');
});







/*
var apiURL = "https://api.twitch.tv/kraken/streams/";
var clientID = "my-id";

new Vue({
    delimiters: ['<%', '%>'],
    el: '#page',

    created: function () {
        var ajaxRequest = new Promise(function (resolve) {
            jQuery.when(
                jQuery.getJSON("/streamers/list/")
            ).done( function(json) {
                resolve(json.channels);
            });
        });
        ajaxRequest.then(function (channels) {
            return Promise.all(channels.map(function (channel) {
                return new Promise(function (resolve) {
                    var data = $.ajax({
                        url: "https://api.twitch.tv/kraken/streams/" + channel,
                        headers: { 'Client-ID': clientID },
                        dataType: "json",
                        success: function(json) {
                            console.log(json);
                            if (json.stream == null) {
                                resolve([ channel, { streams: null } ]);
                            } else { // channel online
                                resolve([ channel, { streams: 'something' } ]);
                            }
                        },
                    });
                })
            }))
        })
        .then(function (channelsData) {
            return channelsData
                .filter(function (channelData) {
                    return channelData[1].streams !== null;
                })
                .map(function (channelData) {
                    return channelData[0];
                });
        })
        .then(function (channels) {
            this.channels = channels;
        }.bind(this));
    },

    data: {
        channels: [],
    },

    computed: {
        playerIds: function () { // mapping of { channel: playerId }
            return this.channels
                .map(function (channel) {
                    return {
                        playerId: 'player-' + channel,
                        channel: channel,
                    };
                })
                .reduce(function (playerIds, data) {
                    playerIds[data.channel] = data.playerId;
                    return playerIds;
                }, {});
        }
    },

    updated: function () {
        this.channels.forEach(function (channel) {
            var options = {
                width: 200,
                height: 200,
                autoplay: false,
                channel: channel,
            };
            var player = new Twitch.Player(this.playerIds[channel], options);
            player.setVolume(0);
        }.bind(this));
    },
});
*/
