from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AccountStatus(_message.Message):
    __slots__ = ["AccountStatus"]
    ACCOUNTSTATUS_FIELD_NUMBER: _ClassVar[int]
    AccountStatus: bool
    def __init__(self, AccountStatus: bool = ...) -> None: ...

class Credentials(_message.Message):
    __slots__ = ["password", "username"]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    password: str
    username: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ["content", "recipient", "sent_time"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    SENT_TIME_FIELD_NUMBER: _ClassVar[int]
    content: str
    recipient: str
    sent_time: str
    def __init__(self, content: _Optional[str] = ..., sent_time: _Optional[str] = ..., recipient: _Optional[str] = ...) -> None: ...

class MessageStatus(_message.Message):
    __slots__ = ["message_status"]
    MESSAGE_STATUS_FIELD_NUMBER: _ClassVar[int]
    message_status: int
    def __init__(self, message_status: _Optional[int] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ["request_status"]
    REQUEST_STATUS_FIELD_NUMBER: _ClassVar[int]
    request_status: int
    def __init__(self, request_status: _Optional[int] = ...) -> None: ...
