var app = require('express')();
var http = require('http').Server(app).listen(3000);
var port = 3000;
var io = require('socket.io')(http);
var kafka = require('kafka-node');

app.get('/', function(req, res){
  res.sendFile(__dirname + '/line-chart-sentiments.html');
});

//Call SocketIO with the message from Kafka 
function callSockets(io, message){
  io.sockets.emit('data', message);
}

var Consumer = kafka.Consumer;
var Offset = kafka.Offset;
var Client = kafka.KafkaClient;

var client = new Client({ kafkaHost: '35.239.57.13:9092' , requestTimeout :100000});
var topics = [{ topic: "blob_sentiments", partition: 0 }];
var options = {autoCommit: false, fromOffset: 'latest',batch : 1, fetchMaxWaitMs: 110200, fetchMaxBytes: 1024 * 1024 };

var consumer = new Consumer(client, topics, options);
var offset = new Offset(client);

//Emit data on socket once the client is connected
io.sockets.on('connection', function (socket) {

    consumer.on('message', function (message) {
      console.log(message['value'])
      io.sockets.emit('data', message);
    });

});

io.sockets.on('error', function(exception) {

  console.log('SOCKET ERROR');
  socket.destroy();

})
 