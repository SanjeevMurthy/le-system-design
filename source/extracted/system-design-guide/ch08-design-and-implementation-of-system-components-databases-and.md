# Chapter 5: Design and Implementation of System Components –Databases and Storage

> Source: System Design Guide for Software Professionals, Chapter 8, Pages 113-158

## Key Concepts

- 5
Design and Implementation of System Components –
Databases and Storage
In our rapidly evolving digital landscape, where information flows ceaselessly and the demand
for data-driven decision-making i
- Here are some key reasons why we need databases:
Data organization: Databases provide a structured and organized way to store data. Data is arranged in tables, rows, and
columns, making it easy to cat

## Content

5
Design and Implementation of System Components –
Databases and Storage
In our rapidly evolving digital landscape, where information flows ceaselessly and the demand
for data-driven decision-making is unrelenting, the role of databases and storage has never been
more pivotal. As we navigate the intricate web of data that defines our modern world, the ability
to efficiently collect, store, retrieve, and manage information is paramount. This chapter delves
into the very heart of this technological foundation, exploring the fundamental concepts,
strategies, and technologies that underpin the organization and preservation of data. We will look
into the details of how some of the popular databases and storage systems are designed.
In a world where data is often hailed as the new currency, databases serve as the repositories of
knowledge, housing vast troves of information that fuel businesses, drive research, and empower
innovation. Yet, without an equally robust and adaptable storage infrastructure, the potential of
these databases remains untapped. Together, databases and storage systems form an inseparable
duo that enables us to harness the power of data and transform it into actionable insights.
We will cover the following concepts in detail in this chapter.
Databases
Key-value stores
DynamoDB
Column-family databases
HBase
Graph-based databases
Neo4j
Databases
Databases provide a way to store, organize, and manipulate large amounts of information in a
systematic and controlled manner. This data can be structured, semi-structured, or unstructured,
depending on the specific type of database and its use case. Let’s think about the reasons why we
would need a database.


Here are some key reasons why we need databases:
Data organization: Databases provide a structured and organized way to store data. Data is arranged in tables, rows, and
columns, making it easy to categorize and access information.
Data retrieval: Databases enable fast and efficient data retrieval. Users can perform complex queries to extract specific
data, and indexing mechanisms speed up data lookup.
Data integrity: Databases enforce data integrity by using constraints, relationships, and validation rules. This ensures that
data is accurate, consistent, and reliable.
Data security: Databases offer security features such as user authentication, authorization, and encryption to protect data
from unauthorized access and breaches.
Data consistency: Through transaction management and ACID (Atomicity, Consistency, Isolation, and Durability)
properties, databases ensure that data remains consistent even when multiple users access and modify it simultaneously.
Scalability: Databases can handle large volumes of data and scale as data needs grow. Both vertical scaling (adding more
resources to a single server) and horizontal scaling (adding more servers or nodes) are possible.
Redundancy and backup and recovery: Databases often incorporate redundancy and backup mechanisms to ensure data
availability and reliability. This includes features such as replication and automated backups. Databases offer mechanisms to
create backups and restore data if there is data loss or a system failure.
Complex queries: Databases allow users to perform complex queries and aggregations, making it possible to extract
valuable insights and reports from large datasets.
Data relationships: In relational databases, data relationships are defined, enabling the efficient management of
interconnected data, such as customer orders, products, and inventory.
Data history: Some databases maintain historical data, providing a historical view of data changes over time. This is
valuable for auditing and compliance purposes.
Data analysis: Databases support data analysis and reporting tools, allowing organizations to make data-driven decisions
and gain insights into their operations and performance.
Data sharing: Databases support concurrent access and the sharing of data among different users and applications, making
them essential for collaborative and real-time environments.
In essence, databases are the foundation for data-driven applications and systems, from websites
and mobile apps to ERP (enterprise resource planning) systems and scientific research. They
ensure that data is stored, managed, and utilized effectively, facilitating informed decisionmaking and efficient data processing.
It’s important to acknowledge that one kind of database may not be able to solve the needs of
different use cases for different systems and applications. Let’s learn about the various types of
databases.
Types of databases


Databases can be broadly classified as relational and NoSQL databases.
In both cases, databases aim to provide efficient data storage, retrieval, and management, but
they do so using different models and approaches. The choice between these two types of
databases depends on the specific needs of an application or system, with factors such as data
structure, scalability, and performance considerations playing a significant role in the decision.
Now, let’s take a look at these two database types in more detail.
Relational databases
Relational databases are a type of database that organizes and store data in a tabular format,
consisting of rows and columns. They are based on the principles of the relational model, which
was introduced by Edgar F. Codd in the 1970s. This model defines relationships between data
elements and enables efficient data storage and retrieval.
Key characteristics and concepts of relational databases include the following:
Tables: In a relational database, data is organized into tables. Each table represents an entity or concept, such as
“customers,” “products,” or “orders.” Tables are further divided into rows and columns.
Rows: Each row in a table, often referred to as a “record” or “tuple,” represents a unique data entry. For example, in a
“customers” table, each row corresponds to an individual customer, with each column containing specific information about
that customer, such as their name, address, and phone number.
Columns: Columns, also known as “attributes” or “fields,” define the type of data that can be stored in a table. Each column
has a name and a data type, such as text, numeric, date, or binary.
Keys: Relational databases use keys to establish relationships between tables. The primary key uniquely identifies each row
in a table, while foreign keys in one table refer to the primary key in another table, creating relationships between them.
Normalization: The process of normalization is used to eliminate data redundancy and improve data integrity. It involves
breaking down tables into smaller, related tables to reduce duplication and maintain consistency.
Structured Query Language (SQL): SQL is the language used to interact with relational databases. It provides a
standardized way to create, retrieve, update, and delete data, as well as to define the structure of tables and establish
relationships between them.
ACID properties: Relational databases are known for their strong support of ACID properties, which ensure data
consistency, reliability, and durability. ACID is crucial for maintaining data integrity.
Transactions: Relational databases enable transactions, which are sequences of one or more SQL operations that are
executed as a single unit. If any part of a transaction fails, the entire transaction can be rolled back, ensuring data
consistency.
Some well-known relational database management systems (RDBMS) include the following:


MySQL
PostgreSQL
Oracle Database
Microsoft SQL Server
SQLite
IBM Db2
Relational databases are widely used in various applications and industries where data
consistency, structure, and reliability are critical, such as financial systems, inventory
management, customer relationship management (CRM), and many others. However, it’s
essential to choose the right RDBMS and database design to match the specific needs of an
application.
There is another class of databases that is very different from the relational database. We will
learn about NoSQL databases in this next section.
NoSQL databases
Non-relational databases, often referred to as NoSQL databases (which stands for Not Only
SQL), are a category of database management systems that depart from the traditional relational
database model. Unlike relational databases that use tables, rows, and columns, NoSQL
databases offer more flexibility in data storage and retrieval. These databases are designed to
handle unstructured or semi-structured data, making them suitable for various types of
applications and use cases.
Here are some types of NoSQL databases:
Key-value stores: Key-value stores associate a unique key with a data value. They are highly efficient for simple data
retrieval but are less suitable for complex queries. Examples include Redis, Amazon DynamoDB, and Riak.
Document-oriented databases: These databases store data as documents, such as JSON or XML, and are commonly used
in web applications. Examples include MongoDB, CouchDB, and RavenDB.
Column-family databases: Column-family stores organize data into column families, which are groups of related data.
These databases are known for their ability to scale horizontally. Examples include Apache Cassandra, HBase, and
ScyllaDB.
Graph-based databases: Graph databases are designed for data with complex relationships. They use graph structures to
represent and navigate relationships between data points. Examples include Neo4j, Amazon Neptune, and OrientDB.


The key benefits of NoSQL databases include their ability to handle large volumes of data,
support scalability, and adapt to evolving data structures and requirements. However, the tradeoff is typically a decreased emphasis on strong data consistency and the need for more careful
consideration of data modeling and indexing.
NoSQL databases are used in a variety of applications, such as content management systems,
real-time analytics, IoT (Internet of Things), and social media platforms. The choice of a
NoSQL database type depends on the specific data needs and characteristics of an application.
The advantages and disadvantages of relational and
NoSQL databases
Now that we have learned about the two types of databases, let’s summarize the advantages and
disadvantages of both these types.
Relational databases
Here are the advantages of relational databases:
Reduced data redundancy: Relational databases enforce data integrity by minimizing data duplication across tables. This
optimizes storage space and simplifies data retrieval.
Robust security features: Built-in security measures safeguard sensitive information from unauthorized access.
ACID transactions: Native support for ACID ensures data consistency and reliability during operations.
Here are the disadvantages of relational databases:
Performance: Complex joins and fetching data from multiple tables can lead to slower performance.
Memory-intensive: Rows and columns consume storage space, even for null values, increasing memory requirements.
Complexity: Managing intricate joins and complex relationships can add significant complexity to database administration.
A lack of horizontal scalability: Traditional relational databases are difficult to scale
horizontally, making them unsuitable for large data volumes.
NoSQL databases
Here are the advantages of NoSQL databases:
A flexible data model: NoSQL databases excel in storing both structured and unstructured data types. This adaptability
allows for diverse data formats and easy accommodation of changing data requirements.


Schema updates: Schema updates in NoSQL databases can be done without disrupting applications, facilitating an evolving
data model.
Horizontal scaling: Superior horizontal scaling capabilities enable seamless expansion of database capacity to handle
growing datasets and workloads.
Here are the disadvantages of NoSQL databases:
A lack of standardization: The absence of standardization leads to a wider range of designs and query languages compared
to relational databases. This can create challenges in interoperability and data consistency across different NoSQL
implementations.
Limited ACID transactions: Most NoSQL databases lack support for ACID transactions (except for some specialized
types). This might impact the reliability and integrity of data operations that require strict consistency guarantees.
By understanding these strengths and weaknesses, you can effectively choose the database type
that best aligns with your project’s specific requirements and performance needs.
In the following sections, we will learn about various types of databases in more detail, such as
key-value stores, DynamoDB, HBase (a column-oriented database), and Neo4j (a graph
database).
Key-value stores
In any sophisticated software system, data storage and retrieval is a fundamental concern. Keyvalue stores provide a simple, efficient, and highly scalable solution to store data. This chapter
delves into the intricacies of designing a robust key-value store while emphasizing key concepts
such as scalability, replication, versioning, configurability, fault tolerance, and failure detection.
This chapter will equip you with the knowledge to design and manage a resilient key-value store.
We’ll embark on this journey by initially defining the requirements of a key-value store and
designing its API. Then, we’ll explore techniques to ensure scalability, using consistent hashing
and strategies to replicate partitioned data. Furthermore, we’ll uncover how to manage
versioning and resolve conflicts that arise due to concurrent modifications. Lastly, we’ll dive into
how to make the key-value store fault-tolerant and devise mechanisms for timely failure
detection. Let’s begin by understanding what a key-value store is.
What is a key-value store?
A key-value store, also known as a key-value database, is a simple data storage paradigm where
each unique key corresponds to a particular value. Think of it as a large, distributed dictionary or


a Distributed Hash Table (DHT), where data can be stored, retrieved, and updated using an
associated key. This key-value pair forms the fundamental unit of data storage, and it’s this
simplicity in design that aids efficient read and write operations. Let’s now look at why it is
useful in distributed systems.
Use in distributed systems
In the realm of distributed systems, key-value stores play a pivotal role due to their high
performance, scalability, and ease of use. Here are a few reasons why:
Scalability: Given the simplicity of key-value pairs, these stores can easily distribute data across multiple nodes, thereby
improving a system’s capacity and throughput.
Performance: Key-value stores typically offer quick read and write access, especially if the key-value pair resides on the
same node.
Flexibility: Unlike relational databases, key-value stores do not require a fixed data schema. This allows for the storage of
structured, semi-structured, or unstructured data.
Fault-tolerance: Key-value stores can be designed to replicate and partition data across multiple nodes. This ensures that
data is still accessible if there is a node failure.
Hence, key-value stores provide an efficient and flexible approach to data storage and retrieval in
distributed systems, making them an integral part of modern software architecture. Let’s now
learn about some of the functional and non-functional requirements of designing a key-value
store.
Designing a key-value store
When embarking on the design of a DHT or key-value store, we must first establish its
functional and non-functional requirements.
Functional requirements
The following are some of the functional requirements:
Put(key, value): A system should support a put operation that inserts a key-value pair into the store. If the key already
exists, the corresponding value should be updated.
Get(key): A system should support a get operation that retrieves the value associated with a specified key. If the key does
not exist, the operation should return an appropriate error message.


Delete(key): A system should support a delete operation that removes a given key-value pair from the store. If the key
does not exist, the operation should return an appropriate error message.
Non-functional requirements
The following are some of the non-functional requirements:
Scalability: As key-value stores are often used in high-demand scenarios, a system must be able to scale horizontally (add
more nodes to the system) to serve a growing amount of data and traffic.
Performance: A system should ensure low latency for put and get operations. Even as data grows and spans multiple
nodes, the time taken for these operations should not degrade significantly.
Durability: Once a value is stored in a system, it should persist. The system should ensure data is not lost due to node
failures.
Consistency: A system should ensure that all read operations reflect the most recent write operation for a given key. If
writes occur simultaneously, this might involve resolving conflicts.
Availability: A system should remain available for operations despite node failures. This would require replication of data
across multiple nodes.
Partition tolerance: The system should function and maintain data integrity even when network failures occur and nodes
are unable to communicate.
Having understood the functional and non-functional requirements of a key-value store, let’s
now delve into the specifics of ensuring scalability and replication. This next section will provide
insight on how to accommodate growing data and traffic, as well as how to achieve data
replication across multiple nodes for higher availability.
Enhancing scalability and data replication
In this section, we will explore how consistent hashing can bolster scalability and how to
replicate partitioned data efficiently.
Boosting scalability
One of the essential design requirements for our system is scalability. We store key-value data
across multiple storage nodes. Depending on demand, we might need to augment or diminish
these storage nodes. This implies that we must distribute data across all nodes in the system to
evenly distribute the load.


For instance, consider a scenario where we have four nodes, and we aim to balance the load
equally by directing 25% of requests to each node. Traditionally, we would use the modulus
operator to achieve this. Each incoming request comes with an associated key. On receiving a
request, we calculate the hash of the key and then find the remainder when the hashed value is
divided by the number of nodes (m). The remainder value (x) indicates the node number to which
we route the request for processing. Figure 5.1 shows a key that is hashed, and a modulo
operation is applied to the result to determine the node to which the request carrying that keyvalue pair should be routed.
Figure 5.1: A modulo-based key-value pair routing
However, this method falls short when we add or remove nodes, as we end up having to move a
significant number of keys, which is inefficient. For example, if we remove node 2, the new
server to process a request will be node 1 because 10%3 equals 1. Given that nodes maintain
information in local caches, such as keys and their values, we need to transfer this data to the


next node tasked with processing the request. However, this can be costly and result in high
latency.
Next, let’s delve into efficient data copying methods.
Consistent hashing
We covered consistent hashing in Chapter 3. Let’s refresh what we learned here. Consistent
hashing offers a powerful way to distribute load across a set of nodes. In this approach, we
assume a conceptual ring of hashes, ranging from 0 to n-1, where n represents the total number
of available hash values. We calculate the hash for each node’s ID and map it onto the ring. The
same process is applied to requests. Each request is completed by the next node found when
moving in a clockwise direction on the ring. Figure 5.2 shows an example of the consistent
hashing scheme, where a request carries a key-value pair, and the key is hashed to a result. The
result of the hash is then mapped to a location on the ring, and the request is sent to the next node
– N3, in this case.


Figure 5.2: Consistent hashing of key-value pairs in requests
When adding a new node to the ring, only the immediate next node is affected, as it shares its
data with the newly added node. Other nodes remain unaffected. This allows us to scale easily,
as we keep changes to our nodes minimal, with only a small portion of overall keys needing to
move. As the hashes are randomly distributed, we expect the request load to be randomly and
evenly distributed on average on the ring.
However, consistent hashing doesn’t always ensure an equal division of the request load. A
server handling a large chunk of data can become a bottleneck in a distributed system, reducing
the overall system performance. These are referred to as hotspots.
Virtual nodes


To achieve a more evenly distributed load across the nodes, we can utilize virtual nodes. Instead
of applying a single hash function, we apply multiple hash functions to the same key.
For instance, if we have three hash functions, we calculate three hashes for each node and place
them onto the ring. For the request, we use only one hash function. Wherever the request lands
on the ring, it’s processed by the next node found when moving in a clockwise direction. Each
server has three positions, so the request load is more uniform. Furthermore, if a node has more
hardware capacity than others, we can add more virtual nodes by using additional hash functions.
This way, it’ll have more positions in the ring and serve more requests.
The advantages of virtual nodes
Virtual nodes offer the following benefits:
If a node fails or undergoes routine maintenance, the workload is uniformly distributed over other nodes. For each newly
accessible node, the other nodes receive nearly equal load when it comes back online or is added to a system.
Each node can decide how many virtual nodes it’s responsible for, considering the heterogeneity of the physical
infrastructure. For example, if a node has roughly double the computational capacity compared to the others, it can handle
more load.
Now that we’ve made our key-value storage design scalable, the next step is to make our system
highly available. To ensure high availability, we need to introduce replication strategies and
mechanisms to handle failures, which will be the focus of the following sections.
Data duplication strategies
There are several ways to duplicate data in a storage system. The two main methods are the
primary-secondary model and the peer-to-peer model.
The primary-secondary model
In this model, one storage area is designated as the primary, while the others act as secondary
storage areas. The primary storage area handles write requests, while the secondary storage areas
handle read requests and duplicate their data from the primary storage area. However, there is a
delay in replication after writing. If the primary storage fails, the system loses its write
capability, making it a single point of failure. Figure 5.3 shows an example of this model, where
writes to the primary storage are replicated to a secondary storage system, and the reads can be
served by additional read-only replicas as well.


Figure 5.3: A primary-secondary data replication model
The peer-to-peer model
In contrast, the peer-to-peer model designates all storage areas as primary. They can all handle
both read and write requests and replicate data among themselves to stay up to date. However,
duplicating data across all nodes is often inefficient and expensive. A common solution is to
select a smaller number, such as three to five nodes, for replication. Figure 5.4 shows a peer-topeer data replication model in which all nodes have all the writes persisted and are used to
service reads.


Figure 5.4: A peer-to-peer data replication model
We’ll use the peer-to-peer model for our data duplication because of the latency and availability
advantage it provides. With the primary-secondary model, we have a single point of failure if the
primary is unavailable; we can avoid that completely by using the peer-to-peer model for data
duplication. This model will help us achieve durability and high availability by replicating data
on multiple hosts. We’ll replicate each data item on n hosts, where n is a parameter configured
for each instance of the key-value store. For instance, if we set n to five, our data will be
replicated across five nodes.
Each node will copy its data to other nodes. The node responsible for handling read or write
operations is called the coordinator. The coordinator node is directly responsible for specific
keys. For example, if a coordinator node is assigned the key K, it is also responsible for
duplicating these keys to n-1 successors on the ring (going clockwise). These lists of successor
virtual nodes are known as preference lists. To prevent placing replicas on identical physical
nodes, the preference list can bypass those virtual nodes whose physical node is already listed.
Let’s now discuss some of the nuances in implementing the get and the put functions in our keyvalue store.
Implementing get and put functions
This section will delve into how to implement get and put functions in our key-value store.


Implementing get and put operations
A key requirement for our system is configurability. This means the ability to adjust the balance
between availability, consistency, cost-effectiveness, and efficiency. We can achieve this by
incorporating the fundamental get and put functions of a key-value store.
In our system, every node can perform get (read) and put (write) operations. The node that
manages these operations is known as a coordinator, which is usually the first among the top n
nodes on the preference list.
Clients can select a node in two ways:
By routing the request through a generic load balancer
By using a partition-aware client library that directs requests straight to the relevant coordinator nodes
Both methods have their advantages. The first approach doesn’t tie the client to the code, while
the second one can achieve lower latency due to a reduced number of hops, as the client can
directly access a particular server.
We can make our service configurable by controlling the balance between availability,
consistency, cost-effectiveness, and performance. One way to do this is by using a protocol
similar to those used in quorum systems.
Let’s assume n from the top n of the preference list equals 3. This implies that three copies of the
data need to be maintained. If nodes are placed in a ring and A, B, C, D, and E are the nodes in
clockwise order, then if a write operation is performed on node A, the data copies will be placed
on nodes B and C. These are the next nodes found when moving in a clockwise direction on the
ring.
Using r and w
Consider two variables, r and w. The former represents the minimum number of nodes required
for a successful read operation, while the latter signifies the minimum number of nodes involved
in a successful write operation. Therefore, if r equals 2, our system will read from two nodes
when data is stored across three nodes. We need to select values for r and w such that at least one
node is common between them. This ensures that readers can access the latest-written value. To
achieve this, we’ll use a quorum-like system by setting r + w > n.
Here’s an overview of how the values of n, r, and w impact the speed of reads and writes:


n
r
w
Description
3
2
1
Violates constraint – r + w > n
3
2
2
Fulfills constraint
3
3
1
Slow reads and fast writes
3
1
3
Slow writes and fast reads
Table 5.1: The impact of selecting different numbers of read and write successful requests on our system
If we design our system such that more nodes have to return success on reads for an incoming
read request from the client to succeed, we will have slow reads, and similar results for the write
requests as well. The right balance is to design quorums such that we do not compromise reads
or writes but have enough redundancy to support arbitrary node failures.
If n equals 3, which means we have three nodes where the data is copied, and w equals 2, the
operation ensures that writing to two nodes makes this request successful. The third node updates
the data asynchronously.
In this model, the latency of a get operation is determined by the slowest of the r replicas. This is
because a larger r value prioritizes availability over consistency.
We’ve now met the requirements for scalability, availability, conflict resolution, and a
configurable service. The final requirement is to have a fault-tolerant system, which we’ll discuss
in the next lesson.
Ensuring fault tolerance and identifying failures in a
key-value store
In this section, we will explore how to construct a fault-tolerant key-value store capable of
identifying and managing system failures. Let’s begin with the techniques to manage temporary
failures, ensuring that our key-value store can weather short-term disturbances or disruptions.
Managing temporary failures


A common approach to dealing with failures in distributed systems is the use of a quorumbased system. A quorum refers to the minimum number of votes that a distributed transaction
needs to carry out an operation. If a server that is part of the consensus goes down, the operation
cannot proceed, impacting a system’s availability and durability.
Instead of relying on strict quorum membership, we propose using a sloppy quorum. In most
cases, a central leader coordinates communication between consensus participants. After a
successful write, participants send an acknowledgment. The leader responds to the client upon
receipt of these acknowledgments. However, this system is vulnerable to network outages. If the
leader temporarily goes down and the participants cannot reach it, they declare the leader dead.
This necessitates the election of a new leader. Frequent elections can hamper performance, as the
system spends more time choosing a leader than performing actual tasks.
In a sloppy quorum, the first n healthy nodes from the preference list handle all read and write
operations. These n healthy nodes may not be the initial n nodes identified when moving
clockwise in the consistent hash ring.
Consider a configuration where n equals 3. If node A is temporarily unavailable or unreachable
during a write operation, the request is sent to the next healthy node from the preference list,
which in this case is node D. This ensures the required availability and durability. After
processing the request, node D includes a hint about the intended recipient node (in this case, A).
Once node A is back online, node D sends the request information to A to update its data. After
the transfer is complete, D removes this item from its local storage, keeping the total number of
replicas in the system unchanged.
Figure 5.5 shows the flow of data in this case, where initially a write request is forwarded to
node A, which may be unavailable at the time, and so the request ends up in node D. This node
persists the request information along with the fact that the request was originally intended for A.
When node A is available again, node D forwards all the requests that it served, which were
originally intended for node A, and cleans up its internal state.


Figure 5.5: A hinted handoff
This approach, known as a hinted handoff, guarantees that read and write operations are fulfilled
even if there is temporary node failure.
Addressing permanent failures


In the face of permanent node failures, it’s crucial to maintain synchronized replicas for
enhanced system durability. The goal is to quickly detect discrepancies among replicas and
minimize data transfer. To this end, we employ Merkle trees.
A Merkle tree hashes individual key values and uses these hashes as tree leaves. Parent nodes
higher up in the tree contain hashes of their child nodes. Each branch of the Merkle tree can be
independently verified, negating the need to download the entire tree or dataset. Merkle trees
reduce the volume of data transferred during inconsistency checks across copies.
Synchronization isn’t necessary if, for instance, two trees’ root hashes and leaf nodes are
identical. Hosts can identify out-of-sync keys as they exchange the hash values of children,
continuing until they reach the tree leaves. This anti-entropy mechanism ensures data
consistency while reducing data transmission and disk access during synchronization.
Here’s how Merkle trees function:
Hash all keys to create leaf nodes.
Each node maintains a unique Merkle tree for the key range it hosts for every virtual node. Nodes can verify the correctness
of keys within a given range. Two nodes exchange the Merkle tree root corresponding to common key ranges. The
comparison proceeds as follows:
I. Compare the root node hashes of Merkle trees.
II. If they’re identical, don’t proceed.
III. Using recursion, traverse the left and right children. Nodes identify any differences and synchronize accordingly.
The advantage of using Merkle trees lies in their ability to independently verify each branch
without downloading the entire tree or dataset. This reduces the volume of data exchanged
during synchronization and the number of disk accesses required during the anti-entropy process.
However, the downside is that when a node joins or leaves a system, tree hashes must be
recalculated, as multiple key ranges are affected.
To ensure other nodes in the ring detect a node failure, we need to incorporate this into our
design.
Ring membership promotion for failure detection
Nodes may be offline briefly or indefinitely. We shouldn’t rebalance partition assignments or
repair unreachable replicas when a single node goes down, as departures are rarely permanent.


Therefore, adding and removing nodes from a ring should be done cautiously.
Planned commissioning and decommissioning of nodes lead to membership changes. These
changes form a history, recorded persistently on each node’s storage and reconciled among ring
members using a gossip protocol. This protocol also maintains an eventually consistent view of
membership. When two nodes randomly select each other as peers, they can efficiently
synchronize their persisted membership histories.
Here’s how a gossip-based protocol works. Suppose node A starts up for the first time and
randomly adds nodes B and E to its token set. The token set has virtual nodes in the consistent
hash space and maps nodes to their respective token sets. This information is stored locally on
the disk space of the node.
Now, suppose node A handles a request, resulting in a change. It communicates this to nodes B
and E. Another node, D, has nodes C and E in its token set. It makes a change and informs
nodes C and E. The other nodes follow the same process. Eventually, every node becomes aware
of every other node’s information. This method efficiently shares information asynchronously
without consuming much bandwidth.
A key-value store offers flexibility and scalability for applications dealing with unstructured
data. Web applications can use key-value stores to store information about a user’s session and
preferences. By using a user key, all data becomes accessible, making key-value stores ideal for
quick read and write operations. Key-value stores can power real-time recommendations and
advertising, as they can quickly access and present fresh recommendations.
A system design interview – key value store design
questions and strategies
During a system design interview, an interviewer may ask you to design a key-value store. This
request tests your understanding of the basic principles of distributed systems, your ability to
think about scale, and your familiarity with trade-offs in consistency and availability.
When designing a key-value store, remember these key strategies:
Clearly define the problem: Start by understanding the requirements and constraints of the problem. A key-value store
could be asked for in many contexts – for a small application or a large-scale system – so clarify the necessary parameters
first.
Focus on scalability and performance: Discuss how you would ensure the key-value store can handle increasing amounts
of data and requests. You might discuss sharding the data and using consistent hashing to distribute keys.


Discuss replication and consistency: Address how you would handle data replication to achieve high availability. Also,
discuss consistency models and how you’d handle write conflicts in replicated data.
Plan for failure: Remember that distributed systems can and will fail. Discuss strategies to achieve fault tolerance, such as
using redundancy and having a strategy for failure detection and recovery.
Think about evolvability: Your system should be able to evolve over time. Discuss how you might handle data versioning
and how you’d make the system configurable to meet changing needs.
Remember, in a system design interview, your ability to communicate your thought process and
justify your design decisions is often as important as getting the “right” answer.
DynamoDB
DynamoDB is a fully managed, serverless NoSQL database service provided by Amazon Web
Services (AWS). It provides fast and predictable performance with seamless scalability.
DynamoDB is a key-value and document database that uses SSD storage and is spread across
three geographically distinct data centers. It is highly available, with replication across multiple
availability zones. DynamoDB is a great choice for applications that need very low latency
access to data, the ability to scale storage and throughput up or down as needed, and high
availability and durability of data.
Let’s understand some aspects of the DynamoDB design that are useful as system design
practitioners. Some of our design principles of a generic key-value store are directly applicable to
DynamoDB.
No fixed schema
DynamoDB aims to have no fixed schema in its design. This allows DynamoDB to support a
multitude of applications and use cases. To meet the diverse needs of a broad customer base, a
database design must be versatile, scalable, and high-performing, which is fulfilled by a NoSQL
database.
Unlike RDBMS, which requires a predetermined schema to build indexes, NoSQL databases
offer flexibility by deferring schema decisions to read time. This enables easy API integration
and accommodates various use cases.
The benefits of NoSQL


Flexibility: NoSQL databases can store unstructured or semi-structured data, allowing data from multiple tables in a
normalized RDBMS to reside in a single document. This ease of use simplifies API coding and enhances functionality.
Scalability: NoSQL databases store data in documents rather than tables, simplifying scaling processes. Unlike RDBMS,
which is tightly linked to its storage hardware, NoSQL can easily distribute its databases across large clusters, providing a
more straightforward scaling mechanism.
Performance: The data models used in NoSQL databases are engineered for optimal performance, which is especially
important for large-scale operations.
Availability: NoSQL databases ensure high availability by enabling seamless node replacement and easier partitioning. This
feature also minimizes downtime during node failures by rerouting requests to replica shards.
In the NoSQL setup, data is organized into tables built atop a key-value store. Tables may
contain zero or more items identified by primary keys. Each item consists of one or more
attributes, considered as basic data types such as strings or numbers.
API functions
The following are some of the API functions:
PutItem: Adds or replaces an item based on the input key
UpdateItem: Modifies an existing item or creates a new one if it doesn’t exist
DeleteItem: Removes an item identified by its primary key
GetItem: Retrieves an item’s attributes based on its primary key
Partitioning data in DynamoDB
In DynamoDB, data is partitioned horizontally across multiple storage servers. To recap, there
are two ways to partition data – vertically or horizontally. For vertical partitioning, there is a
need to know the schema beforehand. Since DynamoDB has no schema, and since we need to
support a large number of rows, horizontal partitioning is the preferred option. Each table will be
split into partitions, with each partition backed by SSD storage.
Figure 5.6 shows the vertical and horizontal partitioning of data.


Figure 5.6: Vertical and horizontal data partitioning in DynamoDB
Primary key types
To locate an item in a partition, for a lookup or update, there are two schemas – a partition key,
and a partition key with a sort key (also called a composite key):
A partition Key: Determines an item’s storage location through a hash function.
A composite key: Consists of a partition key and a sort key. The hash function output, coupled with the sort key, identifies
the item’s storage location.
Figure 5.7 shows an example of the partition key, sort key, and composite keys in DynamoDB.
The hash is applied to the partition key, which along with the sort key, determines the location of
the key on the backend storage node.


Figure 5.7: Partition keys, sort keys, and composite keys in DynamoDB
Secondary indexes
DynamoDB's design accommodates alternative querying keys, in addition to primary keys,
providing more query options.
Throughput optimizations in DynamoDB
In the context of database management, specifically in DynamoDB, the optimization of
throughput allocation is of utmost importance. Throughput, in this case, refers to the rate at
which a system can fulfill read or write requests. Efficiently partitioning the tables and managing
throughput can lead to increased performance and reduced downtime.
In the next section, we will briefly cover read and write capacity units in DynamoDB and ways
in which bursting and adaptive capacity management are used to increase throughput.
Throughput allocation
DynamoDB allows you to set a provisioned throughput, the upper limit of read capacity units
and write capacity units (RCUs and WCUs) that a system will allocate for your tables. Initial
partitioning spreads this allocated throughput equally across all partitions, assuming each key
within those partitions will be accessed uniformly. However, this is often not the case in realworld applications, leading to inefficiencies such as underutilized or overloaded partitions.
RCUs and WCUs are metrics that gauge a system’s ability to complete read and write requests,
respectively. These units are crucial when discussing throughput optimization. For example, if a
table has a provisioned throughput of 20,000 RCUs and 5,000 WCUs, it implies that the system


can, at maximum capacity, read 20,000 items and write 5,000 items per second for an item of a
given arbitrary size.
In DynamoDB, you may need to add or remove partitions based on data storage or throughput
needs. When you alter the number of partitions, the provisioned throughput will need to be
redistributed among the existing partitions. For instance, if a table initially had 10 partitions,
each with 2,000 RCUs and 500 WCUs, and you add 10 more, the throughput of each partition
would be halved to accommodate the new partitions.
Let’s now understand how bursting can help with throughput management, with unevenly
distributed reads and writes in a DynamoDB table.
Bursting – short-term overprovisioning
In real-world scenarios, applications or users can disproportionately access certain keys, causing
uneven distribution of requests across partitions. Bursting is a strategy to temporarily tap into
any unused throughput from neighboring partitions to manage these short-term spikes in
demand.
When allowing for bursting, it’s essential to ensure workload isolation so that the extra
throughput of one partition does not interfere with the regular operations of its neighboring
partitions. This ensures that short-term gains in one partition do not compromise the overall
system’s performance. Figure 5.8 shows the advantage of supporting bursting in DynamoDB,
which allows it to serve more requests.
Figure 5.8: Comparing the reads/sec served without bursting and with bursting support in DynamoDB
A token bucket system


A token bucket system can be implemented at the node level to manage the bursting mechanism.
Two buckets are maintained – the allocated throughput bucket and the available burst throughput
bucket. If the regular bucket is empty (i.e., its provisioned throughput is exhausted), the system
checks for available tokens in the burst bucket. If tokens are there, the partition is allowed to
burst, temporarily exceeding its provisioned limits.
Bursting is beneficial for short-term uneven workload distribution, but if we need a more longterm approach to throughput management, DynamoDB design also supports adaptive capacity
management, which we will cover next.
Adaptive capacity – long-term adjustments
While bursting handles short-term spikes in demand, adaptive capacity aims to reallocate
throughput based on long-term usage patterns. This means that if certain partitions are
consistently underutilized while others are overwhelmed, DynamoDB will gradually redistribute
throughput to accommodate these patterns.
How it works
Under the hood, DynamoDB uses algorithms that study usage patterns over time, identifying hot
partitions (partitions that are consistently accessed more frequently) and cold partitions (those
less frequently accessed). A system then reallocates RCUs and WCUs accordingly. This ensures
that your read and write operations are more evenly distributed, reducing the likelihood of
throttling on busy partitions.
Adaptive capacity is effective but not instantaneous. It may take some time for a system to learn
the access patterns and reallocate resources. Also, there is an upper limit to how much a single
partition’s throughput can be increased.
In the next section, we will learn about global admission control.
Global admission control – cross-partition management
Global admission control is a technique used to manage throughput across all partitions. While
adaptive capacity focuses on individual partitions, global admission control takes a more holistic
approach, managing resources at the table level.
One approach is to set a global limit on the number of operations per second, distributing this
limit among partitions based on their load. This ensures that no single partition overwhelms a


system, providing a more balanced throughput distribution.
Splitting for consumption – proactive partition management
If you anticipate a drastic change in the load pattern, you might decide to manually split or merge
partitions to prepare for it. This is called “splitting for consumption.”
For splitting, you could use key range partitioning or hash partitioning, depending on your data
distribution and access patterns. The aim is to redistribute data such that each partition gets an
equal share of the load, thereby maximizing throughput efficiency.
In conclusion, optimizing throughput allocation in a partitioned DynamoDB database involves
multiple layers of strategies, each with its unique advantages and limitations. By understanding
and judiciously applying these methods, you can significantly enhance the performance,
reliability, and efficiency of your database operations.
In the next section, we will cover how DynamoDB is designed for high availability for reads and
writes.
High availability in DynamoDB
High availability is a cornerstone of any large-scale database architecture, and DynamoDB is no
exception. In this section, we will explore the various aspects that contribute to the high
availability of reads and writes in DynamoDB. Let’s first discuss the high availability of write
requests in DynamoDB.
Write availability
DynamoDB’s architecture adopts a partitioned model where tables are divided into partitions,
and each partition is further replicated. These replicas of the same partition are termed a
replication group. Leadership among these replicas is determined via a multi-Paxos-based
leader election process. We covered the basics of leader election and multi-Paxos in Chapter 3.
The leader replica manages all write requests by first logging them into a write-ahead log and
then indexing them into memory. The leader replica later disseminates this write-ahead log and
tree index to other replicas within the replication group.
The key to write availability is ensuring that a sufficient number of healthy replicas are available
to form a write quorum. One robust strategy to maintain this availability is for the leader replica


to promptly recruit another member into the replication group if it detects that a replica has
become unresponsive or faulty.
For instance, let’s consider four replication groups. Nodes from group 3 may also be a part of
group 2. If a node in replication group 4 becomes faulty but two-thirds of the nodes are still
operational, it may appear that a quorum can still be formed. However, if the leader replica itself
fails, achieving a quorum becomes impossible. This highlights the critical role of a healthy
leader, as it’s responsible for both processing writes and coordinating the election of a new
leader if there are replica failures.
Now, let’s discuss eventually consistent reads in DynamoDB.
Read availability
Read availability in DynamoDB is gauged by its ability to consistently return the most recent
write upon a read request. DynamoDB’s replication system offers eventual read consistency,
with instant consistent reads provided solely by the leader replica. Therefore, it is crucial to
ensure the leader replica’s health for consistent read availability.
In DynamoDB, much hinges on the leader replica’s reliability. If a leader fails, a new leader
cannot take over until the previous leader’s lease expires. To preemptively address this, the
system should have rapid and accurate failure detection mechanisms. This is complicated by
“gray failures,” which are not straightforward to identify. A reliable way to counter gray failures
is to establish communication protocols among replicas to confirm the leader replica’s status
before initiating a leader election.
By adopting these practices and philosophies, you can ensure that your DynamoDB database
remains highly available, scalable, and efficient, thereby meeting the needs of your ever-evolving
application landscape.
In conclusion, DynamoDB is a robust, serverless NoSQL database offered by AWS, designed for
high performance, scalability, and availability. Its flexible, schema-less architecture
accommodates a wide range of applications and workflows. The database efficiently manages
throughput via mechanisms such as partitioning, bursting, and adaptive capacity. It also ensures
high availability through replication groups and leader election processes for write and read
operations. Overall, DynamoDB’s multilayered strategies for throughput optimization and high
availability make it a reliable, efficient choice for any large-scale, low-latency application.


Column-family databases
Column-family databases, a type of NoSQL database, are designed to handle vast amounts of
data while providing high performance and scalability. They are particularly well-suited for
applications that require the storage and retrieval of large volumes of data with high write and
read throughput. Column-family databases are often used in distributed and horizontally scalable
architectures. Apache Cassandra is one of the most prominent column-family databases.
Here are some key characteristics and concepts of column-family databases:
Data organization: Data in a column-family database is organized into column families, which are essentially groups of
related columns. Each column family contains a set of columns, and these columns can be dynamically added to the column
family. Column families provide a flexible way to structure and store data.
Columns: Columns within a column family are individual data elements. In column-family databases, columns do not need
to be pre-defined, allowing you to add columns to the family as needed. This dynamic approach makes them suitable for
handling evolving data requirements.
Rows: Rows in a column-family database contain data specific to a particular entity or record. Data within a row is
organized based on the column families associated with that row.
A wide-column store: Column-family databases are sometimes referred to as “wide-column stores” because they can
efficiently store a large number of columns for each row. This makes them suitable for applications that need to handle a
wide variety of data attributes for each entity.
Scalability: Column-family databases are designed for horizontal scalability. They can handle large volumes of data and
high traffic by adding additional nodes to a cluster, and distributing data across multiple servers.
High write and read throughput: These databases are optimized for high write and read throughput, making them suitable
for real-time applications where data is constantly updated and retrieved.
Data distribution: Data is distributed across nodes in the cluster, and replication is often employed to ensure fault tolerance
and data availability:
Querying: While column-family databases excel in write-heavy and read-heavy workloads, they are not as
suitable for complex querying compared to relational databases. Queries are typically optimized for key-based
lookups.
Use cases: Column-family databases are commonly used in applications where scalability, high availability, and
fault tolerance are essential, such as time-series data storage, event logging, monitoring systems, and distributed
applications.
Consistency models: Column-family databases often provide tunable consistency levels, allowing you to
balance between data consistency and system performance according to your application’s requirements.
Apache Cassandra is a widely known open-source column-family database. It is particularly
popular for its ability to handle large datasets distributed across multiple nodes, making it a
valuable tool in applications that require high availability and seamless scalability. HBase is


another column-family database that is highly consistent and sacrifices availability to maintain
high consistency, as per the CAP theorem.
HBase
Apache HBase is an open-source, distributed, and scalable NoSQL database management
system that is designed to handle large volumes of data with high read and write throughput. It is
built on top of the Hadoop Distributed File System (HDFS) and was inspired by Google
Bigtable. HBase is known for its ability to provide random and real-time access to massive
amounts of structured data, making it suitable for applications with high data requirements, such
as those found in big data and distributed computing ecosystems.
In short, in HBase, the following applies:
A table is a collection of rows
A row is a collection of column families
A column family is a collection of columns
A column is a collection of key-value pairs
The key features and characteristics of Apache HBase include the following:
Distributed and scalable: HBase is designed to run on clusters of commodity hardware, and it offers horizontal scalability.
It can handle the storage and processing of extremely large datasets by adding more nodes to a cluster.
A column-family data model: Similar to Cassandra, HBase uses a column-family data model. Data is organized into
column families, and each column family can contain a flexible number of columns.
A consistency model: HBase offers strong consistency, making it suitable for applications that require strict data
consistency. It uses a distributed write-ahead log (WAL) to ensure durability and consistency.
Data versioning: HBase supports data versioning, allowing you to access and query previous versions of data, which can be
valuable for historical analysis.
Scalability and load balancing: HBase can automatically handle the distribution of data and load balancing across nodes,
ensuring the efficient use of resources.
High write and read throughput: HBase is designed for high write and read throughput, making it a popular choice for
real-time data processing and analytics.
Hadoop integration: HBase integrates well with the Hadoop ecosystem, and it can be used in conjunction with tools such
as Hadoop MapReduce, Apache Spark, and Apache Hive for data processing and analysis.
Bloom filters and block caches: HBase uses data structures such as bloom filters and BlockCaches to optimize data
retrieval and improve query performance.
Compression: Data compression is supported to reduce storage requirements and improve performance.


Use cases: HBase is commonly used in applications that require random access to large datasets, such as time-series data,
sensor data, log data, and applications related to internet services, including ad targeting and recommendation engines.
A community and ecosystem: As an Apache project, HBase has an active open-source community and a rich ecosystem of
tools, libraries, and connectors that support its development and usage.
HBase is particularly well-suited for applications that need to store and query large volumes of
data in real-time, often with complex data models and high scalability requirements. Its
integration with Hadoop and other big data technologies makes it a valuable choice for
applications in the big data and analytics domains.
HBase details
Let’s look at the design, architecture, and components of Hbase in detail. The concepts we will
discuss here are inspired by the book HBase – the Definitive Guide.
HBase concepts and architecture
Figure 5.9: A diagram showing the different components of HBase architecture, namely the RegionServer colocated with the DataNode, the NameNode, the ZooKeeper, and the HBase Master nodes
HBase comprises three types of servers – RegionServer, HBase Master, and ZooKeeper:
RegionServer: The RegionServer plays a vital role in handling data for both read and write operations. Clients directly
interact with HBase RegionServers when accessing data, and the data it manages is stored in the Hadoop DataNode.
To enhance data locality, RegionServers are co-located with HDFS DataNodes. This ensures
that data is situated close to where it is required, optimizing efficiency. HBase tables undergo


horizontal division into “regions,” based on row key ranges.
Each region spans the range from its start key to its end key, covering all rows within that
boundary. These regions are then assigned to cluster nodes, known as “RegionServers,”
which efficiently serve data for both read and write operations. A RegionServer has the
capacity to handle approximately 1,000 regions. Although the default size of a region is 1
GB, it remains configurable to suit specific requirements.
Figure 5.10: A diagram showing the internals of the RegionServer, with the multiple regions it’s responsible for
HBase Master: The HBase Master process takes charge of tasks such as region assignment and DDL (Data Definition
Language)operations (such as table creation and deletion). In a parallel fashion, the NameNode is responsible for


maintaining metadata information related to all the physical data blocks that constitute the files. Specifically, the HBase
Master oversees region assignment and DDL operations (CREATE, ALTER, TRUNCATE, and DROP).
HBase Master has several key responsibilities:
The coordination of region servers
Assignment of regions during startup, and the reassignment of regions for recovery or load balancing
Monitoring all instances of a RegionServer within the cluster, attentively receiving notifications from a
ZooKeeper
Serving as an interface for crucial table operations, including the creation, deletion, and updating of tables
Figure 5.11: A diagram showing the role of HBase Master in the HBase architecture
ZooKeper: A ZooKeeper actively manages the real-time state of a cluster. In HBase, ZooKeeper
functions as a distributed coordination service, ensuring the up-to-date status of servers in a
cluster. It keeps track of the availability of servers, offering notifications if there are server
failures. Utilizing a consensus approach, ZooKeeper guarantees a shared state among servers.
It’s important to note that a consensus is typically achieved with the involvement of three or five
machines.


Figure 5.12: Shows the role of the ZooKeeper in HBase architecture
META table and .META. server
The META table in HBase, also known as the HBase Catalog table (as shown in Figure 5.13)
stores information about the locations of regions within the cluster. The designated .META.
server, known by the ZooKeeper, manages this special table. The META table functions as an
HBase table, maintaining a comprehensive list of all regions in a system.
The structure of the .META. table is organized as follows:
Key: Consisting of the region’s start key and its unique region ID
Values: Indicating the associated RegionServer


Figure 5.13: This diagram shows the META table and .META. server
RegionServer components
A Region Server, operating on an HDFS data node, comprises the following components (as
shown in Figure 5.14):
WAL: The WAL is a file on the distributed filesystem, used to store new data that is yet to be permanently persisted. Its
primary purpose is to facilitate recovery if there is a failure.
BlockCache: Functioning as the read cache, the BlockCache stores frequently read data in memory. When the cache reaches
its capacity, the Least Recently Used (LRU) data is evicted.
MemStore: Serving as the write cache, the MemStore stores new data awaiting a disk write. It undergoes sorting before
being written to disk. There is one MemStore per column family per region, and updates are stored in memory as sorted
KeyValues, mirroring their storage in an HFile.
HFiles: These files store rows as sorted KeyValues on disk. Data is organized in HFiles, each containing sorted key/values.
When the MemStore accumulates sufficient data, the entire set of sorted KeyValues is sequentially written to a new HFile in
HDFS. This sequential write is exceptionally fast, as it eliminates the need to reposition the disk drive head.


Figure 5.14: Shows the several components inside the RegionServer – namely, BlockCache, WAL, MemsStore,
and HFiles
First HBase access (read or write)
Let’s look at the steps you need to execute when you access HBase for the first time in a read or
write operation?"(as illustrated in Figure 5.15):
1. The client initiates communication with the ZooKeeper to retrieve details about the RegionServer, commonly referred to as
the .META. server, hosting the META table.
2. Subsequently, the client queries the .META. server to obtain information about the specific region server associated with the
desired row key.
3. The client then caches this information, including the location of the META table.
4. With this cached information, the client proceeds to retrieve the row from the pertinent RegionServer.


Figure 5.15: This diagram shows the first HBase read or write access
In subsequent read operations, the client relies on the cache to access the META location and
row keys that were previously retrieved. As time progresses, querying the META table becomes
unnecessary unless there is an occurrence of a miss, due to a region relocation. In such cases, the
client will re-query the META table and update the cache accordingly.
HBase writes
When a client issues a Put request, the first step is to write data to the WAL. This is depicted in
Figure 5.16:
1. Edits are appended to the end of the WAL file that is stored on disk. The WAL is used to recover not-yet-persisted data if a
server crashes. The WAL is in an HDFS/filesystem outside the RegionServer.
2. Once the data is written to the WAL, it is placed in the MemStore. Then, the put request acknowledgment returns to the
client.
Figure 5.16: HBase writes are first written to WAL and then to Memstore, and then they are sent back to the user
We will cover the HBase region flush in the next section.
HBase region flush
When the MemStore accumulates enough data, the entire sorted set is written to a new HFile.
HBase uses multiple HFiles per column family, which contain the actual cells, or KeyValue instances. These files are
created over time as KeyValue edits sorted in the MemStores are flushed as files to disk.
Hbase also saves the last written sequence number so that the system knows what has persisted so far. The highest sequence
number is stored as a meta field in each HFile, reflecting where persistence has ended and where to continue from.
On region startup, the sequence number is read, and the highest is used as the sequence number for new edits.


HBase reads
So, when you read a row, how does a system get the corresponding cells to return?
The KeyValue cells corresponding to one row can be in multiple places:
Row cells already persisted are in HFiles
Recently updated cells are in the MemStore
Recently read cells are in the BlockCache
Figure 5.17: This diagram shows the flow of an HBase read – reading data from the BlockCache, MemStore, and
the HFiles and then consolidating them before returning to the client
So, as shown in Figure 5.17, the read needs to check at all these places and do a merge by
reading the key values from the BlockCache, MemStore, and HFiles in the following steps:
1. First, the scanner looks for the row cells in the BlockCache (the read cache). Recently read key values are cached here, and
the least recently used are evicted when memory is needed.
2. Next, the scanner looks in the MemStore, the write cache in memory containing the most recent writes.
3. If the scanner does not find all of the row cells in the MemStore and BlockCache, then HBase will use the BlockCache
indexes and bloom filters to load HFiles into memory, which may contain the target row cells.


Graph-based databases
Graph-based databases are a type of NoSQL database designed specifically to manage and store
data with complex and interconnected relationships. They are well-suited for applications that
require the modeling and querying of data in a way that reflects the relationships between
various entities. These databases use graph structures to represent data and the connections
between data points, making them highly efficient for traversing and querying complex
relationships. Neo4j is one of the most well-known and widely used graph-based NoSQL
databases.
Here are some key characteristics and concepts of graph-based NoSQL databases:
Graph structure: Data in graph-based NoSQL databases is organized in the form of nodes and edges, creating a graph
structure. Nodes represent entities (such as people, products, or locations), and edges represent the relationships between
these entities.
Nodes: Nodes are the fundamental units of data in a graph. Each node can contain properties (key-value pairs) that provide
information about the entity it represents.
Edges: Edges connect nodes and represent the relationships between them. Edges can also have properties to convey
information about the nature of the relationship.
Labels and relationship types: Nodes and edges can be labeled to group them into categories or types. For example, nodes
representing people could be labeled as “person,” and edges representing friendship could be labeled as “friends.”
Traversal: Graph-based databases are optimized to traverse relationships between nodes. This makes them highly efficient
for queries that involve finding paths, connections, or patterns in data.
Cypher query language: Graph-based databases often use the Cypher query language, specifically designed for querying
and manipulating graph data. Cypher allows users to express complex graph queries in a human-readable and intuitive
format.
Indexing: Graph databases use indexing mechanisms to optimize query performance, allowing for fast lookups based on
specific properties or relationship types.
Scalability: Some graph databases offer horizontal scalability, enabling the distribution of data across multiple nodes for
performance and fault tolerance.
Use cases: Graph-based databases are commonly used in applications that require modeling and analyzing complex
relationships, such as social networks, recommendation engines, fraud detection, network and infrastructure management,
and knowledge graphs.
Pattern matching: These databases excel at pattern matching and can find patterns and connections within the graph,
enabling applications such as social network friend suggestions and personalized recommendations.
Graph-based NoSQL databases are valuable tools for scenarios where understanding and
querying the relationships between data points are critical. They are particularly well-suited for
applications that involve navigating and analyzing intricate and evolving networks of data. For


example, consider a use case where we need to find and track friendship and follower
recommendations in a social network application.
A graph database can quickly traverse the graph to suggest friends of friends (second-degree
connections) or people with similar interests based on common interactions and connections.
Neo4j is an example of a graph-based NoSQL database. Let’s take a deeper dive into Neo4j in
the next section.
The Neo4j graph database
Neo4j is a popular and widely used graph database management system (DBMS), known for
its ability to efficiently store, manage, and query data with complex relationships. It is
specifically designed for applications that require modeling, storing, and traversing intricate and
interconnected data structures. Neo4j is often used in scenarios where understanding and
querying relationships between data points are fundamental, making it well-suited for a wide
range of applications, including social networks, recommendation engines, fraud detection,
network and infrastructure management, and knowledge graphs.
The key features and characteristics of Neo4j include the following:
A graph data model: Neo4j employs a graph data model, representing data as nodes and the relationships between nodes.
This model provides an intuitive way to express and manage complex relationships.
Nodes: Nodes in Neo4j represent entities or data points. Each node can have properties (key-value pairs) that describe the
attributes of the entity it represents.
Relationships: Relationships between nodes define connections and associations between data points. Relationships can
also have properties, providing additional information about the nature of the relationship.
Labels and relationship types: Nodes and relationships can be labeled to group them into categories or types. For example,
nodes representing people could be labeled as “person,” and relationships representing friendships could be labeled as
“friends.”
Cypher query language: Neo4j uses the Cypher query language, specifically designed for querying and manipulating graph
data. Cypher is known for its readability and expressiveness when dealing with complex graph structures.
Indexing and query optimization: Neo4j uses indexing mechanisms to optimize query performance, allowing for efficient
lookups based on specific properties or relationship types.
Scalability: Neo4j supports horizontal scalability, enabling the distribution of data across multiple nodes to enhance
performance and fault tolerance.
ACID compliance: Neo4j ensures data integrity by adhering to ACID properties, which are crucial for maintaining data
consistency.


Data versioning: Neo4j can store and query historical data, making it valuable for scenarios requiring a temporal view of
relationships.
Use cases: Neo4j is commonly used in various applications, including social networks, recommendation systems, fraud
detection, real-time analytics, network and infrastructure management, and knowledge graphs.
Community and ecosystem: Neo4j has an active open source community and offers a rich ecosystem of tools, libraries, and
connectors that support its development and usage.
Neo4j’s strength lies in its ability to efficiently navigate and query complex relationships in the
data, making it a powerful choice for applications where understanding and exploiting data
connections are essential. Its ease of use, scalability, and support for graph-based analytics have
made it a leading choice in the field of graph databases.
Neo4j details
Let’s understand the data modeling and inner workings of the Neo4j database by taking a simple
example. Consider a simple social network graph, where there are many users and they follow
each other. In this example (as shown in Figure 5.18), there are three people, represented by
three nodes (nodes 1, 2, and 3). Node 1 follows 2 and 3. Node 2 follows 3.
Figure 5.18: The relationship between three nodes
Relational modeling versus graph modeling
We have two options to store the data if we adopt a relational modeling point of view:
Store the source and destination of an edge (relationship) as a row, and do that for all the edges, as shown in (a) in Figure
5.19. When you need to find the outgoing edges (whom a particular user follows), you can use an index to “seek” the start of
that user’s outbound relationships.


Store an edge twice and add another column to indicate the direction, as shown in (b) in Figure 5.19.
Figure 5.19: A diagram showing the options to store graph data using a relational model
Graph modeling
Now, if we want to store data using graph modeling, we would represent the data in doubly
linked list graphs and two tables, called nodes and relationships:
Figure 5.20 (a) represents nodes and their relations as doubly linked lists. We have three nodes, hence three linked lists.
Figure 5.20 (b) is the actual node storage. Each record stores the first relationship ID (first_rid) of a node. For example,
the first relationship for both nodes 1 and 2 is A.
Figure 5.20 (c) is the actual relationship storage. Each record stores the source (src) and destination (dst) of a relationship.
In addition, it also stores the previous and next relationship IDs for both the source and destination nodes
(src_prev_rid, src_next_rid, dst_prev_rid, and dst_next_rid).


Figure 5.20: A diagram showing a representation of graph data using graph modeling
Adding a new node to an existing graph
If you want to add node 4 to the graph (as shown in Figure 5.21 (a)), where node 2 follows node
4, you would make changes to the doubly linked lists and the two tables, as follows.
Figure 5.21: A diagram showing the process of adding a new node and relationship to an existing graph


The new node's nid is 4, and we added a new relationship D, where we show that src is 2 and
dst is 4, i.e., node 2 follows node 4.
In the nodes table, you would add an entry with nid = 4 and first_rid = D.
In the relationship table, you would add an entry for the new relationship, D, with the appropriate
entries for the columns (rid, src, dst, src_prev_rid, src_next_rid, dst_prev_rid, and
dst_next_rid) and make changes to the existing entries, as shown in the figure.
Nodes and the relationship store
Node store
All the nodes in the database are stored in the node store file.
Each node record accounts for a fixed 15 bytes.
The layout is as follows:
1st byte — isInUse
Next 4 bytes — ID of the node
Next byte — First relationship ID
Next byte — First property ID
Next 5 bytes — Label store
Remaining byte — for future use
Relationship store
Each relationship record is a fixed record of 34 bytes.
The relationship record’s layout is as follows:
Start node ID
End node ID
Pointer to the relationship type
Pointer to the next and previous relationship record for each of the start node and
end node
Summary


In this chapter, we traversed the landscape of databases, exploring the fundamental concepts and
diverse array of database types that play a pivotal role in modern data management.
We began by unraveling the essence of databases themselves, recognizing their crucial role in
data organization, retrieval, and integrity. Databases serve as the foundation to manage data in
various applications and systems, facilitating informed decision-making and efficient data
processing.
Our exploration then delved into the world of database types, where we encountered two primary
categories – relational databases and NoSQL databases. Relational databases, with their tabular
structure and strong data integrity, are well-suited for applications demanding structured data and
complex relationships. Notable examples include MySQL, PostgreSQL, and Oracle.
At the other side of the spectrum, we embraced the diversity of NoSQL databases, which offer
flexibility and scalability. Within this category, we uncovered key-value stores, which provide
efficient data retrieval and storage, and specifically explored Amazon DynamoDB as an example
of this type. We navigated the landscape of column-family databases, where Apache Cassandra
and HBase emerged as scalable solutions to handle extensive data volumes and write-heavy
workloads. We took a deep dive into the HBase design, architecture, and inner workings.
Our journey continued to the realm of graph-based databases. These databases excel in
representing and navigating complex relationships, making them invaluable for applications with
intricate network structures, such as social networks, recommendation engines, and knowledge
graphs. We specifically looked into Neo4j as an example of the graph database and explored it in
a bit more detail.
In conclusion, our chapter traversed the spectrum of databases, from the structured world of
relational databases to the versatile landscape of NoSQL, encompassing key-value stores,
column-family databases, and graph-based databases. This understanding empowers us to make
informed choices when selecting the right database type for the unique demands of each
application and data scenario.
In the next chapter, we will look at caches and their types and purposes in software system
design.
References


HBase – The Definitive Guide: https://www.oreilly.com/library/view/hbase-thedefinitive/9781449314682/

## Examples & Scenarios

- Rows: Each row in a table, often referred to as a “record” or “tuple,” represents a unique data entry. For example, in a
“customers” table, each row corresponds to an individual customer, with each column containing specific information about
that customer, such as their name, address, and phone number.
Columns: Columns, also known as “attributes” or “fields,” define the type of data that can be stored in a table. Each column
has a name and a data type, such as text, numeric, date, or binary.
Keys: Relational databases use keys to establish relationships between tables. The primary key uniquely identifies each row
in a table, while foreign keys in one table refer to the primary key in another table, creating relationships between them.
Normalization: The process of normalization is used to eliminate data redundancy and improve data integrity. It involves
breaking down tables into smaller, related tables to reduce duplication and maintain consistency.
Structured Query Language (SQL): SQL is the language used to interact with relational databases. It provides a

- For instance, consider a scenario where we have four nodes, and we aim to balance the load
equally by directing 25% of requests to each node. Traditionally, we would use the modulus
operator to achieve this. Each incoming request comes with an associated key. On receiving a
request, we calculate the hash of the key and then find the remainder when the hashed value is
divided by the number of nodes (m). The remainder value (x) indicates the node number to which
we route the request for processing. Figure 5.1 shows a key that is hashed, and a modulo
operation is applied to the result to determine the node to which the request carrying that keyvalue pair should be routed.
Figure 5.1: A modulo-based key-value pair routing
However, this method falls short when we add or remove nodes, as we end up having to move a
significant number of keys, which is inefficient. For example, if we remove node 2, the new

- For instance, if we have three hash functions, we calculate three hashes for each node and place
them onto the ring. For the request, we use only one hash function. Wherever the request lands
on the ring, it’s processed by the next node found when moving in a clockwise direction. Each
server has three positions, so the request load is more uniform. Furthermore, if a node has more
hardware capacity than others, we can add more virtual nodes by using additional hash functions.
This way, it’ll have more positions in the ring and serve more requests.
The advantages of virtual nodes
Virtual nodes offer the following benefits:
If a node fails or undergoes routine maintenance, the workload is uniformly distributed over other nodes. For each newly
accessible node, the other nodes receive nearly equal load when it comes back online or is added to a system.

- infrastructure. For example, if a node has roughly double the computational capacity compared to the others, it can handle
more load.
Now that we’ve made our key-value storage design scalable, the next step is to make our system
highly available. To ensure high availability, we need to introduce replication strategies and
mechanisms to handle failures, which will be the focus of the following sections.
Data duplication strategies
There are several ways to duplicate data in a storage system. The two main methods are the
primary-secondary model and the peer-to-peer model.
The primary-secondary model
In this model, one storage area is designated as the primary, while the others act as secondary

- for each instance of the key-value store. For instance, if we set n to five, our data will be
replicated across five nodes.
Each node will copy its data to other nodes. The node responsible for handling read or write
operations is called the coordinator. The coordinator node is directly responsible for specific
keys. For example, if a coordinator node is assigned the key K, it is also responsible for
duplicating these keys to n-1 successors on the ring (going clockwise). These lists of successor
virtual nodes are known as preference lists. To prevent placing replicas on identical physical
nodes, the preference list can bypass those virtual nodes whose physical node is already listed.
Let’s now discuss some of the nuances in implementing the get and the put functions in our keyvalue store.
Implementing get and put functions

- Synchronization isn’t necessary if, for instance, two trees’ root hashes and leaf nodes are
identical. Hosts can identify out-of-sync keys as they exchange the hash values of children,
continuing until they reach the tree leaves. This anti-entropy mechanism ensures data
consistency while reducing data transmission and disk access during synchronization.
Here’s how Merkle trees function:
Hash all keys to create leaf nodes.
Each node maintains a unique Merkle tree for the key range it hosts for every virtual node. Nodes can verify the correctness
of keys within a given range. Two nodes exchange the Merkle tree root corresponding to common key ranges. The
comparison proceeds as follows:
I. Compare the root node hashes of Merkle trees.

- respectively. These units are crucial when discussing throughput optimization. For example, if a
table has a provisioned throughput of 20,000 RCUs and 5,000 WCUs, it implies that the system

- redistributed among the existing partitions. For instance, if a table initially had 10 partitions,
each with 2,000 RCUs and 500 WCUs, and you add 10 more, the throughput of each partition
would be halved to accommodate the new partitions.
Let’s now understand how bursting can help with throughput management, with unevenly
distributed reads and writes in a DynamoDB table.
Bursting – short-term overprovisioning
In real-world scenarios, applications or users can disproportionately access certain keys, causing
uneven distribution of requests across partitions. Bursting is a strategy to temporarily tap into
any unused throughput from neighboring partitions to manage these short-term spikes in
demand.

- For instance, let’s consider four replication groups. Nodes from group 3 may also be a part of
group 2. If a node in replication group 4 becomes faulty but two-thirds of the nodes are still
operational, it may appear that a quorum can still be formed. However, if the leader replica itself
fails, achieving a quorum becomes impossible. This highlights the critical role of a healthy
leader, as it’s responsible for both processing writes and coordinating the election of a new
leader if there are replica failures.
Now, let’s discuss eventually consistent reads in DynamoDB.
Read availability
Read availability in DynamoDB is gauged by its ability to consistently return the most recent
write upon a read request. DynamoDB’s replication system offers eventual read consistency,

- Labels and relationship types: Nodes and edges can be labeled to group them into categories or types. For example, nodes
representing people could be labeled as “person,” and edges representing friendship could be labeled as “friends.”
Traversal: Graph-based databases are optimized to traverse relationships between nodes. This makes them highly efficient
for queries that involve finding paths, connections, or patterns in data.
Cypher query language: Graph-based databases often use the Cypher query language, specifically designed for querying
and manipulating graph data. Cypher allows users to express complex graph queries in a human-readable and intuitive
format.
Indexing: Graph databases use indexing mechanisms to optimize query performance, allowing for fast lookups based on
specific properties or relationship types.
Scalability: Some graph databases offer horizontal scalability, enabling the distribution of data across multiple nodes for

- Labels and relationship types: Nodes and relationships can be labeled to group them into categories or types. For example,
nodes representing people could be labeled as “person,” and relationships representing friendships could be labeled as
“friends.”
Cypher query language: Neo4j uses the Cypher query language, specifically designed for querying and manipulating graph
data. Cypher is known for its readability and expressiveness when dealing with complex graph structures.
Indexing and query optimization: Neo4j uses indexing mechanisms to optimize query performance, allowing for efficient
lookups based on specific properties or relationship types.
Scalability: Neo4j supports horizontal scalability, enabling the distribution of data across multiple nodes to enhance
performance and fault tolerance.
ACID compliance: Neo4j ensures data integrity by adhering to ACID properties, which are crucial for maintaining data

- example. Consider a simple social network graph, where there are many users and they follow
each other. In this example (as shown in Figure 5.18), there are three people, represented by
three nodes (nodes 1, 2, and 3). Node 1 follows 2 and 3. Node 2 follows 3.
Figure 5.18: The relationship between three nodes
Relational modeling versus graph modeling
We have two options to store the data if we adopt a relational modeling point of view:
Store the source and destination of an edge (relationship) as a row, and do that for all the edges, as shown in (a) in Figure
5.19. When you need to find the outgoing edges (whom a particular user follows), you can use an index to “seek” the start of
that user’s outbound relationships.

- Figure 5.20 (b) is the actual node storage. Each record stores the first relationship ID (first_rid) of a node. For example,
the first relationship for both nodes 1 and 2 is A.
Figure 5.20 (c) is the actual relationship storage. Each record stores the source (src) and destination (dst) of a relationship.
In addition, it also stores the previous and next relationship IDs for both the source and destination nodes
(src_prev_rid, src_next_rid, dst_prev_rid, and dst_next_rid).

## Tables & Comparisons

| n | r | w | Description |
| --- | --- | --- | --- |
| 3 | 2 | 1 | Violates constraint – + >
r w n |
| 3 | 2 | 2 | Fulfills constraint |
| 3 | 3 | 1 | Slow reads and fast writes |
| 3 | 1 | 3 | Slow writes and fast reads |

