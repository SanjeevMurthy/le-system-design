# Serviceability or Manageability

> Source: System Design - Grokking (Notes), Chapter 241, Pages 67-67

## Key Concepts

- vs.
Vertical scaling vs. Horizontal scaling
Reliability
By definition, reliability is the probability a system will fail in a given period. In simple terms, a
distributed system is considered reliable

## Content

vs.
Vertical scaling vs. Horizontal scaling
Reliability
By definition, reliability is the probability a system will fail in a given period. In simple terms, a
distributed system is considered reliable if it keeps delivering its services even when one or several of
its software or hardware components fail. Reliability represents one of the main characteristics of any
distributed system, since in such systems any failing machine can always be replaced by another
healthy one, ensuring the completion of the requested task.
Take the example of a large electronic commerce store (like Amazon), where one of the primary
requirement is that any user transaction should never be canceled due to a failure of the machine that
is running that transaction. For instance, if a user has added an item to their shopping cart, the system
is expected not to lose it. A reliable distributed system achieves this through redundancy of both the
software components and data. If the server carrying the user’s shopping cart fails, another server that
has the exact replica of the shopping cart should replace it.
Obviously, redundancy has a cost and a reliable system has to pay that to achieve such resilience for
services by eliminating every single point of failure.
Availability
By definition, availability is the time a system remains operational to perform its required function in a
specific period. It is a simple measure of the percentage of time that a system, service, or a machine
remains operational under normal conditions. An aircraft that can be flown for many hours a month
without much downtime can be said to have a high availability. Availability takes into account
maintainability, repair time, spares availability, and other logistics considerations. If an aircraft is
down for maintenance, it is considered not available during that time.
Reliability is availability over time considering the full range of possible real-world conditions that can
occur. An aircraft that can make it through any possible weather safely is more reliable than one that
has vulnerabilities to possible conditions.
Reliability Vs. Availability
If a system is reliable, it is available. However, if it is available, it is not necessarily reliable. In other
words, high reliability contributes to high availability, but it is possible to achieve a high availability
even with an unreliable product by minimizing repair time and ensuring that spares are always
available when they are needed. Let’s take the example of an online retail store that has 99.99%
availability for the first two years after its launch. However, the system was launched without any
y
y
,
y
y
information security testing. The customers are happy with the system, but they don’t realize that it
isn’t very reliable as it is vulnerable to likely risks. In the third year, the system experiences a series of
information security incidents that suddenly result in extremely low availability for extended periods
of time. This results in reputational and financial damage to the customers.
Efficiency
To understand how to measure the efficiency of a distributed system, let’s assume we have an
operation that runs in a distributed manner and delivers a set of items as result. Two standard
measures of its efficiency are the response time (or latency) that denotes the delay to obtain the first
item and the throughput (or bandwidth) which denotes the number of items delivered in a given time
unit (e.g., a second). The two measures correspond to the following unit costs:
Number of messages globally sent by the nodes of the system regardless of the message size.
Size of messages representing the volume of data exchanges.
The complexity of operations supported by distributed data structures (e.g., searching for a specific key
in a distributed index) can be characterized as a function of one of these cost units. Generally speaking,
the analysis of a distributed structure in terms of ‘number of messages’ is over-simplistic. It ignores the
impact of many aspects, including the network topology, the network load, and its variation, the
possible heterogeneity of the software and hardware components involved in data processing and
routing, etc. However, it is quite difficult to develop a precise cost model that would accurately take
into account all these performance factors; therefore, we have to live with rough but robust estimates
of the system behavior.
Serviceability or Manageability
Another important consideration while designing a distributed system is how easy it is to operate and
maintain. Serviceability or manageability is the simplicity and speed with which a system can be
repaired or maintained; if the time to fix a failed system increases, then availability will decrease.
Things to consider for manageability are the ease of diagnosing and understanding problems when
they occur, ease of making updates or modifications, and how simple the system is to operate (i.e., does
it routinely operate without failure or exceptions?).
Early detection of faults can decrease or avoid system downtime. For example, some enterprise
systems can automatically call a service center (without human intervention) when the system
experiences a system fault.
←    Back
System Design Ba…
Next    →
Load Balancing
Completed

## Examples & Scenarios

- is running that transaction. For instance, if a user has added an item to their shopping cart, the system
is expected not to lose it. A reliable distributed system achieves this through redundancy of both the
software components and data. If the server carrying the user’s shopping cart fails, another server that
has the exact replica of the shopping cart should replace it.
Obviously, redundancy has a cost and a reliable system has to pay that to achieve such resilience for
services by eliminating every single point of failure.
Availability
By definition, availability is the time a system remains operational to perform its required function in a
specific period. It is a simple measure of the percentage of time that a system, service, or a machine
remains operational under normal conditions. An aircraft that can be flown for many hours a month

- unit (e.g., a second). The two measures correspond to the following unit costs:
Number of messages globally sent by the nodes of the system regardless of the message size.
Size of messages representing the volume of data exchanges.
The complexity of operations supported by distributed data structures (e.g., searching for a specific key
in a distributed index) can be characterized as a function of one of these cost units. Generally speaking,
the analysis of a distributed structure in terms of ‘number of messages’ is over-simplistic. It ignores the
impact of many aspects, including the network topology, the network load, and its variation, the
possible heterogeneity of the software and hardware components involved in data processing and
routing, etc. However, it is quite difficult to develop a precise cost model that would accurately take
into account all these performance factors; therefore, we have to live with rough but robust estimates

- Early detection of faults can decrease or avoid system downtime. For example, some enterprise
systems can automatically call a service center (without human intervention) when the system
experiences a system fault.
←    Back
System Design Ba…
Next    →
Load Balancing
Completed

