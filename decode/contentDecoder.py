from io import BytesIO

import gzip
import zlib
import brotli
import zstandard as zstd

from typing import Union, Optional, AnyStr, overload

class ContentDecoder:
    def __init__(self):
        self.custom_decode()

    def decode(
        self, flow, encoding: str
    ) -> Union[None, str, bytes]:
        """
        Decode the given input object
        Returns:
            The decoded value
        Or:
            None
        """
        if flow.response.raw_content is None:
            return None

        try:
            #check whether compression is a single compression
            if encoding in ("gzip", "deflate", "br", "zstd"):
                decoded = self.custom_decode[encoding](flow.response.raw_content)
                return decoded
            else:
                #multiple compressions have been used
                compressions = self.custom_decode[encoding]

                for method in compressions:
                    method(flow.response.raw_content)
        except:
            for decompressionMethod in self.custom_decode:
                try:
                    decoded = self.custom_decode[decompressionMethod](flow.response.raw_content)
                    return decoded
                except:
                    pass
            return None


    def identity(self, content):
        """
            Returns content unchanged. Identity is the default value of
            Accept-Encoding headers.
        """
        return content


    def decode_gzip(self, content: bytes) -> bytes:
        if not content:
            return b""
        gfile = gzip.GzipFile(fileobj=BytesIO(content))
        return gfile.read()

    def decode_brotli(self, content: bytes) -> bytes:
        if not content:
            return b""
        return brotli.decompress(content)

    def decode_zstd(self, content: bytes) -> bytes:
        if not content:
            return b""
        zstd_ctx = zstd.ZstdDecompressor()
        try:
            return zstd_ctx.decompress(content)
        except zstd.ZstdError:
            # If the zstd stream is streamed without a size header,
            # try decoding with a 10MiB output buffer
            return zstd_ctx.decompress(content, max_output_size=10 * 2 ** 20)

    def decode_deflate(self, content: bytes) -> bytes:
        """
            CAUTION
            Returns decompressed data for DEFLATE. Some servers may respond with
            compressed data without a zlib header or checksum. An undocumented
            feature of zlib permits the lenient decompression of data missing both
            values.
            http://bugs.python.org/issue5784
        """
        if not content:
            return b""
        try:
            return zlib.decompress(content)
        except zlib.error:
            return zlib.decompress(content, -15)

    def custom_decode(self):
        self.custom_decode = {
            "gzip": self.decode_gzip,
            "deflate": self.decode_deflate,
            "deflateRaw": self.decode_deflate,
            "br": self.decode_brotli,
            "zstd": self.decode_zstd,
            "identity": self.identity,
            "none": self.identity
        }



# [
#       'gzip, deflate, br',
#       'gzip, deflate',
#       'gzip, br',
#       'gzip, deflate, br',
#       'deflate, br',
#       'gzip, deflate',
#       'gzip, br',
#       'deflate, br',
#     ]