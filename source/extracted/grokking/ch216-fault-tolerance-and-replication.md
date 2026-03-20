# 5. Fault Tolerance and Replication

> Source: System Design - Grokking (Notes), Chapter 216, Pages 59-59

## Key Concepts

- and bandwidth requirements don’t require this, since all this information can easily be stored on one
server, but, for scalability, performance, and fault tolerance, we should distribute DriverLocatio

## Content

and bandwidth requirements don’t require this, since all this information can easily be stored on one
server, but, for scalability, performance, and fault tolerance, we should distribute DriverLocationHT
onto multiple servers. We can distribute based on the DriverID to make the distribution completely
random. Let’s call the machines holding DriverLocationHT the Driver Location server. Other than
storing the driver’s location, each of these servers will do two things:
1. As soon as the server receives an update for a driver’s location, they will broadcast that
information to all the interested customers.
2. The server needs to notify the respective QuadTree server to refresh the driver’s location. As
discussed above, this can happen every 10 seconds.
How can we efficiently broadcast the driver’s location to customers?  We can have a Push
Model where the server will push the positions to all the relevant users. We can have a dedicated
Notification Service that can broadcast the current location of drivers to all the interested customers.
We can build our Notification service on a publisher/subscriber model. When a customer opens the
Uber app on their cell phone, they query the server to find nearby drivers. On the server side, before
returning the list of drivers to the customer, we will subscribe the customer for all the updates from
those drivers. We can maintain a list of customers (subscribers) interested in knowing the location of a
driver and, whenever we have an update in DriverLocationHT for that driver, we can broadcast the
current location of the driver to all subscribed customers. This way, our system makes sure that we
always show the driver’s current position to the customer.
How much memory will we need to store all these subscriptions?  As we have estimated
above, we will have 1M daily active customers and 500K daily active drivers. On average let’s assume
that five customers subscribe to one driver. Let’s assume we store all this information in a hash table so
that we can update it efficiently. We need to store driver and customer IDs to maintain the
subscriptions. Assuming we will need 3 bytes for DriverID and 8 bytes for CustomerID, we will need
21MB of memory.
(500K * 3) + (500K * 5 * 8 ) ~= 21 MB
How much bandwidth will we need to broadcast the driver’s location to customers?  For
every active driver, we have five subscribers, so the total subscribers we have:
5 * 500K => 2.5M
To all these customers we need to send DriverID (3 bytes) and their location (16 bytes) every second,
so, we need the following bandwidth:
2.5M * 19 bytes => 47.5 MB/s
How can we efficiently implement Notification service?  We can either use HTTP long polling
or push notifications.
How will the new publishers/drivers get added for a current customer?  As we have
proposed above, customers will be subscribed to nearby drivers when they open the Uber app for the
first time, what will happen when a new driver enters the area the customer is looking at? To add a new
customer/driver subscription dynamically we need to keep track of the area the customer is watching
customer/driver subscription dynamically, we need to keep track of the area the customer is watching.
This will make our solution complicated; how about if instead of pushing this information, clients pull
it from the server?
How about if clients pull information about nearby drivers from the server?  Clients can
send their current location, and the server will find all the nearby drivers from the QuadTree to return
them to the client. Upon receiving this information, the client can update their screen to reflect the
current positions of the drivers. Clients can query every five seconds to limit the number of round trips
to the server. This solution looks simpler compared to the push model described above.
Do we need to repartition a grid as soon as it reaches the maximum limit?  We can have a
cushion to let each grid grow a little bigger beyond the limit before we decide to partition it. Let’s say
our grids can grow/shrink an extra 10% before we partition/merge them. This should decrease the load
for a grid partition or merge on high traffic grids.
How would “Request Ride” use case work?
1. The customer will put a request for a ride.
2. One of the Aggregator servers will take the request and asks QuadTree servers to return nearby
drivers.
3. The Aggregator server collects all the results and sorts them by ratings.
4. The Aggregator server will send a notification to the top (say three) drivers simultaneously,
whichever driver accepts the request first will be assigned the ride. The other drivers will receive a
cancellation request. If none of the three drivers respond, the Aggregator will request a ride from
the next three drivers from the list.
5. Once a driver accepts a request, the customer is notified.
5. Fault Tolerance and Replication
What if a Driver Location server or Notification server dies?  We would need replicas of these
servers, so that if the primary dies the secondary can take control. Also, we can store this data in some
persistent storage like SSDs that can provide fast IOs; this will ensure that if both primary and

