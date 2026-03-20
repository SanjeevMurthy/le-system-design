# 3 Some Design Considerations

> Source: System Design - Grokking (Notes), Chapter 32, Pages 8-8

## Key Concepts

- Stuck? Get help on   
DISCUSS
Send feedback
304 Recommendations
Designing Pastebin
Let's design a Pastebin like web service, where users can store plain text. Users of the service will enter a
piece o

## Content

Stuck? Get help on   
DISCUSS
Send feedback
304 Recommendations
Designing Pastebin
Let's design a Pastebin like web service, where users can store plain text. Users of the service will enter a
piece of text and get a randomly generated URL to access it. 
Similar Services: pastebin.com, pasted.co, chopapp.com 
Difficulty Level: Easy
1. What is Pastebin?
Pastebin like services enable users to store plain text or images over the network (typically the
Internet) and generate unique URLs to access the uploaded data. Such services are also used to share
data over the network quickly, as users would just need to pass the URL to let other users see it.
If you haven’t used pastebin.com before, please try creating a new ‘Paste’ there and spend some time
going through the different options their service offers. This will help you a lot in understanding this
chapter.
2. Requirements and Goals of the System
Our Pastebin service should meet the following requirements:
Functional Requirements:
1. Users should be able to upload or “paste” their data and get a unique URL to access it.
2. Users will only be able to upload text.
3. Data and links will expire after a specific timespan automatically; users should also be able to
specify expiration time.
4. Users should optionally be able to pick a custom alias for their paste.
Non-Functional Requirements:
1. The system should be highly reliable, any data uploaded should not be lost.
2. The system should be highly available. This is required because if our service is down, users will
not be able to access their Pastes.
3. Users should be able to access their Pastes in real-time with minimum latency.
4. Paste links should not be guessable (not predictable).
Extended Requirements:
1. Analytics, e.g., how many times a paste was accessed?
2. Our service should also be accessible through REST APIs by other services.
3 Some Design Considerations

## Examples & Scenarios

- 1. Analytics, e.g., how many times a paste was accessed?
2. Our service should also be accessible through REST APIs by other services.
3 Some Design Considerations

