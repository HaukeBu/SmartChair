var grpc = require('grpc');

var PROTO_PATH_HEARTBEAT_SERVICE = __dirname + '/../proto/Heartbeat.proto';
var protoDescriptorHeartbeatService = grpc.load(PROTO_PATH_HEARTBEAT_SERVICE);

// The protoDescriptor object has the full package hierarchy
var heartbeatService = protoDescriptorHeartbeatService.HeartbeatService;

//// Internal Variables
var localHeartbeatCheckIntervaInMilliseconds = 0;  // Test without Registry
var heartbeatReceived = true;

var intervalId = 0;


function heartbeatImpl(request) {
    if(localId === request['localId']){
        console.log("Heartbeat Received");
        heartbeatReceived = true;
        return request;
    } else {
        console.log("Heartbeat Request got for localId: " + request['localId'] + ", but is: " + localId);
    }
}

// Procedure Intermediates
function heartbeatInt(call, callback) {
    callback(null, heartbeatImpl(call.request));
}

function stopHeartbeat() {
    if(intervalId !== 0){
        clearInterval(intervalId);
    }

    intervalId = 0;
}

if (localHeartbeatCheckIntervaInMilliseconds > 0){
    intervalID = setInterval(checkLogInStatus, localHeartbeatCheckIntervaInMilliseconds);
}


module.exports = {
    init : function (grpcServer, localHeartbeatCheckIntervaInMilliseconds) {
        grpcServer.addService(heartbeatService.service, {
            heartbeat: heartbeatInt
        });
    },
    getHearbeatReceived : function (){
        return heartbeatReceived;
    },
    getCurrentHeartbeatIntervalInMilliseconds : function () {
      return localHeartbeatCheckIntervaInMilliseconds;
    },
    stopHeartbeat : function () {
        stopHeartbeat();
    }

}