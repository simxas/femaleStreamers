var socket = io.connect('http://localhost:4200');


new Vue({
    delimiters: ['<%', '%>'],
    el: '#page',

    created: function () {
        socket.on('connect', function(data) {
            socket.emit('join', 'Hello World from client');
        });
        socket.on('channels', function(data) {
            this.channels.push(data);
        }.bind(this));
    },

    data: {
        channels: [],
    },

    computed: {
        playerIds: function () { // mapping of { channel: playerId }
            console.log('computed function');
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
        console.log("somesdsd");
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
