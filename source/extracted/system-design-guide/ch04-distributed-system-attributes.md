# Chapter 2: Distributed System Attributes

> Source: System Design Guide for Software Professionals, Chapter 4, Pages 48-63

## Key Concepts

- 2
Distributed System Attributes
Distributed systems have become an integral part of modern computing infrastructure. With the
rise of cloud computing and the internet, distributed systems have become 
- Figure 2.1 – Hotel room booking request flow
As shown in Figure 2.1, a user (u1) is booking a room (r1) in a hotel and another user is trying to
see the availability of the same room (r1) in that hote

## Content

2
Distributed System Attributes
Distributed systems have become an integral part of modern computing infrastructure. With the
rise of cloud computing and the internet, distributed systems have become increasingly important
for providing scalable and reliable services to users around the world. However, designing and
operating distributed systems can be challenging due to several factors, including the need for
consistency, availability, partition tolerance, and low latency. Other attributes, such as
scalability, durability, reliability, and fault tolerance, are critical requirements for any business
application catering to a large and diverse demography. A good understanding of these attributes
is crucial to designing large and complex systems that address business needs.
In this chapter, we will understand how these distributed system attributes come into play when
we think about designing a distributed system. We may need to make appropriate trade-offs
among these attributes to satisfy the system requirements.
We will be covering the following concepts in detail in this chapter:
Consistency
Availability
Partition tolerance
Latency
Durability
Reliability
Fault tolerance
Scalability
A hotel room booking example
Before we jump into the different attributes of a distributed system, let’s set some context in
terms of how reads and writes happen.
Let’s consider an example of a hotel room booking application (Figure 2.1). A high-level design
diagram helps us understand how writes and reads happen:


Figure 2.1 – Hotel room booking request flow
As shown in Figure 2.1, a user (u1) is booking a room (r1) in a hotel and another user is trying to
see the availability of the same room (r1) in that hotel. Let’s say we have three replicas of the
reservations database (db1, db2, and db3). There can be two ways the writes get replicated to the
other replicas: The app server itself writes to all replicas or the database has replication support
and the writes get replicated without explicit writes by the app server.
Let’s look at the write and the read flows:
Write flow:
User (u1) books a room (r1). The device/client makes an API call to book a room (u1,r1) to the
app server. The server writes to one, a few, or all of the replicas.
Read flow:
User (u2) checks the availability of room (r1). The device/client makes an API call in
RoomAvailable (r1) to the app server. The server reads from one, a few, or all of the replicas.
Write options:
For write, we have the following options:
Serial sync writes: The server writes to db1 and gets an ack, then writes to db2 and gets an ack, and then writes to db3 and
gets an ack. Finally, it acks the client. In this case, the response latency back to the user (u1) would be very high.


Serial async writes: The server writes to db1 and gets an ack. The server asks the client. Asynchronously, the server
updates the other two replicas. Write latency is low.
Parallel async writes: The server fires three updates simultaneously, but doesn’t wait for all the acks, gets one (or k) acks,
and then returns an ack to the client. Latency is low, but thread resource usage is high.
Write to a messaging service such as Kafka and return an ack to the client. A consumer then picks up the writes and follows
any of the aforementioned options. Latency in this case is the lowest. It can support very high writes.
Read options:
For read, we have the following options:
Read from only one replica
Read from a quorum number of replicas
Read from all replicas and then return to the client
Each of these read options comes with consistency trade-offs. For example, if we read from only
one replica, the read may be stale in some situations, posing a correctness problem. On the other
hand, reading from all replicas and comparing all the values to determine which one is the latest
value addresses the correctness problem, but this would be slower. Reading from a quorum
number of replicas may be a more balanced approach. We will explore these trade-offs more in
the following sections.
We will use this context in understanding the distributed system attributes.
Consistency
Consistency in distributed system design is the idea that all nodes in a distributed system should
agree on the same state or view of the data, even though the data may be replicated and
distributed across multiple nodes. In other words, consistency ensures that all nodes store the
same data and return updates to the data in the same order on being queried for the same updates
to the data in the same order.
There are primarily two types of consistency models that can be used in distributed systems:
Strong consistency
Eventual consistency
Let’s explore the first type of consistency.
Strong consistency


Strong consistency in distributed systems refers to a property that ensures all nodes in the system
observe the same order of updates to shared data. It guarantees that when a write operation is
performed, any subsequent read operation will always return the most recent value. Strong
consistency enforces strict synchronization and order of operations, providing a linearizable view
of the system.
To achieve strong consistency, distributed systems employ mechanisms such as distributed
transactions, distributed locking, or consensus protocols such as the Raft or Paxos algorithms.
These mechanisms coordinate the execution of operations across multiple nodes, ensuring that
all nodes agree on the order of updates and maintain a consistent state.
Strong consistency offers a straightforward and intuitive programming model as it guarantees
predictable and deterministic behavior. Developers can reason about the system’s state and make
assumptions based on the order of operations. However, achieving strong consistency often
comes at the cost of increased latency and reduced availability as the system may need to wait
for synchronization or consensus before executing operations.
A good example of a system that would require a strong consistency model is a banking system.
Banking and financial applications deal with sensitive data, such as account balances and
transaction histories. Ensuring strong consistency is crucial to avoid discrepancies and to prevent
erroneous operations that could lead to financial losses or incorrect accounting.
Eventual consistency
Eventual consistency, on the other hand, is a consistency model that allows for temporary
inconsistencies in the system but guarantees that eventually, all replicas or nodes will converge
to a consistent state. In other words, it allows updates that are made to the system to propagate
asynchronously across different nodes, and eventually, all replicas will agree on the same value.
Unlike strong consistency, where all nodes observe the same order of updates in real-time,
eventual consistency relaxes the synchronization requirements and accepts that there may be a
period during which different nodes have different views of the system’s state. This temporary
inconsistency is typically due to factors such as network delays, message propagation, or replica
synchronization.
Eventual consistency is often achieved through techniques such as conflict resolution,
replication, and gossip protocols. When conflicts occur, such as concurrent updates to the same


data on different nodes, the system applies conflict resolution strategies to reconcile the
differences and converge toward a consistent state. Replication allows updates to be propagated
to multiple replicas asynchronously, while gossip protocols disseminate updates across the
system gradually.
The key characteristic of eventual consistency is that given enough time, without further updates
or conflicts, all replicas will eventually converge to the same value. The convergence time
depends on factors such as network latency, update frequency, and conflict resolution
mechanisms.
Eventual consistency offers benefits such as increased availability and scalability and faster
response times to the client application. It allows different nodes to continue operating and
serving requests, even in the presence of network partitions or temporary failures. It also
provides the opportunity to distribute the workload across different replicas, improving system
performance.
However, eventual consistency introduces the challenge of dealing with temporary
inconsistencies or conflicts. Applications must handle scenarios where different nodes may have
different views of the system’s state and employ techniques such as conflict resolution,
versioning, or reconciliation algorithms to ensure eventual convergence.
The choice of consistency model, whether strong consistency or eventual consistency, depends
on the specific requirements of the application. Strong consistency is suitable for scenarios where
immediate and strict synchronization is required, while eventual consistency is a trade-off that
offers increased availability and scalability at the expense of temporary inconsistencies.
In the hotel room booking example, as shown diagrammatically in Figure 2.2, when user (u1)
books the room, let’s say the write goes to only db1 and then it gets replicated to db2 and db3.
While this is being replicated, user (u2) makes a call to check if the room (r1) is available for
booking. The API call may return “true” or “false” depending on whether the write has been
replicated to db2 or not:


Figure 2.2 – Hotel room booking example to understand consistency
As system designers, we have the option to design strong consistency or eventual consistency.
Let’s see how we do that.
In this scenario, we have the following:
n = the number of replicas
r = the number of replicas we consider reading from
w = the number of replicas we consider writing to
We talk to all n replicas, but consider w or r number of replicas for evaluation.
Here are our options:
a. w=1, r=3 → strong consistency, fast writes, slow reads
b. w=3, r=1 → strong consistency, slow writes, fast reads
c. w=2, r=2 → strong consistency, writes and reads are both the same pace
d. w=1, r=1 → eventual consistency, fast writes, fast reads
NOTE
We always have strong consistency if (r+w) > n; otherwise, it’s eventual consistency.


Is eventual consistency okay in this hotel booking use case? The answer may seem trivial at this
point. We want to have strong consistency, right? Well, that may not be the case if we consider
availability in the mix. Sometimes, we may want eventual consistency as a trade-off to have
higher availability. More on this in the next section.
Availability
Availability in distributed system design refers to the ability of a distributed system to provide
access to its services or resources to its users, even in the presence of failures. In other words, an
available system is always ready to respond to requests and provide its services to users,
regardless of any faults or failures that may occur in the system.
In the hotel room booking example, the system can be highly available if the writes and reads
happen from only one or a quorum of replicas. This ensures that the user requests will be served
by fewer nodes and doesn’t require all the nodes to be up. So, in case one or more nodes are in a
failed state, the system as a whole is available to take writes and reads.
Achieving high availability in distributed systems can be challenging because distributed
systems are composed of multiple components, each of which may be subject to failures such as
crashes, network failures, or communication failures.
To ensure availability, distributed systems employ various techniques and strategies, including
the following:
Redundancy: Having redundant components or resources enables the system to continue functioning, even if some
components fail. Redundancy can be implemented at various levels, such as hardware redundancy (for example, redundant
power supplies or network links) and software redundancy (for example, redundant processes or service instances).
Replication: When there is redundancy in the system, we need to replicate the data across these multiple redundant nodes.
Replicating data or services across multiple nodes helps ensure that even if one or more nodes fail, others can take over and
continue to provide the required functionality. Replication can be done through techniques such as active-passive
replication, where one node serves as the primary while others act as backups, or active-active replication, where multiple
nodes serve requests simultaneously.
Load balancing: Distributing the workload evenly across multiple nodes helps prevent the overloading of individual nodes
and ensures that resources are efficiently utilized. Load balancing mechanisms route incoming requests to available nodes,
optimizing resource utilization and avoiding CPU, memory, or I/O bottlenecks that may arise if all requests are served by a
small subset of nodes.
Fault detection and recovery: Distributed systems employ mechanisms to detect failures or faults in nodes or components.
Techniques such as heartbeating, monitoring, or health checks are used to identify failed nodes, and recovery mechanisms
are implemented to restore or replace failed components.


Failover and failback: Failover mechanisms automatically redirect requests from a failed node or component to a backup or
alternative node. Failback mechanisms restore the failed node or component once it becomes available again.
By implementing these techniques, distributed systems can provide high availability, reducing
the impact of failures or disruptions and ensuring continuous access to services or resources.
However, achieving high availability often involves trade-offs, such as increased complexity,
resource overhead, or potential inconsistencies or performance compromises, which need to be
carefully considered based on the specific requirements of the system.
Understanding partition tolerance
Before we take a look at partition tolerance, let’s understand what a partition (or network
partition) is.
Network partition
A network partition in distributed systems refers to a situation where a network failure or issue
causes a subset of nodes or components to become disconnected or isolated from the rest of the
system, forming separate groups or partitions. In other words, the network partition divides the
distributed system into multiple disjoint segments that cannot communicate with each other.
Network partitions can occur due to various reasons, such as network failures, hardware
malfunctions, software bugs, or unintentional consequences due to planned actions such as
network configuration changes or network attacks. An example is shown in Figure 2.3, where
the db2 node is isolated and can’t communicate with the other two nodes. When a network
partition happens, the nodes on one side of the partition can no longer send messages or
exchange information with the nodes on the other side. In this example, any writes to db1 or db3
can’t propagate updates to db2. In this scenario, if a user’s read requests land on db2, it may
serve stale data:


Figure 2.3 – Network partition scenario
Hence, the existence of network partitions poses challenges for distributed systems because it
disrupts the communication and coordination between nodes. Nodes within the same partition
can continue to interact and operate normally, but they are unable to reach nodes in other
partitions. This can lead to inconsistencies, conflicts, and challenges in maintaining system
properties such as consistency, availability, and fault tolerance.
Network partitions, as shown in Figure 2.3, can have different characteristics and implications
based on their duration and severity. They can be transient, lasting for a short period, and
resolving automatically once the network issue is resolved. Alternatively, partitions can be longlasting or permanent if network connectivity cannot be restored.
Partition tolerance
Now, partition tolerance (or network partition tolerance) is a property of distributed systems that
refers to the system’s ability to continue functioning despite network failures or network
partitions.
In a distributed system that is designed with network partition tolerance, the system can continue
to operate despite these network failures. Nodes that are isolated due to a network partition can
still function independently and serve their clients, while the rest of the system continues to


operate as usual. When we discuss the CAP theorem (in the next chapter), we will see how the
system behaves when they are partition-tolerant and what trade-off we need to make between
consistency and availability.
Partition tolerance holds immense significance in distributed systems, particularly in scenarios
where high availability is crucial, such as cloud computing, distributed databases, and large-scale
distributed applications. By embracing partition tolerance, distributed systems can ensure
uninterrupted operations and graceful degradation in the face of network failures or partitions,
thereby enhancing robustness and fault tolerance.
Latency
Latency is the time delay between the initiation of a request and the response to that request in a
distributed system design. In other words, it is the time it takes for data to travel from one point
to another in a distributed system.
Latency is an important metric in distributed system design because it can affect the performance
of the system and the user experience. A system with low latency will be able to respond to
requests quickly, providing a better user experience, while a system with high latency may
experience delays and be perceived as slow or unresponsive.
Latency can be influenced by a variety of factors, including the distance between nodes in the
system, network congestion, processing time at each node, and the size and complexity of the
data being transmitted.
Reducing latency in distributed systems can be challenging as it involves optimizing various
aspects of the system. Some techniques and strategies to mitigate latency include the following:
Network optimization: Optimizing network infrastructure, such as using high-speed connections, reducing network hops,
and minimizing network congestion, can help reduce latency.
Caching: Implementing caching mechanisms at various levels, such as in-memory caching or content delivery networks
(CDNs), can improve response times by serving frequently accessed data or content closer to the user.
Data localization: Locating data or services closer to the users or consumers can help reduce latency. This can be achieved
through data replication, edge computing, or utilizing content distribution strategies.
Asynchronous communication: Using asynchronous communication patterns, such as message queues or event-driven
architectures, can decouple components and reduce the impact of latency by allowing parallel processing or non-blocking
interactions.
Performance tuning: Optimizing system configurations, database queries, algorithms, and code execution can help improve
overall system performance and reduce latency.


It’s important to note that while minimizing latency is desirable, it may not always be possible to
eliminate it entirely. Distributed systems often operate in environments with inherent network
delays, and achieving extremely low latency may come at the cost of other system properties,
such as consistency or fault tolerance. Therefore, the appropriate trade-offs should be made
based on the specific requirements and constraints of the distributed system.
Durability
Durability in a distributed system design is the ability of the system to ensure that data stored in
the system is not lost due to failures or errors. It is an important property of distributed systems
because the system may be composed of multiple nodes, which may fail or experience errors,
potentially leading to data loss or corruption.
To achieve durability, a distributed system may use techniques such as replication and backup.
Data can be replicated across multiple nodes in the system so that if one node fails, the data can
still be retrieved from another node. Additionally, backup systems may be used to store copies of
data in case of a catastrophic failure or disaster.
Durability is particularly important in systems that store critical data, such as financial or medical
records, as well as in systems that provide continuous service, such as social media or messaging
platforms. By ensuring durability, we can ensure that the system is reliable and that data is
always available to users.
It is important to note that durability is closely related to other properties of distributed systems,
such as consistency and availability. Achieving high durability may require trade-offs with other
properties of the system. Hence, we must carefully balance these factors when designing and
implementing a distributed system.
Reliability
Reliability in distributed systems means that the system can consistently provide its intended
functionality, despite the occurrence of various failures and errors such as hardware failures,
network issues, software bugs, and human errors. A reliable distributed system ensures that data
and services are always available, accessible, and delivered promptly, even in the face of these
challenges.


Reliability is a crucial aspect of distributed systems, which are composed of multiple
interconnected nodes or components working together to achieve a common goal. Achieving
reliability in distributed systems requires the implementation of various techniques, such as
redundancy, fault tolerance, replication, load balancing, and error handling. These techniques
help prevent, detect, and recover from failures, ensuring that the system remains operational and
consistent in its behavior.
Fault tolerance
Fault tolerance in distributed systems means that the system continues functioning correctly in
the presence of component failures or network problems. It involves designing and implementing
a system that can detect and recover from faults automatically, without any human intervention.
To achieve fault tolerance, distributed systems employ various techniques, such as redundancy,
replication, and error detection and recovery mechanisms. Redundancy involves duplicating
system components or data to ensure that if one fails, another can take its place without
disrupting the overall system. Replication involves creating multiple copies of data or services in
different locations so that if one location fails, others can still provide the required service.
Error detection and recovery mechanisms involve constantly monitoring the system for errors or
failures and taking appropriate actions to restore its normal functioning. For example, if a node
fails to respond, the system may try to communicate with another node or switch to a backup
component to ensure uninterrupted service.
Overall, fault tolerance ensures that distributed systems can continue to provide their services
even in the presence of failures or errors, increasing their reliability and availability.
Scalability
Scalability in distributed systems refers to the ability of a system to handle an increasing
workload as the number of users or size of data grows, without sacrificing performance or
reliability. It involves designing and implementing a system that can efficiently and effectively
handle larger amounts of work, either by adding more resources or by optimizing existing
resources.
In distributed systems, there are primarily two types of scaling – vertical scaling and horizontal
scaling (as shown in Figure 2.4):


Vertical scaling (scaling up)
Horizontal scaling (scaling out):
Figure 2.4 – Vertical scaling versus horizontal scaling
Let’s look into these two types of scaling in detail.
Vertical scaling
Vertical scaling, also known as scaling up, involves increasing the capacity of an individual
node/instance or resource within the node. It typically involves upgrading hardware components,
such as increasing the CPU power, adding more memory, or expanding storage capacity. Vertical
scaling focuses on improving the performance of a single node to handle increased workloads or
demands.
Here are some of the advantages of vertical scaling:
Simplicity: It generally requires minimal changes to the existing system architecture or software
Cost-effectiveness for smaller workloads: Vertical scaling can be a more cost-effective approach for systems with
relatively lower workloads as it eliminates the need for managing and maintaining a large number of nodes
However, there are limitations to vertical scaling:


Hardware limitations: There is a limit to how much a single node can be upgraded in terms of CPU power, memory, or
storage. Eventually, a point is reached where further upgrades become impractical or too expensive.
Single point of failure: Since the system relies on a single node, in case that node fails, the entire system may become
unavailable.
In the next section we will discuss horizontal scaling.
Horizontal scaling
Horizontal scaling, also known as scaling out, involves adding more nodes or instances to the
distributed system to handle increased workloads or demands. It focuses on distributing the
workload across multiple nodes, allowing for parallel processing and improved system capacity.
Here are the advantages of horizontal scaling:
Increased capacity and performance: By adding more nodes, the system can handle a higher volume of requests or data
processing, leading to improved performance and responsiveness.
Fault tolerance: With multiple nodes, the system becomes more resilient to failures. If one node fails, the others can
continue to operate, ensuring the availability of the system.
Horizontal scaling also has considerations and challenges:
Distributed coordination: Distributing the workload across multiple nodes requires effective coordination and
synchronization mechanisms to ensure consistent and correct results.
Data consistency: Maintaining data consistency can be more challenging in distributed systems compared to vertical
scaling, where data resides on a single node. Techniques such as distributed transactions or eventual consistency need to be
employed to handle data across multiple nodes.
It’s worth noting that vertical and horizontal scaling are not mutually exclusive, and they can be
combined to achieve the desired scalability and performance goals for a distributed system.
Often, a combination of both approaches is used to scale different components or layers of the
system effectively. The choice between vertical and horizontal scaling depends on factors such
as the specific requirements of the system, workload patterns, cost considerations, and the ability
to effectively distribute and coordinate the workload across multiple nodes.
To ensure scalability, distributed systems must be designed with a modular and loosely coupled
architecture, which allows for easy addition or removal of components as needed. Additionally,
the system must be able to dynamically adjust its resource allocation in response to changing
workload demands.


Overall, scalability is crucial for distributed systems as it allows them to handle increasing
workloads and continue providing their services effectively and efficiently.
Summary
In this chapter, we explored the critical aspects of distributed system design, including
consistency, availability, partition tolerance, latency, durability, reliability, fault tolerance, and
scalability. We examined the importance of achieving consistency to ensure all nodes in a
distributed system observe the same updates in the same order. Additionally, we discussed
different consistency models, such as strong consistency and eventual consistency, and their
implications for system design.
Ensuring high availability in distributed systems poses challenges due to the potential for system
failures. We examined techniques such as redundancy, replication, and failover, all of which can
be employed to improve system availability. We also emphasized the significance of considering
partition tolerance, which refers to the system’s ability to continue functioning despite network
failures or partitions. Designing distributed systems with effective partition tolerance capabilities
is crucial for maintaining system reliability and uninterrupted operation.
Latency, another critical factor in distributed system design, was explored in detail. We
discussed how latency, the time delay between request initiation and response, can be influenced
by various factors, including network congestion, node distances, data size, and processing time.
Understanding and managing latency is essential for optimizing system performance and
ensuring timely and efficient communication between distributed system components.
Durability and reliability are crucial considerations in distributed systems. We examined
techniques such as replication, backup, redundancy, and fault tolerance, all of which contribute
to achieving data durability and consistent system functionality, even in the presence of failures
or errors. Finally, we explored scalability in distributed systems, discussing the benefits and
considerations of vertical scaling (scaling up) and horizontal scaling (scaling out) to handle
increasing workloads without sacrificing performance or reliability.
By gaining a comprehensive understanding of these fundamental aspects of distributed system
design, you will be better equipped to make informed decisions and address challenges in your
own distributed system architectures.


In the next chapter, we will dive deeper into understanding distributed systems by discussing the
relevant theorems and data structures.

## Examples & Scenarios

- Each of these read options comes with consistency trade-offs. For example, if we read from only
one replica, the read may be stale in some situations, posing a correctness problem. On the other
hand, reading from all replicas and comparing all the values to determine which one is the latest
value addresses the correctness problem, but this would be slower. Reading from a quorum
number of replicas may be a more balanced approach. We will explore these trade-offs more in
the following sections.
We will use this context in understanding the distributed system attributes.
Consistency
Consistency in distributed system design is the idea that all nodes in a distributed system should
agree on the same state or view of the data, even though the data may be replicated and

- components fail. Redundancy can be implemented at various levels, such as hardware redundancy (for example, redundant
power supplies or network links) and software redundancy (for example, redundant processes or service instances).
Replication: When there is redundancy in the system, we need to replicate the data across these multiple redundant nodes.
Replicating data or services across multiple nodes helps ensure that even if one or more nodes fail, others can take over and
continue to provide the required functionality. Replication can be done through techniques such as active-passive
replication, where one node serves as the primary while others act as backups, or active-active replication, where multiple
nodes serve requests simultaneously.
Load balancing: Distributing the workload evenly across multiple nodes helps prevent the overloading of individual nodes
and ensures that resources are efficiently utilized. Load balancing mechanisms route incoming requests to available nodes,
optimizing resource utilization and avoiding CPU, memory, or I/O bottlenecks that may arise if all requests are served by a

- failures and taking appropriate actions to restore its normal functioning. For example, if a node
fails to respond, the system may try to communicate with another node or switch to a backup
component to ensure uninterrupted service.
Overall, fault tolerance ensures that distributed systems can continue to provide their services
even in the presence of failures or errors, increasing their reliability and availability.
Scalability
Scalability in distributed systems refers to the ability of a system to handle an increasing
workload as the number of users or size of data grows, without sacrificing performance or
reliability. It involves designing and implementing a system that can efficiently and effectively
handle larger amounts of work, either by adding more resources or by optimizing existing

