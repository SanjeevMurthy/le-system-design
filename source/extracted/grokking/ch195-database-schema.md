# 4. Database Schema

> Source: System Design - Grokking (Notes), Chapter 195, Pages 53-53

## Key Concepts

- Stuck? Get help on   
DISCUSS
Send feedback
38 Recommendations
Designing Yelp or Nearby Friends
Let's design a Yelp like service, where users can search for nearby places like restaurants, theaters, o

## Content

Stuck? Get help on   
DISCUSS
Send feedback
38 Recommendations
Designing Yelp or Nearby Friends
Let's design a Yelp like service, where users can search for nearby places like restaurants, theaters, or
shopping malls, etc., and can also add/view reviews of places.
Similar Services: Proximity server.
Difficulty Level: Hard
1. Why Yelp or Proximity Server?
Proximity servers are used to discover nearby attractions like places, events, etc. If you haven’t used
yelp.com before, please try it before proceeding (you can search for nearby restaurants, theaters, etc.)
and spend some time understanding different options that the website offers. This will help you a lot in
understanding this chapter better.
2. Requirements and Goals of the System
What do we wish to achieve from a Yelp like service?  Our service will be storing information
about different places so that users can perform a search on them. Upon querying, our service will
return a list of places around the user.
Our Yelp-like service should meet the following requirements:
Functional Requirements:
1. Users should be able to add/delete/update Places.
2. Given their location (longitude/latitude), users should be able to find all nearby places within a
given radius.
3. Users should be able to add feedback/review about a place. The feedback can have pictures, text,
and a rating.
Non-functional Requirements:
1. Users should have a real-time search experience with minimum latency.
2. Our service should support a heavy search load. There will be a lot of search requests compared to
adding a new place.
3. Scale Estimation
Let’s build our system assuming that we have 500M places and 100K queries per second (QPS). Let’s
also assume a 20% growth in the number of places and QPS each year.
4. Database Schema

