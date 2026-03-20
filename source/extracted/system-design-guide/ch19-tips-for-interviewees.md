# Chapter 15: Tips for Interviewees

> Source: System Design Guide for Software Professionals, Chapter 19, Pages 365-372

## Key Concepts

- 15
Tips for Interviewees
System design interviews are a crucial part of the hiring process for senior software engineering
and engineering management roles. They test your ability to architect scalabl
- Scalability: Learn about horizontal and vertical scaling, load balancing, and distributed systems. Learn how load balancers
allocate incoming network traffic among multiple servers to prevent any sing

## Content

15
Tips for Interviewees
System design interviews are a crucial part of the hiring process for senior software engineering
and engineering management roles. They test your ability to architect scalable, efficient, and
robust systems, reflecting your understanding of the trade-offs and complexities involved in realworld applications.
Performing well in these interviews isn’t only required to get an offer. Candidates are often
evaluated on their performance on these system design rounds to be considered for different
levels. For example, a candidate who performs excellently at these system design interviews may
be hired at an L+1 level rather than an L level. That means higher responsibilities, scope, and
compensation.
This chapter offers practical tips and strategies to help you excel in system design interviews,
from understanding the requirements to presenting your solution effectively.
We will cover the following topics in this chapter:
Tips for preparation for system design interviews
Tips for the interview session
Tips for preparation for system design interviews
Preparing for system design interviews requires a strategic approach that combines theoretical
knowledge, practical experience, and effective communication skills. This chapter provides a
comprehensive guide on how to prepare for system design interviews, covering essential topics,
resources, and techniques to help you succeed.
Understanding the fundamentals
Start with a solid understanding of the fundamental concepts in system design. These
foundational basics will help you navigate the path and solve the core challenges, especially
when faced with an unfamiliar system design question. With a solid grasp of these concepts, you
will be able to perform better in your interviews:


Scalability: Learn about horizontal and vertical scaling, load balancing, and distributed systems. Learn how load balancers
allocate incoming network traffic among multiple servers to prevent any single server from becoming a bottleneck.
Databases: Familiarize yourself with different types of databases (SQL versus NoSQL), indexing, sharding, and replication.
Know when to use a relational database such as PostgreSQL versus a NoSQL database such as MongoDB based on the use
case.
Caching: Understand caching strategies, cache eviction policies, and tools such as Redis and Memcached. Use Redis to
cache frequently accessed data to reduce database load and improve response times.
Consistency and availability: Study the CAP and PACELC theorems and learn about consistency models (strong, eventual
consistency). Understand the trade-offs between consistency and availability in distributed systems.
This is not a comprehensive list, but if you have read the first couple of chapters of this book,
you would already have gone through these and more. Let’s move on to learning about some of
the common system design patterns that will come in handy in a system design interview.
Studying common system design patterns
Learning about common system design patterns and their applications will help you to have a
good starting point for your solution. Some of these are as follows:
Microservices architecture: Understand how to design systems using microservices, including inter-service
communication. Use RESTful APIs or gRPC for communication between microservices.
Event-driven architecture: Learn how to design systems that respond to events using message queues or event streams.
Use Apache Kafka to build a real-time data processing pipeline.
Service-Oriented Architecture (SOA): Study how SOA differs from microservices and its use cases. Use SOAP for
communication in legacy systems or when strong contract enforcement is required.
Design patterns: Familiarize yourself with patterns such as Command Query Responsibility Segregation (CQRS), Saga,
and Circuit Breaker. Implement the Circuit Breaker pattern to handle failures in distributed systems gracefully.
Again, this is not a comprehensive list, but identifying and mastering such design patterns is very
important for your system design interview preparation.
Practicing designing systems
Practical experience is essential to mastering system design. Regularly practicing the design of
systems for various scenarios helps solidify theoretical knowledge and improves problemsolving skills. Engaging with diverse use cases, from designing scalable web applications to
architecting robust databases, equips you with the versatility needed to tackle real-world
challenges. Here are some steps to consider:


Mock interviews: Conduct mock interviews with peers or use platforms such as Pramp, Interviewing.io, or Exponent.
Simulate a system design interview scenario, such as designing a URL shortening service, and get feedback on your
approach.
Design challenges: Take on design challenges from resources such as LeetCode, HackerRank, or Grokking the System
Design Interview. Solve design problems such as building a scalable notification system or a ride-sharing service.
Case studies: Analyze real-world case studies of large-scale systems to understand their architecture and design decisions.
Study the architecture of Twitter to learn about handling high throughput and ensuring low latency.
Consistent practice and review not only enhance your understanding of design principles but also
build confidence in your ability to create efficient, reliable, and maintainable systems.
Learning from online resources
You can utilize online resources and courses to deepen your understanding and stay updated with
best practices. Here is a list of some of these resources:
Books: Read foundational books such as Designing Data-Intensive Applications by Martin Kleppmann and The Art of
Scalability by Martin L. Abbott and Michael T. Fisher. These books provide in-depth knowledge on building scalable and
reliable systems.
Online courses: Enroll in online courses from platforms such as Coursera, Udemy, or Educative. Grokking the System
Design Interview on Educative offers practical insights and design patterns.
Blogs and articles: Follow blogs and articles from industry leaders and companies known for their robust architectures.
Read engineering blogs from companies such as Netflix, Uber, and LinkedIn to learn about their system design practices.
YouTube channels: Watch videos and tutorials on system design topics. There are many great channels, such as Tushar
Roy, Tech Dummies, and Gaurav Sen, which provide detailed explanations of system design concepts and interview tips.
System design is a vast and complex field. It’s important to keep learning and look at problems
and solutions from different perspectives.
Honing your communication skills
Effective communication is key to conveying your ideas clearly during the interview:
Practice verbalizing your thoughts: Regularly practice explaining your thought process out loud. Conduct mock
interviews with a friend or mentor and focus on articulating your design decisions clearly.
Use visual aids: Use diagrams and charts to illustrate your design. Practice drawing architecture diagrams and sequence
diagrams to convey complex ideas visually.
Reviewing and reflecting


After each practice session or real interview, review your performance and identify areas for
improvement:
Self-assessment: Reflect on what went well and what could be improved. Did you manage to cover all the requirements?
Were there any components you overlooked?
Seek feedback: Get feedback from peers, mentors, or interviewers to understand your strengths and weaknesses. Ask for
specific feedback on your approach, communication skills, and depth of knowledge.
Continuous improvement: Use the feedback to refine your preparation strategy and focus on areas that need improvement.
For example, if you struggled with database design, spend more time studying database architectures and practicing related
problems.
Preparing for system design interviews requires a combination of theoretical knowledge,
practical experience, and effective communication skills. By understanding the fundamentals,
studying common design patterns, practicing regularly, adopting a methodical approach,
leveraging online resources, honing your communication skills, and reflecting on your
performance, you can build the confidence and expertise needed to excel in system design
interviews. Continuous learning and improvement are key to staying ahead and successfully
navigating the complexities of system design challenges.
Tips for the interview session
Now that you have done extensive preparation, when it comes to the actual interview, you want
to keep some tips in mind. First of all, be prepared that the questions you are asked may be
unfamiliar to you. That’s OK. Don’t panic. Most of the time you should be able to use the
fundamental concepts, components, philosophies, techniques, and subsystems you have learned
about and designed to design a new system. Let’s go over some guidelines and tips now.
Understanding the problem statement
Before diving into designing the system, take the time to thoroughly understand the problem
statement:
Ask clarifying questions: Ensure you have a clear understanding of the requirements. Ask questions about the scope,
constraints, and any ambiguities. For example, if asked to design a chat application, clarify whether the focus is on real-time
messaging, user authentication, or message storage.
Identify functional requirements: List the core functionalities the system must support. For example, for an e-commerce
platform, these might include user registration, product search, shopping cart, and payment processing.


Identify non-functional requirements: Understand performance, scalability, availability, and reliability requirements. For
example, for a social media feed, you might need to handle high read and write throughput with low latency.
Breaking down the problem
Divide the problem into smaller, manageable components or services:
Component identification: Identify the major components or services required. For example, in a URL shortening service,
the components might include an API gateway, URL storage, redirection service, and analytics.
Define interactions: Determine how these components will interact with each other. For example, the API gateway receives
shortening requests, the storage service saves the mapping, and the redirection service handles redirects.
Use diagrams: Visual aids such as block diagrams or sequence diagrams can help convey your design clearly. For example,
draw an architecture diagram showing how data flows between the user, API gateway, storage, and redirection service.
Key steps to follow
A very high-level set of steps you should take are as follows:
1. Write functional requirements:
Write key functional requirements and refrain from spending a lot of time brainstorming and thinking about new
features and auxiliary use cases
Be focused and obtain clarification from the interviewer on the requirements
2. Jot down the non-functional requirements:
One simple way is to just enumerate all the common non-functional requirements and see whether it’s relevant to
the problem and scope.
There are a couple of important points to remember here. Don’t just say general phrases. For example, don’t just
say the system should be highly available, but talk about specifics, such as 99.9% or 99.99% availability.
Similarly, saying that the system should be highly consistent is a very general statement. Instead, talk about
consistency levels for specific sub-use cases.
3. List out the APIs:
Note down the customer-facing and internal system APIs needed for the functional requirements to be satisfied
Preferably you should use REST APIs, but you could use just functions/ methods to keep it simple
4. Do the high-level calculations and estimates:
Make sure the estimates are purposeful – meaning that the calculations should influence your design choices.


Use round numbers closer to powers of 10s, so calculations are easier. For example, 86,400 seconds in a day can
be approximated to 100,000 seconds in a day for easier calculations.
5. Create a high-level block diagram:
Draw a high-level initial block diagram with the major components, such as client device, load balancer, app
server, microservices, and databases.
This will ensure that you have a starting point and the architecture diagram will inform you of the single point of
failure or the major choking points. This is how you would identify what the bottlenecks and core challenges are.
6. Address the core challenges:
Address the bottlenecks and challenges to refine your design
Make sure you are listening to clues provided by your interviewer and that they are on board to do deep dives
into the areas you have identified
7. Draw the final high-level architecture diagram and flow after making the changes to the initial high-level block diagram.
8. Wrap it up by verifying that all the functional and non-functional requirements are satisfied with your final design.
Communicating your solution effectively
As an interviewer for over a decade, I’ve observed that presenting your solution clearly is as
important as the solution itself. I recall many candidates who had brilliant designs for a scalable
system. However, their inability to articulate their ideas effectively made it difficult for the panel
to fully grasp the strengths of their approach. Conversely, I have seen many other candidates
with much simpler designs excelling because they communicated their thought processes and
design decisions with clarity, using diagrams and concise explanations.
So here are some tips for communicating your solution better:
Structure your presentation: Follow a logical structure – state the problem, outline your high-level approach, dive into
components, and discuss trade-offs. Start with the system’s objectives, then describe the architecture, followed by
component details and how they interact.
Highlight key decisions and explain trade-offs: Explain the reasoning behind your choices. Justify why you chose a
particular database or caching strategy based on the requirements. This can be a key differentiator between a senior and a
junior-level candidate.
Listen to the hints and clues provided by the interviewer: It’s a collaborative exercise, and your interviewer is collecting
all the signals needed for them to write up your evaluation. If they are steering the conversation to a particular set of
problems, please listen to them.


Adapt and iterate based on feedback: Be flexible and willing to adapt your design based on the interviewer’s feedback.
Treat the design process as iterative, refining your approach as new information or feedback is received.
Communicate verbally as well as in writing: Write down your thoughts and take advantage of diagrams, blocks, and flows
to explain your thoughts and solution direction. Learn how to speak and write or draw at the same time. Use all the tools and
channels to enhance communication.
Summarize your design: Conclude with a summary of your design, reiterating key points and decisions. Briefly recap the
high-level architecture and main components. Emphasize the strengths of your design and acknowledge any trade-offs or
limitations.
Prepare for follow-up questions: Be ready to answer follow-up questions or delve deeper into specific areas. Be prepared
to discuss details about components, algorithms, and design decisions. Expect questions on how your design handles scaling
and failure scenarios.
Leverage your experience: Use your past experience to inform your design decisions and demonstrate your expertise. Draw
parallels between the problem at hand and similar projects you’ve worked on. Share insights and lessons learned from past
projects, including what worked well and what didn’t.
Keep the other requirements in mind: Consider requirements such as the reliability, observability, debuggability, and
usability of the system design and share your views at the appropriate time, usually at the end, to demonstrate that you care
about these as well.
The ability to present one’s solution is crucial, as it not only demonstrates technical
understanding but also showcases one’s capability to collaborate and convey complex concepts
to others. This can be a deal-breaker in an interview and many times decides the seniority or the
leveling at a company.
Summary
In this chapter, we learned that system design interviews are crucial for senior software
engineering and engineering management roles, assessing your ability to architect scalable,
efficient, and robust systems. Excelling in these interviews not only helps you secure job offers
but also potentially positions you for higher-level roles with greater responsibilities and
compensation.
We looked at some tips for preparing for the interviews. To prepare effectively, start by
understanding the fundamentals of system design. This includes concepts such as scalability,
databases, caching, and consistency models. Familiarize yourself with common design patterns,
such as microservices, event-driven architectures, and SOA. Practicing system design through
mock interviews and design challenges and analyzing case studies of real-world systems is also
essential.


We then moved on to leveraging online resources, including foundational books, courses, blogs,
and YouTube channels, to deepen our understanding and stay updated with best practices. We
learned how honing your communication skills by regularly practicing how to articulate your
design decisions clearly and using visual aids such as diagrams and charts can help you prepare
better.
Then, we moved on to the tips that you should keep in mind while the interview is going on.
During the interview, focus on thoroughly understanding the problem statement by asking
clarifying questions and identifying both functional and non-functional requirements. Break
down the problem into manageable components, define interactions, and use visual aids to
convey your design. Communicate your solution effectively, structure your presentation
logically, highlight key decisions, and be prepared to adapt based on feedback from the
interviewer.
Lastly, we concluded this chapter by sharing how by combining theoretical knowledge, practical
experience, and effective communication, you can excel in system design interviews. Continuous
learning and improvement are key to staying ahead and successfully navigating the complexities
of system design challenges.
In the next chapter, we will share a system design cheat sheet with a lot of quick patterns and
insights that you can brush up on to ace your technical interviews.

## Examples & Scenarios

- levels. For example, a candidate who performs excellently at these system design interviews may
be hired at an L+1 level rather than an L level. That means higher responsibilities, scope, and
compensation.
This chapter offers practical tips and strategies to help you excel in system design interviews,
from understanding the requirements to presenting your solution effectively.
We will cover the following topics in this chapter:
Tips for preparation for system design interviews
Tips for the interview session
Tips for preparation for system design interviews
Preparing for system design interviews requires a strategic approach that combines theoretical

- For example, if you struggled with database design, spend more time studying database architectures and practicing related
problems.
Preparing for system design interviews requires a combination of theoretical knowledge,
practical experience, and effective communication skills. By understanding the fundamentals,
studying common design patterns, practicing regularly, adopting a methodical approach,
leveraging online resources, honing your communication skills, and reflecting on your
performance, you can build the confidence and expertise needed to excel in system design
interviews. Continuous learning and improvement are key to staying ahead and successfully
navigating the complexities of system design challenges.
Tips for the interview session

- constraints, and any ambiguities. For example, if asked to design a chat application, clarify whether the focus is on real-time
messaging, user authentication, or message storage.
Identify functional requirements: List the core functionalities the system must support. For example, for an e-commerce
platform, these might include user registration, product search, shopping cart, and payment processing.

- Component identification: Identify the major components or services required. For example, in a URL shortening service,
the components might include an API gateway, URL storage, redirection service, and analytics.
Define interactions: Determine how these components will interact with each other. For example, the API gateway receives
shortening requests, the storage service saves the mapping, and the redirection service handles redirects.
Use diagrams: Visual aids such as block diagrams or sequence diagrams can help convey your design clearly. For example,
draw an architecture diagram showing how data flows between the user, API gateway, storage, and redirection service.
Key steps to follow
A very high-level set of steps you should take are as follows:
1. Write functional requirements:
Write key functional requirements and refrain from spending a lot of time brainstorming and thinking about new

- There are a couple of important points to remember here. Don’t just say general phrases. For example, don’t just
say the system should be highly available, but talk about specifics, such as 99.9% or 99.99% availability.
Similarly, saying that the system should be highly consistent is a very general statement. Instead, talk about
consistency levels for specific sub-use cases.
3. List out the APIs:
Note down the customer-facing and internal system APIs needed for the functional requirements to be satisfied
Preferably you should use REST APIs, but you could use just functions/ methods to keep it simple
4. Do the high-level calculations and estimates:
Make sure the estimates are purposeful – meaning that the calculations should influence your design choices.

- Use round numbers closer to powers of 10s, so calculations are easier. For example, 86,400 seconds in a day can
be approximated to 100,000 seconds in a day for easier calculations.
5. Create a high-level block diagram:
Draw a high-level initial block diagram with the major components, such as client device, load balancer, app
server, microservices, and databases.
This will ensure that you have a starting point and the architecture diagram will inform you of the single point of
failure or the major choking points. This is how you would identify what the bottlenecks and core challenges are.
6. Address the core challenges:
Address the bottlenecks and challenges to refine your design
Make sure you are listening to clues provided by your interviewer and that they are on board to do deep dives

