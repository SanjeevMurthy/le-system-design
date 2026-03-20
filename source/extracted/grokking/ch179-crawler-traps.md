# 9. Crawler Traps

> Source: System Design - Grokking (Notes), Chapter 179, Pages 48-48

## Key Concepts

- extracting a URL from the frontier, the worker passes that URL to the relevant protocol module, which
initializes the DIS from a network connection to contain the document’s contents. The worker then


## Content

extracting a URL from the frontier, the worker passes that URL to the relevant protocol module, which
initializes the DIS from a network connection to contain the document’s contents. The worker then
passes the DIS to all relevant processing modules.
4. Document Dedupe test: Many documents on the Web are available under multiple, different
URLs. There are also many cases in which documents are mirrored on various servers. Both of these
effects will cause any Web crawler to download the same document multiple times. To prevent
processing of a document more than once, we perform a dedupe test on each document to remove
duplication.
To perform this test, we can calculate a 64-bit checksum of every processed document and store it in a
database. For every new document, we can compare its checksum to all the previously calculated
checksums to see the document has been seen before. We can use MD5 or SHA to calculate these
checksums.
How big would be the checksum store? If the whole purpose of our checksum store is to do
dedupe, then we just need to keep a unique set containing checksums of all previously processed
document. Considering 15 billion distinct web pages, we would need:
15B * 8 bytes => 120 GB
Although this can fit into a modern-day server’s memory, if we don’t have enough memory available,
we can keep smaller LRU based cache on each server with everything backed by persistent storage. The
dedupe test first checks if the checksum is present in the cache. If not, it has to check if the checksum
resides in the back storage. If the checksum is found, we will ignore the document. Otherwise, it will be
added to the cache and back storage.
5. URL filters: The URL filtering mechanism provides a customizable way to control the set of URLs
that are downloaded. This is used to blacklist websites so that our crawler can ignore them. Before
adding each URL to the frontier, the worker thread consults the user-supplied URL filter. We can
define filters to restrict URLs by domain, prefix, or protocol type.
6. Domain name resolution: Before contacting a Web server, a Web crawler must use the Domain
Name Service (DNS) to map the Web server’s hostname into an IP address. DNS name resolution will
be a big bottleneck of our crawlers given the amount of URLs we will be working with. To avoid
repeated requests, we can start caching DNS results by building our local DNS server.
7. URL dedupe test: While extracting links, any Web crawler will encounter multiple links to the
same document. To avoid downloading and processing a document multiple times, a URL dedupe test
must be performed on each extracted link before adding it to the URL frontier.
To perform the URL dedupe test, we can store all the URLs seen by our crawler in canonical form in a
database. To save space, we do not store the textual representation of each URL in the URL set, but
rather a fixed-sized checksum.
To reduce the number of operations on the database store, we can keep an in-memory cache of
popular URLs on each host shared by all threads. The reason to have this cache is that links to some
URLs are quite common so caching the popular ones in memory will lead to a high in-memory hit
URLs are quite common, so caching the popular ones in memory will lead to a high in memory hit
rate.
How much storage we would need for URL’s store?  If the whole purpose of our checksum is to
do URL dedupe, then we just need to keep a unique set containing checksums of all previously seen
URLs. Considering 15 billion distinct URLs and 4 bytes for checksum, we would need:
15B * 4 bytes => 60 GB
Can we use bloom filters for deduping?  Bloom filters are a probabilistic data structure for set
membership testing that may yield false positives. A large bit vector represents the set. An element is
added to the set by computing ‘n’ hash functions of the element and setting the corresponding bits. An
element is deemed to be in the set if the bits at all ‘n’ of the element’s hash locations are set. Hence, a
document may incorrectly be deemed to be in the set, but false negatives are not possible.
The disadvantage of using a bloom filter for the URL seen test is that each false positive will cause the
URL not to be added to the frontier and, therefore, the document will never be downloaded. The
chance of a false positive can be reduced by making the bit vector larger.
8. Checkpointing: A crawl of the entire Web takes weeks to complete. To guard against failures, our
crawler can write regular snapshots of its state to the disk. An interrupted or aborted crawl can easily
be restarted from the latest checkpoint.
7. Fault tolerance
We should use consistent hashing for distribution among crawling servers. Consistent hashing will not
only help in replacing a dead host, but also help in distributing load among crawling servers.
All our crawling servers will be performing regular checkpointing and storing their FIFO queues to
disks. If a server goes down, we can replace it. Meanwhile, consistent hashing should shift the load to
other servers.
8. Data Partitioning
Our crawler will be dealing with three kinds of data: 1) URLs to visit 2) URL checksums for dedupe 3)
Document checksums for dedupe.
Since we are distributing URLs based on the hostnames, we can store these data on the same host. So,
each host will store its set of URLs that need to be visited, checksums of all the previously visited URLs
and checksums of all the downloaded documents. Since we will be using consistent hashing, we can
assume that URLs will be redistributed from overloaded hosts.
Each host will perform checkpointing periodically and dump a snapshot of all the data it is holding
onto a remote server. This will ensure that if a server dies down another server can replace it by taking
its data from the last snapshot.
9. Crawler Traps
There are many crawler traps, spam sites, and cloaked content. A crawler trap is a URL or set of URLs

