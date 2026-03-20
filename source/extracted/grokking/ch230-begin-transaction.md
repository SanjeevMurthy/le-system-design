# BEGIN TRANSACTION;

> Source: System Design - Grokking (Notes), Chapter 230, Pages 63-63

## Key Concepts

- There are no seats available to reserve, but all the seats are not booked yet, as there are some seats
that other users are holding in the reservation pool and have not booked yet. The user will be
ta

## Content

There are no seats available to reserve, but all the seats are not booked yet, as there are some seats
that other users are holding in the reservation pool and have not booked yet. The user will be
taken to a waiting page where they can wait until the required seats get freed from the reservation
pool. This waiting could result in the following options:
If the required number of seats become available, the user is taken to the theater map page
where they can choose seats.
While waiting, if all seats get booked or there are fewer seats in the reservation pool than the
user intend to book, the user is shown the error message.
User cancels the waiting and is taken back to the movie search page.
At maximum, a user can wait one hour, after that user’s session gets expired and the user is
taken back to the movie search page.
9. If seats are reserved successfully, the user has five minutes to pay for the reservation. After
payment, booking is marked complete. If the user is not able to pay within five minutes, all their
reserved seats are freed to become available to other users.
User
Web
Server
Search Movies
User
Web
Server
Confirm Reservation
House Full
Reservation Expired
Application
Server
Reservation Expired
Databases
Search Movies
Movie Search Results
Select Movie
Movie Shows
Select Show
Show Seats
Select Seats
Reservation Confirmation
Search Movies, 
Shows, Seats
Search Results
Reserve Seats
Reserve Seats
No
1 of 8
How would the server keep track of all the active reservation that haven’t been booked
yet? And how would the server keep track of all the waiting customers?
We need two daemon services, one to keep track of all active reservations and remove any expired
reservation from the system; let’s call it ActiveReservationService. The other service would be
keeping track of all the waiting user requests and, as soon as the required number of seats become
available, it will notify the (the longest waiting) user to choose the seats; let’s call
it WaitingUserService.
a. ActiveReservationsService
We can keep all the reservations of a ‘show’ in memory in a data structure similar to Linked HashMap
or a TreeMap in addition to keeping all the data in the database. We will need a linked HashMap kind
of data structure that allows us to jump to any reservation to remove it when the booking is complete.
Also, since we will have expiry time associated with each reservation, the head of the HashMap will
always point to the oldest reservation record so that the reservation can be expired when the timeout is
reached.
To store every reservation for every show, we can have a HashTable where the ‘key’ would be ‘ShowID’
and the ‘value’ would be the Linked HashMap containing ‘BookingID’ and creation ‘Timestamp’.
In the database, we will store the reservation in the ‘Booking’ table and the expiry time will be in the
Timestamp column. The ‘Status’ field will have a value of ‘Reserved (1)’ and, as soon as a booking is
complete, the system will update the ‘Status’ to ‘Booked (2)’ and remove the reservation record from
the Linked HashMap of the relevant show. When the reservation is expired, we can either remove it
from the Booking table or mark it ‘Expired (3)’ in addition to removing it from memory.
ActiveReservationsService will also work with the external financial service to process user payments.
Whenever a booking is completed, or a reservation gets expired, WaitingUsersService will get a signal
so that any waiting customer can be served.
Key
Value
ShowID
LinkedHashMap< BookingID, TimeStamp }
123
{ (1, 1499818500), (2, 1499818700), (3, 1499818800) }
:
:
:
E.g.,
ActiveReservationsService keeping track of all active reservations
b. WaitingUsersService
Just like ActiveReservationsService, we can keep all the waiting users of a show in memory in a Linked
HashMap or a TreeMap. We need a data structure similar to Linked HashMap so that we can jump to
any user to remove them from the HashMap when the user cancels their request. Also, since we are
serving in a first-come-first-serve manner, the head of the Linked HashMap would always be pointing
to the longest waiting user, so that whenever seats become available, we can serve users in a fair
manner.
We will have a HashTable to store all the waiting users for every Show. The ‘key’ would be 'ShowID,
and the ‘value’ would be a Linked HashMap containing ‘UserIDs’ and their wait-start-time.
Clients can use Long Polling for keeping themselves updated for their reservation status. Whenever
seats become available, the server can use this request to notify the user.
Reservation Expiration
On the server, ActiveReservationsService keeps track of expiry (based on reservation time) of active
reservations. As the client will be shown a timer (for the expiration time), which could be a little out of
sync with the server, we can add a buffer of five seconds on the server to safeguard from a broken
experience, such that the client never times out after the server, preventing a successful purchase.
9. Concurrency
How to handle concurrency, such that no two users are able to book same seat.  We can
use transactions in SQL databases to avoid any clashes. For example, if we are using an SQL server we
can utilize Transaction Isolation Levels to lock the rows before we can update them. Here is the sample
code:
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
 
BEGIN TRANSACTION;
 
    -- Suppose we intend to reserve three seats (IDs: 54, 55, 56) for ShowID=99 
    Select * From Show_Seat where ShowID=99 && ShowSeatID in (54, 55, 56) && Statu
s=0 -- free 
 
    -- if the number of rows returned by the above statement is three, we can upda
te to

## Examples & Scenarios

- E.g.,
ActiveReservationsService keeping track of all active reservations
b. WaitingUsersService
Just like ActiveReservationsService, we can keep all the waiting users of a show in memory in a Linked
HashMap or a TreeMap. We need a data structure similar to Linked HashMap so that we can jump to
any user to remove them from the HashMap when the user cancels their request. Also, since we are
serving in a first-come-first-serve manner, the head of the Linked HashMap would always be pointing
to the longest waiting user, so that whenever seats become available, we can serve users in a fair
manner.
We will have a HashTable to store all the waiting users for every Show. The ‘key’ would be 'ShowID,

- use transactions in SQL databases to avoid any clashes. For example, if we are using an SQL server we
can utilize Transaction Isolation Levels to lock the rows before we can update them. Here is the sample
code:
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

