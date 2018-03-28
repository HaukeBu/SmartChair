var PROTO_PATH_REGISTRY_SERVICE = __dirname + '/./proto/Registry.proto';

var grpc = require('grpc');

var protoDescriptorRegistryService = grpc.load(PROTO_PATH_REGISTRY_SERVICE);

var registryService = protoDescriptorRegistryService.RegistryService;

var registryClient = new registryService('0.0.0.0:50052', grpc.credentials.createInsecure());

registryClient.requestObjects({
        'version':1,
        'timestamp': new Date().valueOf(),
        'oid': "0.0.1",
        'requestId': 1
    }, function(err, response) {
        console.log("Error Message: ", err);
        console.log(err);
        console.log("Response:      ", response);
        console.log(response);
    }
);