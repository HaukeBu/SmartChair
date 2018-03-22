var grpc = require('grpc');
var objectImpl = require('./object0_0_1ImplSmartChair.js');
var hearbeatServiceImpl = require('./heartbeatClientService');

var PROTO_PATH_REGISTRY_SERVICE = __dirname + '/../proto/Registry.proto';
var protoDescriptorRegistryService = grpc.load(PROTO_PATH_REGISTRY_SERVICE);

// The protoDescriptor object has the full package hierarchy
var registryService = protoDescriptorRegistryService.RegistryService;


// System Variables
var serverAddressAndPort = '0.0.0.0:50051';
// var localHeartbeatCheckIntervaInMilliseconds = 60000;  // With Heartbeat Check interval
var localHeartbeatCheckIntervaInMilliseconds = 0;  // Test without Registry
var symbolicName = "smartchair4";
var oid = "0.0.1";

//var registryAddress = "0.0.0.0:50052";  // Registry Address to connect to
var registryAddress = null ;  // Test without Registry
var deviceGrpcAddress = null;


var localId = "None";



/////////////////////////////////////////////////////////
///////////////////////  Heartbeat
// Procedure Implementation


/////////////////////////////////////////////////////////
//////////////////////  Registry

function register() {
    if(registryAddress === null){
        console.log("Not connected to the Registry. No Registry Address provided.");
        return;
    }

    var client = new registryService(registryAddress, grpc.credentials.createInsecure());

    console.log("Registry called.");
    client.registerObject({
            'version':1,
            'timestamp': new Date().valueOf(),
            'oid': oid,
            'symbolicName': symbolicName,
            'grpcServer': serverAddressAndPort,
            'requestId': 1
        }, function(err, response) {

            console.log("Error Message: ", err);
            console.log(err);
            console.log("Response:      ", response);
            console.log(response);

            if(response !== undefined && response['success']){
                localId = response['localId'];
                console.log("New LocalId set:" + localId);
            }
        }
    );

}

function checkLogInStatus() {
    if(heartbeatReceived) {
        heartbeatReceived = false;
    } else {
        console.log("Registry has not performed a Heartbeat. -> Reconnect Triggered!");
        register();
    }
}


////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////  Start Server

var grpcServer = new grpc.Server();

console.log("Test1");
console.log(typeof objectImpl.init);

objectImpl.init(grpcServer, deviceGrpcAddress);
hearbeatServiceImpl.init(grpcServer, localHeartbeatCheckIntervaInMilliseconds);

grpcServer.bind(serverAddressAndPort, grpc.ServerCredentials.createInsecure());
grpcServer.start();

console.log("Server is running!\nListening bound on: " + serverAddressAndPort);

////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////  Perform Registry Login.
register();


objectImpl.applyTestSeeds(true);



