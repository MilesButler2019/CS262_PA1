# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\"H\n\x07Message\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\x12\x11\n\tsent_time\x18\x02 \x01(\t\x12\x0b\n\x03src\x18\x03 \x01(\t\x12\x0c\n\x04\x64\x65st\x18\x04 \x01(\t\"1\n\x0b\x43redentials\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"!\n\x07Request\x12\x16\n\x0erequest_status\x18\x01 \x01(\x05\"8\n\rMessageStatus\x12\x16\n\x0emessage_status\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\"7\n\rAccountStatus\x12\x15\n\rAccountStatus\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\x90\x02\n\x0b\x43hatService\x12&\n\x08getUsers\x12\x08.Request\x1a\x0c.Credentials\"\x00\x30\x01\x12\"\n\x08getInbox\x12\x08.Request\x1a\x08.Message\"\x00\x30\x01\x12/\n\rCreateAccount\x12\x0c.Credentials\x1a\x0e.AccountStatus\"\x00\x12\'\n\x05LogIn\x12\x0c.Credentials\x1a\x0e.AccountStatus\"\x00\x12*\n\x08SendChat\x12\x08.Message\x1a\x0e.MessageStatus\"\x00(\x01\x30\x01\x12/\n\rDeleteAccount\x12\x0c.Credentials\x1a\x0e.AccountStatus\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MESSAGE._serialized_start=14
  _MESSAGE._serialized_end=86
  _CREDENTIALS._serialized_start=88
  _CREDENTIALS._serialized_end=137
  _REQUEST._serialized_start=139
  _REQUEST._serialized_end=172
  _MESSAGESTATUS._serialized_start=174
  _MESSAGESTATUS._serialized_end=230
  _ACCOUNTSTATUS._serialized_start=232
  _ACCOUNTSTATUS._serialized_end=287
  _CHATSERVICE._serialized_start=290
  _CHATSERVICE._serialized_end=562
# @@protoc_insertion_point(module_scope)
