# Reasons to use NoSQL database

> Source: System Design - Grokking (Notes), Chapter 266, Pages 76-76

## Key Concepts

- NoSQL databases have different data storage models. The main ones are key-value, document, graph,
and columnar. We will discuss differences between these databases below.
Schema: In SQL, each record c

## Content

NoSQL databases have different data storage models. The main ones are key-value, document, graph,
and columnar. We will discuss differences between these databases below.
Schema: In SQL, each record conforms to a fixed schema, meaning the columns must be decided and
chosen before data entry and each row must have data for each column. The schema can be altered
later, but it involves modifying the whole database and going offline.
In NoSQL, schemas are dynamic. Columns can be added on the fly and each ‘row’ (or equivalent)
doesn’t have to contain data for each ‘column.’
Querying: SQL databases use SQL (structured query language) for defining and manipulating the
data, which is very powerful. In a NoSQL database, queries are focused on a collection of documents.
Sometimes it is also called UnQL (Unstructured Query Language). Different databases have different
syntax for using UnQL.
Scalability: In most common situations, SQL databases are vertically scalable, i.e., by increasing the
horsepower (higher Memory, CPU, etc.) of the hardware, which can get very expensive. It is possible to
scale a relational database across multiple servers, but this is a challenging and time-consuming
process.
On the other hand, NoSQL databases are horizontally scalable, meaning we can add more servers
easily in our NoSQL database infrastructure to handle a lot of traffic. Any cheap commodity hardware
or cloud instances can host NoSQL databases, thus making it a lot more cost-effective than vertical
scaling. A lot of NoSQL technologies also distribute data across servers automatically.
Reliability or ACID Compliancy (Atomicity, Consistency, Isolation, Durability):  The vast
majority of relational databases are ACID compliant. So, when it comes to data reliability and safe
guarantee of performing transactions, SQL databases are still the better bet.
Most of the NoSQL solutions sacrifice ACID compliance for performance and scalability.
SQL VS. NoSQL - Which one to use?
When it comes to database technology, there’s no one-size-fits-all solution. That’s why many
businesses rely on both relational and non-relational databases for different needs. Even as NoSQL
databases are gaining popularity for their speed and scalability, there are still situations where a highly
structured SQL database may perform better; choosing the right technology hinges on the use case.
Reasons to use SQL database
Here are a few reasons to choose a SQL database:
1. We need to ensure ACID compliance. ACID compliance reduces anomalies and protects the
integrity of your database by prescribing exactly how transactions interact with the database.
Generally, NoSQL databases sacrifice ACID compliance for scalability and processing speed, but
for many e-commerce and financial applications, an ACID-compliant database remains the
preferred option.
2. Your data is structured and unchanging. If your business is not experiencing massive growth that
ld
i
d if
’
l
ki
ith d t th t i
i t
t th
th
Stuck? Get help on   
DISCUSS
would require more servers and if you’re only working with data that is consistent, then there may
be no reason to use a system designed to support a variety of data types and high traffic volume.
Reasons to use NoSQL database
When all the other components of our application are fast and seamless, NoSQL databases prevent
data from being the bottleneck. Big data is contributing to a large success for NoSQL databases, mainly
because it handles data differently than the traditional relational databases. A few popular examples of
NoSQL databases are MongoDB, CouchDB, Cassandra, and HBase.
1. Storing large volumes of data that often have little to no structure. A NoSQL database sets no
limits on the types of data we can store together and allows us to add new types as the need
changes. With document-based databases, you can store data in one place without having to
define what “types” of data those are in advance.
2. Making the most of cloud computing and storage. Cloud-based storage is an excellent cost-saving
solution but requires data to be easily spread across multiple servers to scale up. Using
commodity (affordable, smaller) hardware on-site or in the cloud saves you the hassle of
additional software and NoSQL databases like Cassandra are designed to be scaled across multiple
data centers out of the box, without a lot of headaches.
3. Rapid development. NoSQL is extremely useful for rapid development as it doesn’t need to be
prepped ahead of time. If you’re working on quick iterations of your system which require making
frequent updates to the data structure without a lot of downtime between versions, a relational
database will slow you down.
←    Back
Redundancy and R…
Next    →
CAP Theorem
Completed
Send feedback
60 Recommendations

