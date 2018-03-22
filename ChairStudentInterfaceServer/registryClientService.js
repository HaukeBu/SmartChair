var PROTO_PATH_REGISTRY_SERVICE = __dirname + '/../proto/Registry.proto';
var PROTO_PATH_HEARTBEAT_SERVICE = __dirname + '/../proto/Heartbeat.proto';





var protoDescriptorRegistryService = grpc.load(PROTO_PATH_REGISTRY_SERVICE);
var protoDescriptorHeartbeatService = grpc.load(PROTO_PATH_HEARTBEAT_SERVICE);

// The protoDescriptor object has the full package hierarchy
var registryService = protoDescriptorRegistryService.RegistryService;
var heartbeatService = protoDescriptorHeartbeatService.HeartbeatService;

// System Variables
var serverAddressAndPort = '0.0.0.0:50051';
// var localHeartbeatCheckIntervaInMilliseconds = 60000;  // With Heartbeat Check interval
var localHeartbeatCheckIntervaInMilliseconds = 0;  // Test without Registry