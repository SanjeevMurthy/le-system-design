# Part I. Foundations of Data Systems

> Source: Designing Data-Intensive Applications (Martin Kleppmann), Chapter 1, Pages 23-166

## Key Concepts

- PART I
Foundations of Data Systems
The first four chapters go through the fundamental ideas that apply to all data sys‐
tems, whether running on a single machine or distributed across a cluster of
mac
- CHAPTER 1
Reliable, Scalable, and
Maintainable Applications
The Internet was done so well that most people think of it as a natural resource like the
Pacific Ocean, rather than something that was man-

## Content

PART I
Foundations of Data Systems
The first four chapters go through the fundamental ideas that apply to all data sys‐
tems, whether running on a single machine or distributed across a cluster of
machines:
1. Chapter 1 introduces the terminology and approach that we’re going to use
throughout this book. It examines what we actually mean by words like reliabil‐
ity, scalability, and maintainability, and how we can try to achieve these goals.
2. Chapter 2 compares several different data models and query languages—the
most visible distinguishing factor between databases from a developer’s point of
view. We will see how different models are appropriate to different situations.
3. Chapter 3 turns to the internals of storage engines and looks at how databases lay
out data on disk. Different storage engines are optimized for different workloads,
and choosing the right one can have a huge effect on performance.
4. Chapter 4 compares various formats for data encoding (serialization) and espe‐
cially examines how they fare in an environment where application requirements
change and schemas need to adapt over time.
Later, Part II will turn to the particular issues of distributed data systems.




CHAPTER 1
Reliable, Scalable, and
Maintainable Applications
The Internet was done so well that most people think of it as a natural resource like the
Pacific Ocean, rather than something that was man-made. When was the last time a tech‐
nology with a scale like that was so error-free?
—Alan Kay, in interview with Dr Dobb’s Journal (2012)
Many applications today are data-intensive, as opposed to compute-intensive. Raw
CPU power is rarely a limiting factor for these applications—bigger problems are
usually the amount of data, the complexity of data, and the speed at which it is
changing.
A data-intensive application is typically built from standard building blocks that pro‐
vide commonly needed functionality. For example, many applications need to:
• Store data so that they, or another application, can find it again later (databases)
• Remember the result of an expensive operation, to speed up reads (caches)
• Allow users to search data by keyword or filter it in various ways (search indexes)
• Send a message to another process, to be handled asynchronously (stream pro‐
cessing)
• Periodically crunch a large amount of accumulated data (batch processing)
If that sounds painfully obvious, that’s just because these data systems are such a suc‐
cessful abstraction: we use them all the time without thinking too much. When build‐
ing an application, most engineers wouldn’t dream of writing a new data storage
engine from scratch, because databases are a perfectly good tool for the job.
3


But reality is not that simple. There are many database systems with different charac‐
teristics, because different applications have different requirements. There are vari‐
ous approaches to caching, several ways of building search indexes, and so on. When
building an application, we still need to figure out which tools and which approaches
are the most appropriate for the task at hand. And it can be hard to combine tools
when you need to do something that a single tool cannot do alone.
This book is a journey through both the principles and the practicalities of data sys‐
tems, and how you can use them to build data-intensive applications. We will explore
what different tools have in common, what distinguishes them, and how they achieve
their characteristics.
In this chapter, we will start by exploring the fundamentals of what we are trying to
achieve: reliable, scalable, and maintainable data systems. We’ll clarify what those
things mean, outline some ways of thinking about them, and go over the basics that
we will need for later chapters. In the following chapters we will continue layer by
layer, looking at different design decisions that need to be considered when working
on a data-intensive application.
Thinking About Data Systems
We typically think of databases, queues, caches, etc. as being very different categories
of tools. Although a database and a message queue have some superficial similarity—
both store data for some time—they have very different access patterns, which means
different performance characteristics, and thus very different implementations.
So why should we lump them all together under an umbrella term like data systems?
Many new tools for data storage and processing have emerged in recent years. They
are optimized for a variety of different use cases, and they no longer neatly fit into
traditional categories [1]. For example, there are datastores that are also used as mes‐
sage queues (Redis), and there are message queues with database-like durability guar‐
antees (Apache Kafka). The boundaries between the categories are becoming blurred.
Secondly, increasingly many applications now have such demanding or wide-ranging
requirements that a single tool can no longer meet all of its data processing and stor‐
age needs. Instead, the work is broken down into tasks that can be performed effi‐
ciently on a single tool, and those different tools are stitched together using
application code.
For example, if you have an application-managed caching layer (using Memcached
or similar), or a full-text search server (such as Elasticsearch or Solr) separate from
your main database, it is normally the application code’s responsibility to keep those
caches and indexes in sync with the main database. Figure 1-1 gives a glimpse of what
this may look like (we will go into detail in later chapters).
4 
| 
Chapter 1: Reliable, Scalable, and Maintainable Applications


Figure 1-1. One possible architecture for a data system that combines several
components.
When you combine several tools in order to provide a service, the service’s interface
or application programming interface (API) usually hides those implementation
details from clients. Now you have essentially created a new, special-purpose data
system from smaller, general-purpose components. Your composite data system may
provide certain guarantees: e.g., that the cache will be correctly invalidated or upda‐
ted on writes so that outside clients see consistent results. You are now not only an
application developer, but also a data system designer.
If you are designing a data system or service, a lot of tricky questions arise. How do
you ensure that the data remains correct and complete, even when things go wrong
internally? How do you provide consistently good performance to clients, even when
parts of your system are degraded? How do you scale to handle an increase in load?
What does a good API for the service look like?
There are many factors that may influence the design of a data system, including the
skills and experience of the people involved, legacy system dependencies, the time‐
scale for delivery, your organization’s tolerance of different kinds of risk, regulatory
constraints, etc. Those factors depend very much on the situation.
Thinking About Data Systems 
| 
5


In this book, we focus on three concerns that are important in most software systems:
Reliability
The system should continue to work correctly (performing the correct function at
the desired level of performance) even in the face of adversity (hardware or soft‐
ware faults, and even human error). See “Reliability” on page 6.
Scalability
As the system grows (in data volume, traffic volume, or complexity), there should
be reasonable ways of dealing with that growth. See “Scalability” on page 10.
Maintainability
Over time, many different people will work on the system (engineering and oper‐
ations, both maintaining current behavior and adapting the system to new use
cases), and they should all be able to work on it productively. See “Maintainabil‐
ity” on page 18.
These words are often cast around without a clear understanding of what they mean.
In the interest of thoughtful engineering, we will spend the rest of this chapter
exploring ways of thinking about reliability, scalability, and maintainability. Then, in
the following chapters, we will look at various techniques, architectures, and algo‐
rithms that are used in order to achieve those goals.
Reliability
Everybody has an intuitive idea of what it means for something to be reliable or unre‐
liable. For software, typical expectations include:
• The application performs the function that the user expected.
• It can tolerate the user making mistakes or using the software in unexpected
ways.
• Its performance is good enough for the required use case, under the expected
load and data volume.
• The system prevents any unauthorized access and abuse.
If all those things together mean “working correctly,” then we can understand relia‐
bility as meaning, roughly, “continuing to work correctly, even when things go
wrong.”
The things that can go wrong are called faults, and systems that anticipate faults and
can cope with them are called fault-tolerant or resilient. The former term is slightly
misleading: it suggests that we could make a system tolerant of every possible kind of
fault, which in reality is not feasible. If the entire planet Earth (and all servers on it)
were swallowed by a black hole, tolerance of that fault would require web hosting in
6 
| 
Chapter 1: Reliable, Scalable, and Maintainable Applications


space—good luck getting that budget item approved. So it only makes sense to talk
about tolerating certain types of faults.
Note that a fault is not the same as a failure [2]. A fault is usually defined as one com‐
ponent of the system deviating from its spec, whereas a failure is when the system as a
whole stops providing the required service to the user. It is impossible to reduce the
probability of a fault to zero; therefore it is usually best to design fault-tolerance
mechanisms that prevent faults from causing failures. In this book we cover several
techniques for building reliable systems from unreliable parts.
Counterintuitively, in such fault-tolerant systems, it can make sense to increase the
rate of faults by triggering them deliberately—for example, by randomly killing indi‐
vidual processes without warning. Many critical bugs are actually due to poor error
handling [3]; by deliberately inducing faults, you ensure that the fault-tolerance
machinery is continually exercised and tested, which can increase your confidence
that faults will be handled correctly when they occur naturally. The Netflix Chaos
Monkey [4] is an example of this approach.
Although we generally prefer tolerating faults over preventing faults, there are cases
where prevention is better than cure (e.g., because no cure exists). This is the case
with security matters, for example: if an attacker has compromised a system and
gained access to sensitive data, that event cannot be undone. However, this book
mostly deals with the kinds of faults that can be cured, as described in the following
sections.
Hardware Faults
When we think of causes of system failure, hardware faults quickly come to mind.
Hard disks crash, RAM becomes faulty, the power grid has a blackout, someone
unplugs the wrong network cable. Anyone who has worked with large datacenters
can tell you that these things happen all the time when you have a lot of machines.
Hard disks are reported as having a mean time to failure (MTTF) of about 10 to 50
years [5, 6]. Thus, on a storage cluster with 10,000 disks, we should expect on average
one disk to die per day.
Our first response is usually to add redundancy to the individual hardware compo‐
nents in order to reduce the failure rate of the system. Disks may be set up in a RAID
configuration, servers may have dual power supplies and hot-swappable CPUs, and
datacenters may have batteries and diesel generators for backup power. When one
component dies, the redundant component can take its place while the broken com‐
ponent is replaced. This approach cannot completely prevent hardware problems
from causing failures, but it is well understood and can often keep a machine running
uninterrupted for years.
Reliability 
| 
7


i. Defined in “Approaches for Coping with Load” on page 17.
Until recently, redundancy of hardware components was sufficient for most applica‐
tions, since it makes total failure of a single machine fairly rare. As long as you can
restore a backup onto a new machine fairly quickly, the downtime in case of failure is
not catastrophic in most applications. Thus, multi-machine redundancy was only
required by a small number of applications for which high availability was absolutely
essential.
However, as data volumes and applications’ computing demands have increased,
more applications have begun using larger numbers of machines, which proportion‐
ally increases the rate of hardware faults. Moreover, in some cloud platforms such as
Amazon Web Services (AWS) it is fairly common for virtual machine instances to
become unavailable without warning [7], as the platforms are designed to prioritize
flexibility and elasticityi over single-machine reliability.
Hence there is a move toward systems that can tolerate the loss of entire machines, by
using software fault-tolerance techniques in preference or in addition to hardware
redundancy. Such systems also have operational advantages: a single-server system
requires planned downtime if you need to reboot the machine (to apply operating
system security patches, for example), whereas a system that can tolerate machine
failure can be patched one node at a time, without downtime of the entire system (a
rolling upgrade; see Chapter 4).
Software Errors
We usually think of hardware faults as being random and independent from each
other: one machine’s disk failing does not imply that another machine’s disk is going
to fail. There may be weak correlations (for example due to a common cause, such as
the temperature in the server rack), but otherwise it is unlikely that a large number of
hardware components will fail at the same time.
Another class of fault is a systematic error within the system [8]. Such faults are
harder to anticipate, and because they are correlated across nodes, they tend to cause
many more system failures than uncorrelated hardware faults [5]. Examples include:
• A software bug that causes every instance of an application server to crash when
given a particular bad input. For example, consider the leap second on June 30,
2012, that caused many applications to hang simultaneously due to a bug in the
Linux kernel [9].
• A runaway process that uses up some shared resource—CPU time, memory, disk
space, or network bandwidth.
8 
| 
Chapter 1: Reliable, Scalable, and Maintainable Applications


• A service that the system depends on that slows down, becomes unresponsive, or
starts returning corrupted responses.
• Cascading failures, where a small fault in one component triggers a fault in
another component, which in turn triggers further faults [10].
The bugs that cause these kinds of software faults often lie dormant for a long time
until they are triggered by an unusual set of circumstances. In those circumstances, it
is revealed that the software is making some kind of assumption about its environ‐
ment—and while that assumption is usually true, it eventually stops being true for
some reason [11].
There is no quick solution to the problem of systematic faults in software. Lots of
small things can help: carefully thinking about assumptions and interactions in the
system; thorough testing; process isolation; allowing processes to crash and restart;
measuring, monitoring, and analyzing system behavior in production. If a system is
expected to provide some guarantee (for example, in a message queue, that the num‐
ber of incoming messages equals the number of outgoing messages), it can constantly
check itself while it is running and raise an alert if a discrepancy is found [12].
Human Errors
Humans design and build software systems, and the operators who keep the systems
running are also human. Even when they have the best intentions, humans are
known to be unreliable. For example, one study of large internet services found that
configuration errors by operators were the leading cause of outages, whereas hard‐
ware faults (servers or network) played a role in only 10–25% of outages [13].
How do we make our systems reliable, in spite of unreliable humans? The best sys‐
tems combine several approaches:
• Design systems in a way that minimizes opportunities for error. For example,
well-designed abstractions, APIs, and admin interfaces make it easy to do “the
right thing” and discourage “the wrong thing.” However, if the interfaces are too
restrictive people will work around them, negating their benefit, so this is a tricky
balance to get right.
• Decouple the places where people make the most mistakes from the places where
they can cause failures. In particular, provide fully featured non-production
sandbox environments where people can explore and experiment safely, using
real data, without affecting real users.
• Test thoroughly at all levels, from unit tests to whole-system integration tests and
manual tests [3]. Automated testing is widely used, well understood, and espe‐
cially valuable for covering corner cases that rarely arise in normal operation.
Reliability 
| 
9


• Allow quick and easy recovery from human errors, to minimize the impact in the
case of a failure. For example, make it fast to roll back configuration changes, roll
out new code gradually (so that any unexpected bugs affect only a small subset of
users), and provide tools to recompute data (in case it turns out that the old com‐
putation was incorrect).
• Set up detailed and clear monitoring, such as performance metrics and error
rates. In other engineering disciplines this is referred to as telemetry. (Once a
rocket has left the ground, telemetry is essential for tracking what is happening,
and for understanding failures [14].) Monitoring can show us early warning sig‐
nals and allow us to check whether any assumptions or constraints are being vio‐
lated. When a problem occurs, metrics can be invaluable in diagnosing the issue.
• Implement good management practices and training—a complex and important
aspect, and beyond the scope of this book.
How Important Is Reliability?
Reliability is not just for nuclear power stations and air traffic control software—
more mundane applications are also expected to work reliably. Bugs in business
applications cause lost productivity (and legal risks if figures are reported incor‐
rectly), and outages of ecommerce sites can have huge costs in terms of lost revenue
and damage to reputation.
Even in “noncritical” applications we have a responsibility to our users. Consider a
parent who stores all their pictures and videos of their children in your photo appli‐
cation [15]. How would they feel if that database was suddenly corrupted? Would
they know how to restore it from a backup?
There are situations in which we may choose to sacrifice reliability in order to reduce
development cost (e.g., when developing a prototype product for an unproven mar‐
ket) or operational cost (e.g., for a service with a very narrow profit margin)—but we
should be very conscious of when we are cutting corners. 
Scalability
Even if a system is working reliably today, that doesn’t mean it will necessarily work
reliably in the future. One common reason for degradation is increased load: perhaps
the system has grown from 10,000 concurrent users to 100,000 concurrent users, or
from 1 million to 10 million. Perhaps it is processing much larger volumes of data
than it did before.
Scalability is the term we use to describe a system’s ability to cope with increased
load. Note, however, that it is not a one-dimensional label that we can attach to a sys‐
tem: it is meaningless to say “X is scalable” or “Y doesn’t scale.” Rather, discussing
10 
| 
Chapter 1: Reliable, Scalable, and Maintainable Applications


ii. A term borrowed from electronic engineering, where it describes the number of logic gate inputs that are
attached to another gate’s output. The output needs to supply enough current to drive all the attached inputs.
In transaction processing systems, we use it to describe the number of requests to other services that we need
to make in order to serve one incoming request.
scalability means considering questions like “If the system grows in a particular way,
what are our options for coping with the growth?” and “How can we add computing
resources to handle the additional load?”
Describing Load
First, we need to succinctly describe the current load on the system; only then can we
discuss growth questions (what happens if our load doubles?). Load can be described
with a few numbers which we call load parameters. The best choice of parameters
depends on the architecture of your system: it may be requests per second to a web
server, the ratio of reads to writes in a database, the number of simultaneously active
users in a chat room, the hit rate on a cache, or something else. Perhaps the average
case is what matters for you, or perhaps your bottleneck is dominated by a small
number of extreme cases.
To make this idea more concrete, let’s consider Twitter as an example, using data
published in November 2012 [16]. Two of Twitter’s main operations are:
Post tweet
A user can publish a new message to their followers (4.6k requests/sec on aver‐
age, over 12k requests/sec at peak).
Home timeline
A user can view tweets posted by the people they follow (300k requests/sec).
Simply handling 12,000 writes per second (the peak rate for posting tweets) would be
fairly easy. However, Twitter’s scaling challenge is not primarily due to tweet volume,
but due to fan-outii—each user follows many people, and each user is followed by
many people. There are broadly two ways of implementing these two operations:
1. Posting a tweet simply inserts the new tweet into a global collection of tweets.
When a user requests their home timeline, look up all the people they follow,
find all the tweets for each of those users, and merge them (sorted by time). In a
relational database like in Figure 1-2, you could write a query such as:
SELECT tweets.*, users.* FROM tweets
  JOIN users   ON tweets.sender_id    = users.id
  JOIN follows ON follows.followee_id = users.id
  WHERE follows.follower_id = current_user
Scalability 
| 
11


2. Maintain a cache for each user’s home timeline—like a mailbox of tweets for
each recipient user (see Figure 1-3). When a user posts a tweet, look up all the
people who follow that user, and insert the new tweet into each of their home
timeline caches. The request to read the home timeline is then cheap, because its
result has been computed ahead of time.
Figure 1-2. Simple relational schema for implementing a Twitter home timeline.
Figure 1-3. Twitter’s data pipeline for delivering tweets to followers, with load parame‐
ters as of November 2012 [16].
The first version of Twitter used approach 1, but the systems struggled to keep up
with the load of home timeline queries, so the company switched to approach 2. This
works better because the average rate of published tweets is almost two orders of
magnitude lower than the rate of home timeline reads, and so in this case it’s prefera‐
ble to do more work at write time and less at read time.
However, the downside of approach 2 is that posting a tweet now requires a lot of
extra work. On average, a tweet is delivered to about 75 followers, so 4.6k tweets per
second become 345k writes per second to the home timeline caches. But this average
hides the fact that the number of followers per user varies wildly, and some users
12 
| 
Chapter 1: Reliable, Scalable, and Maintainable Applications


iii. In an ideal world, the running time of a batch job is the size of the dataset divided by the throughput. In
practice, the running time is often longer, due to skew (data not being spread evenly across worker processes)
and needing to wait for the slowest task to complete.
have over 30 million followers. This means that a single tweet may result in over 30
million writes to home timelines! Doing this in a timely manner—Twitter tries to
deliver tweets to followers within five seconds—is a significant challenge.
In the example of Twitter, the distribution of followers per user (maybe weighted by
how often those users tweet) is a key load parameter for discussing scalability, since it
determines the fan-out load. Your application may have very different characteristics,
but you can apply similar principles to reasoning about its load.
The final twist of the Twitter anecdote: now that approach 2 is robustly implemented,
Twitter is moving to a hybrid of both approaches. Most users’ tweets continue to be
fanned out to home timelines at the time when they are posted, but a small number
of users with a very large number of followers (i.e., celebrities) are excepted from this
fan-out. Tweets from any celebrities that a user may follow are fetched separately and
merged with that user’s home timeline when it is read, like in approach 1. This hybrid
approach is able to deliver consistently good performance. We will revisit this exam‐
ple in Chapter 12 after we have covered some more technical ground.
Describing Performance
Once you have described the load on your system, you can investigate what happens
when the load increases. You can look at it in two ways:
• When you increase a load parameter and keep the system resources (CPU, mem‐
ory, network bandwidth, etc.) unchanged, how is the performance of your system
affected?
• When you increase a load parameter, how much do you need to increase the
resources if you want to keep performance unchanged?
Both questions require performance numbers, so let’s look briefly at describing the
performance of a system.
In a batch processing system such as Hadoop, we usually care about throughput—the
number of records we can process per second, or the total time it takes to run a job
on a dataset of a certain size.iii In online systems, what’s usually more important is the
service’s response time—that is, the time between a client sending a request and
receiving a response.
Scalability 
| 
13


Latency and response time
Latency and response time are often used synonymously, but they
are not the same. The response time is what the client sees: besides
the actual time to process the request (the service time), it includes
network delays and queueing delays. Latency is the duration that a
request is waiting to be handled—during which it is latent, await‐
ing service [17].
Even if you only make the same request over and over again, you’ll get a slightly dif‐
ferent response time on every try. In practice, in a system handling a variety of
requests, the response time can vary a lot. We therefore need to think of response
time not as a single number, but as a distribution of values that you can measure.
In Figure 1-4, each gray bar represents a request to a service, and its height shows
how long that request took. Most requests are reasonably fast, but there are occa‐
sional outliers that take much longer. Perhaps the slow requests are intrinsically more
expensive, e.g., because they process more data. But even in a scenario where you’d
think all requests should take the same time, you get variation: random additional
latency could be introduced by a context switch to a background process, the loss of a
network packet and TCP retransmission, a garbage collection pause, a page fault
forcing a read from disk, mechanical vibrations in the server rack [18], or many other
causes.
Figure 1-4. Illustrating mean and percentiles: response times for a sample of 100
requests to a service.
It’s common to see the average response time of a service reported. (Strictly speaking,
the term “average” doesn’t refer to any particular formula, but in practice it is usually
understood as the arithmetic mean: given n values, add up all the values, and divide
by n.) However, the mean is not a very good metric if you want to know your “typi‐
cal” response time, because it doesn’t tell you how many users actually experienced
that delay.
Usually it is better to use percentiles. If you take your list of response times and sort it
from fastest to slowest, then the median is the halfway point: for example, if your
14 
| 
Chapter 1: Reliable, Scalable, and Maintainable Applications


median response time is 200 ms, that means half your requests return in less than
200 ms, and half your requests take longer than that.
This makes the median a good metric if you want to know how long users typically
have to wait: half of user requests are served in less than the median response time,
and the other half take longer than the median. The median is also known as the 50th
percentile, and sometimes abbreviated as p50. Note that the median refers to a single
request; if the user makes several requests (over the course of a session, or because
several resources are included in a single page), the probability that at least one of
them is slower than the median is much greater than 50%.
In order to figure out how bad your outliers are, you can look at higher percentiles:
the 95th, 99th, and 99.9th percentiles are common (abbreviated p95, p99, and p999).
They are the response time thresholds at which 95%, 99%, or 99.9% of requests are
faster than that particular threshold. For example, if the 95th percentile response time
is 1.5 seconds, that means 95 out of 100 requests take less than 1.5 seconds, and 5 out
of 100 requests take 1.5 seconds or more. This is illustrated in Figure 1-4.
High percentiles of response times, also known as tail latencies, are important
because they directly affect users’ experience of the service. For example, Amazon
describes response time requirements for internal services in terms of the 99.9th per‐
centile, even though it only affects 1 in 1,000 requests. This is because the customers
with the slowest requests are often those who have the most data on their accounts
because they have made many purchases—that is, they’re the most valuable custom‐
ers [19]. It’s important to keep those customers happy by ensuring the website is fast
for them: Amazon has also observed that a 100 ms increase in response time reduces
sales by 1% [20], and others report that a 1-second slowdown reduces a customer sat‐
isfaction metric by 16% [21, 22].
On the other hand, optimizing the 99.99th percentile (the slowest 1 in 10,000
requests) was deemed too expensive and to not yield enough benefit for Amazon’s
purposes. Reducing response times at very high percentiles is difficult because they
are easily affected by random events outside of your control, and the benefits are
diminishing.
For example, percentiles are often used in service level objectives (SLOs) and service
level agreements (SLAs), contracts that define the expected performance and availa‐
bility of a service. An SLA may state that the service is considered to be up if it has a
median response time of less than 200 ms and a 99th percentile under 1 s (if the
response time is longer, it might as well be down), and the service may be required to
be up at least 99.9% of the time. These metrics set expectations for clients of the ser‐
vice and allow customers to demand a refund if the SLA is not met.
Queueing delays often account for a large part of the response time at high percen‐
tiles. As a server can only process a small number of things in parallel (limited, for
Scalability 
| 
15


example, by its number of CPU cores), it only takes a small number of slow requests
to hold up the processing of subsequent requests—an effect sometimes known as
head-of-line blocking. Even if those subsequent requests are fast to process on the
server, the client will see a slow overall response time due to the time waiting for the
prior request to complete. Due to this effect, it is important to measure response
times on the client side.
When generating load artificially in order to test the scalability of a system, the loadgenerating client needs to keep sending requests independently of the response time.
If the client waits for the previous request to complete before sending the next one,
that behavior has the effect of artificially keeping the queues shorter in the test than
they would be in reality, which skews the measurements [23].
Percentiles in Practice
High percentiles become especially important in backend services that are called mul‐
tiple times as part of serving a single end-user request. Even if you make the calls in
parallel, the end-user request still needs to wait for the slowest of the parallel calls to
complete. It takes just one slow call to make the entire end-user request slow, as illus‐
trated in Figure 1-5. Even if only a small percentage of backend calls are slow, the
chance of getting a slow call increases if an end-user request requires multiple back‐
end calls, and so a higher proportion of end-user requests end up being slow (an
effect known as tail latency amplification [24]).
If you want to add response time percentiles to the monitoring dashboards for your
services, you need to efficiently calculate them on an ongoing basis. For example, you
may want to keep a rolling window of response times of requests in the last 10
minutes. Every minute, you calculate the median and various percentiles over the val‐
ues in that window and plot those metrics on a graph.
The naïve implementation is to keep a list of response times for all requests within the
time window and to sort that list every minute. If that is too inefficient for you, there
are algorithms that can calculate a good approximation of percentiles at minimal
CPU and memory cost, such as forward decay [25], t-digest [26], or HdrHistogram
[27]. Beware that averaging percentiles, e.g., to reduce the time resolution or to com‐
bine data from several machines, is mathematically meaningless—the right way of
aggregating response time data is to add the histograms [28].
16 
| 
Chapter 1: Reliable, Scalable, and Maintainable Applications


Figure 1-5. When several backend calls are needed to serve a request, it takes just a sin‐
gle slow backend request to slow down the entire end-user request.
Approaches for Coping with Load
Now that we have discussed the parameters for describing load and metrics for meas‐
uring performance, we can start discussing scalability in earnest: how do we maintain
good performance even when our load parameters increase by some amount?
An architecture that is appropriate for one level of load is unlikely to cope with 10
times that load. If you are working on a fast-growing service, it is therefore likely that
you will need to rethink your architecture on every order of magnitude load increase
—or perhaps even more often than that.
People often talk of a dichotomy between scaling up (vertical scaling, moving to a
more powerful machine) and scaling out (horizontal scaling, distributing the load
across multiple smaller machines). Distributing load across multiple machines is also
known as a shared-nothing architecture. A system that can run on a single machine is
often simpler, but high-end machines can become very expensive, so very intensive
workloads often can’t avoid scaling out. In reality, good architectures usually involve
a pragmatic mixture of approaches: for example, using several fairly powerful
machines can still be simpler and cheaper than a large number of small virtual
machines.
Some systems are elastic, meaning that they can automatically add computing resour‐
ces when they detect a load increase, whereas other systems are scaled manually (a
human analyzes the capacity and decides to add more machines to the system). An
elastic system can be useful if load is highly unpredictable, but manually scaled sys‐
tems are simpler and may have fewer operational surprises (see “Rebalancing Parti‐
tions” on page 209).
Scalability 
| 
17


While distributing stateless services across multiple machines is fairly straightfor‐
ward, taking stateful data systems from a single node to a distributed setup can intro‐
duce a lot of additional complexity. For this reason, common wisdom until recently
was to keep your database on a single node (scale up) until scaling cost or highavailability requirements forced you to make it distributed.
As the tools and abstractions for distributed systems get better, this common wisdom
may change, at least for some kinds of applications. It is conceivable that distributed
data systems will become the default in the future, even for use cases that don’t han‐
dle large volumes of data or traffic. Over the course of the rest of this book we will
cover many kinds of distributed data systems, and discuss how they fare not just in
terms of scalability, but also ease of use and maintainability.
The architecture of systems that operate at large scale is usually highly specific to the
application—there is no such thing as a generic, one-size-fits-all scalable architecture
(informally known as magic scaling sauce). The problem may be the volume of reads,
the volume of writes, the volume of data to store, the complexity of the data, the
response time requirements, the access patterns, or (usually) some mixture of all of
these plus many more issues.
For example, a system that is designed to handle 100,000 requests per second, each
1 kB in size, looks very different from a system that is designed for 3 requests per
minute, each 2 GB in size—even though the two systems have the same data through‐
put.
An architecture that scales well for a particular application is built around assump‐
tions of which operations will be common and which will be rare—the load parame‐
ters. If those assumptions turn out to be wrong, the engineering effort for scaling is at
best wasted, and at worst counterproductive. In an early-stage startup or an unpro‐
ven product it’s usually more important to be able to iterate quickly on product fea‐
tures than it is to scale to some hypothetical future load.
Even though they are specific to a particular application, scalable architectures are
nevertheless usually built from general-purpose building blocks, arranged in familiar
patterns. In this book we discuss those building blocks and patterns. 
Maintainability
It is well known that the majority of the cost of software is not in its initial develop‐
ment, but in its ongoing maintenance—fixing bugs, keeping its systems operational,
investigating failures, adapting it to new platforms, modifying it for new use cases,
repaying technical debt, and adding new features.
Yet, unfortunately, many people working on software systems dislike maintenance of
so-called legacy systems—perhaps it involves fixing other people’s mistakes, or work‐
18 
| 
Chapter 1: Reliable, Scalable, and Maintainable Applications


ing with platforms that are now outdated, or systems that were forced to do things
they were never intended for. Every legacy system is unpleasant in its own way, and
so it is difficult to give general recommendations for dealing with them.
However, we can and should design software in such a way that it will hopefully min‐
imize pain during maintenance, and thus avoid creating legacy software ourselves. To
this end, we will pay particular attention to three design principles for software
systems:
Operability
Make it easy for operations teams to keep the system running smoothly.
Simplicity
Make it easy for new engineers to understand the system, by removing as much
complexity as possible from the system. (Note this is not the same as simplicity
of the user interface.)
Evolvability
Make it easy for engineers to make changes to the system in the future, adapting
it for unanticipated use cases as requirements change. Also known as extensibil‐
ity, modifiability, or plasticity.
As previously with reliability and scalability, there are no easy solutions for achieving
these goals. Rather, we will try to think about systems with operability, simplicity,
and evolvability in mind.
Operability: Making Life Easy for Operations
It has been suggested that “good operations can often work around the limitations of
bad (or incomplete) software, but good software cannot run reliably with bad opera‐
tions” [12]. While some aspects of operations can and should be automated, it is still
up to humans to set up that automation in the first place and to make sure it’s work‐
ing correctly.
Operations teams are vital to keeping a software system running smoothly. A good
operations team typically is responsible for the following, and more [29]:
• Monitoring the health of the system and quickly restoring service if it goes into a
bad state
• Tracking down the cause of problems, such as system failures or degraded per‐
formance
• Keeping software and platforms up to date, including security patches
• Keeping tabs on how different systems affect each other, so that a problematic
change can be avoided before it causes damage
Maintainability 
| 
19


• Anticipating future problems and solving them before they occur (e.g., capacity
planning)
• Establishing good practices and tools for deployment, configuration manage‐
ment, and more
• Performing complex maintenance tasks, such as moving an application from one
platform to another
• Maintaining the security of the system as configuration changes are made
• Defining processes that make operations predictable and help keep the produc‐
tion environment stable
• Preserving the organization’s knowledge about the system, even as individual
people come and go
Good operability means making routine tasks easy, allowing the operations team to
focus their efforts on high-value activities. Data systems can do various things to
make routine tasks easy, including:
• Providing visibility into the runtime behavior and internals of the system, with
good monitoring
• Providing good support for automation and integration with standard tools
• Avoiding dependency on individual machines (allowing machines to be taken
down for maintenance while the system as a whole continues running uninter‐
rupted)
• Providing good documentation and an easy-to-understand operational model
(“If I do X, Y will happen”)
• Providing good default behavior, but also giving administrators the freedom to
override defaults when needed
• Self-healing where appropriate, but also giving administrators manual control
over the system state when needed
• Exhibiting predictable behavior, minimizing surprises
Simplicity: Managing Complexity
Small software projects can have delightfully simple and expressive code, but as
projects get larger, they often become very complex and difficult to understand. This
complexity slows down everyone who needs to work on the system, further increas‐
ing the cost of maintenance. A software project mired in complexity is sometimes
described as a big ball of mud [30].
20 
| 
Chapter 1: Reliable, Scalable, and Maintainable Applications


There are various possible symptoms of complexity: explosion of the state space, tight
coupling of modules, tangled dependencies, inconsistent naming and terminology,
hacks aimed at solving performance problems, special-casing to work around issues
elsewhere, and many more. Much has been said on this topic already [31, 32, 33].
When complexity makes maintenance hard, budgets and schedules are often over‐
run. In complex software, there is also a greater risk of introducing bugs when mak‐
ing a change: when the system is harder for developers to understand and reason
about, hidden assumptions, unintended consequences, and unexpected interactions
are more easily overlooked. Conversely, reducing complexity greatly improves the
maintainability of software, and thus simplicity should be a key goal for the systems
we build.
Making a system simpler does not necessarily mean reducing its functionality; it can
also mean removing accidental complexity. Moseley and Marks [32] define complex‐
ity as accidental if it is not inherent in the problem that the software solves (as seen
by the users) but arises only from the implementation.
One of the best tools we have for removing accidental complexity is abstraction. A
good abstraction can hide a great deal of implementation detail behind a clean,
simple-to-understand façade. A good abstraction can also be used for a wide range of
different applications. Not only is this reuse more efficient than reimplementing a
similar thing multiple times, but it also leads to higher-quality software, as quality
improvements in the abstracted component benefit all applications that use it.
For example, high-level programming languages are abstractions that hide machine
code, CPU registers, and syscalls. SQL is an abstraction that hides complex on-disk
and in-memory data structures, concurrent requests from other clients, and inconsis‐
tencies after crashes. Of course, when programming in a high-level language, we are
still using machine code; we are just not using it directly, because the programming
language abstraction saves us from having to think about it.
However, finding good abstractions is very hard. In the field of distributed systems,
although there are many good algorithms, it is much less clear how we should be
packaging them into abstractions that help us keep the complexity of the system at a
manageable level.
Throughout this book, we will keep our eyes open for good abstractions that allow us
to extract parts of a large system into well-defined, reusable components.
Evolvability: Making Change Easy
It’s extremely unlikely that your system’s requirements will remain unchanged for‐
ever. They are much more likely to be in constant flux: you learn new facts, previ‐
ously unanticipated use cases emerge, business priorities change, users request new
Maintainability 
| 
21


features, new platforms replace old platforms, legal or regulatory requirements
change, growth of the system forces architectural changes, etc.
In terms of organizational processes, Agile working patterns provide a framework for
adapting to change. The Agile community has also developed technical tools and pat‐
terns that are helpful when developing software in a frequently changing environ‐
ment, such as test-driven development (TDD) and refactoring.
Most discussions of these Agile techniques focus on a fairly small, local scale (a cou‐
ple of source code files within the same application). In this book, we search for ways
of increasing agility on the level of a larger data system, perhaps consisting of several
different applications or services with different characteristics. For example, how
would you “refactor” Twitter’s architecture for assembling home timelines (“Describ‐
ing Load” on page 11) from approach 1 to approach 2?
The ease with which you can modify a data system, and adapt it to changing require‐
ments, is closely linked to its simplicity and its abstractions: simple and easy-tounderstand systems are usually easier to modify than complex ones. But since this is
such an important idea, we will use a different word to refer to agility on a data sys‐
tem level: evolvability [34]. 
Summary
In this chapter, we have explored some fundamental ways of thinking about dataintensive applications. These principles will guide us through the rest of the book,
where we dive into deep technical detail.
An application has to meet various requirements in order to be useful. There are
functional requirements (what it should do, such as allowing data to be stored,
retrieved, searched, and processed in various ways), and some nonfunctional require‐
ments (general properties like security, reliability, compliance, scalability, compatibil‐
ity, and maintainability). In this chapter we discussed reliability, scalability, and
maintainability in detail.
Reliability means making systems work correctly, even when faults occur. Faults can
be in hardware (typically random and uncorrelated), software (bugs are typically sys‐
tematic and hard to deal with), and humans (who inevitably make mistakes from
time to time). Fault-tolerance techniques can hide certain types of faults from the end
user.
Scalability means having strategies for keeping performance good, even when load
increases. In order to discuss scalability, we first need ways of describing load and
performance quantitatively. We briefly looked at Twitter’s home timelines as an
example of describing load, and response time percentiles as a way of measuring per‐
22 
| 
Chapter 1: Reliable, Scalable, and Maintainable Applications


formance. In a scalable system, you can add processing capacity in order to remain
reliable under high load.
Maintainability has many facets, but in essence it’s about making life better for the
engineering and operations teams who need to work with the system. Good abstrac‐
tions can help reduce complexity and make the system easier to modify and adapt for
new use cases. Good operability means having good visibility into the system’s health,
and having effective ways of managing it.
There is unfortunately no easy fix for making applications reliable, scalable, or main‐
tainable. However, there are certain patterns and techniques that keep reappearing in
different kinds of applications. In the next few chapters we will take a look at some
examples of data systems and analyze how they work toward those goals.
Later in the book, in Part III, we will look at patterns for systems that consist of sev‐
eral components working together, such as the one in Figure 1-1.
References
[1] Michael Stonebraker and Uğur Çetintemel: “‘One Size Fits All’: An Idea Whose
Time Has Come and Gone,” at 21st International Conference on Data Engineering
(ICDE), April 2005.
[2] Walter L. Heimerdinger and Charles B. Weinstock: “A Conceptual Framework
for System Fault Tolerance,” Technical Report CMU/SEI-92-TR-033, Software Engi‐
neering Institute, Carnegie Mellon University, October 1992.
[3] Ding Yuan, Yu Luo, Xin Zhuang, et al.: “Simple Testing Can Prevent Most Criti‐
cal Failures: An Analysis of Production Failures in Distributed Data-Intensive Sys‐
tems,” at 11th USENIX Symposium on Operating Systems Design and Implementation
(OSDI), October 2014.
[4] Yury Izrailevsky and Ariel Tseitlin: “The Netflix Simian Army,” techblog.net‐
flix.com, July 19, 2011.
[5] Daniel Ford, François Labelle, Florentina I. Popovici, et al.: “Availability in Glob‐
ally Distributed Storage Systems,” at 9th USENIX Symposium on Operating Systems
Design and Implementation (OSDI), October 2010.
[6] Brian Beach: “Hard Drive Reliability Update – Sep 2014,” backblaze.com, Septem‐
ber 23, 2014.
[7] Laurie Voss: “AWS: The Good, the Bad and the Ugly,” blog.awe.sm, December 18,
2012.
Summary 
| 
23


[8] Haryadi S. Gunawi, Mingzhe Hao, Tanakorn Leesatapornwongsa, et al.: “What
Bugs Live in the Cloud?,” at 5th ACM Symposium on Cloud Computing (SoCC),
November 2014. doi:10.1145/2670979.2670986
[9] Nelson Minar: “Leap Second Crashes Half the Internet,” somebits.com, July 3,
2012.
[10] Amazon Web Services: “Summary of the Amazon EC2 and Amazon RDS Ser‐
vice Disruption in the US East Region,” aws.amazon.com, April 29, 2011.
[11] Richard I. Cook: “How Complex Systems Fail,” Cognitive Technologies Labora‐
tory, April 2000.
[12] Jay Kreps: “Getting Real About Distributed System Reliability,” blog.empathy‐
box.com, March 19, 2012.
[13] David Oppenheimer, Archana Ganapathi, and David A. Patterson: “Why Do
Internet Services Fail, and What Can Be Done About It?,” at 4th USENIX Symposium
on Internet Technologies and Systems (USITS), March 2003.
[14] Nathan Marz: “Principles of Software Engineering, Part 1,” nathanmarz.com,
April 2, 2013.
[15] Michael Jurewitz: “The Human Impact of Bugs,” jury.me, March 15, 2013.
[16] Raffi Krikorian: “Timelines at Scale,” at QCon San Francisco, November 2012.
[17] Martin Fowler: Patterns of Enterprise Application Architecture. Addison Wesley,
2002. ISBN: 978-0-321-12742-6
[18] Kelly Sommers: “After all that run around, what caused 500ms disk latency even
when we replaced physical server?” twitter.com, November 13, 2014.
[19] Giuseppe DeCandia, Deniz Hastorun, Madan Jampani, et al.: “Dynamo: Ama‐
zon’s Highly Available Key-Value Store,” at 21st ACM Symposium on Operating Sys‐
tems Principles (SOSP), October 2007.
[20] Greg Linden: “Make Data Useful,” slides from presentation at Stanford Univer‐
sity Data Mining class (CS345), December 2006.
[21] Tammy Everts: “The Real Cost of Slow Time vs Downtime,” webperformanceto‐
day.com, November 12, 2014.
[22] Jake Brutlag: “Speed Matters for Google Web Search,” googleresearch.blog‐
spot.co.uk, June 22, 2009.
[23] Tyler Treat: “Everything You Know About Latency Is Wrong,” bravenew‐
geek.com, December 12, 2015.
24 
| 
Chapter 1: Reliable, Scalable, and Maintainable Applications


[24] Jeffrey Dean and Luiz André Barroso: “The Tail at Scale,” Communications of the
ACM, 
volume 
56, 
number 
2, 
pages 
74–80, 
February 
2013. 
doi:
10.1145/2408776.2408794
[25] Graham Cormode, Vladislav Shkapenyuk, Divesh Srivastava, and Bojian Xu:
“Forward Decay: A Practical Time Decay Model for Streaming Systems,” at 25th
IEEE International Conference on Data Engineering (ICDE), March 2009.
[26] Ted Dunning and Otmar Ertl: “Computing Extremely Accurate Quantiles Using
t-Digests,” github.com, March 2014.
[27] Gil Tene: “HdrHistogram,” hdrhistogram.org.
[28] Baron Schwartz: “Why Percentiles Don’t Work the Way You Think,” vividcor‐
tex.com, December 7, 2015.
[29] James Hamilton: “On Designing and Deploying Internet-Scale Services,” at 21st
Large Installation System Administration Conference (LISA), November 2007.
[30] Brian Foote and Joseph Yoder: “Big Ball of Mud,” at 4th Conference on Pattern
Languages of Programs (PLoP), September 1997.
[31] Frederick P Brooks: “No Silver Bullet – Essence and Accident in Software Engi‐
neering,” in The Mythical Man-Month, Anniversary edition, Addison-Wesley, 1995.
ISBN: 978-0-201-83595-3
[32] Ben Moseley and Peter Marks: “Out of the Tar Pit,” at BCS Software Practice
Advancement (SPA), 2006.
[33] Rich Hickey: “Simple Made Easy,” at Strange Loop, September 2011.
[34] Hongyu Pei Breivold, Ivica Crnkovic, and Peter J. Eriksson: “Analyzing Software
Evolvability,” at 32nd Annual IEEE International Computer Software and Applica‐
tions Conference (COMPSAC), July 2008. doi:10.1109/COMPSAC.2008.50
Summary 
| 
25




CHAPTER 2
Data Models and Query Languages
The limits of my language mean the limits of my world.
—Ludwig Wittgenstein, Tractatus Logico-Philosophicus (1922)
Data models are perhaps the most important part of developing software, because
they have such a profound effect: not only on how the software is written, but also on
how we think about the problem that we are solving.
Most applications are built by layering one data model on top of another. For each
layer, the key question is: how is it represented in terms of the next-lower layer? For
example:
1. As an application developer, you look at the real world (in which there are peo‐
ple, organizations, goods, actions, money flows, sensors, etc.) and model it in
terms of objects or data structures, and APIs that manipulate those data struc‐
tures. Those structures are often specific to your application.
2. When you want to store those data structures, you express them in terms of a
general-purpose data model, such as JSON or XML documents, tables in a rela‐
tional database, or a graph model.
3. The engineers who built your database software decided on a way of representing
that JSON/XML/relational/graph data in terms of bytes in memory, on disk, or
on a network. The representation may allow the data to be queried, searched,
manipulated, and processed in various ways.
4. On yet lower levels, hardware engineers have figured out how to represent bytes
in terms of electrical currents, pulses of light, magnetic fields, and more.
In a complex application there may be more intermediary levels, such as APIs built
upon APIs, but the basic idea is still the same: each layer hides the complexity of the
layers below it by providing a clean data model. These abstractions allow different
27


groups of people—for example, the engineers at the database vendor and the applica‐
tion developers using their database—to work together effectively.
There are many different kinds of data models, and every data model embodies
assumptions about how it is going to be used. Some kinds of usage are easy and some
are not supported; some operations are fast and some perform badly; some data
transformations feel natural and some are awkward.
It can take a lot of effort to master just one data model (think how many books there
are on relational data modeling). Building software is hard enough, even when work‐
ing with just one data model and without worrying about its inner workings. But
since the data model has such a profound effect on what the software above it can
and can’t do, it’s important to choose one that is appropriate to the application.
In this chapter we will look at a range of general-purpose data models for data stor‐
age and querying (point 2 in the preceding list). In particular, we will compare the
relational model, the document model, and a few graph-based data models. We will
also look at various query languages and compare their use cases. In Chapter 3 we
will discuss how storage engines work; that is, how these data models are actually
implemented (point 3 in the list).
Relational Model Versus Document Model
The best-known data model today is probably that of SQL, based on the relational
model proposed by Edgar Codd in 1970 [1]: data is organized into relations (called
tables in SQL), where each relation is an unordered collection of tuples (rows in SQL).
The relational model was a theoretical proposal, and many people at the time
doubted whether it could be implemented efficiently. However, by the mid-1980s,
relational database management systems (RDBMSes) and SQL had become the tools
of choice for most people who needed to store and query data with some kind of reg‐
ular structure. The dominance of relational databases has lasted around 25‒30 years
—an eternity in computing history.
The roots of relational databases lie in business data processing, which was performed
on mainframe computers in the 1960s and ’70s. The use cases appear mundane from
today’s perspective: typically transaction processing (entering sales or banking trans‐
actions, airline reservations, stock-keeping in warehouses) and batch processing (cus‐
tomer invoicing, payroll, reporting).
Other databases at that time forced application developers to think a lot about the
internal representation of the data in the database. The goal of the relational model
was to hide that implementation detail behind a cleaner interface.
Over the years, there have been many competing approaches to data storage and
querying. In the 1970s and early 1980s, the network model and the hierarchical model
28 
| 
Chapter 2: Data Models and Query Languages


were the main alternatives, but the relational model came to dominate them. Object
databases came and went again in the late 1980s and early 1990s. XML databases
appeared in the early 2000s, but have only seen niche adoption. Each competitor to
the relational model generated a lot of hype in its time, but it never lasted [2].
As computers became vastly more powerful and networked, they started being used
for increasingly diverse purposes. And remarkably, relational databases turned out to
generalize very well, beyond their original scope of business data processing, to a
broad variety of use cases. Much of what you see on the web today is still powered by
relational databases, be it online publishing, discussion, social networking, ecom‐
merce, games, software-as-a-service productivity applications, or much more.
The Birth of NoSQL
Now, in the 2010s, NoSQL is the latest attempt to overthrow the relational model’s
dominance. The name “NoSQL” is unfortunate, since it doesn’t actually refer to any
particular technology—it was originally intended simply as a catchy Twitter hashtag
for a meetup on open source, distributed, nonrelational databases in 2009 [3]. Never‐
theless, the term struck a nerve and quickly spread through the web startup commu‐
nity and beyond. A number of interesting database systems are now associated with
the #NoSQL hashtag, and it has been retroactively reinterpreted as Not Only SQL [4].
There are several driving forces behind the adoption of NoSQL databases, including:
• A need for greater scalability than relational databases can easily achieve, includ‐
ing very large datasets or very high write throughput
• A widespread preference for free and open source software over commercial
database products
• Specialized query operations that are not well supported by the relational model
• Frustration with the restrictiveness of relational schemas, and a desire for a more
dynamic and expressive data model [5]
Different applications have different requirements, and the best choice of technology
for one use case may well be different from the best choice for another use case. It
therefore seems likely that in the foreseeable future, relational databases will continue
to be used alongside a broad variety of nonrelational datastores—an idea that is
sometimes called polyglot persistence [3].
The Object-Relational Mismatch
Most application development today is done in object-oriented programming lan‐
guages, which leads to a common criticism of the SQL data model: if data is stored in
relational tables, an awkward translation layer is required between the objects in the
Relational Model Versus Document Model 
| 
29


i. A term borrowed from electronics. Every electric circuit has a certain impedance (resistance to alternating
current) on its inputs and outputs. When you connect one circuit’s output to another one’s input, the power
transfer across the connection is maximized if the output and input impedances of the two circuits match. An
impedance mismatch can lead to signal reflections and other troubles.
application code and the database model of tables, rows, and columns. The discon‐
nect between the models is sometimes called an impedance mismatch.i
Object-relational mapping (ORM) frameworks like ActiveRecord and Hibernate
reduce the amount of boilerplate code required for this translation layer, but they
can’t completely hide the differences between the two models.
For example, Figure 2-1 illustrates how a résumé (a LinkedIn profile) could be
expressed in a relational schema. The profile as a whole can be identified by a unique
identifier, user_id. Fields like first_name and last_name appear exactly once per
user, so they can be modeled as columns on the users table. However, most people
have had more than one job in their career (positions), and people may have varying
numbers of periods of education and any number of pieces of contact information.
There is a one-to-many relationship from the user to these items, which can be repre‐
sented in various ways:
• In the traditional SQL model (prior to SQL:1999), the most common normalized
representation is to put positions, education, and contact information in separate
tables, with a foreign key reference to the users table, as in Figure 2-1.
• Later versions of the SQL standard added support for structured datatypes and
XML data; this allowed multi-valued data to be stored within a single row, with
support for querying and indexing inside those documents. These features are
supported to varying degrees by Oracle, IBM DB2, MS SQL Server, and Post‐
greSQL [6, 7]. A JSON datatype is also supported by several databases, including
IBM DB2, MySQL, and PostgreSQL [8].
• A third option is to encode jobs, education, and contact info as a JSON or XML
document, store it on a text column in the database, and let the application inter‐
pret its structure and content. In this setup, you typically cannot use the database
to query for values inside that encoded column.
30 
| 
Chapter 2: Data Models and Query Languages


Figure 2-1. Representing a LinkedIn profile using a relational schema. Photo of Bill
Gates courtesy of Wikimedia Commons, Ricardo Stuckert, Agência Brasil.
For a data structure like a résumé, which is mostly a self-contained document, a JSON
representation can be quite appropriate: see Example 2-1. JSON has the appeal of
being much simpler than XML. Document-oriented databases like MongoDB [9],
RethinkDB [10], CouchDB [11], and Espresso [12] support this data model.
Example 2-1. Representing a LinkedIn profile as a JSON document
{
  "user_id":     251,
  "first_name":  "Bill",
  "last_name":   "Gates",
  "summary":     "Co-chair of the Bill & Melinda Gates... Active blogger.",
  "region_id":   "us:91",
  "industry_id": 131,
  "photo_url":   "/p/7/000/253/05b/308dd6e.jpg",
Relational Model Versus Document Model 
| 
31


  "positions": [
    {"job_title": "Co-chair", "organization": "Bill & Melinda Gates Foundation"},
    {"job_title": "Co-founder, Chairman", "organization": "Microsoft"}
  ],
  "education": [
    {"school_name": "Harvard University",       "start": 1973, "end": 1975},
    {"school_name": "Lakeside School, Seattle", "start": null, "end": null}
  ],
  "contact_info": {
    "blog":    "http://thegatesnotes.com",
    "twitter": "http://twitter.com/BillGates"
  }
}
Some developers feel that the JSON model reduces the impedance mismatch between
the application code and the storage layer. However, as we shall see in Chapter 4,
there are also problems with JSON as a data encoding format. The lack of a schema is
often cited as an advantage; we will discuss this in “Schema flexibility in the docu‐
ment model” on page 39.
The JSON representation has better locality than the multi-table schema in
Figure 2-1. If you want to fetch a profile in the relational example, you need to either
perform multiple queries (query each table by user_id) or perform a messy multiway join between the users table and its subordinate tables. In the JSON representa‐
tion, all the relevant information is in one place, and one query is sufficient.
The one-to-many relationships from the user profile to the user’s positions, educa‐
tional history, and contact information imply a tree structure in the data, and the
JSON representation makes this tree structure explicit (see Figure 2-2).
Figure 2-2. One-to-many relationships forming a tree structure.
32 
| 
Chapter 2: Data Models and Query Languages


ii. Literature on the relational model distinguishes several different normal forms, but the distinctions are of
little practical interest. As a rule of thumb, if you’re duplicating values that could be stored in just one place,
the schema is not normalized.
Many-to-One and Many-to-Many Relationships
In Example 2-1 in the preceding section, region_id and industry_id are given as
IDs, not as plain-text strings "Greater Seattle Area" and "Philanthropy". Why?
If the user interface has free-text fields for entering the region and the industry, it
makes sense to store them as plain-text strings. But there are advantages to having
standardized lists of geographic regions and industries, and letting users choose from
a drop-down list or autocompleter:
• Consistent style and spelling across profiles
• Avoiding ambiguity (e.g., if there are several cities with the same name)
• Ease of updating—the name is stored in only one place, so it is easy to update
across the board if it ever needs to be changed (e.g., change of a city name due to
political events)
• Localization support—when the site is translated into other languages, the stand‐
ardized lists can be localized, so the region and industry can be displayed in the
viewer’s language
• Better search—e.g., a search for philanthropists in the state of Washington can
match this profile, because the list of regions can encode the fact that Seattle is in
Washington (which is not apparent from the string "Greater Seattle Area")
Whether you store an ID or a text string is a question of duplication. When you use
an ID, the information that is meaningful to humans (such as the word Philanthropy)
is stored in only one place, and everything that refers to it uses an ID (which only has
meaning within the database). When you store the text directly, you are duplicating
the human-meaningful information in every record that uses it.
The advantage of using an ID is that because it has no meaning to humans, it never
needs to change: the ID can remain the same, even if the information it identifies
changes. Anything that is meaningful to humans may need to change sometime in
the future—and if that information is duplicated, all the redundant copies need to be
updated. That incurs write overheads, and risks inconsistencies (where some copies
of the information are updated but others aren’t). Removing such duplication is the
key idea behind normalization in databases.ii
Relational Model Versus Document Model 
| 
33


iii. At the time of writing, joins are supported in RethinkDB, not supported in MongoDB, and only sup‐
ported in predeclared views in CouchDB.
Database administrators and developers love to argue about nor‐
malization and denormalization, but we will suspend judgment for
now. In Part III of this book we will return to this topic and explore
systematic ways of dealing with caching, denormalization, and
derived data.
Unfortunately, normalizing this data requires many-to-one relationships (many peo‐
ple live in one particular region, many people work in one particular industry), which
don’t fit nicely into the document model. In relational databases, it’s normal to refer
to rows in other tables by ID, because joins are easy. In document databases, joins are
not needed for one-to-many tree structures, and support for joins is often weak.iii
If the database itself does not support joins, you have to emulate a join in application
code by making multiple queries to the database. (In this case, the lists of regions and
industries are probably small and slow-changing enough that the application can
simply keep them in memory. But nevertheless, the work of making the join is shifted
from the database to the application code.)
Moreover, even if the initial version of an application fits well in a join-free docu‐
ment model, data has a tendency of becoming more interconnected as features are
added to applications. For example, consider some changes we could make to the
résumé example:
Organizations and schools as entities
In the previous description, organization (the company where the user worked)
and school_name (where they studied) are just strings. Perhaps they should be
references to entities instead? Then each organization, school, or university could
have its own web page (with logo, news feed, etc.); each résumé could link to the
organizations and schools that it mentions, and include their logos and other
information (see Figure 2-3 for an example from LinkedIn).
Recommendations
Say you want to add a new feature: one user can write a recommendation for
another user. The recommendation is shown on the résumé of the user who was
recommended, together with the name and photo of the user making the recom‐
mendation. If the recommender updates their photo, any recommendations they
have written need to reflect the new photo. Therefore, the recommendation
should have a reference to the author’s profile.
34 
| 
Chapter 2: Data Models and Query Languages


Figure 2-3. The company name is not just a string, but a link to a company entity.
Screenshot of linkedin.com.
Figure 2-4 illustrates how these new features require many-to-many relationships.
The data within each dotted rectangle can be grouped into one document, but the
references to organizations, schools, and other users need to be represented as refer‐
ences, and require joins when queried.
Figure 2-4. Extending résumés with many-to-many relationships.
Relational Model Versus Document Model 
| 
35


Are Document Databases Repeating History?
While many-to-many relationships and joins are routinely used in relational data‐
bases, document databases and NoSQL reopened the debate on how best to represent
such relationships in a database. This debate is much older than NoSQL—in fact, it
goes back to the very earliest computerized database systems.
The most popular database for business data processing in the 1970s was IBM’s Infor‐
mation Management System (IMS), originally developed for stock-keeping in the
Apollo space program and first commercially released in 1968 [13]. It is still in use
and maintained today, running on OS/390 on IBM mainframes [14].
The design of IMS used a fairly simple data model called the hierarchical model,
which has some remarkable similarities to the JSON model used by document data‐
bases [2]. It represented all data as a tree of records nested within records, much like
the JSON structure of Figure 2-2.
Like document databases, IMS worked well for one-to-many relationships, but it
made many-to-many relationships difficult, and it didn’t support joins. Developers
had to decide whether to duplicate (denormalize) data or to manually resolve refer‐
ences from one record to another. These problems of the 1960s and ’70s were very
much like the problems that developers are running into with document databases
today [15].
Various solutions were proposed to solve the limitations of the hierarchical model.
The two most prominent were the relational model (which became SQL, and took
over the world) and the network model (which initially had a large following but
eventually faded into obscurity). The “great debate” between these two camps lasted
for much of the 1970s [2].
Since the problem that the two models were solving is still so relevant today, it’s
worth briefly revisiting this debate in today’s light.
The network model
The network model was standardized by a committee called the Conference on Data
Systems Languages (CODASYL) and implemented by several different database ven‐
dors; it is also known as the CODASYL model [16].
The CODASYL model was a generalization of the hierarchical model. In the tree
structure of the hierarchical model, every record has exactly one parent; in the net‐
work model, a record could have multiple parents. For example, there could be one
record for the "Greater Seattle Area" region, and every user who lived in that
region could be linked to it. This allowed many-to-one and many-to-many relation‐
ships to be modeled.
36 
| 
Chapter 2: Data Models and Query Languages


iv. Foreign key constraints allow you to restrict modifications, but such constraints are not required by the
relational model. Even with constraints, joins on foreign keys are performed at query time, whereas in
CODASYL, the join was effectively done at insert time.
The links between records in the network model were not foreign keys, but more like
pointers in a programming language (while still being stored on disk). The only way
of accessing a record was to follow a path from a root record along these chains of
links. This was called an access path.
In the simplest case, an access path could be like the traversal of a linked list: start at
the head of the list, and look at one record at a time until you find the one you want.
But in a world of many-to-many relationships, several different paths can lead to the
same record, and a programmer working with the network model had to keep track
of these different access paths in their head.
A query in CODASYL was performed by moving a cursor through the database by
iterating over lists of records and following access paths. If a record had multiple
parents (i.e., multiple incoming pointers from other records), the application code
had to keep track of all the various relationships. Even CODASYL committee mem‐
bers admitted that this was like navigating around an n-dimensional data space [17].
Although manual access path selection was able to make the most efficient use of the
very limited hardware capabilities in the 1970s (such as tape drives, whose seeks are
extremely slow), the problem was that they made the code for querying and updating
the database complicated and inflexible. With both the hierarchical and the network
model, if you didn’t have a path to the data you wanted, you were in a difficult situa‐
tion. You could change the access paths, but then you had to go through a lot of
handwritten database query code and rewrite it to handle the new access paths. It was
difficult to make changes to an application’s data model.
The relational model
What the relational model did, by contrast, was to lay out all the data in the open: a
relation (table) is simply a collection of tuples (rows), and that’s it. There are no laby‐
rinthine nested structures, no complicated access paths to follow if you want to look
at the data. You can read any or all of the rows in a table, selecting those that match
an arbitrary condition. You can read a particular row by designating some columns
as a key and matching on those. You can insert a new row into any table without
worrying about foreign key relationships to and from other tables.iv
In a relational database, the query optimizer automatically decides which parts of the
query to execute in which order, and which indexes to use. Those choices are effec‐
tively the “access path,” but the big difference is that they are made automatically by
Relational Model Versus Document Model 
| 
37


the query optimizer, not by the application developer, so we rarely need to think
about them.
If you want to query your data in new ways, you can just declare a new index, and
queries will automatically use whichever indexes are most appropriate. You don’t
need to change your queries to take advantage of a new index. (See also “Query Lan‐
guages for Data” on page 42.) The relational model thus made it much easier to add
new features to applications.
Query optimizers for relational databases are complicated beasts, and they have con‐
sumed many years of research and development effort [18]. But a key insight of the
relational model was this: you only need to build a query optimizer once, and then all
applications that use the database can benefit from it. If you don’t have a query opti‐
mizer, it’s easier to handcode the access paths for a particular query than to write a
general-purpose optimizer—but the general-purpose solution wins in the long run.
Comparison to document databases
Document databases reverted back to the hierarchical model in one aspect: storing
nested records (one-to-many relationships, like positions, education, and
contact_info in Figure 2-1) within their parent record rather than in a separate
table.
However, when it comes to representing many-to-one and many-to-many relation‐
ships, relational and document databases are not fundamentally different: in both
cases, the related item is referenced by a unique identifier, which is called a foreign
key in the relational model and a document reference in the document model [9].
That identifier is resolved at read time by using a join or follow-up queries. To date,
document databases have not followed the path of CODASYL.
Relational Versus Document Databases Today
There are many differences to consider when comparing relational databases to
document databases, including their fault-tolerance properties (see Chapter 5) and
handling of concurrency (see Chapter 7). In this chapter, we will concentrate only on
the differences in the data model.
The main arguments in favor of the document data model are schema flexibility, bet‐
ter performance due to locality, and that for some applications it is closer to the data
structures used by the application. The relational model counters by providing better
support for joins, and many-to-one and many-to-many relationships.
Which data model leads to simpler application code?
If the data in your application has a document-like structure (i.e., a tree of one-tomany relationships, where typically the entire tree is loaded at once), then it’s proba‐
38 
| 
Chapter 2: Data Models and Query Languages


bly a good idea to use a document model. The relational technique of shredding—
splitting a document-like structure into multiple tables (like positions, education,
and contact_info in Figure 2-1)—can lead to cumbersome schemas and unnecessa‐
rily complicated application code.
The document model has limitations: for example, you cannot refer directly to a nes‐
ted item within a document, but instead you need to say something like “the second
item in the list of positions for user 251” (much like an access path in the hierarchical
model). However, as long as documents are not too deeply nested, that is not usually
a problem.
The poor support for joins in document databases may or may not be a problem,
depending on the application. For example, many-to-many relationships may never
be needed in an analytics application that uses a document database to record which
events occurred at which time [19].
However, if your application does use many-to-many relationships, the document
model becomes less appealing. It’s possible to reduce the need for joins by denormal‐
izing, but then the application code needs to do additional work to keep the denor‐
malized data consistent. Joins can be emulated in application code by making
multiple requests to the database, but that also moves complexity into the application
and is usually slower than a join performed by specialized code inside the database.
In such cases, using a document model can lead to significantly more complex appli‐
cation code and worse performance [15].
It’s not possible to say in general which data model leads to simpler application code;
it depends on the kinds of relationships that exist between data items. For highly
interconnected data, the document model is awkward, the relational model is accept‐
able, and graph models (see “Graph-Like Data Models” on page 49) are the most
natural.
Schema flexibility in the document model
Most document databases, and the JSON support in relational databases, do not
enforce any schema on the data in documents. XML support in relational databases
usually comes with optional schema validation. No schema means that arbitrary keys
and values can be added to a document, and when reading, clients have no guaran‐
tees as to what fields the documents may contain.
Document databases are sometimes called schemaless, but that’s misleading, as the
code that reads the data usually assumes some kind of structure—i.e., there is an
implicit schema, but it is not enforced by the database [20]. A more accurate term is
schema-on-read (the structure of the data is implicit, and only interpreted when the
data is read), in contrast with schema-on-write (the traditional approach of relational
Relational Model Versus Document Model 
| 
39


databases, where the schema is explicit and the database ensures all written data con‐
forms to it) [21].
Schema-on-read is similar to dynamic (runtime) type checking in programming lan‐
guages, whereas schema-on-write is similar to static (compile-time) type checking.
Just as the advocates of static and dynamic type checking have big debates about their
relative merits [22], enforcement of schemas in database is a contentious topic, and in
general there’s no right or wrong answer.
The difference between the approaches is particularly noticeable in situations where
an application wants to change the format of its data. For example, say you are cur‐
rently storing each user’s full name in one field, and you instead want to store the
first name and last name separately [23]. In a document database, you would just
start writing new documents with the new fields and have code in the application that
handles the case when old documents are read. For example:
if (user && user.name && !user.first_name) {
    // Documents written before Dec 8, 2013 don't have first_name
    user.first_name = user.name.split(" ")[0];
}
On the other hand, in a “statically typed” database schema, you would typically per‐
form a migration along the lines of:
ALTER TABLE users ADD COLUMN first_name text;
UPDATE users SET first_name = split_part(name, ' ', 1);      -- PostgreSQL
UPDATE users SET first_name = substring_index(name, ' ', 1);      -- MySQL
Schema changes have a bad reputation of being slow and requiring downtime. This
reputation is not entirely deserved: most relational database systems execute the
ALTER TABLE statement in a few milliseconds. MySQL is a notable exception—it
copies the entire table on ALTER TABLE, which can mean minutes or even hours of
downtime when altering a large table—although various tools exist to work around
this limitation [24, 25, 26].
Running the UPDATE statement on a large table is likely to be slow on any database,
since every row needs to be rewritten. If that is not acceptable, the application can
leave first_name set to its default of NULL and fill it in at read time, like it would with
a document database.
The schema-on-read approach is advantageous if the items in the collection don’t all
have the same structure for some reason (i.e., the data is heterogeneous)—for exam‐
ple, because:
• There are many different types of objects, and it is not practical to put each type
of object in its own table.
40 
| 
Chapter 2: Data Models and Query Languages


• The structure of the data is determined by external systems over which you have
no control and which may change at any time.
In situations like these, a schema may hurt more than it helps, and schemaless docu‐
ments can be a much more natural data model. But in cases where all records are
expected to have the same structure, schemas are a useful mechanism for document‐
ing and enforcing that structure. We will discuss schemas and schema evolution in
more detail in Chapter 4.
Data locality for queries
A document is usually stored as a single continuous string, encoded as JSON, XML,
or a binary variant thereof (such as MongoDB’s BSON). If your application often
needs to access the entire document (for example, to render it on a web page), there is
a performance advantage to this storage locality. If data is split across multiple tables,
like in Figure 2-1, multiple index lookups are required to retrieve it all, which may
require more disk seeks and take more time.
The locality advantage only applies if you need large parts of the document at the
same time. The database typically needs to load the entire document, even if you
access only a small portion of it, which can be wasteful on large documents. On
updates to a document, the entire document usually needs to be rewritten—only
modifications that don’t change the encoded size of a document can easily be per‐
formed in place [19]. For these reasons, it is generally recommended that you keep
documents fairly small and avoid writes that increase the size of a document [9].
These performance limitations significantly reduce the set of situations in which
document databases are useful.
It’s worth pointing out that the idea of grouping related data together for locality is
not limited to the document model. For example, Google’s Spanner database offers
the same locality properties in a relational data model, by allowing the schema to
declare that a table’s rows should be interleaved (nested) within a parent table [27].
Oracle allows the same, using a feature called multi-table index cluster tables [28].
The column-family concept in the Bigtable data model (used in Cassandra and
HBase) has a similar purpose of managing locality [29].
We will also see more on locality in Chapter 3.
Convergence of document and relational databases
Most relational database systems (other than MySQL) have supported XML since the
mid-2000s. This includes functions to make local modifications to XML documents
and the ability to index and query inside XML documents, which allows applications
to use data models very similar to what they would do when using a document data‐
base.
Relational Model Versus Document Model 
| 
41


v. Codd’s original description of the relational model [1] actually allowed something quite similar to JSON
documents within a relational schema. He called it nonsimple domains. The idea was that a value in a row
doesn’t have to just be a primitive datatype like a number or a string, but could also be a nested relation
(table)—so you can have an arbitrarily nested tree structure as a value, much like the JSON or XML support
that was added to SQL over 30 years later.
PostgreSQL since version 9.3 [8], MySQL since version 5.7, and IBM DB2 since ver‐
sion 10.5 [30] also have a similar level of support for JSON documents. Given the
popularity of JSON for web APIs, it is likely that other relational databases will follow
in their footsteps and add JSON support.
On the document database side, RethinkDB supports relational-like joins in its query
language, and some MongoDB drivers automatically resolve database references
(effectively performing a client-side join, although this is likely to be slower than a
join performed in the database since it requires additional network round-trips and is
less optimized).
It seems that relational and document databases are becoming more similar over
time, and that is a good thing: the data models complement each other.v If a database
is able to handle document-like data and also perform relational queries on it, appli‐
cations can use the combination of features that best fits their needs.
A hybrid of the relational and document models is a good route for databases to take
in the future. 
Query Languages for Data
When the relational model was introduced, it included a new way of querying data:
SQL is a declarative query language, whereas IMS and CODASYL queried the data‐
base using imperative code. What does that mean?
Many commonly used programming languages are imperative. For example, if you
have a list of animal species, you might write something like this to return only the
sharks in the list:
function getSharks() {
    var sharks = [];
    for (var i = 0; i < animals.length; i++) {
        if (animals[i].family === "Sharks") {
            sharks.push(animals[i]);
        }
    }
    return sharks;
}
In the relational algebra, you would instead write:
sharks  =  σfamily = “Sharks” (animals)
42 
| 
Chapter 2: Data Models and Query Languages


where σ (the Greek letter sigma) is the selection operator, returning only those ani‐
mals that match the condition family = “Sharks”.
When SQL was defined, it followed the structure of the relational algebra fairly
closely:
SELECT * FROM animals WHERE family = 'Sharks';
An imperative language tells the computer to perform certain operations in a certain
order. You can imagine stepping through the code line by line, evaluating conditions,
updating variables, and deciding whether to go around the loop one more time.
In a declarative query language, like SQL or relational algebra, you just specify the
pattern of the data you want—what conditions the results must meet, and how you
want the data to be transformed (e.g., sorted, grouped, and aggregated)—but not how
to achieve that goal. It is up to the database system’s query optimizer to decide which
indexes and which join methods to use, and in which order to execute various parts
of the query.
A declarative query language is attractive because it is typically more concise and eas‐
ier to work with than an imperative API. But more importantly, it also hides imple‐
mentation details of the database engine, which makes it possible for the database
system to introduce performance improvements without requiring any changes to
queries.
For example, in the imperative code shown at the beginning of this section, the list of
animals appears in a particular order. If the database wants to reclaim unused disk
space behind the scenes, it might need to move records around, changing the order in
which the animals appear. Can the database do that safely, without breaking queries?
The SQL example doesn’t guarantee any particular ordering, and so it doesn’t mind if
the order changes. But if the query is written as imperative code, the database can
never be sure whether the code is relying on the ordering or not. The fact that SQL is
more limited in functionality gives the database much more room for automatic opti‐
mizations.
Finally, declarative languages often lend themselves to parallel execution. Today,
CPUs are getting faster by adding more cores, not by running at significantly higher
clock speeds than before [31]. Imperative code is very hard to parallelize across mul‐
tiple cores and multiple machines, because it specifies instructions that must be per‐
formed in a particular order. Declarative languages have a better chance of getting
faster in parallel execution because they specify only the pattern of the results, not the
algorithm that is used to determine the results. The database is free to use a parallel
implementation of the query language, if appropriate [32].
Query Languages for Data 
| 
43


Declarative Queries on the Web
The advantages of declarative query languages are not limited to just databases. To
illustrate the point, let’s compare declarative and imperative approaches in a com‐
pletely different environment: a web browser.
Say you have a website about animals in the ocean. The user is currently viewing the
page on sharks, so you mark the navigation item “Sharks” as currently selected, like
this:
<ul>
    <li class="selected"> 
        <p>Sharks</p> 
        <ul>
            <li>Great White Shark</li>
            <li>Tiger Shark</li>
            <li>Hammerhead Shark</li>
        </ul>
    </li>
    <li>
        <p>Whales</p>
        <ul>
            <li>Blue Whale</li>
            <li>Humpback Whale</li>
            <li>Fin Whale</li>
        </ul>
    </li>
</ul>
The selected item is marked with the CSS class "selected".
<p>Sharks</p> is the title of the currently selected page.
Now say you want the title of the currently selected page to have a blue background,
so that it is visually highlighted. This is easy, using CSS:
li.selected > p {
    background-color: blue;
}
Here the CSS selector li.selected > p declares the pattern of elements to which we
want to apply the blue style: namely, all <p> elements whose direct parent is an <li>
element with a CSS class of selected. The element <p>Sharks</p> in the example
matches this pattern, but <p>Whales</p> does not match because its <li> parent
lacks class="selected".
44 
| 
Chapter 2: Data Models and Query Languages


If you were using XSL instead of CSS, you could do something similar:
<xsl:template match="li[@class='selected']/p">
    <fo:block background-color="blue">
        <xsl:apply-templates/>
    </fo:block>
</xsl:template>
Here, the XPath expression li[@class='selected']/p is equivalent to the CSS selec‐
tor li.selected > p in the previous example. What CSS and XSL have in common
is that they are both declarative languages for specifying the styling of a document.
Imagine what life would be like if you had to use an imperative approach. In Java‐
Script, using the core Document Object Model (DOM) API, the result might look
something like this:
var liElements = document.getElementsByTagName("li");
for (var i = 0; i < liElements.length; i++) {
    if (liElements[i].className === "selected") {
        var children = liElements[i].childNodes;
        for (var j = 0; j < children.length; j++) {
            var child = children[j];
            if (child.nodeType === Node.ELEMENT_NODE && child.tagName === "P") {
                child.setAttribute("style", "background-color: blue");
            }
        }
    }
}
This JavaScript imperatively sets the element <p>Sharks</p> to have a blue back‐
ground, but the code is awful. Not only is it much longer and harder to understand
than the CSS and XSL equivalents, but it also has some serious problems:
• If the selected class is removed (e.g., because the user clicks a different page),
the blue color won’t be removed, even if the code is rerun—and so the item will
remain highlighted until the entire page is reloaded. With CSS, the browser auto‐
matically detects when the li.selected > p rule no longer applies and removes
the blue background as soon as the selected class is removed.
• If you want to take advantage of a new API, such as document.getElementsBy
ClassName("selected") or even document.evaluate()—which may improve
performance—you have to rewrite the code. On the other hand, browser vendors
can improve the performance of CSS and XPath without breaking compatibility.
Query Languages for Data 
| 
45


vi. IMS and CODASYL both used imperative query APIs. Applications typically used COBOL code to iterate
over records in the database, one record at a time [2, 16].
In a web browser, using declarative CSS styling is much better than manipulating
styles imperatively in JavaScript. Similarly, in databases, declarative query languages
like SQL turned out to be much better than imperative query APIs.vi
MapReduce Querying
MapReduce is a programming model for processing large amounts of data in bulk
across many machines, popularized by Google [33]. A limited form of MapReduce is
supported by some NoSQL datastores, including MongoDB and CouchDB, as a
mechanism for performing read-only queries across many documents.
MapReduce in general is described in more detail in Chapter 10. For now, we’ll just
briefly discuss MongoDB’s use of the model.
MapReduce is neither a declarative query language nor a fully imperative query API,
but somewhere in between: the logic of the query is expressed with snippets of code,
which are called repeatedly by the processing framework. It is based on the map (also
known as collect) and reduce (also known as fold or inject) functions that exist
in many functional programming languages.
To give an example, imagine you are a marine biologist, and you add an observation
record to your database every time you see animals in the ocean. Now you want to
generate a report saying how many sharks you have sighted per month.
In PostgreSQL you might express that query like this:
SELECT date_trunc('month', observation_timestamp) AS observation_month, 
       sum(num_animals) AS total_animals
FROM observations
WHERE family = 'Sharks'
GROUP BY observation_month;
The date_trunc('month', timestamp) function determines the calendar month
containing timestamp, and returns another timestamp representing the begin‐
ning of that month. In other words, it rounds a timestamp down to the nearest
month.
This query first filters the observations to only show species in the Sharks family,
then groups the observations by the calendar month in which they occurred, and
finally adds up the number of animals seen in all observations in that month.
The same can be expressed with MongoDB’s MapReduce feature as follows:
46 
| 
Chapter 2: Data Models and Query Languages


db.observations.mapReduce(
    function map() { 
        var year  = this.observationTimestamp.getFullYear();
        var month = this.observationTimestamp.getMonth() + 1;
        emit(year + "-" + month, this.numAnimals); 
    },
    function reduce(key, values) { 
        return Array.sum(values); 
    },
    {
        query: { family: "Sharks" }, 
        out: "monthlySharkReport" 
    }
);
The filter to consider only shark species can be specified declaratively (this is a
MongoDB-specific extension to MapReduce).
The JavaScript function map is called once for every document that matches
query, with this set to the document object.
The map function emits a key (a string consisting of year and month, such as
"2013-12" or "2014-1") and a value (the number of animals in that observation).
The key-value pairs emitted by map are grouped by key. For all key-value pairs
with the same key (i.e., the same month and year), the reduce function is called
once.
The reduce function adds up the number of animals from all observations in a
particular month.
The final output is written to the collection monthlySharkReport.
For example, say the observations collection contains these two documents:
{
    observationTimestamp: Date.parse("Mon, 25 Dec 1995 12:34:56 GMT"),
    family:     "Sharks",
    species:    "Carcharodon carcharias",
    numAnimals: 3
}
{
    observationTimestamp: Date.parse("Tue, 12 Dec 1995 16:17:18 GMT"),
    family:     "Sharks",
    species:    "Carcharias taurus",
    numAnimals: 4
}
Query Languages for Data 
| 
47


The map function would be called once for each document, resulting in
emit("1995-12", 3) and emit("1995-12", 4). Subsequently, the reduce function
would be called with reduce("1995-12", [3, 4]), returning 7.
The map and reduce functions are somewhat restricted in what they are allowed to
do. They must be pure functions, which means they only use the data that is passed to
them as input, they cannot perform additional database queries, and they must not
have any side effects. These restrictions allow the database to run the functions any‐
where, in any order, and rerun them on failure. However, they are nevertheless pow‐
erful: they can parse strings, call library functions, perform calculations, and more.
MapReduce is a fairly low-level programming model for distributed execution on a
cluster of machines. Higher-level query languages like SQL can be implemented as a
pipeline of MapReduce operations (see Chapter 10), but there are also many dis‐
tributed implementations of SQL that don’t use MapReduce. Note there is nothing in
SQL that constrains it to running on a single machine, and MapReduce doesn’t have
a monopoly on distributed query execution.
Being able to use JavaScript code in the middle of a query is a great feature for
advanced queries, but it’s not limited to MapReduce—some SQL databases can be
extended with JavaScript functions too [34].
A usability problem with MapReduce is that you have to write two carefully coordi‐
nated JavaScript functions, which is often harder than writing a single query. More‐
over, a declarative query language offers more opportunities for a query optimizer to
improve the performance of a query. For these reasons, MongoDB 2.2 added support
for a declarative query language called the aggregation pipeline [9]. In this language,
the same shark-counting query looks like this:
db.observations.aggregate([
    { $match: { family: "Sharks" } },
    { $group: {
        _id: {
            year:  { $year:  "$observationTimestamp" },
            month: { $month: "$observationTimestamp" }
        },
        totalAnimals: { $sum: "$numAnimals" }
    } }
]);
The aggregation pipeline language is similar in expressiveness to a subset of SQL, but
it uses a JSON-based syntax rather than SQL’s English-sentence-style syntax; the dif‐
ference is perhaps a matter of taste. The moral of the story is that a NoSQL system
may find itself accidentally reinventing SQL, albeit in disguise. 
48 
| 
Chapter 2: Data Models and Query Languages


Graph-Like Data Models
We saw earlier that many-to-many relationships are an important distinguishing fea‐
ture between different data models. If your application has mostly one-to-many rela‐
tionships (tree-structured data) or no relationships between records, the document
model is appropriate.
But what if many-to-many relationships are very common in your data? The rela‐
tional model can handle simple cases of many-to-many relationships, but as the con‐
nections within your data become more complex, it becomes more natural to start
modeling your data as a graph.
A graph consists of two kinds of objects: vertices (also known as nodes or entities) and
edges (also known as relationships or arcs). Many kinds of data can be modeled as a
graph. Typical examples include:
Social graphs
Vertices are people, and edges indicate which people know each other.
The web graph
Vertices are web pages, and edges indicate HTML links to other pages.
Road or rail networks
Vertices are junctions, and edges represent the roads or railway lines between
them.
Well-known algorithms can operate on these graphs: for example, car navigation sys‐
tems search for the shortest path between two points in a road network, and
PageRank can be used on the web graph to determine the popularity of a web page
and thus its ranking in search results.
In the examples just given, all the vertices in a graph represent the same kind of thing
(people, web pages, or road junctions, respectively). However, graphs are not limited
to such homogeneous data: an equally powerful use of graphs is to provide a consis‐
tent way of storing completely different types of objects in a single datastore. For
example, Facebook maintains a single graph with many different types of vertices and
edges: vertices represent people, locations, events, checkins, and comments made by
users; edges indicate which people are friends with each other, which checkin hap‐
pened in which location, who commented on which post, who attended which event,
and so on [35].
In this section we will use the example shown in Figure 2-5. It could be taken from a
social network or a genealogical database: it shows two people, Lucy from Idaho and
Alain from Beaune, France. They are married and living in London.
Graph-Like Data Models 
| 
49


Figure 2-5. Example of graph-structured data (boxes represent vertices, arrows repre‐
sent edges).
There are several different, but related, ways of structuring and querying data in
graphs. In this section we will discuss the property graph model (implemented by
Neo4j, Titan, and InfiniteGraph) and the triple-store model (implemented by
Datomic, AllegroGraph, and others). We will look at three declarative query lan‐
guages for graphs: Cypher, SPARQL, and Datalog. Besides these, there are also
imperative graph query languages such as Gremlin [36] and graph processing frame‐
works like Pregel (see Chapter 10).
Property Graphs
In the property graph model, each vertex consists of:
• A unique identifier
• A set of outgoing edges
• A set of incoming edges
• A collection of properties (key-value pairs)
Each edge consists of:
• A unique identifier
• The vertex at which the edge starts (the tail vertex)
50 
| 
Chapter 2: Data Models and Query Languages


• The vertex at which the edge ends (the head vertex)
• A label to describe the kind of relationship between the two vertices
• A collection of properties (key-value pairs)
You can think of a graph store as consisting of two relational tables, one for vertices
and one for edges, as shown in Example 2-2 (this schema uses the PostgreSQL json
datatype to store the properties of each vertex or edge). The head and tail vertex are
stored for each edge; if you want the set of incoming or outgoing edges for a vertex,
you can query the edges table by head_vertex or tail_vertex, respectively.
Example 2-2. Representing a property graph using a relational schema
CREATE TABLE vertices (
    vertex_id   integer PRIMARY KEY,
    properties  json
);
CREATE TABLE edges (
    edge_id     integer PRIMARY KEY,
    tail_vertex integer REFERENCES vertices (vertex_id),
    head_vertex integer REFERENCES vertices (vertex_id),
    label       text,
    properties  json
);
CREATE INDEX edges_tails ON edges (tail_vertex);
CREATE INDEX edges_heads ON edges (head_vertex);
Some important aspects of this model are:
1. Any vertex can have an edge connecting it with any other vertex. There is no
schema that restricts which kinds of things can or cannot be associated.
2. Given any vertex, you can efficiently find both its incoming and its outgoing
edges, and thus traverse the graph—i.e., follow a path through a chain of vertices
—both forward and backward. (That’s why Example 2-2 has indexes on both the
tail_vertex and head_vertex columns.)
3. By using different labels for different kinds of relationships, you can store several
different kinds of information in a single graph, while still maintaining a clean
data model.
Those features give graphs a great deal of flexibility for data modeling, as illustrated
in Figure 2-5. The figure shows a few things that would be difficult to express in a
traditional relational schema, such as different kinds of regional structures in differ‐
ent countries (France has départements and régions, whereas the US has counties and
states), quirks of history such as a country within a country (ignoring for now the
Graph-Like Data Models 
| 
51


intricacies of sovereign states and nations), and varying granularity of data (Lucy’s
current residence is specified as a city, whereas her place of birth is specified only at
the level of a state).
You could imagine extending the graph to also include many other facts about Lucy
and Alain, or other people. For instance, you could use it to indicate any food aller‐
gies they have (by introducing a vertex for each allergen, and an edge between a per‐
son and an allergen to indicate an allergy), and link the allergens with a set of vertices
that show which foods contain which substances. Then you could write a query to
find out what is safe for each person to eat. Graphs are good for evolvability: as you
add features to your application, a graph can easily be extended to accommodate
changes in your application’s data structures.
The Cypher Query Language
Cypher is a declarative query language for property graphs, created for the Neo4j
graph database [37]. (It is named after a character in the movie The Matrix and is not
related to ciphers in cryptography [38].)
Example 2-3 shows the Cypher query to insert the lefthand portion of Figure 2-5 into
a graph database. The rest of the graph can be added similarly and is omitted for
readability. Each vertex is given a symbolic name like USA or Idaho, and other parts of
the query can use those names to create edges between the vertices, using an arrow
notation: (Idaho) -[:WITHIN]-> (USA) creates an edge labeled WITHIN, with Idaho
as the tail node and USA as the head node.
Example 2-3. A subset of the data in Figure 2-5, represented as a Cypher query
CREATE
  (NAmerica:Location {name:'North America', type:'continent'}),
  (USA:Location      {name:'United States', type:'country'  }),
  (Idaho:Location    {name:'Idaho',         type:'state'    }),
  (Lucy:Person       {name:'Lucy' }),
  (Idaho) -[:WITHIN]->  (USA)  -[:WITHIN]-> (NAmerica),
  (Lucy)  -[:BORN_IN]-> (Idaho)
When all the vertices and edges of Figure 2-5 are added to the database, we can start
asking interesting questions: for example, find the names of all the people who emigra‐
ted from the United States to Europe. To be more precise, here we want to find all the
vertices that have a BORN_IN edge to a location within the US, and also a LIVING_IN
edge to a location within Europe, and return the name property of each of those verti‐
ces.
Example 2-4 shows how to express that query in Cypher. The same arrow notation is
used in a MATCH clause to find patterns in the graph: (person) -[:BORN_IN]-> ()
52 
| 
Chapter 2: Data Models and Query Languages


matches any two vertices that are related by an edge labeled BORN_IN. The tail vertex
of that edge is bound to the variable person, and the head vertex is left unnamed.
Example 2-4. Cypher query to find people who emigrated from the US to Europe
MATCH
  (person) -[:BORN_IN]->  () -[:WITHIN*0..]-> (us:Location {name:'United States'}),
  (person) -[:LIVES_IN]-> () -[:WITHIN*0..]-> (eu:Location {name:'Europe'})
RETURN person.name
The query can be read as follows:
Find any vertex (call it person) that meets both of the following conditions:
1. person has an outgoing BORN_IN edge to some vertex. From that vertex, you can
follow a chain of outgoing WITHIN edges until eventually you reach a vertex of
type Location, whose name property is equal to "United States".
2. That same person vertex also has an outgoing LIVES_IN edge. Following that
edge, and then a chain of outgoing WITHIN edges, you eventually reach a vertex of
type Location, whose name property is equal to "Europe".
For each such person vertex, return the name property.
There are several possible ways of executing the query. The description given here
suggests that you start by scanning all the people in the database, examine each per‐
son’s birthplace and residence, and return only those people who meet the criteria.
But equivalently, you could start with the two Location vertices and work backward.
If there is an index on the name property, you can probably efficiently find the two
vertices representing the US and Europe. Then you can proceed to find all locations
(states, regions, cities, etc.) in the US and Europe respectively by following all incom‐
ing WITHIN edges. Finally, you can look for people who can be found through an
incoming BORN_IN or LIVES_IN edge at one of the location vertices.
As is typical for a declarative query language, you don’t need to specify such execu‐
tion details when writing the query: the query optimizer automatically chooses the
strategy that is predicted to be the most efficient, so you can get on with writing the
rest of your application.
Graph Queries in SQL
Example 2-2 suggested that graph data can be represented in a relational database.
But if we put graph data in a relational structure, can we also query it using SQL?
The answer is yes, but with some difficulty. In a relational database, you usually know
in advance which joins you need in your query. In a graph query, you may need to
Graph-Like Data Models 
| 
53


traverse a variable number of edges before you find the vertex you’re looking for—
that is, the number of joins is not fixed in advance.
In our example, that happens in the () -[:WITHIN*0..]-> () rule in the Cypher
query. A person’s LIVES_IN edge may point at any kind of location: a street, a city, a
district, a region, a state, etc. A city may be WITHIN a region, a region WITHIN a state, a
state WITHIN a country, etc. The LIVES_IN edge may point directly at the location ver‐
tex you’re looking for, or it may be several levels removed in the location hierarchy.
In Cypher, :WITHIN*0.. expresses that fact very concisely: it means “follow a WITHIN
edge, zero or more times.” It is like the * operator in a regular expression.
Since SQL:1999, this idea of variable-length traversal paths in a query can be
expressed using something called recursive common table expressions (the WITH
RECURSIVE syntax). Example 2-5 shows the same query—finding the names of people
who emigrated from the US to Europe—expressed in SQL using this technique (sup‐
ported in PostgreSQL, IBM DB2, Oracle, and SQL Server). However, the syntax is
very clumsy in comparison to Cypher.
Example 2-5. The same query as Example 2-4, expressed in SQL using recursive
common table expressions
WITH RECURSIVE
  -- in_usa is the set of vertex IDs of all locations within the United States
  in_usa(vertex_id) AS (
      SELECT vertex_id FROM vertices WHERE properties->>'name' = 'United States' 
    UNION
      SELECT edges.tail_vertex FROM edges 
        JOIN in_usa ON edges.head_vertex = in_usa.vertex_id
        WHERE edges.label = 'within'
  ),
  -- in_europe is the set of vertex IDs of all locations within Europe
  in_europe(vertex_id) AS (
      SELECT vertex_id FROM vertices WHERE properties->>'name' = 'Europe' 
    UNION
      SELECT edges.tail_vertex FROM edges
        JOIN in_europe ON edges.head_vertex = in_europe.vertex_id
        WHERE edges.label = 'within'
  ),
  -- born_in_usa is the set of vertex IDs of all people born in the US
  born_in_usa(vertex_id) AS ( 
    SELECT edges.tail_vertex FROM edges
      JOIN in_usa ON edges.head_vertex = in_usa.vertex_id
      WHERE edges.label = 'born_in'
  ),
54 
| 
Chapter 2: Data Models and Query Languages


  -- lives_in_europe is the set of vertex IDs of all people living in Europe
  lives_in_europe(vertex_id) AS ( 
    SELECT edges.tail_vertex FROM edges
      JOIN in_europe ON edges.head_vertex = in_europe.vertex_id
      WHERE edges.label = 'lives_in'
  )
SELECT vertices.properties->>'name'
FROM vertices
-- join to find those people who were both born in the US *and* live in Europe
JOIN born_in_usa     ON vertices.vertex_id = born_in_usa.vertex_id 
JOIN lives_in_europe ON vertices.vertex_id = lives_in_europe.vertex_id;
First find the vertex whose name property has the value "United States", and
make it the first element of the set of vertices in_usa.
Follow all incoming within edges from vertices in the set in_usa, and add them
to the same set, until all incoming within edges have been visited.
Do the same starting with the vertex whose name property has the value
"Europe", and build up the set of vertices in_europe.
For each of the vertices in the set in_usa, follow incoming born_in edges to find
people who were born in some place within the United States.
Similarly, for each of the vertices in the set in_europe, follow incoming lives_in
edges to find people who live in Europe.
Finally, intersect the set of people born in the USA with the set of people living in
Europe, by joining them.
If the same query can be written in 4 lines in one query language but requires 29 lines
in another, that just shows that different data models are designed to satisfy different
use cases. It’s important to pick a data model that is suitable for your application.
Triple-Stores and SPARQL
The triple-store model is mostly equivalent to the property graph model, using differ‐
ent words to describe the same ideas. It is nevertheless worth discussing, because
there are various tools and languages for triple-stores that can be valuable additions
to your toolbox for building applications.
In a triple-store, all information is stored in the form of very simple three-part state‐
ments: (subject, predicate, object). For example, in the triple (Jim, likes, bananas), Jim
is the subject, likes is the predicate (verb), and bananas is the object.
Graph-Like Data Models 
| 
55


The subject of a triple is equivalent to a vertex in a graph. The object is one of two
things:
1. A value in a primitive datatype, such as a string or a number. In that case, the
predicate and object of the triple are equivalent to the key and value of a property
on the subject vertex. For example, (lucy, age, 33) is like a vertex lucy with prop‐
erties {"age":33}.
2. Another vertex in the graph. In that case, the predicate is an edge in the graph,
the subject is the tail vertex, and the object is the head vertex. For example, in
(lucy, marriedTo, alain) the subject and object lucy and alain are both vertices,
and the predicate marriedTo is the label of the edge that connects them.
Example 2-6 shows the same data as in Example 2-3, written as triples in a format
called Turtle, a subset of Notation3 (N3) [39].
Example 2-6. A subset of the data in Figure 2-5, represented as Turtle triples
@prefix : <urn:example:>.
_:lucy     a       :Person.
_:lucy     :name   "Lucy".
_:lucy     :bornIn _:idaho.
_:idaho    a       :Location.
_:idaho    :name   "Idaho".
_:idaho    :type   "state".
_:idaho    :within _:usa.
_:usa      a       :Location.
_:usa      :name   "United States".
_:usa      :type   "country".
_:usa      :within _:namerica.
_:namerica a       :Location.
_:namerica :name   "North America".
_:namerica :type   "continent".
In this example, vertices of the graph are written as _:someName. The name doesn’t
mean anything outside of this file; it exists only because we otherwise wouldn’t know
which triples refer to the same vertex. When the predicate represents an edge, the
object is a vertex, as in _:idaho :within _:usa. When the predicate is a property,
the object is a string literal, as in _:usa :name "United States".
It’s quite repetitive to repeat the same subject over and over again, but fortunately
you can use semicolons to say multiple things about the same subject. This makes the
Turtle format quite nice and readable: see Example 2-7.
56 
| 
Chapter 2: Data Models and Query Languages


vii. Technically, Datomic uses 5-tuples rather than triples; the two additional fields are metadata for version‐
ing.
Example 2-7. A more concise way of writing the data in Example 2-6
@prefix : <urn:example:>.
_:lucy     a :Person;   :name "Lucy";          :bornIn _:idaho.
_:idaho    a :Location; :name "Idaho";         :type "state";   :within _:usa.
_:usa      a :Location; :name "United States"; :type "country"; :within _:namerica.
_:namerica a :Location; :name "North America"; :type "continent".
The semantic web
If you read more about triple-stores, you may get sucked into a maelstrom of articles
written about the semantic web. The triple-store data model is completely independ‐
ent of the semantic web—for example, Datomic [40] is a triple-store that does not
claim to have anything to do with it.vii But since the two are so closely linked in many
people’s minds, we should discuss them briefly.
The semantic web is fundamentally a simple and reasonable idea: websites already
publish information as text and pictures for humans to read, so why don’t they also
publish information as machine-readable data for computers to read? The Resource
Description Framework (RDF) [41] was intended as a mechanism for different web‐
sites to publish data in a consistent format, allowing data from different websites to
be automatically combined into a web of data—a kind of internet-wide “database of
everything.”
Unfortunately, the semantic web was overhyped in the early 2000s but so far hasn’t
shown any sign of being realized in practice, which has made many people cynical
about it. It has also suffered from a dizzying plethora of acronyms, overly complex
standards proposals, and hubris.
However, if you look past those failings, there is also a lot of good work that has come
out of the semantic web project. Triples can be a good internal data model for appli‐
cations, even if you have no interest in publishing RDF data on the semantic web.
The RDF data model
The Turtle language we used in Example 2-7 is a human-readable format for RDF
data. Sometimes RDF is also written in an XML format, which does the same thing
much more verbosely—see Example 2-8. Turtle/N3 is preferable as it is much easier
on the eyes, and tools like Apache Jena [42] can automatically convert between differ‐
ent RDF formats if necessary.
Graph-Like Data Models 
| 
57


Example 2-8. The data of Example 2-7, expressed using RDF/XML syntax
<rdf:RDF xmlns="urn:example:"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <Location rdf:nodeID="idaho">
    <name>Idaho</name>
    <type>state</type>
    <within>
      <Location rdf:nodeID="usa">
        <name>United States</name>
        <type>country</type>
        <within>
          <Location rdf:nodeID="namerica">
            <name>North America</name>
            <type>continent</type>
          </Location>
        </within>
      </Location>
    </within>
  </Location>
  <Person rdf:nodeID="lucy">
    <name>Lucy</name>
    <bornIn rdf:nodeID="idaho"/>
  </Person>
</rdf:RDF>
RDF has a few quirks due to the fact that it is designed for internet-wide data
exchange. The subject, predicate, and object of a triple are often URIs. For example, a
predicate might be an URI such as <http://my-company.com/namespace#within> or
<http://my-company.com/namespace#lives_in>, rather than just WITHIN or
LIVES_IN. The reasoning behind this design is that you should be able to combine
your data with someone else’s data, and if they attach a different meaning to the word
within or lives_in, you won’t get a conflict because their predicates are actually
<http://other.org/foo#within> and <http://other.org/foo#lives_in>.
The URL <http://my-company.com/namespace> doesn’t necessarily need to resolve
to anything—from RDF’s point of view, it is simply a namespace. To avoid potential
confusion with http:// URLs, the examples in this section use non-resolvable URIs
such as urn:example:within. Fortunately, you can just specify this prefix once at the
top of the file, and then forget about it.
58 
| 
Chapter 2: Data Models and Query Languages


The SPARQL query language
SPARQL is a query language for triple-stores using the RDF data model [43]. (It is an
acronym for SPARQL Protocol and RDF Query Language, pronounced “sparkle.”) It
predates Cypher, and since Cypher’s pattern matching is borrowed from SPARQL,
they look quite similar [37].
The same query as before—finding people who have moved from the US to Europe—
is even more concise in SPARQL than it is in Cypher (see Example 2-9).
Example 2-9. The same query as Example 2-4, expressed in SPARQL
PREFIX : <urn:example:>
SELECT ?personName WHERE {
  ?person :name ?personName.
  ?person :bornIn  / :within* / :name "United States".
  ?person :livesIn / :within* / :name "Europe".
}
The structure is very similar. The following two expressions are equivalent (variables
start with a question mark in SPARQL):
(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (location)   # Cypher
?person :bornIn / :within* ?location.                   # SPARQL
Because RDF doesn’t distinguish between properties and edges but just uses predi‐
cates for both, you can use the same syntax for matching properties. In the following
expression, the variable usa is bound to any vertex that has a name property whose
value is the string "United States":
(usa {name:'United States'})   # Cypher
?usa :name "United States".    # SPARQL
SPARQL is a nice query language—even if the semantic web never happens, it can be
a powerful tool for applications to use internally. 
Graph-Like Data Models 
| 
59


viii. Datomic and Cascalog use a Clojure S-expression syntax for Datalog. In the following examples we use a
Prolog syntax, which is a little easier to read, but this makes no functional difference.
Graph Databases Compared to the Network Model
In “Are Document Databases Repeating History?” on page 36 we discussed how
CODASYL and the relational model competed to solve the problem of many-tomany relationships in IMS. At first glance, CODASYL’s network model looks similar
to the graph model. Are graph databases the second coming of CODASYL in
disguise?
No. They differ in several important ways:
• In CODASYL, a database had a schema that specified which record type could be
nested within which other record type. In a graph database, there is no such
restriction: any vertex can have an edge to any other vertex. This gives much
greater flexibility for applications to adapt to changing requirements.
• In CODASYL, the only way to reach a particular record was to traverse one of
the access paths to it. In a graph database, you can refer directly to any vertex by
its unique ID, or you can use an index to find vertices with a particular value.
• In CODASYL, the children of a record were an ordered set, so the database had
to maintain that ordering (which had consequences for the storage layout) and
applications that inserted new records into the database had to worry about the
positions of the new records in these sets. In a graph database, vertices and edges
are not ordered (you can only sort the results when making a query).
• In CODASYL, all queries were imperative, difficult to write and easily broken by
changes in the schema. In a graph database, you can write your traversal in
imperative code if you want to, but most graph databases also support high-level,
declarative query languages such as Cypher or SPARQL.
The Foundation: Datalog
Datalog is a much older language than SPARQL or Cypher, having been studied
extensively by academics in the 1980s [44, 45, 46]. It is less well known among soft‐
ware engineers, but it is nevertheless important, because it provides the foundation
that later query languages build upon.
In practice, Datalog is used in a few data systems: for example, it is the query lan‐
guage of Datomic [40], and Cascalog [47] is a Datalog implementation for querying
large datasets in Hadoop.viii
60 
| 
Chapter 2: Data Models and Query Languages


Datalog’s data model is similar to the triple-store model, generalized a bit. Instead of
writing a triple as (subject, predicate, object), we write it as predicate(subject, object).
Example 2-10 shows how to write the data from our example in Datalog.
Example 2-10. A subset of the data in Figure 2-5, represented as Datalog facts
name(namerica, 'North America').
type(namerica, continent).
name(usa, 'United States').
type(usa, country).
within(usa, namerica).
name(idaho, 'Idaho').
type(idaho, state).
within(idaho, usa).
name(lucy, 'Lucy').
born_in(lucy, idaho).
Now that we have defined the data, we can write the same query as before, as shown
in Example 2-11. It looks a bit different from the equivalent in Cypher or SPARQL,
but don’t let that put you off. Datalog is a subset of Prolog, which you might have
seen before if you’ve studied computer science.
Example 2-11. The same query as Example 2-4, expressed in Datalog
within_recursive(Location, Name) :- name(Location, Name).     /* Rule 1 */
within_recursive(Location, Name) :- within(Location, Via),    /* Rule 2 */
                                    within_recursive(Via, Name).
migrated(Name, BornIn, LivingIn) :- name(Person, Name),       /* Rule 3 */
                                    born_in(Person, BornLoc),
                                    within_recursive(BornLoc, BornIn),
                                    lives_in(Person, LivingLoc),
                                    within_recursive(LivingLoc, LivingIn).
?- migrated(Who, 'United States', 'Europe').
/* Who = 'Lucy'. */
Cypher and SPARQL jump in right away with SELECT, but Datalog takes a small step
at a time. We define rules that tell the database about new predicates: here, we define
two new predicates, within_recursive and migrated. These predicates aren’t triples
stored in the database, but instead they are derived from data or from other rules.
Rules can refer to other rules, just like functions can call other functions or recur‐
sively call themselves. Like this, complex queries can be built up a small piece at a
time.
Graph-Like Data Models 
| 
61


In rules, words that start with an uppercase letter are variables, and predicates are
matched like in Cypher and SPARQL. For example, name(Location, Name) matches
the triple name(namerica, 'North America') with variable bindings Location =
namerica and Name = 'North America'.
A rule applies if the system can find a match for all predicates on the righthand side
of the :- operator. When the rule applies, it’s as though the lefthand side of the :-
was added to the database (with variables replaced by the values they matched).
One possible way of applying the rules is thus:
1. name(namerica, 'North America') exists in the database, so rule 1 applies. It
generates within_recursive(namerica, 'North America').
2. within(usa, namerica) exists in the database and the previous step generated
within_recursive(namerica, 'North America'), so rule 2 applies. It generates
within_recursive(usa, 'North America').
3. within(idaho, usa) exists in the database and the previous step generated
within_recursive(usa, 'North America'), so rule 2 applies. It generates
within_recursive(idaho, 'North America').
By repeated application of rules 1 and 2, the within_recursive predicate can tell us
all the locations in North America (or any other location name) contained in our
database. This process is illustrated in Figure 2-6.
Figure 2-6. Determining that Idaho is in North America, using the Datalog rules from
Example 2-11.
Now rule 3 can find people who were born in some location BornIn and live in some
location LivingIn. By querying with BornIn = 'United States' and LivingIn =
'Europe', and leaving the person as a variable Who, we ask the Datalog system to find
out which values can appear for the variable Who. So, finally we get the same answer as
in the earlier Cypher and SPARQL queries.
62 
| 
Chapter 2: Data Models and Query Languages


The Datalog approach requires a different kind of thinking to the other query lan‐
guages discussed in this chapter, but it’s a very powerful approach, because rules can
be combined and reused in different queries. It’s less convenient for simple one-off
queries, but it can cope better if your data is complex. 
Summary
Data models are a huge subject, and in this chapter we have taken a quick look at a
broad variety of different models. We didn’t have space to go into all the details of
each model, but hopefully the overview has been enough to whet your appetite to
find out more about the model that best fits your application’s requirements.
Historically, data started out being represented as one big tree (the hierarchical
model), but that wasn’t good for representing many-to-many relationships, so the
relational model was invented to solve that problem. More recently, developers found
that some applications don’t fit well in the relational model either. New nonrelational
“NoSQL” datastores have diverged in two main directions:
1. Document databases target use cases where data comes in self-contained docu‐
ments and relationships between one document and another are rare.
2. Graph databases go in the opposite direction, targeting use cases where anything
is potentially related to everything.
All three models (document, relational, and graph) are widely used today, and each is
good in its respective domain. One model can be emulated in terms of another model
—for example, graph data can be represented in a relational database—but the result
is often awkward. That’s why we have different systems for different purposes, not a
single one-size-fits-all solution.
One thing that document and graph databases have in common is that they typically
don’t enforce a schema for the data they store, which can make it easier to adapt
applications to changing requirements. However, your application most likely still
assumes that data has a certain structure; it’s just a question of whether the schema is
explicit (enforced on write) or implicit (handled on read).
Each data model comes with its own query language or framework, and we discussed
several examples: SQL, MapReduce, MongoDB’s aggregation pipeline, Cypher,
SPARQL, and Datalog. We also touched on CSS and XSL/XPath, which aren’t data‐
base query languages but have interesting parallels.
Although we have covered a lot of ground, there are still many data models left
unmentioned. To give just a few brief examples:
• Researchers working with genome data often need to perform sequencesimilarity searches, which means taking one very long string (representing a
Summary 
| 
63


DNA molecule) and matching it against a large database of strings that are simi‐
lar, but not identical. None of the databases described here can handle this kind
of usage, which is why researchers have written specialized genome database
software like GenBank [48].
• Particle physicists have been doing Big Data–style large-scale data analysis for
decades, and projects like the Large Hadron Collider (LHC) now work with hun‐
dreds of petabytes! At such a scale custom solutions are required to stop the
hardware cost from spiraling out of control [49].
• Full-text search is arguably a kind of data model that is frequently used alongside
databases. Information retrieval is a large specialist subject that we won’t cover in
great detail in this book, but we’ll touch on search indexes in Chapter 3 and
Part III.
We have to leave it there for now. In the next chapter we will discuss some of the
trade-offs that come into play when implementing the data models described in this
chapter. 
References
[1] Edgar F. Codd: “A Relational Model of Data for Large Shared Data Banks,” Com‐
munications of the ACM, volume 13, number 6, pages 377–387, June 1970. doi:
10.1145/362384.362685
[2] Michael Stonebraker and Joseph M. Hellerstein: “What Goes Around Comes
Around,” in Readings in Database Systems, 4th edition, MIT Press, pages 2–41, 2005.
ISBN: 978-0-262-69314-1
[3] Pramod J. Sadalage and Martin Fowler: NoSQL Distilled. Addison-Wesley, August
2012. ISBN: 978-0-321-82662-6
[4] Eric Evans: “NoSQL: What’s in a Name?,” blog.sym-link.com, October 30, 2009.
[5] James Phillips: “Surprises in Our NoSQL Adoption Survey,” blog.couchbase.com,
February 8, 2012.
[6] Michael Wagner: SQL/XML:2006 – Evaluierung der Standardkonformität ausge‐
wählter 
Datenbanksysteme. 
Diplomica 
Verlag, 
Hamburg, 
2010. 
ISBN:
978-3-836-64609-3
[7] “XML Data in SQL Server,” SQL Server 2012 documentation, technet.micro‐
soft.com, 2013.
[8] “PostgreSQL 9.3.1 Documentation,” The PostgreSQL Global Development
Group, 2013.
[9] “The MongoDB 2.4 Manual,” MongoDB, Inc., 2013.
64 
| 
Chapter 2: Data Models and Query Languages


[10] “RethinkDB 1.11 Documentation,” rethinkdb.com, 2013.
[11] “Apache CouchDB 1.6 Documentation,” docs.couchdb.org, 2014.
[12] Lin Qiao, Kapil Surlaker, Shirshanka Das, et al.: “On Brewing Fresh Espresso:
LinkedIn’s Distributed Data Serving Platform,” at ACM International Conference on
Management of Data (SIGMOD), June 2013.
[13] Rick Long, Mark Harrington, Robert Hain, and Geoff Nicholls: IMS Primer.
IBM Redbook SG24-5352-00, IBM International Technical Support Organization,
January 2000.
[14] Stephen D. Bartlett: “IBM’s IMS—Myths, Realities, and Opportunities,” The
Clipper Group Navigator, TCG2013015LI, July 2013.
[15] Sarah Mei: “Why You Should Never Use MongoDB,” sarahmei.com, November
11, 2013.
[16] J. S. Knowles and D. M. R. Bell: “The CODASYL Model,” in Databases—Role
and Structure: An Advanced Course, edited by P. M. Stocker, P. M. D. Gray, and M. P.
Atkinson, pages 19–56, Cambridge University Press, 1984. ISBN: 978-0-521-25430-4
[17] Charles W. Bachman: “The Programmer as Navigator,” Communications of the
ACM, 
volume 
16, 
number 
11, 
pages 
653–658, 
November 
1973. 
doi:
10.1145/355611.362534
[18] Joseph M. Hellerstein, Michael Stonebraker, and James Hamilton: “Architecture
of a Database System,” Foundations and Trends in Databases, volume 1, number 2,
pages 141–259, November 2007. doi:10.1561/1900000002
[19] Sandeep Parikh and Kelly Stirman: “Schema Design for Time Series Data in
MongoDB,” blog.mongodb.org, October 30, 2013.
[20] Martin Fowler: “Schemaless Data Structures,” martinfowler.com, January 7,
2013.
[21] Amr Awadallah: “Schema-on-Read vs. Schema-on-Write,” at Berkeley EECS
RAD Lab Retreat, Santa Cruz, CA, May 2009.
[22] Martin Odersky: “The Trouble with Types,” at Strange Loop, September 2013.
[23] Conrad Irwin: “MongoDB—Confessions of a PostgreSQL Lover,” at
HTML5DevConf, October 2013.
[24] “Percona Toolkit Documentation: pt-online-schema-change,” Percona Ireland
Ltd., 2013.
[25] Rany Keddo, Tobias Bielohlawek, and Tobias Schmidt: “Large Hadron Migra‐
tor,” SoundCloud, 2013.
Summary 
| 
65


[26] Shlomi Noach: “gh-ost: GitHub’s Online Schema Migration Tool for MySQL,”
githubengineering.com, August 1, 2016.
[27] James C. Corbett, Jeffrey Dean, Michael Epstein, et al.: “Spanner: Google’s
Globally-Distributed Database,” at 10th USENIX Symposium on Operating System
Design and Implementation (OSDI), October 2012.
[28] Donald K. Burleson: “Reduce I/O with Oracle Cluster Tables,” dba-oracle.com.
[29] Fay Chang, Jeffrey Dean, Sanjay Ghemawat, et al.: “Bigtable: A Distributed Stor‐
age System for Structured Data,” at 7th USENIX Symposium on Operating System
Design and Implementation (OSDI), November 2006.
[30] Bobbie J. Cochrane and Kathy A. McKnight: “DB2 JSON Capabilities, Part 1:
Introduction to DB2 JSON,” IBM developerWorks, June 20, 2013.
[31] Herb Sutter: “The Free Lunch Is Over: A Fundamental Turn Toward Concur‐
rency in Software,” Dr. Dobb’s Journal, volume 30, number 3, pages 202-210, March
2005.
[32] Joseph M. Hellerstein: “The Declarative Imperative: Experiences and Conjec‐
tures in Distributed Logic,” Electrical Engineering and Computer Sciences, Univer‐
sity of California at Berkeley, Tech report UCB/EECS-2010-90, June 2010.
[33] Jeffrey Dean and Sanjay Ghemawat: “MapReduce: Simplified Data Processing on
Large Clusters,” at 6th USENIX Symposium on Operating System Design and Imple‐
mentation (OSDI), December 2004.
[34] Craig Kerstiens: “JavaScript in Your Postgres,” blog.heroku.com, June 5, 2013.
[35] Nathan Bronson, Zach Amsden, George Cabrera, et al.: “TAO: Facebook’s Dis‐
tributed Data Store for the Social Graph,” at USENIX Annual Technical Conference
(USENIX ATC), June 2013.
[36] “Apache TinkerPop3.2.3 Documentation,” tinkerpop.apache.org, October 2016.
[37] “The Neo4j Manual v2.0.0,” Neo Technology, 2013.
[38] Emil Eifrem: Twitter correspondence, January 3, 2014.
[39] David Beckett and Tim Berners-Lee: “Turtle – Terse RDF Triple Language,”
W3C Team Submission, March 28, 2011.
[40] “Datomic Development Resources,” Metadata Partners, LLC, 2013.
[41] W3C RDF Working Group: “Resource Description Framework (RDF),” w3.org,
10 February 2004.
[42] “Apache Jena,” Apache Software Foundation.
66 
| 
Chapter 2: Data Models and Query Languages


[43] Steve Harris, Andy Seaborne, and Eric Prud’hommeaux: “SPARQL 1.1 Query
Language,” W3C Recommendation, March 2013.
[44] Todd J. Green, Shan Shan Huang, Boon Thau Loo, and Wenchao Zhou: “Data‐
log and Recursive Query Processing,” Foundations and Trends in Databases, volume
5, number 2, pages 105–195, November 2013. doi:10.1561/1900000017
[45] Stefano Ceri, Georg Gottlob, and Letizia Tanca: “What You Always Wanted to
Know About Datalog (And Never Dared to Ask),” IEEE Transactions on Knowledge
and Data Engineering, volume 1, number 1, pages 146–166, March 1989. doi:
10.1109/69.43410
[46] Serge Abiteboul, Richard Hull, and Victor Vianu: Foundations of Databases.
Addison-Wesley, 1995. ISBN: 978-0-201-53771-0, available online at web‐
dam.inria.fr/Alice
[47] Nathan Marz: “Cascalog,” cascalog.org.
[48] Dennis A. Benson, Ilene Karsch-Mizrachi, David J. Lipman, et al.: “GenBank,”
Nucleic Acids Research, volume 36, Database issue, pages D25–D30, December 2007.
doi:10.1093/nar/gkm929
[49] Fons Rademakers: “ROOT for Big Data Analysis,” at Workshop on the Future of
Big Data Management, London, UK, June 2013.
Summary 
| 
67




CHAPTER 3
Storage and Retrieval
Wer Ordnung hält, ist nur zu faul zum Suchen.
(If you keep things tidily ordered, you’re just too lazy to go searching.)
—German proverb
On the most fundamental level, a database needs to do two things: when you give it
some data, it should store the data, and when you ask it again later, it should give the
data back to you.
In Chapter 2 we discussed data models and query languages—i.e., the format in
which you (the application developer) give the database your data, and the mecha‐
nism by which you can ask for it again later. In this chapter we discuss the same from
the database’s point of view: how we can store the data that we’re given, and how we
can find it again when we’re asked for it.
Why should you, as an application developer, care how the database handles storage
and retrieval internally? You’re probably not going to implement your own storage
engine from scratch, but you do need to select a storage engine that is appropriate for
your application, from the many that are available. In order to tune a storage engine
to perform well on your kind of workload, you need to have a rough idea of what the
storage engine is doing under the hood.
In particular, there is a big difference between storage engines that are optimized for
transactional workloads and those that are optimized for analytics. We will explore
that distinction later in “Transaction Processing or Analytics?” on page 90, and in
“Column-Oriented Storage” on page 95 we’ll discuss a family of storage engines that
is optimized for analytics.
However, first we’ll start this chapter by talking about storage engines that are used in
the kinds of databases that you’re probably familiar with: traditional relational data‐
bases, and also most so-called NoSQL databases. We will examine two families of
69


storage engines: log-structured storage engines, and page-oriented storage engines
such as B-trees.
Data Structures That Power Your Database
Consider the world’s simplest database, implemented as two Bash functions:
#!/bin/bash
db_set () {
    echo "$1,$2" >> database
}
db_get () {
    grep "^$1," database | sed -e "s/^$1,//" | tail -n 1
}
These two functions implement a key-value store. You can call db_set key value,
which will store key and value in the database. The key and value can be (almost)
anything you like—for example, the value could be a JSON document. You can then
call db_get key, which looks up the most recent value associated with that particular
key and returns it.
And it works:
$ db_set 123456 '{"name":"London","attractions":["Big Ben","London Eye"]}'
$ db_set 42 '{"name":"San Francisco","attractions":["Golden Gate Bridge"]}'
$ db_get 42
{"name":"San Francisco","attractions":["Golden Gate Bridge"]}
The underlying storage format is very simple: a text file where each line contains a
key-value pair, separated by a comma (roughly like a CSV file, ignoring escaping
issues). Every call to db_set appends to the end of the file, so if you update a key sev‐
eral times, the old versions of the value are not overwritten—you need to look at the
last occurrence of a key in a file to find the latest value (hence the tail -n 1 in
db_get):
$ db_set 42 '{"name":"San Francisco","attractions":["Exploratorium"]}'
$ db_get 42
{"name":"San Francisco","attractions":["Exploratorium"]}
$ cat database
123456,{"name":"London","attractions":["Big Ben","London Eye"]}
42,{"name":"San Francisco","attractions":["Golden Gate Bridge"]}
42,{"name":"San Francisco","attractions":["Exploratorium"]}
70 
| 
Chapter 3: Storage and Retrieval


Our db_set function actually has pretty good performance for something that is so
simple, because appending to a file is generally very efficient. Similarly to what
db_set does, many databases internally use a log, which is an append-only data file.
Real databases have more issues to deal with (such as concurrency control, reclaim‐
ing disk space so that the log doesn’t grow forever, and handling errors and partially
written records), but the basic principle is the same. Logs are incredibly useful, and
we will encounter them several times in the rest of this book.
The word log is often used to refer to application logs, where an
application outputs text that describes what’s happening. In this
book, log is used in the more general sense: an append-only
sequence of records. It doesn’t have to be human-readable; it might
be binary and intended only for other programs to read.
On the other hand, our db_get function has terrible performance if you have a large
number of records in your database. Every time you want to look up a key, db_get
has to scan the entire database file from beginning to end, looking for occurrences of
the key. In algorithmic terms, the cost of a lookup is O(n): if you double the number
of records n in your database, a lookup takes twice as long. That’s not good.
In order to efficiently find the value for a particular key in the database, we need a
different data structure: an index. In this chapter we will look at a range of indexing
structures and see how they compare; the general idea behind them is to keep some
additional metadata on the side, which acts as a signpost and helps you to locate the
data you want. If you want to search the same data in several different ways, you may
need several different indexes on different parts of the data.
An index is an additional structure that is derived from the primary data. Many data‐
bases allow you to add and remove indexes, and this doesn’t affect the contents of the
database; it only affects the performance of queries. Maintaining additional structures
incurs overhead, especially on writes. For writes, it’s hard to beat the performance of
simply appending to a file, because that’s the simplest possible write operation. Any
kind of index usually slows down writes, because the index also needs to be updated
every time data is written.
This is an important trade-off in storage systems: well-chosen indexes speed up read
queries, but every index slows down writes. For this reason, databases don’t usually
index everything by default, but require you—the application developer or database
administrator—to choose indexes manually, using your knowledge of the applica‐
tion’s typical query patterns. You can then choose the indexes that give your applica‐
tion the greatest benefit, without introducing more overhead than necessary.
Data Structures That Power Your Database 
| 
71


Hash Indexes
Let’s start with indexes for key-value data. This is not the only kind of data you can
index, but it’s very common, and it’s a useful building block for more complex
indexes.
Key-value stores are quite similar to the dictionary type that you can find in most
programming languages, and which is usually implemented as a hash map (hash
table). Hash maps are described in many algorithms textbooks [1, 2], so we won’t go
into detail of how they work here. Since we already have hash maps for our inmemory data structures, why not use them to index our data on disk?
Let’s say our data storage consists only of appending to a file, as in the preceding
example. Then the simplest possible indexing strategy is this: keep an in-memory
hash map where every key is mapped to a byte offset in the data file—the location at
which the value can be found, as illustrated in Figure 3-1. Whenever you append a
new key-value pair to the file, you also update the hash map to reflect the offset of the
data you just wrote (this works both for inserting new keys and for updating existing
keys). When you want to look up a value, use the hash map to find the offset in the
data file, seek to that location, and read the value.
Figure 3-1. Storing a log of key-value pairs in a CSV-like format, indexed with an inmemory hash map.
This may sound simplistic, but it is a viable approach. In fact, this is essentially what
Bitcask (the default storage engine in Riak) does [3]. Bitcask offers high-performance
reads and writes, subject to the requirement that all the keys fit in the available RAM,
since the hash map is kept completely in memory. The values can use more space
than there is available memory, since they can be loaded from disk with just one disk
72 
| 
Chapter 3: Storage and Retrieval


seek. If that part of the data file is already in the filesystem cache, a read doesn’t
require any disk I/O at all.
A storage engine like Bitcask is well suited to situations where the value for each key
is updated frequently. For example, the key might be the URL of a cat video, and the
value might be the number of times it has been played (incremented every time
someone hits the play button). In this kind of workload, there are a lot of writes, but
there are not too many distinct keys—you have a large number of writes per key, but
it’s feasible to keep all keys in memory.
As described so far, we only ever append to a file—so how do we avoid eventually
running out of disk space? A good solution is to break the log into segments of a cer‐
tain size by closing a segment file when it reaches a certain size, and making subse‐
quent writes to a new segment file. We can then perform compaction on these
segments, as illustrated in Figure 3-2. Compaction means throwing away duplicate
keys in the log, and keeping only the most recent update for each key.
Figure 3-2. Compaction of a key-value update log (counting the number of times each
cat video was played), retaining only the most recent value for each key.
Moreover, since compaction often makes segments much smaller (assuming that a
key is overwritten several times on average within one segment), we can also merge
several segments together at the same time as performing the compaction, as shown
in Figure 3-3. Segments are never modified after they have been written, so the
merged segment is written to a new file. The merging and compaction of frozen seg‐
ments can be done in a background thread, and while it is going on, we can still con‐
tinue to serve read and write requests as normal, using the old segment files. After the
merging process is complete, we switch read requests to using the new merged seg‐
ment instead of the old segments—and then the old segment files can simply be
deleted.
Data Structures That Power Your Database 
| 
73


Figure 3-3. Performing compaction and segment merging simultaneously.
Each segment now has its own in-memory hash table, mapping keys to file offsets. In
order to find the value for a key, we first check the most recent segment’s hash map;
if the key is not present we check the second-most-recent segment, and so on. The
merging process keeps the number of segments small, so lookups don’t need to check
many hash maps.
Lots of detail goes into making this simple idea work in practice. Briefly, some of the
issues that are important in a real implementation are:
File format
CSV is not the best format for a log. It’s faster and simpler to use a binary format
that first encodes the length of a string in bytes, followed by the raw string
(without need for escaping).
Deleting records
If you want to delete a key and its associated value, you have to append a special
deletion record to the data file (sometimes called a tombstone). When log seg‐
ments are merged, the tombstone tells the merging process to discard any previ‐
ous values for the deleted key.
Crash recovery
If the database is restarted, the in-memory hash maps are lost. In principle, you
can restore each segment’s hash map by reading the entire segment file from
beginning to end and noting the offset of the most recent value for every key as
you go along. However, that might take a long time if the segment files are large,
which would make server restarts painful. Bitcask speeds up recovery by storing
74 
| 
Chapter 3: Storage and Retrieval


a snapshot of each segment’s hash map on disk, which can be loaded into mem‐
ory more quickly.
Partially written records
The database may crash at any time, including halfway through appending a
record to the log. Bitcask files include checksums, allowing such corrupted parts
of the log to be detected and ignored.
Concurrency control
As writes are appended to the log in a strictly sequential order, a common imple‐
mentation choice is to have only one writer thread. Data file segments are
append-only and otherwise immutable, so they can be read concurrently by mul‐
tiple threads.
An append-only log seems wasteful at first glance: why don’t you update the file in
place, overwriting the old value with the new value? But an append-only design turns
out to be good for several reasons:
• Appending and segment merging are sequential write operations, which are gen‐
erally much faster than random writes, especially on magnetic spinning-disk
hard drives. To some extent sequential writes are also preferable on flash-based
solid state drives (SSDs) [4]. We will discuss this issue further in “Comparing B-
Trees and LSM-Trees” on page 83.
• Concurrency and crash recovery are much simpler if segment files are appendonly or immutable. For example, you don’t have to worry about the case where a
crash happened while a value was being overwritten, leaving you with a file con‐
taining part of the old and part of the new value spliced together.
• Merging old segments avoids the problem of data files getting fragmented over
time.
However, the hash table index also has limitations:
• The hash table must fit in memory, so if you have a very large number of keys,
you’re out of luck. In principle, you could maintain a hash map on disk, but
unfortunately it is difficult to make an on-disk hash map perform well. It
requires a lot of random access I/O, it is expensive to grow when it becomes full,
and hash collisions require fiddly logic [5].
• Range queries are not efficient. For example, you cannot easily scan over all keys
between kitty00000 and kitty99999—you’d have to look up each key individu‐
ally in the hash maps.
In the next section we will look at an indexing structure that doesn’t have those limi‐
tations. 
Data Structures That Power Your Database 
| 
75


SSTables and LSM-Trees
In Figure 3-3, each log-structured storage segment is a sequence of key-value pairs.
These pairs appear in the order that they were written, and values later in the log take
precedence over values for the same key earlier in the log. Apart from that, the order
of key-value pairs in the file does not matter.
Now we can make a simple change to the format of our segment files: we require that
the sequence of key-value pairs is sorted by key. At first glance, that requirement
seems to break our ability to use sequential writes, but we’ll get to that in a moment.
We call this format Sorted String Table, or SSTable for short. We also require that
each key only appears once within each merged segment file (the compaction process
already ensures that). SSTables have several big advantages over log segments with
hash indexes:
1. Merging segments is simple and efficient, even if the files are bigger than the
available memory. The approach is like the one used in the mergesort algorithm
and is illustrated in Figure 3-4: you start reading the input files side by side, look
at the first key in each file, copy the lowest key (according to the sort order) to
the output file, and repeat. This produces a new merged segment file, also sorted
by key.
Figure 3-4. Merging several SSTable segments, retaining only the most recent value
for each key.
76 
| 
Chapter 3: Storage and Retrieval


i. If all keys and values had a fixed size, you could use binary search on a segment file and avoid the inmemory index entirely. However, they are usually variable-length in practice, which makes it difficult to tell
where one record ends and the next one starts if you don’t have an index.
What if the same key appears in several input segments? Remember that each
segment contains all the values written to the database during some period of
time. This means that all the values in one input segment must be more recent
than all the values in the other segment (assuming that we always merge adjacent
segments). When multiple segments contain the same key, we can keep the value
from the most recent segment and discard the values in older segments.
2. In order to find a particular key in the file, you no longer need to keep an index
of all the keys in memory. See Figure 3-5 for an example: say you’re looking for
the key handiwork, but you don’t know the exact offset of that key in the segment
file. However, you do know the offsets for the keys handbag and handsome, and
because of the sorting you know that handiwork must appear between those two.
This means you can jump to the offset for handbag and scan from there until you
find handiwork (or not, if the key is not present in the file).
Figure 3-5. An SSTable with an in-memory index.
You still need an in-memory index to tell you the offsets for some of the keys, but
it can be sparse: one key for every few kilobytes of segment file is sufficient,
because a few kilobytes can be scanned very quickly.i
3. Since read requests need to scan over several key-value pairs in the requested
range anyway, it is possible to group those records into a block and compress it
before writing it to disk (indicated by the shaded area in Figure 3-5). Each entry
of the sparse in-memory index then points at the start of a compressed block.
Besides saving disk space, compression also reduces the I/O bandwidth use.
Data Structures That Power Your Database 
| 
77


Constructing and maintaining SSTables
Fine so far—but how do you get your data to be sorted by key in the first place? Our
incoming writes can occur in any order.
Maintaining a sorted structure on disk is possible (see “B-Trees” on page 79), but
maintaining it in memory is much easier. There are plenty of well-known tree data
structures that you can use, such as red-black trees or AVL trees [2]. With these data
structures, you can insert keys in any order and read them back in sorted order.
We can now make our storage engine work as follows:
• When a write comes in, add it to an in-memory balanced tree data structure (for
example, a red-black tree). This in-memory tree is sometimes called a memtable.
• When the memtable gets bigger than some threshold—typically a few megabytes
—write it out to disk as an SSTable file. This can be done efficiently because the
tree already maintains the key-value pairs sorted by key. The new SSTable file
becomes the most recent segment of the database. While the SSTable is being
written out to disk, writes can continue to a new memtable instance.
• In order to serve a read request, first try to find the key in the memtable, then in
the most recent on-disk segment, then in the next-older segment, etc.
• From time to time, run a merging and compaction process in the background to
combine segment files and to discard overwritten or deleted values.
This scheme works very well. It only suffers from one problem: if the database
crashes, the most recent writes (which are in the memtable but not yet written out to
disk) are lost. In order to avoid that problem, we can keep a separate log on disk to
which every write is immediately appended, just like in the previous section. That log
is not in sorted order, but that doesn’t matter, because its only purpose is to restore
the memtable after a crash. Every time the memtable is written out to an SSTable, the
corresponding log can be discarded.
Making an LSM-tree out of SSTables
The algorithm described here is essentially what is used in LevelDB [6] and RocksDB
[7], key-value storage engine libraries that are designed to be embedded into other
applications. Among other things, LevelDB can be used in Riak as an alternative to
Bitcask. Similar storage engines are used in Cassandra and HBase [8], both of which
were inspired by Google’s Bigtable paper [9] (which introduced the terms SSTable
and memtable).
Originally this indexing structure was described by Patrick O’Neil et al. under the
name Log-Structured Merge-Tree (or LSM-Tree) [10], building on earlier work on
78 
| 
Chapter 3: Storage and Retrieval


log-structured filesystems [11]. Storage engines that are based on this principle of
merging and compacting sorted files are often called LSM storage engines.
Lucene, an indexing engine for full-text search used by Elasticsearch and Solr, uses a
similar method for storing its term dictionary [12, 13]. A full-text index is much more
complex than a key-value index but is based on a similar idea: given a word in a
search query, find all the documents (web pages, product descriptions, etc.) that
mention the word. This is implemented with a key-value structure where the key is a
word (a term) and the value is the list of IDs of all the documents that contain the
word (the postings list). In Lucene, this mapping from term to postings list is kept in
SSTable-like sorted files, which are merged in the background as needed [14].
Performance optimizations
As always, a lot of detail goes into making a storage engine perform well in practice.
For example, the LSM-tree algorithm can be slow when looking up keys that do not
exist in the database: you have to check the memtable, then the segments all the way
back to the oldest (possibly having to read from disk for each one) before you can be
sure that the key does not exist. In order to optimize this kind of access, storage
engines often use additional Bloom filters [15]. (A Bloom filter is a memory-efficient
data structure for approximating the contents of a set. It can tell you if a key does not
appear in the database, and thus saves many unnecessary disk reads for nonexistent
keys.)
There are also different strategies to determine the order and timing of how SSTables
are compacted and merged. The most common options are size-tiered and leveled
compaction. LevelDB and RocksDB use leveled compaction (hence the name of Lev‐
elDB), HBase uses size-tiered, and Cassandra supports both [16]. In size-tiered com‐
paction, newer and smaller SSTables are successively merged into older and larger
SSTables. In leveled compaction, the key range is split up into smaller SSTables and
older data is moved into separate “levels,” which allows the compaction to proceed
more incrementally and use less disk space.
Even though there are many subtleties, the basic idea of LSM-trees—keeping a cas‐
cade of SSTables that are merged in the background—is simple and effective. Even
when the dataset is much bigger than the available memory it continues to work well.
Since data is stored in sorted order, you can efficiently perform range queries (scan‐
ning all keys above some minimum and up to some maximum), and because the disk
writes are sequential the LSM-tree can support remarkably high write throughput. 
B-Trees
The log-structured indexes we have discussed so far are gaining acceptance, but they
are not the most common type of index. The most widely used indexing structure is
quite different: the B-tree.
Data Structures That Power Your Database 
| 
79


Introduced in 1970 [17] and called “ubiquitous” less than 10 years later [18], B-trees
have stood the test of time very well. They remain the standard index implementation
in almost all relational databases, and many nonrelational databases use them too.
Like SSTables, B-trees keep key-value pairs sorted by key, which allows efficient keyvalue lookups and range queries. But that’s where the similarity ends: B-trees have a
very different design philosophy.
The log-structured indexes we saw earlier break the database down into variable-size
segments, typically several megabytes or more in size, and always write a segment
sequentially. By contrast, B-trees break the database down into fixed-size blocks or
pages, traditionally 4 KB in size (sometimes bigger), and read or write one page at a
time. This design corresponds more closely to the underlying hardware, as disks are
also arranged in fixed-size blocks.
Each page can be identified using an address or location, which allows one page to
refer to another—similar to a pointer, but on disk instead of in memory. We can use
these page references to construct a tree of pages, as illustrated in Figure 3-6.
Figure 3-6. Looking up a key using a B-tree index.
One page is designated as the root of the B-tree; whenever you want to look up a key
in the index, you start here. The page contains several keys and references to child
pages. Each child is responsible for a continuous range of keys, and the keys between
the references indicate where the boundaries between those ranges lie.
In the example in Figure 3-6, we are looking for the key 251, so we know that we need
to follow the page reference between the boundaries 200 and 300. That takes us to a
similar-looking page that further breaks down the 200–300 range into subranges.
80 
| 
Chapter 3: Storage and Retrieval


ii. Inserting a new key into a B-tree is reasonably intuitive, but deleting one (while keeping the tree balanced)
is somewhat more involved [2].
Eventually we get down to a page containing individual keys (a leaf page), which
either contains the value for each key inline or contains references to the pages where
the values can be found.
The number of references to child pages in one page of the B-tree is called the
branching factor. For example, in Figure 3-6 the branching factor is six. In practice,
the branching factor depends on the amount of space required to store the page refer‐
ences and the range boundaries, but typically it is several hundred.
If you want to update the value for an existing key in a B-tree, you search for the leaf
page containing that key, change the value in that page, and write the page back to
disk (any references to that page remain valid). If you want to add a new key, you
need to find the page whose range encompasses the new key and add it to that page.
If there isn’t enough free space in the page to accommodate the new key, it is split
into two half-full pages, and the parent page is updated to account for the new subdi‐
vision of key ranges—see Figure 3-7.ii
Figure 3-7. Growing a B-tree by splitting a page.
This algorithm ensures that the tree remains balanced: a B-tree with n keys always
has a depth of O(log n). Most databases can fit into a B-tree that is three or four levels
deep, so you don’t need to follow many page references to find the page you are look‐
ing for. (A four-level tree of 4 KB pages with a branching factor of 500 can store up to
256 TB.)
Data Structures That Power Your Database 
| 
81


Making B-trees reliable
The basic underlying write operation of a B-tree is to overwrite a page on disk with
new data. It is assumed that the overwrite does not change the location of the page;
i.e., all references to that page remain intact when the page is overwritten. This is in
stark contrast to log-structured indexes such as LSM-trees, which only append to files
(and eventually delete obsolete files) but never modify files in place.
You can think of overwriting a page on disk as an actual hardware operation. On a
magnetic hard drive, this means moving the disk head to the right place, waiting for
the right position on the spinning platter to come around, and then overwriting the
appropriate sector with new data. On SSDs, what happens is somewhat more compli‐
cated, due to the fact that an SSD must erase and rewrite fairly large blocks of a stor‐
age chip at a time [19].
Moreover, some operations require several different pages to be overwritten. For
example, if you split a page because an insertion caused it to be overfull, you need to
write the two pages that were split, and also overwrite their parent page to update the
references to the two child pages. This is a dangerous operation, because if the data‐
base crashes after only some of the pages have been written, you end up with a cor‐
rupted index (e.g., there may be an orphan page that is not a child of any parent).
In order to make the database resilient to crashes, it is common for B-tree implemen‐
tations to include an additional data structure on disk: a write-ahead log (WAL, also
known as a redo log). This is an append-only file to which every B-tree modification
must be written before it can be applied to the pages of the tree itself. When the data‐
base comes back up after a crash, this log is used to restore the B-tree back to a con‐
sistent state [5, 20].
An additional complication of updating pages in place is that careful concurrency
control is required if multiple threads are going to access the B-tree at the same time
—otherwise a thread may see the tree in an inconsistent state. This is typically done
by protecting the tree’s data structures with latches (lightweight locks). Logstructured approaches are simpler in this regard, because they do all the merging in
the background without interfering with incoming queries and atomically swap old
segments for new segments from time to time.
B-tree optimizations
As B-trees have been around for so long, it’s not surprising that many optimizations
have been developed over the years. To mention just a few:
• Instead of overwriting pages and maintaining a WAL for crash recovery, some
databases (like LMDB) use a copy-on-write scheme [21]. A modified page is
written to a different location, and a new version of the parent pages in the tree is
created, pointing at the new location. This approach is also useful for concur‐
82 
| 
Chapter 3: Storage and Retrieval


iii. This variant is sometimes known as a B+ tree, although the optimization is so common that it often isn’t
distinguished from other B-tree variants.
rency control, as we shall see in “Snapshot Isolation and Repeatable Read” on
page 237.
• We can save space in pages by not storing the entire key, but abbreviating it.
Especially in pages on the interior of the tree, keys only need to provide enough
information to act as boundaries between key ranges. Packing more keys into a
page allows the tree to have a higher branching factor, and thus fewer levels.iii
• In general, pages can be positioned anywhere on disk; there is nothing requiring
pages with nearby key ranges to be nearby on disk. If a query needs to scan over a
large part of the key range in sorted order, that page-by-page layout can be ineffi‐
cient, because a disk seek may be required for every page that is read. Many B-
tree implementations therefore try to lay out the tree so that leaf pages appear in
sequential order on disk. However, it’s difficult to maintain that order as the tree
grows. By contrast, since LSM-trees rewrite large segments of the storage in one
go during merging, it’s easier for them to keep sequential keys close to each other
on disk.
• Additional pointers have been added to the tree. For example, each leaf page may
have references to its sibling pages to the left and right, which allows scanning
keys in order without jumping back to parent pages.
• B-tree variants such as fractal trees [22] borrow some log-structured ideas to
reduce disk seeks (and they have nothing to do with fractals). 
Comparing B-Trees and LSM-Trees
Even though B-tree implementations are generally more mature than LSM-tree
implementations, LSM-trees are also interesting due to their performance character‐
istics. As a rule of thumb, LSM-trees are typically faster for writes, whereas B-trees
are thought to be faster for reads [23]. Reads are typically slower on LSM-trees
because they have to check several different data structures and SSTables at different
stages of compaction.
However, benchmarks are often inconclusive and sensitive to details of the workload.
You need to test systems with your particular workload in order to make a valid com‐
parison. In this section we will briefly discuss a few things that are worth considering
when measuring the performance of a storage engine.
Data Structures That Power Your Database 
| 
83


Advantages of LSM-trees
A B-tree index must write every piece of data at least twice: once to the write-ahead
log, and once to the tree page itself (and perhaps again as pages are split). There is
also overhead from having to write an entire page at a time, even if only a few bytes in
that page changed. Some storage engines even overwrite the same page twice in order
to avoid ending up with a partially updated page in the event of a power failure [24,
25].
Log-structured indexes also rewrite data multiple times due to repeated compaction
and merging of SSTables. This effect—one write to the database resulting in multiple
writes to the disk over the course of the database’s lifetime—is known as write ampli‐
fication. It is of particular concern on SSDs, which can only overwrite blocks a limi‐
ted number of times before wearing out.
In write-heavy applications, the performance bottleneck might be the rate at which
the database can write to disk. In this case, write amplification has a direct perfor‐
mance cost: the more that a storage engine writes to disk, the fewer writes per second
it can handle within the available disk bandwidth.
Moreover, LSM-trees are typically able to sustain higher write throughput than B-
trees, partly because they sometimes have lower write amplification (although this
depends on the storage engine configuration and workload), and partly because they
sequentially write compact SSTable files rather than having to overwrite several pages
in the tree [26]. This difference is particularly important on magnetic hard drives,
where sequential writes are much faster than random writes.
LSM-trees can be compressed better, and thus often produce smaller files on disk
than B-trees. B-tree storage engines leave some disk space unused due to fragmenta‐
tion: when a page is split or when a row cannot fit into an existing page, some space
in a page remains unused. Since LSM-trees are not page-oriented and periodically
rewrite SSTables to remove fragmentation, they have lower storage overheads, espe‐
cially when using leveled compaction [27].
On many SSDs, the firmware internally uses a log-structured algorithm to turn ran‐
dom writes into sequential writes on the underlying storage chips, so the impact of
the storage engine’s write pattern is less pronounced [19]. However, lower write
amplification and reduced fragmentation are still advantageous on SSDs: represent‐
ing data more compactly allows more read and write requests within the available I/O
bandwidth.
Downsides of LSM-trees
A downside of log-structured storage is that the compaction process can sometimes
interfere with the performance of ongoing reads and writes. Even though storage
engines try to perform compaction incrementally and without affecting concurrent
84 
| 
Chapter 3: Storage and Retrieval


access, disks have limited resources, so it can easily happen that a request needs to
wait while the disk finishes an expensive compaction operation. The impact on
throughput and average response time is usually small, but at higher percentiles (see
“Describing Performance” on page 13) the response time of queries to log-structured
storage engines can sometimes be quite high, and B-trees can be more predictable
[28].
Another issue with compaction arises at high write throughput: the disk’s finite write
bandwidth needs to be shared between the initial write (logging and flushing a
memtable to disk) and the compaction threads running in the background. When
writing to an empty database, the full disk bandwidth can be used for the initial write,
but the bigger the database gets, the more disk bandwidth is required for compaction.
If write throughput is high and compaction is not configured carefully, it can happen
that compaction cannot keep up with the rate of incoming writes. In this case, the
number of unmerged segments on disk keeps growing until you run out of disk
space, and reads also slow down because they need to check more segment files. Typ‐
ically, SSTable-based storage engines do not throttle the rate of incoming writes, even
if compaction cannot keep up, so you need explicit monitoring to detect this situa‐
tion [29, 30].
An advantage of B-trees is that each key exists in exactly one place in the index,
whereas a log-structured storage engine may have multiple copies of the same key in
different segments. This aspect makes B-trees attractive in databases that want to
offer strong transactional semantics: in many relational databases, transaction isola‐
tion is implemented using locks on ranges of keys, and in a B-tree index, those locks
can be directly attached to the tree [5]. In Chapter 7 we will discuss this point in more
detail.
B-trees are very ingrained in the architecture of databases and provide consistently
good performance for many workloads, so it’s unlikely that they will go away anytime
soon. In new datastores, log-structured indexes are becoming increasingly popular.
There is no quick and easy rule for determining which type of storage engine is better
for your use case, so it is worth testing empirically. 
Other Indexing Structures
So far we have only discussed key-value indexes, which are like a primary key index in
the relational model. A primary key uniquely identifies one row in a relational table,
or one document in a document database, or one vertex in a graph database. Other
records in the database can refer to that row/document/vertex by its primary key (or
ID), and the index is used to resolve such references.
It is also very common to have secondary indexes. In relational databases, you can
create several secondary indexes on the same table using the CREATE INDEX com‐
Data Structures That Power Your Database 
| 
85


mand, and they are often crucial for performing joins efficiently. For example, in
Figure 2-1 in Chapter 2 you would most likely have a secondary index on the
user_id columns so that you can find all the rows belonging to the same user in each
of the tables.
A secondary index can easily be constructed from a key-value index. The main differ‐
ence is that keys are not unique; i.e., there might be many rows (documents, vertices)
with the same key. This can be solved in two ways: either by making each value in the
index a list of matching row identifiers (like a postings list in a full-text index) or by
making each key unique by appending a row identifier to it. Either way, both B-trees
and log-structured indexes can be used as secondary indexes.
Storing values within the index
The key in an index is the thing that queries search for, but the value can be one of
two things: it could be the actual row (document, vertex) in question, or it could be a
reference to the row stored elsewhere. In the latter case, the place where rows are
stored is known as a heap file, and it stores data in no particular order (it may be
append-only, or it may keep track of deleted rows in order to overwrite them with
new data later). The heap file approach is common because it avoids duplicating data
when multiple secondary indexes are present: each index just references a location in
the heap file, and the actual data is kept in one place.
When updating a value without changing the key, the heap file approach can be quite
efficient: the record can be overwritten in place, provided that the new value is not
larger than the old value. The situation is more complicated if the new value is larger,
as it probably needs to be moved to a new location in the heap where there is enough
space. In that case, either all indexes need to be updated to point at the new heap
location of the record, or a forwarding pointer is left behind in the old heap location
[5].
In some situations, the extra hop from the index to the heap file is too much of a per‐
formance penalty for reads, so it can be desirable to store the indexed row directly
within an index. This is known as a clustered index. For example, in MySQL’s
InnoDB storage engine, the primary key of a table is always a clustered index, and
secondary indexes refer to the primary key (rather than a heap file location) [31]. In
SQL Server, you can specify one clustered index per table [32].
A compromise between a clustered index (storing all row data within the index) and
a nonclustered index (storing only references to the data within the index) is known
as a covering index or index with included columns, which stores some of a table’s col‐
umns within the index [33]. This allows some queries to be answered by using the
index alone (in which case, the index is said to cover the query) [32].
86 
| 
Chapter 3: Storage and Retrieval


As with any kind of duplication of data, clustered and covering indexes can speed up
reads, but they require additional storage and can add overhead on writes. Databases
also need to go to additional effort to enforce transactional guarantees, because appli‐
cations should not see inconsistencies due to the duplication.
Multi-column indexes
The indexes discussed so far only map a single key to a value. That is not sufficient if
we need to query multiple columns of a table (or multiple fields in a document)
simultaneously.
The most common type of multi-column index is called a concatenated index, which
simply combines several fields into one key by appending one column to another (the
index definition specifies in which order the fields are concatenated). This is like an
old-fashioned paper phone book, which provides an index from (lastname, first‐
name) to phone number. Due to the sort order, the index can be used to find all the
people with a particular last name, or all the people with a particular lastnamefirstname combination. However, the index is useless if you want to find all the peo‐
ple with a particular first name.
Multi-dimensional indexes are a more general way of querying several columns at
once, which is particularly important for geospatial data. For example, a restaurantsearch website may have a database containing the latitude and longitude of each res‐
taurant. When a user is looking at the restaurants on a map, the website needs to
search for all the restaurants within the rectangular map area that the user is cur‐
rently viewing. This requires a two-dimensional range query like the following:
SELECT * FROM restaurants WHERE latitude  > 51.4946 AND latitude  < 51.5079
                            AND longitude > -0.1162 AND longitude < -0.1004;
A standard B-tree or LSM-tree index is not able to answer that kind of query effi‐
ciently: it can give you either all the restaurants in a range of latitudes (but at any lon‐
gitude), or all the restaurants in a range of longitudes (but anywhere between the
North and South poles), but not both simultaneously.
One option is to translate a two-dimensional location into a single number using a
space-filling curve, and then to use a regular B-tree index [34]. More commonly, spe‐
cialized spatial indexes such as R-trees are used. For example, PostGIS implements
geospatial indexes as R-trees using PostgreSQL’s Generalized Search Tree indexing
facility [35]. We don’t have space to describe R-trees in detail here, but there is plenty
of literature on them.
An interesting idea is that multi-dimensional indexes are not just for geographic
locations. For example, on an ecommerce website you could use a three-dimensional
index on the dimensions (red, green, blue) to search for products in a certain range of
colors, or in a database of weather observations you could have a two-dimensional
Data Structures That Power Your Database 
| 
87


index on (date, temperature) in order to efficiently search for all the observations
during the year 2013 where the temperature was between 25 and 30℃. With a onedimensional index, you would have to either scan over all the records from 2013
(regardless of temperature) and then filter them by temperature, or vice versa. A 2D
index could narrow down by timestamp and temperature simultaneously. This tech‐
nique is used by HyperDex [36].
Full-text search and fuzzy indexes
All the indexes discussed so far assume that you have exact data and allow you to
query for exact values of a key, or a range of values of a key with a sort order. What
they don’t allow you to do is search for similar keys, such as misspelled words. Such
fuzzy querying requires different techniques.
For example, full-text search engines commonly allow a search for one word to be
expanded to include synonyms of the word, to ignore grammatical variations of
words, and to search for occurrences of words near each other in the same document,
and support various other features that depend on linguistic analysis of the text. To
cope with typos in documents or queries, Lucene is able to search text for words
within a certain edit distance (an edit distance of 1 means that one letter has been
added, removed, or replaced) [37].
As mentioned in “Making an LSM-tree out of SSTables” on page 78, Lucene uses a
SSTable-like structure for its term dictionary. This structure requires a small inmemory index that tells queries at which offset in the sorted file they need to look for
a key. In LevelDB, this in-memory index is a sparse collection of some of the keys,
but in Lucene, the in-memory index is a finite state automaton over the characters in
the keys, similar to a trie [38]. This automaton can be transformed into a Levenshtein
automaton, which supports efficient search for words within a given edit distance
[39].
Other fuzzy search techniques go in the direction of document classification and
machine learning. See an information retrieval textbook for more detail [e.g., 40].
Keeping everything in memory
The data structures discussed so far in this chapter have all been answers to the limi‐
tations of disks. Compared to main memory, disks are awkward to deal with. With
both magnetic disks and SSDs, data on disk needs to be laid out carefully if you want
good performance on reads and writes. However, we tolerate this awkwardness
because disks have two significant advantages: they are durable (their contents are
not lost if the power is turned off), and they have a lower cost per gigabyte than
RAM.
As RAM becomes cheaper, the cost-per-gigabyte argument is eroded. Many datasets
are simply not that big, so it’s quite feasible to keep them entirely in memory, poten‐
88 
| 
Chapter 3: Storage and Retrieval


tially distributed across several machines. This has led to the development of inmemory databases.
Some in-memory key-value stores, such as Memcached, are intended for caching use
only, where it’s acceptable for data to be lost if a machine is restarted. But other inmemory databases aim for durability, which can be achieved with special hardware
(such as battery-powered RAM), by writing a log of changes to disk, by writing peri‐
odic snapshots to disk, or by replicating the in-memory state to other machines.
When an in-memory database is restarted, it needs to reload its state, either from disk
or over the network from a replica (unless special hardware is used). Despite writing
to disk, it’s still an in-memory database, because the disk is merely used as an
append-only log for durability, and reads are served entirely from memory. Writing
to disk also has operational advantages: files on disk can easily be backed up,
inspected, and analyzed by external utilities.
Products such as VoltDB, MemSQL, and Oracle TimesTen are in-memory databases
with a relational model, and the vendors claim that they can offer big performance
improvements by removing all the overheads associated with managing on-disk data
structures [41, 42]. RAMCloud is an open source, in-memory key-value store with
durability (using a log-structured approach for the data in memory as well as the data
on disk) [43]. Redis and Couchbase provide weak durability by writing to disk asyn‐
chronously.
Counterintuitively, the performance advantage of in-memory databases is not due to
the fact that they don’t need to read from disk. Even a disk-based storage engine may
never need to read from disk if you have enough memory, because the operating sys‐
tem caches recently used disk blocks in memory anyway. Rather, they can be faster
because they can avoid the overheads of encoding in-memory data structures in a
form that can be written to disk [44].
Besides performance, another interesting area for in-memory databases is providing
data models that are difficult to implement with disk-based indexes. For example,
Redis offers a database-like interface to various data structures such as priority
queues and sets. Because it keeps all data in memory, its implementation is compara‐
tively simple.
Recent research indicates that an in-memory database architecture could be extended
to support datasets larger than the available memory, without bringing back the over‐
heads of a disk-centric architecture [45]. The so-called anti-caching approach works
by evicting the least recently used data from memory to disk when there is not
enough memory, and loading it back into memory when it is accessed again in the
future. This is similar to what operating systems do with virtual memory and swap
files, but the database can manage memory more efficiently than the OS, as it can
work at the granularity of individual records rather than entire memory pages. This
Data Structures That Power Your Database 
| 
89


approach still requires indexes to fit entirely in memory, though (like the Bitcask
example at the beginning of the chapter).
Further changes to storage engine design will probably be needed if non-volatile
memory (NVM) technologies become more widely adopted [46]. At present, this is a
new area of research, but it is worth keeping an eye on in the future. 
Transaction Processing or Analytics?
In the early days of business data processing, a write to the database typically corre‐
sponded to a commercial transaction taking place: making a sale, placing an order
with a supplier, paying an employee’s salary, etc. As databases expanded into areas
that didn’t involve money changing hands, the term transaction nevertheless stuck,
referring to a group of reads and writes that form a logical unit.
A transaction needn’t necessarily have ACID (atomicity, consis‐
tency, isolation, and durability) properties. Transaction processing
just means allowing clients to make low-latency reads and writes—
as opposed to batch processing jobs, which only run periodically
(for example, once per day). We discuss the ACID properties in
Chapter 7 and batch processing in Chapter 10.
Even though databases started being used for many different kinds of data—com‐
ments on blog posts, actions in a game, contacts in an address book, etc.—the basic
access pattern remained similar to processing business transactions. An application
typically looks up a small number of records by some key, using an index. Records
are inserted or updated based on the user’s input. Because these applications are
interactive, the access pattern became known as online transaction processing
(OLTP).
However, databases also started being increasingly used for data analytics, which has
very different access patterns. Usually an analytic query needs to scan over a huge
number of records, only reading a few columns per record, and calculates aggregate
statistics (such as count, sum, or average) rather than returning the raw data to the
user. For example, if your data is a table of sales transactions, then analytic queries
might be:
• What was the total revenue of each of our stores in January?
• How many more bananas than usual did we sell during our latest promotion?
• Which brand of baby food is most often purchased together with brand X
diapers?
90 
| 
Chapter 3: Storage and Retrieval


iv. The meaning of online in OLAP is unclear; it probably refers to the fact that queries are not just for prede‐
fined reports, but that analysts use the OLAP system interactively for explorative queries.
These queries are often written by business analysts, and feed into reports that help
the management of a company make better decisions (business intelligence). In order
to differentiate this pattern of using databases from transaction processing, it has
been called online analytic processing (OLAP) [47].iv The difference between OLTP
and OLAP is not always clear-cut, but some typical characteristics are listed in
Table 3-1.
Table 3-1. Comparing characteristics of transaction processing versus analytic systems
Property
Transaction processing systems (OLTP)
Analytic systems (OLAP)
Main read pattern
Small number of records per query, fetched by key
Aggregate over large number of records
Main write pattern
Random-access, low-latency writes from user input
Bulk import (ETL) or event stream
Primarily used by
End user/customer, via web application
Internal analyst, for decision support
What data represents
Latest state of data (current point in time)
History of events that happened over time
Dataset size
Gigabytes to terabytes
Terabytes to petabytes
At first, the same databases were used for both transaction processing and analytic
queries. SQL turned out to be quite flexible in this regard: it works well for OLTP-
type queries as well as OLAP-type queries. Nevertheless, in the late 1980s and early
1990s, there was a trend for companies to stop using their OLTP systems for analytics
purposes, and to run the analytics on a separate database instead. This separate data‐
base was called a data warehouse.
Data Warehousing
An enterprise may have dozens of different transaction processing systems: systems
powering the customer-facing website, controlling point of sale (checkout) systems in
physical stores, tracking inventory in warehouses, planning routes for vehicles, man‐
aging suppliers, administering employees, etc. Each of these systems is complex and
needs a team of people to maintain it, so the systems end up operating mostly auton‐
omously from each other.
These OLTP systems are usually expected to be highly available and to process trans‐
actions with low latency, since they are often critical to the operation of the business.
Database administrators therefore closely guard their OLTP databases. They are usu‐
ally reluctant to let business analysts run ad hoc analytic queries on an OLTP data‐
base, since those queries are often expensive, scanning large parts of the dataset,
which can harm the performance of concurrently executing transactions.
Transaction Processing or Analytics? 
| 
91


A data warehouse, by contrast, is a separate database that analysts can query to their
hearts’ content, without affecting OLTP operations [48]. The data warehouse con‐
tains a read-only copy of the data in all the various OLTP systems in the company.
Data is extracted from OLTP databases (using either a periodic data dump or a con‐
tinuous stream of updates), transformed into an analysis-friendly schema, cleaned
up, and then loaded into the data warehouse. This process of getting data into the
warehouse is known as Extract–Transform–Load (ETL) and is illustrated in
Figure 3-8.
Figure 3-8. Simplified outline of ETL into a data warehouse.
Data warehouses now exist in almost all large enterprises, but in small companies
they are almost unheard of. This is probably because most small companies don’t
have so many different OLTP systems, and most small companies have a small
amount of data—small enough that it can be queried in a conventional SQL database,
or even analyzed in a spreadsheet. In a large company, a lot of heavy lifting is
required to do something that is simple in a small company.
A big advantage of using a separate data warehouse, rather than querying OLTP sys‐
tems directly for analytics, is that the data warehouse can be optimized for analytic
access patterns. It turns out that the indexing algorithms discussed in the first half of
this chapter work well for OLTP, but are not very good at answering analytic queries.
92 
| 
Chapter 3: Storage and Retrieval


In the rest of this chapter we will look at storage engines that are optimized for ana‐
lytics instead.
The divergence between OLTP databases and data warehouses
The data model of a data warehouse is most commonly relational, because SQL is
generally a good fit for analytic queries. There are many graphical data analysis tools
that generate SQL queries, visualize the results, and allow analysts to explore the data
(through operations such as drill-down and slicing and dicing).
On the surface, a data warehouse and a relational OLTP database look similar,
because they both have a SQL query interface. However, the internals of the systems
can look quite different, because they are optimized for very different query patterns.
Many database vendors now focus on supporting either transaction processing or
analytics workloads, but not both.
Some databases, such as Microsoft SQL Server and SAP HANA, have support for
transaction processing and data warehousing in the same product. However, they are
increasingly becoming two separate storage and query engines, which happen to be
accessible through a common SQL interface [49, 50, 51].
Data warehouse vendors such as Teradata, Vertica, SAP HANA, and ParAccel typi‐
cally sell their systems under expensive commercial licenses. Amazon RedShift is a
hosted version of ParAccel. More recently, a plethora of open source SQL-on-
Hadoop projects have emerged; they are young but aiming to compete with commer‐
cial data warehouse systems. These include Apache Hive, Spark SQL, Cloudera
Impala, Facebook Presto, Apache Tajo, and Apache Drill [52, 53]. Some of them are
based on ideas from Google’s Dremel [54].
Stars and Snowflakes: Schemas for Analytics
As explored in Chapter 2, a wide range of different data models are used in the realm
of transaction processing, depending on the needs of the application. On the other
hand, in analytics, there is much less diversity of data models. Many data warehouses
are used in a fairly formulaic style, known as a star schema (also known as dimen‐
sional modeling [55]).
The example schema in Figure 3-9 shows a data warehouse that might be found at a
grocery retailer. At the center of the schema is a so-called fact table (in this example,
it is called fact_sales). Each row of the fact table represents an event that occurred
at a particular time (here, each row represents a customer’s purchase of a product). If
we were analyzing website traffic rather than retail sales, each row might represent a
page view or a click by a user.
Transaction Processing or Analytics? 
| 
93


Figure 3-9. Example of a star schema for use in a data warehouse.
Usually, facts are captured as individual events, because this allows maximum flexi‐
bility of analysis later. However, this means that the fact table can become extremely
large. A big enterprise like Apple, Walmart, or eBay may have tens of petabytes of
transaction history in its data warehouse, most of which is in fact tables [56].
Some of the columns in the fact table are attributes, such as the price at which the
product was sold and the cost of buying it from the supplier (allowing the profit mar‐
gin to be calculated). Other columns in the fact table are foreign key references to
other tables, called dimension tables. As each row in the fact table represents an event,
the dimensions represent the who, what, where, when, how, and why of the event.
For example, in Figure 3-9, one of the dimensions is the product that was sold. Each
row in the dim_product table represents one type of product that is for sale, including
94 
| 
Chapter 3: Storage and Retrieval


its stock-keeping unit (SKU), description, brand name, category, fat content, package
size, etc. Each row in the fact_sales table uses a foreign key to indicate which prod‐
uct was sold in that particular transaction. (For simplicity, if the customer buys sev‐
eral different products at once, they are represented as separate rows in the fact
table.)
Even date and time are often represented using dimension tables, because this allows
additional information about dates (such as public holidays) to be encoded, allowing
queries to differentiate between sales on holidays and non-holidays.
The name “star schema” comes from the fact that when the table relationships are
visualized, the fact table is in the middle, surrounded by its dimension tables; the
connections to these tables are like the rays of a star.
A variation of this template is known as the snowflake schema, where dimensions are
further broken down into subdimensions. For example, there could be separate tables
for brands and product categories, and each row in the dim_product table could ref‐
erence the brand and category as foreign keys, rather than storing them as strings in
the dim_product table. Snowflake schemas are more normalized than star schemas,
but star schemas are often preferred because they are simpler for analysts to work
with [55].
In a typical data warehouse, tables are often very wide: fact tables often have over 100
columns, sometimes several hundred [51]. Dimension tables can also be very wide, as
they include all the metadata that may be relevant for analysis—for example, the
dim_store table may include details of which services are offered at each store,
whether it has an in-store bakery, the square footage, the date when the store was first
opened, when it was last remodeled, how far it is from the nearest highway, etc. 
Column-Oriented Storage
If you have trillions of rows and petabytes of data in your fact tables, storing and
querying them efficiently becomes a challenging problem. Dimension tables are usu‐
ally much smaller (millions of rows), so in this section we will concentrate primarily
on storage of facts.
Although fact tables are often over 100 columns wide, a typical data warehouse query
only accesses 4 or 5 of them at one time ("SELECT *" queries are rarely needed for
analytics) [51]. Take the query in Example 3-1: it accesses a large number of rows
(every occurrence of someone buying fruit or candy during the 2013 calendar year),
but it only needs to access three columns of the fact_sales table: date_key,
product_sk, and quantity. The query ignores all other columns.
Column-Oriented Storage 
| 
95


Example 3-1. Analyzing whether people are more inclined to buy fresh fruit or candy,
depending on the day of the week
SELECT
  dim_date.weekday, dim_product.category,
  SUM(fact_sales.quantity) AS quantity_sold
FROM fact_sales
  JOIN dim_date    ON fact_sales.date_key   = dim_date.date_key
  JOIN dim_product ON fact_sales.product_sk = dim_product.product_sk
WHERE
  dim_date.year = 2013 AND
  dim_product.category IN ('Fresh fruit', 'Candy')
GROUP BY
  dim_date.weekday, dim_product.category;
How can we execute this query efficiently?
In most OLTP databases, storage is laid out in a row-oriented fashion: all the values
from one row of a table are stored next to each other. Document databases are simi‐
lar: an entire document is typically stored as one contiguous sequence of bytes. You
can see this in the CSV example of Figure 3-1.
In order to process a query like Example 3-1, you may have indexes on
fact_sales.date_key and/or fact_sales.product_sk that tell the storage engine
where to find all the sales for a particular date or for a particular product. But then, a
row-oriented storage engine still needs to load all of those rows (each consisting of
over 100 attributes) from disk into memory, parse them, and filter out those that
don’t meet the required conditions. That can take a long time.
The idea behind column-oriented storage is simple: don’t store all the values from one
row together, but store all the values from each column together instead. If each col‐
umn is stored in a separate file, a query only needs to read and parse those columns
that are used in that query, which can save a lot of work. This principle is illustrated
in Figure 3-10. 
Column storage is easiest to understand in a relational data model,
but it applies equally to nonrelational data. For example, Parquet
[57] is a columnar storage format that supports a document data
model, based on Google’s Dremel [54].
96 
| 
Chapter 3: Storage and Retrieval


Figure 3-10. Storing relational data by column, rather than by row.
The column-oriented storage layout relies on each column file containing the rows in
the same order. Thus, if you need to reassemble an entire row, you can take the 23rd
entry from each of the individual column files and put them together to form the
23rd row of the table.
Column Compression
Besides only loading those columns from disk that are required for a query, we can
further reduce the demands on disk throughput by compressing data. Fortunately,
column-oriented storage often lends itself very well to compression.
Take a look at the sequences of values for each column in Figure 3-10: they often look
quite repetitive, which is a good sign for compression. Depending on the data in the
column, different compression techniques can be used. One technique that is particu‐
larly effective in data warehouses is bitmap encoding, illustrated in Figure 3-11.
Column-Oriented Storage 
| 
97


Figure 3-11. Compressed, bitmap-indexed storage of a single column.
Often, the number of distinct values in a column is small compared to the number of
rows (for example, a retailer may have billions of sales transactions, but only 100,000
distinct products). We can now take a column with n distinct values and turn it into
n separate bitmaps: one bitmap for each distinct value, with one bit for each row. The
bit is 1 if the row has that value, and 0 if not.
If n is very small (for example, a country column may have approximately 200 dis‐
tinct values), those bitmaps can be stored with one bit per row. But if n is bigger,
there will be a lot of zeros in most of the bitmaps (we say that they are sparse). In that
case, the bitmaps can additionally be run-length encoded, as shown at the bottom of
Figure 3-11. This can make the encoding of a column remarkably compact.
Bitmap indexes such as these are very well suited for the kinds of queries that are
common in a data warehouse. For example:
WHERE product_sk IN (30, 68, 69):
Load the three bitmaps for product_sk = 30, product_sk = 68, and product_sk
= 69, and calculate the bitwise OR of the three bitmaps, which can be done very
efficiently.
98 
| 
Chapter 3: Storage and Retrieval


WHERE product_sk = 31 AND store_sk = 3:
Load the bitmaps for product_sk = 31 and store_sk = 3, and calculate the bit‐
wise AND. This works because the columns contain the rows in the same order,
so the kth bit in one column’s bitmap corresponds to the same row as the kth bit
in another column’s bitmap.
There are also various other compression schemes for different kinds of data, but we
won’t go into them in detail—see [58] for an overview.
Column-oriented storage and column families
Cassandra and HBase have a concept of column families, which
they inherited from Bigtable [9]. However, it is very misleading to
call them column-oriented: within each column family, they store
all columns from a row together, along with a row key, and they do
not use column compression. Thus, the Bigtable model is still
mostly row-oriented.
Memory bandwidth and vectorized processing
For data warehouse queries that need to scan over millions of rows, a big bottleneck
is the bandwidth for getting data from disk into memory. However, that is not the
only bottleneck. Developers of analytical databases also worry about efficiently using
the bandwidth from main memory into the CPU cache, avoiding branch mispredic‐
tions and bubbles in the CPU instruction processing pipeline, and making use of
single-instruction-multi-data (SIMD) instructions in modern CPUs [59, 60].
Besides reducing the volume of data that needs to be loaded from disk, columnoriented storage layouts are also good for making efficient use of CPU cycles. For
example, the query engine can take a chunk of compressed column data that fits
comfortably in the CPU’s L1 cache and iterate through it in a tight loop (that is, with
no function calls). A CPU can execute such a loop much faster than code that
requires a lot of function calls and conditions for each record that is processed. Col‐
umn compression allows more rows from a column to fit in the same amount of L1
cache. Operators, such as the bitwise AND and OR described previously, can be
designed to operate on such chunks of compressed column data directly. This techni‐
que is known as vectorized processing [58, 49]. 
Sort Order in Column Storage
In a column store, it doesn’t necessarily matter in which order the rows are stored.
It’s easiest to store them in the order in which they were inserted, since then inserting
a new row just means appending to each of the column files. However, we can choose
to impose an order, like we did with SSTables previously, and use that as an indexing
mechanism.
Column-Oriented Storage 
| 
99


Note that it wouldn’t make sense to sort each column independently, because then
we would no longer know which items in the columns belong to the same row. We
can only reconstruct a row because we know that the kth item in one column belongs
to the same row as the kth item in another column.
Rather, the data needs to be sorted an entire row at a time, even though it is stored by
column. The administrator of the database can choose the columns by which the
table should be sorted, using their knowledge of common queries. For example, if
queries often target date ranges, such as the last month, it might make sense to make
date_key the first sort key. Then the query optimizer can scan only the rows from the
last month, which will be much faster than scanning all rows.
A second column can determine the sort order of any rows that have the same value
in the first column. For example, if date_key is the first sort key in Figure 3-10, it
might make sense for product_sk to be the second sort key so that all sales for the
same product on the same day are grouped together in storage. That will help queries
that need to group or filter sales by product within a certain date range.
Another advantage of sorted order is that it can help with compression of columns. If
the primary sort column does not have many distinct values, then after sorting, it will
have long sequences where the same value is repeated many times in a row. A simple
run-length encoding, like we used for the bitmaps in Figure 3-11, could compress
that column down to a few kilobytes—even if the table has billions of rows.
That compression effect is strongest on the first sort key. The second and third sort
keys will be more jumbled up, and thus not have such long runs of repeated values.
Columns further down the sorting priority appear in essentially random order, so
they probably won’t compress as well. But having the first few columns sorted is still
a win overall.
Several different sort orders
A clever extension of this idea was introduced in C-Store and adopted in the com‐
mercial data warehouse Vertica [61, 62]. Different queries benefit from different sort
orders, so why not store the same data sorted in several different ways? Data needs to
be replicated to multiple machines anyway, so that you don’t lose data if one machine
fails. You might as well store that redundant data sorted in different ways so that
when you’re processing a query, you can use the version that best fits the query
pattern.
Having multiple sort orders in a column-oriented store is a bit similar to having mul‐
tiple secondary indexes in a row-oriented store. But the big difference is that the roworiented store keeps every row in one place (in the heap file or a clustered index), and
secondary indexes just contain pointers to the matching rows. In a column store,
there normally aren’t any pointers to data elsewhere, only columns containing values. 
100 
| 
Chapter 3: Storage and Retrieval


Writing to Column-Oriented Storage
These optimizations make sense in data warehouses, because most of the load con‐
sists of large read-only queries run by analysts. Column-oriented storage, compres‐
sion, and sorting all help to make those read queries faster. However, they have the
downside of making writes more difficult.
An update-in-place approach, like B-trees use, is not possible with compressed col‐
umns. If you wanted to insert a row in the middle of a sorted table, you would most
likely have to rewrite all the column files. As rows are identified by their position
within a column, the insertion has to update all columns consistently.
Fortunately, we have already seen a good solution earlier in this chapter: LSM-trees.
All writes first go to an in-memory store, where they are added to a sorted structure
and prepared for writing to disk. It doesn’t matter whether the in-memory store is
row-oriented or column-oriented. When enough writes have accumulated, they are
merged with the column files on disk and written to new files in bulk. This is essen‐
tially what Vertica does [62].
Queries need to examine both the column data on disk and the recent writes in mem‐
ory, and combine the two. However, the query optimizer hides this distinction from
the user. From an analyst’s point of view, data that has been modified with inserts,
updates, or deletes is immediately reflected in subsequent queries. 
Aggregation: Data Cubes and Materialized Views
Not every data warehouse is necessarily a column store: traditional row-oriented
databases and a few other architectures are also used. However, columnar storage can
be significantly faster for ad hoc analytical queries, so it is rapidly gaining popularity
[51, 63].
Another aspect of data warehouses that is worth mentioning briefly is materialized
aggregates. As discussed earlier, data warehouse queries often involve an aggregate
function, such as COUNT, SUM, AVG, MIN, or MAX in SQL. If the same aggregates are used
by many different queries, it can be wasteful to crunch through the raw data every
time. Why not cache some of the counts or sums that queries use most often?
One way of creating such a cache is a materialized view. In a relational data model, it
is often defined like a standard (virtual) view: a table-like object whose contents are
the results of some query. The difference is that a materialized view is an actual copy
of the query results, written to disk, whereas a virtual view is just a shortcut for writ‐
ing queries. When you read from a virtual view, the SQL engine expands it into the
view’s underlying query on the fly and then processes the expanded query.
When the underlying data changes, a materialized view needs to be updated, because
it is a denormalized copy of the data. The database can do that automatically, but
Column-Oriented Storage 
| 
101


such updates make writes more expensive, which is why materialized views are not
often used in OLTP databases. In read-heavy data warehouses they can make more
sense (whether or not they actually improve read performance depends on the indi‐
vidual case).
A common special case of a materialized view is known as a data cube or OLAP cube
[64]. It is a grid of aggregates grouped by different dimensions. Figure 3-12 shows an
example.
Figure 3-12. Two dimensions of a data cube, aggregating data by summing.
Imagine for now that each fact has foreign keys to only two dimension tables—in
Figure 3-12, these are date and product. You can now draw a two-dimensional table,
with dates along one axis and products along the other. Each cell contains the aggre‐
gate (e.g., SUM) of an attribute (e.g., net_price) of all facts with that date-product
combination. Then you can apply the same aggregate along each row or column and
get a summary that has been reduced by one dimension (the sales by product regard‐
less of date, or the sales by date regardless of product).
In general, facts often have more than two dimensions. In Figure 3-9 there are five
dimensions: date, product, store, promotion, and customer. It’s a lot harder to imag‐
ine what a five-dimensional hypercube would look like, but the principle remains the
same: each cell contains the sales for a particular date-product-store-promotioncustomer combination. These values can then repeatedly be summarized along each
of the dimensions.
The advantage of a materialized data cube is that certain queries become very fast
because they have effectively been precomputed. For example, if you want to know
102 
| 
Chapter 3: Storage and Retrieval


the total sales per store yesterday, you just need to look at the totals along the appro‐
priate dimension—no need to scan millions of rows.
The disadvantage is that a data cube doesn’t have the same flexibility as querying the
raw data. For example, there is no way of calculating which proportion of sales comes
from items that cost more than $100, because the price isn’t one of the dimensions.
Most data warehouses therefore try to keep as much raw data as possible, and use
aggregates such as data cubes only as a performance boost for certain queries.
Summary
In this chapter we tried to get to the bottom of how databases handle storage and
retrieval. What happens when you store data in a database, and what does the data‐
base do when you query for the data again later?
On a high level, we saw that storage engines fall into two broad categories: those opti‐
mized for transaction processing (OLTP), and those optimized for analytics (OLAP).
There are big differences between the access patterns in those use cases:
• OLTP systems are typically user-facing, which means that they may see a huge
volume of requests. In order to handle the load, applications usually only touch a
small number of records in each query. The application requests records using
some kind of key, and the storage engine uses an index to find the data for the
requested key. Disk seek time is often the bottleneck here.
• Data warehouses and similar analytic systems are less well known, because they
are primarily used by business analysts, not by end users. They handle a much
lower volume of queries than OLTP systems, but each query is typically very
demanding, requiring many millions of records to be scanned in a short time.
Disk bandwidth (not seek time) is often the bottleneck here, and columnoriented storage is an increasingly popular solution for this kind of workload.
On the OLTP side, we saw storage engines from two main schools of thought:
• The log-structured school, which only permits appending to files and deleting
obsolete files, but never updates a file that has been written. Bitcask, SSTables,
LSM-trees, LevelDB, Cassandra, HBase, Lucene, and others belong to this group.
• The update-in-place school, which treats the disk as a set of fixed-size pages that
can be overwritten. B-trees are the biggest example of this philosophy, being used
in all major relational databases and also many nonrelational ones.
Log-structured storage engines are a comparatively recent development. Their key
idea is that they systematically turn random-access writes into sequential writes on
disk, which enables higher write throughput due to the performance characteristics
of hard drives and SSDs.
Summary 
| 
103


Finishing off the OLTP side, we did a brief tour through some more complicated
indexing structures, and databases that are optimized for keeping all data in memory.
We then took a detour from the internals of storage engines to look at the high-level
architecture of a typical data warehouse. This background illustrated why analytic
workloads are so different from OLTP: when your queries require sequentially scan‐
ning across a large number of rows, indexes are much less relevant. Instead it
becomes important to encode data very compactly, to minimize the amount of data
that the query needs to read from disk. We discussed how column-oriented storage
helps achieve this goal.
As an application developer, if you’re armed with this knowledge about the internals
of storage engines, you are in a much better position to know which tool is best suited
for your particular application. If you need to adjust a database’s tuning parameters,
this understanding allows you to imagine what effect a higher or a lower value may
have.
Although this chapter couldn’t make you an expert in tuning any one particular stor‐
age engine, it has hopefully equipped you with enough vocabulary and ideas that you
can make sense of the documentation for the database of your choice. 
References
[1] Alfred V. Aho, John E. Hopcroft, and Jeffrey D. Ullman: Data Structures and
Algorithms. Addison-Wesley, 1983. ISBN: 978-0-201-00023-8
[2] Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein:
Introduction to Algorithms, 3rd edition. MIT Press, 2009. ISBN: 978-0-262-53305-8
[3] Justin Sheehy and David Smith: “Bitcask: A Log-Structured Hash Table for Fast
Key/Value Data,” Basho Technologies, April 2010.
[4] Yinan Li, Bingsheng He, Robin Jun Yang, et al.: “Tree Indexing on Solid State
Drives,” Proceedings of the VLDB Endowment, volume 3, number 1, pages 1195–1206,
September 2010.
[5] Goetz Graefe: “Modern B-Tree Techniques,” Foundations and Trends in Data‐
bases, volume 3, number 4, pages 203–402, August 2011. doi:10.1561/1900000028
[6] Jeffrey Dean and Sanjay Ghemawat: “LevelDB Implementation Notes,” lev‐
eldb.googlecode.com.
[7] Dhruba Borthakur: “The History of RocksDB,” rocksdb.blogspot.com, November
24, 2013.
[8] Matteo Bertozzi: “Apache HBase I/O – HFile,” blog.cloudera.com, June, 29 2012.
104 
| 
Chapter 3: Storage and Retrieval


[9] Fay Chang, Jeffrey Dean, Sanjay Ghemawat, et al.: “Bigtable: A Distributed Stor‐
age System for Structured Data,” at 7th USENIX Symposium on Operating System
Design and Implementation (OSDI), November 2006.
[10] Patrick O’Neil, Edward Cheng, Dieter Gawlick, and Elizabeth O’Neil: “The Log-
Structured Merge-Tree (LSM-Tree),” Acta Informatica, volume 33, number 4, pages
351–385, June 1996. doi:10.1007/s002360050048
[11] Mendel Rosenblum and John K. Ousterhout: “The Design and Implementation
of a Log-Structured File System,” ACM Transactions on Computer Systems, volume
10, number 1, pages 26–52, February 1992. doi:10.1145/146941.146943
[12] Adrien Grand: “What Is in a Lucene Index?,” at Lucene/Solr Revolution, Novem‐
ber 14, 2013.
[13] Deepak Kandepet: “Hacking Lucene—The Index Format,” hackerlabs.org, Octo‐
ber 1, 2011.
[14] Michael McCandless: “Visualizing Lucene’s Segment Merges,” blog.mikemccand‐
less.com, February 11, 2011.
[15] Burton H. Bloom: “Space/Time Trade-offs in Hash Coding with Allowable
Errors,” Communications of the ACM, volume 13, number 7, pages 422–426, July
1970. doi:10.1145/362686.362692
[16] “Operating Cassandra: Compaction,” Apache Cassandra Documentation v4.0,
2016.
[17] Rudolf Bayer and Edward M. McCreight: “Organization and Maintenance of
Large Ordered Indices,” Boeing Scientific Research Laboratories, Mathematical and
Information Sciences Laboratory, report no. 20, July 1970.
[18] Douglas Comer: “The Ubiquitous B-Tree,” ACM Computing Surveys, volume 11,
number 2, pages 121–137, June 1979. doi:10.1145/356770.356776
[19] Emmanuel Goossaert: “Coding for SSDs,” codecapsule.com, February 12, 2014.
[20] C. Mohan and Frank Levine: “ARIES/IM: An Efficient and High Concurrency
Index Management Method Using Write-Ahead Logging,” at ACM International
Conference 
on 
Management 
of 
Data 
(SIGMOD), 
June 
1992. 
doi:
10.1145/130283.130338
[21] Howard Chu: “LDAP at Lightning Speed,” at Build Stuff ’14, November 2014.
[22] Bradley C. Kuszmaul: “A Comparison of Fractal Trees to Log-Structured Merge
(LSM) Trees,” tokutek.com, April 22, 2014.
[23] Manos Athanassoulis, Michael S. Kester, Lukas M. Maas, et al.: “Designing
Access Methods: The RUM Conjecture,” at 19th International Conference on Extend‐
ing Database Technology (EDBT), March 2016. doi:10.5441/002/edbt.2016.42
Summary 
| 
105


[24] Peter Zaitsev: “Innodb Double Write,” percona.com, August 4, 2006.
[25] Tomas Vondra: “On the Impact of Full-Page Writes,” blog.2ndquadrant.com,
November 23, 2016.
[26] Mark Callaghan: “The Advantages of an LSM vs a B-Tree,” smalldatum.blog‐
spot.co.uk, January 19, 2016.
[27] Mark Callaghan: “Choosing Between Efficiency and Performance with
RocksDB,” at Code Mesh, November 4, 2016.
[28] Michi Mutsuzaki: “MySQL vs. LevelDB,” github.com, August 2011.
[29] Benjamin Coverston, Jonathan Ellis, et al.: “CASSANDRA-1608: Redesigned
Compaction, issues.apache.org, July 2011.
[30] Igor Canadi, Siying Dong, and Mark Callaghan: “RocksDB Tuning Guide,” git‐
hub.com, 2016.
[31] MySQL 5.7 Reference Manual. Oracle, 2014.
[32] Books Online for SQL Server 2012. Microsoft, 2012.
[33] Joe Webb: “Using Covering Indexes to Improve Query Performance,” simpletalk.com, 29 September 2008.
[34] Frank Ramsak, Volker Markl, Robert Fenk, et al.: “Integrating the UB-Tree into
a Database System Kernel,” at 26th International Conference on Very Large Data
Bases (VLDB), September 2000.
[35] The PostGIS Development Group: “PostGIS 2.1.2dev Manual,” postgis.net, 2014.
[36] Robert Escriva, Bernard Wong, and Emin Gün Sirer: “HyperDex: A Distributed,
Searchable Key-Value Store,” at ACM SIGCOMM Conference, August 2012. doi:
10.1145/2377677.2377681
[37] Michael McCandless: “Lucene’s FuzzyQuery Is 100 Times Faster in 4.0,”
blog.mikemccandless.com, March 24, 2011.
[38] Steffen Heinz, Justin Zobel, and Hugh E. Williams: “Burst Tries: A Fast, Efficient
Data Structure for String Keys,” ACM Transactions on Information Systems, volume
20, number 2, pages 192–223, April 2002. doi:10.1145/506309.506312
[39] Klaus U. Schulz and Stoyan Mihov: “Fast String Correction with Levenshtein
Automata,” International Journal on Document Analysis and Recognition, volume 5,
number 1, pages 67–85, November 2002. doi:10.1007/s10032-002-0082-8
[40] Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schütze: Introduc‐
tion to Information Retrieval. Cambridge University Press, 2008. ISBN:
978-0-521-86571-5, available online at nlp.stanford.edu/IR-book
106 
| 
Chapter 3: Storage and Retrieval


[41] Michael Stonebraker, Samuel Madden, Daniel J. Abadi, et al.: “The End of an
Architectural Era (It’s Time for a Complete Rewrite),” at 33rd International Confer‐
ence on Very Large Data Bases (VLDB), September 2007.
[42] “VoltDB Technical Overview White Paper,” VoltDB, 2014.
[43] Stephen M. Rumble, Ankita Kejriwal, and John K. Ousterhout: “Log-Structured
Memory for DRAM-Based Storage,” at 12th USENIX Conference on File and Storage
Technologies (FAST), February 2014.
[44] Stavros Harizopoulos, Daniel J. Abadi, Samuel Madden, and Michael Stone‐
braker: “OLTP Through the Looking Glass, and What We Found There,” at ACM
International Conference on Management of Data (SIGMOD), June 2008. doi:
10.1145/1376616.1376713
[45] Justin DeBrabant, Andrew Pavlo, Stephen Tu, et al.: “Anti-Caching: A New
Approach to Database Management System Architecture,” Proceedings of the VLDB
Endowment, volume 6, number 14, pages 1942–1953, September 2013.
[46] Joy Arulraj, Andrew Pavlo, and Subramanya R. Dulloor: “Let’s Talk About Stor‐
age & Recovery Methods for Non-Volatile Memory Database Systems,” at ACM
International Conference on Management of Data (SIGMOD), June 2015. doi:
10.1145/2723372.2749441
[47] Edgar F. Codd, S. B. Codd, and C. T. Salley: “Providing OLAP to User-Analysts:
An IT Mandate,” E. F. Codd Associates, 1993.
[48] Surajit Chaudhuri and Umeshwar Dayal: “An Overview of Data Warehousing
and OLAP Technology,” ACM SIGMOD Record, volume 26, number 1, pages 65–74,
March 1997. doi:10.1145/248603.248616
[49] Per-Åke Larson, Cipri Clinciu, Campbell Fraser, et al.: “Enhancements to SQL
Server Column Stores,” at ACM International Conference on Management of Data
(SIGMOD), June 2013.
[50] Franz Färber, Norman May, Wolfgang Lehner, et al.: “The SAP HANA Database
– An Architecture Overview,” IEEE Data Engineering Bulletin, volume 35, number 1,
pages 28–33, March 2012.
[51] Michael Stonebraker: “The Traditional RDBMS Wisdom Is (Almost Certainly)
All Wrong,” presentation at EPFL, May 2013.
[52] Daniel J. Abadi: “Classifying the SQL-on-Hadoop Solutions,” hadapt.com, Octo‐
ber 2, 2013.
[53] Marcel Kornacker, Alexander Behm, Victor Bittorf, et al.: “Impala: A Modern,
Open-Source SQL Engine for Hadoop,” at 7th Biennial Conference on Innovative
Data Systems Research (CIDR), January 2015.
Summary 
| 
107


[54] Sergey Melnik, Andrey Gubarev, Jing Jing Long, et al.: “Dremel: Interactive
Analysis of Web-Scale Datasets,” at 36th International Conference on Very Large Data
Bases (VLDB), pages 330–339, September 2010.
[55] Ralph Kimball and Margy Ross: The Data Warehouse Toolkit: The Definitive
Guide to Dimensional Modeling, 3rd edition. John Wiley & Sons, July 2013. ISBN:
978-1-118-53080-1
[56] Derrick Harris: “Why Apple, eBay, and Walmart Have Some of the Biggest Data
Warehouses You’ve Ever Seen,” gigaom.com, March 27, 2013.
[57] Julien Le Dem: “Dremel Made Simple with Parquet,” blog.twitter.com, Septem‐
ber 11, 2013.
[58] Daniel J. Abadi, Peter Boncz, Stavros Harizopoulos, et al.: “The Design and
Implementation of Modern Column-Oriented Database Systems,” Foundations and
Trends in Databases, volume 5, number 3, pages 197–280, December 2013. doi:
10.1561/1900000024
[59] Peter Boncz, Marcin Zukowski, and Niels Nes: “MonetDB/X100: Hyper-
Pipelining Query Execution,” at 2nd Biennial Conference on Innovative Data Systems
Research (CIDR), January 2005.
[60] Jingren Zhou and Kenneth A. Ross: “Implementing Database Operations Using
SIMD Instructions,” at ACM International Conference on Management of Data (SIG‐
MOD), pages 145–156, June 2002. doi:10.1145/564691.564709
[61] Michael Stonebraker, Daniel J. Abadi, Adam Batkin, et al.: “C-Store: A Columnoriented DBMS,” at 31st International Conference on Very Large Data Bases (VLDB),
pages 553–564, September 2005.
[62] Andrew Lamb, Matt Fuller, Ramakrishna Varadarajan, et al.: “The Vertica Ana‐
lytic Database: C-Store 7 Years Later,” Proceedings of the VLDB Endowment, volume
5, number 12, pages 1790–1801, August 2012.
[63] Julien Le Dem and Nong Li: “Efficient Data Storage for Analytics with Apache
Parquet 2.0,” at Hadoop Summit, San Jose, June 2014.
[64] Jim Gray, Surajit Chaudhuri, Adam Bosworth, et al.: “Data Cube: A Relational
Aggregation Operator Generalizing Group-By, Cross-Tab, and Sub-Totals,” Data
Mining and Knowledge Discovery, volume 1, number 1, pages 29–53, March 2007.
doi:10.1023/A:1009726021843
108 
| 
Chapter 3: Storage and Retrieval






CHAPTER 4
Encoding and Evolution
Everything changes and nothing stands still.
—Heraclitus of Ephesus, as quoted by Plato in Cratylus (360 BCE)
Applications inevitably change over time. Features are added or modified as new
products are launched, user requirements become better understood, or business cir‐
cumstances change. In Chapter 1 we introduced the idea of evolvability: we should
aim to build systems that make it easy to adapt to change (see “Evolvability: Making
Change Easy” on page 21).
In most cases, a change to an application’s features also requires a change to data that
it stores: perhaps a new field or record type needs to be captured, or perhaps existing
data needs to be presented in a new way.
The data models we discussed in Chapter 2 have different ways of coping with such
change. Relational databases generally assume that all data in the database conforms
to one schema: although that schema can be changed (through schema migrations;
i.e., ALTER statements), there is exactly one schema in force at any one point in time.
By contrast, schema-on-read (“schemaless”) databases don’t enforce a schema, so the
database can contain a mixture of older and newer data formats written at different
times (see “Schema flexibility in the document model” on page 39).
When a data format or schema changes, a corresponding change to application code
often needs to happen (for example, you add a new field to a record, and the applica‐
tion code starts reading and writing that field). However, in a large application, code
changes often cannot happen instantaneously:
111


• With server-side applications you may want to perform a rolling upgrade (also
known as a staged rollout), deploying the new version to a few nodes at a time,
checking whether the new version is running smoothly, and gradually working
your way through all the nodes. This allows new versions to be deployed without
service downtime, and thus encourages more frequent releases and better evolva‐
bility.
• With client-side applications you’re at the mercy of the user, who may not install
the update for some time.
This means that old and new versions of the code, and old and new data formats,
may potentially all coexist in the system at the same time. In order for the system to
continue running smoothly, we need to maintain compatibility in both directions:
Backward compatibility
Newer code can read data that was written by older code.
Forward compatibility
Older code can read data that was written by newer code.
Backward compatibility is normally not hard to achieve: as author of the newer code,
you know the format of data written by older code, and so you can explicitly handle it
(if necessary by simply keeping the old code to read the old data). Forward compati‐
bility can be trickier, because it requires older code to ignore additions made by a
newer version of the code.
In this chapter we will look at several formats for encoding data, including JSON,
XML, Protocol Buffers, Thrift, and Avro. In particular, we will look at how they han‐
dle schema changes and how they support systems where old and new data and code
need to coexist. We will then discuss how those formats are used for data storage and
for communication: in web services, Representational State Transfer (REST), and
remote procedure calls (RPC), as well as message-passing systems such as actors and
message queues.
Formats for Encoding Data
Programs usually work with data in (at least) two different representations:
1. In memory, data is kept in objects, structs, lists, arrays, hash tables, trees, and so
on. These data structures are optimized for efficient access and manipulation by
the CPU (typically using pointers).
2. When you want to write data to a file or send it over the network, you have to
encode it as some kind of self-contained sequence of bytes (for example, a JSON
document). Since a pointer wouldn’t make sense to any other process, this
112 
| 
Chapter 4: Encoding and Evolution


i. With the exception of some special cases, such as certain memory-mapped files or when operating directly
on compressed data (as described in “Column Compression” on page 97).
ii. Note that encoding has nothing to do with encryption. We don’t discuss encryption in this book.
sequence-of-bytes representation looks quite different from the data structures
that are normally used in memory.i
Thus, we need some kind of translation between the two representations. The trans‐
lation from the in-memory representation to a byte sequence is called encoding (also
known as serialization or marshalling), and the reverse is called decoding (parsing,
deserialization, unmarshalling).ii
Terminology clash
Serialization is unfortunately also used in the context of transac‐
tions (see Chapter 7), with a completely different meaning. To
avoid overloading the word we’ll stick with encoding in this book,
even though serialization is perhaps a more common term.
As this is such a common problem, there are a myriad different libraries and encod‐
ing formats to choose from. Let’s do a brief overview.
Language-Specific Formats
Many programming languages come with built-in support for encoding in-memory
objects into byte sequences. For example, Java has java.io.Serializable [1], Ruby
has Marshal [2], Python has pickle [3], and so on. Many third-party libraries also
exist, such as Kryo for Java [4].
These encoding libraries are very convenient, because they allow in-memory objects
to be saved and restored with minimal additional code. However, they also have a
number of deep problems:
• The encoding is often tied to a particular programming language, and reading
the data in another language is very difficult. If you store or transmit data in such
an encoding, you are committing yourself to your current programming lan‐
guage for potentially a very long time, and precluding integrating your systems
with those of other organizations (which may use different languages).
• In order to restore data in the same object types, the decoding process needs to
be able to instantiate arbitrary classes. This is frequently a source of security
problems [5]: if an attacker can get your application to decode an arbitrary byte
sequence, they can instantiate arbitrary classes, which in turn often allows them
to do terrible things such as remotely executing arbitrary code [6, 7].
Formats for Encoding Data 
| 
113


• Versioning data is often an afterthought in these libraries: as they are intended
for quick and easy encoding of data, they often neglect the inconvenient prob‐
lems of forward and backward compatibility.
• Efficiency (CPU time taken to encode or decode, and the size of the encoded
structure) is also often an afterthought. For example, Java’s built-in serialization
is notorious for its bad performance and bloated encoding [8].
For these reasons it’s generally a bad idea to use your language’s built-in encoding for
anything other than very transient purposes.
JSON, XML, and Binary Variants
Moving to standardized encodings that can be written and read by many program‐
ming languages, JSON and XML are the obvious contenders. They are widely known,
widely supported, and almost as widely disliked. XML is often criticized for being too
verbose and unnecessarily complicated [9]. JSON’s popularity is mainly due to its
built-in support in web browsers (by virtue of being a subset of JavaScript) and sim‐
plicity relative to XML. CSV is another popular language-independent format, albeit
less powerful.
JSON, XML, and CSV are textual formats, and thus somewhat human-readable
(although the syntax is a popular topic of debate). Besides the superficial syntactic
issues, they also have some subtle problems:
• There is a lot of ambiguity around the encoding of numbers. In XML and CSV,
you cannot distinguish between a number and a string that happens to consist of
digits (except by referring to an external schema). JSON distinguishes strings and
numbers, but it doesn’t distinguish integers and floating-point numbers, and it
doesn’t specify a precision.
This is a problem when dealing with large numbers; for example, integers greater
than 253 cannot be exactly represented in an IEEE 754 double-precision floatingpoint number, so such numbers become inaccurate when parsed in a language
that uses floating-point numbers (such as JavaScript). An example of numbers
larger than 253 occurs on Twitter, which uses a 64-bit number to identify each
tweet. The JSON returned by Twitter’s API includes tweet IDs twice, once as a
JSON number and once as a decimal string, to work around the fact that the
numbers are not correctly parsed by JavaScript applications [10].
• JSON and XML have good support for Unicode character strings (i.e., humanreadable text), but they don’t support binary strings (sequences of bytes without
a character encoding). Binary strings are a useful feature, so people get around
this limitation by encoding the binary data as text using Base64. The schema is
then used to indicate that the value should be interpreted as Base64-encoded.
This works, but it’s somewhat hacky and increases the data size by 33%.
114 
| 
Chapter 4: Encoding and Evolution


• There is optional schema support for both XML [11] and JSON [12]. These
schema languages are quite powerful, and thus quite complicated to learn and
implement. Use of XML schemas is fairly widespread, but many JSON-based
tools don’t bother using schemas. Since the correct interpretation of data (such
as numbers and binary strings) depends on information in the schema, applica‐
tions that don’t use XML/JSON schemas need to potentially hardcode the appro‐
priate encoding/decoding logic instead.
• CSV does not have any schema, so it is up to the application to define the mean‐
ing of each row and column. If an application change adds a new row or column,
you have to handle that change manually. CSV is also a quite vague format (what
happens if a value contains a comma or a newline character?). Although its
escaping rules have been formally specified [13], not all parsers implement them
correctly.
Despite these flaws, JSON, XML, and CSV are good enough for many purposes. It’s
likely that they will remain popular, especially as data interchange formats (i.e., for
sending data from one organization to another). In these situations, as long as people
agree on what the format is, it often doesn’t matter how pretty or efficient the format
is. The difficulty of getting different organizations to agree on anything outweighs
most other concerns.
Binary encoding
For data that is used only internally within your organization, there is less pressure to
use a lowest-common-denominator encoding format. For example, you could choose
a format that is more compact or faster to parse. For a small dataset, the gains are
negligible, but once you get into the terabytes, the choice of data format can have a
big impact.
JSON is less verbose than XML, but both still use a lot of space compared to binary
formats. This observation led to the development of a profusion of binary encodings
for JSON (MessagePack, BSON, BJSON, UBJSON, BISON, and Smile, to name a few)
and for XML (WBXML and Fast Infoset, for example). These formats have been
adopted in various niches, but none of them are as widely adopted as the textual ver‐
sions of JSON and XML.
Some of these formats extend the set of datatypes (e.g., distinguishing integers and
floating-point numbers, or adding support for binary strings), but otherwise they
keep the JSON/XML data model unchanged. In particular, since they don’t prescribe
a schema, they need to include all the object field names within the encoded data.
That is, in a binary encoding of the JSON document in Example 4-1, they will need to
include the strings userName, favoriteNumber, and interests somewhere.
Formats for Encoding Data 
| 
115


Example 4-1. Example record which we will encode in several binary formats in this
chapter
{
    "userName": "Martin",
    "favoriteNumber": 1337,
    "interests": ["daydreaming", "hacking"]
}
Let’s look at an example of MessagePack, a binary encoding for JSON. Figure 4-1
shows the byte sequence that you get if you encode the JSON document in
Example 4-1 with MessagePack [14]. The first few bytes are as follows:
1. The first byte, 0x83, indicates that what follows is an object (top four bits = 0x80)
with three fields (bottom four bits = 0x03). (In case you’re wondering what hap‐
pens if an object has more than 15 fields, so that the number of fields doesn’t fit
in four bits, it then gets a different type indicator, and the number of fields is
encoded in two or four bytes.)
2. The second byte, 0xa8, indicates that what follows is a string (top four bits =
0xa0) that is eight bytes long (bottom four bits = 0x08).
3. The next eight bytes are the field name userName in ASCII. Since the length was
indicated previously, there’s no need for any marker to tell us where the string
ends (or any escaping).
4. The next seven bytes encode the six-letter string value Martin with a prefix 0xa6,
and so on.
The binary encoding is 66 bytes long, which is only a little less than the 81 bytes taken
by the textual JSON encoding (with whitespace removed). All the binary encodings of
JSON are similar in this regard. It’s not clear whether such a small space reduction
(and perhaps a speedup in parsing) is worth the loss of human-readability.
In the following sections we will see how we can do much better, and encode the
same record in just 32 bytes.
116 
| 
Chapter 4: Encoding and Evolution


Figure 4-1. Example record (Example 4-1) encoded using MessagePack.
Thrift and Protocol Buffers
Apache Thrift [15] and Protocol Buffers (protobuf) [16] are binary encoding libraries
that are based on the same principle. Protocol Buffers was originally developed at
Google, Thrift was originally developed at Facebook, and both were made open
source in 2007–08 [17].
Both Thrift and Protocol Buffers require a schema for any data that is encoded. To
encode the data in Example 4-1 in Thrift, you would describe the schema in the
Thrift interface definition language (IDL) like this:
struct Person {
  1: required string       userName,
  2: optional i64          favoriteNumber,
  3: optional list<string> interests
}
Formats for Encoding Data 
| 
117


iii. Actually, it has three—BinaryProtocol, CompactProtocol, and DenseProtocol—although DenseProtocol
is only supported by the C++ implementation, so it doesn’t count as cross-language [18]. Besides those, it also
has two different JSON-based encoding formats [19]. What fun!
The equivalent schema definition for Protocol Buffers looks very similar:
message Person {
    required string user_name       = 1;
    optional int64  favorite_number = 2;
    repeated string interests       = 3;
}
Thrift and Protocol Buffers each come with a code generation tool that takes a
schema definition like the ones shown here, and produces classes that implement the
schema in various programming languages [18]. Your application code can call this
generated code to encode or decode records of the schema.
What does data encoded with this schema look like? Confusingly, Thrift has two dif‐
ferent binary encoding formats,iii called BinaryProtocol and CompactProtocol, respec‐
tively. Let’s look at BinaryProtocol first. Encoding Example 4-1 in that format takes
59 bytes, as shown in Figure 4-2 [19].
Figure 4-2. Example record encoded using Thrift’s BinaryProtocol.
118 
| 
Chapter 4: Encoding and Evolution


Similarly to Figure 4-1, each field has a type annotation (to indicate whether it is a
string, integer, list, etc.) and, where required, a length indication (length of a string,
number of items in a list). The strings that appear in the data (“Martin”, “daydream‐
ing”, “hacking”) are also encoded as ASCII (or rather, UTF-8), similar to before.
The big difference compared to Figure 4-1 is that there are no field names (userName,
favoriteNumber, interests). Instead, the encoded data contains field tags, which are
numbers (1, 2, and 3). Those are the numbers that appear in the schema definition.
Field tags are like aliases for fields—they are a compact way of saying what field we’re
talking about, without having to spell out the field name.
The Thrift CompactProtocol encoding is semantically equivalent to BinaryProtocol,
but as you can see in Figure 4-3, it packs the same information into only 34 bytes. It
does this by packing the field type and tag number into a single byte, and by using
variable-length integers. Rather than using a full eight bytes for the number 1337, it is
encoded in two bytes, with the top bit of each byte used to indicate whether there are
still more bytes to come. This means numbers between –64 and 63 are encoded in
one byte, numbers between –8192 and 8191 are encoded in two bytes, etc. Bigger
numbers use more bytes.
Figure 4-3. Example record encoded using Thrift’s CompactProtocol.
Finally, Protocol Buffers (which has only one binary encoding format) encodes the
same data as shown in Figure 4-4. It does the bit packing slightly differently, but is
Formats for Encoding Data 
| 
119


otherwise very similar to Thrift’s CompactProtocol. Protocol Buffers fits the same
record in 33 bytes.
Figure 4-4. Example record encoded using Protocol Buffers.
One detail to note: in the schemas shown earlier, each field was marked either
required or optional, but this makes no difference to how the field is encoded
(nothing in the binary data indicates whether a field was required). The difference is
simply that required enables a runtime check that fails if the field is not set, which
can be useful for catching bugs.
Field tags and schema evolution
We said previously that schemas inevitably need to change over time. We call this
schema evolution. How do Thrift and Protocol Buffers handle schema changes while
keeping backward and forward compatibility?
As you can see from the examples, an encoded record is just the concatenation of its
encoded fields. Each field is identified by its tag number (the numbers 1, 2, 3 in the
sample schemas) and annotated with a datatype (e.g., string or integer). If a field
value is not set, it is simply omitted from the encoded record. From this you can see
that field tags are critical to the meaning of the encoded data. You can change the
name of a field in the schema, since the encoded data never refers to field names, but
you cannot change a field’s tag, since that would make all existing encoded data
invalid.
120 
| 
Chapter 4: Encoding and Evolution


You can add new fields to the schema, provided that you give each field a new tag
number. If old code (which doesn’t know about the new tag numbers you added)
tries to read data written by new code, including a new field with a tag number it
doesn’t recognize, it can simply ignore that field. The datatype annotation allows the
parser to determine how many bytes it needs to skip. This maintains forward com‐
patibility: old code can read records that were written by new code.
What about backward compatibility? As long as each field has a unique tag number,
new code can always read old data, because the tag numbers still have the same
meaning. The only detail is that if you add a new field, you cannot make it required.
If you were to add a field and make it required, that check would fail if new code read
data written by old code, because the old code will not have written the new field that
you added. Therefore, to maintain backward compatibility, every field you add after
the initial deployment of the schema must be optional or have a default value.
Removing a field is just like adding a field, with backward and forward compatibility
concerns reversed. That means you can only remove a field that is optional (a
required field can never be removed), and you can never use the same tag number
again (because you may still have data written somewhere that includes the old tag
number, and that field must be ignored by new code). 
Datatypes and schema evolution
What about changing the datatype of a field? That may be possible—check the docu‐
mentation for details—but there is a risk that values will lose precision or get trunca‐
ted. For example, say you change a 32-bit integer into a 64-bit integer. New code can
easily read data written by old code, because the parser can fill in any missing bits
with zeros. However, if old code reads data written by new code, the old code is still
using a 32-bit variable to hold the value. If the decoded 64-bit value won’t fit in 32
bits, it will be truncated.
A curious detail of Protocol Buffers is that it does not have a list or array datatype,
but instead has a repeated marker for fields (which is a third option alongside
required and optional). As you can see in Figure 4-4, the encoding of a repeated
field is just what it says on the tin: the same field tag simply appears multiple times in
the record. This has the nice effect that it’s okay to change an optional (singlevalued) field into a repeated (multi-valued) field. New code reading old data sees a
list with zero or one elements (depending on whether the field was present); old code
reading new data sees only the last element of the list.
Thrift has a dedicated list datatype, which is parameterized with the datatype of the
list elements. This does not allow the same evolution from single-valued to multivalued as Protocol Buffers does, but it has the advantage of supporting nested lists. 
Formats for Encoding Data 
| 
121


Avro
Apache Avro [20] is another binary encoding format that is interestingly different
from Protocol Buffers and Thrift. It was started in 2009 as a subproject of Hadoop, as
a result of Thrift not being a good fit for Hadoop’s use cases [21].
Avro also uses a schema to specify the structure of the data being encoded. It has two
schema languages: one (Avro IDL) intended for human editing, and one (based on
JSON) that is more easily machine-readable.
Our example schema, written in Avro IDL, might look like this:
record Person {
    string               userName;
    union { null, long } favoriteNumber = null;
    array<string>        interests;
}
The equivalent JSON representation of that schema is as follows:
{
    "type": "record",
    "name": "Person",
    "fields": [
        {"name": "userName",       "type": "string"},
        {"name": "favoriteNumber", "type": ["null", "long"], "default": null},
        {"name": "interests",      "type": {"type": "array", "items": "string"}}
    ]
}
First of all, notice that there are no tag numbers in the schema. If we encode our
example record (Example 4-1) using this schema, the Avro binary encoding is just 32
bytes long—the most compact of all the encodings we have seen. The breakdown of
the encoded byte sequence is shown in Figure 4-5.
If you examine the byte sequence, you can see that there is nothing to identify fields
or their datatypes. The encoding simply consists of values concatenated together. A
string is just a length prefix followed by UTF-8 bytes, but there’s nothing in the enco‐
ded data that tells you that it is a string. It could just as well be an integer, or some‐
thing else entirely. An integer is encoded using a variable-length encoding (the same
as Thrift’s CompactProtocol).
122 
| 
Chapter 4: Encoding and Evolution


Figure 4-5. Example record encoded using Avro.
To parse the binary data, you go through the fields in the order that they appear in
the schema and use the schema to tell you the datatype of each field. This means that
the binary data can only be decoded correctly if the code reading the data is using the
exact same schema as the code that wrote the data. Any mismatch in the schema
between the reader and the writer would mean incorrectly decoded data.
So, how does Avro support schema evolution?
The writer’s schema and the reader’s schema
With Avro, when an application wants to encode some data (to write it to a file or
database, to send it over the network, etc.), it encodes the data using whatever version
of the schema it knows about—for example, that schema may be compiled into the
application. This is known as the writer’s schema.
When an application wants to decode some data (read it from a file or database,
receive it from the network, etc.), it is expecting the data to be in some schema, which
is known as the reader’s schema. That is the schema the application code is relying on
—code may have been generated from that schema during the application’s build
process.
The key idea with Avro is that the writer’s schema and the reader’s schema don’t have
to be the same—they only need to be compatible. When data is decoded (read), the
Formats for Encoding Data 
| 
123


Avro library resolves the differences by looking at the writer’s schema and the
reader’s schema side by side and translating the data from the writer’s schema into
the reader’s schema. The Avro specification [20] defines exactly how this resolution
works, and it is illustrated in Figure 4-6.
For example, it’s no problem if the writer’s schema and the reader’s schema have
their fields in a different order, because the schema resolution matches up the fields
by field name. If the code reading the data encounters a field that appears in the
writer’s schema but not in the reader’s schema, it is ignored. If the code reading the
data expects some field, but the writer’s schema does not contain a field of that name,
it is filled in with a default value declared in the reader’s schema.
Figure 4-6. An Avro reader resolves differences between the writer’s schema and the
reader’s schema.
Schema evolution rules
With Avro, forward compatibility means that you can have a new version of the
schema as writer and an old version of the schema as reader. Conversely, backward
compatibility means that you can have a new version of the schema as reader and an
old version as writer.
To maintain compatibility, you may only add or remove a field that has a default
value. (The field favoriteNumber in our Avro schema has a default value of null.)
For example, say you add a field with a default value, so this new field exists in the
new schema but not the old one. When a reader using the new schema reads a record
written with the old schema, the default value is filled in for the missing field.
If you were to add a field that has no default value, new readers wouldn’t be able to
read data written by old writers, so you would break backward compatibility. If you
were to remove a field that has no default value, old readers wouldn’t be able to read
data written by new writers, so you would break forward compatibility.
124 
| 
Chapter 4: Encoding and Evolution


iv. To be precise, the default value must be of the type of the first branch of the union, although this is a
specific limitation of Avro, not a general feature of union types.
In some programming languages, null is an acceptable default for any variable, but
this is not the case in Avro: if you want to allow a field to be null, you have to use a
union type. For example, union { null, long, string } field; indicates that
field can be a number, or a string, or null. You can only use null as a default value if
it is one of the branches of the union.iv This is a little more verbose than having every‐
thing nullable by default, but it helps prevent bugs by being explicit about what can
and cannot be null [22].
Consequently, Avro doesn’t have optional and required markers in the same way as
Protocol Buffers and Thrift do (it has union types and default values instead).
Changing the datatype of a field is possible, provided that Avro can convert the type.
Changing the name of a field is possible but a little tricky: the reader’s schema can
contain aliases for field names, so it can match an old writer’s schema field names
against the aliases. This means that changing a field name is backward compatible but
not forward compatible. Similarly, adding a branch to a union type is backward com‐
patible but not forward compatible.
But what is the writer’s schema?
There is an important question that we’ve glossed over so far: how does the reader
know the writer’s schema with which a particular piece of data was encoded? We
can’t just include the entire schema with every record, because the schema would
likely be much bigger than the encoded data, making all the space savings from the
binary encoding futile.
The answer depends on the context in which Avro is being used. To give a few exam‐
ples:
Large file with lots of records
A common use for Avro—especially in the context of Hadoop—is for storing a
large file containing millions of records, all encoded with the same schema. (We
will discuss this kind of situation in Chapter 10.) In this case, the writer of that
file can just include the writer’s schema once at the beginning of the file. Avro
specifies a file format (object container files) to do this.
Database with individually written records
In a database, different records may be written at different points in time using
different writer’s schemas—you cannot assume that all the records will have the
same schema. The simplest solution is to include a version number at the begin‐
ning of every encoded record, and to keep a list of schema versions in your data‐
Formats for Encoding Data 
| 
125


base. A reader can fetch a record, extract the version number, and then fetch the
writer’s schema for that version number from the database. Using that writer’s
schema, it can decode the rest of the record. (Espresso [23] works this way, for
example.)
Sending records over a network connection
When two processes are communicating over a bidirectional network connec‐
tion, they can negotiate the schema version on connection setup and then use
that schema for the lifetime of the connection. The Avro RPC protocol (see
“Dataflow Through Services: REST and RPC” on page 131) works like this.
A database of schema versions is a useful thing to have in any case, since it acts as
documentation and gives you a chance to check schema compatibility [24]. As the
version number, you could use a simple incrementing integer, or you could use a
hash of the schema.
Dynamically generated schemas
One advantage of Avro’s approach, compared to Protocol Buffers and Thrift, is that
the schema doesn’t contain any tag numbers. But why is this important? What’s the
problem with keeping a couple of numbers in the schema?
The difference is that Avro is friendlier to dynamically generated schemas. For exam‐
ple, say you have a relational database whose contents you want to dump to a file, and
you want to use a binary format to avoid the aforementioned problems with textual
formats (JSON, CSV, SQL). If you use Avro, you can fairly easily generate an Avro
schema (in the JSON representation we saw earlier) from the relational schema and
encode the database contents using that schema, dumping it all to an Avro object
container file [25]. You generate a record schema for each database table, and each
column becomes a field in that record. The column name in the database maps to the
field name in Avro.
Now, if the database schema changes (for example, a table has one column added and
one column removed), you can just generate a new Avro schema from the updated
database schema and export data in the new Avro schema. The data export process
does not need to pay any attention to the schema change—it can simply do the
schema conversion every time it runs. Anyone who reads the new data files will see
that the fields of the record have changed, but since the fields are identified by name,
the updated writer’s schema can still be matched up with the old reader’s schema.
By contrast, if you were using Thrift or Protocol Buffers for this purpose, the field
tags would likely have to be assigned by hand: every time the database schema
changes, an administrator would have to manually update the mapping from data‐
base column names to field tags. (It might be possible to automate this, but the
schema generator would have to be very careful to not assign previously used field
126 
| 
Chapter 4: Encoding and Evolution


tags.) This kind of dynamically generated schema simply wasn’t a design goal of
Thrift or Protocol Buffers, whereas it was for Avro.
Code generation and dynamically typed languages
Thrift and Protocol Buffers rely on code generation: after a schema has been defined,
you can generate code that implements this schema in a programming language of
your choice. This is useful in statically typed languages such as Java, C++, or C#,
because it allows efficient in-memory structures to be used for decoded data, and it
allows type checking and autocompletion in IDEs when writing programs that access
the data structures.
In dynamically typed programming languages such as JavaScript, Ruby, or Python,
there is not much point in generating code, since there is no compile-time type
checker to satisfy. Code generation is often frowned upon in these languages, since
they otherwise avoid an explicit compilation step. Moreover, in the case of a dynami‐
cally generated schema (such as an Avro schema generated from a database table),
code generation is an unnecessarily obstacle to getting to the data.
Avro provides optional code generation for statically typed programming languages,
but it can be used just as well without any code generation. If you have an object con‐
tainer file (which embeds the writer’s schema), you can simply open it using the Avro
library and look at the data in the same way as you could look at a JSON file. The file
is self-describing since it includes all the necessary metadata.
This property is especially useful in conjunction with dynamically typed data pro‐
cessing languages like Apache Pig [26]. In Pig, you can just open some Avro files,
start analyzing them, and write derived datasets to output files in Avro format
without even thinking about schemas. 
The Merits of Schemas
As we saw, Protocol Buffers, Thrift, and Avro all use a schema to describe a binary
encoding format. Their schema languages are much simpler than XML Schema or
JSON Schema, which support much more detailed validation rules (e.g., “the string
value of this field must match this regular expression” or “the integer value of this
field must be between 0 and 100”). As Protocol Buffers, Thrift, and Avro are simpler
to implement and simpler to use, they have grown to support a fairly wide range of
programming languages.
The ideas on which these encodings are based are by no means new. For example,
they have a lot in common with ASN.1, a schema definition language that was first
standardized in 1984 [27]. It was used to define various network protocols, and its
binary encoding (DER) is still used to encode SSL certificates (X.509), for example
[28]. ASN.1 supports schema evolution using tag numbers, similar to Protocol Buf‐
Formats for Encoding Data 
| 
127


fers and Thrift [29]. However, it’s also very complex and badly documented, so
ASN.1 is probably not a good choice for new applications.
Many data systems also implement some kind of proprietary binary encoding for
their data. For example, most relational databases have a network protocol over
which you can send queries to the database and get back responses. Those protocols
are generally specific to a particular database, and the database vendor provides a
driver (e.g., using the ODBC or JDBC APIs) that decodes responses from the data‐
base’s network protocol into in-memory data structures.
So, we can see that although textual data formats such as JSON, XML, and CSV are
widespread, binary encodings based on schemas are also a viable option. They have a
number of nice properties:
• They can be much more compact than the various “binary JSON” variants, since
they can omit field names from the encoded data.
• The schema is a valuable form of documentation, and because the schema is
required for decoding, you can be sure that it is up to date (whereas manually
maintained documentation may easily diverge from reality).
• Keeping a database of schemas allows you to check forward and backward com‐
patibility of schema changes, before anything is deployed.
• For users of statically typed programming languages, the ability to generate code
from the schema is useful, since it enables type checking at compile time.
In summary, schema evolution allows the same kind of flexibility as schemaless/
schema-on-read JSON databases provide (see “Schema flexibility in the document
model” on page 39), while also providing better guarantees about your data and bet‐
ter tooling. 
Modes of Dataflow
At the beginning of this chapter we said that whenever you want to send some data to
another process with which you don’t share memory—for example, whenever you
want to send data over the network or write it to a file—you need to encode it as a
sequence of bytes. We then discussed a variety of different encodings for doing this.
We talked about forward and backward compatibility, which are important for evolv‐
ability (making change easy by allowing you to upgrade different parts of your system
independently, and not having to change everything at once). Compatibility is a rela‐
tionship between one process that encodes the data, and another process that decodes
it.
128 
| 
Chapter 4: Encoding and Evolution


That’s a fairly abstract idea—there are many ways data can flow from one process to
another. Who encodes the data, and who decodes it? In the rest of this chapter we
will explore some of the most common ways how data flows between processes:
• Via databases (see “Dataflow Through Databases” on page 129)
• Via service calls (see “Dataflow Through Services: REST and RPC” on page 131)
• Via asynchronous message passing (see “Message-Passing Dataflow” on page 136)
Dataflow Through Databases
In a database, the process that writes to the database encodes the data, and the pro‐
cess that reads from the database decodes it. There may just be a single process
accessing the database, in which case the reader is simply a later version of the same
process—in that case you can think of storing something in the database as sending a
message to your future self.
Backward compatibility is clearly necessary here; otherwise your future self won’t be
able to decode what you previously wrote.
In general, it’s common for several different processes to be accessing a database at
the same time. Those processes might be several different applications or services, or
they may simply be several instances of the same service (running in parallel for scal‐
ability or fault tolerance). Either way, in an environment where the application is
changing, it is likely that some processes accessing the database will be running newer
code and some will be running older code—for example because a new version is cur‐
rently being deployed in a rolling upgrade, so some instances have been updated
while others haven’t yet.
This means that a value in the database may be written by a newer version of the
code, and subsequently read by an older version of the code that is still running.
Thus, forward compatibility is also often required for databases.
However, there is an additional snag. Say you add a field to a record schema, and the
newer code writes a value for that new field to the database. Subsequently, an older
version of the code (which doesn’t yet know about the new field) reads the record,
updates it, and writes it back. In this situation, the desirable behavior is usually for
the old code to keep the new field intact, even though it couldn’t be interpreted.
The encoding formats discussed previously support such preservation of unknown
fields, but sometimes you need to take care at an application level, as illustrated in
Figure 4-7. For example, if you decode a database value into model objects in the
application, and later reencode those model objects, the unknown field might be lost
in that translation process. Solving this is not a hard problem; you just need to be
aware of it.
Modes of Dataflow 
| 
129


v. Except for MySQL, which often rewrites an entire table even though it is not strictly necessary, as men‐
tioned in “Schema flexibility in the document model” on page 39.
Figure 4-7. When an older version of the application updates data previously written
by a newer version of the application, data may be lost if you’re not careful.
Different values written at different times
A database generally allows any value to be updated at any time. This means that
within a single database you may have some values that were written five milli‐
seconds ago, and some values that were written five years ago.
When you deploy a new version of your application (of a server-side application, at
least), you may entirely replace the old version with the new version within a few
minutes. The same is not true of database contents: the five-year-old data will still be
there, in the original encoding, unless you have explicitly rewritten it since then. This
observation is sometimes summed up as data outlives code.
Rewriting (migrating) data into a new schema is certainly possible, but it’s an expen‐
sive thing to do on a large dataset, so most databases avoid it if possible. Most rela‐
tional databases allow simple schema changes, such as adding a new column with a
null default value, without rewriting existing data.v When an old row is read, the
database fills in nulls for any columns that are missing from the encoded data on
disk. LinkedIn’s document database Espresso uses Avro for storage, allowing it to use
Avro’s schema evolution rules [23].
130 
| 
Chapter 4: Encoding and Evolution


Schema evolution thus allows the entire database to appear as if it was encoded with a
single schema, even though the underlying storage may contain records encoded with
various historical versions of the schema.
Archival storage
Perhaps you take a snapshot of your database from time to time, say for backup pur‐
poses or for loading into a data warehouse (see “Data Warehousing” on page 91). In
this case, the data dump will typically be encoded using the latest schema, even if the
original encoding in the source database contained a mixture of schema versions
from different eras. Since you’re copying the data anyway, you might as well encode
the copy of the data consistently.
As the data dump is written in one go and is thereafter immutable, formats like Avro
object container files are a good fit. This is also a good opportunity to encode the data
in an analytics-friendly column-oriented format such as Parquet (see “Column Com‐
pression” on page 97).
In Chapter 10 we will talk more about using data in archival storage. 
Dataflow Through Services: REST and RPC
When you have processes that need to communicate over a network, there are a few
different ways of arranging that communication. The most common arrangement is
to have two roles: clients and servers. The servers expose an API over the network,
and the clients can connect to the servers to make requests to that API. The API
exposed by the server is known as a service.
The web works this way: clients (web browsers) make requests to web servers, mak‐
ing GET requests to download HTML, CSS, JavaScript, images, etc., and making POST
requests to submit data to the server. The API consists of a standardized set of proto‐
cols and data formats (HTTP, URLs, SSL/TLS, HTML, etc.). Because web browsers,
web servers, and website authors mostly agree on these standards, you can use any
web browser to access any website (at least in theory!).
Web browsers are not the only type of client. For example, a native app running on a
mobile device or a desktop computer can also make network requests to a server, and
a client-side JavaScript application running inside a web browser can use
XMLHttpRequest to become an HTTP client (this technique is known as Ajax [30]).
In this case, the server’s response is typically not HTML for displaying to a human,
but rather data in an encoding that is convenient for further processing by the clientside application code (such as JSON). Although HTTP may be used as the transport
protocol, the API implemented on top is application-specific, and the client and
server need to agree on the details of that API.
Modes of Dataflow 
| 
131


Moreover, a server can itself be a client to another service (for example, a typical web
app server acts as client to a database). This approach is often used to decompose a
large application into smaller services by area of functionality, such that one service
makes a request to another when it requires some functionality or data from that
other service. This way of building applications has traditionally been called a serviceoriented architecture (SOA), more recently refined and rebranded as microservices
architecture [31, 32].
In some ways, services are similar to databases: they typically allow clients to submit
and query data. However, while databases allow arbitrary queries using the query lan‐
guages we discussed in Chapter 2, services expose an application-specific API that
only allows inputs and outputs that are predetermined by the business logic (applica‐
tion code) of the service [33]. This restriction provides a degree of encapsulation:
services can impose fine-grained restrictions on what clients can and cannot do.
A key design goal of a service-oriented/microservices architecture is to make the
application easier to change and maintain by making services independently deploya‐
ble and evolvable. For example, each service should be owned by one team, and that
team should be able to release new versions of the service frequently, without having
to coordinate with other teams. In other words, we should expect old and new ver‐
sions of servers and clients to be running at the same time, and so the data encoding
used by servers and clients must be compatible across versions of the service API—
precisely what we’ve been talking about in this chapter.
Web services
When HTTP is used as the underlying protocol for talking to the service, it is called a
web service. This is perhaps a slight misnomer, because web services are not only used
on the web, but in several different contexts. For example:
1. A client application running on a user’s device (e.g., a native app on a mobile
device, or JavaScript web app using Ajax) making requests to a service over
HTTP. These requests typically go over the public internet.
2. One service making requests to another service owned by the same organization,
often located within the same datacenter, as part of a service-oriented/microser‐
vices architecture. (Software that supports this kind of use case is sometimes
called middleware.)
3. One service making requests to a service owned by a different organization, usu‐
ally via the internet. This is used for data exchange between different organiza‐
tions’ backend systems. This category includes public APIs provided by online
services, such as credit card processing systems, or OAuth for shared access to
user data.
132 
| 
Chapter 4: Encoding and Evolution


vi. Even within each camp there are plenty of arguments. For example, HATEOAS (hypermedia as the engine
of application state), often provokes discussions [35].
vii. Despite the similarity of acronyms, SOAP is not a requirement for SOA. SOAP is a particular technology,
whereas SOA is a general approach to building systems.
There are two popular approaches to web services: REST and SOAP. They are almost
diametrically opposed in terms of philosophy, and often the subject of heated debate
among their respective proponents.vi
REST is not a protocol, but rather a design philosophy that builds upon the principles
of HTTP [34, 35]. It emphasizes simple data formats, using URLs for identifying
resources and using HTTP features for cache control, authentication, and content
type negotiation. REST has been gaining popularity compared to SOAP, at least in
the context of cross-organizational service integration [36], and is often associated
with microservices [31]. An API designed according to the principles of REST is
called RESTful.
By contrast, SOAP is an XML-based protocol for making network API requests.vii
Although it is most commonly used over HTTP, it aims to be independent from
HTTP and avoids using most HTTP features. Instead, it comes with a sprawling and
complex multitude of related standards (the web service framework, known as WS-*)
that add various features [37].
The API of a SOAP web service is described using an XML-based language called the
Web Services Description Language, or WSDL. WSDL enables code generation so
that a client can access a remote service using local classes and method calls (which
are encoded to XML messages and decoded again by the framework). This is useful in
statically typed programming languages, but less so in dynamically typed ones (see
“Code generation and dynamically typed languages” on page 127).
As WSDL is not designed to be human-readable, and as SOAP messages are often too
complex to construct manually, users of SOAP rely heavily on tool support, code
generation, and IDEs [38]. For users of programming languages that are not sup‐
ported by SOAP vendors, integration with SOAP services is difficult.
Even though SOAP and its various extensions are ostensibly standardized, interoper‐
ability between different vendors’ implementations often causes problems [39]. For
all of these reasons, although SOAP is still used in many large enterprises, it has fallen
out of favor in most smaller companies.
RESTful APIs tend to favor simpler approaches, typically involving less code genera‐
tion and automated tooling. A definition format such as OpenAPI, also known as
Swagger [40], can be used to describe RESTful APIs and produce documentation.
Modes of Dataflow 
| 
133


The problems with remote procedure calls (RPCs)
Web services are merely the latest incarnation of a long line of technologies for mak‐
ing API requests over a network, many of which received a lot of hype but have seri‐
ous problems. Enterprise JavaBeans (EJB) and Java’s Remote Method Invocation
(RMI) are limited to Java. The Distributed Component Object Model (DCOM) is
limited to Microsoft platforms. The Common Object Request Broker Architecture
(CORBA) is excessively complex, and does not provide backward or forward compat‐
ibility [41].
All of these are based on the idea of a remote procedure call (RPC), which has been
around since the 1970s [42]. The RPC model tries to make a request to a remote net‐
work service look the same as calling a function or method in your programming lan‐
guage, within the same process (this abstraction is called location transparency).
Although RPC seems convenient at first, the approach is fundamentally flawed [43,
44]. A network request is very different from a local function call: 
• A local function call is predictable and either succeeds or fails, depending only on
parameters that are under your control. A network request is unpredictable: the
request or response may be lost due to a network problem, or the remote
machine may be slow or unavailable, and such problems are entirely outside of
your control. Network problems are common, so you have to anticipate them,
for example by retrying a failed request.
• A local function call either returns a result, or throws an exception, or never
returns (because it goes into an infinite loop or the process crashes). A network
request has another possible outcome: it may return without a result, due to a
timeout. In that case, you simply don’t know what happened: if you don’t get a
response from the remote service, you have no way of knowing whether the
request got through or not. (We discuss this issue in more detail in Chapter 8.)
• If you retry a failed network request, it could happen that the requests are
actually getting through, and only the responses are getting lost. In that case,
retrying will cause the action to be performed multiple times, unless you build a
mechanism for deduplication (idempotence) into the protocol. Local function
calls don’t have this problem. (We discuss idempotence in more detail in Chap‐
ter 11.)
• Every time you call a local function, it normally takes about the same time to exe‐
cute. A network request is much slower than a function call, and its latency is
also wildly variable: at good times it may complete in less than a millisecond, but
when the network is congested or the remote service is overloaded it may take
many seconds to do exactly the same thing.
• When you call a local function, you can efficiently pass it references (pointers) to
objects in local memory. When you make a network request, all those parameters
134 
| 
Chapter 4: Encoding and Evolution


need to be encoded into a sequence of bytes that can be sent over the network.
That’s okay if the parameters are primitives like numbers or strings, but quickly
becomes problematic with larger objects.
• The client and the service may be implemented in different programming lan‐
guages, so the RPC framework must translate datatypes from one language into
another. This can end up ugly, since not all languages have the same types—
recall JavaScript’s problems with numbers greater than 253, for example (see
“JSON, XML, and Binary Variants” on page 114). This problem doesn’t exist in a
single process written in a single language.
All of these factors mean that there’s no point trying to make a remote service look
too much like a local object in your programming language, because it’s a fundamen‐
tally different thing. Part of the appeal of REST is that it doesn’t try to hide the fact
that it’s a network protocol (although this doesn’t seem to stop people from building
RPC libraries on top of REST).
Current directions for RPC
Despite all these problems, RPC isn’t going away. Various RPC frameworks have
been built on top of all the encodings mentioned in this chapter: for example, Thrift
and Avro come with RPC support included, gRPC is an RPC implementation using
Protocol Buffers, Finagle also uses Thrift, and Rest.li uses JSON over HTTP.
This new generation of RPC frameworks is more explicit about the fact that a remote
request is different from a local function call. For example, Finagle and Rest.li use
futures (promises) to encapsulate asynchronous actions that may fail. Futures also
simplify situations where you need to make requests to multiple services in parallel,
and combine their results [45]. gRPC supports streams, where a call consists of not
just one request and one response, but a series of requests and responses over time
[46].
Some of these frameworks also provide service discovery—that is, allowing a client to
find out at which IP address and port number it can find a particular service. We will
return to this topic in “Request Routing” on page 214.
Custom RPC protocols with a binary encoding format can achieve better perfor‐
mance than something generic like JSON over REST. However, a RESTful API has
other significant advantages: it is good for experimentation and debugging (you can
simply make requests to it using a web browser or the command-line tool curl,
without any code generation or software installation), it is supported by all main‐
stream programming languages and platforms, and there is a vast ecosystem of tools
available (servers, caches, load balancers, proxies, firewalls, monitoring, debugging
tools, testing tools, etc.).
Modes of Dataflow 
| 
135


For these reasons, REST seems to be the predominant style for public APIs. The main
focus of RPC frameworks is on requests between services owned by the same organi‐
zation, typically within the same datacenter.
Data encoding and evolution for RPC
For evolvability, it is important that RPC clients and servers can be changed and
deployed independently. Compared to data flowing through databases (as described
in the last section), we can make a simplifying assumption in the case of dataflow
through services: it is reasonable to assume that all the servers will be updated first,
and all the clients second. Thus, you only need backward compatibility on requests,
and forward compatibility on responses.
The backward and forward compatibility properties of an RPC scheme are inherited
from whatever encoding it uses:
• Thrift, gRPC (Protocol Buffers), and Avro RPC can be evolved according to the
compatibility rules of the respective encoding format.
• In SOAP, requests and responses are specified with XML schemas. These can be
evolved, but there are some subtle pitfalls [47].
• RESTful APIs most commonly use JSON (without a formally specified schema)
for responses, and JSON or URI-encoded/form-encoded request parameters for
requests. Adding optional request parameters and adding new fields to response
objects are usually considered changes that maintain compatibility.
Service compatibility is made harder by the fact that RPC is often used for communi‐
cation across organizational boundaries, so the provider of a service often has no
control over its clients and cannot force them to upgrade. Thus, compatibility needs
to be maintained for a long time, perhaps indefinitely. If a compatibility-breaking
change is required, the service provider often ends up maintaining multiple versions
of the service API side by side.
There is no agreement on how API versioning should work (i.e., how a client can
indicate which version of the API it wants to use [48]). For RESTful APIs, common
approaches are to use a version number in the URL or in the HTTP Accept header.
For services that use API keys to identify a particular client, another option is to store
a client’s requested API version on the server and to allow this version selection to be
updated through a separate administrative interface [49]. 
Message-Passing Dataflow
We have been looking at the different ways encoded data flows from one process to
another. So far, we’ve discussed REST and RPC (where one process sends a request
over the network to another process and expects a response as quickly as possible),
136 
| 
Chapter 4: Encoding and Evolution


and databases (where one process writes encoded data, and another process reads it
again sometime in the future).
In this final section, we will briefly look at asynchronous message-passing systems,
which are somewhere between RPC and databases. They are similar to RPC in that a
client’s request (usually called a message) is delivered to another process with low
latency. They are similar to databases in that the message is not sent via a direct net‐
work connection, but goes via an intermediary called a message broker (also called a
message queue or message-oriented middleware), which stores the message temporar‐
ily.
Using a message broker has several advantages compared to direct RPC:
• It can act as a buffer if the recipient is unavailable or overloaded, and thus
improve system reliability.
• It can automatically redeliver messages to a process that has crashed, and thus
prevent messages from being lost.
• It avoids the sender needing to know the IP address and port number of the
recipient (which is particularly useful in a cloud deployment where virtual
machines often come and go).
• It allows one message to be sent to several recipients.
• It logically decouples the sender from the recipient (the sender just publishes
messages and doesn’t care who consumes them).
However, a difference compared to RPC is that message-passing communication is
usually one-way: a sender normally doesn’t expect to receive a reply to its messages. It
is possible for a process to send a response, but this would usually be done on a sepa‐
rate channel. This communication pattern is asynchronous: the sender doesn’t wait
for the message to be delivered, but simply sends it and then forgets about it.
Message brokers
In the past, the landscape of message brokers was dominated by commercial enter‐
prise software from companies such as TIBCO, IBM WebSphere, and webMethods.
More recently, open source implementations such as RabbitMQ, ActiveMQ, Hor‐
netQ, NATS, and Apache Kafka have become popular. We will compare them in
more detail in Chapter 11.
The detailed delivery semantics vary by implementation and configuration, but in
general, message brokers are used as follows: one process sends a message to a named
queue or topic, and the broker ensures that the message is delivered to one or more
consumers of or subscribers to that queue or topic. There can be many producers and
many consumers on the same topic.
Modes of Dataflow 
| 
137


A topic provides only one-way dataflow. However, a consumer may itself publish
messages to another topic (so you can chain them together, as we shall see in Chap‐
ter 11), or to a reply queue that is consumed by the sender of the original message
(allowing a request/response dataflow, similar to RPC).
Message brokers typically don’t enforce any particular data model—a message is just
a sequence of bytes with some metadata, so you can use any encoding format. If the
encoding is backward and forward compatible, you have the greatest flexibility to
change publishers and consumers independently and deploy them in any order.
If a consumer republishes messages to another topic, you may need to be careful to
preserve unknown fields, to prevent the issue described previously in the context of
databases (Figure 4-7).
Distributed actor frameworks
The actor model is a programming model for concurrency in a single process. Rather
than dealing directly with threads (and the associated problems of race conditions,
locking, and deadlock), logic is encapsulated in actors. Each actor typically represents
one client or entity, it may have some local state (which is not shared with any other
actor), and it communicates with other actors by sending and receiving asynchro‐
nous messages. Message delivery is not guaranteed: in certain error scenarios, mes‐
sages will be lost. Since each actor processes only one message at a time, it doesn’t
need to worry about threads, and each actor can be scheduled independently by the
framework.
In distributed actor frameworks, this programming model is used to scale an applica‐
tion across multiple nodes. The same message-passing mechanism is used, no matter
whether the sender and recipient are on the same node or different nodes. If they are
on different nodes, the message is transparently encoded into a byte sequence, sent
over the network, and decoded on the other side.
Location transparency works better in the actor model than in RPC, because the actor
model already assumes that messages may be lost, even within a single process.
Although latency over the network is likely higher than within the same process,
there is less of a fundamental mismatch between local and remote communication
when using the actor model.
A distributed actor framework essentially integrates a message broker and the actor
programming model into a single framework. However, if you want to perform roll‐
ing upgrades of your actor-based application, you still have to worry about forward
and backward compatibility, as messages may be sent from a node running the new
version to a node running the old version, and vice versa.
Three popular distributed actor frameworks handle message encoding as follows:
138 
| 
Chapter 4: Encoding and Evolution


• Akka uses Java’s built-in serialization by default, which does not provide forward
or backward compatibility. However, you can replace it with something like Pro‐
tocol Buffers, and thus gain the ability to do rolling upgrades [50].
• Orleans by default uses a custom data encoding format that does not support
rolling upgrade deployments; to deploy a new version of your application, you
need to set up a new cluster, move traffic from the old cluster to the new one, and
shut down the old one [51, 52]. Like with Akka, custom serialization plug-ins can
be used.
• In Erlang OTP it is surprisingly hard to make changes to record schemas (despite
the system having many features designed for high availability); rolling upgrades
are possible but need to be planned carefully [53]. An experimental new maps
datatype (a JSON-like structure, introduced in Erlang R17 in 2014) may make
this easier in the future [54]. 
Summary
In this chapter we looked at several ways of turning data structures into bytes on the
network or bytes on disk. We saw how the details of these encodings affect not only
their efficiency, but more importantly also the architecture of applications and your
options for deploying them.
In particular, many services need to support rolling upgrades, where a new version of
a service is gradually deployed to a few nodes at a time, rather than deploying to all
nodes simultaneously. Rolling upgrades allow new versions of a service to be released
without downtime (thus encouraging frequent small releases over rare big releases)
and make deployments less risky (allowing faulty releases to be detected and rolled
back before they affect a large number of users). These properties are hugely benefi‐
cial for evolvability, the ease of making changes to an application.
During rolling upgrades, or for various other reasons, we must assume that different
nodes are running the different versions of our application’s code. Thus, it is impor‐
tant that all data flowing around the system is encoded in a way that provides back‐
ward compatibility (new code can read old data) and forward compatibility (old code
can read new data).
We discussed several data encoding formats and their compatibility properties:
• Programming language–specific encodings are restricted to a single program‐
ming language and often fail to provide forward and backward compatibility.
• Textual formats like JSON, XML, and CSV are widespread, and their compatibil‐
ity depends on how you use them. They have optional schema languages, which
are sometimes helpful and sometimes a hindrance. These formats are somewhat
Summary 
| 
139


vague about datatypes, so you have to be careful with things like numbers and
binary strings.
• Binary schema–driven formats like Thrift, Protocol Buffers, and Avro allow
compact, efficient encoding with clearly defined forward and backward compati‐
bility semantics. The schemas can be useful for documentation and code genera‐
tion in statically typed languages. However, they have the downside that data
needs to be decoded before it is human-readable.
We also discussed several modes of dataflow, illustrating different scenarios in which
data encodings are important:
• Databases, where the process writing to the database encodes the data and the
process reading from the database decodes it
• RPC and REST APIs, where the client encodes a request, the server decodes the
request and encodes a response, and the client finally decodes the response
• Asynchronous message passing (using message brokers or actors), where nodes
communicate by sending each other messages that are encoded by the sender
and decoded by the recipient
We can conclude that with a bit of care, backward/forward compatibility and rolling
upgrades are quite achievable. May your application’s evolution be rapid and your
deployments be frequent.
References
[1] “Java Object Serialization Specification,” docs.oracle.com, 2010.
[2] “Ruby 2.2.0 API Documentation,” ruby-doc.org, Dec 2014.
[3] “The Python 3.4.3 Standard Library Reference Manual,” docs.python.org, Febru‐
ary 2015.
[4] “EsotericSoftware/kryo,” github.com, October 2014.
[5] “CWE-502: Deserialization of Untrusted Data,” Common Weakness Enumera‐
tion, cwe.mitre.org, July 30, 2014.
[6] Steve Breen: “What Do WebLogic, WebSphere, JBoss, Jenkins, OpenNMS, and
Your Application Have in Common? This Vulnerability,” foxglovesecurity.com,
November 6, 2015.
[7] Patrick McKenzie: “What the Rails Security Issue Means for Your Startup,” kalzu‐
meus.com, January 31, 2013.
[8] Eishay Smith: “jvm-serializers wiki,” github.com, November 2014.
140 
| 
Chapter 4: Encoding and Evolution


[9] “XML Is a Poor Copy of S-Expressions,” c2.com wiki.
[10] Matt Harris: “Snowflake: An Update and Some Very Important Information,”
email to Twitter Development Talk mailing list, October 19, 2010.
[11] Shudi (Sandy) Gao, C. M. Sperberg-McQueen, and Henry S. Thompson: “XML
Schema 1.1,” W3C Recommendation, May 2001.
[12] Francis Galiegue, Kris Zyp, and Gary Court: “JSON Schema,” IETF Internet-
Draft, February 2013.
[13] Yakov Shafranovich: “RFC 4180: Common Format and MIME Type for
Comma-Separated Values (CSV) Files,” October 2005.
[14] “MessagePack Specification,” msgpack.org.
[15] Mark Slee, Aditya Agarwal, and Marc Kwiatkowski: “Thrift: Scalable Cross-
Language Services Implementation,” Facebook technical report, April 2007.
[16] “Protocol Buffers Developer Guide,” Google, Inc., developers.google.com.
[17] Igor Anishchenko: “Thrift vs Protocol Buffers vs Avro - Biased Comparison,”
slideshare.net, September 17, 2012.
[18] “A Matrix of the Features Each Individual Language Library Supports,”
wiki.apache.org.
[19] Martin Kleppmann: “Schema Evolution in Avro, Protocol Buffers and Thrift,”
martin.kleppmann.com, December 5, 2012.
[20] “Apache Avro 1.7.7 Documentation,” avro.apache.org, July 2014.
[21] Doug Cutting, Chad Walters, Jim Kellerman, et al.: “[PROPOSAL] New Subpro‐
ject: Avro,” email thread on hadoop-general mailing list, mail-archives.apache.org,
April 2009.
[22] Tony Hoare: “Null References: The Billion Dollar Mistake,” at QCon London,
March 2009.
[23] Aditya Auradkar and Tom Quiggle: “Introducing Espresso—LinkedIn’s Hot
New Distributed Document Store,” engineering.linkedin.com, January 21, 2015.
[24] Jay Kreps: “Putting Apache Kafka to Use: A Practical Guide to Building a Stream
Data Platform (Part 2),” blog.confluent.io, February 25, 2015.
[25] Gwen Shapira: “The Problem of Managing Schemas,” radar.oreilly.com, Novem‐
ber 4, 2014.
[26] “Apache Pig 0.14.0 Documentation,” pig.apache.org, November 2014.
[27] John Larmouth: ASN.1 Complete. Morgan Kaufmann, 1999. ISBN:
978-0-122-33435-1
Summary 
| 
141


[28] Russell Housley, Warwick Ford, Tim Polk, and David Solo: “RFC 2459: Internet
X.509 Public Key Infrastructure: Certificate and CRL Profile,” IETF Network Work‐
ing Group, Standards Track, January 1999.
[29] Lev Walkin: “Question: Extensibility and Dropping Fields,” lionet.info, Septem‐
ber 21, 2010.
[30] Jesse James Garrett: “Ajax: A New Approach to Web Applications,” adaptive‐
path.com, February 18, 2005.
[31] Sam Newman: Building Microservices. O’Reilly Media, 2015. ISBN:
978-1-491-95035-7
[32] Chris Richardson: “Microservices: Decomposing Applications for Deployability
and Scalability,” infoq.com, May 25, 2014.
[33] Pat Helland: “Data on the Outside Versus Data on the Inside,” at 2nd Biennial
Conference on Innovative Data Systems Research (CIDR), January 2005.
[34] Roy Thomas Fielding: “Architectural Styles and the Design of Network-Based
Software Architectures,” PhD Thesis, University of California, Irvine, 2000.
[35] Roy Thomas Fielding: “REST APIs Must Be Hypertext-Driven,” roy.gbiv.com,
October 20 2008.
[36] “REST in Peace, SOAP,” royal.pingdom.com, October 15, 2010.
[37] “Web Services Standards as of Q1 2007,” innoq.com, February 2007.
[38] Pete Lacey: “The S Stands for Simple,” harmful.cat-v.org, November 15, 2006.
[39] Stefan Tilkov: “Interview: Pete Lacey Criticizes Web Services,” infoq.com,
December 12, 2006.
[40] “OpenAPI Specification (fka Swagger RESTful API Documentation Specifica‐
tion) Version 2.0,” swagger.io, September 8, 2014.
[41] Michi Henning: “The Rise and Fall of CORBA,” ACM Queue, volume 4, number
5, pages 28–34, June 2006. doi:10.1145/1142031.1142044
[42] Andrew D. Birrell and Bruce Jay Nelson: “Implementing Remote Procedure
Calls,” ACM Transactions on Computer Systems (TOCS), volume 2, number 1, pages
39–59, February 1984. doi:10.1145/2080.357392
[43] Jim Waldo, Geoff Wyant, Ann Wollrath, and Sam Kendall: “A Note on Dis‐
tributed Computing,” Sun Microsystems Laboratories, Inc., Technical Report
TR-94-29, November 1994.
[44] Steve Vinoski: “Convenience over Correctness,” IEEE Internet Computing, vol‐
ume 12, number 4, pages 89–92, July 2008. doi:10.1109/MIC.2008.75
142 
| 
Chapter 4: Encoding and Evolution


[45] Marius Eriksen: “Your Server as a Function,” at 7th Workshop on Programming
Languages 
and 
Operating 
Systems 
(PLOS), 
November 
2013. 
doi:
10.1145/2525528.2525538
[46] “grpc-common Documentation,” Google, Inc., github.com, February 2015.
[47] Aditya Narayan and Irina Singh: “Designing and Versioning Compatible Web
Services,” ibm.com, March 28, 2007.
[48] Troy Hunt: “Your API Versioning Is Wrong, Which Is Why I Decided to Do It 3
Different Wrong Ways,” troyhunt.com, February 10, 2014.
[49] “API Upgrades,” Stripe, Inc., April 2015.
[50] Jonas Bonér: “Upgrade in an Akka Cluster,” email to akka-user mailing list, grok‐
base.com, August 28, 2013.
[51] Philip A. Bernstein, Sergey Bykov, Alan Geller, et al.: “Orleans: Distributed Vir‐
tual Actors for Programmability and Scalability,” Microsoft Research Technical
Report MSR-TR-2014-41, March 2014.
[52] “Microsoft Project Orleans Documentation,” Microsoft Research, dotnet.git‐
hub.io, 2015.
[53] David Mercer, Sean Hinde, Yinso Chen, and Richard A O’Keefe: “beginner:
Updating Data Structures,” email thread on erlang-questions mailing list, erlang.com,
October 29, 2007.
[54] Fred Hebert: “Postscript: Maps,” learnyousomeerlang.com, April 9, 2014.
Summary 
| 
143

## Examples & Scenarios

- vide commonly needed functionality. For example, many applications need to:
• Store data so that they, or another application, can find it again later (databases)
• Remember the result of an expensive operation, to speed up reads (caches)
• Allow users to search data by keyword or filter it in various ways (search indexes)
• Send a message to another process, to be handled asynchronously (stream pro‐
cessing)
• Periodically crunch a large amount of accumulated data (batch processing)
If that sounds painfully obvious, that’s just because these data systems are such a suc‐
cessful abstraction: we use them all the time without thinking too much. When build‐
ing an application, most engineers wouldn’t dream of writing a new data storage

- traditional categories [1]. For example, there are datastores that are also used as mes‐
sage queues (Redis), and there are message queues with database-like durability guar‐
antees (Apache Kafka). The boundaries between the categories are becoming blurred.
Secondly, increasingly many applications now have such demanding or wide-ranging
requirements that a single tool can no longer meet all of its data processing and stor‐
age needs. Instead, the work is broken down into tasks that can be performed effi‐
ciently on a single tool, and those different tools are stitched together using
application code.
For example, if you have an application-managed caching layer (using Memcached
or similar), or a full-text search server (such as Elasticsearch or Solr) separate from

- provide certain guarantees: e.g., that the cache will be correctly invalidated or upda‐
ted on writes so that outside clients see consistent results. You are now not only an
application developer, but also a data system designer.
If you are designing a data system or service, a lot of tricky questions arise. How do
you ensure that the data remains correct and complete, even when things go wrong
internally? How do you provide consistently good performance to clients, even when
parts of your system are degraded? How do you scale to handle an increase in load?
What does a good API for the service look like?
There are many factors that may influence the design of a data system, including the
skills and experience of the people involved, legacy system dependencies, the time‐

- rate of faults by triggering them deliberately—for example, by randomly killing indi‐
vidual processes without warning. Many critical bugs are actually due to poor error
handling [3]; by deliberately inducing faults, you ensure that the fault-tolerance
machinery is continually exercised and tested, which can increase your confidence
that faults will be handled correctly when they occur naturally. The Netflix Chaos
Monkey [4] is an example of this approach.
Although we generally prefer tolerating faults over preventing faults, there are cases
where prevention is better than cure (e.g., because no cure exists). This is the case
with security matters, for example: if an attacker has compromised a system and
gained access to sensitive data, that event cannot be undone. However, this book

- given a particular bad input. For example, consider the leap second on June 30,
2012, that caused many applications to hang simultaneously due to a bug in the
Linux kernel [9].
• A runaway process that uses up some shared resource—CPU time, memory, disk
space, or network bandwidth.
8
|
Chapter 1: Reliable, Scalable, and Maintainable Applications

- expected to provide some guarantee (for example, in a message queue, that the num‐
ber of incoming messages equals the number of outgoing messages), it can constantly
check itself while it is running and raise an alert if a discrepancy is found [12].
Human Errors
Humans design and build software systems, and the operators who keep the systems
running are also human. Even when they have the best intentions, humans are
known to be unreliable. For example, one study of large internet services found that
configuration errors by operators were the leading cause of outages, whereas hard‐
ware faults (servers or network) played a role in only 10–25% of outages [13].
How do we make our systems reliable, in spite of unreliable humans? The best sys‐

- • Design systems in a way that minimizes opportunities for error. For example,
well-designed abstractions, APIs, and admin interfaces make it easy to do “the
right thing” and discourage “the wrong thing.” However, if the interfaces are too
restrictive people will work around them, negating their benefit, so this is a tricky
balance to get right.
• Decouple the places where people make the most mistakes from the places where
they can cause failures. In particular, provide fully featured non-production
sandbox environments where people can explore and experiment safely, using
real data, without affecting real users.
• Test thoroughly at all levels, from unit tests to whole-system integration tests and

- case of a failure. For example, make it fast to roll back configuration changes, roll
out new code gradually (so that any unexpected bugs affect only a small subset of
users), and provide tools to recompute data (in case it turns out that the old com‐
putation was incorrect).
• Set up detailed and clear monitoring, such as performance metrics and error
rates. In other engineering disciplines this is referred to as telemetry. (Once a
rocket has left the ground, telemetry is essential for tracking what is happening,
and for understanding failures [14].) Monitoring can show us early warning sig‐
nals and allow us to check whether any assumptions or constraints are being vio‐
lated. When a problem occurs, metrics can be invaluable in diagnosing the issue.

- development cost (e.g., when developing a prototype product for an unproven mar‐
ket) or operational cost (e.g., for a service with a very narrow profit margin)—but we
should be very conscious of when we are cutting corners.
Scalability
Even if a system is working reliably today, that doesn’t mean it will necessarily work
reliably in the future. One common reason for degradation is increased load: perhaps
the system has grown from 10,000 concurrent users to 100,000 concurrent users, or
from 1 million to 10 million. Perhaps it is processing much larger volumes of data
than it did before.
Scalability is the term we use to describe a system’s ability to cope with increased

- expensive, e.g., because they process more data. But even in a scenario where you’d
think all requests should take the same time, you get variation: random additional
latency could be introduced by a context switch to a background process, the loss of a
network packet and TCP retransmission, a garbage collection pause, a page fault
forcing a read from disk, mechanical vibrations in the server rack [18], or many other
causes.
Figure 1-4. Illustrating mean and percentiles: response times for a sample of 100
requests to a service.
It’s common to see the average response time of a service reported. (Strictly speaking,
the term “average” doesn’t refer to any particular formula, but in practice it is usually

- from fastest to slowest, then the median is the halfway point: for example, if your
14
|
Chapter 1: Reliable, Scalable, and Maintainable Applications

- faster than that particular threshold. For example, if the 95th percentile response time
is 1.5 seconds, that means 95 out of 100 requests take less than 1.5 seconds, and 5 out
of 100 requests take 1.5 seconds or more. This is illustrated in Figure 1-4.
High percentiles of response times, also known as tail latencies, are important
because they directly affect users’ experience of the service. For example, Amazon
describes response time requirements for internal services in terms of the 99.9th per‐
centile, even though it only affects 1 in 1,000 requests. This is because the customers
with the slowest requests are often those who have the most data on their accounts
because they have made many purchases—that is, they’re the most valuable custom‐
ers [19]. It’s important to keep those customers happy by ensuring the website is fast

- For example, percentiles are often used in service level objectives (SLOs) and service
level agreements (SLAs), contracts that define the expected performance and availa‐
bility of a service. An SLA may state that the service is considered to be up if it has a
median response time of less than 200 ms and a 99th percentile under 1 s (if the
response time is longer, it might as well be down), and the service may be required to
be up at least 99.9% of the time. These metrics set expectations for clients of the ser‐
vice and allow customers to demand a refund if the SLA is not met.
Queueing delays often account for a large part of the response time at high percen‐
tiles. As a server can only process a small number of things in parallel (limited, for
Scalability

- services, you need to efficiently calculate them on an ongoing basis. For example, you
may want to keep a rolling window of response times of requests in the last 10
minutes. Every minute, you calculate the median and various percentiles over the val‐
ues in that window and plot those metrics on a graph.
The naïve implementation is to keep a list of response times for all requests within the
time window and to sort that list every minute. If that is too inefficient for you, there
are algorithms that can calculate a good approximation of percentiles at minimal
CPU and memory cost, such as forward decay [25], t-digest [26], or HdrHistogram
[27]. Beware that averaging percentiles, e.g., to reduce the time resolution or to com‐
bine data from several machines, is mathematically meaningless—the right way of

- a pragmatic mixture of approaches: for example, using several fairly powerful
machines can still be simpler and cheaper than a large number of small virtual
machines.
Some systems are elastic, meaning that they can automatically add computing resour‐
ces when they detect a load increase, whereas other systems are scaled manually (a
human analyzes the capacity and decides to add more machines to the system). An
elastic system can be useful if load is highly unpredictable, but manually scaled sys‐
tems are simpler and may have fewer operational surprises (see “Rebalancing Parti‐
tions” on page 209).
Scalability

- For example, a system that is designed to handle 100,000 requests per second, each
1 kB in size, looks very different from a system that is designed for 3 requests per
minute, each 2 GB in size—even though the two systems have the same data through‐
put.
An architecture that scales well for a particular application is built around assump‐
tions of which operations will be common and which will be rare—the load parame‐
ters. If those assumptions turn out to be wrong, the engineering effort for scaling is at
best wasted, and at worst counterproductive. In an early-stage startup or an unpro‐
ven product it’s usually more important to be able to iterate quickly on product fea‐
tures than it is to scale to some hypothetical future load.

- • Anticipating future problems and solving them before they occur (e.g., capacity
planning)
• Establishing good practices and tools for deployment, configuration manage‐
ment, and more
• Performing complex maintenance tasks, such as moving an application from one
platform to another
• Maintaining the security of the system as configuration changes are made
• Defining processes that make operations predictable and help keep the produc‐
tion environment stable
• Preserving the organization’s knowledge about the system, even as individual

- For example, high-level programming languages are abstractions that hide machine
code, CPU registers, and syscalls. SQL is an abstraction that hides complex on-disk
and in-memory data structures, concurrent requests from other clients, and inconsis‐
tencies after crashes. Of course, when programming in a high-level language, we are
still using machine code; we are just not using it directly, because the programming
language abstraction saves us from having to think about it.
However, finding good abstractions is very hard. In the field of distributed systems,
although there are many good algorithms, it is much less clear how we should be
packaging them into abstractions that help us keep the complexity of the system at a
manageable level.

- different applications or services with different characteristics. For example, how
would you “refactor” Twitter’s architecture for assembling home timelines (“Describ‐
ing Load” on page 11) from approach 1 to approach 2?
The ease with which you can modify a data system, and adapt it to changing require‐
ments, is closely linked to its simplicity and its abstractions: simple and easy-tounderstand systems are usually easier to modify than complex ones. But since this is
such an important idea, we will use a different word to refer to agility on a data sys‐
tem level: evolvability [34].
Summary
In this chapter, we have explored some fundamental ways of thinking about dataintensive applications. These principles will guide us through the rest of the book,
where we dive into deep technical detail.

- example:
1. As an application developer, you look at the real world (in which there are peo‐
ple, organizations, goods, actions, money flows, sensors, etc.) and model it in
terms of objects or data structures, and APIs that manipulate those data struc‐
tures. Those structures are often specific to your application.
2. When you want to store those data structures, you express them in terms of a
general-purpose data model, such as JSON or XML documents, tables in a rela‐
tional database, or a graph model.
3. The engineers who built your database software decided on a way of representing
that JSON/XML/relational/graph data in terms of bytes in memory, on disk, or

## Key Takeaways

- sity Data Mining class (CS345), December 2006.
[21] Tammy Everts: “The Real Cost of Slow Time vs Downtime,” webperformanceto‐
day.com, November 12, 2014.
[22] Jake Brutlag: “Speed Matters for Google Web Search,” googleresearch.blog‐
spot.co.uk, June 22, 2009.
[23] Tyler Treat: “Everything You Know About Latency Is Wrong,” bravenew‐

