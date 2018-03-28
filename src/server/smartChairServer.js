const CONFIG = require('./config.json');

var grpc = require('grpc');

var hearbeatServiceImpl = require('./heartbeatClientService');
var registryService = require('./registryClientService');
var objectImpl = require(CONFIG.objectImplFileName);


var registrationInformation = {};
registrationInformation['oid'] = CONFIG.oid;
registrationInformation['symbolicName'] = CONFIG.symbolicName;
registrationInformation['serverAddress'] = CONFIG.serverAddress;


var grpcServer = new grpc.Server();
objectImpl.init(grpcServer, CONFIG.deviceAddress);
hearbeatServiceImpl.init(grpcServer);

grpcServer.bind(CONFIG.serverAddress, grpc.ServerCredentials.createInsecure());
grpcServer.start();

console.log("Server is running!\nListening bound on: " + CONFIG.serverAddress);

////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////  Perform Registry Login.

registryService.register(CONFIG.registryAddress, registrationInformation, CONFIG.registryConnectionCheckIntervalMs, hearbeatServiceImpl);


// Object TestSeeds applied
objectImpl.applyTestSeeds(true);



