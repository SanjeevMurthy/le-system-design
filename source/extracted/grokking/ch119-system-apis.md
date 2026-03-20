# 4. System APIs

> Source: System Design - Grokking (Notes), Chapter 119, Pages 30-30

## Key Concepts

- Designing Youtube or Netflix
Let's design a video sharing service like Youtube, where users will be able to upload/view/search videos.
Similar Services: netflix.com, vimeo.com, dailymotion.com, veoh.c

## Content

Designing Youtube or Netflix
Let's design a video sharing service like Youtube, where users will be able to upload/view/search videos.
Similar Services: netflix.com, vimeo.com, dailymotion.com, veoh.com
Difficulty Level: Medium
1. Why Youtube?
Youtube is one of the most popular video sharing websites in the world. Users of the service can
upload, view, share, rate, and report videos as well as add comments on videos.
2. Requirements and Goals of the System
For the sake of this exercise, we plan to design a simpler version of Youtube with following
requirements:
Functional Requirements:
1. Users should be able to upload videos.
2. Users should be able to share and view videos.
3. Users should be able to perform searches based on video titles.
4. Our services should be able to record stats of videos, e.g., likes/dislikes, total number of views,
etc.
5. Users should be able to add and view comments on videos.
Non-Functional Requirements:
1. The system should be highly reliable, any video uploaded should not be lost.
2. The system should be highly available. Consistency can take a hit (in the interest of availability); if
a user doesn’t see a video for a while, it should be fine.
3. Users should have a real time experience while watching videos and should not feel any lag.
Not in scope: Video recommendations, most popular videos, channels, subscriptions, watch later,
favorites, etc.
3. Capacity Estimation and Constraints
Let’s assume we have 1.5 billion total users, 800 million of whom are daily active users. If, on average,
a user views five videos per day then the total video-views per second would be:
800M * 5 / 86400 sec => 46K videos/sec
Let’s assume our upload:view ratio is 1:200, i.e., for every video upload we have 200 videos viewed,
giving us 230 videos uploaded per second.
46K / 200 => 230 videos/sec
Storage Estimates: Let’s assume that every minute 500 hours worth of videos are uploaded to
Youtube. If on average, one minute of video needs 50MB of storage (videos need to be stored in
multiple formats), the total storage needed for videos uploaded in a minute would be:
500 hours * 60 min * 50MB => 1500 GB/min (25 GB/sec)
These numbers are estimated with ignoring video compression and replication, which would change
our estimates.
Bandwidth estimates: With 500 hours of video uploads per minute and assuming each video
upload takes a bandwidth of 10MB/min, we would be getting 300GB of uploads every minute.
500 hours * 60 mins * 10MB => 300GB/min (5GB/sec)
Assuming an upload:view ratio of 1:200, we would need 1TB/s outgoing bandwidth.
4. System APIs
We can have SOAP or REST APIs to expose the functionality of our service. The following could be the
definitions of the APIs for uploading and searching videos:
uploadVideo(api_dev_key, video_title, vide_description, tags[], category_id, defau
lt_language, 
                        recording_details, video_contents)
Parameters:
api_dev_key (string): The API developer key of a registered account. This will be used to, among other
things, throttle users based on their allocated quota.
video_title (string): Title of the video.
vide_description (string): Optional description of the video.
tags (string[]): Optional tags for the video.
category_id (string): Category of the video, e.g., Film, Song, People, etc.
default_language (string): For example English, Mandarin, Hindi, etc.
recording_details (string): Location where the video was recorded.
video_contents (stream): Video to be uploaded.
Returns: (string)
A successful upload will return HTTP 202 (request accepted) and once the video encoding is completed
the user is notified through email with a link to access the video. We can also expose a queryable API to
let users know the current status of their uploaded video.
searchVideo(api_dev_key, search_query, user_location, maximum_videos_to_return, pa
ge_token)
Parameters:

## Examples & Scenarios

- 4. Our services should be able to record stats of videos, e.g., likes/dislikes, total number of views,
etc.
5. Users should be able to add and view comments on videos.
Non-Functional Requirements:
1. The system should be highly reliable, any video uploaded should not be lost.
2. The system should be highly available. Consistency can take a hit (in the interest of availability); if
a user doesn’t see a video for a while, it should be fine.
3. Users should have a real time experience while watching videos and should not feel any lag.
Not in scope: Video recommendations, most popular videos, channels, subscriptions, watch later,
favorites, etc.

- category_id (string): Category of the video, e.g., Film, Song, People, etc.
default_language (string): For example English, Mandarin, Hindi, etc.
recording_details (string): Location where the video was recorded.
video_contents (stream): Video to be uploaded.
Returns: (string)
A successful upload will return HTTP 202 (request accepted) and once the video encoding is completed
the user is notified through email with a link to access the video. We can also expose a queryable API to
let users know the current status of their uploaded video.
searchVideo(api_dev_key, search_query, user_location, maximum_videos_to_return, pa
ge_token)

