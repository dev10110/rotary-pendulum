"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class command_t(object):
    __slots__ = ["pos", "stop_pos", "vel", "max_torque"]

    __typenames__ = ["double", "double", "double", "double"]

    __dimensions__ = [None, None, None, None]

    def __init__(self):
        self.pos = 0.0
        self.stop_pos = 0.0
        self.vel = 0.0
        self.max_torque = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(command_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">dddd", self.pos, self.stop_pos, self.vel, self.max_torque))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != command_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return command_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = command_t()
        self.pos, self.stop_pos, self.vel, self.max_torque = struct.unpack(">dddd", buf.read(32))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if command_t in parents: return 0
        tmphash = (0xa5068b157f9dda16) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if command_t._packed_fingerprint is None:
            command_t._packed_fingerprint = struct.pack(">Q", command_t._get_hash_recursive([]))
        return command_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)
