import pytest
from charset_normalizer import CharsetNormalizerMatches as CnM


@pytest.fixture(scope="module")
def lorem():
    yield "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."


@pytest.fixture(scope="module")
def chinese():
    yield "海島算經 淮南子 淮南子 淮南子 some chinese text"


def normalize(byte_string):
    return (
        CnM.from_bytes(byte_string, preemptive_behaviour=True, explain=False)
        .best()
        .first()
    )


def test_ascii(lorem):
    ascii = normalize(lorem.encode("ascii"))
    assert ascii.encoding == "ascii"


def test_utf_8(lorem):
    utf8 = normalize(lorem.encode("utf-8"))
    assert (
        utf8.encoding == "ascii"
    )  # original was utf-8 but ascii fits regular characters


def test_utf8_chinese(chinese):
    utf8_chinese = normalize(chinese.encode("utf-8"))
    assert utf8_chinese.encoding == "utf_8"


def test_html5():
    html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
              <meta charset="UTF-8">
              <meta http-equiv="X-UA-Compatible" content="IE=edge">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
              <title>Document</title>
            </head>
              <body>
              </body>
            </html>""".encode(
        "utf-8"
    )
    html = normalize(html)
    assert html.encoding == "ascii"


def test_decoing_ascii(lorem):
    encoded = lorem.encode("ascii")
    ascii = normalize(encoded)
    assert encoded.decode(ascii.encoding) == lorem


def test_decoding_utf_8(lorem):
    encoded = lorem.encode("utf-8")
    utf8 = normalize(encoded)
    assert encoded.decode(utf8.encoding) == lorem


def test_decoding_utf8_chinese(chinese):
    encoded = chinese.encode("utf-8")
    utf8_chinese = normalize(encoded)
    assert encoded.decode(utf8_chinese.encoding) == chinese
