# 7. Detailed Component Design

> Source: System Design - Grokking (Notes), Chapter 122, Pages 31-31

## Key Concepts

- Parameters:
api_dev_key (string): The API developer key of a registered account of our service.
search_query (string): A string containing the search terms.
user_location (string): Optional location o

## Content

Parameters:
api_dev_key (string): The API developer key of a registered account of our service.
search_query (string): A string containing the search terms.
user_location (string): Optional location of the user performing the search.
maximum_videos_to_return (number): Maximum number of results returned in one request.
page_token (string): This token will specify a page in the result set that should be returned.
Returns: (JSON)
A JSON containing information about the list of video resources matching the search query. Each
video resource will have a video title, a thumbnail, a video creation date, and a view count.
streamVideo(api_dev_key, video_id, offset, codec, resolution)
Parameters:
api_dev_key (string): The API developer key of a registered account of our service.
video_id (string): A string to identify the video.
offset (number): We should be able to stream video from any offset; this offset would be a time in
seconds from the beginning of the video. If we support playing/pausing a video from multiple devices,
we will need to store the offset on the server. This will enable the users to start watching a video on any
device from the same point where they left off.
codec (string) & resolution(string): We should send the codec and resolution info in the API from the
client to support play/pause from multiple devices. Imagine you are watching a video on your TV’s
Netflix app, paused it, and started watching it on your phone’s Netflix app. In this case, you would
need codec and resolution, as both these devices have a different resolution and use a different codec.
Returns: (STREAM)
A media stream (a video chunk) from the given offset.
5. High Level Design
At a high-level we would need the following components:
1. Processing Queue: Each uploaded video will be pushed to a processing queue to be de-queued
later for encoding, thumbnail generation, and storage.
2. Encoder: To encode each uploaded video into multiple formats.
3. Thumbnails generator: To generate a few thumbnails for each video.
4. Video and Thumbnail storage: To store video and thumbnail files in some distributed file
storage.
5. User Database: To store user’s information, e.g., name, email, address, etc.
6. Video metadata storage: A metadata database to store all the information about videos like
title, file path in the system, uploading user, total views, likes, dislikes, etc. It will also be used to
store all the video comments.
High level design of Youtube
6. Database Schema
Video metadata storage - MySql
Videos metadata can be stored in a SQL database. The following information should be stored with
each video:
VideoID
Title
Description
Size
Thumbnail
Uploader/User
Total number of likes
Total number of dislikes
Total number of views
For each video comment, we need to store following information:
CommentID
VideoID
UserID
Comment
TimeOfCreation
User data storage - MySql
UserID, Name, email, address, age, registration details etc.
7. Detailed Component Design
The service would be read-heavy, so we will focus on building a system that can retrieve videos quickly.
We can expect our read:write ratio to be 200:1, which means for every video upload there are 200
video views.
Where would videos be stored? Videos can be stored in a distributed file storage system like HDFS
or GlusterFS.

## Examples & Scenarios

- 5. User Database: To store user’s information, e.g., name, email, address, etc.
6. Video metadata storage: A metadata database to store all the information about videos like
title, file path in the system, uploading user, total views, likes, dislikes, etc. It will also be used to
store all the video comments.
High level design of Youtube
6. Database Schema
Video metadata storage - MySql
Videos metadata can be stored in a SQL database. The following information should be stored with
each video:
VideoID

