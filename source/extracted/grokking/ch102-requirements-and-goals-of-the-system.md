# 2. Requirements and Goals of the System

> Source: System Design - Grokking (Notes), Chapter 102, Pages 25-25

## Key Concepts

- Stuck? Get help on   
DISCUSS
We can have separate group-chat objects in our system that can be stored on the chat servers. A groupchat object is identified by GroupChatID and will also maintain a lis

## Content

Stuck? Get help on   
DISCUSS
We can have separate group-chat objects in our system that can be stored on the chat servers. A groupchat object is identified by GroupChatID and will also maintain a list of people who are part of that
chat. Our load balancer can direct each group chat message based on GroupChatID and the server
handling that group chat can iterate through all the users of the chat to find the server handling the
connection of each user to deliver the message.
In databases, we can store all the group chats in a separate table partitioned based on GroupChatID.
b. Push notifications
In our current design, users can only send messages to active users and if the receiving user is offline,
we send a failure to the sending user. Push notifications will enable our system to send messages to
offline users.
For Push notifications, each user can opt-in from their device (or a web browser) to get notifications
whenever there is a new message or event. Each manufacturer maintains a set of servers that handles
pushing these notifications to the user.
To have push notifications in our system, we would need to set up a Notification server, which will take
the messages for offline users and send them to the manufacture’s push notification server, which will
then send them to the user’s device.
←    Back
Designing Dropbox
Next    →
Designing Twitter
Completed
Send feedback
75 Recommendations
Designing Twitter
Let's design a Twitter-like social networking service. Users of the service will be able to post tweets, follow
other people, and favorite tweets.
Difficulty Level: Medium
1. What is Twitter?
Twitter is an online social networking service where users post and read short 140-character messages
called "tweets." Registered users can post and read tweets, but those who are not registered can only
read them. Users access Twitter through their website interface, SMS, or mobile app.
2. Requirements and Goals of the System
We will be designing a simpler version of Twitter with the following requirements:
Functional Requirements
1. Users should be able to post new tweets.
2. A user should be able to follow other users.
3. Users should be able to mark tweets as favorites.
4. The service should be able to create and display a user’s timeline consisting of top tweets from all
the people the user follows.
5. Tweets can contain photos and videos.
Non-functional Requirements
1. Our service needs to be highly available.
2. Acceptable latency of the system is 200ms for timeline generation.
3. Consistency can take a hit (in the interest of availability); if a user doesn’t see a tweet for a while, it
should be fine.
Extended Requirements
1. Searching for tweets.
2. Replying to a tweet.
3. Trending topics – current hot topics/searches.
4. Tagging other users.
5. Tweet Notification.
6. Who to follow? Suggestions?
7. Moments.

