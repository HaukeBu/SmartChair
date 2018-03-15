var PROTO_PATH_SMART_CHAIR_STUDENT_INTERFACE_SERVICE = __dirname + '/grpcFiles/SmartChairStudentInterface.proto';

var grpc = require('grpc');

var protoDescriptorSmartChairStudentInterfaceService = grpc.load(PROTO_PATH_SMART_CHAIR_STUDENT_INTERFACE_SERVICE);
var smartChairStudentInterfaceService = protoDescriptorSmartChairStudentInterfaceService.SmartChairStudentInterfaceService;


var client = new smartChairStudentInterfaceService('192.168.188.39:50051', grpc.credentials.createInsecure()); // TODO: Check ip!

client.getAll({'version':1}, function(err, response) {
    console.log("\n************ getAll: ");
    console.log('Client - Response:', response);
});

client.getDistance({'version':1}, function(err, response) {
    console.log("\n************ getDistance: ");
    console.log('Client - Response:', response);
});

client.getTemperature({'version':1}, function(err, response) {
    console.log("\n************ getTemperature: ");
    console.log('Client - Response:', response);
});

client.getPressureAll({'version':1}, function(err, response) {
    console.log("\n************ getPressureAll: ");
    console.log('Client - Response:', response);
});

client.getPressureBackrest({'version':1}, function(err, response) {
    console.log("\n************ getPressureBackrest: ");
    console.log('Client - Response:', response);
});

client.getPressureSeat({'version':1}, function(err, response) {
    console.log("\n************ getPressureSeat: ");
    console.log('Client - Response:', response);
});

client.getMotionAll({'version':1}, function(err, response) {
    console.log("\n************ getMotionAll: ");
    console.log('Client - Response:', response);
});

client.getMotionBackrestAll({'version':1}, function(err, response) {
    console.log("\n************ getMotionBackrestAll: ");
    console.log('Client - Response:', response);
});

client.getMotionBackrestGyroscope({'version':1}, function(err, response) {
    console.log("\n************ getMotionBackrestGyroscope: ");
    console.log('Client - Response:', response);
});

client.getMotionBackrestAccelerometer({'version':1}, function(err, response) {
    console.log("\n************ getMotionBackrestAccelerometer: ");
    console.log('Client - Response:', response);
});

client.getMotionBackrestRotationAngle({'version':1}, function(err, response) {
    console.log("\n************ getMotionBackrestRotationAngle: ");
    console.log('Client - Response:', response);
});

client.getMotionSeatAll({'version':1}, function(err, response) {
    console.log("\n************ getMotionSeatAll: ");
    console.log('Client - Response:', response);
});

client.getMotionSeatGyroscope({'version':1}, function(err, response) {
    console.log("\n************ getMotionSeatGyroscope: ");
    console.log('Client - Response:', response);
});

client.getMotionSeatAccelerometer({'version':1}, function(err, response) {
    console.log("\n************ getMotionSeatAccelerometer: ");
    console.log('Client - Response:', response);
});

client.getMotionSeatRotationAngle({'version':1}, function(err, response) {
    console.log("\n************ getMotionSeatRotationAngle: ");
    console.log('Client - Response:', response);
});
