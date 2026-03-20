# Benefits of Load Balancing

> Source: System Design - Grokking (Notes), Chapter 243, Pages 68-68

## Key Concepts

- Stuck? Get help on   
DISCUSS
Send feedback
33 Recommendations
Load Balancing
Load Balancer (LB) is another critical component of any distributed system. It helps to spread the
traffic across a cluste

## Content

Stuck? Get help on   
DISCUSS
Send feedback
33 Recommendations
Load Balancing
Load Balancer (LB) is another critical component of any distributed system. It helps to spread the
traffic across a cluster of servers to improve responsiveness and availability of applications, websites or
databases. LB also keeps track of the status of all the resources while distributing requests. If a server
is not available to take new requests or is not responding or has elevated error rate, LB will stop
sending traffic to such a server.
Typically a load balancer sits between the client and the server accepting incoming network and
application traffic and distributing the traffic across multiple backend servers using various
algorithms. By balancing application requests across multiple servers, a load balancer reduces
individual server load and prevents any one application server from becoming a single point of failure,
thus improving overall application availability and responsiveness.
Client
Internet
Load Balancer
Servers
To utilize full scalability and redundancy, we can try to balance the load at each layer of the system. We
can add LBs at three places:
Between the user and the web server
Between web servers and an internal platform layer, like application servers or cache servers
Between internal platform layer and database.
Benefits of Load Balancing

