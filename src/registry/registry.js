var PROTO_PATH_REGISTRY_SERVICE = __dirname + '/../../proto/registry.proto';
var PROTO_PATH_HEARTBEAT_SERVICE = __dirname + '/../../proto/heartbeat.proto';

var grpc = require('grpc');

var protoDescriptorRegistryService = grpc.load(PROTO_PATH_REGISTRY_SERVICE);
var protoDescriptorHeartbeatService = grpc.load(PROTO_PATH_HEARTBEAT_SERVICE);

var registryService = protoDescriptorRegistryService.RegistryService;
var heartbeatService = protoDescriptorHeartbeatService.HeartbeatService;

var entriesByOId = {}; // Mapping Oid -> localIds
var entriesByLocalId = {}; // localIds -> objectInfos
var localIds = []; // list of localIds

var localIdCounter = 0; // Inkrement after Usage.

// TODO add parameters for:
// heartbeat intervall
// grpcPort or Addr
//
var heartbeatIntervalInMilliseconds = 10000; // if 0 || < 0  heartbeat not enabled
//var serverAddressAndPort = '0.0.0.0:50051'; Default
var serverAddressAndPort = '0.0.0.0:50052';


function removeEntry(localId) {
    // remove entry from all localIds
    var indexInLocalIds = localIds.indexOf(localId);
    localIds.splice(indexInLocalIds, 1);

    // remove entry from oid specific localId list
    var oid = entriesByLocalId[localId]['oid'];

    var oIdLocalIdArray = entriesByOId[oid];
    var indexInOIdSpecificArray = oIdLocalIdArray.indexOf(localId);
    oIdLocalIdArray.splice(indexInOIdSpecificArray, 1);

    // remove entry from localId Map
    delete entriesByLocalId[localId];
}

//////////////////////////////////////////////////////////////////////////
/////////////////////////// Heartbeat Handling;
///////////////////////////
function heartbeatExecution(localId, grpcServer) {
    var heartbeatClient = new heartbeatService(grpcServer, grpc.credentials.createInsecure());

    heartbeatClient.heartbeat({
            'version':1,
            'timestamp': new Date().valueOf(),
            'local_id': localId
        }, function(err, response) {
            console.log("Object oid: " + entriesByLocalId[localId]['oid'] + " , localId: " + entriesByLocalId[localId]['localId'] + " , symbolic name: " + entriesByLocalId[localId]['symbolicName']);
            if(err !== null){
                removeEntry(localId);
                console.log("Error occured!");
                console.log("Error Message: ");
                console.log(err);
            } else {
                console.log("Response: ");
                console.log(response);
            }
        }
    );
}

function heartbeatExecutionRoutine() {
    console.log("heartbeatExecutionRoutine entered at: " + new Date().valueOf());

    for(var i = 0; i < localIds.length; i++){
        var tempLocalId = localIds[i];
        heartbeatExecution(tempLocalId, entriesByLocalId[tempLocalId]['grpcServer']);
        console.log("execute Heartbeat to: ", tempLocalId);
    }
}

//////////////////////////////////////////////////////////////////////////
/////////////////////////// Object Registration Handling
///////////////////////////
function getNextLocalId() {
    return "" + (localIdCounter++);
}

// Procedure Implementation
function registerObjectImpl(request) {
    console.log("************ New Request ************");
    console.log(request);

    var oid = request['oid'];
    var grpcServer = request['grpc_server'];
    var symbolicName = request['symbolic_name'];
    var timestamp = request['timestamp'];
    var version = request['version'];

    // check if grpcServerAddress is used with the same objectId
    var isAddrUsed = false;
    var localIdOfUsedAddr = '';
    for(var i = 0; i < localIds.length && isAddrUsed === false; i++){
        var tempLocalId = localIds[i];

        if(entriesByLocalId[tempLocalId]['grpcServer'] === grpcServer && entriesByLocalId[tempLocalId]['oid'] === oid){
            isAddrUsed = true;
            localIdOfUsedAddr = tempLocalId;
        }
    }

    var response = request;
    response['success'] = false;

    response['local_id'] = 'None';
    if(isAddrUsed){
        console.log("Existing Entry Returned oid: " + entriesByLocalId[localIdOfUsedAddr]['oid'] + ", localId: " + localIdOfUsedAddr);
        // Return current localId
        response['local_id'] = localIdOfUsedAddr;
        response['success'] = true;
        response['timestamp'] = new Date().valueOf();
    } else {
        // Add new Entry
        var newLocalId = getNextLocalId();
        localIds[localIds.length] = newLocalId;

        // Add new localId to Oid Map
        if(entriesByOId[oid] === undefined){
            entriesByOId[oid] = [];
            entriesByOId[oid][0] = newLocalId;
        } else {
            entriesByOId[oid][entriesByOId[oid].length] = newLocalId;
        }

        // Create localId Entry
        entriesByLocalId[newLocalId] = {};
        entriesByLocalId[newLocalId]['oid'] = oid;
        entriesByLocalId[newLocalId]['localId'] = newLocalId;
        entriesByLocalId[newLocalId]['grpcServer'] = grpcServer;
        entriesByLocalId[newLocalId]['symbolicName'] = symbolicName;
        entriesByLocalId[newLocalId]['timestamp'] = timestamp;

        response['local_id'] = newLocalId;
        response['success'] = true;
        response['timestamp'] = new Date().valueOf();
    }

    console.log("************ Response ************");
    console.log(response);
    return response;
}

function requestObjectsImpl(request) {
    console.log("************ New Request ************");
    console.log(request);
    console.log(entriesByLocalId);

    var oid = request['oid'];
    var json = {};

    var localIdArray = entriesByOId[oid];
    for(var i = 0; localIdArray !== undefined && i < localIdArray.length; i++){
        var tempLocalId = localIdArray[i];
        var tempObjectEntry = entriesByLocalId[tempLocalId];

        console.log("tempObjectEntry");
        console.log(tempObjectEntry);
        json[tempLocalId] = tempObjectEntry;
    }

    var response = request;
    response['json'] = JSON.stringify(json);
    console.log("************ Response ************");
    console.log(response);
    return response;
}

// Procedure Intermediates
function registerObjectInt(call, callback) {
    callback(null, registerObjectImpl(call.request));
}

function requestObjectsInt(call, callback) {
    callback(null, requestObjectsImpl(call.request));
}


/////////////////////////////////////////////////////////
///////////////////////  Server
function getServer() {
    var server = new grpc.Server();
    // HAL Value Input
    server.addService(registryService.service, {
        registerObject: registerObjectInt,
        requestObjects: requestObjectsInt
    });

    return server;
}

var routeServer = getServer();
routeServer.bind(serverAddressAndPort, grpc.ServerCredentials.createInsecure());
routeServer.start();

console.log("Server is running!\nListening bound on: " + serverAddressAndPort);

/////////////////////////////////////////////////////////
///////////////////////  Client
///////////////////////  Check Entries Periodically
// Do a Heartbeat every 5 Seconds

if (heartbeatIntervalInMilliseconds > 0){
    var intervalID = setInterval(heartbeatExecutionRoutine, heartbeatIntervalInMilliseconds);
}
//clearInterval(intervalID); // Set to deactivate Heartbeat