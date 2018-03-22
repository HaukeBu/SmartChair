var grpc = require('grpc');

var PROTO_PATH_REGISTRY_SERVICE = __dirname + '/../proto/Registry.proto';
var protoDescriptorRegistryService = grpc.load(PROTO_PATH_REGISTRY_SERVICE);

// The protoDescriptor object has the full package hierarchy
var registryService = protoDescriptorRegistryService.RegistryService;

// System Variables
var registryGrpcAddress = null;
var localHeartbeatCheckIntervaInMilliseconds = null;
var registrationInformation = null;
var heartbeatService = null;
var intervalId = null;
var localId = null;


function registerImpl(registryGrpcAddressParam, registrationInformationParam, localHeartbeatCheckIntervaInMillisecondsParam, hearbeatServiceParam) {
    registrationInformation = registrationInformationParam;
    registryGrpcAddress = registryGrpcAddressParam;
    localHeartbeatCheckIntervaInMilliseconds = localHeartbeatCheckIntervaInMillisecondsParam;
    heartbeatService = hearbeatServiceParam;

    if(registryGrpcAddress === null){
        console.log("Not connected to the Registry. No Registry Address provided.");
        return;
    }

    var client = new registryService(registryGrpcAddress, grpc.credentials.createInsecure());

    console.log("Registry called.");
    client.registerObject({
            'version':1,
            'timestamp': new Date().valueOf(),
            'oid': registrationInformation['oid'],
            'symbolicName': registrationInformation['symbolicName'],
            'grpcServer': registrationInformation['serverAddressAndPort'] ,
            'requestId': 1
        }, function(err, response) {

            console.log("Error Message: ", err);
            console.log(err);
            console.log("Response:      ", response);
            console.log(response);

            if(response !== undefined && response['success']){
                localId = response['localId'];
                heartbeatService.setLocalId(localId);
                console.log("New LocalId set:" + localId);
            }
        }
    );

    startRegistryLoginCheckImpl();
}

function checkLogInStatus() {
    if(heartbeatService.hearbeatReceived) {
        heartbeatService.resetHearbeatReceived();
    } else {
        console.log("Registry has not performed a Heartbeat. -> Reconnect Triggered!");
        registerImpl();
    }
}

// Functions
function startRegistryLoginCheckImpl() {
    if (localHeartbeatCheckIntervaInMilliseconds > 0) {
        intervalId = setInterval(checkLogInStatus, localHeartbeatCheckIntervaInMilliseconds);
    }
}

function stopRegistryLoginCheckImpl() {
    if(intervalId !== null){
        clearInterval(intervalId);
    }

    intervalId = 0;
}


module.exports = {
    register : registerImpl,
    getCurrentHeartbeatIntervalInMilliseconds : function () {
        return localHeartbeatCheckIntervaInMilliseconds;
    },
    startRegistryLoginCheck : function () {
        startRegistryLoginCheckImpl();
    },
    stopRegistryLoginCheck : function () {
        stopRegistryLoginCheckImpl();
    }
};
