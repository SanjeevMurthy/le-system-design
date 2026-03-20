# Chapter 10: System Design – Proximity Service

> Source: System Design Guide for Software Professionals, Chapter 14, Pages 225-239

## Key Concepts

- 10
System Design – Proximity Service
From location-based marketing to smart transportation systems to finding a nearby restaurant or
a business, proximity services leverage the power of proximity data
- optimizing response times and reducing wait times for passengers.
Dynamic pricing: Proximity data helps adjust fares based on demand and driver availability in specific areas,
ensuring a balance betwe

## Content

10
System Design – Proximity Service
From location-based marketing to smart transportation systems to finding a nearby restaurant or
a business, proximity services leverage the power of proximity data to enhance user
experiences, streamline operations, and unlock new opportunities across various industries.
In this chapter, we will understand the complexities of designing proximity services starting from
stating the functional and non-functional requirements, to thinking about the core challenges,
APIs, data storage, and serving the read and write requests. We’ll also dive deeper into the
technical concepts needed to break the problem down and form the foundations of the solution.
Understanding the principles behind proximity service design is essential for staying ahead in the
rapidly evolving landscape of digital transformation. This chapter attempts to delve into the
details of creating a large-scale system based on the proximity service.
We will cover the following topics in this chapter:
Real-world use cases
Functional requirements
Non-functional requirements
Client APIs needed
Estimates and calculations
System design
Requirements verification
So, let’s start the chapter by considering some real-world use cases for a proximity service.
Real-world use cases
Proximity services play a pivotal role in various popular applications that people use daily. Here
are some real-world use cases of proximity services exemplified by well-known platforms:
Ride-sharing services (Uber, Lyft):
Driver matching: These platforms use proximity services to match riders with nearby drivers efficiently. When a
user requests a ride, the system identifies and notifies drivers in close proximity to the pick-up location,


optimizing response times and reducing wait times for passengers.
Dynamic pricing: Proximity data helps adjust fares based on demand and driver availability in specific areas,
ensuring a balance between supply and demand and providing incentives for drivers to operate in high-demand
zones.
Local search and recommendation services (Yelp, Foursquare):
Location-based recommendations: These platforms leverage proximity services to deliver personalized
recommendations for restaurants, shops, attractions, and services based on a user’s current location. Users
receive suggestions for nearby places tailored to their preferences, ratings, and reviews.
Check-in and loyalty programs: Proximity-based check-in features enable users to notify friends about their
location, share experiences, and participate in loyalty programs or promotions offered by local businesses.
Food delivery services (DoorDash, Grubhub):
Optimized delivery routes: Proximity services help drivers optimize delivery routes by identifying the most
efficient path to reach multiple destinations in a single trip, reducing delivery times and improving overall
efficiency.
Real-time tracking: Users can keep track of the status of their orders in near-real time, getting updates on the
food preparation, pick-up readiness, actual pickup, and estimated arrival time of their food delivery based on the
proximity of the driver to their location.
Social networking and dating apps (Tinder, Bumble):
Geolocation matching: These apps utilize proximity services to connect users with potential matches in their
vicinity, allowing users to view profiles, initiate conversations, and arrange meetings with people nearby.
Event and venue discovery: Proximity-based features enable users to discover local events, gatherings, and
venues, facilitating social interactions and networking opportunities based on shared interests and location.
Navigation and mapping services (Google Maps, Waze):
Turn-by-turn directions: Proximity services provide accurate location data to deliver real-time, turn-by-turn
navigation instructions, helping users navigate to their destinations efficiently and safely.
Traffic and incident alerts: These platforms use proximity data to monitor traffic conditions, identify congestion,
accidents, or road closures in the vicinity, and provide alternative routes to avoid delays.
Fitness and health tracking apps (Strava, Fitbit):
Location-based activity tracking: Proximity services enable these apps to track and analyze users’ activities, such
as running, cycling, or walking, providing insights into performance metrics, route mapping, and personalized
fitness recommendations based on the proximity to popular routes or landmarks.


These examples showcase the diverse applications of proximity services across different
industries, highlighting their role in enhancing user experiences, optimizing operations, and
driving innovation in today’s digital landscape. Whether it’s connecting people, delivering
services, or facilitating interactions based on location data, proximity services continue to
redefine how we engage with the world around us.
Having explored real-world examples of proximity services, let’s now delve into the process of
designing such a system. First, we’ll brainstorm and outline both the functional and nonfunctional requirements, keeping a simple use case in mind – finding nearby restaurants and
placing an order.
Functional requirements
Here are the core requirements for this design problem:
A user should be able to search nearby restaurants, given their location
A user should be able to select a restaurant and place an order
Non-functional requirements
Let’s put down the non-functional requirements for this design problem:
Availability: The system should be highly available.
Scalability: The system should be highly scalable (100M users) and be able to tolerate request spikes.
Latency: Since restaurants’ menus don’t change often and restaurants don’t open and close very frequently, there are not
many write requests happening. Read latency should be within 200 ms.
Consistency: Occasionally, when the restaurants are updated, it’s fine to support eventual consistency.
Reliability: The system should behave correctly and deliver the functional requirements even in the case of failures, request
spikes, and other outages.
Client APIs needed
Now that we have thought about the functional and non-functional requirements, let’s document
the APIs needed for the functional requirements to be satisfied:
1. GET /restaurants/search?lat=37.7749&long=122.4194&distance=5
Response:
[
  {


    "restaurantId": "78566",
    "name": "ABC_Italian",
    "location": "123 Castro St, San Francisco, CA 94056",
    "cuisine": "Italian",
    "rating": 4.9,
    "distance": 2 miles
  },
  {
    "restaurantId": "45678",
    "name": "DEF_Mexican",
    "location": "123 Main St, San Francisco, CA 94056",
    "cuisine": "Mexican",
    "rating": 4.5,
    "distance": 3 miles
  }
…
]
2. POST /orders/place
Request:
{
  "userId": "12345",
  "restaurantId": "78566",
  "items": [
    {
      "itemId": "item1",
      "quantity": 4
    },
    {
      "itemId": "item2",
      "quantity": 3
    }
  ],
  "paymentMethod": "credit_card"
}
Response:
{
  "orderId": "6689092",
  "message": "Thanks for ordering with us!",
  "Bill Amount": $75.92
}
Now that we have thought through the APIs needed, let’s try to estimate the scale of the problem
by doing some back-of-the-envelope calculations.
Estimates and calculations
Let’s start by asking and answering some questions:
How many users do we have? 100M
How many Daily Active Users (DAU) do we have? 10% of total users, making 10M/day.


Queries per second to support for daily active users: People usually order food around lunch and dinner time, so let’s assume
that orders will be placed for 3 hours during lunch and 3 hours at dinner time. 10M DAU placing orders within 6 hours
means that QPS = 10M/6*60*24 ~= 1200 QPS.
What about traffic spikes? I think 5x is a good assumption: 5 * 1200 ~ 60000 QPS.
How many people are browsing restaurants and doing searches? Assuming 10M users doing 5 search queries, then search
QPS = ordering QPS *5 = 60000 QPS.
How many restaurants are on the app? Let’s assume 10M restaurants in the world and also let’s assume 1M restaurants are
online on our app. Restaurant data doesn’t change often.
OK, now we have the high-level estimates done. These tell us that our system will have a high
QPS with spikes, so we should design our system to be scalable and tolerate spikes in demand.
Let’s move on to the actual core part of designing the system.
System design
In this section, we will design the system. First, we will put together a high-level system design
with different components and design the flows that satisfy the functional requirements. Then we
will identify the single points of failure or any issues with our design and list out the core
challenges that we need to address. This will help us refine the design and arrive at the final
high-level system design architecture and flow.
Before we dive deep into the core challenges, let’s put a high-level diagram first to put together
the pieces and the flow.
High-level system design
The following diagram shows the initial high-level design with the important entities and the
flow (Figure 10.1). The core entities we discuss here are Customer, Restaurant, and Order.
The following high-level diagram just shows the basic components and simple databases to store
the data. We will refine it later as we dig deeper.


Figure 10.1: High-level initial design diagram
Core challenge
The challenge in this design problem is finding nearby restaurants given the users location (their
latitude and longitude) and the given radius. We will refer to latitude as lat and longitude as long
henceforth. So the user location is (lat, long). Figure 10.1 depicts this with the
getNearbyRestaurants() call from Restaurant search service to Restaurant DB. Let’s explore
various options to solve this.
Option A
We can store the restaurant details along with its lat and long in a relational DB and do a search
using an SQL query with the user’s lat and long values (user_lat, user_long), as follows:
SQL query
select restaurant_ids from restaurant_table where
    lat > user_lat - 5 AND lat < user_lat + 5 AND
    long > user_long - 5 AND long < user_long + 5
Problem: This query is very expensive and scans the entire table.


Can we build indexes?
Indexes are good in one dimension, allowing us to do a sort of binary search, but not in two
dimensions. So in this case, even if we build two indexes, we will be able to use only one index
at a time. This narrows down the search from the entire world to a search in the range of long +/-
5 miles, which is also huge and not very efficient.
So let’s explore other options.
Option B
Using quadtree
A quadtree is a tree similar to a binary tree, except that it has 4 children.
The world is divided into quadrants. Quadrants are formed as and when we see a quadrant having less than N number of
restaurants (where N=500, let’s say), as shown in Figure 10.2.
Each of these quadrants is a node in a quadtree.
The leaf node contains the list of restaurant IDs.
The non-leaf nodes contain the min and max lat and long values.
The following diagram shows how the whole world map can be divided into recursively smaller
rectangular quadrants.
Figure 10.2: World map divided into quadrants recursively with threshold checks


Figure 10.3 shows a quadtree. As we know, it’s a tree with four child nodes. The Root node here
represents the whole world map, and the four children of the root are the four big quadrants when
the world map rectangle is divided into four equal rectangles. We represent each rectangle as a
node in Figure 10.2. Each node contains the min and max lat and long values. The leaf nodes of
this tree contain the list of given restaurants inside the quadrant in the world map.
Figure 10.3: quadtree structure
Let’s use the quadtree in Figure 10.3 to see how we find the nearby restaurants given the user’s
lat and long and a radius =D.
Here is the high-level algorithm:
1. Start from Root.
2. Check whether the (lat, long) value is within the node’s min and max limits.
3. If yes, do the DFS (Depth First Search) for each of the four children and repeat steps 1 and 2 until you land on a leaf node.
4. Now we are on a leaf node:
Get the list of restaurants
Apply the Cartesian or driving distance filter of distance D from the user’s lat and long
Return the final list of restaurants
It is possible that we find out that the list is not sufficient and we need to expand the radius of the
search. So, we can just go one level up to the parent node of this current node and then visit each


of the other three children of the node’s parent. The following are the pros and cons of this:
Pros: Fast as it’s in memory data structure
Cons: If there is a need for frequent changes, it would be difficult to change the tree all the time
This may be an acceptable tradeoff since restaurants don’t open and close very often. Let’s
discuss another popular approach in this space.
Option C
Geohashing converts latitude and longitude into a single, shorter string. Lets explore using this
solution option.
The world is divided into quadrants as we discussed earlier, but now, we label each quadrant as shown in Figure 10.4
The top left quadrant is 00, the top-right one is 01, the bottom left is 10, and the bottom right is 11
We recursively divide all the quadrants and label them recursively
So the first quadrant 00 is further divided into 4 quadrants called 00, 01, 10, and 11, as discussed
previously, and hence the label for these smaller quadrants will be 0000, 0001, 0010, and 0011
The following Figure 10.4 shows how the world map is divided recursively into smaller
rectangular areas. Contrary to the previous quadtree solution where the world map was divided
conditionally if the number of restaurants was above a threshold, with geohashing, we don’t
consider any threshold.


Figure 10.4: Entire world map divided into quadrants recursively with no thresholds
So imagine the whole world map is 25,000 miles x 12,500 miles. If we divide this into 16
recursive levels, we will have rectangles of .38 miles x 0.19 miles. Each of these rectangles will
have a different 16-digit label in base 4. We can store it in base 4 or base 32, which is how it’s
usually stored.
We can use the numerals 0-9 and all lower case alphabet letters except (a, i, l and o) for the base
32 representation. We skip these 4 letters since we need only 22 and these are good candidates as
they are a bit similar looking (i and l look a bit similar and so as a and o):
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, b, c, d, e, f, g, h, j, k, m, n, p, q, r, s, t, u, v,
w, x, y, z]
For example, say we have a quadrant with the location 0231 0101 0131 0131 (in base 4), then we
can convert this into base 10 first, which comes out as 121610608. Next, let’s convert this into a
base-32 value as follows:
121610608 / 32 = 3794087 remainder 24 (s)
3794087 / 32 = 118565 remainder 7 (6)
118565 / 32 = 3705 remainder 25 (t)


3705 / 32 = 115 remainder 25 (t)
115 / 32 = 3 remainder 19 (m)
3 / 32 = 0 remainder 3 (2)
//
So the 16-digit base-4 number 0231 0101 0131 0131 = 2mtt6s.
COORDINATES OF SAN FRANCISCO CITY IS
(37.7749° N, 122.4194° W) Converting it into base 32 geohash is
Looking at this site: https://www.dcode.fr/geohash-coordinates the coordinates of San Francisco city with precision up
to 4 digits is 9q8yyk8yt
All of the restaurants in this quadrant will thus have the prefix 9q8yyk8yt. So we can store the
location and list of restaurant IDs in a relational table similar to the following.
geohash
restaurant_ids
9q8yyk
{3, 7, 97, 89, 234...}
9q8yym
{1, 4, 73, 91, 212...}
9q8yym
{9, 13, 92, 893, 422...}
…
…
Table 10.1: database table storing the geohash and corresponding list of restaurant IDs in that geohash location.
Let’s say the user’s lat long was 37.7749° N, 122.4194° W. The geohash of this is 9q8yyk. When
this user searches for restaurants in their local area, the query is as follows:
select restaurant_ids where geohash like "9a8yy%"
This will return the geohashes of all the restaurants with the prefix 9q8yy, which are near to the
user’s location as represented by the geohash (9q8yyk).
Making the right choice for the solution
A simple relational DB solution is not appropriate for this problem, but both the quadtree and
geohashing solutions seem to work fine. Which one is better?
Let’s consider one scenario – an area that doesn’t have many restaurants.


Geohashing will continue to divide into additional levels, which may result in unnecessary
subdivisions with few or no restaurants, leading to wasted space and increased time to retrieve
matching restaurants. In contrast, quadtree avoids further subdivision if the number of restaurants
is less than N (e.g., 500), making it more efficient. Another significant advantage of quadtree
over Geohashing is its in-memory structure, which allows for very fast access times.
However, a key drawback of quadtree is the complexity of frequent updates, as it requires
serialization and data persistence to handle crashes and rebuild the in-memory tree. Given that
restaurant locations do not change frequently in our use case, this tradeoff is acceptable.
This brings us to the question of how we populate the restaurant quadtree. We can populate it
whenever a restaurant closes or a new one opens up. Since this doesn’t happen very frequently,
this sync update works fine.
OK, at this point, we have addressed some of the core challenges we had identified and now we
are ready to put the whole design together.
Final high-level solution architecture
The core problem was to get the nearby restaurant data in a scalable and performant way. As
discussed in the previous section, we will use the quadtree for our solution. Figure 10.5 shows
the final high-level system diagram.


Figure 10.5: Final high-level system diagram
Let’s take a look at the high-level flows.
Write flow:
1. The User device calls the API to do Create, Read, Update, and Delete (CRUD) operations. The load balancer redirects it
to the User CRUD service, which makes the changes to the Customer DB.
2. The User device calls an API to place the order. The load balancer routes this request to the order management service,
which in turn fetches the required customer data, gets the menu from the restaurant database, and then helps the customer
select the items and place the order. The order management service also talks to the payment service to take care of the
payment and when done, it finally writes the order entry in the order database.
Read flow:
1. The User device calls the API to search for nearby restaurants.
2. The load balancer routes the request to the restaurant search service, which talks to the quadtree and goes from the root node
to the leaf node based on the customer address and their lat and long. It then returns the list of nearest k restaurants, which in
turn is finally returned to the user.
This concludes our system design work. Now, let’s validate our functional and non-functional
requirements against this design in the next section.
Requirements verification


Let’s quickly check whether all of our functional and non-functional requirements are met with
this design.
The following are the two functional requirements we had:
A user should be able to search nearby restaurants, given their location.
A user should be able to select a restaurant and place an order.
Both these are satisfied by the current design.
The following are the non-functional requirements:
Availability: The system should be highly available.
The system is highly available since we will have all these services have multiple instances
running, so even if one or a few go down, the system doesn’t go down and is still serving the
traffic.
Scalability: The system should be highly scalable (100M users) and be able to tolerate request spikes.
This is a horizontally scalable system with no bottlenecks.
Latency: Read latency should be within 200 ms.
Latency will be < 200 ms since we will use quadtree for the search use case.
Consistency: Occasionally, when the restaurants are updated, it’s fine to support eventual consistency.
Eventual consistency is fine here.
Reliability: The system should behave correctly and deliver the functional requirements even in the case of failures, request
spikes, and other outages.
We can see that the system is durable, reliable, and fault-tolerant. The non-functional
requirements are therefore also satisfied.
Summary
Proximity services leverage proximity data to enhance user experiences, streamline operations,
and unlock new opportunities across various industries. This chapter delves into the complexities
of designing proximity services, starting from defining functional and non-functional
requirements to addressing core challenges and technical concepts. Real-world use cases
highlight the diverse applications of proximity services, ranging from ride-sharing and local
search to food delivery and social networking apps.
The chapter outlines the process of designing a proximity service, focusing on functional


requirements such as searching nearby restaurants and placing orders, and non-functional
requirements including availability, scalability, latency, consistency, and reliability. APIs for
restaurant search and order placement are provided along with estimates and calculations for
handling traffic spikes and user interactions.
We then moved on to solving the core challenge in this use case, which was how to find nearby
restaurants. Two approaches for finding nearby restaurants were discussed: quadtree and
Geohashing. While both solutions offer advantages, quadtree was preferred for its in-memory
nature and efficiency in handling frequent updates. The final high-level solution architecture
incorporated these concepts to meet all functional and non-functional requirements, ensuring
high availability, scalability, low latency, eventual consistency, and reliability.
The chapter concluded by verifying that the proposed solution met all of our requirements,
making it a robust and effective design for proximity services.
In the next chapter, we will learn about the system design of the Twitter app.

## Examples & Scenarios

- For example, say we have a quadrant with the location 0231 0101 0131 0131 (in base 4), then we
can convert this into base 10 first, which comes out as 121610608. Next, let’s convert this into a
base-32 value as follows:
121610608 / 32 = 3794087 remainder 24 (s)
3794087 / 32 = 118565 remainder 7 (6)
118565 / 32 = 3705 remainder 25 (t)

- is less than N (e.g., 500), making it more efficient. Another significant advantage of quadtree
over Geohashing is its in-memory structure, which allows for very fast access times.
However, a key drawback of quadtree is the complexity of frequent updates, as it requires
serialization and data persistence to handle crashes and rebuild the in-memory tree. Given that
restaurant locations do not change frequently in our use case, this tradeoff is acceptable.
This brings us to the question of how we populate the restaurant quadtree. We can populate it
whenever a restaurant closes or a new one opens up. Since this doesn’t happen very frequently,
this sync update works fine.
OK, at this point, we have addressed some of the core challenges we had identified and now we
are ready to put the whole design together.

## Tables & Comparisons

| geohash | restaurant_ids |
| --- | --- |
| 9q8yyk | {3, 7, 97, 89, 234...} |
| 9q8yym | {1, 4, 73, 91, 212...} |
| 9q8yym | {9, 13, 92, 893, 422...} |
| … | … |

