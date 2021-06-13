import pytest
import requests

from htmlparser.parser import HTMLParser


@pytest.fixture(scope="module")
def htmlparser():
    yield HTMLParser(["script", "noscript", "style", "custom", "select"])


def test_incomplete_html(htmlparser):
    output = htmlparser.parse("<p>", pretty_xml=False)
    EXPECTED = "<data><html><head></head><body><p></p></body></html></data>"
    assert output == EXPECTED


def match_output_vs_expected(tests, subtests, htmlparser):
    for testcase in tests:
        with subtests.test(test=testcase["test"]):
            output = htmlparser.parse(testcase["test"], pretty_xml=False)
            assert output == testcase["expected"]


def test_broken_html(htmlparser, subtests):
    tests = (
        {
            "test": "</p>",
            "expected": "<data><html><head></head><body></body></html></data>",
        },
        {
            "test": "</div><p>",
            "expected": "<data><html><head></head><body><p></p></body></html></data>",
        },
        {
            "test": "</a></p></b>",
            "expected": "<data><html><head></head><body></body></html></data>",
        },
        {
            "test": "</p></p></p></p></p>",
            "expected": "<data><html><head></head><body></body></html></data>",
        },
        {
            "test": "<p></b>",
            "expected": "<data><html><head></head><body><p></p></body></html></data>",
        },
        {
            "test": "<div><h1>hello world</p></div>",
            "expected": "<data><html><head></head><body><div><h1>hello world<p></p></h1></div></body></html></data>",
        },
    )
    match_output_vs_expected(tests, subtests, htmlparser)


def test_html_entities(htmlparser, subtests):
    tests = (
        {
            "test": "&lt;",
            "expected": "<data><html><head></head><body>&lt;</body></html></data>",
        },
        {
            "test": "&gt;",
            "expected": "<data><html><head></head><body>&gt;</body></html></data>",
        },
        {
            "test": "&gt;&lt;&gt;",
            "expected": "<data><html><head></head><body>&gt;&lt;&gt;</body></html></data>",
        },
        {
            "test": "&gt;&lt;&gt;&gt;&lt;&gt;&gt;&lt;&gt;",
            "expected": "<data><html><head></head><body>&gt;&lt;&gt;&gt;&lt;&gt;&gt;&lt;&gt;</body></html></data>",
        },
        {
            "test": "&lt;p&gt;",
            "expected": "<data><html><head></head><body>&lt;p&gt;</body></html></data>",
        },
        {
            "test": "&amp;",
            "expected": "<data><html><head></head><body>&amp;</body></html></data>",
        },
        {
            "test": "&quot;",
            "expected": '<data><html><head></head><body>"</body></html></data>',
        },
        {
            "test": "&apos;",
            "expected": "<data><html><head></head><body>'</body></html></data>",
        },
        {
            "test": "&apos;&gt;&apos;&quot;",
            "expected": "<data><html><head></head><body>'&gt;'\"</body></html></data>",
        },
    )
    match_output_vs_expected(tests, subtests, htmlparser)


def test_no_unexpected_errors(htmlparser, subtests):
    urls = [
        "https://www.google.com",
        "https://github.com/" "https://www.youtube.com/",
        "https://www.reddit.com/",
        "https://www.facebook.com",
        "https://www.baidu.com/",
        "https://www.banggood.com/?akmClientCountry=NL&",
    ]
    for url in urls:
        with subtests.test(url=url):
            response = requests.get(url).text
            htmlparser.parse(response)


def test_exclude(htmlparser, subtests):
    tests = (
        {
            "test": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <title>Document</title>
                <script>test</script>
                </head>
                <body>
                    <script>test</script>
                </body>
                </html>
                """,
            "expected": "<data><html><head><title>Document</title></head><body></body></html></data>",
        },
        {
            "test": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <title>Document</title>
                <script>test</script>
                </head>
                <body>
                    <script>test<p>hello world</p></script>
                </body>
                </html>
                """,
            "expected": "<data><html><head><title>Document</title></head><body></body></html></data>",
        },
        {
            "test": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <title>Document</title>
                </head>
                <body>
                    <noscript>test</noscript>
                </body>
                </html>
                """,
            "expected": "<data><html><head><title>Document</title></head><body></body></html></data>",
        },
        {
            "test": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <script>test</script>
                <title>Document</title>
                <script>test</script>
                </head>
                <body>
                    <script>test</script>
                    <custom>test</custom>
                </body>
                </html>
                """,
            "expected": "<data><html><head><title>Document</title></head><body></body></html></data>",
        },
        {
            "test": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <script>test</script>
                <title>Document</title>
                <script>test</script>
                <custom>test</custom>
                </head>
                <body>
                    <script>test</script>
                    <custom>test
                    <custom>test</custom></custom>
                </body>
                </html>
                """,
            "expected": "<data><html><head><title>Document</title></head><body></body></html></data>",
        },
        {
            "test": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <script>test</script>
                <title>Document</title>
                <script>test</script>
                </head>
                <body>
                    <p><script>test</script>hello</p>
                    <script>test</script>
                    <custom>test</custom>
                </body>
                </html>
                """,
            "expected": "<data><html><head><title>Document</title></head><body><p>hello</p></body></html></data>",
        },
        {
            "test": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <script>test</script>
                <title>Document</title>
                <script>test</script>
                </head>
                <body>
                    <p><script>test</script><b>hello</b></p>
                    <script>test</script>
                    <custom>test</custom>
                </body>
                </html>
                """,
            "expected": "<data><html><head><title>Document</title></head><body><p><b>hello</b></p></body></html></data>",
        },
        {
            "test": """
                <form>
                    <select id='languageselect'>
                        <option>မြန်မာ</option>
                        <option>ខ្មែរ</option>
                        <option>한국어</option>
                        <option>日本語</option>
                        <option>简体中文</option>
                        <option>繁體中文</option>
                        <option>繁體中文 (香港)</option>
                    </select>
                </form>
            """,
            "expected": "<data><html><head></head><body><form></form></body></html></data>",
        },
    )
    for test in tests:
        with subtests.test(test=test):
            assert test["expected"] == htmlparser.parse(test["test"], pretty_xml=False)


def test_tag_attributes(htmlparser, subtests):
    tests = (
        {
            "test": '<p class="classy_attribute"/>',
            "expected": "<data><html><head></head><body><p class='classy_attribute'></p></body></html></data>",
        },
        {
            "test": '<p id="classy_attribute"/>',
            "expected": "<data><html><head></head><body><p id='classy_attribute'></p></body></html></data>",
        },
        {
            "test": '<p onclick="some random shit"/>',
            "expected": "<data><html><head></head><body><p></p></body></html></data>",
        },
        {
            "test": '<p mousedown="some random shit"/>',
            "expected": "<data><html><head></head><body><p></p></body></html></data>",
        },
        {
            "test": """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <script>test</script>
                <title>Document</title>
                <script>test</script>
                </head>
                <body>
                    <p class="aardappel"><script>test</script><b>hello</b></p>
                    <script>test</script>
                    <custom>test</custom>
                </body>
                </html>
                """,
            "expected": "<data><html><head><title>Document</title></head><body><p class='aardappel'><b>hello</b></p></body></html></data>",
        },
    )

    for test in tests:
        with subtests.test(test=test):
            assert test["expected"] == htmlparser.parse(test["test"], pretty_xml=False)
