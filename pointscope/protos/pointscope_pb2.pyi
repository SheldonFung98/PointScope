from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VisRequest(_message.Message):
    __slots__ = ["vedo_init", "o3d_init", "add_pcd", "add_color", "add_lines"]
    VEDO_INIT_FIELD_NUMBER: _ClassVar[int]
    O3D_INIT_FIELD_NUMBER: _ClassVar[int]
    ADD_PCD_FIELD_NUMBER: _ClassVar[int]
    ADD_COLOR_FIELD_NUMBER: _ClassVar[int]
    ADD_LINES_FIELD_NUMBER: _ClassVar[int]
    vedo_init: VedoInit
    o3d_init: O3DInit
    add_pcd: AddPointCloud
    add_color: AddColor
    add_lines: AddLines
    def __init__(self, vedo_init: _Optional[_Union[VedoInit, _Mapping]] = ..., o3d_init: _Optional[_Union[O3DInit, _Mapping]] = ..., add_pcd: _Optional[_Union[AddPointCloud, _Mapping]] = ..., add_color: _Optional[_Union[AddColor, _Mapping]] = ..., add_lines: _Optional[_Union[AddLines, _Mapping]] = ...) -> None: ...

class VisResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: Status
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ...) -> None: ...

class VedoInit(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class O3DInit(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class AddPointCloud(_message.Message):
    __slots__ = ["pcd", "tsfm"]
    PCD_FIELD_NUMBER: _ClassVar[int]
    TSFM_FIELD_NUMBER: _ClassVar[int]
    pcd: Matrix
    tsfm: Matrix
    def __init__(self, pcd: _Optional[_Union[Matrix, _Mapping]] = ..., tsfm: _Optional[_Union[Matrix, _Mapping]] = ...) -> None: ...

class AddColor(_message.Message):
    __slots__ = ["colors"]
    COLORS_FIELD_NUMBER: _ClassVar[int]
    colors: Matrix
    def __init__(self, colors: _Optional[_Union[Matrix, _Mapping]] = ...) -> None: ...

class AddLines(_message.Message):
    __slots__ = ["starts", "ends", "colors"]
    STARTS_FIELD_NUMBER: _ClassVar[int]
    ENDS_FIELD_NUMBER: _ClassVar[int]
    COLORS_FIELD_NUMBER: _ClassVar[int]
    starts: Matrix
    ends: Matrix
    colors: Matrix
    def __init__(self, starts: _Optional[_Union[Matrix, _Mapping]] = ..., ends: _Optional[_Union[Matrix, _Mapping]] = ..., colors: _Optional[_Union[Matrix, _Mapping]] = ...) -> None: ...

class Matrix(_message.Message):
    __slots__ = ["data", "shape"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedScalarFieldContainer[float]
    shape: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, data: _Optional[_Iterable[float]] = ..., shape: _Optional[_Iterable[int]] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ["ok"]
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    def __init__(self, ok: bool = ...) -> None: ...
