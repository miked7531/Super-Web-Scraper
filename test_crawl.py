import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_trailing_slash(self):
        # test that a trailing slash is removed
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_http(self):
        # test that http:// is treated the same as https://
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_http_with_trailing_slash(self):
        # test both http and a trailing slash together
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_get_heading_from_html_basic(self):
        # Basic case: an <h1> is present
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)
    
    def test_get_heading_from_html_h2_fallback(self):
        # when there is no <h1>, fall back to <h2>
        input_body = "<html><body><h2>Secondary Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Secondary Title"
        self.assertEqual(actual, expected)
    
    def test_get_heading_from_html_none(self):
        # when neither <h1> nor <h2> exists, return empty string
        input_body = "<html><body><p>No headings here</p></body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)
    
    def test_get_first_paragraph_from_html_main_priority(self):
        # prefer the <p> that lives inside <main>
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)
    
    def test_get_first_paragraph_from_html_no_main(self):
        # when there is no <main>, just take the first <p> in the document
        input_body = """<html><body>
            <p>First paragraph.</p>
            <p>Second paragraph.</p>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)
    
    def test_get_first_paragraph_from_html_none(self):
        # When no <p> tag exists at all, return empty string
        input_body = "<html><body><h1>No paragraphs here</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()