# 2. Requirements and Goals of the System

> Source: System Design - Grokking (Notes), Chapter 221, Pages 60-60

## Key Concepts

- Stuck? Get help on   
DISCUSS
secondary servers die we can recover the data from the persistent storage.
6. Ranking
How about if we want to rank the search results not just by proximity but also by po

## Content

Stuck? Get help on   
DISCUSS
secondary servers die we can recover the data from the persistent storage.
6. Ranking
How about if we want to rank the search results not just by proximity but also by popularity or
relevance?
How can we return top rated drivers within a given radius?  Let’s assume we keep track of the
overall ratings of each driver in our database and QuadTree. An aggregated number can represent this
popularity in our system, e.g., how many stars does a driver get out of ten? While searching for the top
10 drivers within a given radius, we can ask each partition of the QuadTree to return the top 10 drivers
with a maximum rating. The aggregator server can then determine the top 10 drivers among all the
drivers returned by different partitions.
7. Advanced Issues
1. How will we handle clients on slow and disconnecting networks?
2. What if a client gets disconnected when they are a part of a ride? How will we handle billing in
such a scenario?
3. How about if clients pull all the information, compared to servers always pushing it?
←    Back
Designing Yelp or …
Next    →
Design Ticketmast…
Completed
Send feedback
50 Recommendations
Design Ticketmaster (*New*)
Let's design an online ticketing system that sells movie tickets like Ticketmaster or BookMyShow.
Similar Services: bookmyshow.com, ticketmaster.com
Difficulty Level: Hard
1. What is an online movie ticket booking system?
A movie ticket booking system provides its customers the ability to purchase theatre seats online. E-
ticketing systems allow the customers to browse through movies currently being played and to book
seats, anywhere anytime.
2. Requirements and Goals of the System
Our ticket booking service should meet the following requirements:
Functional Requirements:
1. Our ticket booking service should be able to list different cities where its affiliate cinemas are
located.
2. Once the user selects the city, the service should display the movies released in that particular
city.
3. Once the user selects a movie, the service should display the cinemas running that movie and its
available show times.
4. The user should be able to choose a show at a particular cinema and book their tickets.
5. The service should be able to show the user the seating arrangement of the cinema hall. The user
should be able to select multiple seats according to their preference.
6. The user should be able to distinguish available seats from booked ones.
7. Users should be able to put a hold on the seats for five minutes before they make a payment to
finalize the booking.
8. The user should be able to wait if there is a chance that the seats might become available, e.g.,
when holds by other users expire.
9. Waiting customers should be serviced in a fair, first come, first serve manner.
Non-Functional Requirements:
1. The system would need to be highly concurrent. There will be multiple booking requests for the
same seat at any particular point in time. The service should handle this gracefully and fairly.
2. The core thing of the service is ticket booking, which means financial transactions. This means
that the system should be secure and the database ACID compliant.

## Examples & Scenarios

- popularity in our system, e.g., how many stars does a driver get out of ten? While searching for the top
10 drivers within a given radius, we can ask each partition of the QuadTree to return the top 10 drivers
with a maximum rating. The aggregator server can then determine the top 10 drivers among all the
drivers returned by different partitions.
7. Advanced Issues
1. How will we handle clients on slow and disconnecting networks?
2. What if a client gets disconnected when they are a part of a ride? How will we handle billing in
such a scenario?
3. How about if clients pull all the information, compared to servers always pushing it?
←    Back

- 8. The user should be able to wait if there is a chance that the seats might become available, e.g.,
when holds by other users expire.
9. Waiting customers should be serviced in a fair, first come, first serve manner.
Non-Functional Requirements:
1. The system would need to be highly concurrent. There will be multiple booking requests for the
same seat at any particular point in time. The service should handle this gracefully and fairly.
2. The core thing of the service is ticket booking, which means financial transactions. This means
that the system should be secure and the database ACID compliant.

