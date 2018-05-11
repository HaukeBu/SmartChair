const CONFIG = require('./config.json');

var grpc = require('grpc');

var hearbeatService = require('./heartbeatClientService');
var registryService = require('./registryClientService');
var objectImpl = require(CONFIG.objectImplFileName);


var registrationInformation = {};
registrationInformation['oid'] = CONFIG.oid;
registrationInformation['symbolicName'] = CONFIG.symbolicName;
registrationInformation['serverAddress'] = CONFIG.serverAddressSend;


var grpcServer = new grpc.Server();
objectImpl.init(grpcServer);
hearbeatService.init(grpcServer);

grpcServer.bind(CONFIG.serverAddressBind, grpc.ServerCredentials.createInsecure());
grpcServer.start();

console.log("Server is running!\nListening bound on: " + CONFIG.serverAddressBind);

////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////  Perform Registry Login.

registryService.register(CONFIG.registryAddress, registrationInformation, CONFIG.registryConnectionCheckIntervalMs, hearbeatService);


// Object TestSeeds applied
objectImpl.applyTestSeeds(true);



