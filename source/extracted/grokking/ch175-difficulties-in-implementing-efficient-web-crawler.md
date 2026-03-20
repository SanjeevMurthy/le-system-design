# Difficulties in implementing efficient web crawler

> Source: System Design - Grokking (Notes), Chapter 175, Pages 46-46

## Key Concepts

- another for videos, where each module extracts what is considered interesting for that media type.
Let’s assume for now that our crawler is going to deal with HTML only, but it should be extensible an

## Content

another for videos, where each module extracts what is considered interesting for that media type.
Let’s assume for now that our crawler is going to deal with HTML only, but it should be extensible and
make it easy to add support for new media types.
What protocols are we looking at? HTTP? What about FTP links? What different
protocols should our crawler handle? For the sake of the exercise, we will assume HTTP. Again,
it shouldn’t be hard to extend the design to use FTP and other protocols later.
What is the expected number of pages we will crawl? How big will the URL database
become? Let’s assume we need to crawl one billion websites. Since a website can contain many, many
URLs, let’s assume an upper bound of 15 billion different web pages that will be reached by our
crawler.
What is ‘RobotsExclusion’ and how should we deal with it?  Courteous Web crawlers
implement the Robots Exclusion Protocol, which allows Webmasters to declare parts of their sites off
limits to crawlers. The Robots Exclusion Protocol requires a Web crawler to fetch a special document
called robot.txt which contains these declarations from a Web site before downloading any real
content from it.
4. Capacity Estimation and Constraints
If we want to crawl 15 billion pages within four weeks, how many pages do we need to fetch per
second?
15B / (4 weeks * 7 days * 86400 sec) ~= 6200 pages/sec
What about storage? Page sizes vary a lot, but, as mentioned above since, we will be dealing with
HTML text only, let’s assume an average page size of 100KB. With each page, if we are storing 500
bytes of metadata, total storage we would need:
15B * (100KB + 500) ~= 1.5 petabytes
Assuming a 70% capacity model (we don’t want to go above 70% of the total capacity of our storage
system), total storage we will need:
1.5 petabytes / 0.7 ~= 2.14 petabytes
5. High Level design
The basic algorithm executed by any Web crawler is to take a list of seed URLs as its input and
repeatedly execute the following steps.
1. Pick a URL from the unvisited URL list.
2. Determine the IP Address of its host-name.
3. Establish a connection to the host to download the corresponding document.
4. Parse the document contents to look for new URLs.
5. Add the new URLs to the list of unvisited URLs.
6. Process the downloaded document, e.g., store it or index its contents, etc.
7. Go back to step 1
How to crawl?
Breadth first or depth first? Breadth-first search (BFS) is usually used. However, Depth First
Search (DFS) is also utilized in some situations, such as, if your crawler has already established a
connection with the website, it might just DFS all the URLs within this website to save some
handshaking overhead.
Path-ascending crawling: Path-ascending crawling can help discover a lot of isolated resources or
resources for which no inbound link would have been found in regular crawling of a particular Web
site. In this scheme, a crawler would ascend to every path in each URL that it intends to crawl. For
example, when given a seed URL of http://foo.com/a/b/page.html, it will attempt to crawl /a/b/, /a/,
and /.
Difficulties in implementing efficient web crawler
There are two important characteristics of the Web that makes Web crawling a very difficult task:
1. Large volume of Web pages:  A large volume of web pages implies that web crawler can only
download a fraction of the web pages at any time and hence it is critical that web crawler should be
intelligent enough to prioritize download.
2. Rate of change on web pages. Another problem with today’s dynamic world is that web pages on
the internet change very frequently. As a result, by the time the crawler is downloading the last page
from a site, the page may change, or a new page may be added to the site.
A bare minimum crawler needs at least these components:
1. URL frontier: To store the list of URLs to download and also prioritize which URLs should be
crawled first.
2. HTTP Fetcher: To retrieve a web page from the server.
3. Extractor: To extract links from HTML documents.
4. Duplicate Eliminator: To make sure the same content is not extracted twice unintentionally.
5. Datastore: To store retrieved pages, URLs, and other metadata.

## Examples & Scenarios

- 6. Process the downloaded document, e.g., store it or index its contents, etc.
7. Go back to step 1
How to crawl?
Breadth first or depth first? Breadth-first search (BFS) is usually used. However, Depth First
Search (DFS) is also utilized in some situations, such as, if your crawler has already established a
connection with the website, it might just DFS all the URLs within this website to save some
handshaking overhead.
Path-ascending crawling: Path-ascending crawling can help discover a lot of isolated resources or
resources for which no inbound link would have been found in regular crawling of a particular Web
site. In this scheme, a crawler would ascend to every path in each URL that it intends to crawl. For

