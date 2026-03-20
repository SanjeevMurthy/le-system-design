# 3. Common Problems of Data Partitioning

> Source: System Design - Grokking (Notes), Chapter 254, Pages 72-72

## Key Concepts

- 2. Partitioning Criteria
a. Key or Hash-based partitioning: Under this scheme, we apply a hash function to some key
attributes of the entity we are storing; that yields the partition number. For examp

## Content

2. Partitioning Criteria
a. Key or Hash-based partitioning: Under this scheme, we apply a hash function to some key
attributes of the entity we are storing; that yields the partition number. For example, if we have 100 DB
servers and our ID is a numeric value that gets incremented by one each time a new record is inserted.
In this example, the hash function could be ‘ID % 100’, which will give us the server number where we
can store/read that record. This approach should ensure a uniform allocation of data among servers.
The fundamental problem with this approach is that it effectively fixes the total number of DB servers,
since adding new servers means changing the hash function which would require redistribution of data
and downtime for the service. A workaround for this problem is to use Consistent Hashing.
b. List partitioning: In this scheme, each partition is assigned a list of values, so whenever we want
to insert a new record, we will see which partition contains our key and then store it there. For
example, we can decide all users living in Iceland, Norway, Sweden, Finland, or Denmark will be stored
in a partition for the Nordic countries.
c. Round-robin partitioning: This is a very simple strategy that ensures uniform data distribution.
With ‘n’ partitions, the ‘i’ tuple is assigned to partition (i mod n).
d. Composite partitioning: Under this scheme, we combine any of the above partitioning schemes
to devise a new scheme. For example, first applying a list partitioning scheme and then a hash based
partitioning. Consistent hashing could be considered a composite of hash and list partitioning where
the hash reduces the key space to a size that can be listed.
3. Common Problems of Data Partitioning
On a partitioned database, there are certain extra constraints on the different operations that can be
performed. Most of these constraints are due to the fact that operations across multiple tables or
multiple rows in the same table will no longer run on the same server. Below are some of the
constraints and additional complexities introduced by partitioning:
a. Joins and Denormalization: Performing joins on a database which is running on one server is
straightforward, but once a database is partitioned and spread across multiple machines it is often not
feasible to perform joins that span database partitions. Such joins will not be performance efficient
since data has to be compiled from multiple servers. A common workaround for this problem is to
denormalize the database so that queries that previously required joins can be performed from a single
table. Of course, the service now has to deal with all the perils of denormalization such as data
inconsistency.
b. Referential integrity: As we saw that performing a cross-partition query on a partitioned
database is not feasible, similarly, trying to enforce data integrity constraints such as foreign keys in a
partitioned database can be extremely difficult.
Most of RDBMS do not support foreign keys constraints across databases on different database
servers. Which means that applications that require referential integrity on partitioned databases often
have to enforce it in application code. Often in such cases, applications have to run regular SQL jobs to
Stuck? Get help on   
DISCUSS
clean up dangling references.
c. Rebalancing: There could be many reasons we have to change our partitioning scheme:
1. The data distribution is not uniform, e.g., there are a lot of places for a particular ZIP code that
cannot fit into one database partition.
2. There is a lot of load on a partition, e.g., there are too many requests being handled by the DB
partition dedicated to user photos.
In such cases, either we have to create more DB partitions or have to rebalance existing partitions,
which means the partitioning scheme changed and all existing data moved to new locations. Doing this
without incurring downtime is extremely difficult. Using a scheme like directory based partitioning
does make rebalancing a more palatable experience at the cost of increasing the complexity of the
system and creating a new single point of failure (i.e. the lookup service/database).
←    Back
Caching
Next    →
Indexes
Completed
Send feedback
49 Recommendations

## Examples & Scenarios

- attributes of the entity we are storing; that yields the partition number. For example, if we have 100 DB
servers and our ID is a numeric value that gets incremented by one each time a new record is inserted.
In this example, the hash function could be ‘ID % 100’, which will give us the server number where we
can store/read that record. This approach should ensure a uniform allocation of data among servers.
The fundamental problem with this approach is that it effectively fixes the total number of DB servers,
since adding new servers means changing the hash function which would require redistribution of data
and downtime for the service. A workaround for this problem is to use Consistent Hashing.
b. List partitioning: In this scheme, each partition is assigned a list of values, so whenever we want
to insert a new record, we will see which partition contains our key and then store it there. For
example, we can decide all users living in Iceland, Norway, Sweden, Finland, or Denmark will be stored

- to devise a new scheme. For example, first applying a list partitioning scheme and then a hash based
partitioning. Consistent hashing could be considered a composite of hash and list partitioning where
the hash reduces the key space to a size that can be listed.
3. Common Problems of Data Partitioning
On a partitioned database, there are certain extra constraints on the different operations that can be
performed. Most of these constraints are due to the fact that operations across multiple tables or
multiple rows in the same table will no longer run on the same server. Below are some of the
constraints and additional complexities introduced by partitioning:
a. Joins and Denormalization: Performing joins on a database which is running on one server is
straightforward, but once a database is partitioned and spread across multiple machines it is often not

- 1. The data distribution is not uniform, e.g., there are a lot of places for a particular ZIP code that
cannot fit into one database partition.
2. There is a lot of load on a partition, e.g., there are too many requests being handled by the DB
partition dedicated to user photos.
In such cases, either we have to create more DB partitions or have to rebalance existing partitions,
which means the partitioning scheme changed and all existing data moved to new locations. Doing this
without incurring downtime is extremely difficult. Using a scheme like directory based partitioning
does make rebalancing a more palatable experience at the cost of increasing the complexity of the
system and creating a new single point of failure (i.e. the lookup service/database).
←    Back

