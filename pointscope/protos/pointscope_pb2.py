# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pointscope/protos/pointscope.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"pointscope/protos/pointscope.proto\x12\npointscope\"\xfd\x01\n\nVisRequest\x12)\n\tvedo_init\x18\x01 \x01(\x0b\x32\x14.pointscope.VedoInitH\x00\x12\'\n\x08o3d_init\x18\x02 \x01(\x0b\x32\x13.pointscope.O3DInitH\x00\x12,\n\x07\x61\x64\x64_pcd\x18\x03 \x01(\x0b\x32\x19.pointscope.AddPointCloudH\x00\x12)\n\tadd_color\x18\x04 \x01(\x0b\x32\x14.pointscope.AddColorH\x00\x12)\n\tadd_lines\x18\x05 \x01(\x0b\x32\x14.pointscope.AddLinesH\x00\x42\x17\n\x15visualization_request\"1\n\x0bVisResponse\x12\"\n\x06status\x18\x01 \x01(\x0b\x32\x12.pointscope.Status\"\n\n\x08VedoInit\"B\n\x07O3DInit\x12\x11\n\tshow_coor\x18\x01 \x01(\x08\x12$\n\x08\x62g_color\x18\x02 \x01(\x0b\x32\x12.pointscope.Matrix\"R\n\rAddPointCloud\x12\x1f\n\x03pcd\x18\x01 \x01(\x0b\x32\x12.pointscope.Matrix\x12 \n\x04tsfm\x18\x02 \x01(\x0b\x32\x12.pointscope.Matrix\".\n\x08\x41\x64\x64\x43olor\x12\"\n\x06\x63olors\x18\x01 \x01(\x0b\x32\x12.pointscope.Matrix\"t\n\x08\x41\x64\x64Lines\x12\"\n\x06starts\x18\x01 \x01(\x0b\x32\x12.pointscope.Matrix\x12 \n\x04\x65nds\x18\x02 \x01(\x0b\x32\x12.pointscope.Matrix\x12\"\n\x06\x63olors\x18\x03 \x01(\x0b\x32\x12.pointscope.Matrix\"%\n\x06Matrix\x12\x0c\n\x04\x64\x61ta\x18\x01 \x03(\x02\x12\r\n\x05shape\x18\x02 \x03(\x05\"\x14\n\x06Status\x12\n\n\x02ok\x18\x01 \x01(\x08\x32Y\n\nPointScope\x12K\n\x14VisualizationSession\x12\x16.pointscope.VisRequest\x1a\x17.pointscope.VisResponse(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pointscope.protos.pointscope_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_VISREQUEST']._serialized_start=51
  _globals['_VISREQUEST']._serialized_end=304
  _globals['_VISRESPONSE']._serialized_start=306
  _globals['_VISRESPONSE']._serialized_end=355
  _globals['_VEDOINIT']._serialized_start=357
  _globals['_VEDOINIT']._serialized_end=367
  _globals['_O3DINIT']._serialized_start=369
  _globals['_O3DINIT']._serialized_end=435
  _globals['_ADDPOINTCLOUD']._serialized_start=437
  _globals['_ADDPOINTCLOUD']._serialized_end=519
  _globals['_ADDCOLOR']._serialized_start=521
  _globals['_ADDCOLOR']._serialized_end=567
  _globals['_ADDLINES']._serialized_start=569
  _globals['_ADDLINES']._serialized_end=685
  _globals['_MATRIX']._serialized_start=687
  _globals['_MATRIX']._serialized_end=724
  _globals['_STATUS']._serialized_start=726
  _globals['_STATUS']._serialized_end=746
  _globals['_POINTSCOPE']._serialized_start=748
  _globals['_POINTSCOPE']._serialized_end=837
# @@protoc_insertion_point(module_scope)
