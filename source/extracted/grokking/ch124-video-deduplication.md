# 9. Video Deduplication

> Source: System Design - Grokking (Notes), Chapter 124, Pages 32-32

## Key Concepts

- or GlusterFS.
How should we efficiently manage read traffic? We should segregate our read traffic from write
traffic. Since we will have multiple copies of each video, we can distribute our read traff

## Content

or GlusterFS.
How should we efficiently manage read traffic? We should segregate our read traffic from write
traffic. Since we will have multiple copies of each video, we can distribute our read traffic on different
servers. For metadata, we can have master-slave configurations where writes will go to master first and
then gets applied at all the slaves. Such configurations can cause some staleness in data, e.g., when a
new video is added, its metadata would be inserted in the master first and before it gets applied at the
slave our slaves would not be able to see it; and therefore it will be returning stale results to the user.
This staleness might be acceptable in our system as it would be very short-lived and the user would be
able to see the new videos after a few milliseconds.
Where would thumbnails be stored? There will be a lot more thumbnails than videos. If we
assume that every video will have five thumbnails, we need to have a very efficient storage system that
can serve a huge read traffic. There will be two consideration before deciding which storage system
should be used for thumbnails:
1. Thumbnails are small files with, say, a maximum 5KB each.
2. Read traffic for thumbnails will be huge compared to videos. Users will be watching one video at a
time, but they might be looking at a page that has 20 thumbnails of other videos.
Let’s evaluate storing all the thumbnails on a disk. Given that we have a huge number of files, we have
to perform a lot of seeks to different locations on the disk to read these files. This is quite inefficient
and will result in higher latencies.
Bigtable can be a reasonable choice here as it combines multiple files into one block to store on the disk
and is very efficient in reading a small amount of data. Both of these are the two most significant
requirements of our service. Keeping hot thumbnails in the cache will also help in improving the
latencies and, given that thumbnails files are small in size, we can easily cache a large number of such
files in memory.
Video Uploads: Since videos could be huge, if while uploading the connection drops we should
support resuming from the same point.
Video Encoding: Newly uploaded videos are stored on the server and a new task is added to the
processing queue to encode the video into multiple formats. Once all the encoding will be completed
the uploader will be notified and the video is made available for view/sharing.
Detailed component design of Youtube
8. Metadata Sharding
Since we have a huge number of new videos every day and our read load is extremely high, therefore,
we need to distribute our data onto multiple machines so that we can perform read/write operations
efficiently. We have many options to shard our data. Let’s go through different strategies of sharding
this data one by one:
Sharding based on UserID: We can try storing all the data for a particular user on one server.
While storing, we can pass the UserID to our hash function which will map the user to a database
server where we will store all the metadata for that user’s videos. While querying for videos of a user,
we can ask our hash function to find the server holding the user’s data and then read it from there. To
search videos by titles we will have to query all servers and each server will return a set of videos. A
centralized server will then aggregate and rank these results before returning them to the user.
This approach has a couple of issues:
1. What if a user becomes popular? There could be a lot of queries on the server holding that user;
this could create a performance bottleneck. This will also affect the overall performance of our
service.
2. Over time, some users can end up storing a lot of videos compared to others. Maintaining a
uniform distribution of growing user data is quite tricky.
To recover from these situations either we have to repartition/redistribute our data or used consistent
hashing to balance the load between servers.
Sharding based on VideoID: Our hash function will map each VideoID to a random server where
we will store that Video’s metadata. To find videos of a user we will query all servers and each server
will return a set of videos. A centralized server will aggregate and rank these results before returning
them to the user. This approach solves our problem of popular users but shifts it to popular videos.
We can further improve our performance by introducing a cache to store hot videos in front of the
database servers.
9. Video Deduplication
With a huge number of users uploading a massive amount of video data our service will have to deal
with widespread video duplication. Duplicate videos often differ in aspect ratios or encodings, can
contain overlays or additional borders, or can be excerpts from a longer original video. The
proliferation of duplicate videos can have an impact on many levels:
1 Data Storage: We could be wasting storage space by keeping multiple copies of the same video

## Examples & Scenarios

- then gets applied at all the slaves. Such configurations can cause some staleness in data, e.g., when a
new video is added, its metadata would be inserted in the master first and before it gets applied at the
slave our slaves would not be able to see it; and therefore it will be returning stale results to the user.
This staleness might be acceptable in our system as it would be very short-lived and the user would be
able to see the new videos after a few milliseconds.
Where would thumbnails be stored? There will be a lot more thumbnails than videos. If we
assume that every video will have five thumbnails, we need to have a very efficient storage system that
can serve a huge read traffic. There will be two consideration before deciding which storage system
should be used for thumbnails:
1. Thumbnails are small files with, say, a maximum 5KB each.

