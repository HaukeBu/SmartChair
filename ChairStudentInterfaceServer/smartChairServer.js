var grpc = require('grpc');
var objectImpl = require('./object0_0_1ImplSmartChair.js');
var hearbeatServiceImpl = require('./heartbeatClientService');
var registryService = require('./registryClientService');

// System Variables
var serverAddressAndPort = '0.0.0.0:50051';
var registryAddress = "0.0.0.0:50052";  // Registry Address to connect to
//var registryAddress = null ;  // Test without Registry
var deviceGrpcAddress = null;


var localHeartbeatCheckIntervaInMilliseconds = 60000;  // With Heartbeat Check interval
//var localHeartbeatCheckIntervaInMilliseconds = 0;  // Test without Registry
var symbolicName = "smartchair4";
var oid = "0.0.1";

var registrationInformation = {};
registrationInformation['oid'] = oid;
registrationInformation['symbolicName'] = symbolicName;
registrationInformation['serverAddressAndPort'] = serverAddressAndPort;


var grpcServer = new grpc.Server();
objectImpl.init(grpcServer, deviceGrpcAddress);
hearbeatServiceImpl.init(grpcServer);

grpcServer.bind(serverAddressAndPort, grpc.ServerCredentials.createInsecure());
grpcServer.start();

console.log("Server is running!\nListening bound on: " + serverAddressAndPort);

////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////  Perform Registry Login.

registryService.register(registryAddress, registrationInformation, localHeartbeatCheckIntervaInMilliseconds, hearbeatServiceImpl);


// Object TestSeeds applied
objectImpl.applyTestSeeds(true);



