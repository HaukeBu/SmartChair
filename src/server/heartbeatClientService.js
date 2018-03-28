var grpc = require('grpc');

var PROTO_PATH_HEARTBEAT_SERVICE = __dirname + '/../../proto/heartbeat.proto';
var protoDescriptorHeartbeat = grpc.load(PROTO_PATH_HEARTBEAT_SERVICE);

// The protoDescriptor object has the full package hierarchy
var heartbeatService = protoDescriptorHeartbeat.HeartbeatService;

//// Internal Variables
var localHeartbeatCheckIntervaInMilliseconds = 0;  // Test without Registry
var heartbeatReceived = true;
var localId = null;


// GRPC
function heartbeatImpl(request) {
    if(localId === request['local_id']){
        console.log("Heartbeat Received");
        heartbeatReceived = true;
        return request;
    } else {
        console.log("Heartbeat Request got for localId: " + request['local_id'] + ", but is: " + localId);
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