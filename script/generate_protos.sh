# Generate python grpc files 
python -m grpc_tools.protoc -I../proto --python_out=../src/hal/pi/ --grpc_python_out=../src/hal/pi/ ../proto/chair.proto
