# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Chair.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='Chair.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x0b\x43hair.proto\"P\n\x05\x43hair\x12\x0f\n\x07version\x18\x01 \x01(\x05\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\x12\x13\n\x0bsensor_type\x18\x03 \x01(\x05\x12\x0e\n\x06values\x18\x04 \x01(\t\" \n\rChairResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\x37\n\x0c\x43hairService\x12\'\n\x0b\x43hairUpdate\x12\x06.Chair\x1a\x0e.ChairResponse\"\x00\x62\x06proto3')
)




_CHAIR = _descriptor.Descriptor(
  name='Chair',
  full_name='Chair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='Chair.version', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='Chair.timestamp', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sensor_type', full_name='Chair.sensor_type', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='values', full_name='Chair.values', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=95,
)


_CHAIRRESPONSE = _descriptor.Descriptor(
  name='ChairResponse',
  full_name='ChairResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='ChairResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=97,
  serialized_end=129,
)

DESCRIPTOR.message_types_by_name['Chair'] = _CHAIR
DESCRIPTOR.message_types_by_name['ChairResponse'] = _CHAIRRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Chair = _reflection.GeneratedProtocolMessageType('Chair', (_message.Message,), dict(
  DESCRIPTOR = _CHAIR,
  __module__ = 'Chair_pb2'
  # @@protoc_insertion_point(class_scope:Chair)
  ))
_sym_db.RegisterMessage(Chair)

ChairResponse = _reflection.GeneratedProtocolMessageType('ChairResponse', (_message.Message,), dict(
  DESCRIPTOR = _CHAIRRESPONSE,
  __module__ = 'Chair_pb2'
  # @@protoc_insertion_point(class_scope:ChairResponse)
  ))
_sym_db.RegisterMessage(ChairResponse)



_CHAIRSERVICE = _descriptor.ServiceDescriptor(
  name='ChairService',
  full_name='ChairService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=131,
  serialized_end=186,
  methods=[
  _descriptor.MethodDescriptor(
    name='ChairUpdate',
    full_name='ChairService.ChairUpdate',
    index=0,
    containing_service=None,
    input_type=_CHAIR,
    output_type=_CHAIRRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CHAIRSERVICE)

DESCRIPTOR.services_by_name['ChairService'] = _CHAIRSERVICE

# @@protoc_insertion_point(module_scope)
