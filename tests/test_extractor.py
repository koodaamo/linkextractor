import copy
from linkextractor import *


base_url = "http://some.net"
import_css_links = ["http://www.htmlhelp.com/style.css", "stylesheets/punk.css", "http://www.htmlhelp2.com/2style.css"]
img_links = ["http://1"]
rel_stylesheet = "http://2"

SOURCE = open("tests/source.html").read()
EXPANDED = open("tests/expanded.html").read()

def test_baseurl(html=SOURCE):
   assert get_baseurl(html) == base_url

def test_cssimport(html=SOURCE):
   assert extract_css_imports(html) == import_css_links

def test_resourceurls(html=SOURCE):
   assert extract_resourceurls(html) == img_links + [rel_stylesheet] + import_css_links  

def test_expander(html=SOURCE):
   expanded = copy.copy(import_css_links)
   expanded[1] = base_url + "/" + expanded[1]
   result = img_links + [rel_stylesheet] + expanded
   assert expand_urls(html) == result

def test_replacelinks(html=SOURCE):
   transformed_html = ""
   html, links = replace_links(html, replacer = lambda x: "XYZ")
   assert html == EXPANDED
   
