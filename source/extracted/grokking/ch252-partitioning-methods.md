# 1. Partitioning Methods

> Source: System Design - Grokking (Notes), Chapter 252, Pages 71-71

## Key Concepts

- Stuck? Get help on   
DISCUSS
Load Balancing
Next    →
Data Partitioning
Send feedback
62 Recommendations
Data Partitioning
Data partitioning is a technique to break up a big database (DB) into many s

## Content

Stuck? Get help on   
DISCUSS
Load Balancing
Next    →
Data Partitioning
Send feedback
62 Recommendations
Data Partitioning
Data partitioning is a technique to break up a big database (DB) into many smaller parts. It is the
process of splitting up a DB/table across multiple machines to improve the manageability,
performance, availability, and load balancing of an application. The justification for data partitioning is
that, after a certain scale point, it is cheaper and more feasible to scale horizontally by adding more
machines than to grow it vertically by adding beefier servers.
1. Partitioning Methods
There are many different schemes one could use to decide how to break up an application database
into multiple smaller DBs. Below are three of the most popular schemes used by various large scale
applications.
a. Horizontal partitioning: In this scheme, we put different rows into different tables. For example,
if we are storing different places in a table, we can decide that locations with ZIP codes less than 10000
are stored in one table and places with ZIP codes greater than 10000 are stored in a separate table.
This is also called a range based partitioning as we are storing different ranges of data in separate
tables. Horizontal partitioning is also called as Data Sharding.
The key problem with this approach is that if the value whose range is used for partitioning isn’t chosen
carefully, then the partitioning scheme will lead to unbalanced servers. In the previous example,
splitting location based on their zip codes assumes that places will be evenly distributed across the
different zip codes. This assumption is not valid as there will be a lot of places in a thickly populated
area like Manhattan as compared to its suburb cities.
b. Vertical Partitioning: In this scheme, we divide our data to store tables related to a specific
feature in their own server. For example, if we are building Instagram like application - where we need
to store data related to users, photos they upload, and people they follow - we can decide to place user
profile information on one DB server, friend lists on another, and photos on a third server.
Vertical partitioning is straightforward to implement and has a low impact on the application. The
main problem with this approach is that if our application experiences additional growth, then it may
be necessary to further partition a feature specific DB across various servers (e.g. it would not be
possible for a single server to handle all the metadata queries for 10 billion photos by 140 million
users).
c. Directory Based Partitioning: A loosely coupled approach to work around issues mentioned in
the above schemes is to create a lookup service which knows your current partitioning scheme and
abstracts it away from the DB access code. So, to find out where a particular data entity resides, we
query the directory server that holds the mapping between each tuple key to its DB server. This loosely
coupled approach means we can perform tasks like adding servers to the DB pool or changing our
partitioning scheme without having an impact on the application.

## Examples & Scenarios

- a. Horizontal partitioning: In this scheme, we put different rows into different tables. For example,
if we are storing different places in a table, we can decide that locations with ZIP codes less than 10000
are stored in one table and places with ZIP codes greater than 10000 are stored in a separate table.
This is also called a range based partitioning as we are storing different ranges of data in separate
tables. Horizontal partitioning is also called as Data Sharding.
The key problem with this approach is that if the value whose range is used for partitioning isn’t chosen
carefully, then the partitioning scheme will lead to unbalanced servers. In the previous example,
splitting location based on their zip codes assumes that places will be evenly distributed across the
different zip codes. This assumption is not valid as there will be a lot of places in a thickly populated
area like Manhattan as compared to its suburb cities.

- feature in their own server. For example, if we are building Instagram like application - where we need
to store data related to users, photos they upload, and people they follow - we can decide to place user
profile information on one DB server, friend lists on another, and photos on a third server.
Vertical partitioning is straightforward to implement and has a low impact on the application. The
main problem with this approach is that if our application experiences additional growth, then it may
be necessary to further partition a feature specific DB across various servers (e.g. it would not be
possible for a single server to handle all the metadata queries for 10 billion photos by 140 million
users).
c. Directory Based Partitioning: A loosely coupled approach to work around issues mentioned in
the above schemes is to create a lookup service which knows your current partitioning scheme and

