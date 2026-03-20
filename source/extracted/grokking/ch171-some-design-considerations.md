# 3. Some Design Considerations

> Source: System Design - Grokking (Notes), Chapter 171, Pages 45-45

## Key Concepts

- Stuck? Get help on   
DISCUSS
8. Cache
#
To deal with hot tweets we can introduce a cache in front of our database. We can use Memcached,
which can store all such hot tweets in memory. Application ser

## Content

Stuck? Get help on   
DISCUSS
8. Cache
#
To deal with hot tweets we can introduce a cache in front of our database. We can use Memcached,
which can store all such hot tweets in memory. Application servers, before hitting the backend
database, can quickly check if the cache has that tweet. Based on clients’ usage patterns, we can adjust
how many cache servers we need. For cache eviction policy, Least Recently Used (LRU) seems suitable
for our system.
9. Load Balancing
#
We can add a load balancing layer at two places in our system 1) Between Clients and Application
servers and 2) Between Application servers and Backend server. Initially, a simple Round Robin
approach can be adopted; that distributes incoming requests equally among backend servers. This LB
is simple to implement and does not introduce any overhead. Another benefit of this approach is LB
will take dead servers out of the rotation and will stop sending any traffic to it. A problem with Round
Robin LB is it won’t take server load into consideration. If a server is overloaded or slow, the LB will
not stop sending new requests to that server. To handle this, a more intelligent LB solution can be
placed that periodically queries the backend server about their load and adjust traffic based on that.
10. Ranking
#
How about if we want to rank the search results by social graph distance, popularity, relevance, etc?
Let’s assume we want to rank tweets by popularity, like how many likes or comments a tweet is getting,
etc. In such a case, our ranking algorithm can calculate a ‘popularity number’ (based on the number of
likes, etc.) and store it with the index. Each partition can sort the results based on this popularity
number before returning results to the aggregator server. The aggregator server combines all these
results, sorts them based on the popularity number, and sends the top results to the user.
←    Back
Designing an API R…
Next    →
Designing a Web C…
Completed
Send feedback
33 Recommendations
Designing a Web Crawler
Let's design a Web Crawler that will systematically browse and download the World Wide Web. Web
crawlers are also known as web spiders, robots, worms, walkers, and bots.
Difficulty Level: Hard
1. What is a Web Crawler?
A web crawler is a software program which browses the World Wide Web in a methodical and
automated manner. It collects documents by recursively fetching links from a set of starting pages.
Many sites, particularly search engines, use web crawling as a means of providing up-to-date data.
Search engines download all the pages to create an index on them to perform faster searches.
Some other uses of web crawlers are:
To test web pages and links for valid syntax and structure.
To monitor sites to see when their structure or contents change.
To maintain mirror sites for popular Web sites.
To search for copyright infringements.
To build a special-purpose index, e.g., one that has some understanding of the content stored in
multimedia files on the Web.
2. Requirements and Goals of the System
Let’s assume we need to crawl all the web.
Scalability: Our service needs to be scalable such that it can crawl the entire Web and can be used to
fetch hundreds of millions of Web documents.
Extensibility: Our service should be designed in a modular way with the expectation that new
functionality will be added to it. There could be newer document types that needs to be downloaded
and processed in the future.
3. Some Design Considerations
Crawling the web is a complex task, and there are many ways to go about it. We should be asking a few
questions before going any further:
Is it a crawler for HTML pages only? Or should we fetch and store other types of media,
such as sound files, images, videos, etc.? This is important because the answer can change the
design. If we are writing a general-purpose crawler to download different media types, we might want
to break down the parsing module into different sets of modules: one for HTML, another for images, or
th
f
id
h
h
d l
t
t
h t i
id
d i t
ti
f
th t
di t

## Examples & Scenarios

- To build a special-purpose index, e.g., one that has some understanding of the content stored in
multimedia files on the Web.
2. Requirements and Goals of the System
Let’s assume we need to crawl all the web.
Scalability: Our service needs to be scalable such that it can crawl the entire Web and can be used to
fetch hundreds of millions of Web documents.
Extensibility: Our service should be designed in a modular way with the expectation that new
functionality will be added to it. There could be newer document types that needs to be downloaded
and processed in the future.
3. Some Design Considerations

