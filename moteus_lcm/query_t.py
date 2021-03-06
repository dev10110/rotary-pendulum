"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class query_t(object):
    __slots__ = ["mode", "position"]

    __typenames__ = ["int16_t", "double"]

    __dimensions__ = [None, None]

    def __init__(self):
        self.mode = 0
        self.position = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(query_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">hd", self.mode, self.position))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != query_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return query_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = query_t()
        self.mode, self.position = struct.unpack(">hd", buf.read(10))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if query_t in parents: return 0
        tmphash = (0x9ec8874dd74bc04f) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if query_t._packed_fingerprint is None:
            query_t._packed_fingerprint = struct.pack(">Q", query_t._get_hash_recursive([]))
        return query_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

