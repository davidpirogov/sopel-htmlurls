import unittest

from sopel_htmlurls.urls import get_urls_from_string, is_url_valid

class TestHtmlUrlsValidation(unittest.TestCase):
    """
    https://docs.python.org/3.8/library/unittest.html#basic-example
    """


    TEXT_WITH_VALID_URLS = [
        "and then there's https://hackaday.com/2018/01/18/cardboard-wall-is-surprisingly-well-built/",
        "https://www.yahoo.com.au/ for the rest of it",
        "here is some text https://lowtech.io/ with a URL between",
        "here are two urls https://www.google.com and https://finance.yahoo.com/with-a-path between text",
        "https://domain.com/?q1=foo&q2=bar&q3=baz with text and newline \n at the end",
        "https://www.domain.com/?q[]=foo&q[]=bar&q[]=baz &some-text-space",
        "More URLs are https://www6.domain.com:8081 and https://www12.domain.com:9000/some-path/123/?query=1"
    ]

    TEXT_WITH_VALID_URLS_EXPECTED_RESULT = [
        ["https://hackaday.com/2018/01/18/cardboard-wall-is-surprisingly-well-built/"],
        ["https://www.yahoo.com.au/"],
        ["https://lowtech.io/"],
        ["https://www.google.com", "https://finance.yahoo.com/with-a-path"],
        ["https://domain.com/?q1=foo&q2=bar&q3=baz"],
        ["https://www.domain.com/?q[]=foo&q[]=bar&q[]=baz"],
        ["https://www6.domain.com:8081", "https://www12.domain.com:9000/some-path/123/?query=1"]
    ]

    def test_check_valid_https_urls(self):
        """
        Tests a set of valid urls that start with https
        """

        for idx, text in enumerate(self.TEXT_WITH_VALID_URLS):
            assert get_urls_from_string(text) == self.TEXT_WITH_VALID_URLS_EXPECTED_RESULT[idx]

    def test_validate_urls(self):
        """
        Tests that the urls can be validated
        """

        for text in self.TEXT_WITH_VALID_URLS:
            extracted_urls = get_urls_from_string(text)
            for url in extracted_urls:
                assert is_url_valid(url) is True


    def test_invalid_urls(self):
        """
        Tests source strings for invalid urls
        """

        for url in self.TEXT_WITH_VALID_URLS:
            assert is_url_valid(url) is False

if __name__ == '__main__':
    unittest.main()
