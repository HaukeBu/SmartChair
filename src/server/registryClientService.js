var grpc = require('grpc');

var PROTO_PATH_REGISTRY_SERVICE = __dirname + '/../../proto/registry.proto';
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

    console.log(registryGrpcAddress);
    var client = new registryService(registryGrpcAddress, grpc.credentials.createInsecure());

    console.log("Registry called.");
    client.registerObject({
            'version':1,
            'timestamp': new Date().valueOf(),
            'oid': registrationInformation['oid'],
            'symbolic_name': registrationInformation['symbolicName'],
            'grpc_server': registrationInformation['serverAddress'] ,
            'request_id': 1
        }, function(err, response) {

            if(response !== undefined && response['success']){
                localId = response['local_id'];
                heartbeatService.setLocalId(localId);
                console.log("New LocalId set:" + localId);
            } else {
                console.log("************************************************************");
                console.log("Error Message: ");
                console.log(err);
                console.log("");
                console.log("Is the Registry running and the correct addresses are used?");
                console.log("************************************************************");
            }
        }
    );

    startRegistryLoginCheckImpl();
}

function checkLogInStatus() {
    console.log("checkLogInStatus -- Called!");
    console.log(new Date().valueOf());
    console.log(heartbeatService.hearbeatReceived());
    if(heartbeatService.hearbeatReceived()) {
        heartbeatService.resetHearbeatReceived();
    } else {
        console.log("Registry has not performed a Heartbeat. -> Reconnect Triggered!");
        registerImpl(registryGrpcAddress, registrationInformation, localHeartbeatCheckIntervaInMilliseconds, heartbeatService);
    }
}

// Functions
function startRegistryLoginCheckImpl() {
    stopRegistryLoginCheckImpl();
    
    if (localHeartbeatCheckIntervaInMilliseconds > 0) {
        console.log("Check Hearbeat Enabled!!");
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
