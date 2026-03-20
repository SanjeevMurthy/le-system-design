# Part 1

> Source: Acing the System Design Interview (Zhiyong Tan, 2024), Chapter 2, Pages 33-176

## Key Concepts

- Part 1
xxx
This part of the book discusses common topics in system design interviews. It sets the stage for part 2, where we discuss sample system design interview 
questions. 
We begin in chapter 1 b
- 3
1
A walkthrough of 
system design concepts
This chapter covers
¡ Learning the importance of the system design 	
	 interview
¡ Scaling a service
¡ Using cloud hosting vs. bare metal
A system design i

## Content

Part 1
xxx
This part of the book discusses common topics in system design interviews. It sets the stage for part 2, where we discuss sample system design interview 
questions. 
We begin in chapter 1 by walking through a sample system and introducing 
many system design concepts along the way without explaining them in detail, 
then deep dive into these concepts in subsequent chapters. 
In chapter 2, we discuss one’s experience in a typical system design interview. 
We’ll learn to clarify the requirements of the question and what aspects of the system to optimize at the expense of others. Then we discuss other common topics, 
including storing and searching data, operational concerns like monitoring and 
alerting, and edge cases and new constraints. 
In chapter 3, we dive into non-functional requirements, which are usually not 
explicitly requested by the customer or interviewer and must be clarified prior to 
designing a system. 
A large system may serve hundreds of millions of users and receive billions of 
data read and write requests every day. We discuss in chapter 4 how we can scale 
our databases to handle such traffic.
The system may be divided into services, and we may need to write related data 
to these multiple services, which we discuss in chapter 5.
Many systems require certain common functionalities. In chapter 6, we discuss how we can centralize such cross-cutting functionalities into services that can 
serve many other systems.




3
1
A walkthrough of 
system design concepts
This chapter covers
¡ Learning the importance of the system design 	
	 interview
¡ Scaling a service
¡ Using cloud hosting vs. bare metal
A system design interview is a discussion between the candidate and the interviewer 
about designing a software system that is typically provided over a network. The 
interviewer begins the interview with a short and vague request to the candidate to 
design a particular software system. Depending on the particular system, the user 
base may be non-technical or technical.
System design interviews are conducted for most software engineering, software 
architecture, and engineering manager job interviews. (In this book, we collectively 
refer to software engineers, architects, and managers as simply engineers.) Other components of the interview process include coding and behavioral/cultural interviews.


4
Chapter 1  A walkthrough of system design concepts
1.1	
A discussion about tradeoffs
The following factors attest to the importance of system design interviews and preparing well for them as a candidate and an interviewer.
Run in performance as a candidate in the system design interviews is used to estimate 
your breadth and depth of system design expertise and your ability to communicate 
and discuss system designs with other engineers. This is a critical factor in determining 
the level of seniority at which you will be hired into the company. The ability to design 
and review large-scale systems is regarded as more important with increasing engineering seniority. Correspondingly, system design interviews are given more weight in interviews for senior positions. Preparing for them, both as an interviewer and candidate, is 
a good investment of time for a career in tech.
The tech industry is unique in that it is common for engineers to change companies every few years, unlike other industries where an employee may stay at their company for many years or their whole career. This means that a typical engineer will go 
through system design interviews many times in their career. Engineers employed at 
a highly desirable company will go through even more system design interviews as an 
interviewer. As an interview candidate, you have less than one hour to make the best 
possible impression, and the other candidates who are your competition are among the 
smartest and most motivated people in the world.
System design is an art, not a science. It is not about perfection. We make tradeoffs 
and compromises to design the system we can achieve with the given resources and 
time that most closely suits current and possible future requirements. All the discussions of various systems in this book involve estimates and assumptions and are not academically rigorous, exhaustive, or scientific. We may refer to software design patterns 
and architectural patterns, but we will not formally describe these principles. Readers 
should refer to other resources for more details.
A system design interview is not about the right answer. It is about one’s ability to 
discuss multiple possible approaches and weigh their tradeoffs in satisfying the requirements. Knowledge of the various types of requirements and common systems discussed 
in part 1 will help us design our system, evaluate various possible approaches, and discuss tradeoffs.
1.2	
Should you read this book?
The open-ended nature of system design interviews makes it a challenge to prepare 
for and know how or what to discuss during an interview. An engineer or student who 
searches for online learning materials on system design interviews will find a vast quantity of content that varies in quality and diversity of the topics covered. This is confusing and hinders learning. Moreover, until recently, there were few dedicated books on 
this topic, though a trickle of such books is beginning to be published. I believe this is 
because a high-quality book dedicated to the topic of system design interviews is, quoting the celebrated 19th-century French poet and novelist Victor Hugo, “an idea whose 
time has come.” Multiple people will get this same idea at around the same time, and 
this affirms its relevance.


	
5
Overview of this book
This is not an introductory software engineering book. This book is best used after 
one has acquired a minimal level of industry experience. Perhaps if you are a student in 
your first internship, you can read the documentation websites and other introductory 
materials of unfamiliar tools and discuss them together with other unfamiliar concepts 
in this book with engineers at your workplace. This book discusses how to approach 
system design interviews and minimizes duplication of introductory material that we 
can easily find online or in other books. At least intermediate proficiency in coding and 
SQL is assumed. 
This book offers a structured and organized approach to start preparing for system 
design interviews or to fill gaps in knowledge and understanding from studying the 
large amount of fragmented material. Equally valuably, it teaches how to demonstrate 
one’s engineering maturity and communication skills during a system design interview, 
such as clearly and concisely articulating one’s ideas, knowledge, and questions to the 
interviewer within the brief ~50 minutes. 
A system design interview, like any other interview, is also about communication 
skills, quick thinking, asking good questions, and performance anxiety. One may forget 
to mention points that the interviewer is expecting. Whether this interview format is 
flawed can be endlessly debated. From personal experience, with seniority one spends 
an increasing amount of time in meetings, and essential abilities include quick thinking, 
being able to ask good questions, steering the discussion to the most critical and relevant 
topics, and communicating one’s thoughts succinctly. This book emphasizes that one 
must effectively and concisely express one’s system design expertise within the <1 hour 
interview and drive the interview in the desired direction by asking the interviewer the 
right questions. Reading this book, along with practicing system design discussions with 
other engineers, will allow you to develop the knowledge and fluency required to pass 
system design interviews and participate well in designing systems in the company you 
join. It can also be a resource for interviewers who conduct system design interviews.
 One may excel in written over verbal communication and forget to mention important points during the ~50-minute interview. System design interviews are biased in favor 
of engineers with good verbal communication and against engineers less proficient in 
verbal communication, even though the latter may have considerable system design 
expertise and have made valuable system design contributions in the organizations 
where they worked. This book prepares engineers for these and other challenges of system design interviews, shows how to approach them in an organized way, and coaches 
how not to be intimidated.
If you are a software engineer looking to broaden your knowledge of system design 
concepts, improve your ability to discuss a system, or are simply looking for a collection 
of system design concepts and sample system design discussions, read on.
1.3	
Overview of this book
This book is divided into two parts. Part 1 is presented like a typical textbook, with 
chapters that cover the various topics discussed in a system design interview. Part 2 consists of discussions of sample interview questions that reference the concepts covered 
in part 1 and also discusses antipatterns and common misconceptions and mistakes. In 


6
Chapter 1  A walkthrough of system design concepts
those discussions, we also state the obvious that one is not expected to possess all knowledge of all domains. Rather, one should be able to reason that certain approaches will 
help satisfy requirements better, with certain tradeoffs. For example, we don’t need to 
calculate file size reduction or CPU and memory resources required for Gzip compression on a file, but we should be able to state that compressing a file before sending it 
will reduce network traffic but consume more CPU and memory resources on both the 
sender and recipient. 
An aim of this book is to bring together a bunch of relevant materials and organize 
them into a single book so you can build a knowledge foundation or identify gaps in 
your knowledge, from which you can study other materials.
The rest of this chapter is a prelude to a sample system design that mentions some of 
the concepts that will be covered in part 1. Based on this context, we will discuss many of 
the concepts in dedicated chapters.
1.4	
Prelude: A brief discussion of scaling the various services of a 
system
We begin this book with a brief description of a typical initial setup of an app and a 
general approach to adding scalability into our app’s services as needed. Along the 
way, we introduce numerous terms and concepts and many types of services required 
by a tech company, which we discuss in greater detail in the rest of the book.
DEFINITION    The scalability of a service is the ability to easily and cost-effectively 
vary resources allocated to it to serve changes in load. This applies to both 
increasing or decreasing user numbers and/or requests to the system. This is 
discussed more in chapter 3.
1.4.1	
The beginning: A small initial deployment of our app 
Riding the rising wave of interest in artisan bagels, we have just built an awesome consumer-facing app named Beigel that allows users to read and create posts about nearby 
bagel cafes. 
Initially, Beigel consists primarily of the following components: 
¡ Our consumer apps. They are essentially the same app, one for each of the three 
common platforms: 
–	 A browser app. This is a ReactJS browser consumer app that makes requests to 
a JavaScript runtime service. To reduce the size of the JavaScript bundle that 
users need to download, we compress it with Brotli. Gzip is an older and more 
popular choice, but Brotli produces smaller compressed files. 
–	 An iOS app, which is downloaded on a consumer’s iOS device. 
–	 An Android app, which is also downloaded on a consumer’s Android device. 
¡ A stateless backend service that serves the consumer apps. It can be a Go or Java 
service. 
¡ A SQL database contained in a single cloud host. 


	
7
Prelude: A brief discussion of scaling the various services of a system
We have two main services: the frontend service and the backend service. Figure 1.1 
illustrates these components. As shown, the consumer apps are client-side components, while services and database are server-side components. 
NOTE    Refer to sections 6.5.1 and 6.5.2 for a discussion on why we need a front­
end service between the browser and the backend service.
Browser
Android
iOS
Frontend
Backend
Client
Server
SQL
Figure 1.1    Initial system design of our app. For a more thorough discussion on the rationale for having 
three client applications and two server applications (excluding the SQL application/database), refer to 
chapter 6.
When we first launch a service, it may only have a small number of users and thus a low 
request rate. A single host may be sufficient to handle the low request rate. We will set 
up our DNS to direct all requests to this host. 
Initially, we can host the two services within the same data center, each on a single cloud host. (We compare cloud vs. bare metal in the next section.) We configure 
our DNS to direct all requests from our browser app to our Node.js host and from our 
Node.js host and two mobile apps to our backend host. 
1.4.2	
Scaling with GeoDNS 
Months later, Beigel has gained hundreds of thousands of daily active users in Asia, 
Europe, and North America. During periods of peak traffic, our backend service 
receives thousands of requests per second, and our monitoring system is starting to 
report status code 504 responses due to timeouts. We must scale up our system. 
We have observed the rise in traffic and prepared for this situation. Our service is 
stateless as per standard best practices, so we can provision multiple identical backend 
hosts and place each host in a different data center in a different part of the world. 
Referring to figure 1.2, when a client makes a request to our backend via its domain 
beigel.com, we use GeoDNS to direct the client to the data center closest to it. 


8
Chapter 1  A walkthrough of system design concepts
Client
GeoDNS
US DC
Singapore DC
Amsterdam DC
(2) located near...
(1)
...North America
...Asia
...Europe
Figure 1.2    We may provision our service in multiple geographically distributed data centers. Depending 
on the client’s location (inferred from its IP address), a client obtains the IP address of a host of the 
closest data center, to which it sends its requests. The client may cache this host IP address.
If our service serves users from a specific country or geographical region in general, 
we will typically host our service in a nearby data center to minimize latency. If your 
service serves a large geographically distributed userbase, we can host it on multiple 
data centers and use GeoDNS to return to a user the IP address of our service hosted 
in the closest data center. This is done by assigning multiple A records to our domain 
for various locations and a default IP address for other locations. (An A record is a DNS 
configuration that maps a domain to an IP address.) 
When a client makes a request to the server, the GeoDNS obtains the client’s location 
from their IP address and assigns the client the corresponding host IP address. In the 
unlikely but possible event that the data center is inaccessible, GeoDNS can return an 
IP address of the service on another data center. This IP address can be cached at various levels, including the user’s Internet Service Provider (ISP), OS, and browser. 
1.4.3	
Adding a caching service 
Referring to figure 1.3, we next set up a Redis cache service to serve cached requests 
from our consumer apps. We select certain backend endpoints with heavy traffic to 
serve from the cache. That bought us some time as our user base and request load continued to grow. Now, further steps are needed to scale up.


	
9
Prelude: A brief discussion of scaling the various services of a system
Browser
Android
iOS
Node.js
Backend
Client
Server
SQL
Cache
Figure 1.3    Adding a cache to our service. Certain backend endpoints with heavy traffic can be cached. 
The backend will request data from the database on a cache miss or for SQL databases/tables that were 
not cached.
1.4.4	
Content distribution network
Our browser apps had been hosting static content/files that are displayed the same 
to any user and unaffected by user input, such as JavaScript, CSS libraries, and some 
images and videos. We had placed these files within our app’s source code repository, 
and our users were downloading them from our Node.js service together with the rest 
of the app. Referring to figure 1.4, we decided to use a third-party content distribution network (CDN) to host the static content. We selected and provisioned sufficient 
capacity from a CDN to host our files, uploaded our files onto our CDN instance, 
rewrote our code to fetch the files from the URLs of the CDN, and removed the files 
from our source code repository.
Browser
Android
iOS
Node.js
Backend
Client
Server
SQL
Cache
CDN
Figure 1.4    Adding a CDN to our service. Clients can obtain CDN addresses from the backend, or certain 
CDN addresses can be hardcoded in the clients or Node.js service.


10
Chapter 1  A walkthrough of system design concepts
Referring to figure 1.5, a CDN stores copies of the static files in various data centers 
across the world, so a user can download these files from the data center that can provide them the lowest latency, which is usually the geographically closest one, though 
other data centers may be faster if the closest one is serving heavy traffic or suffering a 
partial outage.
Figure 1.5    The left illustration shows all clients downloading from the same host. The right illustration 
shows clients downloading from various hosts of a CDN. (Copyright cc-by-sa https://creativecommons 
.org/licenses/by-sa/3.0/. Image by Kanoha from https://upload.wikimedia.org/wikipedia/
commons/f/f9/NCDN_-_CDN.png.)
Using a CDN improved latency, throughput, reliability, and cost. (We discuss all these 
concepts in chapter 3.) Using a CDN, unit costs decrease with demand because maintenance, integration overhead, and customer support are spread over a larger load.
Popular CDNs include CloudFlare, Rackspace, and AWS CloudFront. 
1.4.5	
A brief discussion of horizontal scalability and cluster management, continuous 
integration, and continuous deployment 
Our frontend and backend services are idempotent (we discuss some benefits of idempotency and its benefits in sections 4.6.1, 6.1.2, and 7.7), thus they are horizontally 
scalable, so we can provision more hosts to support our larger request load without 
rewriting any source code and deploy the frontend or backend service to those hosts 
as needed.
Each of our services has multiple engineers working on its source code. Our engineers submit new commits every day. We change software development and release 
practices to support this larger team and faster development, hiring two DevOps engineers in the process to develop the infrastructure to manage a large cluster. As scaling requirements of a service can change quickly, we want to be able to easily resize its 
cluster. We need to be able to easily deploy our services and required configurations to 
new hosts. We also want to easily build and deploy code changes to all the hosts in our 
service’s cluster. We can take advantage of our large userbase for experimentation by 
deploying different code or configurations to various hosts. This section is a brief discussion of cluster management for horizontal scalability and experimentation.


	
11
Prelude: A brief discussion of scaling the various services of a system
CI/CD and Infrastructure as Code 
To allow new features to be released quickly while minimizing the risk of releasing 
bugs, we adopt continuous integration and continuous deployment with Jenkins and 
unit testing and integration testing tools. (A detailed discussion of CI/CD is outside 
the scope of this book.) We use Docker to containerize our services, Kubernetes (or 
Docker Swarm) to manage our host cluster including scaling and providing load balancing, and Ansible or Terraform for configuration management of our various services running on our various clusters. 
NOTE    Mesos is widely considered obsolete. Kubernetes is the clear winner. A 
couple of relevant articles are https://thenewstack.io/apache-mesos-narrowly 
-avoids-a-move-to-the-attic-for-now/ and https://www.datacenterknowledge.com/ 
business/after-kubernetes-victory-its-former-rivals-change-tack. 
Terraform allows an infrastructure engineer to create a single configuration compatible with multiple cloud providers. A configuration is authored in Terraform’s 
domain-specific language (DSL) and communicates with cloud APIs to provision infrastructure. In practice, a Terraform configuration may contain some vendor-specific 
code, which we should minimize. The overall consequence is less vendor lock-in. 
This approach is also known as Infrastructure as Code. Infrastructure as Code is the 
process of managing and provisioning computer data centers through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools (Wittig, Andreas; Wittig, Michael [2016]. Amazon Web Services in Action. 
Manning Publications. p. 93. ISBN 978-1-61729-288-0). 
Gradual rollouts and rollbacks 
In this section, we briefly discuss gradual rollouts and rollbacks, so we can contrast 
them with experimentation in the next section. 
When we deploy a build to production, we may do so gradually. We may deploy the 
build to a certain percentage of hosts, monitor it and then increase the percentage, 
repeating this process until 100% of production hosts are running this build. For example, we may deploy to 1%, 5%, 10%, 25%, 50%, 75%, and then finally 100%. We may 
manually or automatically roll back deployments if we detect any problems, such as: 
¡ Bugs that slipped through testing. 
¡ Crashes. 
¡ Increased latency or timeouts. 
¡ Memory leaks. 
¡ Increased resource consumption like CPU, memory, or storage utilization. 
¡ Increased user churn. We may also need to consider user churn in gradual outs—
that is, that new users are signing on and using the app, and certain users may 
stop using the app. We can gradually expose an increasing percentage of users to 
a new build and study its effect on churn. User churn may occur due to the mentioned factors or unexpected problems such as many users disliking the changes. 


12
Chapter 1  A walkthrough of system design concepts
For example, a new build may increase latency beyond an acceptable level. We can use 
a combination of caching and dynamic routing to handle this. Our service may specify 
a one-second latency. When a client makes a request that is routed to a new build, and 
a timeout occurs, our client may read from its cache, or it may repeat its request and be 
routed to a host with an older build. We should log the requests and responses so we 
can troubleshoot the timeouts. 
We can configure our CD pipeline to divide our production cluster into several 
groups, and our CD tool will determine the appropriate number of hosts in each group 
and assign hosts to groups. Reassignments and redeployments may occur if we resize 
our cluster. 
Experimentation 
As we make UX changes in developing new features (or removing features) and 
aesthetic designs in our application, we may wish to gradually roll them out to an 
increasing percentage of users, rather than to all users at once. The purpose of experimentation is to determine the effect of UX changes on user behavior, in contrast to 
gradual rollouts, which are about the effect of new deployments on application performance and user churn. Common experimentation approaches are A/B and multivariate testing, such as multi-armed bandit. These topics are outside the scope of this 
book. For more information on A/B testing, refer to https://www.optimizely.com/ 
optimization-glossary/ab-testing/. For multivariate testing, see Experimentation for Engineers by David Sweet (Manning Publications, 2023) or https://www.optimizely.com/ 
optimization-glossary/multi-armed-bandit/ for an introduction to multi-armed 
bandit.)
Experimentation is also done to deliver personalized user experiences. 
Another difference between experimentation vs. gradual rollouts and rollbacks is 
that in experimentation, the percentage of hosts running various builds is often tuned 
by an experimentation or feature toggle tool that is designed for that purpose, while 
in gradual rollouts and rollbacks, the CD tool is used to manually or automatically roll 
back hosts to previous builds if problems are detected. 
CD and experimentation allow short feedback cycles to new deployments and 
features. 
In web and backend applications, each user experience (UX) is usually packaged 
in a different build. A certain percentage of hosts will contain a different build. Mobile 
apps are usually different. Many user experiences are coded into the same build, but 
each individual user will only be exposed to a subset of these user experiences. The 
main reasons for this are: 
¡ Mobile application deployments must be made through the app store. It may 
take many hours to deploy a new version to user devices. There is no way to 
quickly roll back a deployment.
¡ Compared to Wi-Fi, mobile data is slower, less reliable, and more expensive. 
Slow speed and unreliability mean we need to have much content served offline, 


	
13
Prelude: A brief discussion of scaling the various services of a system
already in the app. Mobile data plans in many countries are still expensive and 
may come with data caps and overage charges. We should avoid exposing users to 
these charges, or they may use the app less or uninstall it altogether. To conduct 
experimentation while minimizing data usage from downloading components 
and media, we simply include all these components and media in the app and 
expose the desired subset to each individual user. 
¡ A mobile app may also include many features that some users will never use 
because it is not applicable to them. For example, section 15.1 discusses various 
methods of payment in an app. There are possibly thousands of payment solutions in the world. The app needs to contain all the code and SDKs for every 
payment solution, so it can present each user with the small subset of payment 
solutions they may have. 
A consequence of all this is that a mobile app can be over 100MB in size. The techniques to address this are outside the scope of this book. We need to achieve a balance 
and consider tradeoffs. For example, YouTube’s mobile app installation obviously cannot include many YouTube videos. 
1.4.6	
Functional partitioning and centralization of cross-cutting concerns 
Functional partitioning is about separating various functions into different services or 
hosts. Many services have common concerns that can be extracted into shared services. 
Chapter 6 discusses the motivation, benefits, and tradeoffs. 
Shared services 
Our company is expanding rapidly. Our daily active user count has grown to millions. 
We expand our engineering team to five iOS engineers, five Android engineers, 10 
frontend engineers, 100 backend engineers, and we create a data science team. 
Our expanded engineering team can work on many services beyond the apps directly 
used by consumers, such as services for our expanding customer support and operations departments. We add features within the consumer apps for consumers to contact 
customer support and for operations to create and launch variations of our products. 
Many of our apps contain search bars. We create a shared search service with 
Elasticsearch. 
In addition to horizontal scaling, we use functional partitioning to spread out data 
processing and requests across a large number of geographically distributed hosts by 
partitioning based on functionality and geography. We already did functional partitioning of our cache, Node.js service, backend service, and database service into separate 
hosts, and we do functional partitioning for other services as well, placing each service 
on its own cluster of geographically distributed hosts. Figure 1.6 shows the shared services that we add to Beigel. 


14
Chapter 1  A walkthrough of system design concepts
Logging
Monitoring
Alerting
Search
Browser
Android
iOS
Node.js
Backend
Client
Server
SQL
Cache
CDN
Figure 1.6    Functional partitioning. Adding shared services. 
We added a logging service, consisting of a log-based message broker. We can use the 
Elastic Stack (Elasticsearch, Logstash, Kibana, Beats). We also use a distributed tracing 
system, such as Zipkin or Jaeger or distributed logging, to trace a request as it traverses 
through our numerous services. Our services attach span IDs to each request so they 
can be assembled as traces and analyzed. Section 2.5 discusses logging, monitoring, 
and alerting.
We also added monitoring and alerting services. We build internal browser apps for 
our customer support employees to better assist customers. These apps process the consumer app logs generated by the customer and present them with good UI so our customer support employees can more easily understand the customer’s problem. 
API gateway and service mesh are two ways to centralize cross-cutting concerns. 
Other ways are the decorator pattern and aspect-oriented programming, which are outside the scope of this book. 
API gateway 
By this time, app users make up less than half of our API requests. Most requests 
originate from other companies, which offer services such as recommending useful 
products and services to our users based on their in-app activities. We develop an API 
gateway layer to expose some of our APIs to external developers. 
An API gateway is a reverse proxy that routes client requests to the appropriate backend services. It provides the common functionality to many services, so individual services do not duplicate them: 
¡ Authorization and authentication, and other access control and security policies 
¡ Logging, monitoring, and alerting at the request level


	
15
Prelude: A brief discussion of scaling the various services of a system
¡ Rate limiting 
¡ Billing 
¡ Analytics 
Our initial architecture involving an API gateway and its services is illustrated in figure 
1.7. A request to a service goes through a centralized API gateway. The API gateway carries out all the functionality described previously, does a DNS lookup, and then forwards 
the request to a host of the relevant service. The API gateway makes requests to services 
such as DNS, identity and access control and management, rate-limiting configuration 
service, etc. We also log all configuration changes done through the API gateway. 
Logging
Monitoring
Alerting
Search
Batch ETL 
Service
Streaming ETL 
Service
Browser
Android
iOS
Node.js
CDN
Client
Server
SQL
Cache
Backend
Other clients
API Gateway
Figure 1.7    Initial architecture with our API gateway and services. Requests to services go through the 
API gateway 
However, this architecture has the following drawbacks. The API gateway adds latency 
and requires a large cluster of hosts. The API gateway host and a service’s host that 
serves a particular request may be in different data centers. A system design that tries 
to route requests through API gateway hosts and service hosts will be an awkward and 
complex design. 


16
Chapter 1  A walkthrough of system design concepts
A solution is to use a service mesh, also called the sidecar pattern. We discuss service 
mesh further in chapter 6. Figure 1.8 illustrates our service mesh. We can use a service 
mesh framework such as Istio. Each host of each service can run a sidecar along the 
main service. We use Kubernetes pods to accomplish this. Each pod can contain its 
service (in one container) as well as its sidecar (in another container). We provide an 
admin interface to configure policies, and these configurations can be distributed to all 
sidecars. 
Service 1 host
Certificate authority
Identity and access
management
Auditor
Administrator
Configure proxies
Interface with 
external services
Control plane
Envoy proxy 
host (sidecar)
Pod
Service 1 host
Envoy proxy 
host (sidecar)
Pod
Service 1 host
Envoy proxy 
host (sidecar)
Pod
Service clients
ELK
Data Plane
Distributed tracing
(Zipkin/Jaeger
/OpenTracing)
Prometheus
Observability Plane
Mesh traffic
Management traffic
Operational traffic
Rate limiting rules
Figure 1.8    Illustration of a service mesh. Prometheus makes requests to each proxy host to pull/
scrape metrics, but this is not illustrated in the diagram because the many arrows will make it too 
cluttered and confusing. Figure adapted from https://livebook.manning.com/book/cloud-native/
chapter-10/146. 


	
17
Prelude: A brief discussion of scaling the various services of a system
With this architecture, all service requests and responses are routed through the sidecar. The service and sidecar are on the same host (i.e., same machine) so they can 
address each other over localhost, and there is no network latency. However, the sidecar does consume system resources. 
Sidecarless service mesh—The cutting edge 
The service mesh required our system to nearly double the number of containers. For 
systems that involve communication between internal services (aka ingress or eastwest), we can reduce this complexity by placing the sidecar proxy logic into client hosts 
that make requests to service hosts. In the design of sidecarless service mesh, client 
hosts receive configurations from the control plane. Client hosts must support the 
control plane API, so they must also include the appropriate network communication 
libraries.
A limitation of sidecarless service mesh is that there must be a client who is in the 
same language as the service. 
The development of sidecarless service mesh platforms is in its early stages. Google Cloud Platform (GCP) Traffic Director is an implementation that was released in 
April 2019 (https://cloud.google.com/blog/products/networking/traffic-director 
-global-traffic-management-for-open-service-mesh). 
Command Query Responsibility Segregation (CQRS) 
Command Query Responsibility Segregation (CQRS) is a microservices pattern where 
command/write operations and query/read operations are functionally partitioned 
onto separate services. Message brokers and ETL jobs are examples of CQRS. Any 
design where data is written to one table and then transformed and inserted into 
another table is an example of CQRS. CQRS introduces complexity but has lower 
latency and better scalability and is easier to maintain and use. The write and read services can be scaled separately. 
You will see many examples of CQRS in this book, though they will not be called out. 
Chapter 15 has one such example, where an Airbnb host writes to the Listing Service, 
but guests read from the Booking Service. (Though the Booking Service also provides 
write endpoints for guests to request bookings, which is unrelated to a host updating 
their listings.) 
You can easily find more detailed definition of CQRS in other sources. 
1.4.7	
Batch and streaming extract, transform, and load (ETL) 
Some of our systems have unpredictable traffic spikes, and certain data processing requests do not have to be synchronous (i.e., process immediately and return 
response): 
¡ Some requests that involve large queries to our databases (such as queries that 
process gigabytes of data). 
¡ It may make more sense to periodically preprocess certain data ahead of requests 
rather than process it only when a request is made. For example, our app’s home 


18
Chapter 1  A walkthrough of system design concepts
page may display the top 10 most frequently learned words across all users in the 
last hour or in the seven days. This information should be processed ahead of 
time once an hour or once a day. Moreover, the result of this processing can be 
reused for all users, rather than repeating the processing for each user. 
¡ Another possible example is that it may be acceptable for users to be shown data 
that is outdated by some hours or days. For example, users do not need to see the 
most updated statistics of the number of users who have viewed their shared content. It is acceptable to show them statistics that are out-of-date by a few hours. 
¡ Writes (e.g., INSERT, UPDATE, DELETE database requests) that do not have to 
be executed immediately. For example, writes to the logging service do not have 
to be immediately written to the hard disk drives of logging service hosts. These 
write requests can be placed in a queue and executed later. 
In the case of certain systems like logging, which receive large request volumes from 
many other systems, if we do not use an asynchronous approach like ETL, the logging system cluster will have to have thousands of hosts to process all these requests 
synchronously. 
We can use a combination of event streaming systems like Kafka (or Kinesis if we use 
AWS) and batch ETL tools such as Airflow for such batch jobs. 
If we wish to continuously process data, rather than periodically running batch jobs, 
we can use streaming tools such as Flink. For example, if a user inputs some data into 
our app, and we want to use it to send certain recommendations or notifications to 
them within seconds or minutes, we can create a Flink pipeline that processes recent 
user inputs. A logging system is usually streaming because it expects a non-stop stream 
of requests. If the requests are less frequent, a batch pipeline will be sufficient. 
1.4.8	
Other common services 
As our company grows and our userbase expands, we develop more products, and 
our products should become increasingly customizable and personalized to serve this 
large, growing, and diverse userbase. We will require numerous other services to satisfy 
the new requirements that come with this growth and to take advantage of it. They 
include the following:
¡ Customer/external user credentials management for external user authentication and authorization. 
¡ Various storage services, including database services. The specific requirements 
of each system mean that there are certain optimal ways that the data it uses 
should be persisted, processed, and served. We will need to develop and maintain 
various shared storage services that use different technologies and techniques. 
¡ Asynchronous processing. Our large userbase requires more hosts and may create unpredictable traffic spikes to our services. To handle traffic spikes, we need 
asynchronous processing to efficiently utilize our hardware and reduce unnecessary hardware expenditure.


	
19
Prelude: A brief discussion of scaling the various services of a system
¡ Notebooks service for analytics and machine learning, including experimentation, model creation, and deployment. We can use our large customer base 
for experimentation to discover user preferences, personalize user experiences, 
attract more users, and discover other ways to increase our revenue.
¡ Internal search and subproblems (e.g., autocomplete/typeahead service). Many 
of our web or mobile applications can have search bars for users to search for 
their desired data. 
¡ Privacy compliance services and teams. Our expanding user numbers and large 
amount of customer data will attract malicious external and internal actors, 
who will attempt to steal data. A privacy breach on our large userbase will affect 
numerous people and organizations. We must invest in safeguarding user privacy.
¡ Fraud detection. The increasing revenue of our company will make it a tempting target for criminals and fraudsters, so effective fraud detection systems are a 
must.
1.4.9	
Cloud vs. bare metal 
We can manage our own hosts and data centers or outsource this to cloud vendors. 
This section is a comparative analysis of both approaches.
General considerations 
At the beginning of this section, we decided to use cloud services (renting hosts from 
providers such as Amazon’s AWS, DigitalOcean, or Microsoft Azure) instead of bare 
metal (owning and managing our own physical machines). 
Cloud providers provide many services we will require, including CI/CD, logging, 
monitoring, alerting, and simplified setup and management of various database types 
including caches, SQL, and NoSQL. 
If we chose bare metal from the beginning, we would have set up and maintained any 
of these services that we require. This may take away attention and time from feature 
development, which may prove costly to our company. 
We must also consider the cost of engineering labor vs. cloud tools. Engineers are 
very expensive resources, and besides being monetarily costly, good engineers tend to 
prefer challenging work. Bore them with menial tasks such as small-scale setups of common services, and they may move to another company and be difficult to replace in a 
competitive hiring market. 
Cloud tools are often cheaper than hiring engineers to set up and maintain your 
bare-metal infrastructure. We most likely do not possess the economies of scale and 
their accompanying unit cost efficiencies or the specialized expertise of dedicated 
cloud providers. If our company is successful, it may reach a growth stage where we have 
the economies of scale to consider bare metal. 
Using cloud services instead of bare metal has other benefits including the following. 


20
Chapter 1  A walkthrough of system design concepts
Simplicity of setup 
On a cloud provider’s browser app, we can easily choose a package most suited for our 
purposes. On bare metal, we would need steps such as installing server software like 
Apache or setting up network connections and port forwarding. 
Cost advantages 
Cloud has no initial upfront cost of purchasing physical machines/servers. A cloud 
vendor allows us to pay for incremental use and may offer bulk discounts. Scaling up 
or down in response to unpredictably changing requirements is easy and fast. If we 
choose bare metal, we may end up in a situation where we have too few or too many 
physical machines. Also, some cloud providers offer “auto-scaling” services, which 
automatically resize our cluster to suit the present load.
That being said, cloud is not always cheaper than bare metal. Dropbox (https://
www.geekwire.com/2018/dropbox-saved-almost-75-million-two-years-building-tech 
-infrastructure/) and Uber (https://www.datacenterknowledge.com/uber/want-build 
-data-centers-uber-follow-simple-recipe) are two examples of companies that host on 
their own data centers because their requirements meant it was the more cost-efficient 
choice.
Cloud services may provide better support and quality 
Anecdotal evidence suggests that cloud services generally provide superior performance, user experience, and support and have fewer and less serious outages. A possible reason is that cloud services must be competitive in the market to attract and retain 
customers, compared to bare metal, which an organization’s users have little choice 
but to use. Many organizations tend to value and pay more attention to customers than 
internal users or employees, possibly because customer revenue is directly measurable, 
while the benefit of providing high-quality services and support to internal users may 
be more difficult to quantify. The corollary is that the losses to revenue and morale 
from poor-quality internal services are also difficult to quantify. Cloud services may also 
have economies of scale that bare metal lacks because the efforts of the cloud service’s 
team are spread across a larger user base. 
External-facing documentation may be better than internal-facing documentation. 
It may be better written, updated more often, and placed on a well-organized website 
that is easy to search. There may be more resources allocated, so videos and step-by-step 
tutorials may be provided. 
External services may provide higher-quality input validation than internal services. 
Considering a simple example, if a certain UI field or API endpoint field requires the 
user to input an email address, the service should validate that the user’s input is actually a valid email address. A company may pay more attention to external users who 
complain about the poor quality of input validation because they may stop using and 
paying for the company’s product. Similar feedback from internal users who have little 
choice may be ignored. 
When an error occurs, a high-quality service should return instructive error messages 
that guide the user on how to remedy the error, preferably without the time-consuming 


	
21
Prelude: A brief discussion of scaling the various services of a system
process of having to contact support personnel or the service’s developers. External 
services may provide better error messages as well as allocate more resources and incentives to provide high-quality support. 
If a customer sends a message, they may receive a reply within minutes or hours, 
while it may take hours or days to respond to an employee’s questions. Sometimes a 
question to an internal helpdesk channel is not responded to at all. The response to an 
employee may be to direct them to poorly written documentation. 
An organization’s internal services can only be as good as external services if the 
organization provides adequate resources and incentives. Because better user experience and support improve users’ morale and productivity, an organization may consider setting up metrics to measure how well internal users are served. One way to avoid 
these complications is to use cloud services. These considerations can be generalized to 
external vs. internal services. 
Last, it is the responsibility of individual developers to hold themselves to high standards but not to make assumptions about the quality of others’ work. However, the 
persistent poor quality of internal dependencies can hurt organizational productivity 
and morale. 
Upgrades 
Both the hardware and software technologies used in an organization’s bare metal 
infrastructure will age and be difficult to upgrade. This is obvious for finance companies that use mainframes. It is extremely costly, difficult, and risky to switch from mainframes to commodity servers, so such companies continue to buy new mainframes, 
which are far more expensive than their equivalent processing power in commodity 
servers. Organizations that use commodity servers also need the expertise and effort to 
constantly upgrade their hardware and software. For example, even upgrading the version of MySQL used in a large organization takes considerable time and effort. Many 
organizations prefer to outsource such maintenance to cloud providers. 
Some disadvantages 
One disadvantage of cloud providers is vendor lock-in. Should we decide to transfer 
some or all components of our app to another cloud vendor, this process may not 
be straightforward. We may need considerable engineering effort to transfer data and 
services from one cloud provider to another and pay for duplicate services during this 
transition. 
There are many possible reasons we will want to migrate out of a vendor. Today, the 
vendor may be a well-managed company that fulfills a demanding SLA at a competitive 
price, but there is no guarantee this will always be true. The quality of a company’s service may degrade in the future, and it may fail to fulfill its SLA. The price may become 
uncompetitive, as bare metal or other cloud vendors become cheaper in the future. Or 
the vendor may be found to be lacking in security or other desirable characteristics. 
Another disadvantage is the lack of ownership over the privacy and security of our 
data and services. We may not trust the cloud provider to safeguard our data or ensure 
the security of our services. With bare metal, we can personally verify privacy and 
security. 


22
Chapter 1  A walkthrough of system design concepts
For these reasons, many companies adopt a multi-cloud strategy, using multiple 
cloud vendors instead of a single one, so these companies can migrate away from any 
particular vendor at short notice should the need suddenly arise.
1.4.10	 Serverless: Function as a Service (FaaS)
If a certain endpoint or function is infrequently used or does not have strict latency 
requirements, it may be cheaper to implement it as a function on a Function as a Service (FaaS) platform, such as AWS Lambda or Azure Functions. Running a function 
only when needed means that there does not need to be hosts continuously waiting for 
requests to this function. 
OpenFaaS and Knative are open-source FaaS solutions that we can use to support 
FaaS on our own cluster or as a layer on AWS Lambda to improve the portability of our 
functions between cloud platforms. As of this book’s writing, there is no integration 
between open-source FaaS solutions and other vendor-managed FaaS such as Azure 
Functions. 
Lambda functions have a timeout of 15 minutes. FaaS is intended to process requests 
that can complete within this time. 
In a typical configuration, an API gateway service receives incoming requests and 
triggers the corresponding FaaS functions. The API gateway is necessary because there 
needs to be a continuously running service that waits for requests. 
Another benefit of FaaS is that service developers need not manage deployments 
and scaling and can concentrate on coding their business logic. 
Note that a single run of a FaaS function requires steps such as starting a Docker 
container, starting the appropriate language runtime (Java, Python, Node.js, etc.) and 
running the function, and terminating the runtime and Docker container. This is commonly referred to as cold start. Frameworks that take minutes to start, such as certain 
Java frameworks, may be unsuitable for FaaS. This spurred the development of JDKs 
with fast startups and low memory footprints such as GraalVM (https://www.graalvm 
.org/). 
Why is this overhead required? Why can’t all functions be packaged into a single 
package and run across all host instances, similar to a monolith? The reasons are the 
disadvantages of monoliths (refer to appendix A). 
Why not have a frequently-used function deployed to certain hosts for a certain 
amount of time, (i.e., with an expiry)? Such a system is similar to auto-scaling microservices and can be considered when using frameworks that take a long time to start. 
The portability of FaaS is controversial. At first glance, an organization that has done 
much work in a proprietary FaaS like AWS Lambda can become locked in; migrating 
to another solution becomes difficult, time-consuming, and expensive. Open-source 
FaaS platforms are not a complete solution, because one must provision and maintain 
one’s own hosts, which defeats the scalability purpose of FaaS. This problem becomes 
especially significant at scale, when FaaS may become much more expensive than bare 
metal. 


	
23
Summary
However, a function in FaaS can be written in two layers: an inner layer/function that 
contains the main logic of the function, wrapped by an outer layer/function that contains vendor-specific configurations. To switch vendors for any function, one only needs 
to change the outer function. 
Spring Cloud Function (https://spring.io/projects/spring-cloud-function) is an 
emerging FaaS framework that is a generalization of this concept. It is supported by 
AWS Lambda, Azure Functions, Google Cloud Functions, Alibaba Function Compute, 
and may be supported by other FaaS vendors in the future. 
1.4.11	 Conclusion: Scaling backend services 
In the rest of part 1, we discuss concepts and techniques to scale a backend service. 
A frontend/UI service is usually a Node.js service, and all it does is serve the same 
browser app written in a JavaScript framework like ReactJS or Vue.js to any user, so 
it can be scaled simply by adjusting the cluster size and using GeoDNS. A backend 
service is dynamic and can return a different response to each request. Its scalability 
techniques are more varied and complex. We discussed functional partitioning in the 
previous example and will occasionally touch on it as needed.
Summary
¡ System design interview preparation is critical to your career and also benefits 
your company.
¡ The system design interview is a discussion between engineers about designing a 
software system that is typically provided over a network.
¡ GeoDNS, caching, and CDN are basic techniques for scaling our service.
¡ CI/CD tools and practices allow feature releases to be faster with fewer bugs. 
They also allow us to divide our users into groups and expose each group to a 
different version of our app for experimentation purposes.
¡ Infrastructure as Code tools like Terraform are useful automation tools for cluster management, scaling, and feature experimentation.
¡ Functional partitioning and centralization of cross-cutting concerns are key elements of system design.
¡ ETL jobs can be used to spread out the processing of traffic spikes over a longer 
time period, which reduces our required cluster size.
¡ Cloud hosting has many advantages. Cost is often but not always an advantage. 
There are also possible disadvantages such as vendor lock-in and potential privacy and security risks.
¡ Serverless is an alternative approach to services. In exchange for the cost 
advantage of not having to keep hosts constantly running, it imposes limited 
functionality.


24
2
A typical system 
design interview flow
This chapter covers
¡ Clarifying system requirements and optimizing 	
	 possible tradeoffs
¡ Drafting your system’s API specification
¡ Designing the data models of your system
¡ Discussing concerns like logging, monitoring, 	
	 and alerting or search
¡ Reflecting on your interview experience and 	
	 evaluating the company
In this chapter, we will discuss a few principles of system design interviews that must 
be followed during your 1 hour system design interview. When you complete this 
book, refer to this list again. Keep these principles in mind during your interviews: 
1	 Clarify functional and non-functional requirements (refer to chapter 3), such 
as QPS (queries per second) and P99 latency. Ask whether the interviewer 
desires wants to start the discussion from a simple system and then scale up and 
design more features or start with immediately designing a scalable system. 
2	 Everything is a tradeoff. There is almost never any characteristic of a system 
that is entirely positive and without tradeoffs. Any new addition to a system to 


	
25
﻿
improve scalability, consistency, or latency also increases complexity and cost and 
requires security, logging, monitoring, and alerting. 
3	 Drive the interview. Keep the interviewer’s interest strong. Discuss what they 
want. Keep suggesting topics of discussion to them. 
4	 Be mindful of time. As just stated, there is too much to discuss in 1 hour. 
5	 Discuss logging, monitoring, alerting, and auditing. 
6	 Discuss testing and maintainability including debuggability, complexity, security, 
and privacy. 
7	 Consider and discuss graceful degradation and failure in the overall system and 
every component, including silent and disguised failures. Errors can be silent. 
Never trust anything. Don’t trust external or internal systems. Don’t trust your 
own system. 
8	 Draw system diagrams, flowcharts, and sequence diagrams. Use them as visual 
aids for your discussions. 
9	 The system can always be improved. There is always more to discuss. 
A discussion of any system design interview question can last for many hours. You will 
need to focus on certain aspects by suggesting to the interviewer various directions of 
discussion and asking which direction to go. You have less than 1 hour to communicate 
or hint the at full extent of your knowledge. You must possess the ability to consider 
and evaluate relevant details and to smoothly zoom up and down to discuss high-level 
architecture and relationships and low-level implementation details of every component. If you forget or neglect to mention something, the interviewer will assume you 
don’t know it. One should practice discussing system design questions with fellow engineers to improve oneself in this art. Prestigious companies interview many polished 
candidates, and every candidate who passes is well-drilled and speaks the language of 
system design fluently. 
The question discussions in this section are examples of the approaches you can take 
to discuss various topics in a system design interview. Many of these topics are common, 
so you will see some repetition between the discussions. Pay attention to the use of common industry terms and how many of the sentences uttered within the time-limited 
discussion are filled with useful information. 
The following list is a rough guide. A system design discussion is dynamic, and we 
should not expect it to progress in the order of this list: 
1	 Clarify the requirements. Discuss tradeoffs. 
2	 Draft the API specification. 
3	 Design the data model. Discuss possible analytics. 
4	 Discuss failure design, graceful degradation, monitoring, and alerting. Other 
topics include bottlenecks, load balancing, removing single points of failure, 
high availability, disaster recovery, and caching.
5	 Discuss complexity and tradeoffs, maintenance and decommissioning processes, 
and costs. 


26
Chapter 2  A typical system design interview flow
2.1	
Clarify requirements and discuss tradeoffs 
Clarifying the requirements of the question is the first checkbox to tick off during an 
interview. Chapter 3 describes the details and importance of discussing functional and 
non-functional requirements. 
We end this chapter with a general guide to discussing requirements in an interview. 
We will go through this exercise in each question of part 2. We emphasize that you keep 
in mind that your particular interview may be a unique situation, and you should deviate from this guide as required by your situation.
Discuss functional requirements within 10 minutes because that is already ≥20% of 
the interview time. Nonetheless, attention to detail is critical. Do not write down the 
functional requirements one at a time and discuss them. You may miss certain requirements. Rather, quickly brainstorm and scribble down a list of functional requirements 
and then discuss them. We can tell the interviewer that we want to ensure we have captured all crucial requirements, but we also wish to be mindful of time. 
We can begin by spending 30 seconds or 1 minute discussing the overall purpose 
of the system and how it fits into the big-picture business requirements. We can briefly 
mention endpoints common to nearly all systems, like health endpoints, signup, and 
login. Anything more than a brief discussion is unlikely to be within the scope of the 
interview. We then discuss the details of some common functional requirements: 
1	 Consider user categories/roles: 
a	 Who will use this system and how? Discuss and scribble down user stories. 
Consider various combinations of user categories, such as manual versus programmatic or consumer versus enterprise. For example, a manual/consumer 
combination involves requests from our consumers via our mobile or browser 
apps. A programmatic/enterprise combination involves requests from other 
services or companies. 
b	 Technical or nontechnical? Design platforms or services for developers or 
non-developers. Technical examples include a database service like key-value 
store, libraries for purposes like consistent hashing, or analytics services. 
Non-technical questions are typically in the form of “Design this well-known 
consumer app.” In such questions, discuss all categories of users, not just the 
non-technical consumers of the app. 
c	 List the user roles (e.g., buyer, seller, poster, viewer, developer, manager). 
d	 Pay attention to numbers. Every functional and non-functional requirement 
must have a number. Fetch news items? How many news items? How much 
time? How many milliseconds/seconds/hours/days?
e	 Any communication between users or between users and operations staff? 
f	 Ask about i18n and L10n support, national or regional languages, postal 
address, price, etc. Ask whether multiple currency support is required. 


	
27
Clarify requirements and discuss tradeoffs 
2	 Based on the user categories, clarify the scalability requirements. Estimate the 
number of daily active users and then estimate the daily or hourly request rate. 
For example, if a search service has 1 billion daily users, each submitting 10 
search requests, there are 10 billion daily requests or 420 million hourly requests. 
3	 Which data should be accessible to which users? Discuss the authentication 
and authorization roles and mechanisms. Discuss the contents of the response 
body of the API endpoint. Next, discuss how often is data retrieved—real-time, 
monthly reports, or another frequency? 
4	 Search. What are possible use cases that involve search? 
5	 Analytics is a typical requirement. Discuss possible machine learning requirements, including support for experimentation such as A/B testing or multi-armed 
bandit. Refer to https://www.optimizely.com/optimization-glossary/ab-testing/ 
and https://www.optimizely.com/optimization-glossary/multi-armed-bandit/ for 
introductions to these topics. 
6	 Scribble down pseudocode function signatures (e.g., fetchPosts(userId)) to 
fetch posts by a certain user and match them to the user stories. Discuss with the 
interviewer which requirements are needed and which are out of scope. 
Always ask, “Are there other user requirements?” and brainstorm these possibilities. 
Do not allow the interviewer to do the thinking for you. Do not give the interviewer the 
impression that you want them to do the thinking for you or want them to tell you all 
the requirements. 
Requirements are subtle, and one often misses details even if they think they have 
clarified them. One reason software development follows agile practices is that requirements are difficult or impossible to communicate. New requirements or restrictions are 
constantly discovered through the development process. With experience, one learns 
the clarifying questions to ask. 
Display your awareness that a system can be expanded to serve other functional 
requirements in the future and brainstorm such possibilities. 
The interviewer should not expect you to possess all domain knowledge, so you may 
not think of certain requirements that require specific domain knowledge. What you 
do need is demonstrate your critical thinking, attention to detail, humility, and willingness to learn. 
Next, discuss non-functional requirements. Refer to chapter 3 for a detailed discussion of non-functional requirements. We may need to design our system to serve the 
entire world population and assume that our product has complete global market dominance. Clarify with your interviewer whether we should design immediately for scalability. If not, they may be more interested in how we consider complicated functional 
requirements. This includes the data models we design. After we discuss requirements, 
we can proceed to discuss our system design. 


28
Chapter 2  A typical system design interview flow
2.2	
Draft the API specification 
Based on the functional requirements, determine the data that the system’s users 
expect to receive from and send to the system. We will generally spend less than five 
minutes scrabbling down a draft of the GET, POST, PUT, and DELETE endpoints, 
including path and query parameters. It is generally inadvisable to linger on drafting 
the endpoints. Inform the interviewer that there is much more to discuss within our 50 
minutes, so we will not use much time here. 
You should have already clarified the functional requirements before scribbling 
these endpoints; you are past the appropriate section of the interview to clarify functional requirements and should not do so here unless you missed anything. 
Next, propose an API specification and describe how it satisfies the functional 
requirements, then briefly discuss it and identify any functional requirements that you 
may have missed. 
2.2.1	
Common API endpoints 
These are common endpoints of most systems. You can quickly go over these endpoints and clarify that they are out of scope. It is very unlikely that you will need to 
discuss them in detail, but it never hurts to display that you are detail-oriented while 
also seeing the big picture. 
Health 
GET /health is a test endpoint. A 4xx or 5xx response indicates the system has production problems. It may just do a simple database query, or it may return health information such as disk space, statuses of various other endpoints, and application logic 
checks. 
Signup and login (authentication) 
An app user will typically need to sign up (POST /signup) and log in (POST /login) 
prior to submitting content to the app. OpenID Connect is a common authentication 
protocol, discussed in appendix B. 
User and content management 
We may need endpoints to get, modify, and delete user details. Many consumer apps 
provide channels for users to flag/report inappropriate content, such as content that 
is illegal or violates community guidelines.
2.3	
Connections and processing between users and data 
In section 2.1, we discussed the types of users and data and which data should be accessible to which users. In section 2.2, we designed API endpoints for users to CRUD 
(create, read, update, and delete) data. We can now draw diagrams to represent the 
connections between user and data and to illustrate various system components and 
the data processing that occurs between them.


	
29
Design the data model 
Phase 1: 
¡ Draw a box to represent each type of user. 
¡ Draw a box to represent each system that serves the functional requirements. 
¡ Draw the connections between users and systems. 
Phase 2: 
¡ Break up request processing and storage. 
¡ Create different designs based on the non-functional requirements, such as realtime versus eventual consistency. 
¡ Consider shared services. 
Phase 3: 
¡ Break up the systems into components, which will usually be libraries or services. 
¡ Draw the connections. 
¡ Consider logging, monitoring, and alerting. 
¡ Consider security. 
Phase 4: 
¡ Include a summary of our system design. 
¡ Provide any new additional requirements. 
¡ Analyze fault-tolerance. What can go wrong with each component? Network 
delays, inconsistency, no linearizability. What can we do to prevent and/or mitigate each situation and improve the fault-tolerance of this component and the 
overall system? 
Refer to appendix C for an overview of the C4 model, which is a system architecture diagram technique to decompose a system into various levels of abstraction.
2.4	
Design the data model 
We should discuss whether we are designing the data model from scratch or using 
existing databases. Sharing databases between services is commonly regarded as an 
antipattern, so if we are using existing databases, we should build more API endpoints 
designed for programmatic customers, as well as batch and/or streaming ETL pipelines from and to those other databases as required. 
The following are common problems that may occur with shared databases: 
¡ Queries from various services on the same tables may compete for resources. Certain queries, such as UPDATE on many rows, or transactions that contain other 
long-running queries may lock a table for an extended period of time. 


30
Chapter 2  A typical system design interview flow
¡ Schema migrations are more complex. A schema migration that benefits one 
service may break the DAO code of other services. This means that although an 
engineer may work only on that service, they need to keep up to date with the 
low-level details of the business logic and perhaps even the source code of other 
services that they do not work on, which may be an unproductive use of both 
their time and the time of other engineers who made those changes and need to 
communicate it to them and others. More time will be spent in writing and reading documentation and presentation slides and in meetings. Various teams may 
take time to agree on proposed schema migrations, which may be an unproductive use of engineering time. Other teams may not be able to agree on schema 
migrations or may compromise on certain changes, which will introduce technical debt and decrease overall productivity. 
¡ The various services that share the same set of databases are restricted to using 
those specific database technologies (.g., MySQL, HDFS, Cassandra, Kafka, etc.), 
regardless of how well-suited those technologies are to each service’s use cases. 
Services cannot pick the database technology that best suits their requirements. 
This means that in either case we will need to design a new schema for our service. 
We can use the request and response bodies of the API endpoints we discussed in the 
previous section as starting points to design our schema, closely mapping each body to 
a table’s schema and probably combining the bodies of read (GET) and write (POST 
and PUT) requests of the same paths to the same table. 
2.4.1	
Example of the disadvantages of multiple services sharing databases 
If we were designing an ecommerce system, we may want a service that can retrieve 
business metric data, such as the total number of orders in the last seven days. Our 
teams found that without a source of truth for business metric definitions, different 
teams were computing metrics differently. For example, should the total number of 
orders include canceled or refunded orders? What time zone should be used for the 
cutoff time of “seven days ago”? Does “last seven days” include the present day? The 
communication overhead between multiple teams to clarify metric definitions was 
costly and error-prone. 
Although computing business metrics uses order data from the Orders service, we 
decide to form a new team to create a dedicated Metrics service, since metric definitions can be modified independently of order data. 
The Metrics service will depend on the Orders service for order data. A request for a 
metric will be processed as follows: 
1	 Retrieve the metric. 
2	 Retrieve the related data from the Orders service. 
3	 Compute the metric.
4	 Return the metric’s value. 


	
31
Design the data model 
If both services share the same database, the computation of a metric makes SQL queries on Orders service’s tables. Schema migrations become more complex. For example, the Orders team decides that users of the Order table have been making too many 
large queries on it. After some analysis, the team determined that queries on recent 
orders are more important and require higher latency than queries on older orders. 
The team proposes that the Order table should contain only orders from the last year, 
and older orders will be moved to an Archive table. The Order table can be allocated a 
larger number of followers/read replicas than the Archive table. 
The Metrics team must understand this proposed change and change metric computation to occur on both tables. The Metrics team may object to this proposed change, 
so the change may not go ahead, and the organizational productivity gain from faster 
queries on recent order data cannot be achieved. 
If the Orders team wishes to move the Order table to Cassandra to use its low write 
latency while the Metrics service continues using SQL because of its simplicity and 
because it has a low write rate, the services can no longer share the same database. 
2.4.2	
A possible technique to prevent concurrent user update conflicts
There are many situations where a client application allows multiple users to edit a 
shared configuration. If an edit to this shared configuration is nontrivial for a user (if 
a user needs to spend more than a few seconds to enter some information before submitting their edit), it may be a frustrating UX if multiple users simultaneously edit this 
configuration, and then overwrite each other’s changes when they save them. Source 
control management prevents this for source code, but most other situations involve 
non-technical users, and we obviously cannot expect them to learn git. 
For example, a hotel room booking service may require users to spend some time to 
enter their check-in and check-out dates and their contact and payment information 
and then submit their booking request. We should ensure that multiple users do not 
overbook the room.
Another example may be configuring the contents of a push notification. For example, our company may provide a browser app for employees to configure push notifications sent to our Beigel app (refer to chapter 1). A particular push notification 
configuration may be owned by a team. We should ensure that multiple team members do not edit the push notification simultaneously and then overwrite each other’s 
changes.
There are many ways of preventing concurrent updates. We present one possible way 
in this section. 
To prevent such situations, we can lock a configuration when it is being edited. Our 
service may contain an SQL table to store these configurations. We can add a timestamp 
column to the relevant SQL table that we can name “unix_locked” and string columns 
“edit_username” and “edit_email.” (This schema design is not normalized, but it is usually ok in practice. Ask your interviewer whether they insist on a normalized schema.) 
We can then expose a PUT endpoint that our UI can use to notify our backend when a 


32
Chapter 2  A typical system design interview flow
user clicks on an edit icon or button to start editing the query string. Referring to figure 
2.1, here are a series of steps that may occur when two users decide to edit a push notification at approximately the same time. One user can lock a configuration for a certain 
period (e.g., 10 minutes), and another user finds that it is locked:
1	 Alice and Bob are both viewing the push notification configuration on our Notifications browser app. Alice decides to update the title from “Celebrate National 
Bagel Day!” to “20% off on National Bagel Day!” She clicks on the Edit button. 
The following steps occur:
a	 The click event sends a PUT request, which sends her username and email to 
the backend. The backend’s load balancer assigns this request to a host. 
b	 Alice’s backend host makes two SQL queries, one at a time. First, it determines 
the current unix_locked time: 
SELECT unix_locked FROM table_name WHERE config_id = {config_id}. 
c	 The backend checks whether the “edit_start” timestamp is less than 12 minutes ago. (This includes a 2 minute buffer in case the countdown timer in 
step 2 started late, and also because hosts’ clocks cannot be perfectly synchronized.) If so, it updates the row to indicate to lock the configuration. The 
UPDATE query sets “edit_start” to the backend’s current UNIX time and overwrites the “edit_username” and “edit_email” with Alice’s username and email. 
We need the “unix_locked” filter just in case another user has changed it in 
the meantime. The UPDATE query returns a Boolean to indicate whether it 
ran successfully: 
UPDATE table_name SET unix_locked = {new_time}, edit_username = {username}, 
edit_email = {email} WHERE config_id = {config_id} AND unix_locked = 
{unix_locked}
d	 If the UPDATE query was successful, the backend returns 200 success to the 
UI with a response body like {“can_edit”: “true”}.
2	 The UI opens a page where Alice can make this edit and displays a 10-minute 
countdown timer. She erases the old title and starts to type the new title.
3	 In between the SQL queries of steps 1b and 1c, Bob decides to edit the configuration too:
a	 He clicks on the Edit button, triggering a PUT request, which is assigned to a 
different host.
b	 The first SQL query returns the same unix_locked time as in step 1b.
c	 The second SQL query is sent just after the query in step 1c. SQL DML queries 
are sent to the same host (see section 4.3.2). This means this query cannot 
run until the query in step 1c completes. When the query runs, the unix_time 
value had changed, so the row is not updated, and the SQL service returns 


	
33
Design the data model 
false to the backend. The backend returns a 200 success to the UI with a 
response body like {“can_edit”: “false”, “edit_start”: “1655836315”, “edit_username”: “Alice”, “edit_email”: “alice@beigel.com”}. 
d	 The UI computes the number of minutes Alice has left and displays a banner 
notification that states, “Alice (alice@beigel.com) is making an edit. Try again 
in 8 minutes.”
4	 Alice finishes her edits and clicks on the Save button. This triggers a PUT request 
to the backend, which saves her edited values and erases “unix_locked”, “edit_
start”, “edit_username”, and “edit_email”. 
5	 Bob clicks on the Edit button again, and now he can make edits. If Bob had 
clicked the Edit button at least 12 minutes after the “edit_start” value, he can also 
make edits. If Alice had not saved her changes before her countdown expires, 
the UI will display a notification to inform her that she cannot save her changes 
anymore. 
Alice's
backend host
SQL service
unix_locked value
Bob's
backend host
Same unix_locked value as 1b.
3b. Same request as 1b.
1c. UPDATE the row of the desired config ID.
UPDATE success. unix_locked value changed.
UPDATE failed.
3c. UPDATE a row which no longer exists.
4. Erase "unix_locked" and editor details.
UPDATE success.
unix_locked value.
5. Get unix_locked value of the same config ID.
UPDATE the row of this config ID. 
UPDATE success.
1b. Get unix_locked value of the desired config ID.
Figure 2.1    Illustration of a locking mechanism that uses SQL. Here, two users request to update the 
same SQL row that corresponds to the same configuration ID. Alice’s host first gets the unix_locked 
timestamp value of the desired configuration ID, then sends an UPDATE query to update that row, so 
Alice has locked that specific configuration ID. Right after her host sent that query in step 1c, Bob’s host 
sends an UPDATE query, too, but Alice’s host had changed the unix_locked value, so Bob’s UPDATE query 
cannot run successfully, and Bob cannot lock that configuration ID.


34
Chapter 2  A typical system design interview flow
What if Bob visits the push notification configuration page after Alice starts editing 
the configuration? A possible UI optimization at this point is to disable the Edit button 
and display the banner notification, so Bob knows he cannot make edits because Alice 
is doing so. To implement this optimization, we can add the three fields to the GET 
response for the push notification configuration, and the UI should process those 
fields and render the Edit button as “enabled” or “disabled.”
Refer to https://vladmihalcea.com/jpa-entity-version-property-hibernate/ for an 
overview of version tracking with Jakarta Persistence API and Hibernate. 
2.5	
Logging, monitoring, and alerting
There are many books on logging, monitoring, and alerting. In this section, we will 
discuss key concepts that one must mention in an interview and dive into specific concepts that one may be expected to discuss. Never forget to mention monitoring to the 
interviewer. 
2.5.1	
The importance of monitoring
Monitoring is critical for every system to provide visibility into the customer’s experience. We need to identify bugs, degradations, unexpected events, and other weaknesses in our system’s ability to satisfy current and possible future functional and 
non-functional requirements.
Web services may fail at any time. We may categorize these failures by urgency and 
how quickly they need attention. High-urgency failures must be attended to immediately. Low-urgency failures may wait until we complete higher-priority tasks. Our 
requirements and discretion determine the multiple levels of urgency that we define. 
If our service is a dependency of other services, every time those services experience 
degradations, their teams may identify our service as a potential source of those degradations, so we need a logging and monitoring setup that will allow us to easily investigate possible degradations and answer their questions. 
2.5.2	
Observability
This leads us to the concept of observability. The observability of our system is a measure of how well-instrumented it is and how easily we can find out what’s going on 
inside it (John Arundel & Justin Domingus, Cloud Native DevOps with Kubernetes, p. 
272, O’Reilly Media Inc, 2019.). Without logging, metrics, and tracing, our system is 
opaque. We will not easily know how well a code change meant to decrease P99 of a 
particular endpoint by 10% works in production. If P99 decreased by much less than 
10% or much more than 10%, we should be able to derive relevant insights from our 
instrumentation on why our predictions fell short. 
Refer to Google’s SRE book (https://sre.google/sre-book/monitoring-distributed 
-systems/#xref_monitoring_golden-signals) for a detailed discussion of the four golden 
signals of monitoring: latency, traffic, errors, and saturation. 


	
35
Logging, monitoring, and alerting
1	 Latency—We can set up alerts for latency that exceeds our service-level agreement 
(SLA), such as more than 1 second. Our SLA may be for any individual request 
more than 1 second, or alerts that trigger for a P99 over a sliding window (e.g., 5 
seconds, 10 seconds, 1 minute, 5 minutes). 
2	 Traffic—Measured in HTTP requests per second. We can set up alerts for various 
endpoints that trigger if there is too much traffic. We can set appropriate numbers based on the load limit determined in our load testing. 
3	 Errors—Set up high-urgency alerts for 4xx or 5xx response codes that must be 
immediately addressed. Trigger low-urgency (or high urgency, depending on 
your requirements) alerts on failed audits. 
4	 Saturation—Depending on whether our system’s constraint is CPU, memory, or 
I/O, we can set utilization targets that should not be exceeded. We can set up 
alerts that trigger if utilization targets are reached. Another example is storage 
utilization. We can set up an alert that triggers if storage (due to file or database 
usage) may run out within hours or days. 
The three instruments of monitoring and alerting are metrics, dashboards, and alerts. 
A metric is a variable we measure, like error count, latency, or processing time. A dashboard provides a summary view of a service’s core metrics. An alert is a notification sent 
to service owners in a reaction to some problem happening in the service. Metrics, 
dashboards, and alerts are populated by processing log data. We may provide a common browser UI to create and manage them more easily. 
OS metrics like CPU utilization, memory utilization, disk utilization, and network 
I/O can be included in our dashboard and used to tune the hardware allocation for our 
service as appropriate or detect memory leaks. 
On a backend application, our backend framework may log each request by default 
or provide simple annotations on the request methods to turn on logging. We can put 
logging statements in our application code. We can also manually log the values of certain variables within our code to help us understand how the customer’s request was 
processed. 
Scholl et al. (Boris Scholl, Trent Swanson & Peter Jausovec. Cloud Native: Using Containers, Functions, and Data to build Next-Generation Applications. O’Reilly, 2019. p. 145.) 
states the following general considerations in logging: 
¡ Log entries should be structured to be easy to parse by tools and automation. 
¡ Each entry should contain a unique identifier to trace requests across services 
and share between users and developers. 
¡ Log entries should be small, easy to read, and useful. 
¡ Timestamps should use the same time zone and time format. A log that contains 
entries with different time zones and time formats is difficult to read or parse. 
¡ Categorize log entries. Start with debug, info, and error. 
¡ Do not log private or sensitive information like passwords or connection strings. 
A common term to refer to such information is Personally Identifiable Information (PII). 


36
Chapter 2  A typical system design interview flow
Logs that are common to most services include the following. Many request-level logging tools have default configurations to log these details: 
¡ Host logging: 
–	 CPU and memory utilization on the hosts 
–	 Network I/O 
¡ Request-level logging captures the details of every request: 
–	 Latency 
–	 Who and when made the request 
–	 Function name and line number 
–	 Request path and query parameters, headers, and body 
–	 Return status code and body (including possible error messages)
In a particular system, we may be particularly interested in certain user experiences, 
such as errors. We can place log statements within our application and set up customized metrics, dashboards, and alerts that focus on these user experiences. For example, 
to focus on 5xx errors due to application bugs, we can create metrics, dashboards and 
alerts that process certain details like request parameters and return status codes and 
error messages, if any. 
We should also log events to monitor how well our system satisfies our unique functional and non-functional requirements. For example, if we build a cache, we want to 
log cache faults, hits, and misses. Metrics should include the counts of faults, hits, and 
misses. 
In enterprise systems, we may wish to give users some access to monitoring or even 
build monitoring tools specifically for users for example, customers can create dashboards to track the state of their requests and filter and aggregate metrics and alerts by 
categories such as URL paths. 
We should also discuss how to address possible silent failures. These may be due to 
bugs in our application code or dependencies such as libraries and other services that 
allow the response code to be 2xx when it should be 4xx or 5xx or may indicate your 
service requires logging and monitoring improvements. 
Besides logging, monitoring, and alerting on individual requests, we may also create 
batch and streaming audit jobs to validate our system’s data. This is akin to monitoring 
our system’s data integrity. We can create alerts that trigger if the results of the job indicate failed validations. Such a system is discussed in chapter 10.
2.5.3	
Responding to alerts 
A team that develops and maintains a service may typically consist of a few engineers. 
This team may set up an on-call schedule for the service’s high-urgency alerts. An 
on-call engineer may not be intimately familiar with the cause of a particular alert, so 
we should prepare a runbook that contains a list of the alerts, possible causes, and procedures to find and fix the cause. 


	
37
Logging, monitoring, and alerting
As we prepare the runbook, if we find that certain runbook instructions consist of 
a series of commands that can easily be copied and pasted to solve the problem (e.g., 
restarting a host), these steps should be automated in the application, along with logging that these steps were run (Mike Julian, Practical Monitoring, chapter 3, O’Reilly 
Media Inc, 2017). Failure to implement automated failure recovery when possible is 
runbook abuse. If certain runbook instructions consist of running commands to view 
particuar metrics, we should display these metrics on our dashboard. 
A company may have a Site Reliability Engineering (SRE) team, which consists of 
engineers who develop tools and processes to ensure high reliability of critical services 
and are often on-call for these critical services. If our service obtains SRE coverage, a 
build of our service may have to satisfy the SRE team’s criteria before it can be deployed. 
This criteria typically consists of high unit test coverage, a functional test suite that 
passes SRE review, and a well-written runbook that has good coverage and description 
of possible problems and has been vetted by the SRE team. 
After the outage is resolved, we should author a postmortem that identifies what 
went wrong, why, and how the team will ensure it does not recur. Postmortems should 
be blameless, or employees may attempt to downplay or hide problems instead of 
addressing them. 
Based on identifying patterns in the actions that are taken to resolve the problem, we 
can identify ways to automate the mitigation of these problems, introducing self-healing characteristics to the system. 
2.5.4	
Application-level logging tools 
The open-source ELK (Elasticsearch, Logstash, Beats, Kibana) suite and the paid-service Splunk are common application-level logging tools. Logstash is used to collect 
and manage logs. Elasticsearch is a search engine, useful for storage, indexing, and 
searching through logs. Kibana is for visualization and dashboarding of logs, using 
Elasticsearch as a data source and for users to search logs. Beats was added in 2015 as a 
light data shipper that ships data to Elasticsearch or Logstash in real time.
In this book, whenever we state that we are logging any event, it is understood that 
we log the event to a common ELK service used for logging by other services in our 
organization. 
There are numerous monitoring tools, which may be proprietary or FOSS (Free and 
open-source software). We will briefly discuss a few of these tools, but an exhaustive list, 
detailed discussion, and comparison are outside the scope of this book. 
These tools differ in characteristics such as
¡ Features. Various tools may offer all or a subset of logging, monitoring, alerting, 
and dashboarding.
¡ Support for various operating systems and other types of equipment besides servers, such as load balancers, switches, modems, routers, or network cards, etc. 
¡ Resource consumption.


38
Chapter 2  A typical system design interview flow
¡ Popularity, which is proportionate to the ease of finding engineers familiar with 
the system.
¡ Developer support, such as the frequency of updates.
They also differ in subjective characteristics like 
¡ Learning curve.
¡ Difficulty of manual configuration and the likelihood of a new user to make 
mistakes. 
¡ Ease of integration with other software and services.
¡ Number and severity of bugs.
¡ UX. Some of the tools have browser or desktop UI clients, and various users may 
prefer the UX of one UI over another. 
FOSS monitoring tools include the following:
¡ Prometheus + Grafana—Prometheus for monitoring, Grafana for visualization and 
dashboarding. 
¡ Sensu—A monitoring system that uses Redis to store data. We can configure 
Sensu to send alerts to a third-party alerting service.
¡ Nagios—A monitoring and alerting system. 
¡ Zabbix—A monitoring system that includes a monitoring dashboard tool.
Proprietary tools include Splunk, Datadog, and New Relic. 
A time series database (TSDB) is a system that is optimized for storing and serving time 
series, such as the continuous writes that happen with logging time series data. Examples include the following. Most queries may be made on recent data, so old data will 
be less valuable, and we can save storage by configuring down sampling on TSDB. This 
rolls up old data by computing averages over defined intervals. Only these averages are 
saved, and the original data is deleted, so less storage is used. The data retention period 
and resolution depend on our requirements and budget. 
To further reduce the cost of storing old data, we can compress it or use a cheap storage medium like tape or optical disks. Refer to https://www.zdnet.com/article/could 
-the-tech-beneath-amazons-glacier-revolutionise-data-storage/ or https://arstechnica 
.com/information-technology/2015/11/to-go-green-facebook-puts-petabytes-of-cat 
-pics-on-ice-and-likes-windfarming/ for examples of custom setups such as hard disk 
storage servers that slow down or stop when not in use:
¡ Graphite—Commonly used to log OS metrics (though it can monitor other setups like websites and applications), which are visualized with the Grafana web 
application. 
¡ Prometheus—Also typically visualized with Grafana. 
¡ OpenTSDB—A distributed, scalable TSDB that uses HBase.
¡ InfluxDB—An open-source TSDB written in Go.


	
39
Logging, monitoring, and alerting
Prometheus is an open-source monitoring system built around a time series database. 
Prometheus pulls from target HTTP endpoints to request metrics, and a Pushgateway 
pushes alerts to Alertmanager, which we can configure to push to various channels 
such as email and PagerDuty. We can use Prometheus query language (PromQL) to 
explore metrics and draw graphs. 
Nagios is a proprietary legacy IT infrastructure monitoring tool that focuses on 
server, network, and application monitoring. It has hundreds of third-party plugins, 
web interfaces, and advanced visualization dashboarding tools. 
2.5.5	
Streaming and batch audit of data quality 
Data quality is an informal term that refers to ensuring that data represents the realworld construct to which it refers and can be used for its intended purposes. For example, if a particular table that is updated by an ETL job is missing some rows that were 
produced by that job, the data quality is poor. 
Database tables can be continuously and/or periodically audited to detect data quality problems. We can implement such auditing by defining streaming and batch ETL 
jobs to validate recently added and modified data. 
This is particularly useful to detect silent errors, which are errors that were undetected by earlier validation checks, such as validation checks that occur during processing of a service request. 
We can extend this concept to a hypothetical shared service for database batch auditing, discussed in chapter 10. 
2.5.6	
Anomaly detection to detect data anomalies 
Anomaly detection is a machine learning concept to detect unusual datapoints. A full 
description of machine-learning concepts is outside the scope of this book. This section briefly describes anomaly detection to detect unusual datapoints. This is useful 
both to ensure data quality and for deriving analytical insights, as an unusual rise or fall 
of a particular metric can indicate problems with data processing or changing market 
conditions. 
In its most basic form, anomaly detection consists of feeding a continuous stream of 
data into an anomaly detection algorithm. After it processes a defined number of datapoints, referred to in machine learning as the training set, the anomaly detection algorithm develops a statistical model. The model’s purpose is to accept a datapoint and 
assign a probability that the datapoint is anomalous. We can validate that this model 
works by using it on a set of datapoints called the validation set, where each datapoint 
has been manually labeled as normal or anomalous. Finally, we can quantify accuracy 
characteristics of the model by testing it on another manually-labeled set, called the test 
set. 
Many parameters are manually tunable, such as which machine-learning models are 
used, the number of datapoints in each of the three sets, and the model’s parameters 
to adjust characteristics, such as precision vs. recall. Machine-learning concepts such as 
precision and recall are outside the scope of this book.


40
Chapter 2  A typical system design interview flow
In practice, this approach to detecting data anomalies is complex and costly to implement, maintain, and use. It is reserved for critical datasets. 
2.5.7	
Silent errors and auditing 
Silent errors may occur due to bugs where an endpoint may return status code 200 
even though errors occurred. We can write batch ETL jobs to audit recent changes to 
our databases and raise alerts on failed audits. Further details are provided in chapter 
10. 
2.5.8	
Further reading on observability
¡ Michael Hausenblas, Cloud Observability in Action, Manning Publications, 2023. A 
guide to applying observability practices to cloud-based serverless and Kubernetes environments.
¡ https://www.manning.com/liveproject/configure-observability. A hands-on course 
in implementing a service template’s observability-related features. 
¡ Mike Julian, Practical Monitoring, O’Reilly Media Inc, 2017. A dedicated book on 
observability best practices, incident response, and antipatterns. 
¡ Boris Scholl, Trent Swanson, and Peter Jausovec. Cloud Native: Using Containers, 
Functions, and Data to build Next-Generation Applications. O’Reilly, 2019. Emphasizes that observability is integral to cloud-native applications. 
¡ John Arundel and Justin Domingus, Cloud Native DevOps with Kubernetes, chapters 
15 and 16, O’Reilly Media Inc, 2019. These chapters discuss observability, monitoring, and metrics in cloud-native applications. 
2.6	
Search bar
Search is a common feature of many applications. Most frontend applications provide 
users with search bars to rapidly find their desired data. The data can be indexed in an 
Elasticsearch cluster. 
2.6.1	
Introduction 
A search bar is a common UI component in many apps. It can be just a single search 
bar or may contain other frontend components for filtering. Figure 2.2 is an example 
of a search bar.
Figure 2.2    Google search bar with drop-down menus for filtering results. Image from Google.


	
41
Search bar
Common techniques of implementing search are: 
1	 Search on a SQL database with the LIKE operator and pattern matching. A query 
may resemble something like SELECT <column> FROM <table> WHERE Lower(<column>) LIKE “%Lower(<search_term>)%”. 
2	 Use a library such as match-sorter (https://github.com/kentcdodds/match 
-sorter), which is a JavaScript library that accepts search terms and does matching 
and sorting on the records. Such a solution needs to be separately implemented 
on each client application. This is a suitable and technically simple solution 
for up to a few GB of text data (i.e., up to millions of records). A web application usually downloads its data from a backend, and this data is unlikely to be 
more than a few megabytes, or the application will not be scalable to millions of 
users. A mobile application may store data locally, so it is theoretically possible to 
have GBs of data, but data synchronization between millions of phones may be 
impractical. 
3	 Use a search engine such as Elasticsearch. This solution is scalable and can handle PBs of data. 
The first technique has numerous limitations and should only be used as a quick temporary implementation that will soon be either discarded or changed to a proper 
search engine. Disadvantages include: 
¡ Difficult to customize the search query. 
¡ No sophisticated features like boosting, weight, fuzzy search, or text preprocessing such as stemming or tokenization. 
This discussion assumes that individual records are small; that is, they are text records, 
not video records. For video records, the indexing and search operations are not 
directly on the video data, but on accompanying text metadata. The implementation 
of indexing and search in search engines is outside the scope of this book. 
We will reference these techniques in the question discussions in part 2, paying much 
more attention to using Elasticsearch. 
2.6.2	
Search bar implementation with Elasticsearch
An organization can have a shared Elasticsearch cluster to serve the search requirements of many of its services. In this section, we first describe a basic Elasticsearch fulltext search query, then the basic steps for adding Elasticsearch to your service given 
an existing Elasticsearch cluster. We will not discuss Elasticsearch cluster setup in this 
book or describe Elasticsearch concepts and terminology in detail. We will use our Beigel app (from chapter 1) for our examples. 
To provide basic full-text search with fuzzy matching, we can attach our search bar 
to a GET endpoint that forwards the query to our Elasticsearch service. An Elasticsearch query is done against an Elasticsearch index (akin to a database in a relational 


42
Chapter 2  A typical system design interview flow
database). If the GET query returns a 2xx response with a list of search results, the frontend loads a results page that displays the list. 
For example, if our Beigel app provides a search bar, and a user searches for the term 
“sesame,” the Elasticsearch request may resemble either of the following. 
The search term may be contained in a query parameter, which allows exact matches 
only: 
GET /beigel-index/_search?q=sesame 
We can also use a JSON request body, which allows us to use the full Elasticsearch DSL, 
which is outside the scope of this book: 
GET /beigel-index/_search 
{ 
  "query": {z6 
    "match": { 
      "query": "sesame", 
      "fuzziness": "AUTO" 
    }  
  } 
}  
"fuzziness": "AUTO" is to allow fuzzy (approximate) matching, which has many use 
cases, such as if the search term or search results contain misspellings. 
The results are returned as a JSON array of hits sorted by decreasing relevance, such 
as the following example. Our backend can pass the results back to the frontend, which 
can parse and present them to the user.
2.6.3	
Elasticsearch index and ingestion
Creating an Elasticsearch index consists of ingesting the documents that should be 
searched when the user submits a search query from a search bar, followed by the 
indexing operation.
We can keep the index updated with periodic or event-triggered indexing or delete 
requests using the Bulk API. 
To change the index’s mapping, one way is to create a new index and drop the old one. 
Another way is to use Elasticsearch’s reindexing operation, but this is expensive because 
the internal Lucene commit operation occurs synchronously after every write request 
(https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules 
-translog.html#index-modules-translog). 
Creating an Elasticsearch index requires all data that you wish to search to be stored 
in the Elasticsearch document store, which increases our overall storage requirements. 
There are various optimizations that involve sending only a subset of data to be indexed. 
Table 2.1 is an approximate mapping between SQL and Elasticsearch terminology. 


	
43
Search bar
Table 2.1    Approximate mapping between SQL and Elasticsearch terminology. There are differences 
between the mapped terms, and this table should not be taken at face value. This mapping is meant for an 
Elasticsearch beginner with SQL experience to use as a starting point for further learning. 
SQL
Elasticsearch
Database
Index
Partition
Shard
Table
Type (deprecated without replacement)
Column
Field
Row
Document
Schema
Mapping
Index
Everything is indexed
2.6.4	
Using Elasticsearch in place of SQL 
Elasticsearch can be used like SQL. Elasticsearch has the concept of query context 
vs. filter context (https://www.elastic.co/guide/en/elasticsearch/reference/current/
query-filter-context.html). From the documentation, in a filter context, a query clause 
answers the question, “Does this document match this query clause?” The answer is a 
simple yes or no; no scores are calculated. In a query context, a query clause answers 
the question, “How well does this document match this query clause?”. The query 
clause determines whether the document matches and calculates a relevance score. 
Essentially, query context is analogous to SQL queries, while filter context is analogous 
to search. 
Using Elasticsearch in place of SQL will allow both searching and querying, eliminate duplicate storage requirements, and eliminate the maintenance overhead of the 
SQL database. I have seen services that use only Elasticsearch for data storage. 
However, Elasticsearch is often used to complement relational databases instead of 
replacing them. It is a schemaless database and does not have the concept of normalization or relations between tables such as primary key and foreign key. Unlike SQL, 
Elasticsearch also does not offer Command Query Responsibility Segregation (refer to 
section 1.4.6) or ACID. 
Moreover, the Elasticsearch Query Language (EQL) is a JSON-based language, and 
it is verbose and presents a learning curve. SQL is familiar to non-developers, such as 
data analysts, and non-technical personnel. Non-technical users can easily learn basic 
SQL within a day. 
Elasticsearch SQL was introduced in June 2018 in the release of Elasticsearch 6.3.0 
(https://www.elastic.co/blog/an-introduction-to-elasticsearch-sql-with-practical 
-examples-part-1 and https://www.elastic.co/what-is/elasticsearch-sql). It supports 
all common filter and aggregation operations (https://www.elastic.co/guide/en/ 
elasticsearch/reference/current/sql-functions.html). This is a promising development. SQL’s dominance is well-established, but in the coming years, it is possible that 
more services will use Elasticsearch for all their data storage as well as search.


44
Chapter 2  A typical system design interview flow
2.6.5	
Implementing search in our services 
Mentioning search during the user stories and functional requirements discussion of 
the interview demonstrates customer focus. Unless the question is to design a search 
engine, it is unlikely that we will describe implementing search beyond creating Elasticsearch indexes, ingesting and indexing, making search queries, and processing results. 
Most of the question discussions of part 2 discuss search in this manner. 
2.6.6	
Further reading on search
Here are more resources on Elasticsearch and indexing:
¡ https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html. 
The official Elasticsearch guide. 
¡ Madhusudhan Konda, Elasticsearch in Action (Second Edition), Manning Publications, 2023. A hands-on guide to developing fully functional search engines with 
Elasticsearch and Kibana. 
¡ https://www.manning.com/livevideo/elasticsearch-7-and-elastic-stack. A course 
on Elasticsearch 7 and Elastic Stack.
¡ https://www.manning.com/liveproject/centralized-logging-in-the-cloud-with 
-elasticsearch-and-kibana. A hands-on course on logging in the cloud with Elasticsearch and Kibana.
¡ https://stackoverflow.com/questions/33858542/how-to-really-reindex-data 
-in-elasticsearch. This is a good alternative to the official Elasticsearch guide 
regarding how to update an Elasticsearch index. 
¡ https://developers.soundcloud.com/blog/how-to-reindex-1-billion-documents 
-in-1-hour-at-soundcloud. A case study of a large reindexing operation. 
2.7	
Other discussions 
When we reach a point in our discussion where our system design satisfies our requirements, we can discuss other topics. This section briefly discusses a few possible topics of 
further discussion. 
2.7.1	
Maintaining and extending the application 
We’ve discussed the requirements at the beginning of the interview and have established a system design for them. We can continue to improve our design to better serve 
our requirements. 
We can also expand the discussion to other possible requirements. Anyone who works 
in the tech industry knows that application development is never complete. There are 
always new and competing requirements. Users submit feedback they want developed 
or changed. We monitor the traffic and request contents of our API endpoints to make 
scaling and development decisions. There is constant discussion on what features to 
develop, maintain, deprecate, and decommission. We can discuss these topics: 


	
45
Other discussions 
¡ Maintenance may already be discussed during the interview. Which system 
components rely on technology (such as software packages), and which are 
developed fastest and require the most maintenance work? How will we handle 
upgrades that introduce breaking changes in any component? 
¡ Features we may need to develop in the future and the system design. 
¡ Features that may not be needed in the future and how to gracefully deprecate 
and decommission them. What is an adequate level of user support to provide 
during this process and how to best provide it? 
2.7.2	
Supporting other types of users 
We can extend the service to support other types of users. If we focused on either consumer or enterprise, manual or programmatic, we may discuss extending the system 
to support the other user categories. We can discuss extending the current services, 
building new services, and the tradeoffs of both approaches. 
2.7.3	
Alternative architectural decisions 
During the earlier part of the interview, we should have discussed alternative architectural decisions. We can revisit them in greater detail. 
2.7.4	
Usability and feedback 
Usability is a measure of how well our users can use our system to effectively and efficiently achieve the desired goals. It is an assessment of how easy our user interface is 
to use. We can define usability metrics, log the required data, and implement a batch 
ETL job to periodically compute these metrics and update a dashboard that displays 
them. Usability metrics can be defined based on how we intend our users to use our 
system. 
For example, if we made a search engine, we want our users to find their desired 
result quickly. One possible metric can be the average index of the result list that a user 
clicks on. We want the results to be ordered in decreasing relevance, and we assume that 
a low average chosen index indicates that a user found their desired result close to the 
top of the list. 
Another example metric is the amount of help users need from our support department when they use our application. It is ideal for our application to be self-service; that 
is, a user can perform their desired tasks entirely within the application without having 
to ask for help. If our application has a help desk, this can be measured by the number 
of help desk tickets created per day or week. A high number of help desk tickets indicates that our application is not self-service. 
Usability can also be measured with user surveys. A common usability survey metric 
is Net Promoter Score (NPS). NPS is defined as the percentage of customers rating their 
likelihood to recommend our application to a friend or colleague as 9 or 10 minus the 
percentage rating this at 6 or below on a scale of 0 to 1,083. 


46
Chapter 2  A typical system design interview flow
We can create UI components within our application for users to submit feedback. 
For example, our web UI may have an HTML link or form for users to email feedback 
and comments. If we do not wish to use email, because of reasons such as possible spam, 
we can create an API endpoint to submit feedback and attach our form submission to it. 
Good logging will aid the reproducibility of bugs by helping us match the user’s feedback with her logged activities. 
2.7.5	
Edge cases and new constraints 
Near the end of the interview, the interviewer may introduce edge cases and new constraints, limited only to the imagination. They may consist of new functional requirements or pushing certain non-functional requirements to the extreme. You may have 
anticipated some of these edge cases during requirements planning. We can discuss if 
we can make tradeoffs to fulfill them or redesign our architecture to support our current requirements as well as these new requirements. Here are some examples. 
¡ New functional requirements: We designed a sales service that supports credit 
card payments. What if our payment system needs to be customizable to support different credit card payment requirements in each country? What if we 
also need to support other payment types like store credit? What if we need to 
support coupon codes? 
¡ We designed a text search service. How may we extend it to images, audio, and 
video? 
¡ We designed a hotel room booking service. What if the user needs to change 
rooms? We’ll need to find an available room for them, perhaps in another hotel. 
¡ What if we decide to add social networking features to our news feed recommendation service? 
Scalability and performance: 
¡ What if a user has one million followers or one million recipients of their messages? Can we accept a long P99 message delivery time? Or do we need to design 
for better performance? 
¡ What if we need to perform an accurate audit of our sales data for the last 10 
years? 
Latency and throughput: 
¡ What if our P99 message delivery time needs to be within 500 ms? 
¡ If we designed a video streaming service that does not accommodate live streaming, how may we modify the design to support live streaming? How may we support simultaneously streaming of a million high-resolution videos across 10 
billion devices? 


	
47
Post-interview reflection and assessment 
Availability and fault-tolerance: 
¡ We designed a cache that didn’t require high availability since all our data is also 
in the database. What if we want high availability, at least for certain data? 
¡ What if our sales service was used for high-frequency trading? How may we 
increase its availability?
¡ How may each component in your system fail? How may we prevent or mitigate 
these failures? 
Cost:
¡ We may have made expensive design decisions to support low latency and high 
performance. What may we trade for lower costs? 
¡ How may we gracefully decommission our service if required? 
¡ Did we consider portability? How may we move our application to the cloud 
(or off the cloud)? What are the tradeoffs in making our application portable? 
(Higher costs and complexity.) Consider MinIO (https://min.io/) for portable 
object storage. 
Every question in part 2 of this book ends with a list of topics for further discussion. 
2.7.6	
Cloud-native concepts 
We may discuss addressing the non-functional requirements via cloud-native concepts 
like microservices, service mesh and sidecar for shared services (Istio), containerization (Docker), orchestration (Kubernetes), automation (Skaffold, Jenkins), and infrastructure as code (Terraform, Helm). A detailed discussion of these topics is outside 
the scope of this book. Interested readers can easily find dedicated books or online 
materials.
2.8	
Post-interview reflection and assessment 
You will improve your interview performance as you go through more interviews. To 
help you learn as much as possible from each interview, you should write a post-interview reflection as soon as possible after each interview. Then you will have the best possible written record of your interview, and you can write your honest critical assessment 
of your interview performance. 
2.8.1	
Write your reflection as soon as possible after the interview 
To help with this process, at the end of an interview, politely ask for permission to take 
photos of your diagrams, but do not persist if permission is denied. Carry a pen and a 
paper notebook with you in your bag. If you cannot take photos, use the earliest possible opportunity to redraw your diagrams from memory into your notebook. Next, 
scribble down as much detail you can recall. 


48
Chapter 2  A typical system design interview flow
You should write your reflection as soon as possible after the interview, when you 
can still remember many details. You may be tired after your interview, but it is counterproductive to relax and possibly forget information valuable to improving your future 
interview performance. Immediately go home or back to your hotel room and write 
your reflection, so you may write it in a comfortable and distraction-free environment. 
Your reflection may have the following outline: 
1	 Header: 
a	 The company and group the interview was for. 
b	 The interview’s date. 
c	 Your interviewer’s name and job title. 
d	 The question that the interviewer asked. 
e	 Were diagrams from your photos or redrawn from memory? 
2	 Divide the interview into approximate 10-minute sections. Place your diagrams 
within the sections when you started drawing them. Your photos may contain 
multiple diagrams, so you may need to split your photos into their separate 
diagrams. 
3	 Fill in the sections with as much detail of the interview as you can recall. 
a	 What you said. 
b	 What you drew. 
c	 What the interviewer said. 
4	 Write your personal assessment and reflections. Your assessments may be imprecise, so you should aim to improve them with practice. 
a	 Try to find the interviewer’s resume or LinkedIn profile. 
b	 Put yourself in the interviewer’s shoes. Why do you think the interviewer chose 
that system design question? What did you think the interviewer expected? 
c	 The interviewer’s expressions and body language. Did the interviewer seem 
satisfied or unsatisfied with your statements and your drawings? Which were 
they? Did the interviewer interrupt or was eager to discuss any statements you 
made? What statements were they? 
5	 In the coming days, if you happen to recall more details, append them to these 
as separate sections, so you do not accidentally introduce inaccuracies into your 
original reflection. 
While you are writing your reflection, ask yourself questions such as the following: 
¡ What questions did the interviewer ask you about your design? 
¡ Did the interviewer question your statements by asking , for example, “Are you 
sure?” 
¡ What did the interviewer not tell you? Do you believe this was done on purpose to 
see if you would mention it, or might the interviewer have lacked this knowledge? 
When you have finished your reflection and recollections, take a well-deserved break. 


	
49
Post-interview reflection and assessment 
2.8.2	
Writing your assessment 
Writing your assessment serves to help you learn as much as possible about your areas 
of proficiency and deficiency that you demonstrated at the interview. Begin writing 
your assessment within a few days of the interview. 
Before you start researching the question that you were asked, first write down any 
additional thoughts on the following. The purpose is for you to be aware of the current 
limit of your knowledge and how polished you are at a system design interview. 
2.8.3	
Details you didn’t mention 
It is impossible to comprehensively discuss a system within 50 minutes. You choose 
which details to mention within that time. Based on your current knowledge (i.e., 
before you begin your research), what other details do you think you could have 
added? Why didn’t you mention them during the interview? 
Did you consciously choose not to discuss them? Why? Did you think those details 
were irrelevant or too low level, or were there other reasons you decided to use the 
interview time to discuss other details? 
Was it due to insufficient time? How could you have managed the interview time better, so you had time to discuss it? 
Were you unfamiliar with the material? Now you are clearly aware of this shortcoming. Study the material so you can describe it better. 
Were you tired? Was it due to lack of sleep? Should you have rested more the day 
before instead of cramming too much? Was it from the interviews before this one? 
Should you have requested a short break before the interview? Perhaps the aroma of a 
cup of coffee on the interview table will improve your alertness. 
Were you nervous? Were you intimidated by the interviewer or other aspects of the 
situation? Look up the numerous online resources on how to keep calm. 
Were you burdened by the weight of expectations of yourself or others? Remember to keep things in perspective. There are numerous good companies. Or you may 
be lucky and enter a company that isn’t prestigious but has excellent business performance in the future so your experience and equity become valuable. You know that you 
are humble and determined to keep learning every day, and no matter what, this will be 
one of many experiences that you are determined to learn as much from as possible to 
improve your performance in the many interviews to come. 
Which details were probably incorrect? This indicates concepts that you are unfamiliar with. Do your research and learn these concepts better? 
Now, you should find resources on the question that was asked. You may search in 
books and online resources such as the following: 
¡ Google 
¡ Websites such as http://highscalability.com/
¡ YouTube videos 


50
Chapter 2  A typical system design interview flow
As emphasized throughout this book, there are many possible approaches to a system 
design question. The materials you find will share similarities and also have numerous 
differences from each other. Compare your reflection to the materials that you found. 
Examine how each of those resources did the following compared to you: 
¡ Clarifying the question. Did you ask intelligent questions? What points did you 
miss? 
¡ Diagrams. Did the materials contain understandable flow charts? Compare the 
high-level architecture diagrams and low-level component design diagrams with 
your own. 
¡ How well does their high-level architecture address the requirements? What 
tradeoffs were made? Do you think the tradeoffs were too costly? What technologies were chosen and why? 
¡ Communication proficiency. 
–	 How much of the material did you understand the first time you read or 
watched it? 
–	 What did you not understand? Was it due to your lack of knowledge, or was 
the presentation unclear? What can be changed so that you will understand it 
the first time? Answering these questions improves your ability to clearly and 
concisely communicate complex and intricate ideas. 
You can always add more material to your assessment at any time in the future. Even 
months after the interview, you may have new insights into all manner of topics, ranging from areas of improvement to alternative approaches you could have suggested, 
and you can add these insights to your assessment then. Extract as much value as possible from your interview experiences. 
You can and should discuss the question with others, but never disclose the company where you were asked this question. Respect the privacy of your interviewers and 
the integrity of the interview process. We are all ethically and professionally obliged 
to maintain a level playing field so companies can hire on merit, and we can work and 
learn from other competent engineers. Industry productivity and compensation will 
benefit from all of us doing our part. 
2.8.4	
Interview feedback 
Ask for interview feedback. You may not receive much feedback if the company has a 
policy of not providing specific feedback, but it never hurts to ask. 
The company may request feedback by email or over the phone. You should provide 
interview feedback if asked. Remind yourself that even though there will be no effect on 
the hiring decision, you can help the interviewers as a fellow engineer. 


	
51
Interviewing the company 
2.9	
Interviewing the company 
In this book, we have been focused on how to handle a system design interview as the 
candidate. This section discusses some questions that you, as the candidate, may wish 
to ask to decide whether this company is where you wish to invest the next few years of 
your finite life. 
The interview process goes both ways. The company wants to understand your experience, expertise, and suitability to fill the role with the best candidate it can find. You 
will spend at least a few years of your life at this company, so you must work with the best 
people and development practices and philosophy that you can find, which will allow 
you to develop your engineering skills as much as possible. 
Here are some ideas to estimate how you can develop your engineering skills. 
Before the interview, read the company’s engineering blog to understand more 
about the following. If there are too many articles, read the top 10 most popular ones 
and those most relevant to your position. For each article about a tool, understand the 
following: 
1	 What is this tool? 
2	 Who uses it? 
3	 What does it do? How does it do these things? How does it do certain things 
similarly or differently from other similar tools? What can it do that other tools 
cannot? How does it do these things? What can’t it do that other tools can? 
Consider writing down at least two questions about each article. Before your interview, 
look through your questions and plan which ones to ask during the interview. 
Some points to understand about the company include the following: 
¡ The company’s technology stack in general. 
¡ The data tools and infrastructure the company uses. 
¡ Which tools were bought, and which were developed? How are these decisions 
made? 
¡ Which tools are open source? 
¡ What other open-source contributions has the company made? 
¡ The history and development of various engineering projects. 
¡ The quantity and breakdown of engineering resources the projects consumed—
the VP and director overseeing the project, and the composition, seniority, 
expertise, and experience of the engineering managers, project managers, and 
engineers (frontend, backend, data engineers and scientists, mobile, security, 
etc.). 
¡ The status of the tools. How well did the tools anticipate and address their users’ 
requirements? What are the best experiences and pain points with the company’s 


52
Chapter 2  A typical system design interview flow
tools, as reflected in frequent feedback? Which ones were abandoned, and why? 
How do these tools stack up to competitors and to the state of the art? 
¡ What has the company or the relevant teams within the company done to address 
these points? 
¡ What are the experiences of engineers with the company’s CI/CD tools? How 
often do engineers run into problems with CI/CD? Are there incidents where 
CI builds succeed but CD deployments fail? How much time do they spend to 
troubleshoot these problems? How many messages were sent to the relevant help 
desk channels in the last month, divided by the number of engineers? 
¡ What projects are planned, and what needs do they fulfill? What is the engineering department’s strategic vision? 
¡ What were the organizational-wide migrations in the last two years? Examples of 
migrations: 
–	 Shift services from bare metal to a cloud vendor or between cloud vendors. 
–	 Stop using certain tools (e.g., a database like Cassandra, a particular monitoring solution). 
¡ Have there been sudden U-turns—for example, migrating from bare metal to 
Google Cloud Platform followed by migrating to AWS just a year later? How 
much were these U-turns motivated by unpredictable versus overlooked or political factors? 
¡ Have there been any security breaches in the history of the company, how serious 
were they, and what is the risk of future breaches? This is a sensitive question, and 
companies will only reveal what is legally required. 
¡ The overall level of the company’s engineering competence. 
¡ The management track record, both in the current and previous roles.
Be especially critical of your prospective manager’s technical background. As an engineer or engineering manager, never accept a non-technical engineering manager, 
especially a charismatic one. An engineering manager who cannot critically evaluate 
engineering work, cannot make good decisions on sweeping changes in engineering 
processes or lead the execution of such changes (e.g., cloud-native processes like moving from manual deployments to continuous deployment), and may prioritize fast 
feature development at the cost of technical debt that they cannot recognize. Such a 
manager has typically been in the same company (or an acquired company) for many 
years, has established a political foothold that enabled them to get their position, and 
is unable to get a similar position in other companies that have competent engineering 
organizations. Large companies that breed the growth of such managers have or are 
about to be disrupted by emerging startups. Working at such companies may be more 
lucrative in the short term than alternatives currently available to you, but they may 
set back your long-term growth as an engineer by years. They may also be financially 
worse for you because companies that you rejected for short-term financial gain end 


	
53
Summary
up performing better in the market, with higher growth in the valuation of your equity. 
Proceed at your own peril. 
Overall, what can I learn and cannot learn from this company in the next four years? 
When you have your offers, you can go over the information you have collected and 
make a thoughtful decision. 
https://blog.pragmaticengineer.com/reverse-interviewing/ is an article on interviewing your prospective manager and team.
Summary
¡ Everything is a tradeoff. Low latency and high availability increase cost and complexity. Every improvement in certain aspects is a regression in others. 
¡ Be mindful of time. Clarify the important points of the discussion and focus on 
them. 
¡ Start the discussion by clarifying the system’s requirements and discuss possible 
tradeoffs in the system’s capabilities to optimize for the requirements.
¡ The next step is to draft the API specification to satisfy the functional 
requirements.
¡ Draw the connections between users and data. What data do users read and write 
to the system, and how is data modified as it moves between system components?
¡ Discuss other concerns like logging, monitoring, alerting, search, and others 
that come up in the discussion.
¡ After the interview, write your self-assessment to evaluate your performance and 
learn your areas of strength and weakness. It is a useful future reference to track 
your improvement. 
¡ Know what you want to achieve in the next few years and interview the company 
to determine if it is where you wish to invest your career.
¡ Logging, monitoring, and alerting are critical to alert us to unexpected events 
quickly and provide useful information to resolve them.
¡ Use the four golden signals and three instruments to quantify your service’s 
observability.
¡ Log entries should be easy to parse, small, useful, categorized, have standardized 
time formats, and contain no private information.
¡ Follow the best practices of responding to alerts, such as runbooks that are useful 
and easy to follow, and continuously refine your runbook and approach based on 
the common patterns you identify.


54
3
Non-functional 
requirements
This chapter covers
¡ Discussing non-functional requirements at the 	
	 start of the interview
¡ Using techniques and technologies to fulfill 	
	 non-functional requirements
¡ Optimizing for non-functional requirements
A system has functional and non-functional requirements. Functional requirements 
describe the inputs and outputs of the system. You can represent them as a rough 
API specification and endpoints.
Non-functional requirements refer to requirements other than the system inputs and 
outputs. Typical non-functional requirements include the following, to be discussed 
in detail later in this chapter.
¡ Scalability—The ability of a system to adjust its hardware resource usage easily 
and with little fuss to cost-efficiently support its load.
¡ Availability—The percentage of time a system can accept requests and return 
the desired response.


	
55
﻿
¡ Performance/latency/P99 and throughput—Performance or latency is the time taken 
for a user’s request to the system to return a response. The maximum request 
rate that a system can process is its bandwidth. Throughput is the current request 
rate being processed by the system. However, it is common (though incorrect) to 
use the term “throughput” in place of “bandwidth.” Throughput/bandwidth is 
the inverse of latency. A system with low latency has high throughput.
¡ Fault-tolerance—The ability of a system to continue operating if some of its components fail and the prevention of permanent harm (such as data loss) should 
downtime occur.
¡ Security—Prevention of unauthorized access to systems. 
¡ Privacy—Access control to Personally Identifiable Information (PII), which can 
be used to uniquely identify a person.
¡ Accuracy—A system’s data may not need to be perfectly accurate, and accuracy 
tradeoffs to improve costs or complexity are often a relevant discussion. 
¡ Consistency—Whether data in all nodes/machines match.
¡ Cost—We can lower costs by making tradeoffs against other non-functional properties of the system.
¡ Complexity, maintainability, debuggability, and testability—These are related concepts that determine how difficult it is to build a system and then maintain it after 
it is built.
A customer, whether technical or non-technical, may not explicitly request non-functional requirements and may assume that the system will satisfy them. This means that 
the customer’s stated requirements will almost always be incomplete, incorrect, and 
sometimes excessive. Without clarification, there will be misunderstandings on the 
requirements. We may not obtain certain requirements and therefore inadequately 
satisfy them, or we may assume certain requirements, which are actually not required 
and provide an excessive solution. 
A beginner is more likely to fail to clarify non-functional requirements, but a lack of 
clarification can occur for both functional and non-functional requirements. We must 
begin any systems design discussion with discussion and clarification of both the functional and non-functional requirements. 
Non-functional requirements are commonly traded off against each other. In any 
system design interview, we must discuss how various design decisions can be made for 
various tradeoffs. 
It is tricky to separately discuss non-functional requirements and techniques to 
address them because certain techniques have tradeoff gains on multiple non-functional requirements for losses on others. In the rest of this chapter, we briefly discuss 
each non-functional requirement and some techniques to fulfill it, followed by a 
detailed discussion of each technique. 


56
Chapter 3  Non-functional requirements
3.1	
Scalability
Scalability is the ability of a system to adjust its hardware resource usage easily and with 
little fuss to cost-efficiently support its load. 
The process of expanding to support a larger load or number of users is called scaling. Scaling requires increases in CPU processing power, RAM, storage capacity, and 
network bandwidth. Scaling can refer to vertical scaling or horizontal scaling. 
Vertical scaling is conceptually straightforward and can be easily achieved just by 
spending more money. It means upgrading to a more powerful and expensive host, one 
with a faster processor, more RAM, a bigger hard disk drive, a solid-state drive instead of 
a spinning hard disk for lower latency, or a network card with higher bandwidth. There 
are three main disadvantages of vertical scaling. 
First, we will reach a point where monetary cost increases faster than the upgraded 
hardware’s performance. For example, a custom mainframe that has multiple processors will cost more than the same number of separate commodity machines that have 
one processor each. 
Second, vertical scaling has technological limits. Regardless of budget, current technological limitations will impose a maximum amount of processing power, RAM, or 
storage capacity that is technologically possible on a single host.  
Third, vertical scaling may require downtime. We must stop our host, change its 
hardware and then start it again. To avoid downtime, we need to provision another 
host, start our service on it, and then direct requests to the new host. Moreover, this is 
only possible if the service’s state is stored on a different machine from the old or new 
host. As we discuss later in this book, directing requests to specific hosts or storing a service’s state in a different host are techniques to achieve many non-functional requirements, such as scalability, availability, and fault-tolerance. 
Because vertical scaling is conceptually trivial, in this book unless otherwise stated, 
our use of terms like “scalable” and “scaling” refer to horizontally scalable and horizontal scaling. 
Horizontal scaling refers to spreading out the processing and storage requirements 
across multiple hosts. “True” scalability can only be achieved by horizontal scaling. Horizontal scaling is almost always discussed in a system design interview.
Based on these questions, we determine the customer’s scalability requirements. 
¡ How much data comes to the system and is retrieved from the system? 
¡ How many read queries per second? 
¡ How much data per request? 
¡ How many video views per second? 
¡ How big are sudden traffic spikes?


	
57
Scalability
3.1.1	
Stateless and stateful services
HTTP is a stateless protocol, so a backend service that uses it is easy to scale horizontally. Chapter 4 describes horizontal scaling of database reads. A stateless HTTP backend combined with horizontally scalable database read operations is a good starting 
point to discuss a scalable system design. 
Writes to shared storage are the most difficult to scale. We discuss techniques, including replication, compression, aggregation, denormalization, and Metadata Service 
later in this book.
Refer to section 6.7 for a discussion of various common communication architectures, including the tradeoffs between stateful and stateless.
3.1.2	
Basic load balancer concepts
Every horizontally scaled service uses a load balancer, which may be one of the 
following:
¡ A hardware load balancer, a specialized physical device that distributes traffic 
across multiple hosts. Hardware load balancers are known for being expensive 
and can cost anywhere from a few thousand to a few hundred thousand dollars.
¡ A shared load balancer service, also referred to as LBaaS (load balancing as a 
service). 
¡ A server with load balancing software installed. HAProxy and NGINX are the 
most common.
This section discusses basic concepts of load balancers that we can use in an interview.
In the system diagrams in this book, I draw rectangles to represent various services or 
other components and arrows between them to represent requests. It is usually understood that requests to a service go through a load balancer and are routed to a service’s 
hosts. We usually do not illustrate the load balancers themselves.
We can tell the interviewer that we need not include a load balancer component 
in our system diagrams, as it is implied, and drawing it and discussing it on our system 
diagrams is a distraction from the other components and services that compose our 
service. 
Level 4 vs. level 7
We should be able to distinguish between level 4 and level 7 load balancers and discuss 
which one is more suitable for any particular service. A level 4 load balancer operates 
at the transport layer (TCP). It makes routing decisions based on address information 
extracted from the first few packets in the TCP stream and does not inspect the contents of other packets; it can only forward the packets. A level 7 load balancer operates 
at the application layer (HTTP), so it has these capabilities:
¡ Load balancing/routing decisions—Based on a packet’s contents.
¡ Authentication—It can return 401 if a specified authentication header is absent.


58
Chapter 3  Non-functional requirements
¡ TLS termination—Security requirements for traffic within a data center may be 
lower than traffic over the internet, so performing TLS termination (HTTPS ‹ 
HTTP) means there is no encryption/decryption overhead between data center 
hosts. If our application requires traffic within our data center to be encrypted 
(i.e., encryption in transit), we will not do TLS termination. 
Sticky sessions
A sticky session refers to a load balancer sending requests from a particular client to 
a particular host for a duration set by the load balancer or the application. Sticky sessions are used for stateful services. For example, an ecommerce website, social media 
website, or banking website may use sticky sessions to maintain user session data like 
login information or profile preferences, so a user doesn’t have to reauthenticate or 
reenter preferences as they navigate the site. An ecommerce website may use sticky 
sessions for a user’s shopping cart.
A sticky session can be implemented using duration-based or application-controlled 
cookies. In a duration-based session, the load balancer issues a cookie to a client that 
defines a duration. Each time the load balancer receives a request, it checks the cookie. 
In an application-controlled session, the application generates the cookie. The load 
balancer still issues its own cookie on top of this application-issued cookie, but the load 
balancer’s cookie follows the application cookie’s lifetime. This approach ensures clients are not routed to another host after the load balancer’s cookie expires, but it is 
more complex to implement because it requires additional integration between the 
application and the load balancer.
Session replication
In session replication, writes to a host are copied to several other hosts in the cluster that 
are assigned to the same session, so reads can be routed to any host with that session. 
This improves availability.
These hosts may form a backup ring. For example, if there are three hosts in a session, when host A receives a write, it writes to host B, which in turn writes to host C. 
Another way is for the load balancer to make write requests to all the hosts assigned to 
a session. 
Load balancing vs. reverse proxy
You may come across the term “reverse proxy” in other system design interview preparation materials. We will briefly compare load balancing and reverse proxy.
Load balancing is for scalability, while reverse proxy is a technique to manage ­client–
server communication. A reverse proxy sits in front of a cluster of servers and acts as a 
gateway between clients and servers by intercepting and forwarding incoming requests 
to the appropriate server based on request URI or other criteria. A reverse proxy may 
also provide performance features, such as caching and compression, and security features, such as SSL termination. Load balancers can also provide SSL termination, but 
their main purpose is scalability.


	
59
Availability
Refer to https://www.nginx.com/resources/glossary/reverse-proxy-vs-load-balancer/ 
for a good discussion on load balancing versus reverse proxy.
Further reading
¡ https://www.cloudflare.com/learning/performance/types-of-load-balancing 
-algorithms/ is a good brief description of various load balancing algorithms.
¡ https://rancher.com/load-balancing-in-kubernetes is a good introduction to 
load balancing in Kubernetes.
¡ https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer 
and https://kubernetes.io/docs/tasks/access-application-cluster/create-external 
-load-balancer/ describe how to attach an external cloud service load balancer to 
a Kubernetes service.
3.2	
Availability
Availability is the percentage of time a system can accept requests and return the 
desired response. Common benchmarks for availability are shown in table 3.1. 
Table 3.1    Common benchmarks for availability 
Availability %
Downtime  
per year
Downtime  
per month
Downtime  
per week
Downtime  
per day
99.9 (three 9s)
8.77 hours
43.8 minutes
10.1 minutes
1.44 minutes
99.99 (four 9s)
52.6 minutes
4.38 minutes
1.01 minutes
8.64 seconds
99.999 (five 9s)
5.26 minutes
26.3 seconds
6.05 seconds
864 milliseconds
Refer to https://netflixtechblog.com/active-active-for-multi-regional-resiliency 
-c47719f6685b for a detailed discussion on Netflix’s multi-region active-active deployment for high availability. In this book, we discuss similar techniques for high availability, such as replication within and across data centers in different continents. We also 
discuss monitoring and alerting. 
High availability is required in most services, and other non-functional requirements 
may be traded off to allow high availability without unnecessary complexity. 
When discussing the non-functional requirements of a system, first establish whether 
high availability is required. Do not assume that strong consistency and low latency are 
required. Refer to the CAP theorem and discuss if we can trade them off for higher 
availability. As far as possible, suggest using asynchronous communication techniques 
that accomplish this, such as event sourcing and saga, discussed in chapters 4 and 5. 
Services where requests do not need to be immediately processed and responses 
immediately returned are unlikely to require strong consistency and low latency, such as 
requests made programmatically between services. Examples include logging to longterm storage or sending a request in Airbnb to book a room for some days from now. 
Use synchronous communication protocols when an immediate response is absolutely necessary, typically for requests made directly by people using your app. 


60
Chapter 3  Non-functional requirements
Nonetheless, do not assume that requests made by people need immediate responses 
with the requested data. Consider whether the immediate response can be an acknowledgment and whether the requested data can be returned minutes or hours later. For 
example, if a user requests to submit their income tax payment, this payment need not 
happen immediately. The service can queue the request internally and immediately 
respond to the user that the request will be processed in minutes or hours. The payment can later be processed by a streaming job or a periodic batch job, and then the 
user can be notified of the result (such as whether the payment succeeded or failed) 
through channels such as email, text, or app notifications. 
An example of a situation where high availability may not be required is in a caching 
service. Because caching may be used to reduce the latency and network traffic of a 
request and is not needed to fulfill the request, we may decide to trade off availability 
for lower latency in the caching service’s system design. Another example is rate limiting, discussed in chapter 8.
Availability can also be measured with incident metrics. https://www.atlassian.com/
incident-management/kpis/common-metrics describes various incident metrics like 
MTTR (Mean Time to Recovery) and MTBF (Mean Time Between Failures). These 
metrics usually have dashboards and alerts.
3.3	
Fault-tolerance
Fault-tolerance is the ability of a system to continue operating if some of its components fail and the prevention of permanent harm (such as data loss) should downtime 
occur. This allows graceful degradation, so our system can maintain some functionality 
when parts of it fail, rather than a complete catastrophic failure. This buys engineers 
time to fix the failed sections and restore the system to working order. We may also 
implement self-healing mechanisms that automatically provision replacement components and attach them to our system, so our system can recover without manual intervention and without any noticeable effect on end users. 
Availability and fault-tolerance are often discussed together. While availability is a 
measure of uptime/downtime, fault-tolerance is not a measure but rather a system 
characteristic. 
A closely related concept is failure design, which is about smooth error handling. 
Consider how we will handle errors in third-party APIs that are outside our control as 
well as silent/undetected errors. Techniques for fault-tolerance include the following. 
3.3.1	
Replication and redundancy 
Replication is discussed in chapter 4. 
One replication technique is to have multiple (such as three) redundant instances/
copies of a component, so up to two can be simultaneously down without affecting 
uptime. As discussed in chapter 4, update operations are usually assigned a particular 
host, so update performance is affected only if the other hosts are on different data 
centers geographically further away from the requester, but reads are often done on all 
replicas, so read performance decreases when components are down. 


	
61
Fault-tolerance
One instance is designated as the source of truth (often called the leader), while 
the other two components are designated as replicas (or followers). There are various possible arrangements of the replicas. One replica is on a different server rack 
within the same data center, and another replica is in a different data center. Another 
arrangement is to have all three instances on different data centers, which maximizes 
­fault-tolerance with the tradeoff of lower performance. 
An example is the Hadoop Distributed File System (HDFS), which has a configurable property called “replication factor” to set the number of copies of any block. The 
default value is three. Replication also helps to increase availability. 
3.3.2	
Forward error correction and error correction code 
Forward error correction (FEC) is a technique to prevent errors in data transmission over 
noise or unreliable communication channels by encoding the message in a redundant 
way, such as by using an error correction code (ECC). 
FEC is a protocol-level rather than a system-level concept. We can express our awareness of FEC and ECC during system design interviews, but it is unlikely that we will need 
to explain it in detail, so we do not discuss them further in this book.
3.3.3	
Circuit breaker 
The circuit breaker is a mechanism that stops a client from repeatedly attempting an 
operation that is likely to fail. With respect to downstream services, a circuit breaker 
calculates the number of requests that failed within a recent interval. If an error threshold is exceeded, the client stops calling downstream services. Sometime later, the client 
attempts a limited number of requests. If they are successful, the client assumes that 
the failure is resolved and resumes sending requests without restrictions. 
DEFINITION    If a service B depends on a service A, A is the upstream service and B 
is the downstream service.
A circuit breaker saves resources from being spent to make requests that are likely to fail. 
It also prevents clients from adding additional burden to an already overburdened system. 
However, a circuit breaker makes the system more difficult to test. For example, say 
we have a load test that is making incorrect requests but is still properly testing our 
system’s limits. This test will now activate the circuit breaker, and a load that may have 
previously overwhelmed the downstream services and will now pass. A similar load by 
our customers will cause an outage. It is also difficult to estimate the appropriate error 
threshold and timers. 
A circuit breaker can be implemented on the server side. An example is Resilience4j (https://github.com/resilience4j/resilience4j). It was inspired by Hystrix 
(https://github.com/Netflix/Hystrix), which was developed at Netflix and transi­
tioned to maintenance mode in 2017 (https://github.com/Netflix/Hystrix/issues/ 
1876#issuecomment-440065505). Netflix’s focus has shifted toward more adaptive 
implementations that react to an application’s real-time performance rather than 
pre-configured settings, such as adaptive concurrency limits (https://netflixtechblog 
.medium.com/performance-under-load-3e6fa9a60581).


62
Chapter 3  Non-functional requirements
3.3.4	
Exponential backoff and retry 
Exponential backoff and retry is similar to a circuit breaker. When a client receives an 
error response, it will wait before reattempting the request and exponentially increase 
the wait duration between retries. The client also adjusts the wait period by a small random negative or positive amount, a technique called “jitter.” This prevents multiple clients from submitting retries at exactly the same time, causing a “retry storm” that may 
overwhelm the downstream service. Similar to a circuit breaker, when a client receives 
a success response, it assumes that the failure is resolved and resumes sending requests 
without restrictions.
3.3.5	
Caching responses of other services
Our service may depend on external services for certain data. How should we handle 
the case where an external service is unavailable? It is generally preferable to have 
graceful degradation instead of crashing or returning an error. We can use a default or 
empty response in place of the return value. If using stale data is better than no data, 
we can cache the external service’s responses whenever we make successful requests 
and use these responses when the external service is unavailable.
3.3.6	
Checkpointing 
A machine may perform certain data aggregation operations on many data points by 
systematically fetching a subset of them, performing the aggregation on them, then 
writing the result to a specified location, repeating this process until all data points are 
processed or infinitely, such as in the case of a streaming pipeline. Should this machine 
fail during data aggregation, the replacement machine should know from which data 
points to resume the aggregation. This can be done by writing a checkpoint after each 
subset of data points are processed and the result is successfully written. The replacement machine can resume processing at the checkpoint. 
Checkpointing is commonly applied to ETL pipelines that use message brokers such 
as Kafka. A machine can fetch several events from a Kafka topic, process the events, 
and then write the result, followed by writing a checkpoint. Should this machine fail, its 
replacement can resume at the most recent checkpoint. 
Kafka offers offset storages at the partition level in Kafka (https://kafka.apache 
.org/22/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html). Flink 
consumes data from Kafka topics and periodically checkpoints using Flink’s distributed 
checkpointing mechanism (https://ci.apache.org/projects/flink/flink-docs-master/
docs/dev/datastream/fault-tolerance/checkpointing/). 
3.3.7	
Dead letter queue 
If a write request to a third-party API fails, we can queue the request in a dead letter 
queue and try the requests again later. 
Are dead letter queues stored locally or on a separate service? We can trade off complexity and reliability: 


	
63
Fault-tolerance
¡ The simplest option is that if it is acceptable to miss requests, just drop failed 
requests.  
¡ Implement the dead letter queue locally with a try-catch block. Requests will be 
lost if the host fails. 
¡ A more complex and reliable option is to use an event-streaming platform like 
Kafka.  
In an interview, you should discuss multiple approaches and their tradeoffs. Don’t just 
state one approach. 
3.3.8	
Logging and periodic auditing 
One method to handle silent errors is to log our write requests and perform periodic 
auditing. An auditing job can process the logs and verify that the data on the service we 
write to matches the expected values. This is discussed further in chapter 10. 
3.3.9	
Bulkhead 
The bulkhead pattern is a fault-tolerance mechanism where a system is divided into 
isolated pools, so a fault in one pool will not affect the entire system. 
For example, the various endpoints of a service can each have their own thread pool, 
and not share a thread pool, so if an endpoint’s thread pool is exhausted, this will not 
affect the ability of other endpoints to serve requests (To learn more about this, see 
Microservices for the Enterprise: Designing, Developing, and Deploying by Indrasiri and Siriwardena (Apress, 2019).
Another example of bulkhead is discussed in Release It!: Design and Deploy Production-Ready Software, Second Edition by Michael T. Nygard’s (Pragmatic Bookshelf, 2018). 
A certain request may cause a host to crash due to a bug. Each time this request is 
repeated, it will crash another host. Dividing the service into bulkheads (i.e., dividing 
the hosts into pools) prevents this request from crashing all the hosts and causing a 
total outage. This request should be investigated, so the service must have logging and 
monitoring. Monitoring will detect the offending request, and engineers can use the 
logs to troubleshoot the crash and determine its cause. 
Or a requestor may have a high request rate to a service and prevent the latter from 
serving other requestors. The bulkhead pattern allocates certain hosts to a particular 
requestor, preventing the latter from consuming all the service’s capacity. (Rate limiting discussed in chapter 8 is another way to prevent this situation.) 
A service’s hosts can be divided into pools, and each pool is allocated requestors. 
This is also a technique to prioritize certain requestors by allocating more resources to 
them.
In figure 3.1, a service serves two other services. Unavailability of the service’s hosts 
will prevent it from serving any requestor. 


64
Chapter 3  Non-functional requirements
Service 1
Service 2
Service 0
Figure 3.1    All requests to service 
0 are load-balanced across its 
hosts. The unavailability of service 
0’s hosts will prevent it from 
serving any requestor.  
In figure 3.2, a service’s hosts are divided into pools, which are allocated to requestors. 
The unavailability of the hosts of one pool will not affect other requestors. An obvious 
tradeoff of this approach is that the pools cannot support each other if there are traffic 
spikes from certain requestors. This is a deliberate decision that we made to allocate a 
certain number of hosts to a particular requestor. We can either manually or automatically scale the pools as required. 
Service 1
Service 2
Service 0
pool 0
Service 0
pool 1
Service 0
Figure 3.2    Service 0 is divided 
into two pools, each allocated to 
a requestor. The unavailability of 
one pool will not affect the other. 
Refer to Michael Nygard’s book Release It!: Design and Deploy Production-Ready Software, 
Second Edition (Pragmatic Bookshelf, 2018), for other examples of the bulkhead 
pattern. 
We will not mention bulkhead in the system design discussions of part 2, but it is generally applicable for most systems, and you can discuss it during an interview. 
3.3.10	 Fallback pattern
The fallback pattern consists of detecting a problem and then executing an alternative 
code path, such as cached responses or alternative services that are similar to the service 
the client is trying to get information from. For example, if a client requests our backend for a list of nearby bagel cafes, it can cache the response to be used in the future if 
our backend service is experiencing an outage. This cached response may not be up to 
date, but it is better than returning an error message to the user. An alternative is for 
the client to make a request to a third-party maps API like Bing or Google Maps, which 
may not have the customized content that our backend provides. When we design a 
fallback, we should consider its reliability and that the fallback itself may fail. 


	
65
Performance/latency and throughput
NOTE    Refer to https://aws.amazon.com/builders-library/avoiding-fallback-in 
-distributed-systems/ for more information on fallback strategies, why Amazon 
almost never uses the fallback pattern, and alternatives to the fallback pattern 
that Amazon uses.
3.4	
Performance/latency and throughput
Performance or latency is the time taken for a user’s request to the system to return a 
response. This includes the network latency of the request to leave the client and travel 
to the service, the time the service takes to process the request and create the response, 
and the network latency of the response to leave the service and travel to the client. A 
typical request on a consumer-facing app (e.g., viewing a restaurant’s menu on a food 
delivery app or submitting a payment on an ecommerce app) has a desired latency 
of tens of milliseconds to several seconds. High-frequency trading applications may 
demand latency of several milliseconds. 
Strictly speaking, latency refers to the travel time of a packet from its source to its 
destination. However, the term “latency” has become commonly used to have the same 
meaning as “performance,” and both terms are often used interchangeably. We still use 
the term latency if we need to discuss packet travel time. 
The term latency can also be used to describe the request-response time between 
components within the system, rather than the user’s request-response time. For example, if a backend host makes a request to a logging or storage system to store data, the 
system’s latency is the time required to log/store the data and return a response to the 
backend host.
The system’s functional requirements may mean that a response may not actually 
need to contain the information requested by the user but may simply be an acknowledgment along with a promise that after a specified duration, the requested information will be sent to the user or will be available for the user to obtain by making another 
request. Such a tradeoff may simplify the system’s design, so we must always clarify 
requirements and discuss how soon information is required after a user’s request. 
Typical design decisions to achieve low latency include the following. We can deploy 
the service in a data center geographically close to its users, so packets between users 
and our service do not need to travel far. If our users are geographically dispersed, we 
may deploy our service in multiple data centers that are chosen to minimize geographical distance to clusters of users. If hosts across data centers need to share data, our service must be horizontally scalable. 
Occasionally, there may be other factors that contribute more to latency than the 
physical distance between users and data centers, such as traffic or network bandwidth, 
or the backend system processing (the actual business logic and the persistence layer). 
We can use test requests between users and various data centers to determine the data 
center with the lowest latency for users in a particular location. 
Other techniques include using a CDN, caching, decreasing the data size with RPC 
instead of REST, designing your own protocol with a framework like Netty to use TCP 
and UDP instead of HTTP, and using batch and streaming techniques.   


66
Chapter 3  Non-functional requirements
In examining latency and throughput, we discuss the characteristics of the data and 
how it gets in and out of the system, and then we can suggest strategies. Can we count 
views several hours after they happened? This will allow batch or streaming approaches. 
What is the response time? If small, data must already be aggregated, and aggregation 
should be done during writes, with minimal or no aggregation during reads.
3.5	
Consistency
Consistency has different meanings in ACID and CAP (from the CAP theorem). ACID 
consistency focuses on data relationships like foreign keys and uniqueness. As stated 
in Martin Kleppmann’s Designing Data-Intensive Applications (O’Reilly, 2017), CAP consistency is actually linearizability, defined as all nodes containing the same data at a 
moment in time, and changes in data must be linear; that is, nodes must start serving 
the changes at the same time.  
Eventually, consistent databases trade off consistency for improvements in availability, scalability, and latency. An ACID database, including RDBMS databases, cannot 
accept writes when it experiences a network partition because it cannot maintain ACID 
consistency if writes occur during a network partition. Summarized in table 3.2, MongoDB, HBase, and Redis trade off availability for linearizability, while CouchDB, Cassandra, Dynamo, Hadoop, and Riak trade off linearizability for availability.
Table 3.2    Databases that favor availability vs. linearizability 
Favor linearizability
Favor availability
HBase 
MongoDB
Redis
Cassandra 
CouchDB 
Dynamo 
Hadoop 
Riak
During the discussion, we should emphasize the distinction between ACID and CAP 
consistency, and the tradeoffs between linearizability vs. eventual consistency. In this 
book, we will discuss various techniques for linearizability and eventual consistency, 
including the following: 
¡ Full mesh
¡ Quorum 
Techniques for eventual consistency that involve writing to a single location, which 
propagates this write to the other relevant locations: 
¡ Event sourcing (section 5.2), a technique to handle traffic spikes. 
¡ Coordination service. 
¡ Distributed cache. 


	
67
Consistency
Techniques for eventual consistency that trade off consistency and accuracy for lower 
cost: 
¡ Gossip protocol. 
¡ Random leader selection. 
Disadvantages of linearizability include the following: 
¡ Lower availability, since most or all nodes must be sure of consensus before they 
can serve requests. This becomes more difficult with a larger number of nodes. 
¡ More complex and expensive. 
3.5.1	
Full mesh 
Figure 3.3 illustrates an example of full mesh. Every host in the cluster has the address 
of every other host and broadcasts messages to all of them.
Figure 3.3    
Illustration of full 
mesh. Every host 
is connected to 
every other host 
and broadcasts 
messages to all of 
them. 
How do hosts discover each other? When a new host is added, how is its address sent to 
other hosts? Solutions for host discovery include: 
¡ Maintain the list of addresses in a configuration file. Each time the list changes, 
deploy this file across all hosts/nodes. 
¡ Use a third-party service that listens for heartbeats from every host. A host is kept 
registered as long as the service receives heartbeats. All hosts use this service to 
obtain the full list of addresses. 
Full mesh is easier to implement than other techniques, but it is not scalable. The number of messages grows quadratically with the number of hosts. Full mesh works well 
for small clusters but cannot support big clusters. In quorum, only a majority of hosts 
need to have the same data for the system to be considered consistent. BitTorrent is an 
example of a protocol that uses full mesh for decentralized p2p file sharing. During an 
interview, we can briefly mention full mesh and compare it with scalable approaches. 


68
Chapter 3  Non-functional requirements
3.5.2	
Coordination service
Figure 3.4 illustrates a coordination service, a third-party component that chooses a 
leader node or set of leader nodes. Having a leader decreases the number of messages. 
All other nodes send their messages to the leader, and the leader may do some necessary processing and send back the final result. Each node only needs to communicate 
with its leader or set of leaders, and each leader manages a number of nodes. 
Coordination Service
Figure 3.4 
Illustration of 
a coordination 
service 
Example algorithms are Paxos, Raft, and Zab. Another example is single leader multiple follower in SQL (section 4.3.2), a technique to allow scalable reads. ZooKeeper 
(https://zookeeper.apache.org/) is a distributed coordination service. ZooKeeper 
has the following advantages over a config file stored on a single host. (Most of these 
advantages are discussed at https://stackoverflow.com/q/36312640/1045085.) We 
can implement these features on a distributed filesystem or distributed database, but 
ZooKeeper already provides them: 
¡ Access control (https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers 
.html#sc_ZooKeeperAccessControl). 
¡ Storing data in memory for high performance. 
¡ Scalability, with horizontal scaling by adding hosts to the ZooKeeper Ensemble 
(https://zookeeper.apache.org/doc/r3.1.2/zookeeperAdmin.html#sc_zkMulit 
ServerSetup). 
¡ Guaranteed eventual consistency within a specified time bound or strong consistency with higher cost (https://zookeeper.apache.org/doc/current/zookeeper 
Internals.html#sc_consistency). ZooKeeper trades off availability for consistency; 
it is a CP system in the CAP theorem. 
¡ Clients can read data in the order it is written.
Complexity is the main disadvantage of a coordination service. A coordination service 
is a sophisticated component that has to be highly reliable and ensure one and only 
one leader is elected. (The situation where two nodes both believe they are the leader 
is called “split brain.” Refer to Martin Kleppmann, Designing Data-Intensive Applications, 
O’Reilly, 2017, p. 158.) 


	
69
Consistency
3.5.3	
Distributed cache 
We can use a distributed cache like Redis or Memcached. Referring to figure 3.5, our 
service’s nodes can make periodic requests to the origin to fetch new data, then make 
requests to the distributed cache (e.g., an in-memory store like Redis) to update its 
data. This solution is simple, has low latency, and the distributed cache cluster can be 
scaled independently of our service. However, this solution has more requests than 
every other solution here except the full mesh. 
Figure 3.5    Illustration of using 
a distributed cache to broadcast 
messages. The nodes can make 
requests to an in-memory store like 
Redis to update data, or it can make 
periodic requests to fetch new data. 
NOTE    Redis is an in-memory cache, not a typically distributed one by definition. It 
is used as a distributed cache for practical intents and purposes. Refer to https://
redis.io/docs/about/ and https://stacoverflow.com/questions/18376665/redis 
-distributed-or-not. 
Both a sender and receiver host can validate that a message contains its required fields. 
This is often done by both sides because the additional cost is trivial while reducing the 
possibility of errors on either side, resulting in an invalid message. When a sender host 
sends an invalid message to a receiver host via an HTTP request, and the receiver host 
can detect that this message is invalid, it can immediately return a 400 or 422. We can 
set up high-urgency alerts to trigger on 4xx errors, so we will immediately be alerted 
of this error and can immediately investigate. However, if we use Redis, invalid data 
written by a node may stay undetected until it is fetched by another node, so there will 
be a delay in alerts. 
Requests sent directly from one host to another go through schema validation. 
However, Redis is just a database, so it does not validate schema, and hosts can write 
arbitrary data to it. This may create security problems. (Refer to https://www 
.trendmicro.com/en_us/research/20/d/exposed-redis-instances-abused-for-remote 
-code-execution-cryptocurrency-mining.html and https://www.imperva.com/blog/
new-research-shows-75-of-open-redis-servers-infected.) Redis is designed to be accessed 
by trusted clients inside trusted environments (https://redis.io/topics/security). Redis 
does not support encryption, which may be a privacy concern. Implementing encryption at rest increases complexity, costs, and reduces performance (https://docs.aws 
.amazon.com/AmazonElastiCache/latest/red-ug/at-rest-encryption.html). 
A coordination service addresses these disadvantages but has higher complexity and 
cost. 


70
Chapter 3  Non-functional requirements
3.5.4	
Gossip protocol 
Gossip protocol is modeled after how epidemics spread. Referring to figure 3.6, each 
node randomly selects another node periodically or with a random interval and then 
shares data. This approach trades off consistency for lower cost and complexity. 
Figure 3.6    
Illustration 
of gossip 
communication 
Cassandra uses a gossip protocol to maintain consistency across distributed data partitions. DynamoDB uses a gossip protocol called “vector clocks” to maintain consistency 
across multiple data centers.
3.5.5	
Random Leader Selection 
Referring to figure 3.7, random leader selection uses a simple algorithm to elect a 
leader. This simple algorithm does not guarantee one and only one leader, so there 
may be multiple leaders. This is a minor problem because each leader can share data 
with all other hosts, so all hosts, including all leaders, will have the correct data. The 
disadvantage is possible duplicate requests and unnecessary network traffic.
Leader
Leader
Figure 3.7    
Illustration of 
multiple leaders, 
which can result 
from random leader 
selection 
Kafka uses a leader-follower replication model with random leader selection to provide 
fault-tolerance. YARN uses a random leader selection approach to manage resource 
allocation across a cluster of hosts. 
3.6	
Accuracy
Accuracy is a relevant non-functional requirement in systems with complex data processing or a high rate of writes. Accuracy of data means that the data values are correct and are not approximations. Estimation algorithms trade off accuracy for lower 
complexity. Examples of estimation algorithms include HyperLogLog for cardinality 


	
71
Complexity and maintainability
(COUNT DISTINCT) estimate in the Presto distributed SQL query engine and countmin sketch for estimating frequencies of events in a stream of data. 
A cache is stale if the data in its underlying database has been modified. A cache 
may have a refresh policy where it will fetch the latest data at a fixed periodic interval. 
A short refresh policy is more costly. An alternative is for the system to update or delete 
the associated cache key when data is modified, which increases complexity. 
Accuracy is somewhat related to consistency. Systems that are eventually consistent 
trade off accuracy for improvements in availability, complexity, and cost. When a write 
is made to an eventually consistent system, results from reads made after this write 
may not include the effects of the write, which makes them inaccurate. The eventually 
consistent system is inaccurate until the replicas are updated with the effects of the 
write operation. However, we use the term “consistency” to discuss such a situation, not 
“accuracy.”
3.7	
Complexity and maintainability
The first step to minimize complexity is to clarify both functional and non-functional 
requirements, so we do not design for unnecessary requirements. 
As we sketch design diagrams, note which components may be separated into independent systems. Use common services to reduce complexity and improve maintainability. Common services that are generalizable across virtually all services include 
¡ Load balancer service.
¡ Rate limiting. Refer to chapter 8.
¡ Authentication and authorization. Refer to appendix B.
¡ Logging, monitoring, alerting. Refer to section 2.5.
¡ TLS termination. Refer to other sources for more information.
¡ Caching. Refer to section 4.8.
¡ DevOps and CI/CD if applicable. These are outside the scope of this book.
Services that are generalizable for certain organizations, such as those that collect user 
data for data science, include analytics and machine learning. 
Complex systems may require yet more complexity for high availability and high 
fault-tolerance. If a system has an unavoidable degree of complexity, consider tradeoffs 
of complexity for lower availability and fault-tolerance. 
Discuss possible tradeoffs in other requirements to improve complexity, such as ETL 
pipelines to delay data processing operations that need not occur in real time. 
A common technique to trade off complexity for better latency and performance is 
to use techniques that minimize the size of messages in network communication. Such 
techniques include RPC serialization frameworks and Metadata services. (Refer to section 6.3 for a discussion on Metadata service.)
RPC serialization frameworks such as Avro, Thrift, and protobuf can reduce message 
size at the expense of maintaining schema files. (Refer to section 6.7 for a discussion 


72
Chapter 3  Non-functional requirements
of REST vs RPC.) We should always suggest using such serialization frameworks in any 
interview, and we will not mention this point again in the book. 
We should also discuss how outages can occur, evaluate the effect of various outages 
on users and the business, and how to prevent and mitigate outages. Common concepts 
include replication, failover, and authoring runbooks. Runbooks are discussed in section 2.5.3. 
We will discuss complexity in all chapters of part 2. 
3.7.1	
Continuous deployment (CD) 
Continuous deployment (CD) was first mentioned in this book in section 1.4.5. As 
mentioned in that section, CD allows easy deployments and rollbacks. We have a fast 
feedback cycle that improves our system’s maintainability. If we accidentally deploy a 
buggy build to production, we can easily roll it back. Fast and easy deployments of 
incremental upgrades and new features lead to a fast software development lifecycle. 
This is a major advantage of services over monoliths, as discussed in appendix A. 
Other CD techniques include blue/green deployments, also referred to as zero 
downtime deployments. Refer to sources such as https://spring.io/blog/2016/05/31/ 
zero-downtime-deployment-with-a-database, https://dzone.com/articles/zero-downtime 
-deployment, and https://craftquest.io/articles/what-are-zero-downtime-atomic 
-deployments for more information.
Static code analysis tools like SonarQube (https://www.sonarqube.org/) also improve 
our system’s maintainability. 
3.8	
Cost
In system design discussions, we can suggest trading off other non-functional requirements for lower cost. Examples: 
¡ Higher cost for lower complexity by vertical scaling instead of horizontal scaling. 
¡ Lower availability for improved costs by decreasing the redundancy of a system 
(such as the number of hosts, or the replication factor in a database). 
¡ Higher latency for improved costs by using a data center in a cheaper location 
that is further away from users. 
Discuss the cost of implementation, cost of monitoring, and cost of each non-functional requirement such as high availability. 
Production problems vary in seriousness and how quickly they must be addressed 
and resolved, so do not implement more monitoring and alerting than required. Costs 
are higher if engineers need to be alerted to a problem as soon as it occurs, compared 
to when it is permissible for alerts to be created hours after a problem. 
Besides the cost of maintenance in the form of addressing possible production problems, there will also be costs due to the natural atrophy of software over time as libraries 
and services are deprecated. Identify components that may need future updates. Which 
dependencies (such as libraries) will prevent other components from being easily 


	
73
Privacy
updated if these dependencies become unsupported in the future? How may we design 
our system to more easily replace these dependencies if updates are required? 
How likely is it that we will need to change dependencies in the future, particularly 
third-party dependencies where we have less control? Third-party dependencies may 
be decommissioned or prove unsatisfactory for our requirements, such as reliability or 
security problems.
A complete cost discussion should include consideration of the costs to decommission the system if necessary. We may decide to decommission the system for multiple 
reasons, such as the team deciding to change its focus or the system has too few users to 
justify its development and maintenance costs. We may decide to provide the existing 
users with their data, so we will need to extract the data into various text and/or CSV 
files for our users.
3.9	
Security
During an interview, we may need to discuss possible security vulnerabilities in our system and how we will prevent and mitigate security breaches. This includes access both 
from external parties and internally within our organization. The following topics are 
commonly discussed with regard to security: 
¡ TLS termination versus keeping data encrypted between services or hosts in a 
data center (called encryption in transit). TLS termination is usually done to 
save processing because encryption between hosts in a data center is usually not 
required. There may be exceptions for sensitive data on which we use encryption 
in transit. 
¡ Which data can be stored unencrypted, and which should be stored encrypted 
(called encryption at rest). Encryption at rest is conceptually different from storing 
hashed data.
We should have some understanding of OAuth 2.0 and OpenID Connect, which are 
described in appendix B. 
We may also discuss rate limiting to prevent DDoS attacks. A rate-limiting system can 
make up its own interview question, and this is discussed in chapter 8. It should be mentioned during the design of almost any external-facing system.
3.10	 Privacy
Personally Identifiable Information (PII) is data that can be used to uniquely identify 
a customer, such as full name, government identifiers, addresses, email addresses, and 
bank account identifiers. PII must be safeguarded to comply with regulations such as 
the General Data Protection Regulation (GDPR) and the California Consumer Privacy 
Act (CCPA). This includes both external and internal access. 
Within our system, access control mechanisms should be applied to PII stored in 
databases and files. We can use mechanisms such as the Lightweight Directory Access 
Protocol (LDAP). We can encrypt data both in transit (using SSL) and at rest. 


74
Chapter 3  Non-functional requirements
Consider using hashing algorithms such as SHA-2 and SHA-3 to mask PII and maintain individual customer privacy in computing aggregate statistics (e.g., mean number 
of transactions per customer).
If PII is stored on an append-only database or file system like HDFS, a common privacy technique is to assign each customer an encryption key. The encryption keys can 
be stored in a mutable storage system like SQL. Data associated with a particular customer should be encrypted with their encryption key before it is stored. If a customer’s 
data needs to be deleted, all that must be done is to delete the customer’s encryption 
key, and then all of the customer’s data on the append-only storage becomes inaccessible and hence effectively deleted.
We can discuss the complexity, cost, and effects of privacy along many aspects, such 
as customer service or personalization, including machine learning. 
 We should also discuss prevention and mitigation strategies for data breaches, such 
as data retention policies and auditing. The details tend to be specific to each organization, so it is an open-ended discussion. 
3.10.1	 External vs. internal services
If we design an external service, we definitely should design security and privacy mechanisms. What about internal services that only serve other internal services? We may 
decide to rely on the security mechanisms of our user services against malicious external attackers and assume that internal users will not attempt malicious actions, so security measures are not required for our rate limiter service. We may also decide that we 
trust our user services not to request data about rate limiter requestors from other user 
services, so privacy measures are not required. 
However, it is likely that we will decide that our company should not trust internal 
users to properly implement security mechanisms, should not trust that internal users 
are not malicious, and should not trust internal users to not inadvertently or maliciously 
violate our customer’s privacy. We should adopt an engineering culture of implementing security and privacy mechanisms by default. This is consistent with the internal 
access controls and privacy policies of all kinds of services and data adopted by most 
organizations. For example, most organizations have role-based access control for each 
service’s Git repository and CI/CD. Most organizations also have procedures to grant 
access to employee and customer data only to persons they deem necessary to have 
access to this data. These access controls and data access are typically limited in scope 
and duration as much as possible. There is no logical reason to adopt such policies for 
certain systems and not adopt them for others. We should ensure that our internal service does not expose any sensitive features or data before we decide that it can exclude 
security and privacy mechanisms. Moreover, every service, external or internal, should 
log access to sensitive databases.
Another privacy mechanism is to have a well-defined policy for storing user information. Databases that store user information should be behind services that are 


	
75
Further reading
well-documented and have tight security and strict access control policies. Other services and databases should only store user IDs and no other user data. The user IDs can 
be changed either periodically or in the event of a security or privacy breach. 
Figure 1.8 illustrates a service mesh, including security and privacy mechanisms, 
illustrated as an external request to an identity and access management service.
3.11	 Cloud native
Cloud native is an approach to address non-functional requirements, including scalability, fault-tolerance, and maintainability. The definition of cloud native by the Cloud 
Native Computing Foundation is as follows (https://github.com/cncf/toc/blob/
main/DEFINITION.md). I italicized certain words for emphasis: 
Cloud native technologies empower organizations to build and run scalable 
applications in modern, dynamic environments such as public, private, and 
hybrid clouds. Containers, service meshes, microservices, immutable infrastructure, and 
declarative APIs exemplify this approach.
These techniques enable loosely coupled systems that are resilient, manageable, and 
observable. Combined with robust automation, they allow engineers to make highimpact changes frequently and predictably with minimal toil. 
The Cloud Native Computing Foundation seeks to drive adoption of this 
paradigm by fostering and sustaining an ecosystem of open source, vendorneutral projects. We democratize state-of-the-art patterns to make these 
innovations accessible for everyone. 
This is not a book on cloud-native computing, but we utilize cloud-native techniques 
(containers, service meshes, microservices, serverless functions, immutable infrastructure or Infrastructure as Code, declarative APIs, automation) throughout this book to 
achieve the benefits (resilient, manageable, observable, allow frequent and predictable changes), and include references to materials on the relevant concepts.
3.12	 Further reading
Interested readers can look up the PACELC theorem, which we do not discuss in this 
book. The PACELC is an extension of the CAP theorem. It states that when a network partition occurs in a distributed system, one must choose between availability and 
consistency, or else during normal operation, one must choose between latency and 
consistency. 
A useful resource that has content similar to this chapter is Microservices for the Enterprise: Designing, Developing, and Deploying (2018, Apress) by Kasun Indrasiri and Prabath 
Siriwardena.


76
Chapter 3  Non-functional requirements
Summary
¡ We must discuss both the functional and non-functional requirements of a 
system. Do not make assumptions about the non-functional requirements. 
­Non-functional characteristics can be traded off against each other to optimize 
for the non-functional requirements.
¡ Scalability is the ability to easily adjust the system’s hardware resource usage for 
cost efficiency. This is almost always discussed because it is difficult or impossible 
to predict the amount of traffic to our system.
¡ Availability is the percentage of time a system can accept requests and return the 
desired response. Most, but not all, systems require high availability, so we should 
clarify whether it is a requirement in our system.
¡ Fault-tolerance is the ability of a system to continue operating if some components fail and the prevention of permanent harm should downtime occur. This 
allows our users to continue using some features and buys time for engineers to 
fix the failed components.
¡ Performance or latency is the time taken for a user’s request to the system to 
return a response. Users expect interactive applications to load fast and respond 
quickly to their input.
¡ Consistency is defined as all nodes containing the same data at a moment in time, 
and when changes in data occur, all nodes must start serving the changed data at 
the same time. In certain systems, such as financial systems, multiple users viewing the same data must see the same values, while in other systems such as social 
media, it may be permissible for different users to view slightly different data at 
any point in time, as long as the data is eventually the same.
¡ Eventually, consistent systems trade off accuracy for lower complexity and cost. 
¡ Complexity must be minimized so the system is cheaper and easier to build 
and maintain. Use common techniques, such as common services, wherever 
applicable.
¡ Cost discussions include minimizing complexity, cost of outages, cost of maintenance, cost of switching to other technologies, and cost of decommissioning.
¡ Security discussions include which data must be secured and which can be unsecured, followed by using concepts such as encryption in transit and encryption 
at rest. 
¡ Privacy considerations include access control mechanisms and procedures, deletion or obfuscation of user data, and prevention and mitigation of data breaches.
¡ Cloud native is an approach to system design that employs a collection of techniques to achieve common non-functional requirements.


77
4
Scaling databases
This chapter covers
¡ Understanding various types of storage 	
	
	 services
¡ Replicating databases
¡ Aggregating events to reduce database writes
¡ Differentiating normalization vs. 	 	
	
	 denormalization
¡ Caching frequent queries in memory
In this chapter, we discuss concepts in scaling databases, their tradeoffs, and common databases that utilize these concepts in their implementations. We consider 
these concepts when choosing databases for various services in our system.  
4.1	
Brief prelude on storage services
Storage services are stateful services. Compared to stateless services, stateful services 
have mechanisms to ensure consistency and require redundancy to avoid data loss. 
A stateful service may choose mechanisms like Paxos for strong consistency or eventual-consistency mechanisms. These are complex decisions, and tradeoffs have to 
be made, which depend on the various requirements like consistency, complexity, 
security, latency, and performance. This is one reason we keep all services stateless 
as much as possible and keep state only in stateful services.


78
Chapter 4  Scaling databases
NOTE    In strong consistency, all accesses are seen by all parallel processes (or 
nodes, processors, etc.) in the same order (sequentially). Therefore, only one 
consistent state can be observed, as opposed to weak consistency, where different 
parallel processes (or nodes, etc.) can perceive variables in different states.
Another reason is that if we keep state in individual hosts of a web or backend service, 
we will need to implement sticky sessions, consistently routing the same user to the 
same host. We will also need to replicate the data in case a host fails and handle failover 
(such as routing the users to the appropriate new host when their host fails). By pushing all states to a stateful storage service, we can choose the appropriate storage/database technology for our requirements, and take advantage of not having to design, 
implement, and make mistakes with managing state. 
Storage can be broadly classified into the following. We should know how to distinguish between these categories. A complete introduction to various storage types is outside the scope of this book (refer to other materials if required), the following are brief 
notes required to follow the discussions in this book: 
¡ Database: 
–	 SQL—Has relational characteristics such as tables and relationships between 
tables, including primary keys and foreign keys. SQL must have ACID 
properties. 
–	 NoSQL—A database that does not have all SQL properties. 
–	 Column-oriented—Organizes data into columns instead of rows for efficient filtering. Examples are Cassandra and HBase. 
–	 Key-value—Data is stored as a collection of key-value pairs. Each key corresponds to a disk location via a hashing algorithm. Read performance is good. 
Keys must be hashable, so they are primitive types and cannot be pointers to 
objects. Values don’t have this limitation; they can be primitives or pointers. 
Key-value databases are usually used for caching, employing various techniques like Least Recently Used (LRU). Cache has high performance but does 
not require high availability (because if the cache is unavailable, the requester 
can query the original data source). Examples are Memcached and Redis. 
¡ Document—Can be interpreted as a key-value database where values have no size 
limits or much larger limits than key-value databases. Values can be in various formats. Text, JSON, or YAML are common. An example is MongoDB. 
¡ Graph—Designed to efficiently store relationships between entities. Examples 
are Neo4j, RedisGraph, and Amazon Neptune. 
¡ File storage—Data stored in files, which can be organized into directories/folders. 
We can see it as a form of key-value, with path as the key.  
¡ Block storage—Stores data in evenly sized chunks with unique identifiers. We are 
unlikely to use block storage in web applications. Block storage is relevant for 
designing low-level components of other storage systems (such as databases).  


	
79
Replication
¡ Object storage—Flatter hierarchy than file storage. Objects are usually accessed 
with simple HTTP APIs. Writing objects is slow, and objects cannot be modified, 
so object storage is suited for static data. AWS S3 is a cloud example.
4.2	
When to use vs. avoid databases
When deciding how to store a service’s data, you may discuss using a database vs. other 
possibilities such as file, block, and object storage. During the interview, remember that 
even though you may prefer certain approaches and you can state a preference during 
an interview, you must be able to discuss all relevant factors and consider others’ opinions. In this section, we discuss various factors that you may bring up. As always, discuss 
various approaches and tradeoffs.  
The decision to choose between a database or filesystem is usually based on discretion 
and heuristics. There are few academic studies or rigorous principles. A commonly cited 
conclusion from an old 2006 Microsoft paper (https://www.microsoft.com/en-us/ 
research/publication/to-blob-or-not-to-blob-large-object-storage-in-a-database-or-a 
-filesystem) states, “Objects smaller than 256K are best stored in a database while objects 
larger than 1M are best stored in the filesystem. Between 256K and 1M, the read:write 
ratio and rate of object overwrite or replacement are important factors.” A few other 
points: 
¡ SQL Server requires special configuration settings to store files larger than 2 GB. 
¡ Database objects are loaded entirely into memory, so it is inefficient to stream a 
file from a database.
¡ Replication will be slow if database table rows are large objects because these 
large blob objects will need to be replicated from the leader node to follower 
nodes.
4.3	
Replication
We scale a database(i.e., implement a distributed database onto multiple hosts, commonly called nodes in database terminology) via replication, partitioning, and sharding. Replication is making copies of data, called replicas, and storing them on different 
nodes. Partitioning and sharing are both about dividing a data set into subsets. Sharding implies the subsets are distributed across multiple nodes, while partitioning does 
not. A single host has limitations, so it cannot fulfill our requirements: 
¡ Fault-tolerance—Each node can back up its data onto other nodes within and 
across data centers in case of node or network failure. We can define a failover 
process for other nodes to take over the roles and partitions/shards of failed 
nodes. 
¡ Higher storage capacity—A single node can be vertically scaled to contain multiple 
hard drives of the largest available capacity, but this is monetarily expensive, and 
along the way, the node’s throughput may become a problem. 


80
Chapter 4  Scaling databases
¡ Higher throughput—The database needs to process reads and writes for multiple 
simultaneous processes and users. Vertical scaling approaches its limits with the 
fastest network card, a better CPU, and more memory. 
¡ Lower latency—We can geographically distribute replicas to be closer to dispersed 
users. We can increase the number of particular replicas on a data center if there 
are more reads on that data from that locality. 
To scale reads (SELECT operation), we simply increase the number of replicas of that 
data. Scaling writes is more difficult, and much of this chapter is about handling the 
difficulties of scaling write operations.
4.3.1	
Distributing replicas
A typical design is to have one backup onto a host on the same rack and one backup on 
a host on a different rack or data center or both. There is much literature on this topic 
(e.g., https://learn.microsoft.com/en-us/azure/availability-zones/az-overview). 
The data may also be sharded, which provides the following benefits. The main 
tradeoff of sharding is increased complexity from needing to track the shards’ locations: 
¡ Scale storage—If a database/table is too big to fit into a single node, sharding 
across nodes allows the database/table to remain a single logical unit. 
¡ Scale memory—If a database is stored in memory, it may need to be sharded, 
since vertical scaling of memory on a single node quickly becomes monetarily 
expensive. 
¡ Scale processing—A sharded database may take advantage of parallel processing. 
¡ Locality—A database may be sharded such that the data a particular cluster node 
needs is likely to be stored locally rather than on another shard on another node. 
NOTE    For linearizability, certain partitioned databases like HDFS implement 
deletion as an append operation (called a logical soft delete). In HDFS, this is 
called appending a tombstone. This prevents disruptions and inconsistency to 
read operations that are still running while deletion occurs.
4.3.2	
Single-leader replication 
In single-leader replication, all write operations occur on a single node, called the 
leader. Single-leader replication is about scaling reads, not writes. Some SQL distributions such as MySQL and Postgres have configurations for single-leader replication. The SQL service loses its ACID consistency. This is a relevant consideration if we 
choose to horizontally scale a SQL database to serve a service with high traffic.


	
81
Replication
Figure 4.1 illustrates single-leader replication with primary-secondary leader failover. 
All writes (also called Data Manipulation Language or DDL queries in SQL) occur on 
the primary leader node and are replicated to its followers, including the secondary 
leader. If the primary leader fails, the failover process promotes the secondary leader to 
primary. When the failed leader is restored, it becomes the secondary leader. 
Clients
Leader
Secondary Leader
Follower 0
Follower 1
Follower n
Follower n + 1
Follower n + 2
Follower n + m
When leader fails, write to secondary leader, promote it to primary leader.
Reads
Figure 4.1    Single-leader replication with primary-secondary leader failover. Figure adapted from Web 
Scalability for Startup Engineers by Artur Ejsmont, figure 5.4 (McGraw Hill, 2015).
A single node has a maximum throughput that must be shared by its followers, imposing a maximum number of followers, which in turn limits read scalability. To scale 
reads further, we can use multi-level replication, shown in figure 4.2. There are multiple levels of followers, like a pyramid. Each level replicates to the one below. Each node 
replicates to the number of followers that it is capable of handling, with the tradeoff 
that consistency is further delayed. 


82
Chapter 4  Scaling databases
Leader
Follower 0
Follower 1
Follower n
Follower 0
Follower 1
Follower n
Follower 0
Follower 1
Follower n
Follower 0
Follower 1
Follower n
Figure 4.2    Multi-level replication. Each node replicates to its followers, which in turn replicates to their 
followers. This architecture ensures a node replicates to the number of followers that it is capable of 
handling, with the tradeoff that consistency is further delayed. 
Single-leader replication is the simplest to implement. The main limitation of single-leader replication is that the entire database must fit into a single host. Another 
limitation is eventual consistency, as write replication to followers takes time.  
MySQL binlog-based replication is an example of single-leader replication. Refer to 
chapter 5 of Ejsmont’s book Web Scalability for Startup Engineers for a good discussion. 
Here are some relevant online documents:
¡ https://dev.to/tutelaris/introduction-to-mysql-replication-97c


	
83
Replication
¡ https://dev.mysql.com/doc/refman/8.0/en/binlog-replication-configuration 
-overview.html 
¡ https://www.digitalocean.com/community/tutorials/how-to-set-up-replication 
-in-mysql
¡ https://docs.microsoft.com/en-us/azure/mysql/single-server/how-to-data-in 
-replication
¡ https://www.percona.com/blog/2013/01/09/how-does-mysql-replication 
-really-work/
¡ https://hevodata.com/learn/mysql-binlog-based-replication/ 
A hack to scaling single-leader replication: Query logic in the application layer 
Manually entered strings increase database size slowly, which you can verify with simple 
estimates and calculations. If data was programmatically generated or has accumulated 
for a long period of time, storage size may grow beyond a single node.  
If we cannot reduce the database size but we wish to continue using SQL, a possible 
way is to divide the data between multiple SQL databases. This means that our service 
has to be configured to connect to more than one SQL database, and we need to rewrite 
our SQL queries in the application to query from the appropriate database. 
If we had to partition a single table into two or more databases, then our application 
will need to query multiple databases and combine the results. Querying logic is no longer encapsulated in the database and has spilled into the application. The application 
must store metadata to track which databases contain particular data. This is essentially 
multi-leader replication with metadata management in the application. The services 
and databases are more difficult to maintain, particularly if there are multiple services 
using these databases.  
For example, if our bagel cafe recommender Beigel processes billions of searches 
daily, a single SQL table fact_searches that records our searches will grow to TBs 
within days. We can partition this data across multiple databases, each in its own cluster. We can partition by day and create a new table daily and name the tables in the 
format fact_searches_YYYY_MM_DD (e.g., fact_searches_2023_01_01 and fact_
searches_2023_01_02). Any application that queries these tables will need to have this 
partition logic, which, in this case, is the table-naming convention. In a more complex 
example, certain customers may make so many transactions that we need tables just 
for them. If many queries to our search API originate from other food recommender 
apps, we may create a table for each of them (e.g., fact_searches_a_2023_01_01) 
to store all searches on January 1, 2023, from companies that start with the letter A. We 
may need another SQL table, search_orgs, that stores metadata about companies that 
make search requests to Beigel. 
We may suggest this during a discussion as a possibility, but it is highly unlikely that we 
will use this design. We should use databases with multi-leader or leaderless replication. 


84
Chapter 4  Scaling databases
4.3.3	
Multi-leader replication 
Multi-leader and leaderless replication are techniques to scale writes and database 
storage size. They require handling of race conditions, which are not present in single-leader replication. 
In multi-leader replication, as the name suggests, there are multiple nodes designated as leaders and writes can be made on any leader. Each leader must replicate its 
writes to all other nodes.  
Consistency problems and approaches 
This replication introduces consistency and race conditions for operations where 
sequence is important. For example, if a row is updated in one leader while it is being 
deleted in another, what should be the outcome? Using timestamps to order operations does not work because the clocks on different nodes cannot be perfectly synchronized. Attempting to use the same clock on different nodes doesn’t work because 
each node will receive the clock’s signals at different times, a well-known phenomenon 
called clock skew. So even server clocks that are periodically synchronized with the same 
source will differ by a few milliseconds or greater. If queries are made to different servers within time intervals smaller than this difference, it is impossible to determine the 
order in which they were made. 
Here we discuss replication problems and scenarios related to consistency that we 
commonly encounter in a system design interview. These situations may occur with any 
storage format, including databases and file systems. The book Designing Data-Intensive 
Applications by Martin Kleppmann and its references have more thorough treatments of 
replication pitfalls. 
What is the definition of database consistency? Consistency ensures a database 
transaction brings the database from one valid state to another, maintaining database 
invariants; any data written to the database must be valid according to all defined rules, 
including constraints, cascades, triggers, or any combination thereof. 
As discussed elsewhere in this book, consistency has a complex definition. A common informal understanding of consistency is that the data must be the same for every 
user:  
1	 The same query on multiple replicas should return the same results, even though 
the replicas are on different physical servers. 
2	 Data Manipulation Language (DML) queries (i.e., INSERT, UPDATE, or DELETE) 
on different physical servers that affect the same rows should be executed in the 
sequence that they were sent.  
We may accept eventual consistency, but any particular user may need to receive data 
that is a valid state to them. For example, if user A queries for a counter’s value, increments a counter by one and then queries again for that counter’s value, it will make 
sense to user A to receive a value incremented by one. Meanwhile, other users who 
query for the counter may be provided the value before it was incremented. This is 
called read-after-write consistency. 


	
85
Replication
In general, look for ways to relax the consistency requirements. Find approaches 
that minimize the amount of data that must be kept consistent for all users. 
DML queries on different physical servers that affect the same rows may cause race 
conditions. Some possible situations: 
¡ DELETE and INSERT the same row on a table with a primary key. If the DELETE 
executed first, the row should exist. If the INSERT was first, the primary key prevents execution, and DELETE should delete the row. 
¡ Two UPDATE operations on the same cell with different values. Only one should 
be the eventual state. 
What about DML queries sent at the same millisecond to different servers? This is 
an exceedingly unlikely situation, and there seems to be no common convention for 
resolving race conditions in such situations. We can suggest various approaches. One 
approach is to prioritize DELETE over INSERT/UPDATE and randomly break the ties 
for other INSERT/UPDATE queries. Anyway, a competent interviewer will not waste 
seconds of the 50-minute interview on discussions that yield no signals like this one. 
4.3.4	
Leaderless replication 
In leaderless replication, all nodes are equal. Reads and writes can occur on any node. 
How are race conditions handled? One method is to introduce the concept of quorum. A quorum is the minimum number of nodes that must be in agreement for consensus. It is easy to reason that if our database has n nodes and reads and writes both 
have quorums of n/2 + 1 nodes, consistency is guaranteed. If we desire consistency, 
we choose between fast writes and fast reads. If fast writes are required, set a low write 
quorum and high read quorum, and vice versa for fast reads. Otherwise, only eventual 
consistency is possible, and UPDATE and DELETE operations cannot be consistent. 
Cassandra, Dynamo, Riak, and Voldemort are examples of databases that use leaderless replication. In Cassandra, UPDATE operations suffer from race conditions, while 
DELETE operations are implemented using tombstones instead of the rows actually 
being deleted. In HDFS, reads and replication are based on rack locality, and all replicas are equal.  
4.3.5	
HDFS replication 
This is a brief refresher section on HDFS, Hadoop, and Hive. Detailed discussions are 
outside the scope of this book. 
HDFS replication does not fit cleanly into any of these three approaches. An HDFS 
cluster has an active NameNode, a passive (backup) NameNode, and multiple Data­
Node nodes. The NameNode executes file system namespace operations like opening, 
closing, and renaming files and directories. It also determines the mapping of blocks 
to DataNodes. The DataNodes are responsible for serving read and write requests from 
the file system’s clients. The DataNodes also perform block creation, deletion, and 
replication upon instruction from the NameNode. User data never flows through the 


86
Chapter 4  Scaling databases
NameNode. HDFS stores a table as one or more files in a directory. Each file is divided 
into blocks, which are sharded across DataNode nodes. The default block size is 64 MB; 
this value can be set by admins. 
Hadoop is a framework that stores and processes distributed data using the 
MapReduce programming model. Hive is a data warehouse solution built on top of 
Hadoop. Hive has the concept of partitioning tables by one or more columns for efficient filter queries. For example, we can create a partitioned Hive table as follows: 
CREATE TABLE sample_table (user_id STRING, created_date DATE, 
country STRING) PARTITIONED BY (created_date, country);  
Figure 4.3 illustrates the directory tree of this table. The table’s directory has subdirectories for the date values, which in turn have subdirectories for the column values. 
Queries filtered by created_date and/or country will process only the relevant files, 
avoiding the waste of a full table scan. 
Figure 4.3     An example HDFS directory tree of a table 
“sample_table” whose columns include date and country, 
and the table is partitioned by these two columns. The 
sample_table directory has subdirectories for the date 
values, which in turn have subdirectories for the column 
values.  (Source:  https://stackoverflow.com/ 
questions/44782173/hive-does-hive-support 
-partitioning-and-bucketing-while-usiing-external-tables.)
HDFS is append-only, and does not support UPDATE or DELETE operations, possibly 
because of possible replication race conditions from UPDATE and DELETE. INSERT 
does not have race conditions.  
HDFS has name quotas, space quotas, and storage type quotas. Regarding a directory tree:  
¡ A name quota is a hard limit on the number of file and directory names.  
¡ A space quota is a hard limit on the number of bytes in all files. 
¡ A storage type quota is a hard limit on the usage of specific storage types. Discussion of HDFS storage types is outside the scope of this book. 
TIP    Novices to Hadoop and HDFS often use the Hadoop INSERT command, 
which should be avoided. An INSERT query creates a new file with a single row, 
which will occupy an entire 64 MB block and is wasteful. It also contributes to 
the number of names, and programmatic INSERT queries will soon exceed the  


	
87
Scaling storage capacity with sharded databases  
name quota. Refer to https://hadoop.apache.org/docs/current/hadoop-project 
-dist/hadoop-hdfs/HdfsQuotaAdminGuide.html for more information. One 
should append directly to the HDFS file, while ensuring that the appended rows 
have the same fields as the existing rows in the file to prevent data inconsistency 
and processing errors.
If we are using Spark, which saves data on HDFS, we should use saveAsTable or 
saveAsTextFile instead, such as the following example code snippet. Refer to the 
Spark documentation such as https://spark.apache.org/docs/latest/sql-data-sources 
-hive-tables.html.  
val spark = SparkSession.builder().appName("Our app").config("some.config", 
"value").getOrCreate() 
val df = spark.sparkContext.textFile({hdfs_file}) 
df.createOrReplaceTempView({table_name}) 
spark.sql({spark_sql_query_with_table_name}).saveAsTextFile({hdfs_directory}) 
4.3.6	
Further reading 
Refer to Designing Data-Intensive Applications by Martin Kleppmann (O'Reilly, 2017) for 
more discussion on topics such as
¡ Consistency techniques like read repair, anti-entropy, and tuples. 
¡ Multi-leader replication consensus algorithm and implementations in CouchDB, 
MySQL Group replication, and Postgres. 
¡ Failover problems, like split brain. 
¡ Various consensus algorithms to resolve these race conditions. A consensus algorithm is for achieving agreement on a data value.
4.4	
Scaling storage capacity with sharded databases  
If the database size grows to exceed the capacity of a single host, we will need to delete 
old rows. If we need to retain this old data, we should store it in sharded storage such as 
HDFS or Cassandra. Sharded storage is horizontally scalable and in theory should support an infinite storage capacity simply by adding more hosts. There are production 
HDFS clusters with over 100 PB (https://eng.uber.com/uber-big-data-platform/). 
Cluster capacity of YB is theoretically possible, but the monetary cost of the hardware 
required to store and perform analytics on such amounts of data will be prohibitively 
expensive. 
TIP    We can use a database with low latency such as Redis to store data used to 
directly serve consumers. 
Another approach is to store the data in the consumer’s devices or browser cookies 
and localStorage. However, this means that any processing of this data must also be 
done on the frontend and not the backend.


88
Chapter 4  Scaling databases
4.4.1	
Sharded RDBMS
If we need to use an RDBMS, and the amount of data exceeds what can be stored on 
a single node, we can use a sharded RDBMS solution like Amazon RDS (https://aws 
.amazon.com/blogs/database/sharding-with-amazon-relational-database-service/), 
or implement our own sharded SQL. These solutions impose limitations on SQL 
operations: 
¡ JOIN queries will be much slower. A JOIN query will involve considerable network traffic between each node and every other node. Consider a JOIN between 
two tables on a particular column. If both tables are sharded across the nodes, 
each shard of one table needs to compare the value of this column in every row 
with the same column in every row of the other table. If the JOIN is being done 
on the columns that are used as the shard keys, then the JOIN will be much more 
efficient, since each node will know which other nodes to perform the JOIN on. 
We may constrain JOIN operations to such columns only. 
¡ Aggregation operations will involve both the database and application. Certain 
aggregation operations will be easier than others, such as sum or mean. Each 
node simply needs to sum and/or count the values and then return these aggregated values to the application, which can perform simple arithmetic to obtain 
the final result. Certain aggregation operations such as median and percentile 
will be more complicated and slower. 
4.5	
Aggregating events  
Database writes are difficult and expensive to scale, so we should try to reduce the rate 
of database writes wherever possible in our system’s design. Sampling and aggregation 
are common techniques to reduce database write rate. An added bonus is slower database size growth. 
Besides reducing database writes, we can also reduce database reads by techniques 
such as caching and approximation. Chapter 17 discusses count-min sketch, an algorithm for creating an approximate frequency table for events in a continuous data 
stream. 
Sampling data means to consider only certain data points and ignoring others. There 
are many possible sampling strategies, including sampling every nth data point or just 
random sampling. With sampling in writes, we write data at a lower rate than if we write 
all data points. Sampling is conceptually trivial and is something we can mention during 
an interview.  
Aggregating events is about aggregating/combining multiple events into a single 
event, so instead of multiple database writes, only a single database write must occur. We 
can consider aggregation if the exact timestamps of individual events are unimportant. 
Aggregation can be implemented using a streaming pipeline. The first stage of the 
streaming pipeline may receive a high rate of events and require a large cluster with 
thousands of hosts. Without aggregation, every succeeding stage will also require a 


	
89
Aggregating events  
large cluster. Aggregation allows each succeeding stage to have fewer hosts. We also use 
replication and checkpointing in case hosts fail. Referring to chapter 5, we can use a 
distributed transaction algorithm such as Saga, or quorum writes, to ensure that each 
event is replicated to a minimum number of replicas. 
4.5.1	
Single-tier aggregation
Aggregation can be single or multi-tier. Figure 4.4 illustrates an example of single-tier 
aggregation, for counting numbers of values. In this example, an event can have value 
A, B, C, etc. These events can be evenly distributed across the hosts by a load balancer. 
Each host can contain a hash table in memory and aggregate these counts in its hash 
table. Each host can flush the counts to the database periodically (such as every five 
minutes) or when it is running out of memory, whichever is sooner.
A = 1
B = 3
C = 3
B = 1
C = 2
D = 3
Load Balancer
B = 1
C = 2
D = 3
Figure 4.4     An example illustration of single-tier aggregation. A load balancer distributes events 
across a single layer/tier of hosts, which aggregate them and then writes these aggregated counts to 
the database. If the individual events were written directly to the database, the write rate will be much 
higher, and the database will have to be scaled up. Not illustrated here are the host replicas, which are 
required if high availability and accuracy are necessary. 
4.5.2	
Multi-tier aggregation    
Figure 4.5 illustrates multi-tier aggregation. Each layer of hosts can aggregate events 
from its ancestors in the previous tier. We can progressively reduce the number of hosts 
in each layer until there is a desired number of hosts (this number is up to our requirements and available resources) in the final layer, which writes to the database.
The main tradeoffs of aggregation are eventual consistency and increased complexity. Each layer adds some latency to our pipeline and thus our database writes, so database reads may be stale. Implementing replication, logging, monitoring, and alerting 
also add complexity to this system.


90
Chapter 4  Scaling databases
Load Balancer
Figure 4.5     An example illustration of multi-tier aggregation. This is similar to the inverse of multi-level 
replication. 
4.5.3	
Partitioning  
This requires a level 7 load balancer. (Refer to section 3.1.2 for a brief description of 
a level 7 load balancer.) The load balancer can be configured to process incoming 
events and forward them to certain hosts depending on the events’ contents.   
Referring to the example in figure 4.6, if the events are simply values from A–Z, the 
load balancer can be configured to forward events with values of A–I to certain hosts, 
events with values J–R to certain hosts, and events with values S–Z to certain hosts. The 
hash tables from the first layer of hosts are aggregated into a second layer of hosts, then 
into a final hash table host. Finally, this hash table is sent to a max-heap host, which constructs the final max-heap. 
We can expect event traffic to follow normal distribution, which means certain partitions will receive disproportionately high traffic. To address this, referring to figure 
4.6, we observe that we can allocate a different number of hosts to each partition. Partition A–I has three hosts, J–R has one host, and S–Z has two hosts. We make these 


	
91
Aggregating events  
partitioning decisions because traffic is uneven across partitions, and certain hosts may 
receive disproportionately high traffic, (i.e., they become “hot”), more than what they 
are able to process.  
A: 1
B: 2
C: 5
A: 3
F: 2
E: 2
F: 3
K: 5
Q: 3
S: 5
V: 8
U: 2
Y: 3
Z: 8
A: 4
B: 2
C: 5
E: 2
F: 5
S: 5
U: 2
V: 8
Y: 3
Z: 8
A: 4
B: 2
Z: 8
A–I
J–R
S–Z
V: 8
Z: 8
Max-heap host
Level 7
Load Balancer
Figure 4.6     An example illustration of multi-tier aggregation with partitioning
We also observe that partition J–R has only one host, so it does not have a second layer. 
As designers, we can make such decisions based on our situation. 
Besides allocating a different number of hosts to each partition, another way to 
evenly distribute traffic is to adjust the number and width of the partitions. For example, instead of {A-I, J-R, S-Z}, we can create partitions {{A-B, D-F}, {C, G-J}, {K-S}, {T-Z}}. 
That is, we changed from three to four partitions and put C in the second partition. We 
can be creative and dynamic in addressing our system’s scalability requirements. 
4.5.4	
Handling a large key space  
Figure 4.6 in the previous section illustrates a tiny key space of 26 keys from A–Z. In a 
practical implementation, the key space will be much larger. We must ensure that the 
combined key spaces of a particular level do not cause memory overflow in the next 
level. The hosts in the earlier aggregation levels should limit their key space to less 
than what their memory can accommodate, so that the hosts in the later aggregation 
levels have sufficient memory to accommodate all the keys. This may mean that the 
hosts in earlier aggregation levels will need to flush more frequently. 


92
Chapter 4  Scaling databases
For example, figure 4.7 illustrates a simple aggregation service with only two levels. 
There are two hosts in the first level and one host in the second level. The two hosts in 
the first level should limit their key space to half of what they can actually accommodate, so the host in the second level can accommodate all keys.
A = 1
B = 3
C = 3
B = 1
C = 2
D = 3
events
events
A = 1
B = 4
C = 5
D = 3
Figure 4.7      
A simple aggregation 
service with only two 
levels; two hosts in the 
first level and one host 
in the second level 
We can also provision hosts with less memory for earlier aggregation levels, and hosts 
with more memory in later levels.  
4.5.5	
Replication and fault-tolerance  
So far, we have not discussed replication and fault-tolerance. If a host goes down, it 
loses all of its aggregated events. Moreover, this is a cascading failure because all its earlier hosts may overflow, and these aggregated events will likewise be lost. 
We can use checkpointing and dead letter queues, discussed in sections 3.3.6 and 
3.3.7. However, since a large number of hosts may be affected by the outage of a host 
that is many levels deep, a large amount of processing has to be repeated, which is a 
waste of resources. This outage may also add considerable latency to the aggregation. 
A possible solution is to convert each node into an independent service with a cluster of multiple stateless nodes that make requests to a shared in-memory database like 
Redis. Figure 4.8 illustrates such a service. The service can have multiple hosts (e.g., 
three stateless hosts). A shared load balancing service can spread requests across these 
hosts. Scalability is not a concern here, so each service can have just a few (e.g., three 
hosts for fault-tolerance).
Host 0
Host 1
Redis
Host 2
Load balancer
Figure 4.8     We can 
replace a node with a 
service, which we refer 
to as an aggregation 
unit. This unit has three 
stateless hosts for faulttolerance, but we can use 
more hosts if desired. 


	
93
Batch and streaming ETL
At the beginning of this chapter, we discussed that we wanted to avoid database writes, 
which we seem to contradict here. However, each service has a separate Redis cluster, so 
there is no competition for writing to the same key. Moreover, these aggregated events 
are deleted each successful flush, so the database size will not grow uncontrollably. 
NOTE     We can use Terraform to define this entire aggregation service. Each 
aggregation unit can be a Kubernetes cluster with three pods, and one host per 
pod (two hosts if we are using a sidecar service pattern). 
4.6	
Batch and streaming ETL
ETL (Extract, Transform, Load) is a general procedure of copying data from one or 
more sources into a destination system, which represents the data differently from the 
source(s) or in a different context than the source(s). Batch refers to processing the 
data in batches, usually periodically, but it can also be manually triggered. Streaming 
refers to a continuous flow of data to be processed in real time.
We can think of batch vs. streaming as analogous to polling vs. interrupt. Similar to 
polling, a batch job always runs at a defined frequency regardless of whether there are 
new events to process, while a streaming job runs whenever a trigger condition is met, 
which is usually the publishing of a new event. 
An example use case for batch jobs is to generate monthly bills (such as PDF or CSV 
files) for customers. Such a batch job is especially relevant if the data required for these 
bills are only available on a certain date each month (e.g., billing statements from our 
vendors that we need to generate bills for our customers). If all data to generate these 
periodic files are generated within our organization, we can consider Kappa architecture (refer to chapter 17) and implement a streaming job that processes each piece of 
data as soon as it is available. The advantages of this approach are that the monthly files 
are available almost as soon as the month is over, the data processing costs are spread 
out over the month, and it is easier to debug a function that processes a small piece of 
data at a time, rather than a batch job that processes GBs of data. 
Airflow and Luigi are common batch tools. Kafka and Flink are common streaming 
tools. Flume and Scribe are specialized streaming tools for logging; they aggregate log 
data streamed in real time from many servers. Here we briefly introduce some ETL 
concepts.
An ETL pipeline consists of a Directed Acyclic Graph (DAG) of tasks. In the DAG, a 
node corresponds to a task, and its ancestors are its dependencies. A job is a single run 
of an ETL pipeline.
4.6.1	
A simple batch ETL pipeline
A simple batch ETL pipeline can be implemented using a crontab, two SQL tables, and 
a script (i.e., a program written in a scripting language) for each job. cron is suitable 
for small noncritical jobs with no parallelism where a single machine is adequate. The 
following are the two example SQL tables: 


94
Chapter 4  Scaling databases
CREATE TABLE cron_dag (
  id INT,         -- ID of a job.
  parent_id INT,	
-- Parent job. A job can have 0, 1, or multiple 
parents.
  PRIMARY KEY (id),
  FOREIGN KEY (parent_id) REFERENCES cron_dag (id)
);
CREATE TABLE cron_jobs (
  id INT,
  name VARCHAR(255),
  updated_at INT,
  PRIMARY KEY (id)
);
The crontab’s instructions can be a list of the scripts. In this example, we used Python 
scripts, though we can use any scripting language. We can place all the scripts in a common directory /cron_dag/dag/, and other Python files/modules in other directories. 
There are no rules on how to organize the files; this is up to what we believe is the best 
arrangement:
0 * * * * ~/cron_dag/dag/first_node.py
0 * * * * ~/cron_dag/dag/second_node.py
Each script can follow the following algorithm. Steps 1 and 2 can be abstracted into 
reusable modules:
1	 Check that the updated_at value of the relevant job is less than its dependent 
jobs.
2	 Trigger monitoring if necessary.
3	 Execute the specific job.
The main disadvantages of this setup are:
¡ It isn’t scalable. All jobs run on a single host, which carries all the usual disadvantages of a single host:
–	 There’s a single point of failure.
–	 There may be insufficient computational resources to run all the jobs scheduled at a particular time.
–	 The host’s storage capacity may be exceeded.
¡ A job may consist of numerous smaller tasks, like sending a notification to millions of devices. If such a job fails and needs to be retried, we need to avoid 
repeating the smaller tasks that succeeded (i.e., the individual tasks should be 
idempotent). This simple design does not provide such idempotency.
¡ No validation tools to ensure the job IDs are consistent in the Python scripts and 
SQL tables, so this setup is vulnerable to programming errors.
¡ No GUI (unless we make one ourselves).


	
95
Batch and streaming ETL
¡ We have not yet implemented logging, monitoring, or alerting. This is very 
important and should be our next step. For example, what if a job fails or a host 
crashes while it is running a job? We need to ensure that scheduled jobs complete 
successfully. 
QUESTION    How can we horizontally scale this simple batch ETL pipeline to 
improve its scalability and availability?
Dedicated job scheduling systems include Airflow and Luigi. These tools come with 
web UIs for DAG visualization and GUI user-friendliness. They are also vertically scalable and can be run on clusters to manage large numbers of jobs. In this book, whenever we need a batch ETL service, we use an organizational-level shared Airflow service.
4.6.2	
Messaging terminology
The section clarifies common terminology for various types of messaging and streaming setups that one tends to encounter in technical discussions or literature. 
Messaging system
A messaging system is a general term for a system that transfers data from one application to another to reduce the complexity of data transmission and sharing in applications, so application developers can focus on data processing. 
Message queue
A message contains a work object of instructions sent from one service to another, 
waiting in the queue to be processed. Each message is processed only once by a single 
consumer.
Producer/consumer 
Producer/consumer aka publisher/subscriber or pub/sub, is an asynchronous messaging system that decouples services that produce events from services that process 
events. A producer/consumer system contains one or more message queues. 
Message broker
A message broker is a program that translates a message from the formal messaging 
protocol of the sender to the formal messaging protocol of the receiver. A message 
broker is a translation layer. Kafka and RabbitMQ are both message brokers. RabbitMQ claims to be “the most widely deployed open-source message broker” (https://
www.rabbitmq.com/). AMQP is one of the messaging protocols implemented by RabbitMQ. A description of AMQP is outside the scope of this book. Kafka implements its 
own custom messaging protocol.
Event streaming
Event streaming is a general term that refers to a continuous flow of events that are 
processed in real time. An event contains information about a change of state. Kafka is 
the most common event streaming platform. 


96
Chapter 4  Scaling databases
Pull vs. push
Inter-service communication can be done by pull or push. In general, pull is better 
than push, and this is the general concept behind producer-consumer architectures. 
In pull, the consumer controls the rate of message consumption and will not be 
overloaded. 
Load testing and stress testing may be done on the consumer during its development, and monitoring its throughput and performance with production traffic and 
comparing the measurements with the tests allows the team to accurately determine if 
more engineering resources are needed to improve the tests. The consumer can monitor its throughput and producer queue sizes over time, and the team can scale it as 
required.
If our production system has a continuously high load, it is unlikely that the queue 
will be empty for any significant period, and our consumer can keep polling for messages. If we have a situation where we must maintain a large streaming cluster to process unpredictable traffic spikes within a few minutes, we should use this cluster for 
other lower-priority messages too (i.e., a common Flink, Kafka, or Spark service for the 
organization).
Another situation where polling or pull from a user is better than push is if the user 
is firewalled, or if the dependency has frequent changes and will make too many push 
requests. Pull also will have one less setup step than push. The user is already making 
requests to the dependency. However, the dependency usually does not make requests 
to the user.
The flip side (https://engineering.linkedin.com/blog/2019/data-hub) is if our system collects data from many sources using crawlers; development and maintenance of 
all these crawlers may be too complex and tedious. It may be more scalable for individual data providers to push information to our central repository. Push also allows more 
timely updates.
One more exception where push is better than pull is in lossy applications like audio 
and video live-streaming. These applications do not resend data that failed to deliver 
the first time, and they generally use UDP to push data to their recipients.
4.6.3	
Kafka vs. RabbitMQ
In practice, most companies have a shared Kafka service, that is used by other services. 
In the rest of this book, we will use Kafka when we need a messaging or event-streaming service. In an interview, rather than risk the ire of an opinionated interviewer, it 
is safer to display our knowledge of the details of and differences between Kafka and 
RabbitMQ and discuss their tradeoffs. 
Both can be used to smooth out uneven traffic, preventing our service from being 
overloaded by traffic spikes, and keeping our service cost-efficient, because we do not 
need to provision a large number of hosts just to handle periods of high traffic.
Kafka is more complex than RabbitMQ and provides a superset of capabilities over 
RabbitMQ. In other words, Kafka can always be used in place of RabbitMQ but not vice 
versa.


	
97
Batch and streaming ETL
If RabbitMQ is sufficient for our system, we can suggest using RabbitMQ, and also 
state that our organization likely has a Kafka service that we can use so as to avoid the 
trouble of setup and maintenance (including logging, monitoring and alerting) of 
another component such as RabbitMQ. Table 4.1 lists differences between Kafka and 
RabbitMQ.
Table 4.1    Some differences between Kafka and RabbitMQ
Kafka
RabbitMQ
Designed for scalability, reliability, and availability. More complex setup required than 
RabbitMQ.
Requires ZooKeeper to manage the 
Kafka cluster. This includes configuring IP 
addresses of every Kafka host in ZooKeeper.
Simple to set up, but not scalable by default.  
We can implement scalability on our own at the application level by attaching our application to a load balancer 
and producing to and consuming from the load balancer. 
But this will take more work to set up than Kafka and being 
far less mature will almost certainly be inferior in many 
ways.
A durable message broker because it has 
replication. We can adjust the replication 
factor on ZooKeeper and arrange replication 
to be done on different server racks and 
data centers.
Not scalable, so not durable by default. Messages are lost 
if downtime occurs. Has a “lazy queue” feature to persist 
messages to disk for better durability, but this does not 
protect against disk failure on the host.
Events on the queue are not removed after 
consumption, so the same event can be 
consumed repeatedly. This is for failure tolerance, in case the consumer fails before it 
finished processing the event and needs to 
reprocess the event.
In this regard, it is conceptually inaccurate to 
use the term “queue” in Kafka. It is actually a 
list. But the term “Kafka queue” is commonly 
used.
We can configure a retention period in 
Kafka, which is seven days by default, so an 
event is deleted after seven days regardless 
of whether it has been consumed. We can 
choose to set the retention period to infinite 
and use Kafka as a database.
Messages on the queue are removed upon dequeuing, as 
per the definition of “queue” (RabbitMQ 3.9 released on 
July 26, 2021, has a stream https://www.rabbitmq.com/
streams.html feature that allows repeated consumption of 
each message, so this difference is only present for earlier 
versions.) 
We may create several queues to allow several consumers 
per message, one queue per consumer. But this is not the 
intended use of having multiple queues.
Has the concept of AMQP standard per-message queue 
priority. We can create multiple queues with varying 
priority. Messages on a queue are not dequeued until 
higher-priority queues are empty. No concept of fairness or 
consideration of starvation.
No concept of priority.
4.6.4	
Lambda architecture  
Lambda architecture is a data-processing architecture for processing big data running 
batch and streaming pipelines in parallel. In informal terms, it refers to having parallel 
fast and slow pipelines that update the same destination. The fast pipeline trades off 
consistency and accuracy for lower latency (i.e., fast updates), and vice versa for the 
slow pipeline. The fast pipeline employs techniques such as: 


98
Chapter 4  Scaling databases
¡ Approximation algorithms (discussed in section 17.7). 
¡ In-memory databases like Redis. 
¡ For faster processing, nodes in the fast pipeline may not replicate the data that 
they process so there may be some data loss and lower accuracy from node outages. 
The slow pipeline usually uses MapReduce databases, such as Hive and Spark with 
HDFS. We can suggest lambda architecture for systems that involve big data and 
require consistency and accuracy. 
Note on various database solutions
There are numerous database solutions. Common ones include various SQL distributions, Hadoop and HDFS, Kafka, Redis, and Elasticsearch. There are numerous 
less-common ones, including MongoDB, Neo4j, AWS DynamoDB, and Google’s Firebase 
Realtime Database. In general, knowledge of less common databases, especially proprietary databases, is not expected in a system design interview. Proprietary databases 
are seldom adopted. If a startup does adopt a proprietary database, it should consider 
migrating to an open-source database sooner rather than later. The bigger the database, 
the worse the vendor lock-in as the migration process will be more difficult, error-prone, 
and expensive. 
An alternative to Lambda architecture is Kappa architecture. Kappa architecture is a software architecture pattern for processing streaming data, performing both batch and 
streaming processing with a single technology stack. It uses an append-only immutable 
log like Kafka to store incoming data, followed by stream processing and storage in a 
database for users to query. Refer to section 17.9.1 for a detailed comparison between 
Lambda and Kappa architecture. 
4.7	
Denormalization 
If our service’s data can fit into a single host, a typical approach is to choose SQL and 
normalize our schema. The benefits of normalization include the following: 
¡ They are consistent, with no duplicate data, so there will not be tables with inconsistent data. 
¡ Inserts and updates are faster since only one table has to be queried. In a denormalized schema, an insert or update may need to query multiple tables. 
¡ Smaller database size because there is no duplicate data. Smaller tables will have 
faster read operations. 
¡ Normalized tables tend to have fewer columns, so they will have fewer indexes. 
Index rebuilds will be faster. 
¡ Queries can JOIN only the tables that are needed.  
The disadvantages of normalization include the following:  


	
99
Caching 
¡ JOIN queries are much slower than queries on individual tables. In practice, 
denormalization is frequently done because of this. 
¡ The fact tables contain codes rather than data, so most queries both for our service and ad hoc analytics will contain JOIN operations. JOIN queries tend to be 
more verbose than queries on single tables, so they are more difficult to write and 
maintain.
An approach to faster read operations that is frequently mentioned in interviews is to 
trade off storage for speed by denormalizing our schema to avoid JOIN queries.  
4.8	
Caching 
For databases that store data on disk, we can cache frequent or recent queries in memory. In an organization, various database technologies can be provided to users as 
shared database services, such as an SQL service or Spark with HDFS. These services 
can also utilize caching, such as with a Redis cache.
This section is a brief description of various caching strategies. The benefits of caching include improvements to: 
¡ Performance: This is the intended benefit of a cache, and the other benefits below 
are incidental. A cache uses memory, which is faster and more expensive than a 
database, which uses disk. 
¡ Availability: If the database is unavailable, the service is still available so applications can retrieve data from the cache. This only applies to data that is cached. 
To save costs, a cache may contain only a subset of data in the database. However, 
caches are designed for high performance and low latency, not for high availability. A cache’s design may trade off availability and other non-functional requirements for high performance. Our database should be highly available, and we 
must not rely on the cache for our service’s availability. 
¡ Scalability: By serving frequently requested data, the cache can serve much of 
the service’s load. It is also faster than the database, so requests are served faster 
which decreases the number of open HTTP connections at any one time, and 
a smaller backend cluster can serve the same load. However, this is an inadvisable scalability technique if your cache is typically designed to optimize latency 
and may make tradeoffs against availability to achieve this. For example, one will 
not replicate a cache across data centers because cross data-center requests are 
slow and defeat the main purpose of a cache which is to improve latency. So, if a 
data center experiences an outage (such as from network problems), the cache 
becomes unavailable, and all the load is transferred to the database, which may 
be unable to handle it. The backend service should have rate limiting, adjusted 
to the capacity of the backend and database. 


100
Chapter 4  Scaling databases
Caching can be done at many levels, including client, API Gateway (Rob Vettor, David 
Coulter, Genevieve Warren, “Caching in a cloud-native application.” Microsoft Docs. 
May 17, 2020. (https://docs.microsoft.com/en-us/dotnet/architecture/cloud-native/ 
azure-caching), and at each service (Cloud Native Patterns by Cornelia Davis, (Manning 
Publications, 2019). Figure 4.9 illustrates caching at an API Gateway. This cache can 
scale independently of the services, to serve the traffic volume at any given time. 
Client
API Gateway
Service 1
Service 2
Service 3
Cache
Figure 4.9     Caching at an API gateway. Diagram adapted from Rob Vettor, David Coulter, Genevieve 
Warren. May 17, 2020. “Caching in a cloud-native application.” Microsoft Docs. https://docs.microsoft 
.com/en-us/dotnet/architecture/cloud-native/azure-caching.
4.8.1	
Read strategies
Read strategies are optimized for fast reads.
Cache-aside (lazy loading) 
Cache-aside refers to the cache sitting “aside” the database. Figure 4.10 illustrates cacheaside. In a read request, the application first makes a read request to the cache, which 
returns the data on a cache hit. On a cache miss, the application makes a read request 
to the database, then writes the data to the cache so subsequent requests for this data 
will be cache hits. So, data is loaded only when it is first read, which is called lazy load. 
App
Figure 4.10     
Illustration of 
cache-aside


	
101
Caching 
Cache-aside is best for read-heavy loads. Advantages: 
¡ Cache-aside minimizes the number of read requests and resource consumption. 
To further reduce the number of requests, the application can store the results of 
multiple database requests as a single cache value (i.e., a single cache key for the 
results of multiple database requests). 
¡ Only requested data is written to the cache, so we can easily determine our 
required cache capacity and adjust it as needed to save costs. 
¡ Simplicity of implementation.  
If the cache cluster goes down, all requests will go to the database. We must ensure that 
the database can handle this load. Disadvantages: 
¡ The cached data may become stale/inconsistent, especially if writes are made 
directly to the database. To reduce stale data, we can set a TTL or use writethrough (refer section below) so every write goes through the cache. 
¡ A request with a cache miss is slower than a request directly to the database, 
because of the additional read request and additional write request to the cache. 
Read-through 
In read-through, write-through, or write-back caching, the application makes requests to 
the cache, which may make requests to the database if necessary.
Figure 4.11 illustrates the architecture of read-through, write-through, or write-back 
caching. In a cache miss on a read-through cache, the cache makes a request to the 
database and stores the data in the cache (i.e., also lazy load, like cache-aside), then 
returns the data to the application. 
App
Figure 4.11     In read-through, write-through, or write-back caching, the application makes requests to 
the cache, which makes requests to the database if necessary. So, this simple architecture diagram can 
represent all three caching strategies. 
Read-through is best for read-heavy loads. As the application does not contact the database, the implementation burden of database requests is shifted from the application 
to the cache. A tradeoff is that unlike cache-aside, a read-through cache cannot group 
multiple database requests as a single cache value.
4.8.2	
Write strategies 
Write strategies are optimized to minimize cache staleness, in exchange for higher 
latency or complexity.


102
Chapter 4  Scaling databases
Write-through  
Every write goes through the cache, then to the database. Advantages: 
¡ It is consistent. The cache is never stale since cache data is updated with every 
database write. 
Disadvantages: 
¡ Slower writes since every write is done on both the cache and database. 
¡ Cold start problem because a new cache node will have missing data and cache 
misses. We can use cache-aside to resolve this. 
¡ Most data is never read, so we incur unnecessary cost. We can configure a TTL 
(time-to-live) to reduce wasted space. 
¡ If our cache is smaller than our database, we must determine the most appropriate cache eviction policy. 
Write-back/write-behind 
The application writes data to the cache, but the cache does not immediately write to 
the database. The cache periodically flushes updated data to the database. Advantages: 
¡ Faster writes on average than write-through. Writes to database are not blocking. 
Disadvantages: 
¡ Same disadvantages as write-through, other than slower writes. 
¡ Complexity because our cache must have high availability, so we cannot make 
tradeoffs against availability to improve performance/latency. The design will be 
more complex since it must have both high availability and performance. 
Write-around 
In write-around, the application only writes to the database. Referring to figure 4.12, 
write-around is usually combined with cache-aside or read-through. The application 
updates the cache on a cache miss. 
App
App
Figure 4.12     Two possible architectures of write-around. (Left) Write-around with cache-aside. (Right) 
Write-around with read-through. 


	
103
Examples of different kinds of data to cache and how to cache them
4.9	
Caching as a separate service
Why is caching a separate service? Why not just cache in the memory of a service’s 
hosts? 
¡ Services are designed to be stateless, so each request is randomly assigned to a 
host. Since each host may cache different data, it is less likely to have cached any 
particular request that it receives. This is unlike databases, which are stateful and 
can be partitioned, so each database node is likely to serve requests for the same 
data. 
¡ Further to the previous point, caching is especially useful when there are uneven 
request patterns that lead to hot shards. Caching is useless if requests or responses 
are unique. 
¡ If we cache on hosts, the cache will be wiped out every time our service gets a 
deployment, which may be multiple times every day. 
¡ We can scale the cache independently of the services that it serves (though this 
comes with the dangers discussed in the beginning of this chapter). Our caching 
service can use specific hardware or virtual machines that are optimized for the 
non-functional requirements of a caching service, which may be different from 
the services that it serves.
¡ If many clients simultaneously send the same request that is a cache miss, our 
database service will execute the same query many times. Caches can deduplicate 
requests and send a single request to our service. This is called request coalescing, and it reduces the traffic on our service.
Besides caching on our backend service, we should also cache on clients (browser or 
mobile apps) to avoid the overhead of network requests if possible. We should also 
consider using a CDN.
4.10	 Examples of different kinds of data to cache and how to cache them
We can cache either HTTP responses or database queries. We can cache the body of an 
HTTP response, and retrieve it using a cache key, which is the HTTP method and URI 
of the request. Within our application, we can use the cache-aside pattern to cache 
relational database queries.
Caches can be private or public/shared. Private cache is on a client and is useful for 
personalized content. Public cache is on a proxy such as a CDN, or on our services. 
Information that should not be cached includes the following:
¡ Private information must never be stored in a cache. An example is bank account 
details.
¡ Realtime public information, such as stock prices, or flight arrival times or hotel 
room availabilities in the near future. 


104
Chapter 4  Scaling databases
¡ Do not use private caching for paid or copyrighted content, such as books or videos that require payment.
¡ Public information that may change can be cached but should be revalidated 
against the origin server. An example is availability of flight tickets or hotel rooms 
next month. The server response will be just a response code 304 confirmation 
that the cached response is fresh, so this response will be much smaller than if 
there was no caching. This will improve network latency and throughput. We set 
a max-age value that indicates our assessment on how long the cached response 
remains fresh. However, we may have reason to believe that conditions may 
change in the future that cause this max-age value may become too long, so we 
may wish to implement logic in our backend that quickly validates that a cached 
response is still fresh. If we do this, we return must-revalidate in our response 
so clients will revalidate cached responses with our backend before using them.
Public information that will not change for a long time can be cached with a long 
cache expiry time. Examples include bus or train schedules.
In general, a company can save hardware costs by pushing as much processing and 
storage as possible onto the clients’ devices and use data centers only to back up critical data and for communication between users. For example, WhatsApp stores a user’s 
authentication details and their connections, but does not store their messages (which 
are the bulk of a user’s storage consumption). It provides Google Drive backup, so it 
pushes message backup costs onto another company. Freed of this cost, WhatsApp can 
continue to be free to its users, who pay Google for storage if they exceed the free storage tier. 
However, we should not assume that the localStorage caching is functioning as 
intended, so we should always expect cache misses and prepare our service to receive 
these requests. We cache in every layer (client/browser, load balancer, frontend/API 
Gateway/sidecar, and in our backend) so requests pass through as few services as possible. 
This allows lower latency and cost.
A browser starts rendering a webpage only after it has downloaded and processed all 
the latter’s CSS files, so browser caching of CSS may considerably improve browser app 
performance.
NOTE    Refer to https://csswizardry.com/2018/11/css-and-network-performance/
for a discussion on optimizing a webpage’s performance by allowing the browser 
to download and process all of a webpage’s CSS as quickly as possible.
A disadvantage of caching on the client is that it complicates usage analytics, since the 
backend will not receive an indication that the client accessed this data. If it is necessary or beneficial to know that the client accessed its cached data, we will need the 
additional complexity of logging these usage counts in the client and send these logs 
to our backend. 


	
105
Cache invalidation
4.11	 Cache invalidation
Cache invalidation is the process where cache entries are replaced or removed. Cache 
busting is cache invalidation specifically for files. 
4.11.1	 Browser cache invalidation
For browser caches, we typically set a max-age for each file. What if a file is replaced by 
a new version before its cache expiry? We use a technique called fingerprinting, which 
gives these files new identifiers (version numbers, file names or query string hashes). 
For example, a file named “style.css” can instead be named “style.b3d716.css,” and the 
hash in the file name can be replaced during a new deployment. In another example, 
an HTML tag <img src=/assets/image.png /> that contains an image file name 
can instead be <img src=/assets/image.png?hash=a3db6e />; we use a query 
parameter hash to indicate the file version. With fingerprinting, we can also use the 
immutable cache-control option to prevent unnecessary requests to the origin server.
Fingerprinting is important for caching multiple GET requests or files that depend 
on each other. GET request caching headers cannot express that certain files or 
responses are interdependent, which may cause old versions of files to be deployed.
For example, we will typically cache CSS and JavaScript but not HTML (unless the 
webpage is static; many browser apps we build will display different content on each 
visit). However, all of them may change in a new deployment of our browser app. If 
we serve new HTML with old CSS or JavaScript, the webpage may be broken. A user 
may instinctively click the browser reload button, which will resolve the problem as the 
browser revalidates with the origin server when the user reloads the page. But this is a 
bad user experience. These problems are difficult to find during testing. Fingerprinting ensures that the HTML contains the correct CSS and JavaScript file names.
We may decide to try to avoid this problem without fingerprinting by caching HTML 
as well as CSS and JavaScript and setting the same max-age for all these files so they will 
expire simultaneously. However, the browser may make requests for these different files 
at different times, separated by seconds. If a new deployment happens to be in progress 
during these requests, the browser may still get a mix of old and new files.
Besides dependent files, an application may also contain dependent GET requests. 
For example, a user may make a GET request for a list of items (items on sale, hotel 
rooms, flights to San Francisco, photo thumbnails, etc.), followed by a GET request for 
details of an item. Caching the first request may cause requests for details of a product 
that no longer exists. REST architecture best practices dictate that requests are cacheable by default, but depending on these considerations, we should either not cache or 
set a short expiry time.
4.11.2	 Cache invalidation in caching services
We do not have direct access to clients’ caches, so this restricts our cache invalidation options to techniques like setting max-age or fingerprinting. However, we can 
directly create, replace, or remove entries in a caching service. There are many online 


106
Chapter 4  Scaling databases
resources on cache replacement policies, and their implementations are outside the 
scope of this book, so we will only briefly define a few common ones here.
¡ Random replacement: Replace a random item when the cache is full. It is the 
simplest strategy.
¡ Least recently used (LRU): Replace the least recently used item first. 
¡ First in first out (FIFO): Replace the items in the order they were added, regardless of how often they are used/accessed.
¡ Last in first out (LIFO), also called first in last out (FILO): Replace the items 
in the reverse order they were added, regardless of how often they are used/
accessed.
4.12	 Cache warming
Cache warming means to fill a cache with entries ahead of the first requests for these 
entries, so each first request for an entry can be served from the cache rather than 
result in a cache miss. Cache warming applies to services like CDNs or our frontend or 
backend services, not to browser cache.
The advantage of cache warming is that the first request for precached data will have 
the same low latency as subsequent requests. However, cache warming comes with many 
disadvantages, including the following:
¡ Additional complexity and cost of implementing cache warning. A caching service may contain thousands of hosts and warming them can be a complex and 
costly process. We can reduce the cost by only partially filling the cache, with 
entries, which will be most frequently requested. Refer to https://netflixtechblog 
.com/cache-warming-agility-for-a-stateful-service-2d3b1da82642 for a discussion 
of Netflix’s cache warmer system design.
¡ Additional traffic from querying our service to fill the cache, including on our 
frontend, backend, and database services. Our service may not be able to take the 
load of cache warming.
¡ Assuming we have user base of millions of users, only the first user who accessed 
that data will receive a slow experience. This may not justify the complexity and 
cost of cache warming. Frequently accessed data will be cached on its first request, 
while infrequently accessed data does not justify caching or cache warming.
¡ The cache expiry time cannot be short, or cache items may expire before they 
are used, and warming the cache is a waste of time. So, we either need to set a 
long expiry time, and our cache service is bigger and more expensive than necessary, or we will need to set different expiry times for different entries, introducing 
additional complexity and possible mistakes.
The P99 for requests made without caching should generally be less than one second. 
Even if we relax this requirement, it should not exceed 10 seconds. Instead of cache 
warming, we can ensure that requests served without caching have a reasonable P99.


	
107
Summary
4.13	 Further reading
This chapter uses material from Web Scalability for Startup Engineers by Artur Ejsmont 
(McGraw Hill, 2015).
4.13.1	 Caching references 
¡ Kevin Crawley “Scaling Microservices — Understanding and Implementing 
Cache,” August 22, 2019 (https://dzone.com/articles/scaling-microservices 
-understanding-and-implementi) 
¡ Rob Vettor, David Coulter, and Genevieve Warren “Caching in a cloud-native 
application,” Microsoft Docs, May 17, 2020 Microsoft Docs. (https://docs.microsoft.com/en-us/dotnet/architecture/cloud-native/azure-caching)
¡ Cloud Native Patterns by Cornelia Davis (Manning Publications, 2019)
¡ https://jakearchibald.com/2016/caching-best-practices/
¡ https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
¡ Tom Barker Intelligent Caching (O’Reilly Media, 2017)
Summary
¡ Designing a stateful service is much more complex and error-prone than a stateless service, so system designs try to keep services stateless, and use shared stateful 
services.
¡ Each storage technology falls into a particular category. We should know how to 
distinguish these categories, which are as follows.
–	 Database, which can be SQL or NoSQL. NoSQL can be categorized into column-oriented or key-value.
–	 Document.
–	 Graph.
–	 File storage.
–	 Block storage.
–	 Object storage. 
¡ Deciding how to store a service’s data involves deciding to use a database vs. 
another storage category.
¡ There are various replication techniques to scale databases, including single-leader replication, multi-leader replication, leaderless replication, and other 
techniques such as HDFS replication that do not fit cleanly into these three 
approaches.
¡ Sharding is needed if a database exceeds the storage capacity of a single host.


108
Chapter 4  Scaling databases
¡ Database writes are expensive and difficult to scale, so we should minimize database writes wherever possible. Aggregating events helps to reduce the rate of 
database writes.
¡ Lambda architecture involves using parallel batch and streaming pipelines to 
process the same data, and realize the benefits of both approaches while allowing 
them to compensate for each other’s disadvantages.
¡ Denormalizing is frequently used to optimize read latency and simpler SELECT 
queries, with tradeoffs like consistency, slower writes, more storage required, and 
slower index rebuilds.
¡ Caching frequent queries in memory reduces average query latency.
¡ Read strategies are for fast reads, trading off cache staleness.
¡ Cache-aside is best for read-heavy loads, but the cached data may become stale 
and cache misses are slower than if the cache wasn’t present.
¡ A read-through cache makes requests to the database, removing this burden 
from the application.
¡ A write-through cache is never stale, but it is slower.
¡ A write-back cache periodically flushes updated data to the database. Unlike 
other cache designs, it must have high availability to prevent possible data loss 
from outages.
¡ A write-around cache has slow writes and a higher chance of cache staleness. It is 
suitable for situations where the cached data is unlikely to change.
¡ A dedicated caching service can serve our users much better than caching on the 
memory of our services’ hosts.
¡ Do not cache private data. Cache public data; revalidation and cache expiry time 
depends on how often and likely the data will change.
¡ Cache invalidation strategies are different in services versus clients because we 
have access to the hosts in the former but not the latter.
¡ Warming a cache allows the first user of the cached data to be served as quickly as 
subsequent users, but cache warming has many disadvantages.


109
5
Distributed transactions
This chapter covers
¡ Creating data consistency across multiple 		
	 services
¡ Using event sourcing for scalability, availability, 	
	 lower cost, and consistency
¡ Writing a change to multiple services with 		
	 Change Data Capture (CDC) 
¡ Doing transactions with choreography vs. 	 	
	 orchestration
In a system, a unit of work may involve writing data to multiple services. Each write 
to each service is a separate request/event. Any write may fail; the causes may 
include bugs or host or network outages. This may cause data inconsistency across 
the services. For example, if a customer bought a tour package consisting of both an 
air ticket and a hotel room, the system may need to write to a ticket service, a room 
reservation service, and a payments service. If any write fails, the system will be in an 
inconsistent state. Another example is a messaging system that sends messages to 
recipients and logs to a database that messages have been sent. If a message is successfully sent to a recipient’s device, but the write to the database fails, it will appear 
that the message has not been delivered.


110
Chapter 5  Distributed transactions
A transaction is a way to group several reads and writes into a logical unit to maintain 
data consistency across services. They execute atomically, as a single operation, and the 
entire transaction either succeeds (commit) or fails (abort, rollback). A transaction has 
ACID properties, though the understanding of ACID concepts differs between databases, so the implementations also differ. 
If we can use an event-streaming platform like Kafka to distribute these writes, allowing downstream services to pull instead of push these writes, we should do so. (Refer 
to section 4.6.2 for a discussion of pull vs. push.) For other situations, we introduce the 
concept of a distributed transaction, which combines these separate write requests as a 
single distributed (atomic) transaction. We introduce the concept of consensus—that 
is, all the services agree that the write event has occurred (or not occurred). For consistency across the services, consensus should occur despite possible faults during write 
events. This section describes algorithms for maintaining consistency in distributed 
transactions: 
¡ The related concepts of event sourcing, Change Data Capture (CDC), and Event 
Driven Architecture (EDA). 
¡ Checkpointing and dead letter queue were discussed in sections 3.3.6 and 3.3.7.
¡ Saga.
¡ Two-phase commit. (This is outside the scope of this book. Refer to appendix D 
for a brief discussion on two-phase commit.) 
Two-phase commit and saga achieve consensus (all commit or all abort), while the 
other techniques are designed to designate a particular database as a source of truth 
should inconsistency result from failed writes. 
5.1	
Event Driven Architecture (EDA)
In Scalability for Startup Engineers (2015), Artur Ejsmont states, “Event Driven Architecture (EDA) is an architectural style where most interactions between different components are realized by announcing events that have already happened instead of 
requesting work to be done” (p. 295).
EDA is asynchronous and non-blocking. A request does not need to be processed, 
which may take considerable time and result in high latency. Rather, it only has to 
publish an event. If the event is successfully published, the server returns a successful 
response. The event can be processed afterwards. If necessary, the server can then send 
the response to the requestor. EDA promotes loose coupling, scalability, and responsiveness (low latency). 
The alternative to EDA is that a service makes a request directly to another service. 
Regardless of whether such a request was blocking or non-blocking, unavailability or 
slow performance of either service means that the overall system is unavailable. This 
request also consumes a thread in each service, so there is one less thread available 
during the time the request takes to process. This effect is especially noticeable if the 


	
111
Event sourcing 
request takes a long time to process or occurs during traffic spikes. A traffic spike can 
overwhelm the service and cause 504 timeouts. The requestors will also be affected 
because each requestor must continue to maintain a thread as long as the request has 
not completed, so the requestor device has fewer resources for other work.
To prevent traffic spikes from causing outages, we need to use complex auto-scaling 
solutions or maintain a large cluster of hosts, which incurs more expense. (Rate limiting is another possible solution and is discussed in chapter 8.)
These alternatives are more expensive, complex, error-prone, and less scalable. The 
strong consistency and low latency that they provide may not actually be needed by 
users.
A less resource-intensive approach is to publish an event onto an event log. The publisher service does not need to continuously consume a thread to wait for the subscriber 
service to finish processing an event. 
In practice, we may choose not to completely follow the non-blocking philosophy of 
EDA, such as by performing request validation when a request is made. For example, 
the server may validate that the request contains all required fields and valid values; a 
string field may need to be nonempty and not null; it may also have a minimum and 
maximum length. We may make this choice so that an invalid request can fail quickly, 
rather than waste resources and time persisting invalid data only to find an error afterwards. Event sourcing and Change Data Capture (CDC) are examples of EDA. 
5.2	
Event sourcing 
Event sourcing is a pattern for storing data or changes to data as events in an appendonly log. According to Davis (Cloud Native Patterns by Cornelia Davis (Manning Publications, 2019)), the idea of event sourcing is that the event log is the source of truth, 
and all other databases are projections of the event log. Any write must first be made to 
the event log. After this write succeeds, one or more event handlers consume this new 
event and writes it to the other databases.
Event sourcing is not tied to any particular data source. It can capture events from 
various sources, such as user interactions and external and internal systems. Referring to figure 5.1, event sourcing consists of publishing and persisting fine-grained, 
state-changing events of an entity as a sequence of events. These events are stored in a 
log, and subscribers process the log’s event to determine the entity’s current state. So, 
the publisher service asynchronously communicates with the subscriber service via the 
event log. 
Publisher
Subscriber
Log
Figure 5.1     In event sourcing, a publisher publishes a sequence of events to a log that indicates 
changes to the state of an entity. A subscriber processes the log events in sequence to determine the 
entity’s current state. 


112
Chapter 5  Distributed transactions
This can be implemented in various ways. A publisher can publish an event to an event 
store or append-only log such as a Kafka topic, write a row to a relational database 
(SQL), write a document to a document database like MongoDB or Couchbase, or 
even write to an in-memory database such as Redis or Apache Ignite for low latency. 
QUESTION    What if a subscriber host crashes while processing an event? How will 
the subscriber service know that it must process that event again? 
Event sourcing provides a complete audit trail of all events in the system, and the ability to derive insights into the system’s past states by replaying events for debugging or 
analytics. Event sourcing also allows business logic to change by introducing new event 
types and handlers without affecting existing data. 
Event sourcing adds complexity to system design and development because we must 
manage event stores, replay, versioning, and schema evolution. It increases storage 
requirements. Event replay becomes more costly and time-consuming as the logs grow.
5.3	
Change Data Capture (CDC)
Change Data Capture (CDC) is about logging data change events to a change log event 
stream and providing this event stream through an API. 
Figure 5.2 illustrates CDC. A single change or group of changes can be published as 
a single event to a change log event stream. This event stream has multiple consumers, 
each corresponding to a service/application/database. Each consumer consumes the 
event and provides it to its downstream service to be processed. 
Event stream
Application
Downstream 
application 1
Downstream 
application 2
Database 
1
Database 
2
Consumer
Consumer
Consumer
Consumer
Figure 5.2    Using a change log event stream to synchronize data changes. Besides consumers, 
serverless functions can also be used to propagate changes to downstream applications or databases. 


	
113
Comparison of event sourcing and CDC
CDC ensures consistency and lower latency than event sourcing. Each request is processed in near real time, unlike in event sourcing where a request can stay in the log for 
some time before a subscriber processes it.
The transaction log tailing pattern (Chris Richardson, Microservices Patterns: With 
Examples in Java, pp. 99–100, Manning Publications, 2019) is another system design pattern to prevent possible inconsistency when a process needs to write to a database and 
produce to Kafka. One of the two writes may fail, causing inconsistency. 
Figure 5.3 illustrates the transaction log tailing pattern. In transaction log tailing, a 
process called the transaction log miner tails a database’s transaction log and produces 
each update as an event.  
Transaction Log 
Miner
Log file
Message broker
Database client
Database
Figure 5.3    Illustration of the transaction log tailing pattern. A service does a write query to a database, 
which records this query in its log file. The transaction log miner tails the log file and picks up this query, 
then produces an event to the message broker.
CDC platforms include Debezium (https://debezium.io/), Databus (https://github 
.com/linkedin/databus), DynamoDB Streams (https://docs.aws.amazon.com/ 
amazondynamodb/latest/developerguide/Streams.html), and Eventuate CDC Service (https://github.com/eventuate-foundation/eventuate-cdc). They can be used as 
transaction log miners. 
Transaction log miners may generate duplicate events. One way to handle duplicate 
events is to use the message broker’s mechanisms for exactly-once delivery. Another way 
is for the events to be defined and processed idempotently.
5.4	
Comparison of event sourcing and CDC
Event-driven architecture (EDA), event sourcing, and CDC are related concepts used 
in distributed systems that to propagate data changes to interested consumers and 
downstream services. They decouple services by using asynchronous communication patterns to communicate these data changes. In some system designs, you might 
use both event sourcing and CDC together. For example, you can use event sourcing 
within a service to record data changes as events, while using CDC to propagate those 
events to other services. They differ in some of their purposes, in their granularity, and 
in their sources of truth. These differences are discussed in table 5.1. 


114
Chapter 5  Distributed transactions
Table 5.1    Differences between event sourcing and Change Data Capture (CDC) 
Event Sourcing
Change Data Capture (CDC)
Purpose
Record events as the source of truth.
Synchronize data changes by propagating 
events from a source service to downstream 
services. 
Source of truth
The log, or events published to the 
log, are the source of truth.
A database in the publisher service. The published events are not the source of truth.
Granularity
Fine-grained events that represent 
specific actions or changes in state. 
Individual database level changes such as 
new, updated, or deleted rows or documents. 
5.5	
Transaction supervisor
A transaction supervisor is a process that ensures a transaction is successfully completed or is compensated. It can be implemented as a periodic batch job or serverless 
function. Figure 5.4 shows an example of a transaction supervisor.
Application 1
Application 2
Transaction 
Supervisor
Database
Application
Figure 5.4    Example illustration of a transaction supervisor. An application may write to multiple 
downstream applications and databases. A transaction supervisor periodically syncs the various 
destinations in case any writes fail.
A transaction supervisor should generally be first implemented as an interface for manual review of inconsistencies and manual executions of compensating transactions. 
Automating compensating transactions is generally risky and should be approached 
with caution. Before automating a compensating transaction, it must first be extensively tested. Also ensure that there are no other distributed transaction mechanisms, 
or they may interfere with each other, leading to data loss or situations that are difficult 
to debug.
A compensating transaction must always be logged, regardless of whether it was manually or automatically run. 


	
115
Saga
5.6	
Saga
A saga is a long-lived transaction that can be written as a sequence of transactions. All 
transactions must complete successfully, or compensating transactions are run to roll 
back the executed transactions. A saga is a pattern to help manage failures. A saga itself 
has no state. 
A typical saga implementation involves services communicating via a message broker 
like Kafka or RabbitMQ. In our discussions in this book that involve saga, we will use 
Kafka. 
An important use case of sagas is to carry out a distributed transaction only if certain 
services satisfy certain requirements. For example, in booking a tour package, a travel 
service may make a write request to an airline ticket service, and another write request 
to a hotel room service. If there are either no available flights or hotel rooms, the entire 
saga should be rolled back.
The airline ticket service and hotel room service may also need to write to a payments 
service, which is separate from the airline ticket service and hotel service for possible 
reasons including the following: 
¡ The payment service should not process any payments until the airline ticket 
service confirms that the ticket is available, and the hotel room service confirms 
that the room is available. Otherwise, it may collect money from the user before 
confirming the entire tour package. 
¡ The airline ticket and hotel room services may belong to other companies, and 
we cannot pass the user’s private payment information to them. Rather, our company needs to handle the user’s payment, and our company should make payments to other companies. 
If a transaction to the payments service fails, the entire saga should be rolled back in 
reverse order using compensating transactions on the other two services. 
There are two ways to structure the coordination: choreography (parallel) or orchestration (linear). In the rest of this section, we discuss one example of choreography and 
one example of orchestration, then compare choreography vs. orchestration. Refer to 
https://microservices.io/patterns/data/saga.html for another example.
5.6.1	
Choreography
In choreography, the service that begins the saga communicates with two Kafka topics. 
It produces to one Kafka topic to start the distributed transaction and consumes from 
another Kafka topic to perform any final logic. Other services in the saga communicate directly with each other via Kafka topics. 
Figure 5.5 illustrates a choreography saga to book a tour package. In this chapter, the 
figures that include Kafka topics illustrate event consumption with the line arrowheads 
pointing away from the topic. In the other chapters of this book, an event consumption is illustrated with the line arrowhead pointing to the topic. The reason for this 
difference is that the diagrams in this chapter may be confusing if we follow the same 


116
Chapter 5  Distributed transactions
convention as the other chapters. The diagrams in this chapter illustrate multiple services consuming from multiple certain topics and producing to multiple other topics, 
and it is clearer to display the arrowhead directions in the manner that we chose. 
Booking Service
Booking Topic
Ticket Service
Hotel Service
Ticket Topic
Hotel Topic
Payment Service
Payment Topic
1
2a
2b
3a
3b
4a
4b
5
6a
6b
6c
Figure 5.5    A choreography saga to book an airline ticket and a hotel room for a tour package. Two 
labels with the same number but different letters represent steps that occur in parallel. 
The steps of a successful booking are as follows: 
1	 A user may make a booking request to the booking service. The booking service 
produces a booking request event to the booking topic.
2	 The ticket service and hotel service consume this booking request event. They 
both confirm that their requests can be fulfilled. Both services may record 
this event in their respective databases, with the booking ID and a state like 
“AWAITING_PAYMENT”.
3	 The ticket service and hotel service each produce a payment request event to the 
ticket topic and hotel topic, respectively.
4	 The payment service consumes these payment request events from the ticket 
topic and hotel topic. Because these two events are consumed at different times 
and likely by different hosts, the payment service needs to record the receipt of 
these events in a database, so the service’s hosts will know when all the required 
events have been received. When all required events are received, the payment 
service will process the payment.
5	 If the payment is successful, the payment service produces a payment success 
event to the payment topic.
6	 The ticket service, hotel service, and booking service consume this event. The 
ticket service and hotel service both confirm this booking, which may involve 
changing the state of that booking ID to CONFIRMED, or other processing and 
business logic as necessary. The booking service may inform the user that the 
booking is confirmed. 


	
117
Saga
Steps 1–4 are compensable transactions, which can be rolled back by compensating 
transactions. Step 5 is a pivot transaction. Transactions after the pivot transaction can 
be retried until they succeed. The step 6 transactions are retriable transactions; this is 
an example of CDC as discussed in section 5.3. The booking service doesn’t need to 
wait for any responses from the ticket service or the hotel service. 
A question that may be asked is how does an external company subscribe to our 
company’s Kafka topics? The answer is that it doesn’t. For security reasons, we never 
allow direct external access to our Kafka service. We have simplified the details of this 
discussion for clarity. The ticket service and hotel service actually belong to our company. They communicate directly with our Kafka service/topics and make requests to 
external services. Figure 5.5 did not illustrate these details, so they don’t clutter the 
design diagram. 
If the payment service responds with an error that the ticket cannot be reserved 
(maybe because the requested flight is fully booked or canceled), step 6 will be different. Rather than confirming the booking, the ticket service and hotel service will cancel 
the booking, and the booking service may return an appropriate error response to the 
user. Compensating transactions made by error responses from the hotel service or payment service will be similar to the described situation, so we will not discuss them. Other 
points to note in choreography: 
¡ There are no bidirectional lines; that is, a service does not both produce to and 
subscribe to the same topic. 
¡ No two services produce to the same topic. 
¡ A service can subscribe to multiple topics. If a service needs to receive multiple 
events from multiple topics before it can perform an action, it needs to record in 
a database that it has received certain events, so it can read the database to determine if all the required events have been received. 
¡ The relationship between topics and services can be 1:many or many:1, but not 
many:many. 
¡ There may be cycles. Notice the cycle in figure 5.5 (hotel topic > payment service 
> payment topic > hotel service > hotel topic). 
In figure 5.5, there are many lines between multiple topics and services. Choreography 
between a larger number of topics and services can become overly complex, errorprone, and difficult to maintain. 
5.6.2	
Orchestration 
In orchestration, the service that begins the saga is the orchestrator. The orchestrator 
communicates with each service via a Kafka topic. In each step in the saga, the orchestrator must produce to a topic to request this step to begin, and it must consume from 
another topic to receive the step’s result. 
An orchestrator is a finite-state machine that reacts to events and issues commands. 
The orchestrator must only contain the sequence of steps. It must not contain any other 
business logic, except for the compensation mechanism. 


118
Chapter 5  Distributed transactions
Figure 5.6 illustrates an orchestration saga to book a tour package. The steps in a 
successful booking process are as shown. 
Booking Topic
Ticket Service
Hotel Service
Response Topic
Hotel Topic
Payment Service
Payment Topic
Booking Service 
Orchestrator
1, 13
2, 14
3, 15
5, 17
6, 18
7, 19
9
10
11
4, 8, 12, 16, 20
Figure 5.6    An orchestration saga to book an airline ticket and a hotel room for a tour package 
1	 The orchestrator produces a ticket request event to the booking topic. 
2	 The ticket service consumes this ticket request event and reserves the airline 
ticket for the booking ID with the state “AWAITING_PAYMENT”. 
3	 The ticket service produces a “ticket pending payment” event to the response 
topic.
4	 The orchestrator consumes the “ticket pending payment” event. 
5	 The orchestrator produces a hotel reservation request event to the hotel topic. 
6	 The hotel service consumes the hotel reservation request event and reserves the 
hotel room for the booking ID with the state “AWAITING_PAYMENT”. 
7	 The hotel service produces a “room pending payment” event to the response 
topic. 
8	 The orchestrator consumes the “room pending payment” event. 
9	 The orchestrator produces a payment request event to the payment topic. 
10	 The payment service consumes the payment request event. 
11	 The payment service processes the payment and then produces a payment confirmation event to the response topic. 
12	 The orchestrator consumes the payment confirmation event. 
13	 The orchestrator produces a payment confirmation event to the booking topic. 
14	 The ticket service consumes the payment confirmation event and changes the 
state corresponding to that booking to “CONFIRMED”. 
15	 The ticket service produces a ticket confirmation event to the response topic. 
16	 The orchestrator consumes this ticket confirmation event from response topic. 


	
119
Saga
17	 The orchestrator produces a payment confirmation event to the hotel topic. 
18	 The hotel service consumes this payment confirmation event and changes the 
state corresponding to that booking to “CONFIRMED”. 
19	 The hotel service produces a hotel room confirmation event to the response 
topic. 
20	 The booking service orchestrator consumes the hotel room confirmation event. 
It can then perform next steps, such as sending a success response to the user, or 
any further logic internal to the booking service. 
Steps 18 and 19 appear unnecessary, as step 18 will not fail; it can keep retrying until 
it succeeds. Steps 18 and 20 can be done in parallel. However, we carry out these steps 
linearly to keep the approach consistent. 
Steps 1–13 are compensable transactions. Step 14 is the pivot transaction. Steps 15 
onward are retriable transactions. 
If any of the three services produces an error response to the booking topic, the 
orchestrator can produce events to the various other services to run compensating 
transactions. 
5.6.3	
Comparison 
Table 5.1 compares choreography vs. orchestration. We should understand their differences and tradeoffs to evaluate which approach to use in a particular system design. 
The final decision may be partly arbitrary, but by understanding their differences, we 
also understand what we are trading off by choosing one approach over another.
Table 5.1    Choreography saga vs. orchestration saga
Choreography
Orchestration
Requests to services are made in parallel. This is 
the observer object-oriented design pattern.
Requests to services are made linearly. This is the 
controller object-oriented design pattern. 
The service that begins the saga communicates 
with two Kafka topics. It produces one Kafka topic 
to start the distributed transaction and consumes 
from another Kafka topic to perform any final logic.
The orchestrator communicates with each service 
via a Kafka topic. In each step in the saga, the 
orchestrator must produce to a topic to request this 
step to begin, and it must consume from another 
topic to receive the step’s result.
The service that begins the saga only has code that 
produces to the saga’s first topic and consumes 
from the saga’s last topic. A developer must read 
the code of every service involved in the saga to 
understand its steps. 
The orchestrator has code that produces and consumes Kafka topics that correspond to steps in the 
saga, so reading the orchestrator’s code allows one 
to understand the services and steps in the distributed transaction.
A service may need to subscribe to multiple Kafka 
topics, such as the Accounting Service in figure 
5.5 of Richardson’s book. This is because it may 
produce a certain event only when it has consumed 
certain other events from multiple services. This 
means that it must record in a database which 
events it has already consumed.
Other than the orchestrator, each service only 
subscribes to one other Kafka topic (from one 
other service). The relationships between the 
various services are easier to understand. Unlike 
choreography, a service never needs to consume 
multiple events from separate services before it 
can produce a certain event, so it may be possible 
to reduce the number of database writes.


120
Chapter 5  Distributed transactions
Choreography
Orchestration
Less resource-intensive, less chatty, and less network traffic; hence, it has lower latency overall.
Since every step must pass through the orchestrator, the number of events is double that of choreography. The overall effect is that orchestration is 
more resource-intensive, chattier, and has more 
network traffic; hence, it has higher latency overall.
Parallel requests also result in lower latency.
Requests are linear, so latency is higher.
Services have a less independent software development lifecycle because developers must understand all services to change any one of them.
Services are more independent. A change to a 
service only affects the orchestrator and does not 
affect other services.
No such single point of failure as in orchestration 
(i.e., no service needs to be highly available except 
the Kafka service).
If the orchestration service fails, the entire saga 
cannot execute (i.e., the orchestrator and the Kafka 
service must be highly available).
Compensating transactions are triggered by the 
various services involved in the saga.
Compensating transactions are triggered by the 
orchestrator.
5.7	
Other transaction types
The following consensus algorithms are typically more useful for achieving consensus for a large number of nodes, typically in distributed databases. We will not discuss 
them in this book. Refer to Designing Data-Intensive Applications by Martin Kleppman for 
more details.
¡ Quorum writes
¡ Paxos and EPaxos 
¡ Raft 
¡ Zab (ZooKeeper atomic broadcast protocol) – Used by Apache ZooKeeper.
5.8	
Further reading 
¡ Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and 
Maintainable Systems by Martin Kleppmann (O'Reilly Media, 2017)
¡ Cloud Native: Using Containers, Functions, and Data to Build Next-Generation Applications by Boris Scholl, Trent Swanson, and Peter Jausovec (O’Reilly Media, 2019) 
¡ Cloud Native Patterns by Cornelia Davis (Manning Publications, 2019)
¡ Microservices Patterns: With Examples in Java by Chris Richardson (Manning Publications, 2019). Chapter 3.3.7 discusses the transaction log tailing pattern. Chapter 4 is a detailed chapter on saga.


	
121
Summary
Summary
¡ A distributed transaction writes the same data to multiple services, with either 
eventual consistency or consensus.
¡ In event sourcing, write events are stored in a log, which is the source of truth and 
an audit trail that can replay events to reconstruct the system state.
¡ In Change Data Capture (CDC), an event stream has multiple consumers, each 
corresponding to a downstream service.
¡ A saga is a series of transactions that are either all completed successfully or are 
all rolled back.
¡ Choreography (parallel) or orchestration (linear) are two ways to coordinate 
sagas. 


122
6
Common services for 
functional partitioning
This chapter covers
¡ Centralizing cross-cutting concerns with API 	
	 gateway or service mesh/sidecar
¡ Minimizing network traffic with a metadata 	
	 service
¡ Considering web and mobile frameworks to 	
	 fulfill requirements
¡ Implementing functionality as libraries vs. 		
	 services
¡ Selecting an appropriate API paradigm between 	
	 REST, RPC, and GraphQL
Earlier in this book, we discussed functional partitioning as a scalability technique 
that partitions out specific functions from our backend to run on their own dedicated clusters. This chapter first discusses the API gateway, followed by the sidecar 
pattern (also called service mesh), which was a recent innovation. Next, we discuss 
centralization of common data into a metadata service. A common theme of these 
services is that they contain functionalities common to many backend services, 
which we can partition from those services into shared common services. 
NOTE    Istio, a popular service mesh implementation, had its first production 
release in 2018.


	
123
Common functionalities of various services
Last, we discuss frameworks that can be used to develop the various components in a 
system design. 
6.1	
Common functionalities of various services
A service can have many non-functional requirements, and many services with different functional requirements can share the same non-functional requirements. For 
example, a service that calculates sales taxes and a service to check hotel room availability may both take advantage of caching to improve performance or only accept 
requests from registered users.
If engineers implement these functionalities separately for each service, there 
may be duplication of work or duplicate code. Errors or inefficiencies are more likely 
because scarce engineering resources are spread out across a larger amount of work. 
One possible solution is to place this code into libraries where various services can 
use them. However, this solution has the disadvantages discussed in section 6.7. Library 
updates are controlled by users, so the services may continue to run old versions that 
contain bugs or security problems fixed in newer versions. Each host running the service also runs the libraries, so the different functionalities cannot be independently 
scaled.
A solution is to centralize these cross-cutting concerns with an API gateway. An API 
gateway is a lightweight web service that consists of stateless machines located across 
several data centers. It provides common functionalities to our organization’s many 
services for centralization of cross-cutting concerns across various services, even if they 
are written in different programming languages. It should be kept as simple as possible despite its many responsibilities. Amazon API Gateway (https://aws.amazon.com/
api-gateway/) and Kong (https://konghq.com/kong) are examples of cloud-provided 
API gateways.
The functionalities of an API gateway include the following, which can be grouped 
into categories. 
6.1.1	
Security
These functionalities prevent unauthorized access to a service’s data:
¡ Authentication: Verifies that a request is from an authorized user. 
¡ Authorization: Verifies that a user is allowed to make this request. 
¡ SSL termination: Termination is usually not handled by the API gateway itself but 
by a separate HTTP proxy that runs as a process on the same host. We do termination on the API gateway because termination on a load balancer is expensive. 
Although the term “SSL termination” is commonly used, the actual protocol is 
TLS, which is the successor to SSL. 
¡ Server-side data encryption: If we need to store data securely on backend hosts or 
on a database, the API gateway can encrypt data before storage and decrypt data 
before it is sent to a requestor. 


124
Chapter 6  Common services for functional partitioning
6.1.2	
Error-checking
Error-checking prevents invalid or duplicate requests from reaching service hosts, 
allowing them to process only valid requests:
¡ Request validation: One validation step is to ensure the request is properly formatted. For example, a POST request body should be valid JSON. It ensures that 
all required parameters are present in the request and their values honor constraints. We can configure these requirements on our service on our API gateway.
¡ Request deduplication: Duplication may occur when a response with success status 
fails to reach the requestor/client because the requestor/client may reattempt 
this request. Caching is usually used to store previously seen request IDs to avoid 
duplication. If our service is idempotent, stateless, or “at least once” delivery, it 
can handle duplicate requests, and request duplication will not cause errors. 
However, if our service expects “exactly once” or “at most once” delivery, request 
duplication may cause errors.
6.1.3	
Performance and availability
An API gateway can improve the performance and availability of services by providing 
caching, rate limiting, and request dispatching. 
¡ Caching: The API gateway can cache common requests to the database or other 
services such as: 
–	 In our service architecture, the API gateway may make requests to a metadata 
service (refer to section 6.3). It can cache information on the most actively 
used entities. 
–	 Use identity information to save calls to authentication and authorization 
services. 
¡ Rate Limiting (also called throttling): Prevents our service from being overwhelmed 
by requests. (Refer to chapter 8 for a discussion on a sample rate-limiting service.) 
¡ Request dispatching: The API gateway makes remote calls to other services. It creates HTTP clients for these various services and ensures that requests to these 
services are properly isolated. When one service experiences slowdown, requests 
to other services are not affected. Common patterns like bulkhead and circuit 
breaker help implement resource isolation and make services more resilient 
when remote calls fail. 
6.1.4	
Logging and analytics
Another common functionality provided by an API gateway is request logging or usage 
data collection, which is the gathering real-time information for various purposes such 
as analytics, auditing, billing, and debugging. 


	
125
Service mesh/sidecar pattern 
6.2	
Service mesh/sidecar pattern 
Section 1.4.6 briefly discussed using a service mesh to address the disadvantages of an 
API gateway, repeated here:
¡ Additional latency in each request, from having to route the request through an 
additional service.
¡ A large cluster of hosts, which requires scaling to control costs.
Figure 6.1 is a repeat of figure 1.8, illustrating a service mesh. A slight disadvantage of 
this design is that a service’s host will be unavailable if its sidecar is unavailable, even if 
the service is up; this is the reason we generally do not run multiple services or containers on a single host. 
Service 1 host
Certificate 
authority
Identity and access 
management
Configure proxies
Interface with 
external services
Control plane
Envoy proxy 
host (sidecar)
Pod
Service 1 host
Envoy proxy 
host (sidecar)
Pod
Service 1 host
Envoy proxy 
host (sidecar)
Pod
Service clients
ELK
Data Plane
Distributed tracing
(Zipkin/Jaeger
/OpenTracing)
Prometheus
Observability Plane
Mesh traffic
Management traffic
Operational traffic
Rate limiting 
rules
Auditor
Administrator
Figure 6.1    Illustration of a service mesh, repeated from figure 1.8


126
Chapter 6  Common services for functional partitioning
Istio’s documentation states that a service mesh consists of a control plane and a data 
plane (https://istio.io/latest/docs/ops/deployment/architecture/), while Jenn Gile 
from Nginx also described an observability plane (https://www.nginx.com/blog/ 
how-to-choose-a-service-mesh/). Figure 6.1 contains all three types of planes. 
An administrator can use the control plane to manage proxies and interface with 
external services. For example, the control plane can connect to a certificate authority to 
obtain a certificate, or to an identity and access control service to manage certain configurations. It can also push the certificate ID or the identify and access control service configurations to the proxy hosts. Interservice and intraservice requests occur between the 
Envoy (https://www.envoyproxy.io/) proxy hosts, which we refer to as mesh traffic. Sidecar proxy interservice communication can use various protocols including HTTP and 
gRPC (https://docs.microsoft.com/en-us/dotnet/architecture/cloud-native/service 
-mesh-communication-infrastructure). The observability plane provides logging, monitoring, alerting, and auditing. 
Rate limiting is another example of a common shared service that can be managed 
by a service mesh. Chapter 8 discusses this in more detail. AWS App Mesh (https://aws 
.amazon.com/app-mesh) is a cloud-provided service mesh.
NOTE    Refer to section 1.4.6 for a brief discussion on sidecarless service mesh. 
6.3	
Metadata service 
A metadata service stores information that is used by multiple components within a 
system. If these components pass this information between each other, they can pass 
IDs rather than all the information. A component that receives an ID can request the 
metadata service for the information that corresponds to that ID. There is less duplicate information in the system, analogous to SQL normalization, so there is better 
consistency.
One example is ETL pipelines. Consider an ETL pipeline for sending welcome 
emails for certain products that users have signed up for. The email message may be 
an HTML file of several MB that contains many words and images, which are different 
according to product. Referring to figure 6.2, when a producer produces a message 
to the pipeline queue, instead of including an entire HTML file in the message, the 
producer can only include the ID of the file. The file can be stored in a metadata service. When a consumer consumes a message, it can request the metadata service for the 
HTML file that corresponds to that ID. This approach saves the queue from containing 
large amounts of duplicate data. 
Metadata Service
Queue
Producer
Consumer
Figure 6.2    We can use a 
metadata service to reduce 
the size of individual messages 
in a queue, by placing large 
objects in the metadata 
service, and enqueuing only 
IDs in individual messages. 


	
127
Service discovery
A tradeoff of using a metadata service is increased complexity and overall latency. 
Now the producer must write both to the Metadata Service and the queue. In certain 
designs, we may populate the metadata service in an earlier step, so the producer does 
not need to write to the metadata service.
If the producer cluster experiences traffic spikes, it will make a high rate of read 
requests to the metadata service, so the metadata service should be capable of supporting high read volumes. 
In summary, a metadata service is for ID lookups. We will use metadata services in 
many of our sample question discussions in part 2.
Figure 6.3 illustrates the architecture changes from introducing the API gateway and 
metadata services. Instead of making requests to the backend, clients will make requests 
to the API gateway, which performs some functions and may send requests to either the 
metadata service and/or the backend. Figure 1.8 illustrates a service mesh.
Client
API Gateway
Service 1
Service 2
Service 3
Metadata Service
Client
Service
Figure 6.3    Functional partitioning of a service (top) to separate out the API gateway and metadata 
service (bottom). Before this partitioning, clients query the service directly. With the partitioning, clients 
query the API gateway, which performs some functions and may route the request to one of the services, 
which in turn may query the metadata service for certain shared functionalities. 
6.4	
Service discovery
Service discovery is a microservices concept that might be briefly mentioned during an 
interview in the context of managing multiple services. Service discovery is done under 
the hood, and most engineers do not need to understand their details. Most engineers 
only need to understand that each internal API service is typically assigned a port number via which it is accessed. External API services and most UI services are assigned 
URLs through which they are accessed. Service discovery may be covered in interviews 
for teams that develop infrastructure. It is unlikely that the details of service discovery 
will be discussed for other engineers because it provides little relevant interview signal. 


128
Chapter 6  Common services for functional partitioning
Very briefly, service discovery is a way for clients to identify which service hosts are 
available. A service registry is a database that keeps track of the available hosts of a 
service. Refer to sources such as https://docs.aws.amazon.com/whitepapers/latest/
microservices-on-aws/service-discovery.html for details on service registries in Kubernetes and AWS. Refer to https://microservices.io/patterns/client-side-discovery.html 
and https://microservices.io/patterns/server-side-discovery.html for details on client-side discovery and server-side discovery.
6.5	
Functional partitioning and various frameworks
In this section, we discuss some of the countless frameworks that can be used to develop 
the various components in a system design diagram. New frameworks are continuously 
being developed, and various frameworks fall in and out of favor with the industry. The 
sheer number of frameworks can be confusing to a beginner. Moreover, certain frameworks can be used for more than one component, making the overall picture even 
more confusing. This section is a broad discussion of various frameworks, including 
¡ Web 
¡ Mobile, including Android and iOS 
¡ Backend 
¡ PC 
The universe of languages and frameworks is far bigger than can be covered in this section, and it is not the aim of this section to discuss them all. The purpose of this section 
is to provide some awareness of several frameworks and languages. By the end of this 
section, you should be able to read more easily the documentation of a framework to 
understand its purposes and where it fits into a system design.
6.5.1	
Basic system design of an app
Figure 1.1 introduced a basic system design of an app. In almost all cases today, a company that develops a mobile app that makes requests to a backend service will have an 
iOS app on the iOS app store and an Android app on the Google Play store. It may also 
develop a browser app that has the same features as the mobile apps or maybe a simple 
page that directs users to download the mobile apps. There are many variations. For 
example, a company may also develop a PC app. But attempting to explain every possible combination is counterproductive, and we will not do so. 
We will start with discussing the following questions regarding figure 1.1, then 
expand our discussion to various frameworks and their languages: 
¡ Why is there a separate web server application from the backend and browser 
app? 
¡ Why does the browser app make requests to this Node.js app, which then makes 
requests to the backend that is shared with the Android and iOS apps?


	
129
Functional partitioning and various frameworks
6.5.2	
Purposes of a web server app
The purposes of a web server app include the following: 
¡ When someone using a web browser accesses the URL (e.g., https://google 
.com/), the browser downloads the browser app from the Node.js app. As stated 
in section 1.4.1, the browser app should preferably be small so it can be downloaded quickly. 
¡ When the browser makes a specific URL request (e.g., with a specific path like 
https://google.com/about), Node.js handles the routing of the URL and serves 
the corresponding page. 
¡ The URL may include certain path and query parameters that require specific 
backend requests. The Node.js app processes the URL and makes the appropriate backend requests. 
¡ Certain user actions on the browser app, such as filling and submitting forms or 
clicking on buttons, may require backend requests. A single action may correspond to multiple backend requests, so the Node.js app exposes its own API to 
the browser app. Referring to figure 6.4, for each user action, the browser app 
makes an API request to the Node.js app/server, which then makes one or more 
appropriate backend requests and returns the requested data. 
Browser
node.js
server
Web Service 0
Web Service 1
Web Service N
Figure 6.4    A Node.js server can serve a request from a browser by making appropriate requests to one 
or more web services, aggregate and process their responses, and return the appropriate response to the 
browser. 
Why doesn’t a browser make requests directly to the backend? If the backend was a 
REST app, its API endpoints may not return the exact data required by the browser. 
The browser may have to make multiple API requests and fetch more data than 
required. This data transmission occurs over the internet, between a user’s device and 
a data center, which is inefficient. It is more efficient for the Node.js app to make these 


130
Chapter 6  Common services for functional partitioning
large requests because the data transmission will likely happen between adjacent hosts 
in the same data center. The Node.js app can then return the exact data required by 
the browser. 
GraphQL apps allow users to request the exact data required, but securing GraphQL 
endpoints is more work than a REST app, causing more development time and possible 
security breaches. Other disadvantages include the following. Refer to section 6.7.4 for 
more discussion on GraphQL: 
¡ Flexible queries mean that more work is required to optimize performance. 
¡ More code on the client. 
¡ More work needed to define the schema. 
¡ Larger requests. 
6.5.3	
Web and mobile frameworks 
This section contains a list of frameworks, classified into the following: 
¡ Web/browser app development
¡ Mobile app development 
¡ Backend app development 
¡ PC aka desktop app development (i.e., for Windows, Mac, and Linux)
A complete list will be very long, include many frameworks that one will be unlikely to 
encounter or even read about during their career, and in the author’s opinion, will not 
be useful to the reader. This list only states some of the frameworks that are prominent 
or used to be prominent. 
The flexibility of these spaces makes a complete and objective discussion difficult. 
Frameworks and languages are developed in countless ways, some of which make sense 
and others which do not. 
Browser app development 
Browsers accept only HTML, CSS, and JavaScript, so browser apps must be in these languages for backward compatibility. A browser is installed on a user’s device, so it must 
be upgraded by the user themselves, and it is difficult and impractical to persuade 
or force users to download a browser that accepts another language. It is possible to 
develop a browser app in vanilla JavaScript (i.e., without any frameworks), but this is 
impractical for all but the smallest browser apps because frameworks contain many 
functions that one will otherwise have to reimplement in vanilla JavaScript (e.g., animation or data rendering like sorting tables or drawing charts). 
Although browser apps must be in these three languages, a framework can offer 
other languages. The browser app code written in these languages is transpiled to 
HTML, CSS, and JavaScript. 
The most popular browser app frameworks include React, Vue.js, and Angular. 
Other frameworks include Meteor, jQuery, Ember.js, and Backbone.js. A common 
theme of these frameworks is that developers mix the markup and logic in the same 


	
131
Functional partitioning and various frameworks
files, rather than having separate HTML files for markup and JavaScript files for logic. 
These frameworks may also contain their own languages for markup and logic. For 
example, React introduced JSX, which is an HTML-like markup language. A JSX file 
can include both markup and JavaScript functions and classes. Vue.js has the template 
tag, which is similar to HTML. 
Some of the more prominent web development languages (which are transpiled to 
JavaScript) include the following: 
¡ TypeScript (https://www.typescriptlang.org/) is a statically typed language. It is 
a wrapper/superset around JavaScript. Virtually any JavaScript framework can 
also use TypeScript, with some setup work. 
¡ Elm (https://elm-lang.org/) can be directly transpiled to HTML, CSS, and 
JavaScript, or it can also be used within other frameworks like React. 
¡ PureScript (https://www.purescript.org/) aims for a similar syntax as Haskell. 
¡ Reason (https://reasonml.github.io/). 
¡ ReScript (https://rescript-lang.org/). 
¡ Clojure (https://clojure.org/) is a general-purpose language. The ClojureScript 
(https://clojurescript.org/) framework transpiles to Clojure to JavaScript. 
¡ CoffeeScript (https://coffeescript.org/). 
These browser app frameworks are for the browser/client side. Here are some server-side frameworks. Any server-side framework can also make requests to databases and 
be used for backend development. In practice, a company often chooses one framework for server development and another framework for backend development. This 
is a common point of confusion for beginners trying to distinguish between “server-side frontend” frameworks and “backend” frameworks. There is no strict division 
between them. 
¡ Express (https://expressjs.com/) is a Node.js (https://nodejs.org/) server 
framework. Node.js is a JavaScript runtime environment built on Chrome’s V8 
JavaScript engine. The V8 JavaScript engine was originally built for Chrome, but 
it can also run on an operating system like Linux or Windows. The purpose of 
Node.js is for JavaScript code to run on an operating system. Most frontend or 
full-stack job postings that state Node.js as a requirement are actually referring 
to Express. 
¡ Deno (https://deno.land/) supports JavaScript and TypeScript. It was created by 
Ryan Dahl, the original creator of Node.js, to address his regrets about Node.js. 
¡ Goji (https://goji.io/) is a Golang framework. 
¡ Rocket (https://rocket.rs/) is a Rust framework. Refer to https://blog.logrocket 
.com/the-current-state-of-rust-web-frameworks/ for more examples of Rust web 
server and backend frameworks. 
¡ Vapor (https://vapor.codes/) is a framework for the Swift language. 


132
Chapter 6  Common services for functional partitioning
¡ Vert.x (https://vertx.io/) offers development in Java, Groovy, and Kotlin. 
¡ PHP (https://www.php.net/). (There is no universal agreement on whether 
PHP is a language or a framework. The author’s opinion is that there is no practical value in debating this semantic.) A common solution stack is the LAMP 
(Linux, Apache, MySQL, PHP/Perl/Python) acronym. PHP code can be run on 
an Apache (https://httpd.apache.org/) server, which in turn runs on a Linux 
host. PHP was popular before ~2010 (https://www.tiobe.com/tiobe-index/ 
php/), but in the author’s experience, PHP code is seldom directly used for 
new projects. PHP remains prominent for web development via the Word-
Press platform, which is useful for building simple websites. More sophisticated 
user interfaces and customizations are more easily done by web developers, 
using frameworks that require considerable coding, such as React and Vue.js. 
Meta (formerly known as Facebook) was a prominent PHP user. The Facebook 
browser app was formerly developed in PHP. In 2014, Facebook introduced the 
Hack language (https://hacklang.org/) and HipHop Virtual Machine (HHVM) 
(https://hhvm.com/). Hack is a PHP-like language that does not suffer from 
the bad security and performance of PHP. It runs on HVVM. Meta is an extensive 
user of Hack and HHVM. 
Mobile app development 
The dominant mobile operating systems are Android and iOS, developed by Google 
and Apple, respectively. Google and Apple each offer their own Android or iOS app 
development platform, which are commonly referred to as “native” platforms. The 
native Android development languages are Kotlin and Java, while the native iOS development languages are Swift and Objective-C. 
Cross-platform development 
Cross-platform development frameworks in theory reduce duplicate work by running the same code on multiple platforms. In practice, there may be additional code 
required to code the app for each platform, which will negate some of this benefit. 
Such situations occur when the UI (user interface) components provided by operating systems are too different from each other. Frameworks which are cross-platform 
between Android and iOS include the following: 
¡ React Native is distinct from React. The latter is for web development only. There 
is also a framework called React Native for Web (https://github.com/necolas/
react-native-web), which allows web development using React Native. 
¡ Flutter (https://flutter.dev/) is cross-platform across Android, iOS, web, and PC. 
¡ Ionic (https://ionicframework.com/) is cross-platform across Android, iOS, 
web, and PC. 
¡ Xamarin (https://dotnet.microsoft.com/en-us/apps/xamarin) is cross-platform 
across Android, iOS, and Windows. 


	
133
Functional partitioning and various frameworks
Electron (https://www.electronjs.org/) is cross-platform between web and PC. 
Cordova (https://cordova.apache.org/) is a framework for mobile and PC development using HTML, CSS, and JavaScript. With Cordova, cross-platform development 
with web development frameworks like Ember.js is possible. 
Another technique is to code a progressive web app (PWA). A PWA is a browser app or 
web application that can provide a typical desktop browser experience and also uses 
certain browser features such as service workers and app manifests to provide mobile user 
experiences similar to mobile devices. For example, using service workers, a progressive 
web app can provide user experiences, such as push notifications, and cache data in the 
browser to provide offline experiences similar to native mobile apps. A developer can 
configure an app manifest so the PWA can be installed on a desktop or mobile device. 
A user can add an icon of the app on their device’s home screen, start menu, or desktop 
and tap on that icon to open the app; this is a similar experience to installing apps from 
the Android or iOS app stores. Since different devices have different screen dimensions, designers and developers should use a responsive web design approach, which is an 
approach to web design to make the web app render well on various screen dimensions 
or when the user resizes their browser window. Developers can use approaches like 
media queries (https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries/
Using_media_queries) or ResizeObserver (https://developer.mozilla.org/en-US/docs/
Web/API/ResizeObserver) to ensure the app renders well on various browser or screen 
dimensions.
Backend development 
Here is a list of backend development frameworks. Backend frameworks can be classified into RPC, REST, and GraphQL. Some backend development frameworks are fullstack; that is, they can be used to develop a monolithic browser application that makes 
database requests. We can also choose to use them for browser app development and 
make requests to a backend service developed in another framework, but the author 
has never heard of these frameworks being used this way: 
¡ gRPC (https://grpc.io/) is an RPC framework that can be developed in C#, C++, 
Dart, Golang, Java, Kotlin, Node, Objective-C, PHP, Python, or Ruby. It may be 
extended to other languages in the future. 
¡ Thrift (https://thrift.apache.org/) and Protocol Buffers (https://developers 
.google.com/protocol-buffers) are used to serialize data objects, compressing 
them to reduce network traffic. An object can be defined in a definition file. 
We can then generate client and server (backend, not web server) code from a 
definition file. Clients can use the client code to serialize requests to the backend, which uses the backend code to deserialize the requests, and vice versa for 
the backend’s responses. Definition files also help to maintain backward and forward compatibility by placing limitations on possible changes.


134
Chapter 6  Common services for functional partitioning
¡ Dropwizard (https://www.dropwizard.io/) is an example of a Java REST framework. Spring Boot (https://spring.io/projects/spring-boot) can be used to create Java applications, including REST services. 
¡ Flask (https://flask.palletsprojects.com/) and Django (https://www 
.djangoproject.com/) are two examples of REST frameworks in Python. They 
can also be used for web server development. 
Here are several examples of full-stack frameworks: 
¡ Dart (https://dart.dev) is a language that offers frameworks for any solution. It 
can be used for full-stack, backend, server, browser, and mobile apps. 
¡ Rails (https://rubyonrails.org/) is a Ruby full-stack framework that can also be 
used for REST. Ruby on Rails is often used as a single solution, rather than using 
Ruby with other frameworks or Rails with other languages. 
¡ Yesod (https://www.yesodweb.com/) is a Haskell framework that can also be used 
just for REST. Browser app development can be done with Yesod using its Shakespearean template languages https://www.yesodweb.com/book/shakespearean 
-templates, which transpiles to HTML, CSS, and JavaScript. 
¡ Integrated Haskell Platform (https://ihp.digitallyinduced.com/) is another 
Haskell framework. 
¡ Phoenix (https://www.phoenixframework.org/) is a framework for the Elixir 
language.
¡ JavaFX (https://openjfx.io/) is a Java client application platform for desktop, 
mobile, and embedded systems. It is descended from Java Swing (https://docs 
.oracle.com/javase/tutorial/uiswing/), for developing GUI for Java programs. 
¡ Beego (https://beego.vip/) and Gin (https://gin-gonic.com/) are Golang 
frame­works.
6.6	
Library vs. service 
After determining our system’s components, we can discuss the pros and cons of implementing each component on the client-side vs. server-side, as a library vs. service. Do 
not immediately assume that a particular choice is best for any particular component. 
In most situations, there is no obvious choice between using a library vs. service, so we 
need to be able to discuss design and implementation details and tradeoffs for both 
options. 
A library may be an independent code bundle, a thin layer that forwards all requests 
and responses between clients and servers, respectively, or it may contain elements of 
both. In other words, some of the API logic is implemented within the library while 
the rest may be implemented by services called by the library. In this chapter, for the 
purpose of comparing libraries vs. services, the term “library” refers to an independent 
library. 
Table 6.1 summarizes a comparison of libraries vs. services. Most of these points are 
discussed in detail in the rest of this chapter. 


	
135
Library vs. service 
Table 6.1    Summary comparison of libraries vs. services
Library
Service
Users choose which version/build to use and have 
more choice on upgrading to new versions. 
A disadvantage is that users may continue to use 
old versions of libraries that contain bugs or security problems fixed in newer versions. 
Users who wish to always use the latest version of a 
frequently updated library have to implement programmatic upgrades themselves. 
Developers select the build and control when 
upgrades happen.
No communication or data sharing between 
devices limits applications. If the user is another 
service, this service is horizontally scaled, and data 
sharing between hosts is needed, the customer 
service’s hosts must be able to communicate with 
each other to share data. This communication must 
be implemented by the user service’s developers.
No such limitation. Data synchronization between 
multiple hosts can be done via requests to each 
other or to a database. Users need not be concerned about this. 
Language-specific.
Technology-agnostic.
Predictable latency.
Less predictable latency due to dependence on 
network conditions.
Predictable, reproducible behavior.
Network problems are unpredictable and difficult to 
reproduce, so the behavior may be less predictable 
and less reproducible.
If we need to scale up the load on the library, the 
entire application must be scaled up with it. Scaling 
costs are borne by the user’s service.
Independently scalable. Scaling costs are borne by 
the service.
Users may be able to decompile the code to steal 
intellectual property.
Code is not exposed to users. (Though APIs can be 
reverse-engineered. This is outside the scope of 
this book.)
6.6.1	
Language specific vs. technology-agnostic 
For ease of use, a library should be in the client’s language, so the same library must be 
reimplemented in each supported language. 
Most libraries are optimized to perform a well-defined set of related tasks, so they 
can be optimally implemented in a single language. However, certain libraries may 
be partially or completely written in another language because certain languages and 
frameworks may be better suited for specific purposes. Implementing this logic entirely 
in the same language may cause inefficiencies during use. Moreover, while developing 
our library, we may want to utilize libraries written in other languages. There are various utility libraries that one can use to develop a library that contains components in 
other languages. This is outside the scope of this book. A practical difficulty is that the 
team or company that develops this library will require engineers fluent in all of these 
languages. 


136
Chapter 6  Common services for functional partitioning
A service is technology-agnostic because a client can utilize a service regardless of the 
former or latter’s technology stacks. A service can be implemented in the language and 
frameworks best-suited for its purposes. There is a slight additional overhead for clients, 
who will need to instantiate and maintain HTTP, RPC, or GraphQL connections to the 
service. 
6.6.2	
Predictability of latency 
A library has no network latency, has guaranteed and predictable response time, and 
can be easily profiled with tools such as flame graphs. 
A service has unpredictable and uncontrollable latency as it depends on numerous 
factors such as: 
¡ Network latency, which depends on the user’s internet connection quality. 
¡ The service’s ability to handle its current traffic volume. 
6.6.3	
Predictability and reproducibility of behavior 
A service has less predictable and reproducible behavior than a library because its 
behavior has more dependencies such as: 
¡ A deployment rollout is usually gradual (i.e., the build is deployed to a few service 
hosts at a time). Requests may be routed by the load balancer to hosts running 
different builds, resulting in different behavior. 
¡ Users do not have complete control of the service’s data, and it may be changed 
between requests by the service’s developers. This is unlike a library, where users 
have complete control of their machine’s file system. 
¡ A service may make requests to other services and be affected by their unpredictable and unreproducible behavior. 
Despite these factors, a service is often easier to debug than a library because: 
¡ A service’s developers have access to its logs, while a library’s developers do not 
have access to the logs on the users’ devices. 
¡ A service’s developers control its environment and can set up a uniform environment using tools like virtual machines and Docker for its hosts. A library is run 
by users on a diversity of environments such as variations in hardware, firmware, 
and OS (Android vs. iOS). A user may choose to send their crash logs to the 
developers, but it may still be difficult to debug without access to the user’s device 
and exact environment. 
6.6.4	
Scaling considerations for libraries 
A library cannot be independently scaled up since it is contained within the user’s 
application. It does not make sense to discuss scaling up a library on a single user 
device. If the user’s application runs in parallel on multiple devices, the user can scale 


	
137
Common API paradigms
up the library by scaling the application that uses it. To scale just the library alone, the 
user can create their own service that is a wrapper around that library and scale that 
service. But this won’t be a library anymore, but simply a service that is owned by the 
user, so scaling costs are borne by the user. 
6.6.5	
Other considerations 
This section briefly described some anecdotal observations from the author’s personal 
experiences. 
Some engineers have psychological hesitations in bundling their code with libraries 
but are open to connecting to services. They may be concerned that a library will inflate 
their build size, especially for JavaScript bundles. They are also concerned about the 
possibility of malicious code in libraries, while this is not a concern for services since 
the engineers control the data sent to services and have full visibility of the service’s 
responses. 
People expect breaking changes to occur in libraries but are less tolerant of breaking 
changes in services, particularly internal services. Service developers may be forced to 
adopt clumsy API endpoint naming conventions such as including terms like “/v2,” 
“/v3,” etc., in their endpoint names. 
Anecdotal evidence suggests that adapter pattern is followed more often when using 
a library instead of a service. 
6.7	
Common API paradigms
This section introduces and compares the following common communication paradigms. One should consider the tradeoffs in selecting a paradigm for their service:
¡ REST (Representational State Transfer) 
¡ RPC (Remote Procedure Call)
¡ GraphQL
¡ WebSocket
6.7.1	
The Open Systems Interconnection (OSI) model 
The 7-layer OSI model is a conceptual framework/model that characterizes the functions of a networking system without regard to its underlying internal structure and 
technology. Table 6.2 briefly describes each layer. A convenient way to think of this 
model is that the protocols of each level are implemented using protocols of the lower 
level. 
Actor, GraphQL, REST, and WebSocket are implemented on top of HTTP. RPC is 
classified as layer 5 because it handles connections, ports, and sessions directly, rather 
than relying on a higher-level protocol like HTTP. 


138
Chapter 6  Common services for functional partitioning
Table 6.2    The OSI model
Layer no.
Name
Description
Examples
7
Application
User interface.
FTP, HTTP, Telnet
6
Presentation
Presents data. Encryption occurs here.
UTF, ASCII, JPEG, 
MPEG, TIFF
5
Session
Distinction between data of separate applications. Maintains connections. Controls ports 
and sessions.
RPC, SQL, NFX, X 
Windows
4
Transport
End-to-end connections. Defines reliable or 
unreliable delivery and flow control.
TCP, UDP
3
Network
Logical addressing. 
Defines the physical path the data uses. Routers work at this layer.
IP, ICMP
2
Data link
Network format. May correct errors at the physical layer.
Ethernet, wi-fi
1
Physical
Raw bits over physical medium.
Fiber, coax, repeater, 
modem, network 
adapter, USB
6.7.2	
REST 
We assume the reader is familiar with the basics of REST as a stateless communication 
architecture that uses HTTP methods and request/response body most commonly 
encoded in JSON or XML. In this book, we use REST for APIs and JSON for POST 
request and response body. We can represent JSON schema with the specification by 
the JSON Schema organization (https://json-schema.org/), but we don’t do so in this 
book because it is usually too verbose and low-level to discuss JSON schemas in detail in 
a 50-minute system design interview. 
REST is simple to learn, set up, experiment, and debug with (using curl or a REST 
client). Its other advantages include its hypermedia and caching capabilities, which we 
discuss below.
Hypermedia 
Hypermedia controls (HATEOAS) or hypermedia is about providing a client with 
information about “next available actions” within a response. This takes the form of 
a field such as “links” within a response JSON, which contains API endpoints that the 
client may logically query next.
For example, after an ecommerce app displays an invoice, the next step is for the 
client to make payment. The response body for an invoice endpoint may contain a link 
to a payment endpoint, such as this: 
{ 
  "data": { 
    "type": "invoice", 
    "id": "abc123", 
  }, 


	
139
Common API paradigms
  "links": { 
    "pay": "https://api.acme.com/payment/abc123" 
  } 
} 
where the response contains an invoice ID, and the next step is to POST a payment for 
that invoice ID. 
There is also the OPTIONS HTTP method, which is for fetching metadata about an 
endpoint, such as available actions, fields that can be updated, or what data do certain 
fields expect. 
In practice, hypermedia and OPTIONS are difficult for client developers to use, 
and it makes more sense to provide a client developer with API documentation of each 
endpoint or function, such as using OpenAPI (https://swagger.io/specification/) for 
REST or the built-in documentation tools of RPC and GraphQL frameworks. 
Refer to https://jsonapi.org/ for conventions on request/response JSON body 
specification. 
Other communication architectures like RPC or GraphQL do not provide 
hypermedia. 
Caching 
Developers should declare REST resources as cacheable whenever possible, a practice 
which carries advantages such as the following: 
¡ Lower latency because some network calls are avoided. 
¡ Higher availability because the resource is available even if the service is not. 
¡ Better scalability, since there is lower load on the server. 
Use the Expires, Cache-Control, ETag, and Last-Modified HTTP headers for 
caching. 
The Expires HTTP header specifies an absolute expiry time for a cached resource. 
A service can set a time value up to one year ahead of its current clock time. An example 
header is Expires: Mon, 11 Dec 2021 18:00 PST. 
The Cache-Control header consists of comma-separated directives (instructions) 
for caching in both requests and responses. An example header is Cache-Control: 
max-age=3600, which means the response is cacheable for 3600 seconds. A POST or 
PUT request (noun) may include a Cache-Control header as a directive to the server to 
cache this data, but this does not mean that the server will follow this directive, and this 
directive might not be contained in responses for this data. Refer to https://developer 
.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control for all cache request 
and response directives. 
An ETag value is an opaque string token that is an identifier for a specific version of 
a resource. (An opaque token is a token that has a proprietary format that is only known 
to the issuer. To validate an opaque token, the recipient of the token needs to call the 
server that issued the token.) A client can refresh its resource more efficiently by including the ETag value in the GET request. The server will only return the resource’s value if 


140
Chapter 6  Common services for functional partitioning
the latter’s ETag is different. In other words, the resource’s value changed, so it does not 
unnecessarily return the resource’s value if the client already has it. 
The Last-Modified header contains the date and time the resource was last modified and can be used as a fallback for the ETag header if the latter is unavailable. Related 
headers are If-Modified-Since and If-Unmodified-Since.
Disadvantages of REST 
A disadvantage is that it has no integrated documentation mechanisms, other than 
hypermedia or OPTIONS endpoints, which developers can choose not to provide. 
One must add an OpenAPI documentation framework to a service implemented 
using a REST framework. Otherwise, clients have no way of knowing the available 
request endpoints, or their details such as path or query parameters or the request and 
response body fields. REST also has no standardized versioning procedure; a common 
convention is to use a path like “/v2,” “/v3,” etc. for versioning. Another disadvantage 
of REST is that it does not have a universal specification, which leads to confusion. 
OData and JSON-API are two popular specifications. 
6.7.3	
RPC (Remote Procedure Call) 
RPC is a technique to make a procedure execute in a different address space (i.e., 
another host), without the programmer having to handle the network details. Popular 
open-source RPC frameworks include Google’s gRPC, Facebook’s Thrift, and RPyC in 
Python. 
For an interview, you should be familiar with the following common encoding formats. You should understand how encoding (also called serialization or marshalling) 
and decoding (also called parsing, deserialization, or unmarshalling) are done. 
¡ CSV, XML, JSON 
¡ Thrift 
¡ Protocol Buffers (protobuf) 
¡ Avro 
The main advantages of RPC frameworks like gRPC over REST are: 
¡ RPC is designed for resource optimization, so it is the best communication 
architecture choice for low-power devices, such as IoT devices like smart home 
devices. For a large web service, its lower resource consumption compared to 
REST or GraphQL becomes significant with scale. 
¡ Protobuf is an efficient encoding. JSON is repetitive and verbose, causing 
requests and responses to be large. Network traffic savings become significant 
with scale. 
¡ Developers define the schemas of their endpoints in files. Common formats 
include Avro, Thrift, and protobuf. Clients use these files to create requests and 
interpret responses. As schema documentation is a required step in developing 


	
141
Common API paradigms
the API, client developers will always have good API documentation. These 
encoding formats also have schema modification rules, which make it clear to 
developers how to maintain backward and/or forward compatibility in schema 
modifications. 
The main disadvantages of RPC are also from its nature as a binary protocol. It is troublesome for clients to have to update to the latest version of the schema files, especially 
outside an organization. Also, if an organization wishes to monitor its internal network 
traffic, it is easier to do so with text protocols like REST than with binary protocols like 
RPC.
6.7.4	
GraphQL 
GraphQL is a query language that enables declarative data fetching, where a client can 
specify exactly what data it needs from an API. It provides an API data query and 
manipulation language for pinpoint requests. It also provides an integrated API documentation tool that is essential for navigating this flexibility. The main benefits are: 
¡ The client decides what data they want and its format. 
¡ The server is efficient and delivers exactly what the client requests without under 
fetching (which necessitates multiple requests) or over-fetching (which inflates 
response size). 
Tradeoffs: 
¡ May be too complex for simple APIs. 
¡ Has a higher learning curve than RPC and REST, including security mechanisms. 
¡ Has a smaller user community than RPC and REST. 
¡ Encodes in JSON only, which carries all the tradeoffs of JSON. 
¡ User analytics may be more complicated because each API user performs slightly 
different queries. In REST and RPC, we can easily see how many queries were 
made to each API endpoint, but this is less obvious in GraphQL.
¡ We should be cautious when using GraphQL for external APIs. It is similar to 
exposing a database and allowing clients to make SQL queries. 
Many of the benefits of GraphQL can be done in REST. A simple API can begin with 
simple REST HTTP methods (GET, POST, PUT, DELETE) with simple JSON bodies. 
As its requirements become more complex, it can use more REST capabilities such 
as OData https://www.odata.org/, or use JSON-API capabilities like https://jsonapi 
.org/format/#fetching-includes to combine related data from multiple resources into 
a single request. GraphQL may be more convenient than REST in addressing complex 
requirements because it provides a standard implementation and documentation of its 
capabilities. REST, on the other hand, has no universal standard.


142
Chapter 6  Common services for functional partitioning
6.7.5	
WebSocket 
WebSocket is a communications protocol for full-duplex communication over a 
persistent TCP connection, unlike HTTP, which creates a new connection for every 
request and closes it with every response. REST, RPC, GraphQL, and Actor model are 
design patterns or philosophies, while WebSocket and HTTP are communication protocols. However, it makes sense to compare WebSocket to the rest as API architectural 
styles because we can choose to implement our API using WebSocket rather than the 
other four choices. 
To create a WebSocket connection, a client sends a WebSocket request to the server. 
WebSocket uses an HTTP handshake to create an initial connection and requests the 
server to upgrade to WebSocket from HTTP. Subsequent messages can use WebSocket 
over this persistent TCP connection. 
WebSocket keeps connections open, which increases overhead for all parties. This 
means that WebSocket is stateful (compared to REST and HTTP, which are stateless). 
A request must be handled by the host that contains the relevant state/connection, 
unlike in REST where any host can handle any request. Both the stateful nature of Web-
Socket and the resource overhead of maintaining connections means that WebSocket 
is less scalable. 
WebSocket allows p2p communication, so no backend is required. It trades off scalability for lower latency and higher performance.
6.7.6	
Comparison 
During an interview, we may need to evaluate the tradeoffs between these architectural styles and the factors to consider in choosing a style and protocol. REST and 
RPC are the most common. Startups usually use REST for simplicity, while large 
organizations can benefit from RPC’s efficiency and backward and forward compatibility. GraphQL is a relatively new philosophy. WebSocket is useful for bidirectional 
communication, including p2p communication. Other references include https://
apisyouwonthate.com/blog/picking-api-paradigm/ and https://www.baeldung.com/
rest-vs-websockets. 
Summary
¡ An API gateway is a web service designed to be stateless and lightweight yet fulfill 
many cross-cutting concerns across various services, which can be grouped into 
security, error-checking, performance and availability, and logging.
¡ A service mesh or sidecar pattern is an alternative pattern. Each host gets its own 
sidecar, so no service can consume an unfair share.
¡ To minimize network traffic, we can consider using a metadata service to store 
data that is processed by multiple components within a system.
¡ Service discovery is for clients to identify which service hosts are available.


	
143
Summary
¡ A browser app can have two or more backend services. One of them is a web 
server service that intercepts requests and responses from the other backend 
services.
¡ A web server service minimizes network traffic between the browser and data center, by performing aggregation and filtering operations with the backend.
¡ Browser app frameworks are for browser app development. Server-side frameworks are for web service development. Mobile app development can be done 
with native or cross-platform frameworks.
¡ There are cross-platform or full-stack frameworks for developing browser apps, 
mobile apps, and web servers. They carry tradeoffs, which may make them unsuitable for one’s particular requirements.
¡ Backend development frameworks can be classified into RPC, REST, and 
GraphQL frameworks.
¡ Some components can be implemented as either libraries or services. Each 
approach has its tradeoffs.
¡ Most communication paradigms are implemented on top of HTTP. RPC is a lower-level protocol for efficiency.
¡ REST is simple to learn and use. We should declare REST resources as cacheable 
whenever possible.
¡ REST requires a separate documentation framework like OpenAPI.
¡ RPC is a binary protocol designed for resource optimization. Its schema modification rules also allow backward- and forward-compatibility.
¡ GraphQL allows pinpoint requests and has an integrated API documentation 
tool. However, it is complex and more difficult to secure.
¡ WebSocket is a stateful communications protocol for full-duplex communication. It has more overhead on both the client and server than other communication paradigms.

## Examples & Scenarios

- help satisfy requirements better, with certain tradeoffs. For example, we don’t need to
calculate file size reduction or CPU and memory resources required for Gzip compression on a file, but we should be able to state that compressing a file before sending it
will reduce network traffic but consume more CPU and memory resources on both the
sender and recipient.
An aim of this book is to bring together a bunch of relevant materials and organize
them into a single book so you can build a knowledge foundation or identify gaps in
your knowledge, from which you can study other materials.
The rest of this chapter is a prelude to a sample system design that mentions some of
the concepts that will be covered in part 1. Based on this context, we will discuss many of
the concepts in dedicated chapters.

- repeating this process until 100% of production hosts are running this build. For example, we may deploy to 1%, 5%, 10%, 25%, 50%, 75%, and then finally 100%. We may
manually or automatically roll back deployments if we detect any problems, such as:
¡ Bugs that slipped through testing.
¡ Crashes.
¡ Increased latency or timeouts.
¡ Memory leaks.
¡ Increased resource consumption like CPU, memory, or storage utilization.
¡ Increased user churn. We may also need to consider user churn in gradual outs—
that is, that new users are signing on and using the app, and certain users may
stop using the app. We can gradually expose an increasing percentage of users to

- For example, a new build may increase latency beyond an acceptable level. We can use
a combination of caching and dynamic routing to handle this. Our service may specify
a one-second latency. When a client makes a request that is routed to a new build, and
a timeout occurs, our client may read from its cache, or it may repeat its request and be
routed to a host with an older build. We should log the requests and responses so we
can troubleshoot the timeouts.
We can configure our CD pipeline to divide our production cluster into several
groups, and our CD tool will determine the appropriate number of hosts in each group
and assign hosts to groups. Reassignments and redeployments may occur if we resize
our cluster.

- because it is not applicable to them. For example, section 15.1 discusses various
methods of payment in an app. There are possibly thousands of payment solutions in the world. The app needs to contain all the code and SDKs for every
payment solution, so it can present each user with the small subset of payment
solutions they may have.
A consequence of all this is that a mobile app can be over 100MB in size. The techniques to address this are outside the scope of this book. We need to achieve a balance
and consider tradeoffs. For example, YouTube’s mobile app installation obviously cannot include many YouTube videos.
1.4.6
Functional partitioning and centralization of cross-cutting concerns
Functional partitioning is about separating various functions into different services or
hosts. Many services have common concerns that can be extracted into shared services.

- rather than process it only when a request is made. For example, our app’s home

- that is outdated by some hours or days. For example, users do not need to see the
most updated statistics of the number of users who have viewed their shared content. It is acceptable to show them statistics that are out-of-date by a few hours.
¡ Writes (e.g., INSERT, UPDATE, DELETE database requests) that do not have to
be executed immediately. For example, writes to the logging service do not have
to be immediately written to the hard disk drives of logging service hosts. These
write requests can be placed in a queue and executed later.
In the case of certain systems like logging, which receive large request volumes from
many other systems, if we do not use an asynchronous approach like ETL, the logging system cluster will have to have thousands of hosts to process all these requests
synchronously.
We can use a combination of event streaming systems like Kafka (or Kinesis if we use

- we can use streaming tools such as Flink. For example, if a user inputs some data into
our app, and we want to use it to send certain recommendations or notifications to
them within seconds or minutes, we can create a Flink pipeline that processes recent
user inputs. A logging system is usually streaming because it expects a non-stop stream
of requests. If the requests are less frequent, a batch pipeline will be sufficient.
1.4.8
Other common services
As our company grows and our userbase expands, we develop more products, and
our products should become increasingly customizable and personalized to serve this
large, growing, and diverse userbase. We will require numerous other services to satisfy

- ¡ Internal search and subproblems (e.g., autocomplete/typeahead service). Many
of our web or mobile applications can have search bars for users to search for
their desired data.
¡ Privacy compliance services and teams. Our expanding user numbers and large
amount of customer data will attract malicious external and internal actors,
who will attempt to steal data. A privacy breach on our large userbase will affect
numerous people and organizations. We must invest in safeguarding user privacy.
¡ Fraud detection. The increasing revenue of our company will make it a tempting target for criminals and fraudsters, so effective fraud detection systems are a
must.
1.4.9

- constantly upgrade their hardware and software. For example, even upgrading the version of MySQL used in a large organization takes considerable time and effort. Many
organizations prefer to outsource such maintenance to cloud providers.
Some disadvantages
One disadvantage of cloud providers is vendor lock-in. Should we decide to transfer
some or all components of our app to another cloud vendor, this process may not
be straightforward. We may need considerable engineering effort to transfer data and
services from one cloud provider to another and pay for duplicate services during this
transition.
There are many possible reasons we will want to migrate out of a vendor. Today, the
vendor may be a well-managed company that fulfills a demanding SLA at a competitive

- Consider various combinations of user categories, such as manual versus programmatic or consumer versus enterprise. For example, a manual/consumer
combination involves requests from our consumers via our mobile or browser
apps. A programmatic/enterprise combination involves requests from other
services or companies.
b	 Technical or nontechnical? Design platforms or services for developers or
non-developers. Technical examples include a database service like key-value
store, libraries for purposes like consistent hashing, or analytics services.
Non-technical questions are typically in the form of “Design this well-known
consumer app.” In such questions, discuss all categories of users, not just the
non-technical consumers of the app.

- c	 List the user roles (e.g., buyer, seller, poster, viewer, developer, manager).
d	 Pay attention to numbers. Every functional and non-functional requirement
must have a number. Fetch news items? How many news items? How much
time? How many milliseconds/seconds/hours/days?
e	 Any communication between users or between users and operations staff?
f	 Ask about i18n and L10n support, national or regional languages, postal
address, price, etc. Ask whether multiple currency support is required.

- For example, if a search service has 1 billion daily users, each submitting 10
search requests, there are 10 billion daily requests or 420 million hourly requests.
3	 Which data should be accessible to which users? Discuss the authentication
and authorization roles and mechanisms. Discuss the contents of the response
body of the API endpoint. Next, discuss how often is data retrieved—real-time,
monthly reports, or another frequency?
4	 Search. What are possible use cases that involve search?
5	 Analytics is a typical requirement. Discuss possible machine learning requirements, including support for experimentation such as A/B testing or multi-armed
bandit. Refer to https://www.optimizely.com/optimization-glossary/ab-testing/
and https://www.optimizely.com/optimization-glossary/multi-armed-bandit/ for

- 6	 Scribble down pseudocode function signatures (e.g., fetchPosts(userId)) to
fetch posts by a certain user and match them to the user stories. Discuss with the
interviewer which requirements are needed and which are out of scope.
Always ask, “Are there other user requirements?” and brainstorm these possibilities.
Do not allow the interviewer to do the thinking for you. Do not give the interviewer the
impression that you want them to do the thinking for you or want them to tell you all
the requirements.
Requirements are subtle, and one often misses details even if they think they have
clarified them. One reason software development follows agile practices is that requirements are difficult or impossible to communicate. New requirements or restrictions are
constantly discovered through the development process. With experience, one learns

- teams were computing metrics differently. For example, should the total number of
orders include canceled or refunded orders? What time zone should be used for the
cutoff time of “seven days ago”? Does “last seven days” include the present day? The
communication overhead between multiple teams to clarify metric definitions was
costly and error-prone.
Although computing business metrics uses order data from the Orders service, we
decide to form a new team to create a dedicated Metrics service, since metric definitions can be modified independently of order data.
The Metrics service will depend on the Orders service for order data. A request for a
metric will be processed as follows:
1	 Retrieve the metric.

- If both services share the same database, the computation of a metric makes SQL queries on Orders service’s tables. Schema migrations become more complex. For example, the Orders team decides that users of the Order table have been making too many
large queries on it. After some analysis, the team determined that queries on recent
orders are more important and require higher latency than queries on older orders.
The team proposes that the Order table should contain only orders from the last year,
and older orders will be moved to an Archive table. The Order table can be allocated a
larger number of followers/read replicas than the Archive table.
The Metrics team must understand this proposed change and change metric computation to occur on both tables. The Metrics team may object to this proposed change,
so the change may not go ahead, and the organizational productivity gain from faster
queries on recent order data cannot be achieved.
If the Orders team wishes to move the Order table to Cassandra to use its low write

- For example, a hotel room booking service may require users to spend some time to
enter their check-in and check-out dates and their contact and payment information
and then submit their booking request. We should ensure that multiple users do not
overbook the room.
Another example may be configuring the contents of a push notification. For example, our company may provide a browser app for employees to configure push notifications sent to our Beigel app (refer to chapter 1). A particular push notification
configuration may be owned by a team. We should ensure that multiple team members do not edit the push notification simultaneously and then overwrite each other’s
changes.
There are many ways of preventing concurrent updates. We present one possible way
in this section.
To prevent such situations, we can lock a configuration when it is being edited. Our

- period (e.g., 10 minutes), and another user finds that it is locked:
1	 Alice and Bob are both viewing the push notification configuration on our Notifications browser app. Alice decides to update the title from “Celebrate National
Bagel Day!” to “20% off on National Bagel Day!” She clicks on the Edit button.
The following steps occur:
a	 The click event sends a PUT request, which sends her username and email to
the backend. The backend’s load balancer assigns this request to a host.
b	 Alice’s backend host makes two SQL queries, one at a time. First, it determines
the current unix_locked time:
SELECT unix_locked FROM table_name WHERE config_id = {config_id}.
c	 The backend checks whether the “edit_start” timestamp is less than 12 minutes ago. (This includes a 2 minute buffer in case the countdown timer in

- more than 1 second, or alerts that trigger for a P99 over a sliding window (e.g., 5
seconds, 10 seconds, 1 minute, 5 minutes).
2	 Traffic—Measured in HTTP requests per second. We can set up alerts for various
endpoints that trigger if there is too much traffic. We can set appropriate numbers based on the load limit determined in our load testing.
3	 Errors—Set up high-urgency alerts for 4xx or 5xx response codes that must be
immediately addressed. Trigger low-urgency (or high urgency, depending on
your requirements) alerts on failed audits.
4	 Saturation—Depending on whether our system’s constraint is CPU, memory, or
I/O, we can set utilization targets that should not be exceeded. We can set up
alerts that trigger if utilization targets are reached. Another example is storage

- such as errors. We can place log statements within our application and set up customized metrics, dashboards, and alerts that focus on these user experiences. For example,
to focus on 5xx errors due to application bugs, we can create metrics, dashboards and
alerts that process certain details like request parameters and return status codes and
error messages, if any.
We should also log events to monitor how well our system satisfies our unique functional and non-functional requirements. For example, if we build a cache, we want to
log cache faults, hits, and misses. Metrics should include the counts of faults, hits, and
misses.
In enterprise systems, we may wish to give users some access to monitoring or even
build monitoring tools specifically for users for example, customers can create dashboards to track the state of their requests and filter and aggregate metrics and alerts by
categories such as URL paths.

- a series of commands that can easily be copied and pasted to solve the problem (e.g.,
restarting a host), these steps should be automated in the application, along with logging that these steps were run (Mike Julian, Practical Monitoring, chapter 3, O’Reilly
Media Inc, 2017). Failure to implement automated failure recovery when possible is
runbook abuse. If certain runbook instructions consist of running commands to view
particuar metrics, we should display these metrics on our dashboard.
A company may have a Site Reliability Engineering (SRE) team, which consists of
engineers who develop tools and processes to ensure high reliability of critical services
and are often on-call for these critical services. If our service obtains SRE coverage, a
build of our service may have to satisfy the SRE team’s criteria before it can be deployed.
This criteria typically consists of high unit test coverage, a functional test suite that

## Tables & Comparisons

| Pod
Envoy proxy
host (sidecar)
Service 1 host |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Pod
Envoy proxy
host (sidecar)
Service 1 host |  |  |  |
|  |  | Envoy proxy
host (sidecar)
Service 1 host |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

|  |  |
| --- | --- |
|  |  |
|  |  |

|  |  |
| --- | --- |
|  | Service 1 host |

| Pod
Envoy proxy
host (sidecar)
Service 1 host |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Pod
Envoy proxy
host (sidecar)
Service 1 host |  |  |  |
|  |  | Envoy proxy
host (sidecar)
Service 1 host |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

|  |  |
| --- | --- |
|  | Service 1 host |

| Pod
Envoy proxy
host (sidecar)
Service 1 host |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Pod
Envoy proxy
host (sidecar)
Service 1 host |  |  |  |
|  |  | Envoy proxy
host (sidecar)
Service 1 host |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

|  |  |
| --- | --- |
|  | Service 1 host |

| 1b. Get u |  |  | n | i | x_locked value of the desired config ID. |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  | unix_locked value
3b. Same request as 1b.
Same unix_locked value as 1b.
DATE the row of the desired config ID. |  |
|  | 1c. UP |  |  | DATE the row of the desired config ID. |  |
|  |  |  |  | success. unix_locked value changed.
3c. UPDATE a row which no longer exists.
UPDATE failed.
ase "unix_locked" and editor details. |  |
|  |  | 4. Er |  | ase "unix_locked" and editor details. |  |

| SQL | Elasticsearch |
| --- | --- |
| Database
Partition
Table
Column
Row
Schema
Index | Index
Shard
Type (deprecated without replacement)
Field
Document
Mapping
Everything is indexed |

| Availability % | Downtime
per year | Downtime
per month | Downtime
per week | Downtime
per day |
| --- | --- | --- | --- | --- |
| 99.9 (three 9s)
99.99 (four 9s)
99.999 (five 9s) | 8.77 hours
52.6 minutes
5.26 minutes | 43.8 minutes
4.38 minutes
26.3 seconds | 10.1 minutes
1.01 minutes
6.05 seconds | 1.44 minutes
8.64 seconds
864 milliseconds |

| Favor linearizability | Favor availability |
| --- | --- |
| HBase
MongoDB
Redis | Cassandra
CouchDB
Dynamo
Hadoop
Riak |

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  |  |  | de |
|  |  |  |  |  |
|  |  |  |  |  |

| Kafka | RabbitMQ |
| --- | --- |
| Designed for scalability, reliability, and avail-
ability. More complex setup required than
RabbitMQ.
Requires ZooKeeper to manage the
Kafka cluster. This includes configuring IP
addresses of every Kafka host in ZooKeeper.
A durable message broker because it has
replication. We can adjust the replication
factor on ZooKeeper and arrange replication
to be done on different server racks and
data centers.
Events on the queue are not removed after
consumption, so the same event can be
consumed repeatedly. This is for failure tol-
erance, in case the consumer fails before it
finished processing the event and needs to
reprocess the event.
In this regard, it is conceptually inaccurate to
use the term “queue” in Kafka. It is actually a
list. But the term “Kafka queue” is commonly
used.
We can configure a retention period in
Kafka, which is seven days by default, so an
event is deleted after seven days regardless
of whether it has been consumed. We can
choose to set the retention period to infinite
and use Kafka as a database.
No concept of priority. | Simple to set up, but not scalable by default.
We can implement scalability on our own at the applica-
tion level by attaching our application to a load balancer
and producing to and consuming from the load balancer.
But this will take more work to set up than Kafka and being
far less mature will almost certainly be inferior in many
ways.
Not scalable, so not durable by default. Messages are lost
if downtime occurs. Has a “lazy queue” feature to persist
messages to disk for better durability, but this does not
protect against disk failure on the host.
Messages on the queue are removed upon dequeuing, as
per the definition of “queue” (RabbitMQ 3.9 released on
July 26, 2021, has a stream https://www.rabbitmq.com/
streams.html feature that allows repeated consumption of
each message, so this difference is only present for earlier
versions.)
We may create several queues to allow several consumers
per message, one queue per consumer. But this is not the
intended use of having multiple queues.
Has the concept of AMQP standard per-message queue
priority. We can create multiple queues with varying
priority. Messages on a queue are not dequeued until
higher-priority queues are empty. No concept of fairness or
consideration of starvation. |

|  | Event Sourcing | Change Data Capture (CDC) |
| --- | --- | --- |
| Purpose
Source of truth
Granularity | Record events as the source of truth.
The log, or events published to the
log, are the source of truth.
Fine-grained events that represent
specific actions or changes in state. | Synchronize data changes by propagating
events from a source service to downstream
services.
A database in the publisher service. The pub-
lished events are not the source of truth.
Individual database level changes such as
new, updated, or deleted rows or documents. |

| Choreography | Orchestration |
| --- | --- |
| Requests to services are made in parallel. This is
the observer object-oriented design pattern.
The service that begins the saga communicates
with two Kafka topics. It produces one Kafka topic
to start the distributed transaction and consumes
from another Kafka topic to perform any final logic.
The service that begins the saga only has code that
produces to the saga’s first topic and consumes
from the saga’s last topic. A developer must read
the code of every service involved in the saga to
understand its steps.
A service may need to subscribe to multiple Kafka
topics, such as the Accounting Service in figure
5.5 of Richardson’s book. This is because it may
produce a certain event only when it has consumed
certain other events from multiple services. This
means that it must record in a database which
events it has already consumed. | Requests to services are made linearly. This is the
controller object-oriented design pattern.
The orchestrator communicates with each service
via a Kafka topic. In each step in the saga, the
orchestrator must produce to a topic to request this
step to begin, and it must consume from another
topic to receive the step’s result.
The orchestrator has code that produces and con-
sumes Kafka topics that correspond to steps in the
saga, so reading the orchestrator’s code allows one
to understand the services and steps in the distrib-
uted transaction.
Other than the orchestrator, each service only
subscribes to one other Kafka topic (from one
other service). The relationships between the
various services are easier to understand. Unlike
choreography, a service never needs to consume
multiple events from separate services before it
can produce a certain event, so it may be possible
to reduce the number of database writes. |

| Choreography | Orchestration |
| --- | --- |
| Less resource-intensive, less chatty, and less net-
work traffci ; hence, it has lower latency overall.
Parallel requests also result in lower latency.
Services have a less independent software devel-
opment lifecycle because developers must under-
stand all services to change any one of them.
No such single point of failure as in orchestration
(i.e., no service needs to be highly available except
the Kafka service).
Compensating transactions are triggered by the
various services involved in the saga. | Since every step must pass through the orchestra-
tor, the number of events is double that of chore-
ography. The overall effect is that orchestration is
more resource-intensive, chattier, and has more
network traffic; hence, it has higher latency overall.
Requests are linear, so latency is higher.
Services are more independent. A change to a
service only affects the orchestrator and does not
affect other services.
If the orchestration service fails, the entire saga
cannot execute (i.e., the orchestrator and the Kafka
service must be highly available).
Compensating transactions are triggered by the
orchestrator. |

| Pod
Envoy proxy
host (sidecar)
Service 1 host |  |  |  |
| --- | --- | --- | --- |
|  | Pod
Envoy proxy
host (sidecar)
Service 1 host |  |  |
|  |  |  |  |
|  |  |  |  |

|  |  |
| --- | --- |
|  |  |
|  |  |

| Pod
Envoy proxy
host (sidecar)
Service 1 host |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Pod
Envoy proxy
host (sidecar)
Service 1 host |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

| Pod
Envoy proxy
host (sidecar)
Service 1 host |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Pod
Envoy proxy
host (sidecar)
Service 1 host |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

| Library | Service |
| --- | --- |
| Users choose which version/build to use and have
more choice on upgrading to new versions.
A disadvantage is that users may continue to use
old versions of libraries that contain bugs or secu-
rity problems fixed in newer versions.
Users who wish to always use the latest version of a
frequently updated library have to implement pro-
grammatic upgrades themselves.
No communication or data sharing between
devices limits applications. If the user is another
service, this service is horizontally scaled, and data
sharing between hosts is needed, the customer
service’s hosts must be able to communicate with
each other to share data. This communication must
be implemented by the user service’s developers.
Language-specific.
Predictable latency.
Predictable, reproducible behavior.
If we need to scale up the load on the library, the
entire application must be scaled up with it. Scaling
costs are borne by the user’s service.
Users may be able to decompile the code to steal
intellectual property. | Developers select the build and control when
upgrades happen.
No such limitation. Data synchronization between
multiple hosts can be done via requests to each
other or to a database. Users need not be con-
cerned about this.
Technology-agnostic.
Less predictable latency due to dependence on
network conditions.
Network problems are unpredictable and difficult to
reproduce, so the behavior may be less predictable
and less reproducible.
Independently scalable. Scaling costs are borne by
the service.
Code is not exposed to users. (Though APIs can be
reverse-engineered. This is outside the scope of
this book.) |

| Layer no. | Name | Description | Examples |
| --- | --- | --- | --- |
| 7
6
5
4
3
2
1 | Application
Presentation
Session
Transport
Network
Data link
Physical | User interface.
Presents data. Encryption occurs here.
Distinction between data of separate applica-
tions. Maintains connections. Controls ports
and sessions.
End-to-end connections. Defines reliable or
unreliable delivery and flow control.
Logical addressing.
Defines the physical path the data uses. Rout-
ers work at this layer.
Network format. May correct errors at the phys-
ical layer.
Raw bits over physical medium. | FTP, HTTP, Telnet
UTF, ASCII, JPEG,
MPEG, TIFF
RPC, SQL, NFX, X
Windows
TCP, UDP
IP, ICMP
Ethernet, wi-fi
Fiber, coax, repeater,
modem, network
adapter, USB |

