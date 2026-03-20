# Chapter 8: Design and Implementation of System Components: API, Security, and Metrics

> Source: System Design Guide for Software Professionals, Chapter 12, Pages 193-211

## Key Concepts

- 8
Design and Implementation of System Components:
API, Security, and Metrics
In the realm of software engineering, the design and implementation of system components play
a pivotal role in determining

## Content

8
Design and Implementation of System Components:
API, Security, and Metrics
In the realm of software engineering, the design and implementation of system components play
a pivotal role in determining the efficiency, reliability, and scalability of a system. This chapter
delves into the intricacies of key system components, namely APIs (with a focus on REST and
gRPC), API security, logging, metrics, alerting, and tracing in a distributed system. The
objective is to provide a comprehensive understanding of these components, their design
principles, and their contribution to the overall performance of a system.
Application Programming Interfaces (APIs) serve as the communication bridge between
different software components. They have become increasingly important in today’s world of
microservices and distributed systems. This chapter will provide an in-depth exploration of
REST and gRPC APIs, two popular approaches to building APIs, each with its unique strengths
and suitable use cases.
API security is another critical aspect that will be covered in this chapter. As APIs are often
targeted by attackers, understanding and implementing robust API security measures is crucial.
We will delve into the basics of API security, including authentication, authorization, secure
communication, and rate limiting.
Logging and metrics are essential tools for monitoring and debugging in a distributed system.
They provide insights into the system’s behavior and performance, helping engineers identify
and resolve issues. This chapter will guide you through the design and implementation of
distributed logging and the relevance of metrics.
Alerting is a proactive way to manage system incidents. It notifies engineers about potential
issues before they escalate into major problems. This chapter will discuss the importance of
alerting, how to set up effective alerts, and how to respond to them.
Finally, we will explore tracing, a technique used to track a request as it travels through various
services in a distributed system. Tracing helps in diagnosing performance issues and
understanding the system’s behavior.


Here is a list of topics covered in this chapter:
REST APIs
gRPC APIs
Comparing REST and gRPC
API security
Distributed logging
Metrics in a distributed system
Alerting in a distributed system
Tracing in a distributed system
By the end of this chapter, you will have gained practical skills in designing and implementing
these system components, which are essential for building robust, scalable, and efficient systems.
Let’s embark on this journey by exploring REST and gRPC APIs.
REST APIs
Representational State Transfer (REST) is an architectural style for designing networked
applications. It has gained popularity due to its simplicity and the use of standard HTTP
methods, which are understood by most developers. Let us learn about the design principles, use
cases, and strengths and weaknesses of REST APIs.
Design principles of REST APIs
REST APIs are built around resources, which are any kind of object, data, or service that can be
accessed by the client. A resource is identified by a Uniform Resource Identifier (URI), and
the API interacts with these resources using HTTP methods such as GET, POST, PUT, DELETE, and
others. These methods correspond to create, read, update, and delete (CRUD) operations in
database systems.
A key feature of REST is its statelessness. Each request from a client to a server must contain all
the information needed to understand and process the request. This makes the server’s operations
more predictable and reliable as it doesn’t need to retain any context between requests. Let us
now look at the use cases of REST APIs.


Use cases for REST APIs
REST APIs are particularly suitable for public APIs exposed over the internet. Their use of
HTTP protocol makes them easily consumable by any client that can send HTTP requests. This
includes web browsers, mobile applications, and other servers.
REST APIs are also a good fit for CRUD-based operations where the system is primarily dealing
with entities that need to be created, read, updated, or deleted. For example, a web application
that manages a list of users or products can benefit from a RESTful API design. Let us look at
the strengths and weaknesses of REST APIs.
Strengths and weaknesses
REST APIs are simple to understand and use. They leverage HTTP’s built-in methods and status
codes, making them intuitive for developers familiar with HTTP. However, REST APIs can be
less efficient for complex operations that require multiple requests to complete. They also use
JSON for data exchange, which can be verbose and lead to larger payloads.
In the next section, we will explore gRPC APIs, a different approach to building APIs that can
address some of the limitations of REST. By understanding both REST and gRPC, you will be
better equipped to choose the right approach for your specific use case.
gRPC APIs
Google Remote Procedure Call (gRPC) is a high-performance, open-source framework for
executing remote procedure calls. It was developed by Google and is based on the HTTP/2
protocol. Unlike REST, which is data-centric, gRPC is function-centric, making it a powerful
tool for creating highly efficient APIs. We will now discuss the design principles, use cases, and
strengths and weaknesses of gRPC APIs.
Design principles of gRPC APIs
gRPC uses Protocol Buffers (protobuf) as its interface definition language. Protobuf is a
language-neutral, platform-neutral, extensible mechanism for serializing structured data. It’s
more efficient and faster than JSON, which is commonly used in REST APIs.


gRPC allows you to define services in a .proto file, and then automatically generates client and
server stubs in a variety of languages. This makes it easier to create and maintain APIs, as
changes to the service definition are automatically propagated to the client and server code.
One of the main advantages of gRPC is its support for multiple programming languages, making
it a good choice for polyglot environments. It also supports features including authentication,
load balancing, and bidirectional streaming. Let us now look at some of the use cases.
Use cases for gRPC APIs
gRPC is particularly suitable for microservices architectures where services need to
communicate with each other frequently and efficiently. Its support for bidirectional streaming
and its small message size due to Protocol Buffers make it a good choice for real-time
applications.
gRPC is also a good fit for systems that require high-performance inter-service communication,
as it reduces the overhead of communication between services. Let us talk about the strengths
and weaknesses of gRPC APIs.
Strengths and weaknesses
gRPC APIs are highly efficient and versatile, supporting a wide range of use cases. They offer
significant performance benefits over REST APIs, especially in terms of payload size and speed.
gRPC has strictly typed data definition contracts guaranteed by protobufs. However, gRPC APIs
can be more complex to set up and debug due to their binary format and the need for HTTP/2
support. Changes to gRPC communication can require data definition changes to be made and
deployed as code changes, thus increasing the change release time. On the other hand, changing
messages and testing these changes is quicker when using REST v/s gRPC.
We will now compare REST and gRPC, discussing when to use each based on specific
requirements. This comparison will provide a deeper understanding of these two approaches,
enabling you to make an informed decision for your system design.
Comparing REST and gRPC


REST and gRPC are two powerful approaches to building APIs, each with its unique strengths
and suitable use cases. Understanding the differences between them can help you make an
informed decision based on your specific requirements. We will compare them across several
dimensions including performance, ease of use, compatibility, and streaming support. Figure 8.1
shows typical request and response structures for both REST and gRPC. REST endpoints are
easier to test and are generally preferred for public APIs, whereas gRPC APIs are preferred for
inter-service communications and have a binary format.
Figure 8.1: REST and gRPC APIs
While both gRPC and REST APIs excel at building efficient communication protocols for
services, a key difference lies in their browser compatibility. gRPC, designed for machine-tomachine communication, is not directly supported by web browsers due to limitations in browser
APIs. This makes REST APIs the preferred choice for browser-based applications where data
needs to be exchanged between the client-side (web browser) and the server. However, for
service-to-service communication where efficiency and performance are paramount, gRPC
remains a powerful option. We will now discuss the differences between the two APIs based on
factors such as performance, ease of use, compatibility, streaming support, and use cases:


Performance: gRPC generally has better performance than REST due to its use of HTTP/2 and Protocol Buffers. HTTP/2
can send multiple requests in parallel over a single TCP connection, reducing the latency inherent in HTTP/1.1. Protocol
Buffers are a more efficient data format than JSON, leading to smaller payloads.
Ease of use: REST APIs are simpler to use and understand, especially for developers already familiar with HTTP methods
and status codes. They can easily be tested and debugged using standard tools such as cURL or Postman. On the other hand,
gRPC APIs require specific tools for testing and debugging due to their binary format.
Compatibility: REST APIs have broader compatibility as they use HTTP, which is universally supported by all internetconnected devices. gRPC, however, requires HTTP/2 support, which might not be available on all platforms or network
infrastructures.
Streaming support: gRPC supports bidirectional streaming, allowing both the client and server to send data independently
of each other. REST, however, only supports request-response communication.
Use cases: REST is a good choice for public APIs exposed over the internet, especially for CRUD-based operations. It’s
also suitable when you need broad compatibility across different platforms and network environments.
gRPC is a better choice for high-performance inter-service communication, especially in a
microservices architecture. It’s also suitable for real-time applications due to its support for
bidirectional streaming.
In conclusion, the choice between REST and gRPC should be based on your specific use case,
considering factors such as performance requirements, ease of use, compatibility, and the type of
communication needed.
In the next section, we will delve into API security, a critical aspect of any API design.
API security
API security is a critical aspect of any system design, especially in today’s world where data
breaches are common. As APIs serve as the communication bridge between different software
components, they are often targeted by attackers. Therefore, understanding and implementing
robust API security measures is crucial. We will discuss authentication and authorization as it
pertains to API security in the next sections. Figure 8.2 shows the difference between
authentication and authorization. Authentication is concerned with answering the question, “Who
are you?”, which is akin to logging into a website with your username and password, whereas
authorization deals with checking users’ permissions to access data, thus answering the question,
“Are you allowed to do that?” Let us now delve into explaining both authentication and
authorization.


Figure 8.2: Authentication vs. Authorization
Authentication
Authentication is the process of verifying the identity of a user, system, or application. It’s the
first line of defense in API security. There are several methods to implement authentication in
APIs, each with its strengths and weaknesses.
API keys: API keys are a simple method where the client sends a key in the header of the HTTP request. However, they are
not the most secure method as they can be easily intercepted and don’t provide fine-grained access control.
OAuth: OAuth is a more secure method that allows users to grant limited access to their resources from one site to another
site, without having to expose their credentials. OAuth 2.0, the latest version, is widely used in the industry and supports
different “flows” for web applications, desktop applications, mobile applications, and smart devices.
JSON Web Tokens (JWT): JWT is a streamlined method for securely exchanging information between two entities. It
encapsulates claims in a JSON format, which are then encapsulated within a JSON Web Signature (JWS) structure. This
design allows for the digital signing or integrity protection of the claims using a Message Authentication Code (MAC),
and optionally, encryption. The compact and URL-safe nature of JWTs makes them an ideal choice for transmitting data
across different systems or networks.
We have thus seen the different ways in which authentication is implemented. Authentication
helps to answer the question “Who are you?”, i.e., it validates that the system is being accessed
by the right person. Now, let us understand authorization, which checks for the access
permissions of a given user.
Authorization


Once a user is authenticated, the next step is to ensure they have the correct permissions to
access the resources they are requesting. This is known as authorization. Let us review some
ways in which authorization is typically implemented in large-scale systems:
Role-Based Access Control (RBAC): RBAC is a popular method for implementing authorization, where permissions are
associated with roles, and users are assigned roles. This simplifies managing permissions as you only need to manage roles,
not individual user permissions.
Attribute-Based Access Control (ABAC): ABAC, on the other hand, defines permissions based on attributes. These
attributes can be associated with a user, a resource, an environment, or a combination of these. ABAC provides more finegrained control than RBAC but can be more complex to implement.
These are two basic ways that authorization has been implemented in many large-scale systems.
To understand API security, we also need to understand that APIs typically require secure
communications and rate limiting, which we define below.
Secure communication of APIs
When building APIs, it’s crucial to prioritize security to safeguard data in transit. Using
Hypertext Transfer Protocol Secure (HTTPS) is a fundamental practice in achieving this.
HTTPS ensures that the communication between the client and the server is encrypted, making it
difficult for potential eavesdroppers or attackers to intercept and decipher the transmitted data.
This is especially important when dealing with sensitive information such as passwords, personal
details, or financial transactions. Additionally, maintaining up-to-date Transport Layer
Security (TLS) configurations is vital. As new vulnerabilities are discovered and security
standards evolve, keeping your TLS settings current helps protect against emerging threats and
ensures compliance with industry best practices for encryption and data integrity.
Rate limiting
Rate limiting is an essential mechanism for API management and security. By restricting the
number of requests a client can make within a specified timeframe, rate limiting helps prevent
abuse and overuse of your API. This is particularly important for defending against Denial of
Service (DoS) attacks, where an attacker attempts to overwhelm your server by flooding it with
an excessive number of requests, leading to service degradation or downtime. Implementing rate
limiting also aids in managing server resources and ensuring fair usage among clients. By setting
reasonable limits, you can help ensure that no single user or application monopolizes your API,


allowing for a more equitable distribution of resources and a better overall experience for all
users.
There are several popular rate-limiting algorithms you can choose from, each with its own
advantages and disadvantages. Here are a few common ones:
Token bucket algorithm: This algorithm visualizes rate limits as a bucket with a fixed number of tokens. Each request
consumes a token, and new tokens are added to the bucket at a set rate. Requests are rejected if there are no available tokens.
Leaky bucket algorithm: Similar to the token bucket, the leaky bucket algorithm has a bucket but with a hole at the bottom.
Tokens are added at a set rate, but they also leak out at a constant rate. Requests are rejected if the bucket is full.
Sliding window algorithm: This algorithm tracks the number of requests made within a specific time window. If the
request count exceeds the limit during that window, subsequent requests are throttled.
The best algorithm for your specific needs depends on factors such as desired granularity,
burstiness tolerance, and implementation complexity.
We have discussed the basics of API security in this section. In the following section, we will
transition into the importance of logging and metrics in a distributed system.
Distributed systems logging
In a distributed system, where multiple services are running on different machines, logging
becomes a critical aspect of system monitoring and debugging.
Logging is the process of recording events in a system. It provides a way to understand what’s
happening inside your application, helping you identify patterns, detect anomalies, and
troubleshoot issues. In a distributed system, logs from different services can provide a holistic
view of the system’s behavior, making it easier to identify and resolve issues. Most large-scale
systems use some form of centralized logging infrastructure, where logs are collected from
different systems into a central logging repository. We will now delve into centralized logging.
Centralized logging
In a distributed system, logs are generated by different services running on different machines.
These logs need to be collected and stored in a central location for easy access and analysis. This
is known as centralized logging.
Benefits of centralized logging


The following are some of the benefits of centralized logging:
Ease of access: All logs are available in one place, making it easier to search and analyze them
Correlation: Logs from different services can be correlated based on timestamps or unique identifiers, providing a complete
picture of a transaction or operation
Long-term storage: Logs can be archived for long-term storage and compliance purposes
Figure 8.3 shows an example of the most commonly used centralized logging architecture,
which leverages Logstash for log collection, parsing, and transformation; Elasticsearch for
storing, indexing; and searching logs; and Kibana for visualizations and analysis. This is just one
of the different ways in which you can build your logging infrastructure.
Figure 8.3: An example of a centralized logging architecture
When designing your logging strategy, consider what information to include in your logs. At a
minimum, each log entry should contain the following:
Timestamp: The date and time the event occurred
Service name: The name of the service that generated the log
Severity level: The severity of the event (e.g., INFO, WARNING, ERROR)
Message: A descriptive message explaining the event
Context: Additional context about the event, such as user ID, transaction ID, and so on
Building upon the importance of logging and the basics of centralized logging, let’s delve into
the tools and best practices for implementing distributed logging.
Open source tools for centralized logging


There are various open-source tools available for centralized logging, each offering unique
features and capabilities:
Logstash: A component of the Elastic Stack, Logstash is designed to efficiently process data from various sources,
transform it, and then route it to a storage destination like Elasticsearch.
Fluentd: Fluentd is a versatile open-source data collector that allows for the aggregation and management of data from
multiple sources, facilitating easier analysis and utilization of the information.
Graylog: Graylog is a prominent solution for centralized log management that adheres to open standards. It is engineered to
collect, store, and enable real-time analysis of vast amounts of machine-generated data.
Let us now talk about some of the best practices for implementing logging.
Best practices for implementing distributed logging
Implementing distributed logging can be challenging, but the following best practices can guide
you through the process:
Use a consistent log format: A consistent log format makes it easier to search and analyze logs. This is especially important
in a distributed system where logs are generated by different services.
Include context in your logs: Contextual information such as user ID, transaction ID, and other relevant data can help you
understand the scope and impact of an event.
Handle exceptions properly: Make sure to log exceptions along with their stack traces. This will help you identify the root
cause of errors.
Use appropriate log levels: Using appropriate log levels helps filter logs and reduces noise. For example, use the ERROR
level for events that require immediate attention, and the INFO level for events that are useful but not critical.
Rotate and archive logs: To manage storage and ensure compliance, implement a strategy for rotating and archiving logs.
This involves deleting old logs and storing important logs for long-term analysis.
In the next section, we will transition into the importance of metrics in a distributed system.
Metrics in a distributed system
Metrics are a numerical representation of data measured over intervals of time. They provide a
quantifiable way to assess the performance and health of your system. In a distributed system,
it’s important to collect metrics from all your services and aggregate them in a central location.
Metrics provide insights into the behavior and performance of your system, helping you make
informed decisions about scaling, performance optimization, and troubleshooting. They can help
you answer questions such as the following:


How is the system performing?
Is the system meeting its service level objectives?
Are there any performance bottlenecks?
Is the system behaving as expected?
We will now talk about the types of metrics in a distributed system, some open-source tools
typically used by enterprises, and some best practices for system design architects to implement
metrics at scale.
Types of metrics
There are several types of metrics you can collect, each providing different insights into your
system:
System metrics: These include CPU usage, memory usage, disk I/O, and network I/O. They provide insights into the
resource usage of your system.
Application metrics: These include request rate, error rate, and response times. They provide insights into the performance
and reliability of your application.
Business metrics: These are specific to your application’s domain, such as the number of user sign-ups, and number of
orders placed. They provide insights into the business impact of your system.
Building upon the importance and types of metrics, let’s delve into the tools and best practices
for implementing metrics in a distributed system.
Open source tools for metrics
Several open-source tools are available for the collection, storage, and visualization of metrics,
each offering unique features and strengths:
Prometheus: Prometheus is a popular open-source system for monitoring and alerting. It features a multi-dimensional data
model, a powerful query language called PromQL, and seamless integration with a variety of graphing and dashboarding
tools. Prometheus is particularly well suited for monitoring dynamic cloud environments and microservices architectures.
Graphite: Graphite is a well-established monitoring tool that specializes in storing and graphing numeric time-series data.
Its web interface, Graphite-web, allows users to create and display custom graphs based on the stored data. Graphite is
known for its simplicity and scalability, making it a good choice for large-scale deployments.
Datadog: Although not open source, Datadog is a widely-used SaaS-based monitoring service for cloud-scale applications.
It offers comprehensive monitoring capabilities for servers, databases, tools, and services, along with advanced data
analytics features. Datadog’s platform is designed to provide real-time insights and alerts, helping teams quickly identify
and resolve issues.


Let us now discuss some of the best practices for implementing metrics.
Best practices for implementing metrics
Implementing metrics in a distributed system can be challenging, but the following best practices
can guide you through the process:
Identify key metrics: Not all metrics are equally important. Identify key metrics that directly impact your service level
objectives and focus on them.
Use a consistent naming scheme: A consistent naming scheme makes it easier to search and analyze metrics. This is
especially important in a distributed system where metrics are generated by different services.
Monitor error rates and latencies: These are often the first indicators of a problem. Set up alerts to notify you when these
metrics cross a certain threshold.
Visualize your metrics: Use dashboards to visualize your metrics. This can help you spot trends and anomalies that might
not be apparent in raw data.
In the next section, we will transition into the importance of alerting in a distributed system.
Alerting in a distributed system
Alerting is a crucial aspect of maintaining the health of a distributed system. It serves as a
proactive measure to identify potential issues before they escalate into significant problems,
ensuring system reliability and performance.
Alerting is an essential part of any monitoring strategy. It provides real-time notifications about
system anomalies, errors, or performance issues. Without an effective alerting mechanism, teams
may remain unaware of critical issues until they have caused significant damage or downtime.
Alerts can be triggered based on various conditions, such as exceeding a certain threshold of
error rate, response time, or resource usage. They can also be triggered based on specific events,
such as a service failure or a system-wide outage.
It is important as a system design architect to design effective and actionable alerts, without
overwhelming support. We will therefore discuss this topic, some open-source tools for alerting,
and some best practices for designing alerts in the next few sections.
Designing effective alerts


Designing effective alerts involves striking a balance between sensitivity and specificity. Alerts
should be sensitive enough to catch real issues but specific enough to avoid false alarms, which
can lead to alert fatigue.
Here are some key considerations when designing alerts:
Severity: Not all alerts are created equal. Classify alerts based on their severity to help prioritize responses. Critical alerts
might require immediate attention, while warnings could be addressed during regular working hours.
Actionability: An effective alert is one that requires action. If an alert doesn’t require any action, it might not be necessary.
Context: Alerts should provide enough context to help diagnose the issue. Include relevant information such as the service
affected, the time the issue occurred, and any associated error messages or logs.
Building upon the importance and design principles of alerting, let’s delve into the tools and best
practices for implementing alerting in a distributed system.
Open-source tools for alerting
Several open-source tools are available for configuring alerts, each offering unique features and
advantages:
Prometheus with Alertmanager: Prometheus is a widely-used open-source monitoring and alerting toolkit. It includes a
component called Alertmanager, which is responsible for processing alerts generated by Prometheus or other client
applications. Alertmanager handles tasks such as deduplication, grouping, and routing of alerts to the appropriate receiver,
ensuring that alerts are managed efficiently and effectively.
Grafana: Grafana is a versatile open-source analytics and visualization platform. It supports a wide range of data sources
and provides powerful visualization tools, including charts and graphs. Grafana also includes an alerting feature that allows
users to set up alerts based on specific conditions in their data. These alerts can be configured to send notifications through
various channels, such as email, Slack, or webhook, enabling timely responses to potential issues.
PagerDuty: Although not open source, PagerDuty is a popular incident response platform used by IT departments and
operations teams. It integrates seamlessly with a variety of monitoring tools, including both Prometheus and Grafana, to
provide centralized alerting and incident management. PagerDuty can alert users through multiple channels, including phone
calls, SMS, emails, and push notifications, ensuring that critical issues are addressed promptly.
Let us now discuss some of the best practices for implementing alerting.
Best practices for implementing alerting
Implementing alerting in a distributed system can be challenging, but the following best practices
can guide you through the process:
Avoid alert fatigue: Alert fatigue occurs when too many alerts are triggered, causing teams to ignore them. To avoid this,


ensure that your alerts are actionable and adjust their thresholds to avoid false positives.
Test your alerts: Regularly test your alerts to ensure they are working as expected. This can be done during chaos
engineering experiments or as part of your regular testing process.
Document your alerting process: Document how to respond to each type of alert. This can include troubleshooting steps,
who to escalate to, and any relevant runbooks.
In the next section, we will transition into the importance of tracing in a distributed system.
Tracing in a distributed system
Tracing is a technique used to track a request as it travels through various services in a
distributed system. It provides a detailed view of how a request is processed, making it an
invaluable tool for diagnosing performance issues and understanding the system’s behavior.
In a distributed system, a single request can involve multiple services. Understanding how this
request is processed can be challenging, especially when things go wrong. This is where tracing
comes in.
Tracing provides a detailed view of a request’s journey through the system. It shows the
interaction between services, the latency of each service, and any errors that occurred during the
processing of the request. This information can help diagnose performance issues, identify
bottlenecks, and understand the overall flow of requests in the system.
In the next few sections, we will discuss the importance of tracing, some open-source tools that
can be used by system design practitioners for effective tracing, and some best practices to
follow when designing distributed tracing.
Distributed tracing
Distributed tracing extends the concept of tracing to a distributed system. It involves tracking a
request as it travels across multiple services and machines. Each step in the request’s journey is
recorded as a span. A collection of spans forms a trace, which represents the entire journey of the
request.
Distributed tracing provides several benefits:
Performance optimization: By visualizing the flow of requests, you can identify performance bottlenecks and optimize
them
Error diagnosis: If a request fails, you can use the trace to identify where the error occurred and what caused it


System understanding: Tracing helps you understand the flow of requests in your system, which can be useful when
onboarding new team members or when planning system changes
Open-source tools for distributed tracing
Several open-source tools are available for implementing distributed tracing, each offering
distinct features and capabilities:
Jaeger: Jaeger is a distributed tracing system that was developed by Uber Technologies and subsequently released as opensource software. It is designed to monitor and troubleshoot microservices-based distributed systems, drawing inspiration
from Google’s Dapper and OpenZipkin. Jaeger provides a comprehensive set of features, including distributed context
propagation, transaction monitoring, root cause analysis, and performance optimization. It supports various storage
backends, including Elasticsearch, Cassandra, and Kafka, for scalable trace storage.
Zipkin: Zipkin is another distributed tracing system that focuses on collecting and managing timing data for troubleshooting
latency issues in microservice architectures. It provides a simple and intuitive interface for visualizing trace data, enabling
developers to quickly identify and address performance bottlenecks. Zipkin supports multiple data storage options, such as
in-memory, MySQL, Cassandra, and Elasticsearch, and can be integrated with various programming languages and
frameworks.
OpenTelemetry: OpenTelemetry is a unified observability framework that provides APIs, libraries, agents, and collector
services for capturing distributed traces and metrics from applications. It aims to standardize the collection and analysis of
telemetry data across different platforms and tools. OpenTelemetry supports a wide range of programming languages and
integrates seamlessly with popular observability tools such as Prometheus and Jaeger. It offers advanced features such as
context propagation, distributed tracing, and metric collection, making it a versatile choice for modern cloud-native
applications.
Figure 8.4 shows an example of how Newrelic’s tracing dashboard allows us to look at the API
calls in a distributed system. It shows the entire trace duration, as well as sections of it, such as
the backend duration, root span duration, and more. Within Backend duration, it shows
different process entry and exit points, which is useful in debugging performance issues with
different processes:


Figure 8.4: Newrelic tracing dashboard example
Best practices for implementing tracing
Implementing tracing in a distributed system can be challenging, but the following best practices
can guide you through the process:
Instrument your code: To collect traces, you need to instrument your code with the tracing library. This usually involves
creating spans around operations you want to track.
Propagate context: For a trace to span across multiple services, you need to propagate the trace context from one service to
another. This is usually done by injecting the trace context into the headers of the HTTP request.
Use appropriate span names: Span names should be descriptive and consistent so you can easily understand what
operation they represent.
Annotate your spans: Annotating spans with additional metadata can provide more context about the operation, making it
easier to understand and troubleshoot issues.
Best practices


Throughout this chapter, we have explored key components of system design, including REST
and gRPC APIs, API security, logging, metrics, alerting, and tracing in a distributed system.
Each of these components plays a crucial role in building robust, scalable, and efficient systems.
As we conclude, let’s summarize some best practices that can guide you in leveraging these
components effectively:
Choose the right API design: REST and gRPC each have their strengths and suitable use cases. Choose the one that best
fits your system’s requirements in terms of performance, ease of use, and compatibility.
Prioritize API security: Implement robust authentication and authorization mechanisms, ensure secure communication, and
use rate limiting to protect your APIs.
Implement centralized logging: Collect logs from all your services and store them in a central location. This will make it
easier to search and analyze logs, providing valuable insights into your system’s behavior.
Monitor key metrics: Identify key system, application, and business metrics, and monitor them regularly. This will help
you understand your system’s performance and make informed decisions.
Set up effective alerts: Design alerts that are sensitive, specific, and provide enough context to diagnose issues. Regularly
test your alerts to ensure they are working as expected.
Use distributed tracing: Implement distributed tracing to track a request as it travels through various services. This will
help you diagnose performance issues, understand the flow of requests, and optimize your system’s performance.
Remember, the goal is not just to design a system that works, but to design a system that works
well under a variety of conditions and can scale as your needs grow. By understanding and
effectively leveraging these components, you will be well-equipped to design and build robust,
scalable, and efficient systems.
Summary
In this chapter, we delved into the critical components of system design, covering APIs, security,
logging, metrics, alerting, and tracing in distributed systems. We explored the nuances of REST
and gRPC APIs, highlighting their distinct advantages and ideal use cases. The chapter
emphasized the paramount importance of API security, outlining strategies for authentication,
authorization, secure communication, and rate limiting.
We also examined the pivotal roles of logging and metrics in monitoring and debugging
distributed systems, introducing centralized logging and the significance of key metrics. Alerting
was discussed as a proactive measure for managing system incidents and ensuring timely
response to potential issues. Furthermore, we explored tracing as a technique for tracking
requests across services, providing invaluable insights into system performance and behavior.


By the end of this chapter, readers should gain a good understanding of the skills needed in
designing and implementing these essential system components. These skills are crucial for
building robust, scalable, and efficient systems, enabling readers to effectively monitor,
troubleshoot, and optimize their systems in real-world scenarios. The lessons learned in this
chapter lay the foundation for the subsequent chapters, where we will continue to build upon
these concepts and explore advanced topics in system design.
In the next chapter, we will leverage all the basic components of system design that we have
learned in the previous chapters to design real-world systems.

## Examples & Scenarios

- with entities that need to be created, read, updated, or deleted. For example, a web application
that manages a list of users or products can benefit from a RESTful API design. Let us look at
the strengths and weaknesses of REST APIs.
Strengths and weaknesses
REST APIs are simple to understand and use. They leverage HTTP’s built-in methods and status
codes, making them intuitive for developers familiar with HTTP. However, REST APIs can be
less efficient for complex operations that require multiple requests to complete. They also use
JSON for data exchange, which can be verbose and lead to larger payloads.
In the next section, we will explore gRPC APIs, a different approach to building APIs that can
address some of the limitations of REST. By understanding both REST and gRPC, you will be

- Severity level: The severity of the event (e.g., INFO, WARNING, ERROR)
Message: A descriptive message explaining the event
Context: Additional context about the event, such as user ID, transaction ID, and so on
Building upon the importance of logging and the basics of centralized logging, let’s delve into
the tools and best practices for implementing distributed logging.
Open source tools for centralized logging

- Use appropriate log levels: Using appropriate log levels helps filter logs and reduces noise. For example, use the ERROR
level for events that require immediate attention, and the INFO level for events that are useful but not critical.
Rotate and archive logs: To manage storage and ensure compliance, implement a strategy for rotating and archiving logs.
This involves deleting old logs and storing important logs for long-term analysis.
In the next section, we will transition into the importance of metrics in a distributed system.
Metrics in a distributed system
Metrics are a numerical representation of data measured over intervals of time. They provide a
quantifiable way to assess the performance and health of your system. In a distributed system,
it’s important to collect metrics from all your services and aggregate them in a central location.
Metrics provide insights into the behavior and performance of your system, helping you make

