linkextractor - HTML link extraction
=====================================

This library aims to provide means for extracting links from both HTML
and plain text. For that, it uses a combination of lxml, BeautifulSoup and
regular expressions.

It is built with linked resource retrieval in mind, so it tries very hard
to find all links in a document.

For HTML, the library supports:

* extraction of any link found in SRC or HREF attribute
* extraction of CSS import links
 
For plaintext documents:

* extraction of all valid URLs

Optional functionality

* validate and fix the source documents prior to parsing
* extract BASE URL and expand relative URLs

Usage:

>>> from linkextractor import from_html()
>>> docs_iter = [doc1, doc2, doc3]
>>> linksets = [links for links in from_html(docs_iter)]

The from_html call is a generator that yields lists of links found in
each document. Besides an iterable producing source documents, It takes
the following optional boolean keywords:

* validate - whether to validate the document beforehand
* fix - whether to also fix it (implies validate=True)
* expand - whether to expand relative URLs

Similarly importable from_text(docs_iter) function behaves the same, except
that it takes no keyword arguments; all links in text documents are expected
to be well-formed valid URLs.

