import HTMLParser, logging
from BeautifulSoup import BeautifulSoup, SoupStrainer
from urlparse import urlparse
#from misc import get_timestamp

import requests

__all__ = ("html", "process_links", "replace_links")


logger = logging.getLogger("links")


def filter_redirects(url_list, redirected=True):
   "generator that by default filters out redirected urls"
   table = {}
   for url in url_list:
      table[url] = True if requests.get(url).history else False
   return table

 
def get_baseurl(html):
   "get the base url"
   constrained = SoupStrainer(["BASE","base"])
   base = BeautifulSoup(html, parseOnlyThese=constrained).find(["BASE","base"])
   return base.get("href") or base.get("HREF")
   

def expand_urls(html, base=None):
   url = urlparse(base or "http://")
   base = get_baseurl(html) or url[0] + "://" + url[1]
   links = extract_resourceurls(html)
   replacer = lambda url: url if url.startswith("http://") else '/'.join([base.rstrip('/'), url.lstrip('/')])
   return [(link, replacer(link)) for link in links]


def extract_resourceurls(html, custom=False):
   "get all found links, using BeautifulSoup or a custom parser"

   if custom:
      p = LinkedResourceParser()
      try:
         links = p.feed(html)
      except Exception, e:
         logger.error("html parse failed: %s" % e)
   else:
      constraint = SoupStrainer(["img","link"])
      data = BeautifulSoup(html, parseOnlyThese=constraint)
      links = [l.get("src") or l.get("href") for l in data]

   return links + extract_css_imports(html)


def replace_links(html, replacer=None):
   if not replacer:
      replacer = lambda x: "XXX"
   p = LinkedResourceParser()
   try:
      p.feed(html)
   except Exception, e:
      logger.error("html parse failed: %s" % e)
      return (html, [])

   for link in p:
      html = html.replace(link, replacer(link))
   
   html, importlinks = replace_css_imports(html, replacer=replacer)
   return (html, p.keys() + importlinks)
   

class LinkedResourceParser(HTMLParser.HTMLParser, dict):

   def handle_starttag(self, tag, attrs):
      try:
         getattr(self, "do_" + tag)(attrs)
      except:
         pass
      
   def do_link(self, attrs):
      self[dict(attrs)["href"].strip("\"'")] = self.getpos()
      
   def do_img(self, attrs):
      self[dict(attrs)["src"].strip("\"'")] = self.getpos()
      
   #def do_a(self, attrs):
   #   process links, mailto;s, ...


def extract_css_imports(html):
   "get links in @import url(http://...) statements"
   out = []
   links = []
   END = False
   start = 0
   
   while 1:
      pos = html.find("@import url(", start)
      if pos==-1:
         out.append(html[start:])
         break
      end = html.find(')', pos)
      link = html[pos+12:end]
      links.append(link.strip("\"'"))
      start = end + 1 
      
   return links


def replace_css_imports(html, replacer=None):
   "replace links in @import url(http://...) statements"
   if not replacer:
      replacer = lambda x: "XXX"
   
   out = []
   links = []
   END = False
   start = 0
   
   while 1:
      pos = html.find("@import url(", start)
      if pos==-1:
         out.append(html[start:])
         break
      end = html.find(')', pos)
      link = html[pos+12:end]
      links.append(link.strip("\"'"))
      out.append(html[start:pos+12])
      out.append(replacer(link) + ")")
      start = end + 1 
      
   return ("".join(out), links)
      
      
def link_select(element):
   attrnames = [attr[0] for attr in element.attrs]
   if element.name in ("link", "img", "script"): #and ("src" in attrnames or "href" in attrnames):
      return True
   else:
      return False
      

def process_links(soup, baseurl=None, buidfunc=get_timestamp):
   "return all link urls referred to from the html"
   links = soup.findAll(link_select)

   urls = []
   
   for link in links:
      
      # 1. get link url attribute
      try:
         url = link["src"]
         attr = "src"
      except:
         url = link["href"]
         attr = "href"

      # 2. expand any relative urls
      if url[:4] != "http":
         
         base = urlparse(baseurl)
         if url[0] == '/':
            url = "http://" + base.hostname + url
         else:
            url = base.geturl() + url
            
         #except AttributeError:
         #   raise Exception("relative url encountered: baseurl argument is required")
            
      urls.append(url)
      
      # 3. replace links with local ones
      url = urlparse(url)
      link[attr] = "".join((url.hostname or "", buidfunc(), url.path))       

   return urls


def extract():
   ""
