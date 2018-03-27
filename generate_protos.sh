# Generate python grpc files 
python -m grpc_tools.protoc -I./proto --python_out=./sensor/pi_python/ --grpc_python_out=./sensor/pi_python/ proto/Chair.proto
