from io import BytesIO

import gzip
import zlib
import brotli
import zstandard as zstd

from typing import Union, Optional, AnyStr, overload

class ContentDecoder:
    def __init__(self):
        self.single_compression = {
            "gzip": self.decode_gzip,
            "deflate": self.decode_deflate,
            "deflateRaw": self.decode_deflate,
            "br": self.decode_brotli,
            "zstd": self.decode_zstd,
            "identity": self.identity,
            "none": self.identity
        }

        self.multiple_compression = {
            "gzip, deflate, br, zstd": [self.decode_gzip, self.decode_deflate, self.decode_brotli, self.decode_zstd],
            "gzip, deflate, br": [self.decode_gzip, self.decode_deflate, self.decode_brotli],
            "gzip, deflate, zstd": [self.decode_gzip, self.decode_deflate, self.decode_zstd],
            "gzip, br, zstd": [self.decode_gzip, self.decode_brotli, self.decode_zstd],
            "deflate, br, zstd": [self.decode_deflate, self.decode_brotli, self.decode_zstd],
            "deflate, zstd": [self.decode_deflate, self.decode_zstd],
            "deflate, br": [self.decode_deflate, self.decode_brotli],
            "br, zstd": [self.decode_brotli, self.decode_zstd],
            "gzip, br": [self.decode_gzip, self.decode_brotli],
            "gzip, deflate": [self.decode_gzip, self.decode_deflate],
            "gzip, zstd": [self.decode_gzip, self.decode_zstd]
        }

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

        if not encoding:
            decoded = self.guess_decompression_method(flow)
            return decoded
        
        #check whether compression is a single compression
        if encoding in ("gzip", "deflate", "br", "zstd"):
            decoded = self.single_decode(flow, encoding)
            return decoded
        
        decoded = self.multi_decode(flow, encoding)
        return decoded


    def single_decode(
        self, flow, encoding: str
    ) -> Union[None, str, bytes]:
        try:
            decoded = self.single_compression[encoding](flow.response.raw_content)
        except (brotli.error, zstd.ZstdError, zlib.error, gzip.BadGzipFile):
            decoded = self.guess_decompression_method(flow)

        return decoded

    def multi_decode(
        self, flow, encoding: str
    ) -> Union[None, str, bytes]:
            #multiple compressions have been used -> list is returned
            compressions = self.multiple_compression[encoding]

            decoded = ''

            try:
                for decompressMethod in compressions:
                    if not decoded:
                        decoded = decompressMethod(flow.response.raw_content)
                    else:
                        decoded = decompressMethod(decoded)
            except (brotli.error, zstd.ZstdError, zlib.error, gzip.BadGzipFile):
                decoded = self.guess_decompression_method(flow)
            
            return decoded

    def guess_decompression_method(self, flow):
        decoded = ''

        # check for multiple compression combinations. header cannot be trusted
        for decompressionMethod in self.multiple_compression:
            try:
                for decompressMethod in self.multiple_compression[decompressionMethod]:
                    if not decoded:
                        decoded = decompressMethod(flow.response.raw_content)
                    else:
                        decoded = decompressMethod(decoded)

                return decoded
            except (brotli.error, zstd.ZstdError, zlib.error, gzip.BadGzipFile):
                # reset to prevent new cycle from appending to old cycle
                decoded = ''

        # check for each single compression. Header cannot be trusted
        for decompressionMethod in self.single_compression:
            try:
                decoded = self.single_compression[decompressionMethod](flow.response.raw_content)
                return decoded
            except (brotli.error, zstd.ZstdError, zlib.error, gzip.BadGzipFile):
                pass

        

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