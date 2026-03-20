# 13. Fault Tolerance

> Source: System Design - Grokking (Notes), Chapter 128, Pages 33-33

## Key Concepts

- 1. Data Storage: We could be wasting storage space by keeping multiple copies of the same video.
2. Caching: Duplicate videos would result in degraded cache efficiency by taking up space that could
be

## Content

1. Data Storage: We could be wasting storage space by keeping multiple copies of the same video.
2. Caching: Duplicate videos would result in degraded cache efficiency by taking up space that could
be used for unique content.
3. Network usage: Duplicate videos will also increase the amount of data that must be sent over the
network to in-network caching systems.
4. Energy consumption: Higher storage, inefficient cache, and network usage could result in energy
wastage.
For the end user, these inefficiencies will be realized in the form of duplicate search results, longer
video startup times, and interrupted streaming.
For our service, deduplication makes most sense early; when a user is uploading a video as compared
to post-processing it to find duplicate videos later. Inline deduplication will save us a lot of resources
that can be used to encode, transfer, and store the duplicate copy of the video. As soon as any user
starts uploading a video, our service can run video matching algorithms (e.g., Block Matching, Phase
Correlation, etc.) to find duplications. If we already have a copy of the video being uploaded, we can
either stop the upload and use the existing copy or continue the upload and use the newly uploaded
video if it is of higher quality. If the newly uploaded video is a subpart of an existing video or, vice
versa, we can intelligently divide the video into smaller chunks so that we only upload the parts that are
missing.
10. Load Balancing
We should use Consistent Hashing among our cache servers, which will also help in balancing the load
between cache servers. Since we will be using a static hash-based scheme to map videos to hostnames
it can lead to an uneven load on the logical replicas due to the different popularity of each video. For
instance, if a video becomes popular, the logical replica corresponding to that video will experience
more traffic than other servers. These uneven loads for logical replicas can then translate into uneven
load distribution on corresponding physical servers. To resolve this issue any busy server in one
location can redirect a client to a less busy server in the same cache location. We can use dynamic
HTTP redirections for this scenario.
However, the use of redirections also has its drawbacks. First, since our service tries to load balance
locally, it leads to multiple redirections if the host that receives the redirection can’t serve the video.
Also, each redirection requires a client to make an additional HTTP request; it also leads to higher
delays before the video starts playing back. Moreover, inter-tier (or cross data-center) redirections lead
a client to a distant cache location because the higher tier caches are only present at a small number of
locations.
11. Cache
To serve globally distributed users, our service needs a massive-scale video delivery system. Our
service should push its content closer to the user using a large number of geographically distributed
video cache servers. We need to have a strategy that will maximize user performance and also evenly
distributes the load on its cache servers.
W
i t
d
h f
t d t
t
h h t d t b
U i
M
h t
h
Stuck? Get help on   
DISCUSS
We can introduce a cache for metadata servers to cache hot database rows. Using Memcache to cache
the data and Application servers before hitting database can quickly check if the cache has the desired
rows. Least Recently Used (LRU) can be a reasonable cache eviction policy for our system. Under this
policy, we discard the least recently viewed row first.
How can we build more intelligent cache? If we go with 80-20 rule, i.e., 20% of daily read
volume for videos is generating 80% of traffic, meaning that certain videos are so popular that the
majority of people view them; it follows that we can try caching 20% of daily read volume of videos and
metadata.
12. Content Delivery Network (CDN)
A CDN is a system of distributed servers that deliver web content to a user based in the geographic
locations of the user, the origin of the web page and a content delivery server. Take a look at ‘CDN’
section in our Caching chapter.
Our service can move popular videos to CDNs:
CDNs replicate content in multiple places. There’s a better chance of videos being closer to the
user and, with fewer hops, videos will stream from a friendlier network.
CDN machines make heavy use of caching and can mostly serve videos out of memory.
Less popular videos (1-20 views per day) that are not cached by CDNs can be served by our servers in
various data centers.
13. Fault Tolerance
We should use Consistent Hashing for distribution among database servers. Consistent hashing will
not only help in replacing a dead server, but also help in distributing load among servers.
←    Back
Designing Twitter
Next    →
Designing Typeahe…
Completed
Send feedback
50 Recommendations

## Examples & Scenarios

- starts uploading a video, our service can run video matching algorithms (e.g., Block Matching, Phase
Correlation, etc.) to find duplications. If we already have a copy of the video being uploaded, we can
either stop the upload and use the existing copy or continue the upload and use the newly uploaded
video if it is of higher quality. If the newly uploaded video is a subpart of an existing video or, vice
versa, we can intelligently divide the video into smaller chunks so that we only upload the parts that are
missing.
10. Load Balancing
We should use Consistent Hashing among our cache servers, which will also help in balancing the load
between cache servers. Since we will be using a static hash-based scheme to map videos to hostnames
it can lead to an uneven load on the logical replicas due to the different popularity of each video. For

