# 11. Data Partitioning

> Source: System Design - Grokking (Notes), Chapter 233, Pages 64-64

## Key Concepts

- -- return success otherwise return failure to the user.
    update Show_Seat ...
    update Booking ...
 
COMMIT TRANSACTION;
‘Serializable’ is the highest isolation level and guarantees safety from D

## Content

-- return success otherwise return failure to the user.
    update Show_Seat ...
    update Booking ...
 
COMMIT TRANSACTION;
‘Serializable’ is the highest isolation level and guarantees safety from Dirty, Nonrepeatable, and
Phantoms reads. One thing to note here; within a transaction, if we read rows, we get a write lock on
them so that they can’t be updated by anyone else.
Once the above database transaction is successful, we can start tracking the reservation in
ActiveReservationService.
10. Fault Tolerance
What happens when ActiveReservationsService or WaitingUsersService crashes?
Whenever ActiveReservationsService crashes, we can read all the active reservations from the
‘Booking’ table. Remember that we keep the ‘Status’ column as ‘Reserved (1)’ until a reservation gets
booked. Another option is to have a master-slave configuration so that, when the master crashes, the
slave can take over. We are not storing the waiting users in the database, so, when
WaitingUsersService crashes, we don’t have any means to recover that data unless we have a masterslave setup.
Similarly, we’ll have a master-slave setup for databases to make them fault tolerant.
11. Data Partitioning
Database partitioning: If we partition by ‘MovieID’, then all the Shows of a movie will be on a single
server. For a very hot movie, this could cause a lot of load on that server. A better approach would be to
partition based on ShowID; this way, the load gets distributed among different servers.
ActiveReservationService and WaitingUserService partitioning: Our web servers will
manage all the active users’ sessions and handle all the communication with the users. We can use the
Consistent Hashing to allocate application servers for both ActiveReservationService and
WaitingUserService based upon the ‘ShowID’. This way, all reservations and waiting users of a
particular show will be handled by a certain set of servers. Let’s assume for load balancing our
Consistent Hashing allocates three servers for any Show, so whenever a reservation is expired, the
server holding that reservation will do the following things:
1. Update database to remove the Booking (or mark it expired) and update the seats’ Status in
‘Show_Seats’ table.
2. Remove the reservation from the Linked HashMap.
3. Notify the user that their reservation has expired.
4. Broadcast a message to all WaitingUserService servers that are holding waiting users of that Show
to figure out the longest waiting user. Consistent Hashing scheme will tell what servers are
holding these users.
5. Send a message to the WaitingUserService server holding the longest waiting user to process their
Stuck? Get help on   
DISCUSS
5. Se d a
essage to t e Wa t
gUse Se v ce se ve
o d
g t e o gest wa t
g use to p ocess t e
request if required seats have become available.
Whenever a reservation is successful, following things will happen:
1. The server holding that reservation sends a message to all servers holding the waiting users of
that Show, so that those servers can expire all the waiting users that need more seats than the
available seats.
2. Upon receiving the above message, all servers holding the waiting users will query the database to
find how many free seats are available now. A database cache would greatly help here to run this
query only once.
3. Expire all waiting users who want to reserve more seats than the available seats. For this,
WaitingUserService has to iterate through the Linked HashMap of all the waiting users.
←    Back
Designing Uber ba…
Next    →
Additional Resourc…
Completed
Send feedback
51 Recommendations

