import unittest
from crawl import (
    normalize_url, 
    get_heading_from_html, 
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data,
    )

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
    
    def test_get_urls_from_html_absolute(self):
        # Absolute URL should be returned as-is
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        # Relative URL should be turned into an absolute URL
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/path/one"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one"]
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_multiple(self):
        # should find every <a> tag
        input_url = "https://crawler-test.com"
        input_body = '''
        <html><body>
            <a href="/path/one">Link 1</a>
            <a href="https://other.com/path">Link 2</a>
        </body></html>
        '''
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/path/one",
            "https://other.com/path",
        ]
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_relative(self):
        # relative image src should become absolute
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        # absolute image src should be returned as-is
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_multiple(self):
        # should find every <img> tag
        input_url = "https://crawler-test.com"
        input_body = '''
        <html><body>
            <img src="/logo.png" alt="Logo">
            <img src="https://other.com/image.jpg" alt="Other">
        </body></html>
        '''
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/logo.png",
            "https://other.com/image.jpg",
        ]
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        # Basic happy-path: page has a heading, paragraph, link and image
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_missing_elements(self):
        # page is missing a paragraph and an image
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Only a heading</h1>
            <a href="/link1">Link 1</a>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Only a heading",
            "first_paragraph": "",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)
    
    def test_extract_page_data_empty(self):
        # completely empty page
        input_url = "https://crawler-test.com"
        input_body = "<html><body></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()