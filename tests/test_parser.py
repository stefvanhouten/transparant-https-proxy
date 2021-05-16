import pytest

from htmlparser.parser import HTMLParser

EXCLUDE = (
    "script",
    "noscript",
    "html",
    "style",
)


@pytest.fixture(scope="module")
def htmlparser():
    yield HTMLParser(EXCLUDE)


@pytest.fixture(scope="module")
def path_to_files():
    yield (
        "/home/stef/devel/transparant-https-proxy/tests/websites/so.html",
        "/home/stef/devel/transparant-https-proxy/tests/websites/baidu.html",
    )


def test_incomplete_html(htmlparser):
    output = htmlparser.parse("<p>", pretty_xml=False)
    EXPECTED = "<data><head></head><body><p></p></body></data>"
    assert output == EXPECTED


def match_output_vs_expected(tests, subtests, htmlparser):
    for testcase in tests:
        with subtests.test(test=testcase["test"]):
            output = htmlparser.parse(testcase["test"], pretty_xml=False)
            assert output == testcase["expected"]


def test_broken_html(htmlparser, subtests):
    tests = (
        {"test": "</p>", "expected": "<data><head></head><body></body></data>"},
        {
            "test": "</div><p>",
            "expected": "<data><head></head><body><p></p></body></data>",
        },
        {"test": "</a></p></b>", "expected": "<data><head></head><body></body></data>"},
        {
            "test": "</p></p></p></p></p>",
            "expected": "<data><head></head><body></body></data>",
        },
        {
            "test": "<p></b>",
            "expected": "<data><head></head><body><p></p></body></data>",
        },
        {
            "test": "<div><h1>hello world</p></div>",
            "expected": "<data><head></head><body><div><h1>hello world<p></p></h1></div></body></data>",
        },
    )
    match_output_vs_expected(tests, subtests, htmlparser)


def test_html_entities(htmlparser, subtests):
    tests = (
        {"test": "&lt;", "expected": "<data><head></head><body>&lt;</body></data>"},
        {"test": "&gt;", "expected": "<data><head></head><body>&gt;</body></data>"},
        {
            "test": "&lt;p&gt;",
            "expected": "<data><head></head><body>&lt;p&gt;</body></data>",
        },
        {"test": "&amp;", "expected": "<data><head></head><body>&amp;</body></data>"},
        {
            "test": "&quot;",
            "expected": '<data><head></head><body>"</body></data>',
        },  # Apparently &qout is accepted to escape to "
        {
            "test": "&apos;",
            "expected": "<data><head></head><body>'</body></data>",
        },  # Same here for &apos to be '
    )
    match_output_vs_expected(tests, subtests, htmlparser)


def test_no_unexpected_errors(htmlparser, subtests, path_to_files):
    for path_to_file in path_to_files:
        with subtests.test(path_to_file=path_to_file):
            htmlparser.parse(path_to_file)


def test_exclude(htmlparser, subtests):
    tests = (
        {
            "test": "<script>script</script",
            "expected": "<data><head></head><body></body></data>",
        },
        {
            "test": "<noscript>noscript</noscript>",
            "expected": "<data><head></head><body></body></data>",
        },
        {
            "test": "<style>noscript</style>",
            "expected": "<data><head></head><body></body></data>",
        },
    )
    for test in tests:
        with subtests.test(test=test):
            assert test["expected"] == htmlparser.parse(test["test"], pretty_xml=False)


def test_tag_attributes(htmlparser, subtests):
    tests = (
        {
            "test": '<p class="classy_attribute"/>',
            "expected": "<data><head></head><body><p class='classy_attribute'></p></body></data>",
        },
        {
            "test": '<p id="classy_attribute"/>',
            "expected": "<data><head></head><body><p id='classy_attribute'></p></body></data>",
        },
        {
            "test": '<p onclick="some random shit"/>',
            "expected": "<data><head></head><body><p></p></body></data>",
        },
        {
            "test": '<p mousedown="some random shit"/>',
            "expected": "<data><head></head><body><p></p></body></data>",
        },
    )

    for test in tests:
        with subtests.test(test=test):
            assert test["expected"] == htmlparser.parse(test["test"], pretty_xml=False)
