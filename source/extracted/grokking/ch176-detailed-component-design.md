# 6. Detailed Component Design

> Source: System Design - Grokking (Notes), Chapter 176, Pages 47-47

## Key Concepts

- 6. Detailed Component Design
Let’s assume our crawler is running on one server and all the crawling is done by multiple working
threads where each working thread performs all the steps needed to downl

## Content

6. Detailed Component Design
Let’s assume our crawler is running on one server and all the crawling is done by multiple working
threads where each working thread performs all the steps needed to download and process a document
in a loop.
The first step of this loop is to remove an absolute URL from the shared URL frontier for downloading.
An absolute URL begins with a scheme (e.g., “HTTP”) which identifies the network protocol that
should be used to download it. We can implement these protocols in a modular way for extensibility, so
that later if our crawler needs to support more protocols, it can be easily done. Based on the URL’s
scheme, the worker calls the appropriate protocol module to download the document. After
downloading, the document is placed into a Document Input Stream (DIS). Putting documents into
DIS will enable other modules to re-read the document multiple times.
Once the document has been written to the DIS, the worker thread invokes the dedupe test to
determine whether this document (associated with a different URL) has been seen before. If so, the
document is not processed any further and the worker thread removes the next URL from the frontier.
Next, our crawler needs to process the downloaded document. Each document can have a different
MIME type like HTML page, Image, Video, etc. We can implement these MIME schemes in a modular
way, so that later if our crawler needs to support more types, we can easily implement them. Based on
the downloaded document’s MIME type, the worker invokes the process method of each processing
module associated with that MIME type.
Furthermore, our HTML processing module will extract all links from the page. Each link is converted
into an absolute URL and tested against a user-supplied URL filter to determine if it should be
downloaded. If the URL passes the filter, the worker performs the URL-seen test, which checks if the
URL has been seen before, namely, if it is in the URL frontier or has already been downloaded. If the
URL is new, it is added to the frontier.
Let’s discuss these components one by one, and see how they can be distributed onto multiple
machines:
1. The URL frontier: The URL frontier is the data structure that contains all the URLs that remain
to be downloaded. We can crawl by performing a breadth-first traversal of the Web, starting from the
pages in the seed set. Such traversals are easily implemented by using a FIFO queue.
Since we’ll be having a huge list of URLs to crawl, we can distribute our URL frontier into multiple
servers. Let’s assume on each server we have multiple worker threads performing the crawling tasks.
Let’s also assume that our hash function maps each URL to a server which will be responsible for
crawling it.
Following politeness requirements must be kept in mind while designing a distributed URL frontier:
1. Our crawler should not overload a server by downloading a lot of pages from it.
2. We should not have multiple machines connecting a web server.
To implement this politeness constraint our crawler can have a collection of distinct FIFO sub-queues
on each server. Each worker thread will have its separate sub-queue, from which it removes URLs for
crawling. When a new URL needs to be added, the FIFO sub-queue in which it is placed will be
determined by the URL’s canonical hostname. Our hash function can map each hostname to a thread
number. Together, these two points imply that, at most, one worker thread will download documents
from a given Web server and also, by using FIFO queue, it’ll not overload a Web server.
How big will our URL frontier be? The size would be in the hundreds of millions of URLs. Hence,
we need to store our URLs on a disk. We can implement our queues in such a way that they have
separate buffers for enqueuing and dequeuing. Enqueue buffer, once filled, will be dumped to the disk,
whereas dequeue buffer will keep a cache of URLs that need to be visited; it can periodically read from
disk to fill the buffer.
2. The fetcher module: The purpose of a fetcher module is to download the document
corresponding to a given URL using the appropriate network protocol like HTTP. As discussed above,
webmasters create robot.txt to make certain parts of their websites off limits for the crawler. To avoid
downloading this file on every request, our crawler’s HTTP protocol module can maintain a fixed-sized
cache mapping host-names to their robot’s exclusion rules.
3. Document input stream: Our crawler’s design enables the same document to be processed by
multiple processing modules. To avoid downloading a document multiple times, we cache the
document locally using an abstraction called a Document Input Stream (DIS).
A DIS is an input stream that caches the entire contents of the document read from the internet. It also
provides methods to re-read the document. The DIS can cache small documents (64 KB or less)
entirely in memory, while larger documents can be temporarily written to a backing file.
Each worker thread has an associated DIS, which it reuses from document to document. After

## Examples & Scenarios

- An absolute URL begins with a scheme (e.g., “HTTP”) which identifies the network protocol that
should be used to download it. We can implement these protocols in a modular way for extensibility, so
that later if our crawler needs to support more protocols, it can be easily done. Based on the URL’s
scheme, the worker calls the appropriate protocol module to download the document. After
downloading, the document is placed into a Document Input Stream (DIS). Putting documents into
DIS will enable other modules to re-read the document multiple times.
Once the document has been written to the DIS, the worker thread invokes the dedupe test to
determine whether this document (associated with a different URL) has been seen before. If so, the
document is not processed any further and the worker thread removes the next URL from the frontier.
Next, our crawler needs to process the downloaded document. Each document can have a different

