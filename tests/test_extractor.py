from linkextractor import *

import BeautifulSoup

html1 = """
<html>
   <head><base href="http://some.net"/></head>
   <body>
      <p>test</p>
      <img src="http://1"/>
      <link rel="stylesheet" href="http://2"></link>
      <STYLE TYPE="text/css" MEDIA="screen, projection">
      <!--
        @import url(http://www.htmlhelp.com/style.css);
        @import url('stylesheets/punk.css');
        @import url("http://www.htmlhelp2.com/2style.css");
        DT { background: yellow; color: black }
      -->
      </STYLE>

   </body>
</html>
"""

testdata = [html1]

def test_baseurl(html):
   assert get_baseurl(html) == "http://some.net"

def test_cssimport(html):
   assert extract_css_imports(html) == ["http://www.htmlhelp.com/style.css"]
   
if __name__=="__main__":
   print "extracts:\n", extract_resourceurls(html)
   print "expander:\n", expand_urls(html, base="http:/test.fi")
   html, links = replace_links(html, replacer = lambda x: "XYZ")
   print html
   print links
