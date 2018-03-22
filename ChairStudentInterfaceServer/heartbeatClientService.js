var grpc = require('grpc');

var PROTO_PATH_HEARTBEAT_SERVICE = __dirname + '/../proto/Heartbeat.proto';
var protoDescriptorHeartbeatService = grpc.load(PROTO_PATH_HEARTBEAT_SERVICE);

// The protoDescriptor object has the full package hierarchy
var heartbeatService = protoDescriptorHeartbeatService.HeartbeatService;

//// Internal Variables
var localHeartbeatCheckIntervaInMilliseconds = 0;  // Test without Registry
var heartbeatReceived = true;
var localId = null;



// GRPC
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


module.exports = {
    init : function (grpcServer, localId) {
        this.localId = localId;

        grpcServer.addService(heartbeatService.service, {
            heartbeat: heartbeatInt
        });
    },
    hearbeatReceived : function (){
        return heartbeatReceived;
    },
    resetHearbeatReceived : function (){
        heartbeatReceived = false;
    },
    setLocalId : function (localIdParam){
        localId =  localIdParam;
    },
    getCurrentHeartbeatIntervalInMilliseconds : function () {
      return localHeartbeatCheckIntervaInMilliseconds;
    },
    stopHeartbeat : function () {
        stopHeartbeat();
    }

};