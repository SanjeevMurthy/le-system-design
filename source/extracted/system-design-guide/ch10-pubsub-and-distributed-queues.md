# Chapter 7: Pub/Sub and Distributed Queues

> Source: System Design Guide for Software Professionals, Chapter 10, Pages 178-191

## Key Concepts

- 7
Pub/Sub and Distributed Queues
In today’s digital age, where data is generated at an unprecedented scale and speed, the need for
robust, scalable, and efficient systems for processing and distributi
- where each message is intended for a single consumer. The upcoming sections will delve deeper
into designing and implementing distributed queues and pub/sub systems.
Designing a distributed queue
Dist

## Content

7
Pub/Sub and Distributed Queues
In today’s digital age, where data is generated at an unprecedented scale and speed, the need for
robust, scalable, and efficient systems for processing and distributing this data is paramount. This
is where distributed systems come into play, particularly through the use of messaging patterns
such as Publish-Subscribe (Pub/Sub) systems and distributed queues.
As we have discussed in previous chapters, a distributed system is a network of independent
components designed to work together to achieve a common goal. These components
communicate and coordinate their actions by passing messages to one another. The two primary
messaging patterns used in distributed systems are as follows:
Pub/sub systems
Distributed queues
Both pub/sub systems and distributed queues are crucial in the architecture of modern distributed
systems, particularly in microservices architecture. They provide a means for services to
communicate in a loosely coupled manner, enhancing scalability and reliability.
We will be covering the following topics in this chapter:
The evolution of distributed systems
Designing a distributed queue
Designing a Pub/sub system
Kafka
Kinesis
The evolution of distributed systems
Distributed systems have evolved from monolithic architectures, where components are tightly
coupled and reside in a single service, to microservices architectures, where services are
decoupled and communicated via message passing. A distributed queue is a queue that is spread
across multiple servers. It allows for the storage and forwarding of messages. Queues are
typically used in scenarios where it’s crucial to process messages in the order they were sent or


where each message is intended for a single consumer. The upcoming sections will delve deeper
into designing and implementing distributed queues and pub/sub systems.
Designing a distributed queue
Distributed queues are a fundamental part of modern distributed systems. They provide a reliable
way to process and distribute messages across different parts of a system, ensuring that the load
is balanced and that the system can scale with demand. Let us now learn about the advantages of
leveraging distributed queues.
The advantages of using queues
Queues help with load management, allowing different parts of the system to independently scale
and operate and provide reliability:
Load management: Queues help in managing workloads by acting as a buffer between message producers and consumers.
This buffering allows for handling bursts of messages without overwhelming the system.
Decoupling system components: Queues enable different parts of a system to operate independently. Producers and
consumers do not need to be aware of each other’s states, leading to a more modular and maintainable architecture.
Reliability and consistency: By using queues, systems can ensure that messages are processed in a fail-safe manner. If a
consumer fails to process a message, the queue can redeliver it, ensuring data consistency.
Now that we have seen the benefits of using queues, let us look at some considerations when
designing a queue system.
Designing and implementing a distributed queue
Designing a distributed queue involves several key considerations around load management,
reliability, and providing delivery guarantees:
Scalability: Determining how the queue will handle increasing loads and message sizes
Fault tolerance: Ensuring that the queue remains operational even if some components fail
Message integrity: Guaranteeing that messages are delivered exactly once and in the correct order, whenever required
Let us now discuss the key features of a distributed queue.
Key features of a distributed queue
A distributed queue consists of several integral components that work together to manage the
flow of messages efficiently. Understanding their key features is essential for designing a robust


distributed queue system:
Queue manager: The queue manager is the core component that handles the distribution of messages within the queue. It is
responsible for maintaining the order of messages, ensuring their delivery to the appropriate consumers, and managing
retries in case of processing failures.
Message storage: This component is where the messages are stored until they are processed by a consumer. The storage
system needs to be highly reliable and capable of handling large volumes of data. It should also support fast read and write
operations to ensure efficient message handling.
Load balancing: Effective load balancing is crucial in a distributed queue to ensure that no single consumer is overwhelmed
with messages. This involves evenly distributing messages across multiple consumers based on their current load and
processing capacity.
Fault tolerance and recovery: A distributed queue must be resilient to failures. This involves using mechanisms for
detecting failed messages and processing attempts, as well as rerouting or retrying message delivery to ensure reliability.
Scalability: The ability to scale the queue system based on the load is essential. This means being able to handle an
increasing number of messages and consumers without degradation in performance.
Figure 7.1 shows how the components of the distributed queue system fit together.
Figure 7.1: Architecture of a distributed queue system
Now that we have a brief idea about the several components that make up a distributed queue
system, let us focus on some architectural considerations.
Architectural considerations


In the complex and evolving landscape of system design, the construction of a distributed queue
system requires careful consideration of several architectural elements. Each aspect plays a
critical role in ensuring the system’s efficiency, scalability, and reliability:
Message ordering: A fundamental consideration in the design process is message ordering and delivery guarantees.
Depending on the application’s needs, the queue may need to enforce strict message ordering or provide varying levels of
delivery guarantees, such as at-least-once or exactly-once delivery. This impacts how the system manages and prioritizes the
flow of data, ensuring accurate and reliable communication between different components.
Persistence: Equally important is the aspect of data persistence. The design must determine the extent to which messages
are stored in the system. Some applications necessitate the retention of messages until they are acknowledged by the
consumer, while others may allow for a level of message loss, balancing data integrity and system performance.
Security: Security and access control are also critical. Implementing robust security measures is essential to protect the
integrity of messages and maintain a secure environment. This involves not only safeguarding the data itself but also
controlling who has access to the queue, thus ensuring data privacy and compliance with regulatory standards.
Choice of technology stack: The next phase involves the selection of the appropriate technology stack. This decision is
influenced by factors such as language support, performance requirements, and compatibility with existing infrastructure.
Technologies such as RabbitMQ, Apache Kafka, and Amazon SQS are popular choices, each offering unique features and
capabilities suited to different types of applications.
Message format design: Designing the message format is another critical aspect. This includes determining the size of
messages and the methods for serialization and deserialization, as well as incorporating metadata for tracking and
debugging. The format chosen can significantly affect the performance and ease of use of the queue.
Fault tolerance: Ensuring fault tolerance is crucial for system reliability. Strategies for dealing with component failures,
such as retry mechanisms and dead letter queues for unprocessable messages, are necessary for maintaining continuous
operation and minimizing data loss.
In conclusion, designing a distributed queue is a multifaceted process that requires a careful
balance of technical and practical considerations. Each element, from message ordering to
security measures, plays a vital role in creating a robust and efficient system that meets the
demands of modern applications.
Now that we have discussed the basics of distributed queues, let us understand a Pub/Sub system
that is used extensively in the real world.
Designing a pub/sub system
The pub/sub model is a messaging pattern whereby messages are published by producers
(publishers) on a specific topic and consumers (subscribers) receive messages based on their
subscription to those topics. This model is highly effective for broadcasting information to
multiple consumers and is widely used in real-time data processing systems.


In a pub/sub system, topics are categories or channels to which messages are published by
producers to which consumers can subscribe to receive messages. Topics provide a logical
grouping of related messages, allowing for targeted distribution of information to interested
parties.
Let us look at some of the key characteristics of the pub/sub system.
Key characteristics of pub/sub systems
A good pub/sub system should allow independent scaling of producers and consumers while
providing scale and reliability guarantees. We will now touch upon these key characteristics.
Decoupling of producers and consumers: In a pub/sub model, publishers and subscribers are loosely coupled. Publishers
do not need to know about the subscribers, which allows for greater flexibility and scalability.
Scalability and efficiency: The pub/sub model can handle a large number of messages and distribute them to many
subscribers efficiently, making it suitable for large-scale distributed systems.
Flexibility in message processing: Subscribers can process messages in various ways, allowing for diverse applications
ranging from real-time data analytics to event-driven architectures.
Pub/sub systems need to inherently support scalability, reliability, and decoupled architecture. In
order to design an effective system, several critical architectural decisions must therefore be
made around managing topics, routing messages, managing subscribers, and defining the
Quality of Service (QoS) for the system:
Topic management: It’s crucial to define how topics are created, managed, and destroyed. This includes considering how to
handle dynamic topic creation and deletion. Topics need to be created to provide a destination for publishers to send
messages and for subscribers to receive messages from. This includes considering how to handle dynamic topic creation and
deletion based on the evolving needs of the system and its users.
Message routing: Developing a mechanism for routing messages from publishers to the appropriate subscribers is essential.
Subscriber management: Handling subscriber registration, maintaining the list of active subscribers, and managing their
subscriptions is necessary. Managing subscriptions involves allowing subscribers to specify which topics they want to
receive messages from and handling the process of subscribing and unsubscribing from topics based on their changing
interests or requirements.
QoS: Deciding on the levels of service, such as message delivery guarantees (at-most-once, at-least-once, exactly-once), and
handling message ordering is also vital.
Scalability and load balancing: Ensuring that the system can scale to accommodate a growing number of publishers and
subscribers, including strategies for load balancing, is also highly important.
Figure 7.2 shows a typical pub/sub system.


Figure 7.2: Architecture of a pub/sub system with publishers, subscribers, topics, and messages
In the preceding diagram, there are multiple publishers publishing messages on the same topic
and multiple consumers consuming these messages.
Let us now learn about some of the design considerations in building a pub/sub system.
Pub/sub system design considerations
The pub/sub model is particularly relevant in the context of microservices architecture. It enables
services to communicate asynchronously and react to events, leading to highly responsive and
flexible systems. We will explore this in more detail, providing insights into how pub/sub
systems can be effectively integrated into microservices.
When architecting a pub/sub system, two pivotal factors that warrant meticulous attention are
scalability and reliability. These elements are the cornerstones of ensuring that the system not
only accommodates high volumes of messages seamlessly but also maintains unwavering
performance regardless of varying operational loads.
Scalability is the system’s ability to gracefully handle increases in workload without
compromising performance. In a pub/sub context, this translates to effectively managing an
escalating number of messages and subscribers. Let us look at scalability aspects of pub/sub
systems:
Horizontal versus vertical scaling: This critical decision determines the scaling strategy. Horizontal scaling, which
involves adding more machines to the system, offers enhanced flexibility and robustness. It allows the system to expand in
capacity with the addition of resources, aligning with the fluctuating demands of message throughput. On the other hand,
vertical scaling, which entails bolstering existing machines with more resources, might offer a simpler short-term solution
but often lacks the long-term scalability and resilience of horizontal scaling. We have previously discussed horizontal and
vertical scaling in Chapter 2


Dynamic load balancing: In pub/sub systems, load balancing is typically handled by message brokers to distribute the load
across subscribers within a subscriber group. The aim is to decouple the concerns of production and consumption load
distribution from publishers and subscribers as much as possible, minimizing the need for message orchestration patterns.
By distributing the load across multiple brokers, the system can achieve increased scalability and stability. Brokers
dynamically adapt to changes in message volume and subscriber demand, ensuring that no single node becomes a bottleneck
and maintaining optimal performance.
Topic partitioning: This technique involves dividing topics into smaller, more manageable partitions. In a pub/sub system,
topics are logical channels or categories used to organize and distribute messages. Publishers send messages to specific
topics, while subscribers express interest in one or more topics and receive messages published to those topics. Topics
provide a way to decouple the production and consumption of messages, allowing multiple publishers to send messages to
the same topic and multiple subscribers to receive messages from the same topic independently. This decoupling enables
greater scalability and flexibility in the system, as publishers and subscribers can be added or removed without affecting
each other. Topics can be created dynamically based on the needs of the system and can have varying levels of granularity,
from broad categories to highly specific subjects, depending on application requirements. This division not only facilitates
load distribution across the system but also enhances throughput. By spreading the workload across multiple nodes, topic
partitioning plays a significant role in optimizing the performance of a pub/sub system.
Reliability in a pub/sub system is pivotal for ensuring consistent operation and trustworthiness,
particularly in handling message delivery and system resilience. Here are the design decisions to
consider for reliability of pub/sub systems:
Message delivery guarantees: Implementing varying levels of delivery guarantees is fundamental to ensuring message
integrity. Options such as at-most-once, at-least-once, or exactly-once delivery provide different assurances depending on
the criticality of the message content. These guarantees are instrumental in defining how the system handles potential data
loss or duplication, thus impacting the reliability that is perceived by end users.
Fault tolerance: A robust pub/sub system must be resilient to failures. Designing for fault tolerance involves strategies such
as replicating data across different nodes and implementing message re-delivery mechanisms. This ensures that the system
remains operational and efficient even in the face of component failures, thereby maintaining uninterrupted service.
Message ordering: For applications where the sequence of messages is crucial, ensuring correct message order is a key
aspect of reliability. This involves designing the system to maintain the chronological integrity of messages, which can be
especially challenging in distributed environments where messages may traverse various paths.
In essence, these high-level considerations of scalability and reliability form the backbone of a
well-designed pub/sub system. They are crucial in ensuring that the system not only meets the
current demands but is also well-prepared for future expansions and challenges. This focus helps
in creating a resilient, efficient, and future-proof messaging infrastructure.
Given that we have discussed the importance of scalability and reliability in pub/sub systems, let
us now delve into some aspects of their architecture.
Subscriber management and message routing


Managing subscribers and efficiently routing messages to them are vital components of a
pub/sub system. This involves the following:
Subscriber registration and management: Handling the process by which subscribers can register, deregister, and manage
their topic subscriptions
Efficient message routing: Developing algorithms to ensure that messages are routed to the right subscribers in the most
efficient way, minimizing latency and resource usage
QoS levels
Different applications require different levels of QoS. For instance, some systems might need
guaranteed delivery (at-least-once or exactly-once), while others might prioritize lower latency
over delivery guarantees.
Let us discuss some steps that you, as a system design architect, can take to architect pub/sub
systems in the real world.
Building a basic pub/sub system
The practical implementation of a pub/sub system involves several key steps, which cover
everything from initial setup to ensuring efficient and robust operation. Here, we will outline the
process of creating a basic pub/sub system:
1. Choosing the right tools and technologies:
Select a pub/sub platform (such as Apache Kafka, RabbitMQ, or Google Pub/Sub) that fits the requirements of
your system in terms of scalability, reliability, and feature set.
Decide on the programming languages and frameworks that will be used for developing publishers and
subscribers.
2. Setting up the pub/sub infrastructure:
Establish topics for publishers to send messages to.
Configure the pub/sub system, including setting up the necessary infrastructure for message storage, routing, and
processing.
3. Developing publishers and subscribers:
Write the code for publishers to send messages to topics.
Create subscribers that listen to topics and process incoming messages.
Implement error handling and retry mechanisms for reliable message processing.


4. Testing and optimization:
Conduct thorough testing to ensure that the system works as expected under different scenarios.
Optimize performance, including tweaking configurations for load balancing and message routing.
Now that we have extensively covered pub/sub system design, let us look at some real-world
systems in the next section
Kafka
Apache Kafka is a distributed streaming platform that has become synonymous with handling
high-throughput, real-time data feeds. Kafka is designed to be durable, fast, and scalable, making
it an ideal choice for implementing both pub/sub and queue-based messaging patterns. Before we
get into the details, let us recap some core concepts of Kafka:
Topics: In Kafka, records are published to a category called topics, to which many consumers subscribe.
Producers and consumers: In Kafka, producers publish the data. Consumers read that data. This data is published and read
from topics. Kafka’s power lies in allowing producers and consumers to scale independently in a decoupled manner.
Brokers: Kafka clusters consist of one or more servers known as brokers, which are responsible for maintaining published
data, managing subscribers, tracking consumption offsets, and fanning out data to consumers on demand.
Partitions and replication: Each topic can be split into partitions, which allows for data to be spread over multiple brokers
for fault tolerance and increased throughput.
In practice, as producers send messages to a topic, they assign these messages to different
partitions within the topic. Consumers then subscribe to these topics and read messages from the
partitions. Kafka takes care of maintaining the offset of messages for each consumer, ensuring
that each message is read once and in order. The use of replication across multiple brokers
protects against data loss and contributes to the overall reliability of the system.
Overall, Kafka’s architecture, characterized by its use of topics, partitions, and brokers, is adept
at balancing loads by evenly distributing messages and consumer requests. This not only ensures
scalability but also maintains a high level of performance, making Kafka an ideal platform for
handling real-time data feeds in distributed environments.
The following figure demonstrates the basic architecture of Kafka. As you can see in the figure,
messages are published to topics that contain partitions. Brokers are hubs that manage topics and
partitions. ZooKeeper is used to determine which broker is the leader for each partition and as a
service registry for all the brokers.


NOTE:
In recent versions of Kafka (starting from version 2.8), the dependency on ZooKeeper has been reduced. Kafka now
uses its own internal components, such as the Kafka Controller Broker and the Kafka Raft consensus protocol, to
manage cluster metadata and coordinate brokers. However, some older versions of Kafka may still rely on
ZooKeeper for these purposes.
Figure 7.3: Kafka architecture
Now that we have a better understanding of the Kafka architecture, let us focus on understanding
the importance of Kafka in distributed systems and what steps need to be followed to deploy it.
The importance of Kafka in distributed systems
Kafka is not just a messaging system but a full-fledged event streaming platform. It plays a
crucial role in modern distributed systems, particularly in scenarios that require handling large
volumes of data with minimal latency. Deploying Kafka in a distributed environment involves
several crucial steps, from initial setup to fine-tuning for optimal performance:
1. Setting up a Kafka cluster:
Cluster configuration: Configuring a Kafka cluster involves setting up multiple brokers to ensure fault
tolerance and high availability. This includes deciding on the number of brokers and their configuration for


optimal load distribution.
ZooKeeper integration: Kafka uses ZooKeeper for managing cluster metadata and coordinating brokers.
Setting up and configuring ZooKeeper is an essential step in deploying Kafka.
2. Creating and configuring topics:
Topic creation: Topics in Kafka are where messages are stored and published. Creating topics with the right
configurations, such as the number of partitions and the replication factor, is crucial for performance and
reliability.
Topic management: Understanding how to manage topics, including modifying configurations, deleting topics,
and monitoring topic performance, is crucial.
3. Developing Kafka producers and consumers:
Writing producers: Implementing producers that publish messages to Kafka topics, including handling
serialization of messages and managing connections to the Kafka cluster, is an essential step.
Creating consumers: It’s important to develop consumers that subscribe to topics and process messages, with a
focus on concurrency and offset management, as well as on ensuring message processing reliability.
4. Monitoring and maintenance:
Cluster monitoring: Monitoring is a crucial aspect for any distributed system deployment at scale, and
therefore, a successful deployment of Kafka should include tools and techniques for monitoring the cluster
health and performance metrics to identify potential issues.
Performance tuning: Ensure that you observe the best practices for tuning Kafka performance, such as
optimizing producer and consumer configurations, and tuning network and disk IO.
We have talked about the architecture of Apache Kafka. Now, let us look at Kafka Streams,
which provides a stream processing library on top of Kafka.
Kafka Streams
Kafka Streams is a powerful stream-processing library built on top of Apache Kafka. It allows
developers to build scalable, fault-tolerant, and real-time stream processing applications using a
high-level Domain-Specific Language (DSL) or a low-level Processor API. Kafka Streams
enables you to process and analyze data directly within Kafka, eliminating the need for separate
stream processing frameworks. The following are the key features of Kafka Streams:
Native Kafka integration: Kafka Streams is tightly integrated with Kafka, allowing seamless reading from and writing to
Kafka topics. It leverages Kafka’s features, such as partitioning and replication, for fault tolerance and scalability.


High-level DSL: Kafka Streams provides a high-level DSL that simplifies the development of stream processing
applications. The DSL includes operations such as map, filter, join, and aggregate, which can be combined to
express complex processing logic declaratively.
Low-level Processor API: For more advanced use cases, Kafka Streams offers a low-level Processor API that gives
developers fine-grained control over the processing topology. The Processor API allows for custom processing logic and
state management.
Stateful processing: Kafka Streams supports stateful processing, enabling you to build applications that maintain and
update state over time. It provides state stores, which are fault-tolerant and can be used to store and query application state.
Exactly-once processing: Kafka Streams guarantees exactly-once processing semantics, ensuring that each record is
processed exactly once, even in the presence of failures. This is achieved through the use of transaction support in Kafka.
Scalability and fault tolerance: Kafka Streams applications can be scaled horizontally by adding more instances, with
Kafka handling the distribution of partitions among the instances. It also provides fault tolerance through the use of Kafka’s
replication and failover mechanisms.
Stream processing topology
In Kafka Streams, a stream processing application is defined as a topology. A topology is a graph
of stream processors (nodes) and streams (edges). Each processor performs a specific operation
on the input data and produces an output stream. The topology defines how data flows through
the processors and how the processors are connected.
Kafka Streams provides a fluent API for building topologies using the high-level DSL. You can
define sources (input topics), processors (transformation operations), and sinks (output topics) to
create a complete stream processing pipeline.
Example use cases
Kafka Streams is suitable for a wide range of stream processing scenarios, such as the following:
Real-time data analytics: Analyzing streaming data in real-time to derive insights, detect anomalies, or generate metrics
Event-driven architectures: Building event-driven systems that react to and process events in real-time, enabling
communication and coordination between microservices
Data enrichment and transformation: Enriching streaming data with additional information from external sources or
transforming data into a desired format for downstream consumption
Fraud detection: Analyzing streaming transactions or user behavior in real time to identify and prevent fraudulent activities
Streaming ETL: Performing real-time Extract, Transform, and Load (ETL) operations on streaming data to enable
continuous data integration and processing
By leveraging Kafka Streams, you can build powerful and scalable stream processing
applications that seamlessly integrate with your Kafka-based architecture. Its combination of


high-level abstractions, low-level control, and native Kafka integration makes it a compelling
choice for real-time data processing needs.
In the next section, we will discuss another significant player in the world of real-time data
streaming and processing: Amazon Kinesis.
While Kafka offers a powerful solution for handling high-throughput data feeds, the dynamic
and ever-expanding field of distributed systems continually demands diverse approaches and
technologies. Kinesis represents another facet of this evolving landscape, providing a fully
managed, cloud-based service that addresses specific challenges and use cases in streaming data.
As we transition from Kafka to Kinesis, we’ll explore how Kinesis complements and differs
from Kafka, particularly in its approach to stream processing in cloud environments, and how it
fits into the broader picture of modern data-driven applications.
Kinesis
Kinesis is a cloud-based service from Amazon Web Services (AWS) that facilitates real-time
processing of large data streams. Kinesis is designed to handle massive amounts of data with
very low latencies, making it an ideal solution for real-time analytics, log and event data
processing, and large-scale application monitoring. Kinesis comprises several core components,
each serving distinct roles in the stream processing ecosystem:
Kinesis Data Streams form the backbone of the Kinesis service. They enable the capture and processing of large data
records in real time. Data producers, ranging from log generators to real-time event sources, continuously feed data into
these streams. The flexibility of Kinesis Data Streams lies in their ability to handle high-throughput ingestion from multiple
sources simultaneously, making them ideal for scenarios requiring immediate data processing and analysis.
Kinesis Data Firehose complements Kinesis Data Streams by facilitating the direct loading of streaming data into other
AWS services and external data stores. This service captures the data from streams, optionally transforms it, and then
automatically loads it into repositories such as Amazon S3, Amazon Redshift, Amazon Elasticsearch, or even Splunk. The
seamless integration of Kinesis Data Firehose with these data stores simplifies the architecture for real-time analytics
applications, allowing for efficient data storage, querying, and visualization.
Lastly, Kinesis Data Analytics offers a powerful solution for analyzing streaming data using standard SQL queries. This
component allows users to write SQL queries to process data directly within the stream, enabling real-time analytics and
decision-making. Kinesis Data Analytics is particularly powerful when combined with Kinesis Data Streams, as it allows for
the immediate analysis of incoming data without the need for batch processing or data offloading.
Together, these components create a comprehensive ecosystem for real-time data processing in
the cloud. From data ingestion and storage to processing and analysis, Kinesis offers scalable and


efficient solutions, making it a go-to choice for applications that require real-time insights from
streaming data.
Summary
In this chapter, we embarked on a detailed journey through the realms of pub/sub and distributed
queue systems, which are integral to the architecture of modern distributed systems. We delved
into the intricacies of designing and implementing distributed queues, focusing on their
scalability, reliability, and message integrity. The chapter also explored pub/sub systems,
emphasizing their role in decoupling components and enhancing system flexibility. We covered
practical aspects, including integration with microservices. Finally, we examined Apache Kafka
and Amazon Kinesis, shedding light on their core concepts and operational dynamics. This
chapter has armed you with a comprehensive understanding of these crucial components,
preparing you to design and implement efficient, scalable distributed systems.
In the next chapter, we will cover some cornerstones of a well-architected distributed system
such as API design, security, and metrics.

## Examples & Scenarios

- Different applications require different levels of QoS. For instance, some systems might need
guaranteed delivery (at-least-once or exactly-once), while others might prioritize lower latency
over delivery guarantees.
Let us discuss some steps that you, as a system design architect, can take to architect pub/sub
systems in the real world.
Building a basic pub/sub system
The practical implementation of a pub/sub system involves several key steps, which cover
everything from initial setup to ensuring efficient and robust operation. Here, we will outline the
process of creating a basic pub/sub system:
1. Choosing the right tools and technologies:

