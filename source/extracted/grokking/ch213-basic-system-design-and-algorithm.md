# 4. Basic System Design and Algorithm

> Source: System Design - Grokking (Notes), Chapter 213, Pages 58-58

## Key Concepts

- Designing Uber backend
Let's design a ride-sharing service like Uber, which connects passengers who need a ride with drivers who
have a car.
Similar Services: Lyft, Didi, Via, Sidecar, etc.
Difficulty

## Content

Designing Uber backend
Let's design a ride-sharing service like Uber, which connects passengers who need a ride with drivers who
have a car.
Similar Services: Lyft, Didi, Via, Sidecar, etc.
Difficulty level: Hard
Prerequisite: Designing Yelp
1. What is Uber?
Uber enables its customers to book drivers for taxi rides. Uber drivers use their personal cars to drive
customers around. Both customers and drivers communicate with each other through their
smartphones using the Uber app.
2. Requirements and Goals of the System
Let’s start with building a simpler version of Uber.
There are two types of users in our system: 1) Drivers 2) Customers.
Drivers need to regularly notify the service about their current location and their availability to
pick passengers.
Passengers get to see all the nearby available drivers.
Customer can request a ride; nearby drivers are notified that a customer is ready to be picked up.
Once a driver and a customer accept a ride, they can constantly see each other’s current location
until the trip finishes.
Upon reaching the destination, the driver marks the journey complete to become available for the
next ride.
3. Capacity Estimation and Constraints
Let’s assume we have 300M customers and 1M drivers with 1M daily active customers and 500K
daily active drivers.
Let’s assume 1M daily rides.
Let’s assume that all active drivers notify their current location every three seconds.
Once a customer puts in a request for a ride, the system should be able to contact drivers in realtime.
4. Basic System Design and Algorithm
We will take the solution discussed in Designing Yelp and modify it to make it work for the abovementioned “Uber” use cases. The biggest difference we have is that our QuadTree was not built keeping
mentioned Uber  use cases. The biggest difference we have is that our QuadTree was not built keeping
in mind that there would be frequent updates to it. So, we have two issues with our Dynamic Grid
solution:
Since all active drivers are reporting their locations every three seconds, we need to update our
data structures to reflect that. If we have to update the QuadTree for every change in the driver’s
position, it will take a lot of time and resources. To update a driver to its new location, we must
find the right grid based on the driver’s previous location. If the new position does not belong to
the current grid, we have to remove the driver from the current grid and move/reinsert the user to
the correct grid. After this move, if the new grid reaches the maximum limit of drivers, we have to
repartition it.
We need to have a quick mechanism to propagate the current location of all the nearby drivers to
any active customer in that area. Also, when a ride is in progress, our system needs to notify both
the driver and passenger about the current location of the car.
Although our QuadTree helps us find nearby drivers quickly, a fast update in the tree is not
guaranteed.
Do we need to modify our QuadTree every time a driver reports their location?  If we don’t
update our QuadTree with every update from the driver, it will have some old data and will not reflect
the current location of drivers correctly. If you recall, our purpose of building the QuadTree was to find
nearby drivers (or places) efficiently. Since all active drivers report their location every three seconds,
therefore there will be a lot more updates happening to our tree than querying for nearby drivers. So,
what if we keep the latest position reported by all drivers in a hash table and update our QuadTree a
little less frequently? Let’s assume we guarantee that a driver’s current location will be reflected in the
QuadTree within 15 seconds. Meanwhile, we will maintain a hash table that will store the current
location reported by drivers; let’s call this DriverLocationHT.
How much memory we need for DriverLocationHT?  We need to store DriveID, their present
and old location, in the hash table. So, we need a total of 35 bytes to store one record:
1. DriverID (3 bytes - 1 million drivers)
2. Old latitude (8 bytes)
3. Old longitude (8 bytes)
4. New latitude (8 bytes)
5. New longitude (8 bytes) Total = 35 bytes
If we have 1 million total drivers, we need the following memory (ignoring hash table overhead):
1 million * 35 bytes => 35 MB
How much bandwidth will our service consume to receive location updates from all
drivers? If we get DriverID and their location, it will be (3+16 => 19 bytes). If we receive this
information every three seconds from 500K daily active drivers, we will be getting 9.5MB per three
seconds.
Do we need to distribute DriverLocationHT onto multiple servers?  Although our memory

