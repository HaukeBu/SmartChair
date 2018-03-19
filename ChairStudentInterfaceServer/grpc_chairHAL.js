var PROTO_PATH_CHAIR_SERVICE = __dirname + '/../proto/Chair.proto';
var PROTO_PATH_SMART_CHAIR_STUDENT_INTERFACE_SERVICE = __dirname + '/../proto/SmartChairStudentInterface.proto';

var grpc = require('grpc');

var protoDescriptorChairService = grpc.load(PROTO_PATH_CHAIR_SERVICE);
var protoDescriptorSmartChairStudentInterfaceService = grpc.load(PROTO_PATH_SMART_CHAIR_STUDENT_INTERFACE_SERVICE);
// The protoDescriptor object has the full package hierarchy
var chairService = protoDescriptorChairService.ChairService;
var smartChairStudentInterfaceService = protoDescriptorSmartChairStudentInterfaceService.SmartChairStudentInterfaceService;

var chair = {};
chair['distance'] = {};
chair['temperature'] = {};
chair['pressure'] = {};
chair['pressure']['backrest'] = {};
chair['pressure']['backrest']['values'] = [];
chair['pressure']['seat'] = {};
chair['pressure']['seat']['values'] = [];
chair['motion'] = {};
chair['motion']['seat'] = {};
chair['motion']['seat']['gyroscope'] = [];
chair['motion']['seat']['accelerometer'] = [];
chair['motion']['seat']['rotationAngle'] = [];
chair['motion']['backrest'] = {};
chair['motion']['backrest']['gyroscope'] = [];
chair['motion']['backrest']['accelerometer'] = [];
chair['motion']['backrest']['rotationAngle'] = [];

// /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////// HAL Interface
function HALInterfaceImpl(request){
    console.log("");
    console.log("");
    console.log("grpcCallReceived");

    var tempPlatformMessage = {
        version: 1,
        json: '{"version": 1, "callObject": "test1"}'
    };

    /*
    console.log("Type of request: " + typeof(request));
    console.log("request: " + request);
    console.log(request);
    console.log(request['version']);
    console.log(request['timestamp']);
    console.log(request['sensor_type']);
    */
    console.log(request['values']);

    var response = processMessage(request);

    console.log("");
    console.log("Type of response: " + typeof(response));
    console.log(response);

    return response;
}

function processMessage(request) {

    // extract Values
    var values = JSON.parse(request['values']);
    values = values['values'];

    var timestamp = request['timestamp'];

    // select sensor_type
    switch( request['sensor_type']) {
        case 0 :
            // Debug
            console.log("Debug Message timestamp: " + request['timestamp']);

            for(var i = 0; i < values.length; i++){
                console.log("Debug Message id: " + values[i]['id'] + ", value: " + values[i]['value']);
            }

            break;
        case 1 :
            // Distance
            chair['distance']['value'] = values[0]['value'];
            chair['distance']['timestamp'] = timestamp;
            break;

        case 2 :
            // Pressure Backrest

            for(var i = 0; i < values.length; i++){
                chair['pressure']['backrest']['values'][i] = values[i]['value'];
            }

            chair['pressure']['backrest']['timestamp'] = timestamp;
            break;

        case 3 :
            // Pressure Seat
            for(var i = 0; i < values.length; i++){
                chair['pressure']['seat']['values'][i] = values[i]['value'];
            }

            chair['pressure']['seat']['timestamp'] = timestamp;
            break;

        case 4 :
            // Temperature
            var temp = values[0]['value'];

            chair['temperature']['value'] = temp / 10;
            chair['temperature']['timestamp'] = timestamp;
            break;

        case 5 :
            // Motion Backrest
            // Gyroscope
            var valuesPerKind = 3;
            for(var i = 0; i < valuesPerKind && i < values.length; i++){
                chair['motion']['backrest']['gyroscope'][i] = values[i]['value'];
            }

            // Accelerometer
            var offsetAccelerometer = 3;
            for(var i = 0; (i + offsetAccelerometer) < (valuesPerKind + offsetAccelerometer) && (i + offsetAccelerometer) < values.length; i++){
                chair['motion']['backrest']['accelerometer'][i] = values[offsetAccelerometer + i]['value'];
            }

            // Rotation Angle
            var offsetRotationAngle = 6;
            for(var i = 0; (i + offsetRotationAngle) < (valuesPerKind + offsetRotationAngle) && (i + offsetRotationAngle) < values.length; i++){
                chair['motion']['backrest']['rotationAngle'][i] = values[offsetRotationAngle + i]['value'];

                //console.log("Backrest Rotation " + i + ": " + values[offsetRotationAngle + i]['value']);
            }

            chair['motion']['backrest']['timestamp'] = timestamp;
            break;

        case 6 :
            // Motion Seat
            // Gyroscope
            var valuesPerKind = 3;
            for(var i = 0; i < valuesPerKind && i < values.length; i++){
                chair['motion']['seat']['gyroscope'][i] = values[i]['value'];

                console.log("Seat Rotation " + i + ": " + values[i]['value']);
            }

            // Accelerometer
            var offsetAccelerometer = 3;
            for(var i = 0; (i + offsetAccelerometer) < (valuesPerKind + offsetAccelerometer) && (i + offsetAccelerometer) < values.length; i++){
                chair['motion']['seat']['accelerometer'][i] = values[offsetAccelerometer + i]['value'];

                console.log("Seat Rotation " + i + ": " + values[offsetAccelerometer + i]['value']);
            }

            // Rotation Angle
            var offsetRotationAngle = 6;
            for(var i = 0; (i + offsetRotationAngle) < (valuesPerKind + offsetRotationAngle) && (i + offsetRotationAngle) < values.length; i++){
                chair['motion']['seat']['rotationAngle'][i] = values[offsetRotationAngle + i]['value'];

                console.log("Seat Rotation " + i + ": " + values[offsetRotationAngle + i]['value']);
            }

            chair['motion']['seat']['timestamp'] = timestamp;
            break;
    }

    var response = {};
    response['success'] = true;

    return response;
}

function ChairUpdateInt(call, callback) {
    callback(null, HALInterfaceImpl(call.request));
}

///////////////////////////////
///////////// Request Interface

function createResponse(valueObject) {
    var response = {};
    response['version'] = 1;
    response['success'] = true;
    response['timestamp'] = new Date().valueOf(); // UTC Timestamp in Milliseconds
    // console.log("Timestamp: ", response['timestamp']);
    response['values'] = JSON.stringify(valueObject);
    return response;
}

function getAllImpl(request) {
    console.log("getAll - Request: ", request);
    var response = createResponse(chair);
    console.log("getAll - Response: ", request);
    return response;
}
function getDistanceImpl(request) {
    var valuesObj = {};
    console.log(chair['distance']);
    valuesObj['distance'] = chair['distance'];
    return createResponse(valuesObj);
}
function getTemperatureImpl(request) {
    var valuesObj = {};
    valuesObj['temperature'] = chair['temperature'];
    return createResponse(valuesObj);
}
function getPressureAllImpl(request) {
    return createResponse(chair['pressure']);
}
function getPressureBackrestImpl(request) {
    var valuesObj = {};
    valuesObj['backrest'] = chair['pressure']['backrest'];
    return createResponse(valuesObj);
}
function getPressureSeatImpl(request) {
    var valuesObj = {};
    valuesObj['seat'] = chair['pressure']['seat'];
    return createResponse(valuesObj);
}
function getMotionAllImpl(request) {
    return createResponse(chair['motion']);
}
function getMotionBackrestAllImpl(request) {
    return createResponse(chair['motion']['backrest']);
}
function getMotionBackrestGyroscopeImpl(request) {
    var valuesObj = {};
    valuesObj['gyroscope'] = chair['motion']['backrest']['gyroscope'];
    return createResponse(valuesObj);
}
function getMotionBackrestAccelerometerImpl(request) {
    var valuesObj = {};
    valuesObj['accelerometer'] = chair['motion']['backrest']['accelerometer'];
    return createResponse(valuesObj);
}
function getMotionBackrestRotationAngleImpl(request) {
    var valuesObj = {};
    valuesObj['rotationAngle'] = chair['motion']['backrest']['rotationAngle'];
    return createResponse(valuesObj);
}
function getMotionSeatAllImpl(request) {
    return createResponse(chair['motion']['seat']);
}
function getMotionSeatGyroscopeImpl(request) {
    var valuesObj = {};
    valuesObj['gyroscope'] = chair['motion']['seat']['gyroscope'];
    return createResponse(valuesObj);
}
function getMotionSeatAccelerometerImpl(request) {
    var valuesObj = {};
    valuesObj['accelerometer'] = chair['motion']['seat']['accelerometer'];
    return createResponse(valuesObj);
}
function getMotionSeatRotationAngleImpl(request) {
    var valuesObj = {};
    valuesObj['rotationAngle'] = chair['motion']['seat']['rotationAngle'];
    return createResponse(valuesObj);
}

// Procedure Intermediates
function getAllInt(call, callback) {
    callback(null, getAllImpl(call.request));
}
function getDistanceInt(call, callback) {
    callback(null, getDistanceImpl(call.request));
}
function getTemperatureInt(call, callback) {
    callback(null, getTemperatureImpl(call.request));
}
function getPressureAllInt(call, callback) {
    callback(null, getPressureAllImpl(call.request));
}
function getPressureBackrestInt(call, callback) {
    callback(null, getPressureBackrestImpl(call.request));
}
function getPressureSeatInt(call, callback) {
    callback(null, getPressureSeatImpl(call.request));
}
function getMotionAllInt(call, callback) {
    callback(null, getMotionAllImpl(call.request));
}
function getMotionBackrestAllInt(call, callback) {
    callback(null, getMotionBackrestAllImpl(call.request));
}
function getMotionBackrestGyroscopeInt(call, callback) {
    callback(null, getMotionBackrestGyroscopeImpl(call.request));
}
function getMotionBackrestAccelerometerInt(call, callback) {
    callback(null, getMotionBackrestAccelerometerImpl(call.request));
}
function getMotionBackrestRotationAngleInt(call, callback) {
    callback(null, getMotionBackrestRotationAngleImpl(call.request));
}
function getMotionSeatAllInt(call, callback) {
    callback(null, getMotionSeatAllImpl(call.request));
}
function getMotionSeatGyroscopeInt(call, callback) {
    callback(null, getMotionSeatGyroscopeImpl(call.request));
}
function getMotionSeatAccelerometerInt(call, callback) {
    callback(null, getMotionSeatAccelerometerImpl(call.request));
}
function getMotionSeatRotationAngleInt(call, callback) {
    callback(null, getMotionSeatRotationAngleImpl(call.request));
}

/////////////////////////////////////////////////////////
///////////////////////  Server
function getServer() {
    var server = new grpc.Server();
    // HAL Value Input
    server.addService(chairService.service, {
        ChairUpdate: ChairUpdateInt
    });

    server.addService(smartChairStudentInterfaceService.service, {
        getAll: getAllInt,
        getDistance: getDistanceInt,
        getTemperature: getTemperatureInt,
        getPressureAll: getPressureAllInt,
        getPressureBackrest: getPressureBackrestInt,
        getPressureSeat: getPressureSeatInt,
        getMotionAll: getMotionAllInt,
        getMotionBackrestAll: getMotionBackrestAllInt,
        getMotionBackrestGyroscope: getMotionBackrestGyroscopeInt,
        getMotionBackrestAccelerometer: getMotionBackrestAccelerometerInt,
        getMotionBackrestRotationAngle: getMotionBackrestRotationAngleInt,
        getMotionSeatAll: getMotionSeatAllInt,
        getMotionSeatGyroscope: getMotionSeatGyroscopeInt,
        getMotionSeatAccelerometer: getMotionSeatAccelerometerInt,
        getMotionSeatRotationAngle: getMotionSeatRotationAngleInt
    });
    return server;
}

var routeServer = getServer();
routeServer.bind('0.0.0.0:50051', grpc.ServerCredentials.createInsecure());
routeServer.start();

console.log("Server is running!");


var testRequest = {};
// Commonfields
testRequest['version'] = 1;
testRequest['timestamp'] = 1520442151;

// Distance
testRequest['sensor_type'] = 1;
testRequest['values'] = '{"values": [{"id": 0, "value": 22}]}';
processMessage(testRequest);

testRequest['timestamp'] = 1520442152;
// PressureBackrest
testRequest['sensor_type'] = 2;
testRequest['values'] = '{"values": [{"id": 0, "value": 0}, {"id": 1, "value": 1}, {"id": 2, "value": 2}, {"id": 3, "value": 0}, {"id": 4, "value": 0}, {"id": 5, "value": 0}]}';
processMessage(testRequest);

testRequest['timestamp'] = 1520442153;
// PressureSeat
testRequest['sensor_type'] = 3;
testRequest['values'] = '{"values": [{"id": 0, "value": 0}, {"id": 1, "value": 1}, {"id": 2, "value": 2}, {"id": 3, "value": 3}]}';
processMessage(testRequest);

testRequest['timestamp'] = 1520442154;
//Temperature
testRequest['sensor_type'] = 4;
testRequest['values'] = '{"values": [{"id": 0, "value": 221}]}';
processMessage(testRequest);

testRequest['timestamp'] = 1520442155;
// Gyros Backrest
testRequest['sensor_type'] = 5;
testRequest['values'] = '{"values": [{"id": 0, "value": -15955}, {"id": 1, "value": -855}, {"id": 2, "value": 3355}, {"id": 3, "value": -215}, {"id": 4, "value": 1875}, {"id": 5, "value": 16385}, {"id": 6, "value": 855}, {"id": 7, "value": -65}, {"id": 8, "value": -95}]}';
processMessage(testRequest);

testRequest['timestamp'] = 1520442156;
// Gyros Seat
testRequest['sensor_type'] = 6;
testRequest['values'] = '{"values": [{"id": 0, "value": -15956}, {"id": 1, "value": -856}, {"id": 2, "value": 3356}, {"id": 3, "value": -216}, {"id": 4, "value": 1876}, {"id": 5, "value": 16386}, {"id": 6, "value": 856}, {"id": 7, "value": -66}, {"id": 8, "value": -96}]}';
processMessage(testRequest);

console.log("Result Chair Object");
console.log(chair);
