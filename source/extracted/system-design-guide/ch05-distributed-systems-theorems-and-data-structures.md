# Chapter 3: Distributed Systems Theorems and Data Structures

> Source: System Design Guide for Software Professionals, Chapter 5, Pages 64-89

## Key Concepts

- 3
Distributed Systems Theorems and Data Structures
Various theorems, algorithms, and data structures play a crucial role in the design and
implementation of distributed systems. By exploring these con
- The CAP theorem, also known as Brewer’s theorem, is a fundamental principle in distributed
systems. It states that a distributed system cannot simultaneously provide consistency,
availability, and par

## Content

3
Distributed Systems Theorems and Data Structures
Various theorems, algorithms, and data structures play a crucial role in the design and
implementation of distributed systems. By exploring these concepts, we aim to provide a solid
foundation for understanding and tackling the intricacies of building reliable, scalable, and faulttolerant distributed systems.
We will dive deeper into a collection of essential theorems that form the theoretical
underpinnings of distributed systems. These theorems provide formal proofs and insights into
various aspects of distributed computing, such as consensus protocols, distributed algorithms,
and fault tolerance. We’ll examine classical theorems such as the CAP theorem, the PACELC
theorem, the FLP impossibility result, and the Byzantine generals problem (BGP), among
others. These theorems serve as guiding principles for reasoning about the limitations and
possibilities of distributed systems. With a solid grasp of the foundational theorems, we’ll shift
our focus to various techniques and data structures that are used in distributed systems.
We will cover the following topics in this chapter:
CAP theorem
PACELC theorem
The Paxos and Raft algorithms
BGP
FLP impossibility theorem
Consistent hashing
Bloom filters
Count-min sketch
HyperLogLog
Let's begin by exploring the CAP theorem.
CAP theorem


The CAP theorem, also known as Brewer’s theorem, is a fundamental principle in distributed
systems. It states that a distributed system cannot simultaneously provide consistency,
availability, and partition tolerance all at once. The acronym CAP represents the three properties.
In distributed systems, network partitions are an inevitable occurrence due to various reasons,
such as hardware failures, network outages, or even routine maintenance. These partitions lead to
nodes being split into isolated groups, disrupting the normal flow of communication.
Consequently, the system faces a crucial decision in the face of such partitions: prioritizing
between consistency and availability. On one hand, if a system opts for availability and
partition tolerance (AP), it continues to function despite the partition but may sacrifice
consistency, meaning all nodes might not have the same data at the same time. On the other
hand, prioritizing consistency and partition tolerance (CP) ensures all nodes have the same
data, but this might come at the cost of the system’s availability, potentially leading to
downtimes or reduced functionality during partitions. It’s important to note that compromising
between these three aspects – consistency, availability, and partition tolerance – is fundamentally
impossible due to the CAP theorem.
In a distributed system, especially those spread across multiple locations or relying on the
internet, network partitions are inevitable. These partitions can be caused by various factors, such
as hardware failures, network outages, routing issues, or even large-scale disasters. Given this
inevitability, a system must be designed to handle such partitions. Ignoring partition tolerance
means assuming a perfect, fault-free network, which is unrealistic in practical scenarios.
Essentially, when a distributed system encounters a network partition, where nodes are separated
into isolated groups, it must choose between consistency and availability. In other words, during
a partition, a system can prioritize availability and partition tolerance, sacrificing consistency
(AP), or it can prioritize consistency and partition tolerance, sacrificing availability (CP).
It’s crucial to understand that the CAP theorem doesn’t imply an all-or-nothing sacrifice of
properties in every situation. Instead, it highlights the inherent trade-offs that distributed systems
face, requiring designers to make conscious decisions based on their specific system
requirements and priorities.
Different distributed systems may opt for different trade-offs based on factors such as the nature
of the application, user needs, and expected network conditions. For instance, in scenarios where
strict consistency is vital, such as financial transactions, a CP system may be preferred.


Conversely, in scenarios prioritizing high availability and responsiveness, such as web
applications, an AP system may be chosen:
Figure 3.1 – CAP theorem
The CAP theorem, as shown in Figure 3.1, establishes a foundation for comprehending the
challenges and design considerations in distributed systems. It assists system architects in
making informed decisions regarding consistency, availability, and partition tolerance based on
the unique requirements of their systems.
PACELC theorem
The PACELC theorem, an extension of the CAP theorem, considers the trade-offs in distributed
systems when confronted with network partitions. Let’s take a look at what PACELC stands for:
Partition tolerance (P): Partition tolerance refers to a distributed system’s ability to function and provide services even
when network partitions or communication failures occur. It means the system can tolerate the loss of network connectivity
between different nodes.
Availability (A): Availability ensures that every request made to the distributed system eventually receives a response,
regardless of the state of individual nodes or network partitions. The focus is on providing timely responses, even if it means
sacrificing strong consistency.
Consistency (C): Consistency entails all nodes in a distributed system agreeing on the current state of the system. Strong
consistency guarantees that every read operation sees the most recent write operation. However, achieving strong
consistency in a distributed system often leads to increased latency or reduced availability.
Else (E): The “E” in PACELC represents the “else” scenario, where there is no network partition. In this case, a trade-off
arises between latency and consistency.


Latency (L): Latency refers to the time delay between initiating a request and receiving a response. In some cases,
optimizing for low latency may require relaxing consistency guarantees or reducing availability.
Consistency Level (C): The consistency level indicates the desired or provided level of consistency in a distributed system.
It can vary based on application requirements or the design choices made by system architects.
The PACELC theorem offers a more nuanced perspective compared to the CAP theorem. It
states that in the presence of a network partition, we must choose between consistency and
availability (as in the CAP theorem). However, even without a network partition, a trade-off
emerges between latency and consistency. Different distributed systems may prioritize high
consistency at the expense of increased latency or opt for lower latency with eventual
consistency. Figure 3.2 captures how PACELC is different from the CAP theorem:
Figure 3.2 – PACELC theorem
Understanding the PACELC theorem helps system architects and designers make informed
decisions based on the specific requirements and priorities of their distributed systems while
considering both network partitions and the impact on latency and consistency.
In the realm of distributed systems, ensuring consensus among multiple nodes is a fundamental
challenge. In this section, we will discuss two seminal algorithms that help with distributed
consensus: Paxos and Raft.
Paxos
Paxos is a consensus algorithm that was introduced by Leslie Lamport in 1990, and with its
elegant design, Paxos has become a cornerstone of modern distributed systems, serving as the
foundation for numerous applications, including databases and distributed storage systems.


At its core, Paxos aims to enable a distributed system to agree on a single value, even in the
presence of failures and network delays. The “single value” in the context of the Paxos algorithm
refers to a specific piece of data or a decision that the nodes in a distributed system need to agree
upon. This consensus is crucial for ensuring that the system behaves consistently and reliably,
particularly in scenarios where multiple nodes might propose different values or updates. It
achieves this by employing a protocol that allows a group of nodes to reach a consensus on a
proposed value through a series of communication rounds.
Key components
To understand Paxos, we need to familiarize ourselves with its key components:
Proposers: These are the nodes that are responsible for initiating the consensus process. A proposer suggests a value to be
agreed upon and broadcasts this proposal to the other nodes in the system.
Acceptors: Acceptors are the nodes that receive proposals from proposers. They play a crucial role in the protocol by
accepting proposals and communicating their acceptance to other nodes.
Learners: Learners are the final recipients of the agreed-upon value. Once consensus is reached, learners acquire the value
and take appropriate actions based on it.
Now, let’s dive into the protocol itself.
Protocol steps
The Paxos protocol proceeds through a series of steps, as shown in Figure 3.3, which can be
summarized as follows:
Prepare phase: A proposer selects a unique proposal number and sends a prepare request to a majority of acceptors.
Acceptors respond with the highest-numbered proposal they have accepted.
Accept phase: If the proposer receives responses from a majority of acceptors, it proceeds to the accept phase. The proposer
sends an accept request, along with its proposal number and value, to the acceptors.
Consensus reached: If the majority of the acceptors accept the proposal, consensus is reached, and the value is chosen. The
learners are then informed of the chosen value:
Figure 3.3. shows how the Paxos algorithm operates in practice.


Figure 3.3 – The Paxos algorithm
While Paxos provides a robust mechanism for achieving consensus in distributed systems, it is
not without its challenges:
Fault tolerance: Paxos accounts for failures and network delays by tolerating the absence of some nodes and ensuring
progress despite potential disruptions.
Scalability: The performance of Paxos can be impacted by the number of nodes involved. As the system scales,
coordination and communication overhead may increase.
Complexity: Paxos is renowned for its elegance, but it can be challenging to understand and implement correctly. Careful
attention must be given to ensure all participants adhere to the protocol’s requirements.
Paxos variants and optimization techniques
Over the years, researchers and practitioners have introduced various variants and optimization
techniques to improve the efficiency and understandability of Paxos. Some notable
advancements are shown here:
Multi-Paxos: Multi-Paxos extends the basic Paxos protocol to allow for continuous consensus on multiple values without
repeating the prepare and accept phases. It reduces the overhead of repeated agreement rounds and enables faster agreement
on subsequent values.
Fast Paxos: Fast Paxos introduces an optimization to reduce the number of messages required for consensus. It allows a
proposer to bypass the traditional prepare phase by proposing a value directly to the acceptors, thereby reducing the latency
in reaching a consensus.
Simple Paxos: Simple Paxos aims to simplify the original Paxos protocol by combining the prepare and accept phases into a
single round. This reduces the number of message exchanges that are required and enhances the protocol’s
understandability.
Real-world use cases


Paxos finds applications in various distributed systems that require fault-tolerant consensus. Here
are some notable use cases:
Distributed databases: Paxos is commonly used in distributed databases to ensure consistency and durability across
replicas. It allows database nodes to agree on the order of committed transactions and handle failures gracefully.
Distributed filesystems: Filesystems such as Google’s GFS and Hadoop’s HDFS leverage Paxos to maintain the
consistency and availability of file metadata across multiple nodes. Paxos ensures that all replicas agree on the state of the
filesystem, even in the presence of failures.
Replicated state machines: Paxos serves as the foundation for implementing replicated state machines, where a cluster of
nodes agrees on a sequence of commands or operations to maintain consistency across replicas. This enables fault tolerance
and replication in systems such as distributed key-value stores and consensus-based algorithms.
Hence, we can say that Paxos provides a robust and widely adopted solution for achieving
consensus in distributed systems. Its elegance and versatility have made it a key building block
for numerous applications. By understanding this conceptual overview, as well as key
components, protocol steps, challenges, and real-world use cases of Paxos, software engineers
can effectively leverage this consensus algorithm to design and build reliable distributed
systems.
In the next section, we will explore Raft and its applications.
Raft
Raft, a consensus algorithm introduced by Diego Ongaro and John Ousterhout in 2013, provides
a simplified and intuitive approach to distributed consensus. With its emphasis on
understandability and ease of implementation, Raft has gained popularity as an alternative to
more complex consensus algorithms such as Paxos.
Raft aims to enable a distributed system to agree on a single, consistent state, even in the
presence of failures. It achieves this by dividing the consensus problem into three subproblems:
leader election, log replication, and safety. By tackling these subproblems, Raft simplifies the
coordination and communication required among nodes to reach consensus. Raft differs from
Paxos in that it has a designated “leader.”
Key components
To understand Raft, let’s explore its key components:


Leader: Raft operates under the assumption that the system has a designated leader. The leader is responsible for managing
the consensus process and coordinating the replication of log entries across other nodes.
Followers: Followers are passive nodes that replicate the leader’s log and respond to incoming requests. They rely on the
leader for guidance in the consensus process.
Candidate: When a leader fails or a new leader needs to be elected, nodes transition to the candidate state. Candidates
initiate leader election by requesting votes from other nodes in the system.
As you can see, most of the key components of Raft are similar to Paxos but Raft has a
designated leader. Now, let’s dive into the protocol’s steps.
Protocol steps
The Raft protocol proceeds through a series of steps, as shown in Figure 3.4, which can be
summarized as follows:
Leader election: When a system starts or detects the absence of a leader, a new leader needs to be elected. Nodes transition
to the candidate state and send out RequestVote messages to other nodes. A candidate becomes the leader if they receive
votes from a majority of nodes.
Log replication: The leader is responsible for receiving client requests, appending them to its log, and replicating the log
entries to followers. Followers apply received log entries to their state machines to maintain consistency across the system.
Safety and consistency: Raft ensures safety and consistency by enforcing specific rules, such as the “Append Entries” rule
and the “Voting” rule. These rules prevent inconsistencies and guarantee that only the most up-to-date log entries are
committed. See Figure 3.4.
Figure 3.4 – Raft protocol steps
Challenges and considerations
While Raft simplifies the consensus problem, there are some considerations to keep in mind:


Leader availability: The availability of a leader is crucial for the progress of the system. If the leader becomes unavailable,
a new leader must be elected promptly to avoid interruptions in the consensus process.
Scalability: As the system scales and the number of nodes increases, the communication and coordination overhead can
become a performance bottleneck. Proper optimization techniques and configuration adjustments are necessary to ensure
scalability.
Fault tolerance: Raft provides fault tolerance by allowing nodes to detect leader failures and initiate leader elections. The
algorithm ensures that the system can continue to make progress, even in the presence of failures.
Practical applications
The following are some practical applications of the Raft algorithm with examples of how it is
used in all major companies companies:
Distributed databases – Amazon DynamoDB: Distributed databases require a consensus algorithm such as Raft to
maintain consistency and durability across replicas. Raft ensures that all nodes agree on the order of committed transactions
and handle failures gracefully. Amazon DynamoDB, a highly scalable and managed NoSQL database service, employs
distributed consensus mechanisms such as Raft to ensure data consistency and availability across its distributed
infrastructure.
Distributed filesystems – Google File System (GFS): Distributed filesystems rely on consensus algorithms to maintain
consistency and availability of file metadata across multiple nodes. Raft is employed to ensure that all replicas agree on the
state of the filesystem, even in the presence of failures. GFS, which is used by Google for storing large-scale distributed
data, utilizes consensus algorithms such as Raft to achieve fault tolerance, data consistency, and replication across its
distributed filesystem.
Cluster coordination and service discovery – Apache ZooKeeper: Distributed systems often require coordination and
consensus among nodes for tasks such as leader election and service discovery. Raft is used in cluster coordination
frameworks such as Apache ZooKeeper to provide a reliable and consistent coordination service. ZooKeeper leverages Raft
to ensure consensus on critical system metadata, such as leader election, configuration changes, and distributed locks,
enabling fault-tolerant coordination among distributed services.
Consensus-based algorithms – Google Spanner: Consensus-based algorithms such as Paxos and Raft are fundamental in
building distributed systems that require strong consistency guarantees. Google Spanner, a globally distributed database,
utilizes Raft to ensure consistency and fault tolerance across its globally distributed replicas. Raft helps maintain consensus
on the order of operations and transaction commits, ensuring data integrity and consistency in Spanner’s distributed
architecture.
Cloud infrastructure management –Netflix’s Chaos Automation Platform (ChAP): Cloud infrastructure management
platforms, such as Netflix’s ChAP, require coordination and agreement among distributed components for tasks such as
resource allocation, fault tolerance, and auto-scaling. Raft can be employed to provide consensus and coordination among
the different components of the platform, ensuring that resource management decisions are made consistently across the
distributed infrastructure.
These are just a few examples of how the Raft algorithm is practically applied within top tech
companies. Raft’s simplicity, understandability, and fault-tolerant properties make it a preferred


choice for distributed consensus in various scenarios, from distributed databases and filesystems
to cluster coordination and infrastructure management.
The Raft algorithm provides a reliable consensus protocol when dealing with crash failures, but
it does not address more subtle failure scenarios, such as nodes that behave erroneously or
maliciously. This leads us to a more complex consensus problem known as BGP.
BGP
BGP is a classic thought experiment in the area of reliability and fault tolerance in distributed
systems. The problem illustrates the challenges of achieving reliable consensus when some
components are unreliable or behaving unexpectedly.
Imagine a group of generals of the Byzantine Empire of Rome, in around 300 CE, camped with
their troops around an enemy city. The generals can use only a messenger to communicate with
each other. To win the battle, all the generals must agree upon a common plan of action. Some of
the generals could be traitors who can confuse the loyal generals.
The loyal generals need a way to reliably agree upon a coordinated plan of action, even in the
presence of these traitorous generals spreading false information. This is a non-trivial problem
because of the following reasons:
The generals can only communicate through a messenger, which can fail or be intercepted.
Some fraction of the generals may be traitors who will deliberately try to confuse the loyal generals and prevent consensus.
The loyal generals do not know which generals are loyal and which are traitors. All generals seem identical from the outside.
The traitorous generals may collude together to prevent consensus among the loyal generals.
There are a few basic requirements for a solution to BGP:
If the majority of the generals are loyal, a solution must allow the loyal generals to eventually reach a consensus
The loyal generals must be able to tolerate up to f traitors, where f < (n-1)/2 and n is the total number of generals
The loyal generals must be able to make decisions in a reasonable amount of time
The key challenge is reliably achieving consensus in a distributed system where some arbitrary
number of components may be faulty or adversarial. This problem illustrates the complexities
involved and serves as an instructive starting point for the development of fault-tolerant
distributed systems and algorithms.
There are a few common solutions to BGP:


Voting algorithms: The generals vote on the proposed plan of action. If a threshold of votes is reached (for example, a 2/3
majority), then that plan is chosen. Traitorous generals can cast faulty votes, but so long as less than 1/3 of generals are
traitors, the loyal generals can still reach a consensus.
Multi-round signing: The generals propose a plan and sign it to vote for it. If a plan gets signatures from 2/3 of the
generals, it is chosen. Any general who does not sign a chosen plan is identified as a traitor. This is done over multiple
rounds to weed out traitors.
Quorum systems: The generals are divided into quorums, where each quorum must have a majority of loyal generals. Each
quorum votes on a plan independently. If a plan gets a majority vote in every quorum, it is chosen. The intersection of all
quorums ensures a plan has the majority support of loyal generals.
Timeouts and questioning: Generals propose a plan and vote for it. If a general does not vote within a timeout, it is marked
as a suspect. Generals can also question other generals about their votes and remove generals who give conflicting answers.
Randomization: Generals propose a plan with a random nonce (number used once). Traitorous generals cannot know the
correct nonce in advance. If a general’s vote has the correct nonce, it is likely loyal. Randomization makes it harder for
traitors to interfere successfully.
In general, solutions involve some form of voting, identifying faulty or traitorous generals, and
redundancy to tolerate a minority of failures while ensuring consensus among the majority of
loyal generals. The challenge lies in designing algorithms that are efficient, resilient, and able to
make forward progress even under adversarial conditions.
The Byzantine fault
The term Byzantine fault refers to the unpredictable and unreliable behavior exhibited by some
nodes in the system, comparable to the traitorous generals in BGP. Byzantine faults can include a
variety of issues, such as software bugs, hardware failures, or malicious attacks, which can result
in a node failing in arbitrary ways.
These faults are particularly challenging to manage as they can produce false or contradictory
information, making it difficult for the system to identify and isolate the problematic nodes.
Byzantine fault tolerance
To counter BGP, a system needs to implement Byzantine fault tolerance (BFT). This is a
property of a system that allows it to function correctly and reach consensus, even when some
nodes fail or act maliciously. In other words, a system is BFT if it can still provide its services
accurately to users, despite the Byzantine faults.


One of the earliest solutions for BFT was proposed by Lamport, Shostak, and Pease. They
proposed a voting system where each node sends its value (or “vote”) to every other node. Each
node then decides on the majority value. However, the protocol only works if less than a third of
the nodes are faulty. This solution requires every node to communicate with every other node,
resulting in high computational and communication overheads.
Modern BFT
Modern systems often implement variations of BFT algorithms, such as the Practical Byzantine
Fault Tolerance (PBFT) protocol or variants of it. PBFT reduces the communication overhead
and allows for more efficient consensus mechanisms in large networks. These solutions have
been instrumental in the operation of modern distributed systems, including blockchain
technologies such as Bitcoin and Ethereum.
BGP is a critical challenge in system design, highlighting the difficulty of achieving consensus in
a distributed system, especially when some nodes may behave unpredictably or maliciously. The
study of BFT and the creation of algorithms to achieve it is crucial to the design and
implementation of reliable, resilient distributed systems and networks.
As system designers, understanding BGP, its implications, and the methods to achieve BFT
equips us to build robust and reliable distributed systems. The world is increasingly reliant on
such systems – from digital currencies and distributed databases to large-scale computing
clusters – making BGP more relevant than ever.
FLP impossibility theorem
The FLP impossibility theorem, named after Fischer, Lynch, and Paterson, who proved it in
1985, states that it is impossible to design a totally asynchronous distributed system that can
reliably solve the consensus problem in the presence of even one failure.
The consensus problem requires that all processes in a distributed system eventually agree on a
single value, given some initial set of proposed values. For example, in BGP, the generals need
to reach a consensus on a plan of attack.
The key assumptions in the FLP impossibility proof are as follows:
Asynchrony: There are no bounds on message delays or process speeds. Processes communicate by sending messages but
have no shared clock.


Process failures: Up to f out of n processes may fail by crashing, where 0 < f < n.
Finite steps: Processes take a finite number of steps and messages have a finite size.
Under these conditions, the FLP theorem proves that there is no deterministic algorithm that can
ensure all correct processes reach consensus. This impossibility holds even if only one process
fails. The FLP impossibility states that it is impossible to simultaneously achieve all three of the
desirable properties in an asynchronous distributed system, such as fault tolerance, agreement,
and termination. We can design systems that can only achieve two of these properties, as
depicted in Figure 3.5:
Figure 3.5 – FLP impossibility triangle
The intuition behind the proof is that in an asynchronous system, processes have no way to
differentiate between a slow process and a crashed process. A live process may appear dead to
other processes due to long message delays, creating ambiguity that prevents consensus from
being reached reliably.
The implications of the FLP impossibility theorem are significant. It shows that purely
asynchronous distributed systems are fundamentally limited in what problems they can solve
reliably. Approaches to overcome the impossibility result typically involve one of the following:
Introducing synchronous assumptions, such as known bounds on message delays
Using probabilistic algorithms that can reach a consensus with a high probability
Adding randomness or a clock synchronization mechanism
Implementing a leader election or coordinator role
Overall, the FLP impossibility theorem helps explain why distributed consensus remains a
complex and challenging problem and highlights the trade-offs involved in designing distributed
algorithms and systems. It serves as a theoretical bound on what is computationally possible in
distributed systems under certain assumptions.


Hence, the FLP theorem proves that totally asynchronous distributed systems cannot
deterministically solve the consensus problem in the presence of even one process failure. This
fundamental impossibility has significant ramifications and suggests strategies for overcoming
the limitations.
Now that we’ve talked about various theorems, let’s shift gears to understand some of the
techniques and data structures that are widely used in designing distributed systems. A good
understanding of these concepts will help us build a foundation for future chapters.
Consistent hashing
Consistent hashing is a technique that’s used in distributed systems to efficiently distribute data
across multiple nodes while minimizing the need for data reorganization or rebalancing when
nodes are added or removed from the system. It provides a scalable and fault-tolerant approach
to handling data distribution.
In traditional hashing techniques, such as modulo hashing, the number of nodes or buckets where
data can be stored is fixed. When nodes are added or removed, the hash function that’s used to
map data keys to nodes changes, requiring a significant amount of data to be remapped and
redistributed across the nodes. This process can be time-consuming, resource-intensive, and
disruptive to the system’s availability.
The key problem that consistent hashing addresses is the scalability and fault tolerance of
distributed systems. It aims to minimize the impact of adding or removing nodes from the system
by ensuring that only a fraction of the data needs to be remapped when the number of nodes
changes. This property makes consistent hashing particularly useful in large-scale systems where
nodes are frequently added or removed, such as content delivery networks (CDNs) or
distributed databases.
In consistent hashing, a hash function is used to map data keys and node identifiers to a common
hash space. The hash space is typically represented as a ring, forming a circular continuum. Each
node in the distributed system is also assigned a position on the ring based on its identifier. To
store or retrieve data, the same hash function is applied to the data key, mapping it to a position
on the ring. Moving clockwise on the ring from the key’s position, the first node encountered is
responsible for storing or handling that particular data. This node is known as the “owner” or
“responsible node” for that data.


Let’s consider an example to understand this better. There are user API requests and we need to
assign these requests to servers. Let’s assume we have four servers (server0, server1, server2,
and server3) in this example. Figure 3.6 shows the hash ring where we will be mapping the
requests and the servers. We need to choose a hash function that takes the server IDs and
generates points on this hash ring. We will use the same hash function and pass the request IDs
to generate points to be mapped on this hash ring. Let’s call the hash function h().
Here, servers get mapped to points in the ring, like this:
h(server0) = s0
h(server1) = s1
h(server2) = s2
h(server3) = s3
The requests get mapped to points in the ring, like this:
h(req_id1) = r1
h(req_id2) = r2…. and so on.
Now, to determine which server takes on which request, we take the point (let’s say r1)
corresponding to the request (req_id1) and walk clockwise to find the first server point that’s
encountered, which in this case is s1 (corresponding to server1):
Figure 3.6 – Simple consistent hashing ring
This initial design still has a couple of issues:


The distribution of the requests to the servers may not be even. In Figure 3.6, it appears that all
four points corresponding to the four servers are placed equidistant. But that may not always be
true.
When one server goes down, the next server (walking in a clockwise direction) will have to bear
the load of the failed server as well. That may be too much for the server. As a result, this next
server may also go down due to excessive load, which can create a chain reaction that causes all
the servers to go down.
Let’s enhance the consistent hashing technique to fix these issues. Figure 3.7 shows an enhanced
version of the consistent hashing ring:
Figure 3.7 – Enhanced consistent hashing ring
In this enhanced approach, we use extra dummy points for the servers and place them in different
positions in the hash ring. In this example, let’s consider creating three extra dummy points for
each server. To do this, we must use three extra hash functions (h1(), h2(), and h3()) and use
them to create three extra points in the hash ring corresponding to each server.
So, for server0, we have the following:
h(server0) = s0
h1(server0) = s01
h2(server0) = s02


h3(server0) = s03
For server1, we have the following:
h(server1) = s1
h1(server1) = s11
h2(server1) = s12
h3(server1) = s13
Similarly, we generate points for server2 and server3.
As you can see, when using this enhanced consistent hashing technique, we have a better
distribution of nodes (the original point and the dummy points for the servers) so that the
requests are assigned to the server more evenly. Also, when a server goes down, the four
corresponding points will go down, but since the distribution of points corresponding to other
servers is well distributed, the requests will be almost evenly distributed among the surviving
servers, not just one. This helps prevent the cascading failure issue we mentioned earlier with the
simple consistent hashing ring.
So, in conclusion, by using a hash ring and mapping data keys and node identifiers to a common
hash space, consistent hashing provides a way to consistently assign data to nodes in a scalable
and fault-tolerant manner. When a node is added or removed, only a portion of the data needs to
be remapped to the neighboring nodes, limiting the amount of data movement required and
minimizing disruption to the system.
Bloom filters
A Bloom filter is a space-efficient probabilistic data structure that is used to test whether an
element is a member of a set. It provides a fast and memory-efficient way to perform
membership queries. The primary advantage of a Bloom filter is its ability to quickly determine
if an element is “possibly” in a set, with a small probability of false positives.
The Bloom filter is based on the concept of hash functions and bit arrays. It consists of a bit array
of a fixed size and a set of hash functions. Initially, all the bits in the array are set to 0. To add an
element to the filter, it is hashed by the set of hash functions, and the corresponding bits in the
array are set to 1. To check the membership of an element, it is hashed again using the same hash
functions, and the corresponding bits are examined. If any of the bits are 0, the element is not in


the set. However, if all the bits are 1, it is only probable that the element is in the set, as there is a
chance of false positives.
Let’s understand the Bloom filter by looking at an example. Let’s say we’re checking the
availability of usernames for a website. We need to give a unique username to a new user.
Here, we have the following aspects to consider:
The number of hash functions is k = 2
The bitcount (the size of the bit array) is m = 10
The two hash functions are h1() and h2(), both of which generate a number between 0 and 9.
Initialize the bit array via a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0].
Now, there are 3 usernames, john, dave, peter.
h1("john") = 5; h2("john") = 8,
h1("dave") = 3; h2("dave") = 5,
h1("peter") = 2; h2("peter") = 9
Mark bits for "john" in array [0, 0, 0, 0, 0, 1, 0, 0, 1, 0]
Mark bits for "dave" in array [0, 0, 0, 1, 0, 1, 0, 0, 1, 0]
Mark bits for "peter" in array [0, 0, 1, 1, 0, 1, 0, 0, 1, 1]
Now, let’s check whether a username is available or not.
Check "donald" in bloom filter:
h1("donald") = 3; h2("donald") = 7
On checking these two bit positions, we see that donald is for sure not in the existing set (and
hence its available)
Check "sarah" in bloom filter h1("sarah") = 3; h2("sarah") = 8
Checking these two bit positions, we see that sarah may not be available.
We can see from the above example that sarah was actually available, but bloom filter said that
it’s not available (a false positive), but donald was available and it did say that it’s indeed
available (no false negative).
Bloom filters have several use cases. Let’s take a look at a few:


Membership testing: Bloom filters can efficiently test if an element is a member of a set, such as a URL in a web crawler
or a word in a spell checker, without the need to store the entire set
Caching: Bloom filters can be used in caching systems to determine if a requested item is present in the cache, thereby
avoiding expensive cache lookups
Database optimization: Bloom filters can be utilized to filter out unnecessary disk reads by quickly identifying data that is
likely not present in a database, reducing I/O operations
Network routing: Bloom filters can assist in routing decisions by indicating potential destinations for a given packet or
message
Duplicate elimination: Bloom filters can help identify duplicates in large datasets, reducing storage requirements and
improving efficiency
It is important to note that while Bloom filters provide efficient and fast membership queries,
they have a probability of providing false positives. If a Bloom filter reports that an element is
present in a set, there is a chance it might not be. However, false negatives (indicating that an
element is not present when it is) are not possible.
To mitigate false positives, the size of the bit array and the number of hash functions used can be
adjusted. Increasing the size of the bit array reduces the probability of false positives, but it
increases memory requirements. Similarly, increasing the number of hash functions decreases
the probability of false positives, but it increases computational overhead.
Hence, a Bloom filter is a space-efficient data structure that provides a probabilistic way to test
membership in a set. It finds applications in scenarios where quick and memory-efficient
membership queries are required, with an acceptance for a small probability of false positives.
Count-min sketch
Count-min sketch is a probabilistic data structure that’s used to estimate the frequency of
elements in a data stream. It provides an approximate representation of the frequency distribution
of elements while using a small amount of memory. Count-min sketch is particularly useful in
scenarios where memory is limited or when processing large-scale data streams in real time.
Count-min sketch consists of a two-dimensional array of counters, with the number of rows and
columns determined by the desired accuracy and error rate. When an element is encountered in
the data stream, multiple hash functions are applied to determine the positions in the array to
increment the corresponding counters. By using multiple hash functions, collisions are
distributed, and the frequency of elements is estimated across different counters.


Let’s consider an example to understand this better. We have a stream of four alphabets (A, B, C,
and D) coming to our system and we need to be able to determine the count of these alphabets at
any given time.
For this, we will use five hash functions (depth, d=5) and an array length of (w)=10.
The values that correspond to each of the letters when they’re passed through the five hash
functions are shown in Figure 3.8(a):
Figure 3.8(a)
Initially, all the values for the two-dimensional array state are zeros. This is before any of the
letters have been streamed. The initial state is shown in Figure 3.8(b):
Figure 3.8(b)
Now, let’s assume the stream of letters comes as (A, A, B, D, B, A, A, D, B, B,…).
Here are the steps we must follow:
When the first letter is received, which is A the corresponding hash function values are {0, 2, 4,
8, 9}, as depicted in Figure 3.8(a). What we need to do is increment the cell corresponding to
the h1() row and 0th column by 1 . Similarly, we must increment the cell corresponding to (h2()
row, 2nd column), (h3() row, 4th column), (h4() row, 8th column) and (h5() row, 9th
column) by 1. The resultant two-dimensional array looks as follows:


Figure 3.8(c)
For the second alphabet, A, we do what we did previously – that is, increment the cells
corresponding to (h1() row and 0th column), (h2() row, 2nd column), (h3() row, 4th column),
(h4() row, 8th column) and (h5() row, 9th column) by 1. The resultant two-dimensional array
looks as follows:
Figure 3.8(d)
For the third alphabet, B, we do the same thing again but consider the hash values of B, which are
{1, 3, 4, 7, 2}. So, we must increment the cells corresponding to (h1() row and 1st column),
(h2() row, 3rd column), (h3() row, 4th column), (h4() row, 7th column) and (h5() row, 2nd
column) by 1. The resultant two-dimensional array looks as follows. Notice that the cell
corresponding to (h3() row, 4th column) has a collision – both A and B increment the cell value:
Figure 3.8(e)
Similarly, for the fourth alphabet, D, we must consider the hash values of D, which are {8, 3, 5,
7, 1}. Here, we must increment the cells corresponding to (h1() row and 8th column), (h2()


row, 3rd column), (h3() row, 5th column), (h4() row, 7th column) and (h5() row, 1st
column) by 1. The resultant two-dimensional array looks like this:
Figure 3.8(f)
Now, if we want to count how many times A appeared in the stream, we must figure out the
minimum of the cell values that correspond to the row and column for A. In Figure 3.8(f), the cell
values that correspond to (h1() row and 0th column), (h2() row, 2nd column), (h3() row, 4th
column), (h4() row, 8th column), and (h5() row, 9th column) are (2, 2, 3, 2, 2). The
minimum of these 5 values is 2. So, the count of A is 2.
Similarly, we can count how many times B appeared by finding the minimum of the cell values
that correspond to (h1() row and 1st column), (h2() row, 3rd column), (h3() row, 4th column),
(h4() row, 7th column), and (h5() row, 2nd column), which is (1, 2, 3, 2, 1) = 1. Hence the
count of B is 1.
The accuracy of count-min sketch depends on the number of counters and the number of hash
functions used. Increasing the number of counters improves accuracy but also increases memory
usage. Similarly, using more hash functions reduces collision probabilities and improves
accuracy, but it also introduces additional computational overhead.
Count-min sketch finds applications in various areas, including the following:
Frequency estimation: Count-min sketch can estimate the frequency of elements in a data stream, such as counting the
number of times a word appears in a text corpus or tracking the popularity of items in online shopping
Traffic analysis: It can be used in network traffic analysis to estimate the number of packets or flows associated with
specific protocols or network addresses


Web analytics: Count-min sketch can approximate the frequency of website visits, clicks, or user interactions, allowing
efficient analysis of web traffic
Distributed systems: Count-min sketch is valuable in distributed systems for collecting statistics and monitoring key
metrics, such as tracking the frequency of requests across different nodes
Data stream processing: It enables approximate counting and frequency estimation in real-time data streams, where the
entire dataset cannot be stored in memory
It’s important to note that count-min sketch provides an approximate representation of
frequencies and is susceptible to overestimation due to collisions. However, it offers a trade-off
between memory usage and accuracy, making it a valuable tool in scenarios where precise
frequency counts are not required, and memory constraints are a concern.
HyperLogLog
HyperLogLog is a probabilistic algorithm that’s used for estimating the cardinality (or the
number of distinct elements) of a set with very low memory usage. It was introduced by Philippe
Flajolet and is particularly useful when dealing with large datasets or when memory efficiency is
a concern. The HyperLogLog algorithm approximates the cardinality of a set by using a fixed
amount of memory, regardless of the size of the set. It achieves this by exploiting the properties
of hash functions and probabilistic counting.
The basic idea behind HyperLogLog is to hash each element of the set and determine the longest
run of zeros in the binary representation of the hash values. The length of the longest run of zeros
is used as an estimation of the cardinality. By averaging these estimations over multiple hash
functions, a more accurate cardinality estimate can be obtained.
Let’s understand this by considering an example. The problem statement is, “We need to find the
count of unique visitors for a website.”
What are some naive solutions here? We can maintain a hashmap with key as the unique user ID
and value to count how many times a particular user visited the website. This works fine for a
low-scale website, but as the website scales up in terms of the number of visitors, the memory
footprint grows linearly. So, for one billion visitors, we need 1 GB if we represent each visitor
just by 1 byte. Let’s explore how HyperLogLog comes to the rescue here.
We need to use randomness here. Let’s use a hash function to convert a username into a binary
number and assume it’s perfectly random. Also, the same username will yield the same hash


value. We’ll assume we have a perfect hash function that provides a complete random hash and
converts the value into a binary representation.
Let’s say we have 1 billion users. We need at least 30 bits to represent them:
u1(1,000,000,000) -> 111011100110101100101000000000
Now, let’s say we have the following:
hash("John_1275") = 111011100110101100101000001100
hash("David.raymond23") = 111011100110101100001000000010
hash("Sarah1978") = 100011100110101100101000000001
hash("John") -> 111011100110101100101000001100
Let’s reframe the problem: “We need to count the unique number of random binary numbers.”
Let’s understand how we can do this by using an analogy of flipping a coin – we need to flip the
coin until we get a T. Think about getting a sequence – H, H, H, T. The probability of getting
this is very hard, right?
That’s a ½ * ½ * ½ * ½ = 1/16 probability on average. So, that also means that to get H H H T,
we must flip the coin 16 times.
To extend this, if someone shows that the largest streak of leading heads (H) they got was L, this
means that, approximately, they flipped the coin 2^(L+1) times. In the preceding example, L=3,
so 2^(3+1) = 16.
Let’s get back to our binary numbers (hash of usernames):
hash("John_1275") = 111011100110101100101000001100
hash("David.raymond23") = 111011100110101100001000000010
hash("Sarah1978") = 100011100110101100101000000001
hash("John") = 111011100110101100101000001100
Instead of leading Hs, we will use ending 0s. In the preceding sample of four usernames, the
longest subsequence of 0s at the end is 2, so we likely have 2^(2+1) = 8 visitors.
In a small sample set, this isn’t correct, but at a large scale, does it become accurate? Even at a
high scale, we can see the accuracy problem because there could be outliers. If there is one bad
hash, it will screw up the estimate.
To increase the accuracy, we can follow these steps:
1. Split the incoming hash(usernames) randomly into k buckets.


2. Calculate the number of max ending 0s in each of these buckets.
3. Store "ending 0 counters" in these k buckets.
4. Calculate L= average of these k counters. Instead of taking the arithmetic mean, we can take the harmonic mean (this is why
it’s called HyperLogLog). The harmonic mean is better at ignoring outliers than the arithmetic mean.
5. The arithmetic mean of N numbers is (n1, n2, …) = (n1+n2+n3+....)/N.
6. The harmonic mean of N numbers is (n1, n2, …) = N/(1/n1+1/n2+1/n3…).
7. Estimate the final number of unique visitors via = 2^(L+1).
Calculating the exact cardinality of a multiset requires an amount of memory proportional to the
cardinality, which is impractical for very large datasets. HyperLogLog uses significantly less
memory than this, at the cost of obtaining only an approximation of the cardinality.
HyperLogLog provides a relatively small memory footprint compared to traditional methods for
exact counting, such as storing each element in a set.
We can use the following code to estimate the space of the HyperLogLog counter:
2^(L+1) = 1 billion visitors
L = log2(1000000000) = at max 30 ending 0's
log2(30) = 5 bits
5 bits can represent the number of ending 0s, so let’s say a byte. So, even if we use k =10
counters, it will be 10 bytes.
HyperLogLog has found applications in various domains where cardinality estimation is
important, such as database systems, network traffic analysis, web analytics, and big data
processing. It is widely used in distributed systems and data streaming scenarios where memory
is limited, and fast approximate cardinality estimation is required.
Summary
In this chapter, we embarked on a deep exploration of the essential theorems that serve as the
foundation for distributed systems. These theorems offer formal proofs and valuable insights into
different facets of distributed computing, including consensus protocols, distributed algorithms,
and fault tolerance. By studying these theorems, we gained a comprehensive understanding of
the limitations and possibilities that are inherent in distributed systems. Additionally, we talked


about some probabilistic data structures that are commonly employed in distributed systems,
further expanding our knowledge in this domain.
The first part of this chapter focused on examining classical theorems that are integral to
understanding distributed systems. We explored prominent theorems such as the CAP theorem,
which delves into the trade-offs between consistency, availability, and partition tolerance. The
PACELC theorem, another key theorem, provides insights into the behavior of systems when
network partition doesn’t happen, but there is a trade-off between consistency and latency.
Next, we covered some important topics, such as the Paxos and Raft algorithms, which are
consensus algorithms that are essential for fault-tolerant distributed systems. These algorithms
provide a means to achieve agreement among multiple nodes despite potential failures or
network partitions.
After that, we dove into the intricacies of BGP, which addresses the challenges that are posed by
malicious actors in distributed systems. Understanding this problem is crucial for designing
resilient and secure distributed systems. Additionally, we explored the FLP impossibility
theorem, which establishes the fundamental limitations of achieving consensus in an
asynchronous system with even a single faulty process. This theorem highlights the inherent
challenges of ensuring fault tolerance in distributed systems.
Finally, we delved into various techniques and data structures that are employed in distributed
systems. We discussed consistent hashing, a technique for distributing data across multiple nodes
in a scalable and load-balanced manner. Bloom filters, another data structure, allow for efficient
probabilistic set membership testing. Count-min sketch, on the other hand, offers an approximate
frequency counting mechanism, which is useful for tracking events in large-scale distributed
systems. Lastly, we explored HyperLogLog, a probabilistic algorithm that allows us to estimate
the cardinality in sets with minimal memory usage.
With a good understanding of these theorems, algorithms, and data structures, we can start
designing and implementing various system components in the next chapters.

## Examples & Scenarios

- of the application, user needs, and expected network conditions. For instance, in scenarios where
strict consistency is vital, such as financial transactions, a CP system may be preferred.

- Voting algorithms: The generals vote on the proposed plan of action. If a threshold of votes is reached (for example, a 2/3
majority), then that plan is chosen. Traitorous generals can cast faulty votes, but so long as less than 1/3 of generals are
traitors, the loyal generals can still reach a consensus.
Multi-round signing: The generals propose a plan and sign it to vote for it. If a plan gets signatures from 2/3 of the
generals, it is chosen. Any general who does not sign a chosen plan is identified as a traitor. This is done over multiple
rounds to weed out traitors.
Quorum systems: The generals are divided into quorums, where each quorum must have a majority of loyal generals. Each
quorum votes on a plan independently. If a plan gets a majority vote in every quorum, it is chosen. The intersection of all
quorums ensures a plan has the majority support of loyal generals.
Timeouts and questioning: Generals propose a plan and vote for it. If a general does not vote within a timeout, it is marked

- single value, given some initial set of proposed values. For example, in BGP, the generals need
to reach a consensus on a plan of attack.
The key assumptions in the FLP impossibility proof are as follows:
Asynchrony: There are no bounds on message delays or process speeds. Processes communicate by sending messages but
have no shared clock.

