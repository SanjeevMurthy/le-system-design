# High level differences between SQL and NoSQL

> Source: System Design - Grokking (Notes), Chapter 263, Pages 75-75

## Key Concepts

- Redundancy and Replication
Stuck? Get help on   
DISCUSS
Redundancy is the duplication of critical components or functions of a system with the intention of
increasing the reliability of the system, u

## Content

Redundancy and Replication
Stuck? Get help on   
DISCUSS
Redundancy is the duplication of critical components or functions of a system with the intention of
increasing the reliability of the system, usually in the form of a backup or fail-safe, or to improve actual
system performance. For example, if there is only one copy of a file stored on a single server, then
losing that server means losing the file. Since losing data is seldom a good thing, we can create
duplicate or redundant copies of the file to solve this problem.
Redundancy plays a key role in removing the single points of failure in the system and provides
backups if needed in a crisis. For example, if we have two instances of a service running in production
and one fails, the system can failover to the other one.
Replication means sharing information to ensure consistency between redundant resources, such as
software or hardware components, to improve reliability, fault-tolerance, or accessibility.
Replication is widely used in many database management systems (DBMS), usually with a masterslave relationship between the original and the copies. The master gets all the updates, which then
ripple through to the slaves. Each slave outputs a message stating that it has received the update
successfully, thus allowing the sending of subsequent updates.
←    Back
Proxies
Next    →
SQL vs. NoSQL
Completed
Send feedback
24 Recommendations
SQL vs. NoSQL
In the world of databases, there are two main types of solutions: SQL and NoSQL (or relational
databases and non-relational databases). Both of them differ in the way they were built, the kind of
information they store, and the storage method they use.
Relational databases are structured and have predefined schemas like phone books that store phone
numbers and addresses. Non-relational databases are unstructured, distributed, and have a dynamic
schema like file folders that hold everything from a person’s address and phone number to their
Facebook ‘likes’ and online shopping preferences.
SQL
Relational databases store data in rows and columns. Each row contains all the information about one
entity and each column contains all the separate data points. Some of the most popular relational
databases are MySQL, Oracle, MS SQL Server, SQLite, Postgres, and MariaDB.
NoSQL
Following are the most common types of NoSQL:
Key-Value Stores: Data is stored in an array of key-value pairs. The ‘key’ is an attribute name which
is linked to a ‘value’. Well-known key-value stores include Redis, Voldemort, and Dynamo.
Document Databases: In these databases, data is stored in documents (instead of rows and columns
in a table) and these documents are grouped together in collections. Each document can have an
entirely different structure. Document databases include the CouchDB and MongoDB.
Wide-Column Databases: Instead of ‘tables,’ in columnar databases we have column families,
which are containers for rows. Unlike relational databases, we don’t need to know all the columns up
front and each row doesn’t have to have the same number of columns. Columnar databases are best
suited for analyzing large datasets - big names include Cassandra and HBase.
Graph Databases: These databases are used to store data whose relations are best represented in a
graph. Data is saved in graph structures with nodes (entities), properties (information about the
entities), and lines (connections between the entities). Examples of graph database include Neo4J and
InfiniteGraph.
High level differences between SQL and NoSQL
Storage: SQL stores data in tables where each row represents an entity and each column represents a
data point about that entity; for example, if we are storing a car entity in a table, different columns
could be ‘Color’, ‘Make’, ‘Model’, and so on.
N SQL d
b
h
diff
d
d l
Th
i
k
l
d
h

## Examples & Scenarios

- system performance. For example, if there is only one copy of a file stored on a single server, then
losing that server means losing the file. Since losing data is seldom a good thing, we can create
duplicate or redundant copies of the file to solve this problem.
Redundancy plays a key role in removing the single points of failure in the system and provides
backups if needed in a crisis. For example, if we have two instances of a service running in production
and one fails, the system can failover to the other one.
Replication means sharing information to ensure consistency between redundant resources, such as
software or hardware components, to improve reliability, fault-tolerance, or accessibility.
Replication is widely used in many database management systems (DBMS), usually with a masterslave relationship between the original and the copies. The master gets all the updates, which then
ripple through to the slaves. Each slave outputs a message stating that it has received the update

- data point about that entity; for example, if we are storing a car entity in a table, different columns
could be ‘Color’, ‘Make’, ‘Model’, and so on.
N SQL d
b
h
diff
d
d l
Th
i

