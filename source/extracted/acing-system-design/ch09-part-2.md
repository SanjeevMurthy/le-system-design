# Part 2

> Source: Acing the System Design Interview (Zhiyong Tan, 2024), Chapter 9, Pages 177-453

## Key Concepts

- Part 2
xxx
In part 1, we learned about common topics in system design interviews. We 
will now go over a series of sample system design interview questions. In each 
question, we apply the concepts we
- 147
7
Design Craigslist
This chapter covers
¡ Designing an application with two distinct types 	
	 of users
¡ Considering geolocation routing for

## Content

Part 2
xxx
In part 1, we learned about common topics in system design interviews. We 
will now go over a series of sample system design interview questions. In each 
question, we apply the concepts we learned in part 1 as well as introducing concepts relevant to the specific question.
We begin with chapter 7 on how to design a system like Craigslist, a system that 
is optimized for simplicity. 
Chapters 8–10 discuss designs of systems that are themselves common components of many other systems. 
Chapter 11 discusses an autocomplete/typeahead service, a typical system that 
continuously ingests and processes large amounts of data into a few megabytes 
data structure that users query for a specific purpose. 
Chapter 12 discusses an image-sharing service. Sharing and interacting with 
images and video are basic functionalities in virtually every social application, 
and a common interview topic. This leads us to the topic of chapter 13, where we 
discuss a Content Distribution Network (CDN), a system that is commonly used 
to cost-efficiently serve static content like images and videos to a global audience. 
Chapter 14 discusses a text messaging app, a system that delivers messages sent 
from many users to many other users and should not accidentally deliver duplicate messages. 
Chapter 15 discusses a room reservation and marketplace system. Sellers 
can offer rooms for rent, and renters can reserve and pay for them. Our system 
must also allow our internal operations staff to conduct arbitration and content 
moderation. 
Chapters 16 and 17 discuss systems that process data feeds. Chapter 16 discusses a news feed system that sorts data for distribution to many interested users, 
while chapter 17 discusses a data analytics service that aggregates large amounts 
of data into a dashboard that can be used to make decisions. 




147
7
Design Craigslist
This chapter covers
¡ Designing an application with two distinct types 	
	 of users
¡ Considering geolocation routing for partitioning 	
	 users
¡ Designing read-heavy vs. write-heavy 	
	
	 applications
¡ Handling minor deviations during the interview
We want to design a web application for classifieds posts. Craigslist is an example of 
a typical web application that may have more than a billion users. It is partitioned 
by geography. We can discuss the overall system, which includes browser and mobile 
apps, a stateless backend, simple storage requirements, and analytics. More use 
cases and constraints can be added for an open-ended discussion. This chapter is 
unique in that it is the only one in this book where we discuss a monolith architecture as a possible system design. 


148
Chapter 7  Design Craigslist
7.1	
User stories and requirements 
Let’s discuss the user stories for Craigslist. We distinguish two primary user types: 
viewer and poster.
A poster should be able to create and delete a post and search their posts as they may 
have many, especially if they were programmatically generated. This post should contain the following information: 
¡ Title.
¡ Some paragraphs of description. 
¡ Price. Assume a single currency and ignore currency conversions. 
¡ Location.
¡ Up to 10 photos of 1 MB each.
¡ Video, though this may be added to a later iteration of our application. 
A poster can renew their post every seven days. They will receive an email notification 
with a click-through to renew their post. 
A viewer should be able to 
1	 View all posts or search in posts within any city made in the last seven days. View a 
list of results, possibly as an endless scroll. 
2	 Apply filters on the results. 
3	 Click an individual post to view its details. 
4	 Contact the poster, such as by email. 
5	 Report fraud and misleading posts (e.g., a possible clickbait technique is to state 
a low price on the post but a higher price in the description). 
The non-functional requirements are as follows: 
¡ Scalable—Up to 10 million users in a single city. 
¡ High availability—99.9% uptime. 
¡ High performance—Viewers should be able to view posts within seconds of creation. Search and viewing posts should have 1 second P99.
¡ Security—A poster should log in before creating a post. We can use an authentication library or service. Appendix B discusses OpenID Connect, which is a popular authentication mechanism. We will not discuss this further in the rest of this 
chapter. 
Most of the required storage will be for Craigslist posts. The amount of required storage is low:
¡ We may show a Craigslist user only the posts in their local area. This means that 
a data center serving any individual user only needs to store a fraction of all the 
posts (though it may also back up posts from other data centers).


	
149
API 
¡ Posts are manually (not programmatically) created, so storage growth will be 
slow. 
¡ We do not handle any programmatically generated data. 
¡ A post may be automatically deleted after one week. 
A low storage requirement means that all the data can fit into a single host, so we do 
not require distributed storage solutions. Let’s assume an average post contains 1,000 
letters or 1 KB of text. If we assume that a big city has 10 million people and 10% of 
them are posters creating an average of 10 posts/day (i.e., 10 GB/day), our SQL database can easily store months of posts. 
7.2	
API 
Let’s scribble down some API endpoints, separated into managing posts and managing users. (In an interview, we have no time to write down a formal API specification 
such as in OpenAPI format or GraphQL schema, so we can tell the interviewer that we 
can use a formal specification to define our API, but in the interest of time we will use 
rough scribbles during the interview. We will not mention this again in the rest of the 
book.) 
CRUD posts:
¡ GET and DELETE /post/{id} 
¡ GET /post?search={search_string}. This can be an endpoint to GET all posts. It 
can have a “search” query parameter to search on posts’ content. We may also 
implement query parameters for pagination, which will be discussed in section 
12.7.1. 
¡ POST and PUT /post
¡ POST /contact 
¡ POST /report 
¡ DELETE /old_posts
User management: 
¡ POST /signup. We do not need to discuss user account management. 
¡ POST /login 
¡ DELETE /user 
Other:
¡ GET /health. Usually automatically generated by the framework. Our implementation can be as simple as making a small GET request and verifying it returns 
200, or it can be detailed and include statistics like P99 and availability of various 
endpoints. 


150
Chapter 7  Design Craigslist
There are various filters, which may vary by the product category. For simplicity, we 
assume a fixed set of filters. Filters can be implemented both on the frontend and 
backend: 
¡ Neighborhood: enum 
¡ Minimum price 
¡ Maximum price 
¡ Item condition: enum. Values include NEW, EXCELLENT, GOOD, and 
ACCEPTABLE. 
The GET /post endpoint can have a “search” query parameter to search on posts. 
7.3	
SQL database schema 
We can design the following SQL schema for our Craigslist user and post data. 
¡ User: id PRIMARY KEY, first_name text, last_name text, signup_ts integer 
¡ Post: This table is denormalized, so JOIN queries are not required to get all the 
details of a post. id PRIMARY KEY, created_at integer, poster_id integer, location_id integer, title text, description text, price integer, condition text, country_code char(2), state text, city text, street_number integer, street_name text, 
zip_code text, phone_number integer, email text
¡ Images: id PRIMARY KEY, ts integer, post_id integer, image_address text
¡ Report: id PRIMARY KEY, ts integer, post_id integer, user_id integer, abuse_type 
text, message text 
¡ Storing images: We can store images on an object store. AWS S3 and Azure Blob 
Storage are popular because they are reliable, simple to use and maintain, and 
cost-efficient. 
¡ image_address: The identifier used to retrieve an image from the object store. 
When low latency is required, such as when responding to user queries, we usually use 
SQL or in-memory databases with low latency such as Redis. NoSQL databases that use 
distributed file systems such as HDFS are for large data-processing jobs. 
7.4	
Initial high-level architecture 
Referring to figure 7.1, we can discuss multiple possibilities for our initial Craigslist design, in order of complexity. We will discuss these two designs in the next two 
sections.
1	 A monolith that uses a user authentication service for authentication and an 
object store for storing posts. 
2	 A client frontend service, a backend service, a SQL service, an object store, and a 
user authentication service.


	
151
A monolith architecture
In all designs, we also include a logging service because logging is almost always a must, 
so we can effectively debug our system. For simplicity, we can exclude monitoring and 
alerting. However, most cloud vendors provide logging, monitoring, and alerting tools 
that are easy to set up, and we should use them.
Monolith
SQL
Object Store
Client
Backend
SQL
Object Store
Figure 7.1    Simple initial designs for our high-level architecture. (Top) Our high-level architecture 
consists of just a monolith and an object store. (Bottom) A conventional high-level architecture with a 
UI frontend service and a backend service. Image files are stored in an object store, which clients make 
requests to. The rest of a post is stored in SQL.
7.5	
A monolith architecture
Our first suggested design to use a monolith is unintuitive, and the interviewer may 
even be taken aback. One is unlikely to use monolith architecture for web services 
in their career. However, we should keep in mind that every design decision is about 
tradeoffs and not be afraid to suggest such designs and discuss tradeoffs.
We can implement our application as a monolith that contains both the UI and the 
backend functionality and store entire webpages in our object store. A key design decision is that we can store a post’s webpage in its entirety in the object store, including the 
post’s photos. Such a design decision means that we may not use many of the columns 
of the Post table discussed in section 7.3; we will use this table for the high-level architecture illustrated at the bottom of figure 7.1, which we discuss later in this chapter. 
Referring to figure 7.2, the home page is static, except for the location navigation 
bar (containing a regional location such as “SF bay area” and links to more specific locations such as “sfc,” “sby,” etc.), and the “nearby cl” section that has a list of other cities. 
Other sites are static, including the sites on the left navigation bar, such as “craigslist 
app” and “about craigslist,” and the sites on the bottom navigation bar, such as “help,” 
“safety,” “privacy,” etc., are static. 


152
Chapter 7  Design Craigslist
Figure 7.2    A Craigslist homepage. (Source: https://sfbay.craigslist.org/) 
This approach is simple to implement and maintain. Its main tradeoffs are:
1	 HTML tags, CSS, and JavaScript are duplicated on every post.
2	 If we develop a native mobile app, it cannot share a backend with the browser 
app. A possible solution is to develop a progressive web app (discussed in section 
6.5.3), which is installable on mobile devices and can be used on web browsers on 
any device. 
3	 Any analytics on posts will require us to parse the HTML. This is only a minor 
disadvantage. We can develop and maintain our own utility scripts to fetch post 
pages and parse the HTML.
A disadvantage of the first tradeoff is that additional storage is required to store the 
duplicate page components. Another disadvantage is that new features or fields cannot 
be applied to old posts, though since posts are automatically deleted after one week, 
this may be acceptable depending on our requirements. We can discuss this with our 
interviewer as an example of how we should not assume any requirement when designing a system.


	
153
Migrations are troublesome
We can partially mitigate the second tradeoff by writing the browser app using a 
responsive design approach and implementing the mobile app as a wrapper around the 
browser app using WebViews. https://github.com/react-native-webview/react-native 
-webview is a WebView library for React Native. https://developer.android.com/ 
reference/android/webkit/WebView is the WebView library for native Android, and 
https://developer.apple.com/documentation/webkit/wkwebview is the WebView 
library for native iOS. We can use CSS media queries (https://developer.mozilla.org/
en-US/docs/Learn/CSS/CSS_layout/Responsive_Design#media_queries) to display 
different page layouts for phone displays, tablet displays, and laptop and desktop displays. This way, we do not need to use UI components from a mobile framework. A 
comparison of UX between using this approach versus the conventional approach of 
using the UI components in mobile development frameworks is outside the scope of 
this book.
For authentication on the backend service and Object Store Service, we can use a 
third-party user authentication service or maintain our own. Refer to appendix B for a 
detailed discussion of Simple Login and OpenID Connect authentication mechanisms.
7.6	
Using an SQL database and object store
The bottom diagram of figure 7.1 shows a more conventional high-level architecture. 
We have a UI frontend service that makes requests to a backend service and an object 
store service. The backend service makes requests to an SQL service.
In this approach, the object store is for image files, while the SQL database stores 
the rest of a post’s data as discussed in section 7.4. We could have simply stored all data 
in the SQL database, including images, and not had an object store at all. However, 
this will mean that a client must download image files through the backend host. This 
is an additional burden on the backend host, increases image download latency, and 
increases the overall possibility of download failures from sudden network connectivity 
problems. 
If we wish to keep our initial implementation simple, we can consider going without 
the feature to have images on posts and add the object store when we wish to implement 
this feature.
That being said, because each post is limited to 10 image files of 1 MB each, and we 
will not store large image files, we can discuss with the interviewer whether this requirement may change in the future. We can suggest that if we are unlikely to require larger 
images, we can store the images in SQL. The image table can have a post_id text column and an image blob column. An advantage of this design is its simplicity. 
7.7	
Migrations are troublesome
While we are on the subject of choosing the appropriate data stores for our non-functional requirements, let’s discuss the problem of data migrations before we proceed 
with discussing other features and requirements.
Another disadvantage of storing image files on SQL is that in the future we will have 
to migrate to storing them on an object store. Migration from one data store to another 
is generally troublesome and tedious. 


154
Chapter 7  Design Craigslist
Let’s discuss a possible simple migration process, assuming the following:
1	 We can treat both data stores as single entities. That is, replication is abstracted 
away from us, and we do not need to consider how data is distributed across various data centers to optimize for non-functional requirements like latency or 
availability. 
2	 Downtime is permissible. We can disable writes to our application during the 
data migration, so users will not add new data to the old data store while data is 
being transferred from the old data store to the new data store.
3	 We can disconnect/terminate requests in progress when the downtime begins, 
so users who are making write (POST, PUT, DELETE) requests will receive 500 
errors. We can give users advance notification of this downtime via various channels, such as email, browser and mobile push notifications, or a banner notification on the client.
We can write a Python script that runs on a developer’s laptop to read records from 
one store and write it to another store. Referring to figure 7.3, this script will make 
GET requests to our backend to get the current data records and POST requests to 
our new object store. Generally, this simple technique is suitable if the data transfer 
can complete within hours and only needs to be done once. It will take a developer a 
few hours to write this script, so it may not be worth it for the developer to spend more 
time improving the script to speed up the data transfer.
We should expect that our migration job may stop suddenly due to bugs or network 
problems, and we will need to restart the script execution. The write endpoints should 
be idempotent to prevent duplicate records from being written to our new data store. 
The script should do checkpointing, so it does not reread and rewrite records that have 
already been transferred. A simple checkpointing mechanism will suffice; after each 
write, we can save the object’s ID to our local machine’s hard disk. If the job fails midway, the job can resume from the checkpoint when we restart it (after fixing bugs if 
necessary).
Local machine
Get checkpoint
Old data store
Data record
GET
POST
New data store
Success
loop
Figure 7.3    Sequence 
diagram of a simple data 
migration process. The 
local machine first finds the 
checkpoint if there is any, 
then makes the relevant 
requests to move each 
record from the old data 
store to the new data store.


	
155
Migrations are troublesome
An alert reader will notice that for this checkpoint mechanism to work, the script needs 
to read the records in the same order each time it is run. There are many possible ways 
to achieve this, including the following:
¡ If we can obtain a complete and sorted list of our records’ IDs and store it in our 
local machine’s hard disk, our script can load this list into memory before commencing the data transfer. Our script fetches each record by its ID, writes it to the 
new data store, and records on our hard disk that this ID has been transferred. 
Because hard disk writes are slow, we can write/checkpoint these completed 
IDs in batches. With this batching, a job may fail before a batch of IDs has been 
checkpointed, so these objects may be reread and rewritten, and our idempotent 
write endpoints prevent duplicate records. 
¡ If our data objects have any ordinal (indicates position) fields such as timestamps, 
our script can checkpoint using this field. For example, if we checkpoint by date, 
our script first transfers the records with the earliest date, checkpoints this date, 
increments the date, transfers the records with this date, and so on, until the 
transfer is complete. 
This script must read/write the fields of the data objects to the appropriate tables and 
columns. The more features we add before a data migration, the more complex the 
migration script will be. More features mean more classes and properties. There will be 
more database tables and columns, we will need to author a larger number of ORM/
SQL queries, and these query statements will also be more complex and may have 
JOINs between tables.
If the data transfer is too big to complete with this technique, we will need to run 
the script within the data center. We can run it separately on each host if the data is distributed across multiple hosts. Using multiple hosts allows the data migration to occur 
without downtime. If our data store is distributed across many hosts, it is because we 
have many users, and in these circumstances, downtime is too costly to revenue and 
reputation. 
To decommission the old data store one host at a time, we can follow these steps on 
each host.
1	 Drain the connections on the host. Connection draining refers to allowing existing requests to complete while not taking on new requests. Refer to sources like 
https://cloud.google.com/load-balancing/docs/enabling-connection-draining, 
https://aws.amazon.com/blogs/aws/elb-connection-draining-remove-instances 
-from-service-with-care/, and https://docs.aws.amazon.com/elasticloadbalancing/ 
latest/classic/config-conn-drain.html for more information on connection 
draining.
2	 After the host is drained, run the data transfer script on the host.
3	 When the script has finished running, we no longer need this host. 


156
Chapter 7  Design Craigslist
How should we handle write errors? If this migration takes many hours or days to complete, it will be impractical if the transfer job crashes and terminates each time there is 
an error with reading or writing data. Our script should instead log the errors and continue running. Each time there is an error, log the record that is being read or written, 
and continue reading and writing the other records. We can examine the errors, fix 
bugs, if necessary, then rerun the script to transfer these specific records.
A lesson to take away from this is that a data migration is a complex and costly exercise that should be avoided if possible. When deciding which data stores to use for a 
system, unless we are implementing this system as a proof-of-concept that will handle 
only a small amount of data (preferably unimportant data that can be lost or discarded 
without consequences), we should set up the appropriate data stores at the beginning, 
rather than set them up later then have to do a migration.
7.8	
Writing and reading posts
Figure 7.4 is a sequence diagram of a poster writing a post, using the architecture in 
section 7.6. Although we are writing data to more than one service, we will not require 
distributed transaction techniques for consistency. The following steps occur:
1	 The client makes a POST request to the backend with the post, excluding the 
images. The backend writes the post to the SQL database and returns the post ID 
to the client.
2	 The client can upload the image files one at a time to the object store, or fork 
threads to make parallel upload requests.
Client
Backend
Post ID.
Write post.
SQL
Success
loop
Object Store
POST /post.
Success
POST /file
Figure 7.4    Sequence diagram of writing a new post, where the client handles image uploads
In this approach, the backend returns 200 success without knowing if the image files 
were successfully uploaded to the object store. For the backend to ensure that the 
entire post is uploaded successfully, it must upload the images to the object store itself. 


	
157
Writing and reading posts
Figure 7.5 illustrates such an approach. The backend can only return 200 success to 
the client after all image files are successfully uploaded to the object store, just in case 
image file uploads are unsuccessful. This may occur due to reasons such as the backend host crashing during the upload process, network connectivity problems, or if the 
object store is unavailable.
Client
Backend
Post ID.
Write post.
Success
SQL
Success
loop
Object Store
POST /post.
POST /file
Figure 7.5    Sequence diagram of writing a new post, where the backend handles image uploads
Let’s discuss the tradeoffs of either approach. Advantages of excluding the backend 
from the image uploads include
¡ Fewer resources—We push the burden of uploading images onto the client. If 
image file uploads went through our backend, our backend must scale up with 
our object store. 
¡ Lower overall latency—The image files do not need to go through an additional 
host. If we decide to use a CDN to store images, this latency problem will become 
even worse because clients cannot take advantage of CDN edges close to their 
locations.
Advantages of including the backend in the image uploads are as follows:
¡ We will not need to implement and maintain authentication and authorization 
mechanisms on our object store. Because the object store is not exposed to the 
outside world, our system has a smaller overall attack surface.
¡ Viewers are guaranteed to be able to view all images of a post. In the previous 
approach, if some or all images are not successfully uploaded, viewers will not 
see them when they view the post. We can discuss with the interviewer if this is an 
acceptable tradeoff.
One way to capture most of the advantages of both approaches is for clients to write 
image files to the backend but read image files from the CDN. 


158
Chapter 7  Design Craigslist
QUESTION   What are the tradeoffs of uploading each image file in a separate 
request vs. uploading all the files in a single request? 
Does the client really need to upload each image file in a separate request? This complexity may be unnecessary. The maximum size of a write request will be slightly more 
than 10 MB, which is small enough to be uploaded in seconds. But this means that 
retries will also be more expensive. Discuss these tradeoffs with the interviewer.
The sequence diagram of a viewer reading a post is identical to figure 7.4, except that 
we have GET instead of POST requests. When a viewer reads a post, the backend fetches 
the post from the SQL database and returns it to the client. Next, the client fetches and 
displays the post’s images from the object store. The image fetch requests can be parallel, so the files are stored on different storage hosts and are replicated, and they can be 
downloaded in parallel from separate storage hosts. 
7.9	
Functional partitioning 
The first step in scaling up can be to employ functional partitioning by geographical 
region, such as by city. This is commonly referred to as geolocation routing, serving traffic based on the location DNS queries originate from the geographic location of our 
users, for example. We can deploy our application into multiple data centers and route 
each user to the data center that serves their city, which is also usually the closest data 
center. So, the SQL cluster in each data center contains only the data of the cities that 
it serves. We can implement replication of each SQL cluster to two other SQL services 
in different data centers as described with MySQL’s binlog-based replication (refer to 
section 4.3.2). 
Craigslist does this geographical partitioning by assigning a subdomain to each city 
(e.g., sfbay.craigslist.org, shanghai.craiglist.org, etc). If we go to craigslist.org in our 
browser, the following steps occur. An example is shown on figure 7.6. 
1	 Our internet service provider does a DNS lookup for craigslist.org and returns its 
IP address. (Browsers and OS have DNS caches, so the browser can use its DNS 
cache or the OS’s DNS cache for future DNS lookups, which is faster than sending this DNS lookup request to the ISP.)
2	 Our browser makes a request to the IP address of craigslist.org. The server determines our location based on our IP address, which is contained in the address, 
and returns a 3xx response with the subdomain that corresponds to our location. 
This returned address can be cached by the browser and other intermediaries 
along the way, such as the user’s OS and ISP.
3	 Another DNS lookup is required to obtain the IP address of this subdomain. 
4	 Our browser makes a request to the IP address of the subdomain. The server 
returns the webpage and data of that subdomain. 


	
159
Caching 
Browser near
San Francisco.
ISP
craigslist.org IP address.
Request for craigslist.org.
craigslist.org
sfbay.craigslist.org
Request
sfbay domain IP address.
Request
Response
DNS lookup
Figure 7.6    Sequence diagram for using GeoDNS to direct user requests to the appropriate IP address
We can use GeoDNS for our Craigslist. Our browser only needs to do a DNS lookup 
once for craigslist.org, and the IP address returned will be the data center that corresponds to our location. Our browser can then make a request to this data center to get 
our city’s posts. Instead of having a subdomain specified in our browser’s address bar, 
we can state the city in a drop-down menu on our UI. The user can select a city in this 
drop-down menu to make a request to the appropriate data center and view that city’s 
posts. Our UI can also provide a simple static webpage page that contains all Craigslist 
cities, where a user can click through to their desired city. 
Cloud services such as AWS (https://docs.aws.amazon.com/Route53/latest/
DeveloperGuide/routing-policy-geo.html) provide guides to configuring geolocation 
routing. 
7.10	 Caching 
Certain posts may become very popular and receive a high rate of read requests, for 
example, a post that shows an item with a much lower price than its market value. To 
ensure compliance with our latency SLA (e.g., 1-second P99) and prevent 504 timeout 
errors, we can cache popular posts. 
We can implement an LRU cache using Redis. The key can be a post ID, and the 
value is the entire HTML page of a post. We may implement an image service in front 
of the object store, so it can contain its own cache mapping object identifiers to images. 
The static nature of posts limits potential cache staleness, though a poster may 
update their post. If so, the host should refresh the corresponding cache entry. 


160
Chapter 7  Design Craigslist
7.11	 CDN 
Referring to figure 7.7, we can consider using a CDN, although Craigslist has very little 
static media (i.e., images and video) that are shown to all users. The static contents it 
does have are CSS and JavaScript files, which are only a few MB in total. We can also 
use browser caching for the CSS and JavaScript files. (Browser caching was discussed in 
section 4.10.) 
Client
Backend
SQL
Object Store
Cache
CDN
Figure 7.7    Our Craigslist architecture diagram after adding our cache and CDN 
7.12	 Scaling reads with a SQL cluster 
It is unlikely that we will need to go beyond functional partitioning and caching. If we 
do need to scale reads, we can follow the approaches discussed in chapter 3, one of 
which is SQL replication.
7.13	 Scaling write throughput 
At the beginning of this chapter, we stated that this is a read-heavy application. It is 
unlikely that we will need to allow programmatic creation of posts. This section is a 
hypothetical situation where we do allow it and perhaps expose a public API for post 
creation. 
If there are traffic spikes in inserting and updating to the SQL host, the required 
throughput may exceed its maximum write throughput. Referring to https://stackoverflow.com/questions/2861944/how-to-do-very-fast-inserts-to-sql-server-2008, 
certain SQL implementations offer methods for fast INSERT for example, SQL Server’s 
ExecuteNonQuery achieves thousands of INSERTs per second. Another solution is to 
use batch commits instead of individual INSERT statements, so there is no log flush overhead for each INSERT statement.


	
161
Email service 
Use a message broker like Kafka
To handle write traffic spikes, we can use a streaming solution like Kafka, by placing a 
Kafka service in front of the SQL services. 
Figure 7.8 shows a possible design. When a poster submits a new or updated post, the 
hosts of the Post Writer Service can produce to the Post topic. The service is stateless 
and horizontally scalable. We can create a new service we name “Post Writer” that continuously consumes from the Post topic and writes to the SQL service. This SQL service 
can use leader-follower replication, which was discussed in chapter 3.
Post topic
SQL leader
Post writer/
consumer
Post 
producer 0
Post Producer Service
Load balancer
Post 
producer 1
Post 
producer n
New/updated post
Figure 7.8    Using horizontal scaling and a message broker to handle write traffic spikes
The main tradeoffs of this approach are complexity and eventual consistency. Our 
organization likely has a Kafka service that we can use, so we don’t have to create our 
own Kafka service, somewhat negating the complexity. Eventual consistency duration 
increases as writes will take longer to reach the SQL followers. 
If the required write throughput exceeds the average write throughput of a single 
SQL host, we can do further functional partitioning of SQL clusters and have dedicated 
SQL clusters for categories with heavy write traffic. This solution is not ideal because 
the application logic for viewing posts will need to read from particular SQL clusters 
depending on category. Querying logic is no longer encapsulated in the SQL service 
but present in the application, too. Our SQL service is no longer independent on our 
backend service, and maintenance of both services becomes more complex. 
If we need higher write throughput, we can use a NoSQL database such as Cassandra 
or Kafka with HDFS. 
We may also wish to discuss adding a rate limiter (refer to chapter 8) in front of our 
backend cluster to prevent DDoS attacks.
7.14	 Email service 
Our backend can send requests to a shared email service for sending email. 
To send a renewal reminder to posters when a post is seven days old, this can be 
implemented as a batch ETL job that queries our SQL database for posts that are seven 
days old and then requests the email service to send an email for each post. 
The notification service for other apps may have requirements such as handling 
unpredictable traffic spikes, low latency, and notifications should be delivered within a 
short time. Such a notification service is discussed in the next chapter. 


162
Chapter 7  Design Craigslist
7.15	 Search 
Referring to section 2.6, we create an Elasticsearch index on the Post table for users to 
search posts. We can discuss if we wish to allow the user to filter the posts before and 
after searching, such as by user, price, condition, location, recency of post, etc., and we 
make the appropriate modifications to our index. 
7.16	 Removing old posts 
Craigslist posts expire after a certain number of days, upon which the post is no longer 
accessible. This can be implemented with a cron job or Airflow, calling the DELETE /
old_posts endpoint daily. DELETE /old_posts may be its own endpoint separate 
from DELETE /post/{id} because the latter is a single simple database delete operation, while the former contains more complex logic to first compute the appropriate 
timestamp value then delete posts older than this timestamp value. Both endpoints 
may also need to delete the appropriate keys from the Redis cache. 
This job is simple and non-critical because it is acceptable for posts that were supposed to be deleted to continue to be accessible for days, so a cron job may be sufficient, 
and Airflow may introduce unneeded complexity. We must be careful not to accidentally delete posts before they are due, so any changes to this feature must be thoroughly 
tested in staging before a deployment to production. The simplicity of cron over a complex workflow management platform like Airflow improves maintainability, especially if 
the engineer who developed the feature has moved on and maintenance is being done 
by a different engineer. 
Removing old posts or deletion of old data in general has the following advantages: 
¡ Monetary savings on storage provisioning and maintenance. 
¡ Database operations, such as reads and indexing, are faster. 
¡ Maintenance operations that require copying all data to a new location are faster, 
less complex, and lower cost, such as adding or migrating to a different database 
solution. 
¡ Fewer privacy concerns for the organization and limiting the effect of data 
breaches, though this advantage is not strongly felt since this is public data. 
Disadvantages: 
¡ Prevents analytics and useful insights that may be gained from keeping the data. 
¡ Government regulations may make it necessary to keep data for a certain period. 
¡ A tiny probability that the deleted post’s URL may be used for a newer post, and 
a viewer may think they are viewing the old post. The probability of such events is 
higher if one is using a link-shortening service. However, the probability of this is 
so low, and it has little user effect, so this risk is acceptable. This risk will be unacceptable if sensitive personal data may be exposed. 


	
163
Summary of our architecture discussion so far
If cost is a problem and old data is infrequently accessed, an alternative to data deletion may be compression followed by storing on low-cost archival hardware such as 
tape, or an online data archival service like AWS Glacier or Azure Archive Storage. 
When certain old data is required, it can be written onto disk drives prior to data processing operations. 
7.17	 Monitoring and alerting 
Besides what was discussed in section 2.5, we should monitor and send alerts for the 
following: 
¡ Our database monitoring solution (discussed in chapter 10) should trigger a 
low-urgency alert if old posts were not removed. 
¡ Anomaly detection for: 
–	 Number of posts added or removed. 
–	 High number of searches for a particular term. 
–	 Number of posts flagged as inappropriate. 
7.18	 Summary of our architecture discussion so far
Figure 7.9 shows our Craigslist architecture with many of the services we have discussed, namely the client, backend, SQL, cache, notification service, search service, 
object store, CDN, logging, monitoring, alerting, and batch ETL. 
Client
Backend
SQL
Object Store
Cache
CDN
Notification 
Service
Search
Logging
Monitoring
Alerting
Batch ETL
Figure 7.9    Our Craigslist 
architecture with notification 
service, search, logging, 
monitoring, and alerting. 
Logging, monitoring, and 
alerting can serve many 
other components, so on our 
diagram, they are shown as 
loose components. We can 
define jobs on the batch ETL 
service for purposes such as to 
periodically remove old posts. 


164
Chapter 7  Design Craigslist
7.19	 Other possible discussion topics 
Our system design fulfills the requirements stated at the beginning of this chapter. The 
rest of the interview may be on new constraints and requirements.
7.19.1	 Reporting posts
We have not discussed the functionality for users to report posts because it is straightforward. Such a discussion may include a system design to fulfill such requirements:
¡ If a certain number of reports are made, the post is taken down, and the poster 
receives an email notification.
¡ A poster’s account and email may be automatically banned, so the poster cannot 
log in to Craigslist or create posts. However, they can continue viewing posts without logging in and can continue sending emails to other posters.
¡ A poster should be able to contact an admin to appeal this decision. We may need 
to discuss with the interviewer if we need a system to track and record these interactions and decisions.
¡ If a poster wishes to block emails, they will need to configure their own email 
account to block the sender’s email address. Craigslist does not handle this.
7.19.2	 Graceful degradation 
How can we handle a failure on each component? What are the possible corner cases 
that may cause failures and how may we handle them? 
7.19.3	 Complexity 
Craigslist is designed to be a simple classifieds app that is optimized for simplicity of 
maintenance by a small engineering team. The feature set is deliberately limited and 
well-defined, and new features are seldomly introduced. We may want to discuss strategies to achieve this.
Minimize dependencies
Any app that contains dependencies to libraries and/or services naturally atrophies 
over time and requires developers to maintain it just to keep providing its current 
functionality. Old library versions and occasionally entire libraries are deprecated, and 
services can be decommissioned, necessitating that developers install a later version 
or find alternatives. New library versions or service deployments may also break our 
application. Library updates may also be necessary if bugs or security flaws are found in 
the currently used libraries. Minimizing our system’s feature set minimizes its dependencies, which simplifies debugging, troubleshooting, and maintenance. 
This approach requires an appropriate company culture that focuses on providing the minimal useful set of features that do not require extensive customization for 
each market. For example, possibly the main reason that Craigslist does not provide 
payments is that the business logic to handle payments can be different in each city. 


	
165
Other possible discussion topics 
We must consider different currencies, taxes, payment processors (MasterCard, Visa, 
PayPal, WePay, etc.), and constant work is required to keep up with changes in these 
factors. Many big tech companies have engineering cultures that reward program managers and engineers for conceptualizing and building new services; such a culture is 
unsuitable for us here.
Use cloud services
In figure 7.9, other than the client and backend, every service can be deployed on 
a cloud service. For example, we can use the following AWS services for each of the 
services in figure 7.9. Other cloud vendors like Azure or GCP provide similar services:
¡ SQL: RDS (https://aws.amazon.com/rds/) 
¡ Object Store: S3 (https://aws.amazon.com/s3/) 
¡ Cache: ElastiCache (https://aws.amazon.com/elasticache/)
¡ CDN: CloudFront (https://www.amazonaws.cn/en/cloudfront/)
¡ Notification service: Simple Notification Service (https://aws.amazon.com/sns)
¡ Search: CloudSearch (https://aws.amazon.com/cloudsearch/) 
¡ Logging, monitoring, and alerting: CloudWatch (https://aws.amazon.com/
cloudwatch/)
¡ Batch ETL: Lambda functions with rate and cron expressions (https://docs.aws 
.amazon.com/lambda/latest/dg/services-cloudwatchevents-expressions.html)
Storing entire webpages as HTML documents
A webpage usually consists of an HTML template with interspersed JavaScript functions that make backend requests to fill in details. In the case of Craigslist, a post’s 
HTML page template may contain fields such as title, description, price, photo, etc., 
and each field’s value can be filled in with JavaScript. 
The simple and small design of Craigslist’s post webpage allows the simpler alternative we first discussed in section 7.5, and we can discuss it further here. A post’s webpage can be stored as a single HTML document in our database or CDN. This can be 
as simple as a key-value pair where the key is the post’s ID, and the value is the HTML 
document. This solution trades off some storage space because there will be duplicate 
HTML in every database entry. Search indexes can be built against this list of post IDs. 
This approach also makes it less complex to add or remove fields from new posts. If 
we decide to add a new required field (e.g., subtitle), we can change the fields without 
a SQL database migration. We don’t need to modify the fields in old posts, which have a 
retention period and will be automatically deleted. The Post table is simplified, replacing a post’s fields with the post’s CDN URL. The columns become “id, ts, poster_id, 
location_id, post_url”.
Observability
Any discussion of maintainability must emphasize the importance of observability, discussed in detail in section 2.5. We must invest in logging, monitoring, alerting, automated testing and adopt good SRE practices, including good monitoring dashboards, 
runbooks, and automation of debugging.


166
Chapter 7  Design Craigslist
7.19.4	 Item categories/tags 
We can provide item categories/tags, such as “automotive,” “real estate,” “furniture,” 
etc., and allow posters to place up to a certain number of tags (e.g., three) on a listing. 
We can create a SQL dimension table for tags. Our Post table can have a column for a 
comma-separated tag list. An alternative is to have an associative/junction table “post_
tag,” as shown in figure 7.10. 
post
id
PK
other columns...
tag
id
PK
other columns...
post_tag
post_id
FK
tag_id
FK
Figure 7.10    Associative/junction table for posts and tags. This schema normalization maintains 
consistency by avoiding duplicate data. If the data is in a single table, there will be duplicate values 
across rows. 
We can expand this from a flat list to a hierarchical list, so users can apply more precise 
filters to view posts that are more relevant to their interests. For example, “real estate” 
may have the following nested subcategories. 
¡ Real estate > Transaction type > Rent 
¡ Real estate > Transaction type > Sale
¡ Housing type > Apartment 
¡ Housing type > Single-family house 
¡ Housing type > Townhouse 
7.19.5	 Analytics and recommendations 
We can create daily batch ETL jobs that query our SQL database and populate dashboards for various metrics: 
¡ Number of items by tag. 
¡ Tags that received the most clicks. 
¡ Tags that got the highest number of viewers contacting posters. 
¡ Tags with the fastest sales, which may be measured by how soon the poster 
removed the post after posting it. 
¡ Numbers and geographical and time distributions of reported, suspected, and 
confirmed fraudulent posts. 


	
167
Other possible discussion topics 
Craigslist does not offer personalization, and posts are ordered starting from most 
recent. We may discuss personalization, which includes tracking user activity and recommending posts.
7.19.6	 A/B testing 
As briefly discussed in section 1.4.5, as we develop new features and aesthetic designs 
in our application, we may wish to gradually roll them out to an increasing percentage 
of users, rather than to all users at once. 
7.19.7	 Subscriptions and saved searches 
We may provide an API endpoint for viewers to save search terms (with a character 
limit) and notify them (by email, text message, in-app message, etc.) of any new posts 
that match their saved searches. A POST request to this endpoint can write a row (timestamp, user_id, search_term) to a SQL table we name “saved_search”.
This saved search subscription service can be a complex system in itself, as described 
in this section. 
A user should receive a single daily notification that covers all their saved searches. 
This notification may consist of a list of search terms and up to 10 corresponding results 
for each search term. Each result in turn consists of a list of post data for that search 
term. The data can include a link to the post and some summary information (title, 
price, first 100 characters of the description) to display in the notification. 
For example, if a user has two saved search terms, “san francisco studio apartment” 
and “systems design interview book,” the notification may contain the following. (You 
certainly do not write down all of this during an interview. You can scribble down some 
quick snippets and verbally describe what they mean.) 
[  
  { 
    "search_term": "san francisco studio apartment", 
    "results": [ 
      { 
        "link": "sfbay.craigslist.org/12345", 
        "title": "Totally remodeled studio", 
        "price": 3000, 
        "description_snippet": "Beautiful cozy studio apartment in the 
Mission. Nice views in a beautiful and safe neighborhood. Clo" 
      }, 
      { 
        "link": "sfbay.craigslist.org/67890" 
        "title": "Large and beautiful studio", 
        "price": 3500, 
        "description_snippet": "Amenities\nComfortable, open floor plan\nIn 
unit laundry\nLarge closets\nPet friendly\nCeiling fan\nGar" 
      }, 
      ... 
    ] 
  }, 
  { 


168
Chapter 7  Design Craigslist
    "search_term": "systems design interview book", 
    "results": [ 
      ... 
    ] 
  } 
] 
To send the users new results for their saved searches, we can implement a daily batch 
ETL job. We can suggest at least two ways to implement this job: a simpler way that 
allows duplicate requests to the search service and another more complex way that 
avoids these duplicate requests. 
7.19.8	 Allow duplicate requests to the search service 
Elasticsearch caches frequent search requests (https://www.elastic.co/blog/elasticsearch 
-caching-deep-dive-boosting-query-speed-one-cache-at-a-time), so frequent requests with 
the same search terms do not waste many resources. Our batch ETL job can process 
users and their individual saved search terms one at a time. Each process consists of 
sending a user’s search terms as separate requests to the search service, consolidating 
the results, then sending a request to a notification service (the subject of chapter 9). 
7.19.9	 Avoid duplicate requests to the search service 
Our batch ETL job runs the following steps: 
1	 Deduplicate the search terms, so we only need to run a search on each term once. 
We can run a SQL query like SELECT DISTINCT LOWER(search_term) FROM 
saved_search WHERE timestamp >= UNIX_TIMESTAMP(DATEADD(CURDATE(), 
INTERVAL -1 DAY)) AND timestamp < UNIX_TIMESTAMP(CURDATE()) to 
deduplicate yesterday’s search terms. Our search can be case-insensitive, so we 
lowercase the search terms as part of deduplication. Since our Craigslist design is 
partitioned by city, we should not have more than 100M search terms. Assuming 
an average of 10 characters per search term, there will be 1 GB of data, which 
easily fits into a single host’s memory.  
2	 For each search term: 
a	 Send a request to the (Elasticsearch) search service and get the results. 
b	 Query the “saved_search” table for the user IDs associated with this search 
term. 
c	 For each (user ID, search term, results) tuple, send a request to a notification 
service. 
What if the job fails during step 2? How do we avoid resending notifications to users? 
We can use a distributed transaction mechanism described in chapter 5. Or we can 
implement logic on the client that checks if a notification has already been displayed 
(and possibly dismissed) before displaying the notification. This is possible for certain 
types of clients like a browser or mobile app, but not for email or texting. 


	
169
Other possible discussion topics 
If saved searches expire, we can clean up old table rows with a daily batch job that 
runs a SQL DELETE statement on rows older than the expiry date. 
7.19.10	Rate limiting 
All requests to our service can pass through a rate limiter to prevent any individual user 
from sending requests too frequently and thus consuming too many resources. The 
design of a rate limiter is discussed in chapter 8. 
7.19.11	Large number of posts 
What if we would like to provide a single URL where all listings are accessible to anyone (regardless of location)? Then the Post table may be too big for a single host, and 
the Elasticsearch index for posts may also be too big for a single host. However, we 
should continue to serve a search query from a single host. Any design where a query 
is processed by multiple hosts and results aggregated in a single host before returning them to the viewer will have high latency and cost. How can we continue to serve 
search queries from a single host? Possibilities include: 
¡ Impose a post expiry (retention period) of one week and implement a daily 
batch job to delete expired posts. A short retention period means there is less 
data to search and cache, reducing the system’s costs and complexity.
¡ Reduce the amount of data stored in a post. 
¡ Do functional partitioning on categories of posts. Perhaps create separate SQL 
tables for various categories. But the application may need to contain the mappings to the appropriate table. Or this mapping can be stored in a Redis cache, 
and the application will need to query the Redis cache to determine which table 
to query. 
¡ We may not consider compression because it is prohibitively expensive to search 
compressed data. 
7.19.12	Local regulations 
Each jurisdiction (country, state, county, city, etc.) may have its own regulations that 
affect Craigslist. Examples include: 
¡ The types of products or services permitted on Craigslist may differ by jurisdiction. How could our system handle this requirement? Section 15.10.1 discusses a 
possible approach. 
¡ Customer data and privacy regulations may not allow the company to export customer data outside of the country. It may be required to delete customer data 
on customer demand or share data with governments. These considerations are 
likely outside the scope of the interview. 
We will need to discuss the exact requirements. Is it sufficient to selectively display 
certain products and services sections on the client applications based on the user’s 


170
Chapter 7  Design Craigslist
location, or do we also need to prevent users from viewing or posting about banned 
products and services?
An initial approach to selectively display sections will be to add logic in the clients to 
display or hide sections based on the country of the user’s IP address. Going further, if 
these regulations are numerous or frequently changing, we may need to create a regulations service that Craigslist admins can use to configure regulations, and the clients 
will make requests to this service to determine which HTML to show or hide. Because 
this service will receive heavy read traffic and much lighter write traffic, we can apply 
CQRS techniques to ensure that writes succeed. For example, we can have separate 
regulation services for admins and viewers that scale separately and periodic synchronization between them.
If we need to ensure that no forbidden content is posted on our Craigslist, we may 
need to discuss systems that detect forbidden words or phrases, or perhaps machine 
learning approaches.
A final thought is that Craigslist does not attempt to customize its listings based on 
country. A good example was how it removed its Personals section in 2018 in response 
to new regulations passed in the United States. It did not attempt to keep this section in 
other countries. We can discuss the tradeoffs of such an approach.
Summary
¡ We discuss the users and their various required data types (like text, images, or 
video) to determine the non-functional requirements, which in our Craigslist 
system are scalability, high availability, and high performance. 
¡ A CDN is a common solution for serving images or video, but don’t assume it is 
always the appropriate solution. Use an object store if these media will be served 
to a small fraction of users.
¡ Functional partitioning by GeoDNS is the first step in discussing scaling up.
¡ Next are caching and CDN, mainly to improve the scalability and latency of serving posts. 
¡ Our Craigslist service is read-heavy. If we use SQL, consider leader-follower replication for scaling reads. 
¡ Consider horizontal scaling of our backend and message brokers to handle write 
traffic spikes. Such a setup can serve write requests by distributing them across 
many backend hosts, and buffer them in a message broker. A consumer cluster 
can consume requests from the message broker and process them accordingly. 
¡ Consider batch or streaming ETL jobs for any functionality that don’t require 
real-time latency. This is slower, but more scalability and lower cost. 
¡ The rest of the interview may be on new constraints and requirements. In this 
chapter, the new constraints and requirements we mentioned were reporting 
posts, graceful degradation, decreasing complexity, adding categories/tags of 
posts, analytics and recommendations, A/B testing, subscriptions and saved 
searches, rate limiting, serving more posts to each user, and local regulations.


171
8
Design a 
rate-limiting service
This chapter covers
¡ Using rate limiting
¡ Discussing a rate-limiting service
¡ Understanding various rate-limiting algorithms
Rate limiting is a common service that we should almost always mention during a 
system design interview and is mentioned in most of the example questions in this 
book. This chapter aims to address situations where 1) the interviewer may ask for 
more details when we mention rate limiting during an interview, and 2) the question itself is to design a rate-limiting service. 
Rate limiting defines the rate at which consumers can make requests to API endpoints. Rate limiting prevents inadvertent or malicious overuse by clients, especially 
bots. In this chapter, we refer to such clients as “excessive clients”. 
Examples of inadvertent overuse include the following: 
¡ Our client is another web service that experienced a (legitimate or malicious) 
traffic spike.
¡ The developers of that service decided to run a load test on their production 
environment.
Such inadvertent overuse causes a “noisy neighbor” problem, where a client utilizes too much resource on our service, so our other clients will experience higher 
latency or higher rate of failed requests. 


172
Chapter 8  Design a rate-limiting service 
Malicious attacks include the following. There are other bot attacks that rate limiting does not prevent(see https://www.cloudflare.com/learning/bots/what-is-bot 
-management/ for more information) 
¡ Denial-of-service (DoS) or distributed denial-of-service (DDoS) attacks—DoS floods a 
target with requests, so normal traffic cannot be processed. DoS uses a single 
machine, while DDoS is the use of multiple machines for the attack. This distinction is unimportant in this chapter, and we refer to them collectively as “DoS”. 
¡ Brute force attack—A brute force attack is repeated trial and error to find sensitive data, such as cracking passwords, encryption keys, API keys, and SSH login 
credentials. 
¡ Web scraping—Web scraping uses bots to make GET requests to many web pages 
of a web application to obtain a large amount of data. An example is scraping 
Amazon product pages for prices and product reviews.
Rate limiting can be implemented as a library or as a separate service called by a frontend, API gateway, or service mesh. In this question, we implement it as a service to 
gain the advantages of functional partitioning discussed in chapter 6. Figure 8.1 illustrates a rate limiter design that we will discuss in this chapter. 
API 
Gateway
Backend
Rules 
service
SQL
Users
(other services)
Redis
Rules 
service
users
Figure 8.1    Initial high-level architecture of rate limiter. The frontend, backend, and Rules service also 
log to a shared logging service; this is not shown here. The Redis database is usually implemented as 
a shared Redis service, rather than our service provisioning its own Redis database. The Rules service 
users may make API requests to the Rules service via a browser app. We can store the rules in SQL. 
8.1	
Alternatives to a rate-limiting service and why they are infeasible 
Why don’t we scale out the service by monitoring the load and adding more hosts 
when needed, instead of doing rate limiting? We can design our service to be horizontally scalable, so it will be straightforward to add more hosts to serve the additional 
load. We can consider auto-scaling. 
The process of adding new hosts when a traffic spike is detected may be too slow. 
Adding a new host involves steps that take time, like provisioning the host hardware, 


	
173
Alternatives to a rate-limiting service and why they are infeasible 
downloading the necessary Docker containers, starting up the service on the new host, 
then updating our load balancer configuration to direct traffic to the new host. This 
process may be too slow, and our service may already have crashed by the time the new 
hosts are ready to serve traffic. Even auto-scaling solutions may be too slow. 
A load balancer can limit the number of requests sent to each host. Why don’t we use 
our load balancer to ensure that hosts are not overloaded and drop requests when our 
cluster has no more spare capacity? 
We should not serve malicious requests, as we mentioned previously. Rate limiting 
guards against such requests by detecting their IP addresses and simply dropping them. 
As discussed later, our rate limiter can usually return 429 Too Many Requests, but if we 
are sure that certain requests are malicious, we can choose either of these options: 
¡ Drop the request and not return any response and allow the attacker to think 
that our service is experiencing an outage. 
¡ Shadow ban the user by returning 200 with an empty or misleading response. 
Why does rate limiting need to be a separate service? Can each host independently 
track the request rate from its requestors, and rate limit them? 
The reason is that certain requests are more expensive than others. Certain users 
may make requests that return more data, require more expensive filtering and aggregation, or involve JOIN operations between larger datasets. A host may become slow 
from processing expensive requests from particular clients. 
A level 4 load balancer cannot process a request’s contents. We will need a level 7 
load balancer for sticky sessions (to route requests from a user to the same host), which 
introduces cost and complexity. If we do not have other use cases for a level 7 load balancer, it may not be worth it to use level 7 load balancer just for this purpose, and a dedicated and shared rate limiting service may be a better solution. Table 8.1 summarizes 
our discussion. 
Table 8.1    Comparison of rate limiting to its alternatives 
Rate limiting
Add new hosts
Use level 7 load balancer
Handles traffic spikes by 
returning 429 Too Many 
Requests responses to the 
users with high request 
rates. 
Adding new hosts may be 
too slow to respond to traffic spikes. Our service may 
crash by the time the new 
hosts are ready to serve 
traffic. 
Not a solution to handle 
traffic spikes. 
Handles DoS attacks 
by providing misleading 
responses. 
Processes malicious 
requests, which we should 
not do. 
Not a solution. 
Can rate limit users who 
make expensive requests. 
Causes our service to incur 
the costs of processing 
expensive requests. 
Can reject expensive 
requests but may be too 
costly and complex as a 
standalone solution. 


174
Chapter 8  Design a rate-limiting service 
8.2	
When not to do rate limiting 
Rate limiting is not necessarily the appropriate solution for any kind of client overuse. 
For example, consider a social media service we designed. A user may subscribe to 
updates associated with a particular hashtag. If a user makes too many subscription 
requests within a certain period, the social media service may respond to the user, “you 
have made too many subscription requests within the last few minutes.” If we did rate 
limiting, we will simply drop the user’s requests and return 429 (Too Many Requests) 
or return nothing, and the client decides the response is 500. This will be a poor user 
experience. If the request is sent by a browser or mobile app, the app can display to the 
user that they sent too many requests, providing a good user experience. 
Another example is services that charge subscription fees for certain request rates 
(e.g., different subscription fees for 1,000 or 10,000 hourly requests). If a client exceeds 
its quota for a particular time interval, further requests should not be processed until 
the next time interval. A shared rate-limiting service is not the appropriate solution to 
prevent clients from exceeding their subscriptions. As discussed in more detail below, 
the shared rate-limiting service should be limited to supporting simple use cases, not 
complex use cases like giving each client a different rate limit. 
8.3	
Functional requirements 
Our rate-limiting service is a shared service, and our users are mainly services that are 
used by parties external to the company and not by internal users such as employees. 
We refer to such services as “user services.” A user should be able to set a maximum 
request rate over which further requests from the same requestor will be delayed or 
rejected, with a 429 response. We can assume the interval can be 10 seconds or 60 seconds. We can set a maximum of 10 requests in 10 seconds. Other functional requirements are as follows: 
¡ We assume that each user service must rate limit its requestors across its hosts, but 
we do not need to rate limit the same users across services. Rate limiting is independent on each user service. 
¡ A user can set multiple rate limits, one per endpoint. We do not need more complicated user-specific configurations, such as allowing different rate limits to 
particular requestors/users. We want our rate limiter to be a cheap and scalable 
service that is easy to understand and use. 
¡ Our users should be able to view which users were rate limited and the timestamps these rate limiting events began and ended. We provide an endpoint for 
this. 
¡ We can discuss with the interviewer whether we should log every request because 
we will need a large amount of storage to do so, which is expensive. We will 
assume that this is needed and discuss techniques to save storage to reduce cost. 
¡ We should log the rate-limited requestors for manual follow-up and analytics. 
This is especially required for suspected attacks. 


	
175
Non-functional requirements 
8.4	
Non-functional requirements 
Rate limiting is a basic functionality required by virtually any service. It must be scalable, have high performance, be as simple as possible, secure, and private. Rate limiting is not essential to a service’s availability, so we can trade off high availability and 
fault-tolerance. Accuracy and consistency are fairly important but not stringent.  
8.4.1	
Scalability 
Our service should be scalable to billions of daily requests that query whether a particular requestor should be rate limited. Requests to change rate limits will only be 
manually made by internal users in our organization, so we do not need to expose this 
capability to external users.
How much storage is required? Assume our service has one billion users, and we 
need to store up 100 requests per user at any moment. Only the user IDs and a queue 
of 100 timestamps per user need to be recorded; each is 64 bits. Our rate limiter is a 
shared service, so we will need to associate requests with the service that is being rate 
limited. A typical big organization has thousands of services. Let’s assume up to 100 of 
them need rate limiting. 
We should ask whether our rate limiter actually needs to store data for one billion 
users. What is the retention period? A rate limiter usually should only need to store data 
for 10 seconds because it makes a rate limiting decision based on the user’s request rate 
for the last 10 seconds. Moreover, we can discuss with the interviewer whether there will 
be more than 1–10 million users within a 10-second window. Let’s make a conservative 
worst-case estimate of 10 million users. Our overall storage requirement is 100 * 64 * 
101 * 10M = 808 GB. If we use Redis and assign a key to each user, a value’s size will be 
just 64 * 100 = 800 bytes. It may be impractical to delete data immediately after it is older 
than 10 seconds, so the actual amount of required storage depends on how fast our service can delete old data.
8.4.2	
Performance 
When another service receives a request from its user (we refer to such requests as 
user requests), it makes a request to our rate limiting service (we refer to such requests 
as rate limiter requests) to determine if the user request should be rate-limited. The rate 
limiter request is blocking; the other service cannot respond to its user before the rate 
limiter request is completed. The rate limiter request’s response time adds to the user 
request’s response time. So, our service needs very low latency, perhaps a P99 of 100 
ms. The decision to rate-limit or not rate-limit the user request must be quick. We 
don’t require low latency for viewing or analytics of logs. 
8.4.3	
Complexity 
Our service will be a shared service, used by many other services in our organization. 
Its design should be simple to minimize the risk of bugs and outages, aid troubleshooting, allow it to focus on its single functionality as a rate limiter, and minimize costs. 
Developers of other services should be able to integrate our rate limiting solution as 
simply and seamlessly as possible. 


176
Chapter 8  Design a rate-limiting service 
8.4.4	
Security and privacy 
Chapter 2 discussed security and privacy expectations for external and internal services. Here, we can discuss some possible security and privacy risks. The security and 
privacy implementations of our user services may be inadequate to prevent external 
attackers from accessing our rate limiting service. Our (internal) user services may also 
attempt to attack our rate limiter, for example, by spoofing requests from another user 
service to rate limit it. Our user services may also violate privacy by requesting data 
about rate limiter requestors from other user services. 
For these reasons, we will implement security and privacy in our rate limiter’s system 
design. 
8.4.5	
Availability and fault-tolerance 
We may not require high availability or fault-tolerance. If our service has less than three 
nines availability and is down for an average of a few minutes daily, user services can 
simply process all requests during that time and not impose rate limiting. Moreover, 
the cost increases with availability. Providing 99.9% availability is fairly cheap, while 
99.99999% may be prohibitively expensive.
As discussed later in this chapter, we can design our service to use a simple highly 
available cache to cache the IP addresses of excessive clients. If the rate-limiting service 
identified excessive clients just prior to the outage, this cache can continue to serve 
rate-limiter requests during the outage, so these excessive clients will continue to be 
rate limited. It is statistically unlikely that an excessive client will occur during the few 
minutes the rate limiting service has an outage. If it does occur, we can use other techniques such as firewalls to prevent a service outage, at the cost of a negative user experience during these few minutes. 
8.4.6	
Accuracy 
To prevent poor user experience, we should not erroneously identify excessive clients 
and rate limit them. In case of doubt, we should not rate limit the user. The rate limit 
value itself does not need to be precise. For example, if the limit is 10 requests in 10 
seconds, it is acceptable to occasionally rate limit a user at 8 or 12 requests in 10 seconds. If we have an SLA that requires us to provide a minimum request rate, we can set 
a higher rate limit (e.g., 12+ requests in 10 seconds). 
8.4.7	
Consistency 
The previous discussion on accuracy leads us to the related discussion on consistency. We do not need strong consistency for any of our use cases. When a user service 
updates a rate limit, this new rate limit need not immediately apply to new requests; a 
few seconds of inconsistency may be acceptable. Eventual consistency is also acceptable for viewing logged events such as which users were rate-limited or performing 
analytics on these logs. Eventual rather than strong consistency will allow a simpler and 
cheaper design. 


	
177
High-level architecture
8.5	
Discuss user stories and required service components 
A rate-limiter request contains a required user ID and a user service ID. Since rate limiting is independent on each user service, the ID format can be specific to each user 
service. The ID format for a user service is defined and maintained by the user service, 
not by our rate-limiting service. We can use the user service ID to distinguish possible 
identical user IDs from different user services. Because each user service has a different rate limit, our rate limiter also uses the user service ID to determine the rate limit 
value to apply. 
Our rate limiter will need to store this (user ID, service ID) data for 60 seconds, since 
it must use this data to compute the user’s request rate to determine if it is higher than 
the rate limit. To minimize the latency of retrieving any user’s request rate or any service’s rate limit, these data must be stored (or cached) on in-memory storage. Because 
consistency and latency are not required for logs, we can store logs on an eventually 
consistent storage like HDFS, which has replication to avoid data loss from possible host 
failures. 
Last, user services can make infrequent requests to our rate-limiting service to create 
and update rate limits for their endpoints. This request can consist of a user service ID, 
endpoint ID, and the desired rate limit (e.g., a maximum of 10 requests in 10 seconds). 
Putting these requirements together, we need the following: 
¡ A database with fast reads and writes for counts. The schema will be simple; it 
is unlikely to be much more complex than (user ID, service ID). We can use an 
in-memory database like Redis. 
¡ A service where rules can be defined and retrieved, which we call the Rules 
service. 
¡ A service that makes requests to the Rules service and the Redis database, which 
we can call the Backend service. 
The two services are separate because requests to the Rules service for adding or modifying rules should not interfere with requests to the rate limiter that determine if a 
request should be rate limited. 
8.6	
High-level architecture
Figure 8.2 (repeated from figure 8.1) illustrates our high-level architecture considering these requirements and stories. When a client makes a request to our rate-limiting 
service, this request initially goes through the frontend or service mesh. If the frontend’s security mechanisms allow the request, the request goes to the backend, where 
the following steps occur: 
1	 Get the service’s rate limit from the Rules service. This can be cached for lower 
latency and lower request volume to the Rules service. 
2	 Determine the service’s current request rate, including this request. 
3	 Return a response that indicates if the request should be rate-limited. 


178
Chapter 8  Design a rate-limiting service 
Steps 1 and 2 can be done in parallel to reduce overall latency by forking a thread for 
each step or using threads from a common thread pool. 
The frontend and Redis (distributed cache) services in our high-level architecture in 
figure 8.2 are for horizontal scalability. This is the distributed cache approach discussed 
in section 3.5.3. 
API 
Gateway
Backend
Rules 
service
SQL
Users
(other services)
Redis
Rules 
service
users
Figure 8.2    Initial high-level architecture of rate limiter. The frontend, backend, and Rules service also 
log to a shared logging service; this is not shown here. The Redis database is usually implemented as 
a shared Redis service, rather than our service provisioning its own Redis database. The Rules service 
users may make API requests to the Rules service via a browser app. 
We may notice in figure 8.2 that our Rules service has users from two different services 
(Backend and Rules service users) with very different request volumes, one of which 
(Rules service users) does all the writes. 
Referring back to the leader-follower replication concepts in sections 3.3.2 and 3.3.3, 
and illustrated in figure 8.3, the Rules service users can make all their SQL queries, 
both reads and writes to the leader node. The backend should make its SQL queries, 
which are only read/SELECT queries, to the follower nodes. This way, the Rules service 
users have high consistency and experience high performance.
Leader
Follower 0
Follower 1
Follower n
All requests from Rules 
service users, and all writes
Rules Service
Reads from backend
Figure 8.3    The leader host should process all requests from Rules service users, and all write 
operations. Reads from the backend can be distributed across the follower hosts. 


	
179
High-level architecture
Referring to figure 8.4, as we do not expect rules to change often, we can add a Redis 
cache to the Rules service to improve its read performance even further. Figure 8.4 
displays cache-aside caching, but we can also use other caching strategies from section 
3.8. Our Backend service can also cache rules in Redis. As discussed earlier in section 
8.4.5, we can also cache the IDs of excessive users. As soon as a user exceeds its rate 
limit, we can cache its ID along with an expiry time where a user should no longer 
be rate-limited. Then our backend need not query the Rules service to deny a user’s 
request. 
If we are using AWS (Amazon Web Services), we can consider DynamoDB instead of 
Redis and SQL. DynamoDB can handle millions of requests per second (https:// 
aws.amazon.com/dynamodb/), and it can be either eventually consistent or strongly 
consistent (https://docs.aws.amazon.com/whitepapers/latest/comparing-dynamodb 
-and-hbase-for-nosql/consistency-model.html), but using it subjects us to vendor 
lock-in. 
Frontend
Backend
Rules 
service
SQL
Users
(other services)
Redis
Rules 
service
users
Redis
cache
Figure 8.4    Rate limiter with Redis cache on the Rules service. Frequent requests from the backend can 
be served from this cache instead of the SQL database. 
The backend has all our non-functional requirements. It is scalable, has high performance, is not complex, is secure and private, and is eventually consistent. The SQL 
database with its leader-leader replication is highly available and fault-tolerant, which 
goes beyond our requirements. We will discuss accuracy in a later section. This design is 
not scalable for the Rules service users, which is acceptable as discussed in section 8.4.1.
Considering our requirements, our initial architecture may be overengineered, 
overly complex, and costly. This design is highly accurate and strongly consistent, both 
of which are not part of our non-functional requirements. Can we trade off some accuracy and consistency for lower cost? Let’s first discuss two possible approaches to scaling 
up our rate limiter: 
1	 A host can serve any user, by not keeping any state and fetching data from a 
shared database. This is the stateless approach we have followed for most questions in this book. 
2	 A host serves a fixed set of users and stores its user’s data. This is a stateful 
approach that we discuss in the next section. 


180
Chapter 8  Design a rate-limiting service 
8.7	
Stateful approach/sharding
Figure 8.5 illustrates the backend of a stateful solution that is closer to our non-functional requirements. When a request arrives, our load balancer routes it to its host. 
Each host stores the counts of its clients in its memory. The host determines if the user 
has exceeded their rate limit and returns true or false. If a user makes a request and its 
host is down, our service will return a 500 error, and the request will not be rate limited. 
Level 7
Load 
balancer
Host 0
Host 1
Host N
To Rules service
From Frontend
Backend
Figure 8.5    Backend architecture of rate limiter that employs a stateful sharded approach. The counts 
are stored in the hosts’ memory, rather than in a distributed cache like Redis. 
A stateful approach requires a level 7 load balancer. This may seem to contradict what 
we discussed in section 8.1 about using a level 7 load balancer, but note that we are now 
discussing using it in a distributed rate-limiting solution, not just for sticky sessions to 
allow each host to reject expensive requests and perform its own rate limiting.
A question that immediately arises in such an approach is fault-tolerance, whether we 
need to safeguard against data loss when a host goes down. If so, this leads to discussions 
on topics like replication, failover, hot shards, and rebalancing. As briefly discussed in 
section 3.1, we can use sticky sessions in replication. But in our requirements discussion 
earlier in the chapter, we discussed that we don’t need consistency, high availability, 
or fault-tolerance. If a host that contains certain users’ data goes down, we can simply 
assign another host to those users and restart the affected users’ request rate counts 
from 0. Instead, the relevant discussion will be on detecting host outages, assigning and 
provisioning replacement hosts, and rebalancing traffic. 
The 500 error should trigger an automated response to provision a new host. Our 
new host should fetch its list of addresses from the configuration service, which can 
be a simple manually updated file stored on a distributed object storage solution like 
AWS S3 (for high availability, this file must be stored on a distributed storage solution 
and not on a single host), or a complex solution like ZooKeeper. When we develop our 
rate-limiting service, we should ensure that the host setup process does not exceed a 


	
181
Stateful approach/sharding
few minutes. We should also have monitoring on the host setup duration and trigger a 
low-urgency alert if the setup duration exceeds a few minutes. 
We should monitor for hot shards and periodically rebalance traffic across our hosts. 
We can periodically run a batch ETL job that reads the request logs, identifies hosts that 
receive large numbers of requests, determines an appropriate load balancing configuration, and then writes this configuration to a configuration service. The ETL job can 
also push the new configuration to the load-balancer service. We write to a configuration service in case any load balancer host goes down. When the host recovers or a new 
load balancer host is provisioned, it can read the configuration from the configuration 
service. 
Figure 8.6 illustrates our backend architecture with the rebalancing job. This rebalancing prevents a large number of heavy users from being assigned to a particular host, 
causing it to go down. Since our solution does not have failover mechanisms that distribute the users of a failed host over other hosts, we do not have the risk of a death spiral, where a host fails because of excessive traffic, then its traffic is redistributed over the 
remaining hosts and increases their traffic, which in turn causes them to fail. 
Level 7
Load
balancer
Host 0
Host 1
Host N
To Rules service
From Frontend
Backend
Configuration
Service
Rebalancing 
ETL job
Logging 
Service
Figure 8.6    Backend architecture with a rebalancing ETL job 
A tradeoff of this approach is that it is less resilient to DoS/DDoS attacks. If a user has 
a very high request rate, such as hundreds of requests per second, its assigned host 
cannot handle this, and all users assigned to this host cannot be rate limited. We may 


182
Chapter 8  Design a rate-limiting service 
choose to have an alert for such cases, and we should block requests from this user 
across all services. Load balancers should drop requests from this IP address—that is, 
do not send the requests to any backend host, and do not return any response, but do 
log the request. 
Compared to the stateless approach, the stateful approach is more complex and has 
higher consistency and accuracy, but has lower: 
¡ Cost 
¡ Availability 
¡ Fault-tolerance 
Overall, this approach is a poor cousin of a distributed database. We attempted to 
design our own distributed storage solution, and it will not be as sophisticated or 
mature as widely used distributed databases. It is optimized for simplicity and low cost 
and has neither strong consistency nor high availability.
8.8	
Storing all counts in every host
The stateless backend design discussed in section 8.6 used Redis to store request 
timestamps. Redis is distributed, and it is scalable and highly available. It also has low 
latency and will be an accurate solution. However, this design requires us to use a Redis 
database, which is usually implemented as a shared service. Can we avoid our dependency on an external Redis service, which will expose our rate limiter to possible degradation on that service?
The stateful backend design discussed in section 8.7 avoids this lookup by storing 
state in the backend, but it requires the load balancer to process every request to determine which host to send it to, and it also requires reshuffling to prevent hot shards. 
What if we can reduce the storage requirement such that all user request timestamps 
can fit in memory on a single host? 
8.8.1	
High-level architecture
How can we reduce the storage requirement? We can reduce our 808 GB storage 
requirement to 8.08 GB ≈ 8 GB by creating a new instance of our rate-limiting service 
for each of the ~100 services that uses it and use the frontend to route requests by 
service to the appropriate service. 8 GB can fit into a host’s memory. Due to our high 
request rate, we cannot use a single host for rate limiting. If we use 128 hosts, each host 
will store only 64 MB. The final number we decide upon will likely be between 1 and 
128.
Figure 8.7 is the backend architecture of this approach. When a host receives a 
request, it does the following in parallel:
¡ Makes a rate-limiting decision and returns it.
¡ Asynchronously synchronizes its timestamps with other hosts. 


	
183
Storing all counts in every host
Level 4
Load 
balancer
Host 0
Host 1
Host N
To Rules service
From Frontend
Backend
To synchronization 
mechanism
Figure 8.7    High-level architecture of a rate-limiting service where all user request timestamps can 
fit into a single backend host, requests are randomly load balanced across hosts, and each host can 
respond to a user request with a rate limiting decision without first making requests to other services or 
hosts. Hosts synchronize their timestamps with each other in a separate process.
Our level 4 load balancer randomly balances requests across hosts, so a user may be 
directed to different hosts in each rate limiting request. For rate limits to be accurately computed, the rate limits on our hosts need to be kept synchronized. There are 
multiple possible ways to synchronize the hosts. We discuss them in detail in the next 
section. Here we’ll just say that we will use streaming instead of batch updates because 
batch updates are too infrequent and cause users to be rate-limited at a much higher 
request rate than the set request rate. 
Compared to the other two designs discussed earlier (the stateless backend design 
and stateful backend design), this design trades off consistency and accuracy for lower 
latency and higher performance (it can process a higher request rate). Because a host 
may not have all the timestamps in memory before making a rate-limiting decision, it 
may compute a lower request rate than the actual value. It also has these characteristics:
¡ Use a level 4 load balancer to direct requests to any host like a stateless service 
(though the frontend).
¡ A host can make rate limiting decisions with its data in memory.
¡ Data synchronization can be done in an independent process. 
What if a host goes down and its data is lost? Certain users who will be rate limited will 
be permitted to make more requests before they are rate limited. As discussed earlier, 
this is acceptable. Refer to pp. 157–158 of Martin Kleppmann’s book Designing Data-Intensive Systems for a brief discussion on leader failover and possible problems. Table 8.2 
summarizes our comparison between the three approaches that we have discussed. 


184
Chapter 8  Design a rate-limiting service 
Table 8.2    Comparison of our stateless backend design, stateful backend design, and design that stores 
counts in every host 
Stateless backend design
Stateful backend design
Storing counts in every host
Stores counts in a distributed 
database.
Stores each user’s count in a 
backend host.
Store every user’s counts in 
every host. 
Stateless, so a user can be 
routed to any host. 
Requires a level 7 load balancer 
to route each user to its assigned 
host. 
Every host has every user’s 
counts, so a user can be routed 
to any host. 
Scalable. We rely on the distributed database to serve both high 
read and high write traffic. 
Scalable. A load balancer is an 
expensive and vertically scalable 
component that can handle a 
high request rate. 
Not scalable because each host 
needs to store the counts of 
every user. Need to divide users 
into separate instances of this 
service and require another 
component (such as a frontend) 
to route users to their assigned 
instances. 
Efficient storage consumption. 
We can configure our desired 
replication factor in our distributed database. 
Lowest storage consumption 
because there is no backup by 
default. We can design a storage service with an in-cluster 
or out-cluster approach, as 
discussed in section 13.5. Without backup, it is the cheapest 
approach. 
Most expensive approach. High 
storage consumption. Also, high 
network traffic from n–n communication between hosts to 
synchronize counts. 
Eventually consistent. A host 
making a rate limiting decision 
may do so before synchronization is complete, so this decision 
may be slightly inaccurate. 
Most accurate and consistent 
since a user always makes 
requests to the same hosts. 
Least accurate and consistent 
approach because it takes time 
to synchronize counts between 
all hosts. 
Backend is stateless, so we use 
the highly available and fault-tolerant properties of the distributed database. 
Without backup, any host failure will result in data loss of 
all the user counts it contains. 
This is the lowest availability 
and fault-tolerant of the three 
designs. However, these factors 
may be inconsequential because 
they are not non-functional 
requirements. If the rate limiter 
cannot obtain an accurate count, 
it can simply let the request 
through. 
Hosts are interchangeable, so 
this is the most highly available 
and fault-tolerant of the three 
designs. 
Dependent on external database 
service. Outages of such services may affect our service, and 
remediating such outages may 
be outside our control. 
Not dependent on external database services. Load balancer 
needs to process every request 
to determine which host to send 
it to. This also requires reshuffling to prevent hot shards. 
Not dependent on external 
database services like Redis. 
Avoids risk of service outage 
from outages of such downstream services. Also, it’s easier 
to implement, particularly in big 
organizations where provisioning 
or modifying database services 
may involve considerable 
bureaucracy. 


	
185
Storing all counts in every host
8.8.2	
Synchronizing counts
How can the hosts synchronize their user request counts? In this section, we discuss 
a few possible algorithms. All the algorithms except all-to-all are feasible for our rate 
limiter.
Should the synchronization mechanism be pull or push? We can choose push to 
trade off consistency and accuracy for higher performance, lower resource consumption, and lower complexity. If a host goes down, we can simply disregard its counts and 
allow users to make more requests before they are rate-limited. With these considerations, we can decide that hosts should asynchronously share their timestamps using 
UDP instead of TCP.
We should consider that hosts must be able to handle their traffic from these two 
main kinds of requests:
1	 Request to make a rate limiting decision. Such requests are limited by the load 
balancer and by provisioning a larger cluster of hosts as necessary.
2	 Request to update the host’s timestamps in memory. Our synchronization mechanism must ensure that a host does not receive a high rate of requests, especially 
as we increase the number of hosts in our cluster. 
All-to-all
All-to-all means every node transmits messages to every other node in a group. It is 
more general than broadcasting, which refers to simultaneous transfer of the message to 
recipients. Referring to figure 3.3 (repeated in figure 8.8), all-to-all requires a full mesh 
topology, where every node in a network is connected to every other node. All-to-all 
scales quadratically with the number of nodes, so it is not scalable. If we use all-to-all 
communication with 128 hosts, each all-to-call communication will require 128 * 128 * 
64 MB, which is > 1 TB, which is infeasible. 
Figure 8.8    A full mesh 
topology. Every node in 
a network is connected 
to every other node. In 
our rate limiter, every 
node receives user 
requests, computes 
request rate, and 
approves or denies the 
request. 
Gossip protocol
In gossip protocol, referring to figure 3.6 (repeated in figure 8.9), nodes periodically randomly pick other nodes and send them messages. Yahoo’s distributed rate 


186
Chapter 8  Design a rate-limiting service 
limiter uses gossip protocol to synchronize its hosts (https://yahooeng.tumblr.com/
post/111288877956/cloud-bouncer-distributed-rate-limiting-at-yahoo). This approach 
trades off consistency and accuracy for higher performance and lower resource consumption. It is also more complex.
Figure 8.9    Gossip 
protocol. Each node 
periodically randomly 
picks other nodes and 
sends them messages.
In this section, all-to-all and gossip protocol are the synchronization mechanisms that 
require all nodes to send messages directly to each other. This means that all nodes 
must know the IP addresses of the other nodes. Since nodes are continuously added 
and removed from the cluster, each node will make requests to the configuration service (such as ZooKeeper) to find the other nodes’ IP addresses.
In the other synchronization mechanisms, hosts make requests to each other via a 
particular host or service.
External storage or coordination service
Referring to figure 8.10 (almost identical to figure 3.4), these two approaches use 
external components for hosts to communicate with each other.
Hosts can communicate with each other via a leader host. This host is selected by the 
cluster’s configuration service (such as ZooKeeper). Each host only needs to know the 
IP address of the leader host, while the leader host needs to periodically update its list 
of hosts.
External storage / 
Coordination Service
Figure 8.10    Hosts can 
communicate through 
an external component, 
such as an external 
storage service or 
coordination service.
Random leader selection
We can trade off higher resource consumption for lower complexity by using a simple 
algorithm to elect a leader. Referring to figure 3.7 (repeated in figure 8.11), this may 
cause multiple leaders to be elected. As long as each leader communicates with all 


	
187
Rate-limiting algorithms 
other hosts, every host will be updated with the all the request timestamps. There will 
be unnecessary messaging overhead.
Leader
Leader
Figure 8.11    Random 
leader selection may cause 
multiple leaders to be 
elected. This will cause 
unnecessary messaging 
overhead but does not 
present other problems.
8.9	
Rate-limiting algorithms 
Up to this point, we have assumed that a user’s request rate is determined by its request 
timestamps, but we have not actually discussed possible techniques to compute the 
request rate. At this point, one of the main questions is how our distributed rate-limiting service determines the requestor’s current request rate. Common rate-limiting 
algorithms include the following: 
¡ Token bucket 
¡ Leaky bucket 
¡ Fixed window counter 
¡ Sliding window log 
¡ Sliding window counter 
Before we continue, we note that certain system design interview questions may seem 
to involve specialized knowledge and expertise that most candidates will not have prior 
experience with. The interviewer may not expect us to be familiar with rate-limiting 
algorithms. This is an opportunity for them to assess the candidate’s communication 
skills and learning ability. The interviewer may describe a rate limiting algorithm to us 
and assess our ability to collaborate with them to design a solution around it that satisfies our requirements. 
The interviewer may even make sweeping generalizations or erroneous statements, 
and assess our ability to critically evaluate them and tactfully, firmly, clearly, and concisely ask intelligent questions and express our technical opinions. 
We can consider implementing more than one rate-limiting algorithm in our service 
and allow each user of this service to choose a rate-limiting algorithm to select the algorithm that most closely suits the user’s requirements. In this approach, a user selects the 
desired algorithm and sets the desired configurations in the Rules service. 
For simplicity of discussion, the discussions of the rate limiting algorithms in this 
section assume that the rate limit is 10 requests in 10 seconds.


188
Chapter 8  Design a rate-limiting service 
8.9.1	
Token bucket 
Referring to figure 8.12, the token bucket algorithm is based on an analogy of a bucket 
filled with tokens. A bucket has three characteristics: 
¡ A maximum number of tokens. 
¡ The number of currently available tokens. 
¡ A refill rate at which tokens are added to the bucket. 
Bucket
Token
Token
Token
Token
Each request 
removes 1 token.
Each second, if < 10 tokens, add 1 token.
Figure 8.12    A token bucket that enqueues once per second
Each time a request arrives, we remove a token from the bucket. If there are no tokens, 
the request is rejected or rate limited. The bucket is refilled at a constant rate. 
In a straightforward implementation of this algorithm, the following occurs with 
each user request. A host can store key-value pairs using a hash map. If the host does 
not have a key for this user ID, the system initializes an entry with a user ID and a token 
count of 9 (10–1). If the host has a key for this user ID and its value is more than 0, the 
system decrements its count. If the count is 0, it returns true, i.e., the user should be rate 
limited. If it returns false, the user should not be rate limited. Our system also needs to 
increment every value by 1 each second if it is less than 10.
The advantages of token bucket are that it is easy to understand and implement, and 
it is memory efficient (each user only needs a single integer variable to count tokens). 
One obvious consideration with this implementation is that each host will need to 
increment every key in the hash map. It is feasible to do this on a hash map in a host’s 
memory. If the storage is external to the host, such as on a Redis database, Redis provides the MSET (https://redis.io/commands/mset/) command to update multiple 


	
189
Rate-limiting algorithms 
keys, but there may be a limit on the number of keys that can be updated in a single 
MSET operation (https://stackoverflow.com/questions/49361876/mset-over-400-000 
-map-entries-in-redis). (Stack Overflow is not an academically credible source, and the 
official Redis documentation on MSET does not state an upper limit on the number 
of keys in a request. However, when designing a system, we must always ask reasonable 
questions and should not completely trust even official documentation.) Moreover, if 
each key is 64 bits, a request to update 10 million keys will be 8.08 GB in size, which is 
much too big. 
If we need to divide the update command into multiple requests, each request incurs 
resource overhead and network latency.
Moreover, there is no mechanism to delete keys (i.e., removing users who have not 
made recent requests), so the system doesn’t know when to remove users to reduce 
the token refill request rate or to make room in the Redis database for other users who 
made recent requests. Our system will need a separate storage mechanism to record the 
last timestamp of a user’s request, and a process to delete old keys.
In a distributed implementation like in section 8.8, every host may contain its own 
token bucket and use this bucket to make rate limiting decisions. Hosts may synchronize their buckets using techniques discussed in section 8.8.2. If a host makes a rate-limiting decision using its bucket before synchronizing this bucket with other hosts, a user 
may be able to make requests at a higher rate than the set rate limit. For example, if two 
hosts each receive requests close in time, each one will subtract a token and have nine 
tokens left, then synchronize with other hosts. Even though there were two requests, all 
hosts will synchronize to nine tokens.
Cloud Bouncer    
Cloud Bouncer, (https://yahooeng.tumblr.com/post/111288877956/cloud-bouncer 
-distributed-rate-limiting-at-yahoo), which was developed at Yahoo in 2014, is an example of a distributed rate-limiting library that is based on a token bucket.
8.9.2	
Leaky bucket 
A leaky bucket has a maximum number of tokens, leaks at a fixed rate, and stops 
leaking when empty. Each time a request arrives, we add a token to the bucket. If the 
bucket is full, the request is rejected, or rate limited. 
Referring to figure 8.13, a common implementation of a leaky bucket is to use a 
FIFO queue with a fixed size. The queue is dequeued periodically. When a request 
arrives, a token is enqueued if the queue has spare capacity. Due to the fixed queue size, 
this implementation is less memory-efficient than a token bucket.


190
Chapter 8  Design a rate-limiting service 
Leaky bucket.
FIFO quele of fixed size.
Token
Token
A request enqueues a token.
Each second, dequeue a token.
Figure 8.13    A leaky bucket that dequeues once per second 
This algorithm has some of the same problems as a token bucket:
¡ Every second, a host needs to dequeue every queue in every key. 
¡ We need a separate mechanism to delete old keys. 
¡ A queue cannot exceed its capacity, so in a distributed implementation, there 
may be multiple hosts that simultaneously fill their buckets/queues fully before 
they synchronize. This means that the user exceeded its rate limit.
Another possible design is to enqueue timestamps instead of tokens. When a request 
arrives, we first dequeue timestamps until the remaining timestamps in the queue are 
older than our retention period, then enqueue the request’s timestamp if the queue 
has space. It returns false if the enqueue was successful and true otherwise. This 
approach avoids the requirement to dequeue from every single queue every second.
QUESTION    Do you notice any possible consistency problems? 
An alert reader will immediately notice two possible consistency problems that will 
introduce inaccuracy into a rate limiting decision: 
1	 A race condition can occur where a host writes a key-value pair to the leader host, 
and it is immediately overwritten by another host.
2	 Hosts’ clocks are not synchronized, and a host may make a rate limiting decision 
using timestamps written by other hosts with slightly different clocks.
This slight inaccuracy is acceptable. These two problems also apply to all the distributed rate-limiting algorithms discussed in this section that use timestamps, namely 
fixed window counter and sliding window log, but we will not mention them again.
8.9.3	
Fixed window counter
Fixed window counters are implemented as key-value pairs. A key can be a combination of a client ID and a timestamp (e.g., user0_1628825241), while the value is the 
request count. When a client makes a request, its key is incremented if it exists or created if it does not exist. The request is accepted if the count is within the set rate limit 
and rejected if the count exceeds the set rate limit. 
The window intervals are fixed. For example, a window can be between the [0, 60) 
seconds of each minute. After a window has passed, all keys expire. For example, the 
key “user0_1628825241” is valid from 3:27:00 AM GMT to 3:27:59 AM GMT because 
1628825241 is 3:27:21 AM GMT, which is within the minute of 3:27 AM GMT. 
QUESTION    How much can the request rate exceed the set rate limit? 


	
191
Rate-limiting algorithms 
A disadvantage of fixed window counter is that it may allow a request rate of up to twice 
the set rate limit. For example, referring to figure 8.13, if the rate limit is five requests 
in one minute, a client can make up to five requests in [8:00:00 AM, 8:01:00 AM) and 
up to another five requests in [8:01:00 AM, 8:01:30 AM). The client has actually made 
10 requests in a one-minute interval, twice the set rate limit of five requests per minute 
(figure 8.14). 
Token
Token
Token
Token
Token
8:00 – 8:01 AM
8:00:30 – 8:01:30 AM
Token
Token
Token
Token
Token
8:01 – 8:02 AM
Figure 8.14     The user made five requests in [8:00:30 AM, 8:01:30 AM) and another five in [8:01:00 
AM, 8:01:30 AM). Even though it was within the limit of five requests per fixed window, it actually made 
10 requests in one minute. 
Adapting this approach for our rate limiter, each time a host receives a user request, it 
takes these steps with its hash map. Refer to figure 8.15 for a sequence diagram of these 
steps:
1	 Determine the appropriate keys to query. For example, if our rate limit had 
a 10-second expiry, the corresponding keys for user0 at 1628825250 will be 
[“user0_1628825241”, “user0_1628825242”, …, “user0_1628825250”]. 
2	 Make requests for these keys. If we are storing key-value pairs in Redis instead of 
the host’s memory, we can use the MGET (https://redis.io/commands/mget/) 
command to return the value of all specified keys. Although the MGET command is O(N) where N is the number of keys to retrieve, making a single request 
instead of multiple requests has lower network latency and resource overhead.
3	 If no keys are found, create a new key-value pair, such as, for example, 
(user0_1628825250, 1). If one key is found, increment its value. If more than one 
key is found (due to race conditions), sum the values of all the returned keys and 
increment this sum by one. This is the number of requests in the last 10 seconds. 
4	 In parallel:
a	 Write the new or updated key-value pair to the leader host (or Redis database). If there were multiple keys, delete all keys except the oldest one.
b	 Return true if the count is more than 10 and false otherwise.


192
Chapter 8  Design a rate-limiting service 
:Host
:User service
par
:Leader host
User request
Steps 1–3
User request
Rate limit decision
Figure 8.15     Sequence diagram of our fixed window counter approach. This diagram illustrates the 
approach of using the host’s memory to store the request timestamps, instead of Redis. The rate-limiting 
decision is made immediately on the host, using only data stored in the host’s memory. The subsequent 
steps on the leader host for synchronization are not illustrated.
QUESTION    How may race conditions cause multiple keys to be found in step 5?
Redis keys can be set to expire (https://redis.io/commands/expire/), so we should 
set the keys to expire after 10 seconds. Otherwise, we will need to implement a separate 
process to continuously find and delete expired keys. If this process is needed, it is an 
advantage of the fixed window counter that the key deletion process is independent of 
the hosts. This independent deletion process can be scaled separately from the host, 
and it can be developed independently, making it easier to test and debug.
8.9.4	
Sliding window log 
A sliding window log is implemented as a key-value pair for each client. The key is the 
client ID, and the value is a sorted list of timestamps. A sliding window log stores a 
timestamp for each request. 
Figure 8.16 is a simple illustration of sliding window log. When a new request comes 
in, we append its timestamp and check if the first timestamp is expired. If so, perform 
a binary search to find the last expired timestamp, then remove all timestamps before 
that. Use a list instead of a queue because a queue does not support binary search. 
Return true if the list has more than 10 timestamps, and false otherwise.


	
193
Logging, monitoring, and alerting
When 62 is appended, do a binary search for 62 – 60 = 2.
1
2
4
5
62
Figure 8.16     Simple sliding window log illustration. A timestamp is appended when a new request is 
made. Next, the last expired timestamp is found using binary search, and then all expired timestamps are 
removed. The request is allowed if the size of the list does not exceed the limit. 
Sliding window log is accurate (except in a distributed implementation, due to the factors discussed in the last paragraph of section 8.9.2) but storing a timestamp value for 
every request consumes more memory than a token bucket.
The sliding window log algorithm counts requests even after the rate limit is 
exceeded, so it also allows us to measure the user’s request rate.
8.9.5	
Sliding window counter 
Sliding window counter is a further development of fixed window counter and sliding 
window log. It uses multiple fixed window intervals, and each interval is 1/60th the 
length of the rate limit’s time window. 
For example, if the rate limit interval is one hour, we use 60 one-minute windows 
instead of one one-hour window. The current rate is determined by summing the last 
60 windows. It may slightly undercount requests. For example, counting requests at 
11:00:35 will sum the 60 one-minute windows from the [10:01:00, 10:01:59] window 
to the [11:00:00, 11:00:59] window, and ignore the [10:00:00, 10:00:59] window. This 
approach is still more accurate than a fixed window counter. 
8.10	 Employing a sidecar pattern 
This brings us to the discussion of applying sidecar pattern to rate limiting policies. 
Figure 1.8 illustrates our rate limiting service architecture using a sidecar pattern. Like 
what was discussed in section 1.4.6, an administrator can configure a user service’s 
rate limiting policies in the control plane, which distributes them to the sidecar hosts. 
With this design where user services contain their rate limiting policies in their sidecar 
hosts, user service hosts do not need to make requests to our rate-limiting service to 
look up their rate-limiting policies, saving the network overhead of these requests. 
8.11	 Logging, monitoring, and alerting
Besides the logging, monitoring, and alerting practices discussed in section 2.5, we 
should configure monitoring and alerting for the following. We can configure monitoring tasks in our shared monitoring service on the logs in our shared logging service, 
and these tasks should trigger alerts to our shared alerting service to alert developers 
about these problems: 


194
Chapter 8  Design a rate-limiting service 
¡ Signs of possible malicious activity, such as users, which continue to make 
requests at a high rate despite being shadow-banned.
¡ Signs of possible DDoS attempts, such as an unusually high number of users 
being rate limited in a short interval.
8.12	 Providing functionality in a client library
Does a user service need to query the rate limiter service for every request? An alternative approach is for the user service to aggregate user requests and then query the rate 
limiter service in certain circumstances such as when it
¡ Accumulates a batch of user requests
¡ Notices a sudden increase in request rate
Generalizing this approach, can rate limiting be implemented as a library instead of 
a service? Section 6.7 is a general discussion of a library vs. service. If we implement it 
entirely as a library, we will need to use the approach in section 8.7, where a host can 
contain all user requests in memory and synchronize the user requests with each other. 
Hosts must be able to communicate with each other to synchronize their user request 
timestamps, so the developers of the service using our library must configure a configuration service like ZooKeeper. This may be overly complex and error-prone for most 
developers, so as an alternative, we can offer a library with features to improve the performance of the rate limiting service, by doing some processing on the client, thereby 
allowing a lower rate of requests to the service. 
This pattern of splitting processing between client and server can generalize to 
any system, but it may cause tight coupling between the client and server, which is, in 
general, an antipattern. The development of the server application must continue to 
support old client versions for a long time. For this reason, a client SDK (software development kit) is usually just a layer on a set of REST or RPC endpoints and does not do 
any data processing. If we wish to do any data processing in the client, at least one of the 
following conditions should be true: 
¡ The processing should be simple, so it is easy to continue to support this client 
library in future versions of the server application.
¡ The processing is resource-intensive, so the maintenance overhead of doing such 
processing on the client is a worthy tradeoff for the significant reduction in the 
monetary cost of running the service.
¡ There should be a stated support lifecycle that clearly informs users when the 
client will no longer be supported.
Regarding batching of requests to the rate limiter, we can experiment with batch size 
to determine the best balance between accuracy and network traffic.
What if the client also measures the request rate and only uses the rate limiting service if the request rate exceeds a set threshold? A problem with this is that since clients 
do not communicate with each other, a client can only measure the request rate on the 


	
195
Summary
specific host it’s installed on and cannot measure the request rate of specific users. This 
means that rate limiting is activated based on the request rate across all users, not on 
specific users. Users may be accustomed to a particular rate limit and may complain if 
they are suddenly rate limited at a particular request rate where they were not rate limited before.
An alternative approach is for the client to use anomaly detection to notice a sudden 
increase in the request rate, then start sending rate-limiting requests to the server.
8.13	 Further reading
¡ Smarshchok, Mikhail, 2019. System Design Interview YouTube channel, https://
youtu.be/FU4WlwfS3G0. 
¡ The discussions of fixed window counter, sliding window log, and sliding window counter were adapted from https://www.figma.com/blog/an-alternative 
-approach-to-rate-limiting/. 
¡ Madden, Neil, 2020. API Security in Action. Manning Publications.
¡ Posta, Christian E. and Maloku, Rinor, 2022. Istio in Action. Manning Publications.
¡ Bruce, Morgan and Pereira, Paulo A., 2018. Microservices in Action, chapter 3.5. 
Manning Publications.
Summary
¡ Rate limiting prevents service outages and unnecessary costs.
¡ Alternatives such as adding more hosts or using the load balancer for rate limiting are infeasible. Adding more hosts to handle traffic spikes may be too slow, 
while using a level 7 load balancer just for rate limiting may add too much cost 
and complexity. 
¡ Do not use rate limiting if it results in poor user experience or for complex use 
cases such as subscriptions.
¡ The non-functional requirements of a rate limiter are scalability, performance, 
and lower complexity. To optimize for these requirements, we can trade off availability, fault-tolerance, accuracy, and consistency.
¡ The main input to our rate-limiter service is user ID and service ID, which will be 
processed according to rules defined by our admin users to return a “yes” or “no” 
response on rate limiting.
¡ There are various rate limiting algorithms, each with its own tradeoffs. Token 
bucket is easy to understand and implement and is memory-efficient, but synchronization and cleanup are tricky. Leaky bucket is easy to understand and 
implement but is slightly inaccurate. A fixed window log is easy to test and debug, 
but it is inaccurate and more complicated to implement. A sliding window log is 
accurate, but it requires more memory. A sliding window counter uses less memory than sliding window log, but it is less accurate than sliding window log. 
¡ We can consider a sidecar pattern for our rate-limiting service.


196
9
Design a notification/ 
alerting service
This chapter covers
¡ Limiting the feature scope and discussion of a 	
	 service
¡ Designing a service that delegates to  
	 platform-specific channels
¡ Designing a system for flexible configurations 	
	 and templates
¡ Handling other typical concerns of a service
We create functions and classes in our source code to avoid duplication of coding, 
debugging, and testing, to improve maintainability, and to allow reuse. Likewise, we 
generalize common functionalities used by multiple services (i.e. centralization of 
cross-cutting concerns). 
Sending user notifications is a common system requirement. In any system design 
discussion, whenever we discuss sending notifications, we should suggest a common 
notification service for the organization.  
9.1	
Functional requirements
Our notification service should be as simple as possible for a wide range of users, 
which causes considerable complexity in the functional requirements. There are 
many possible features that a notification service can provide. Given our limited 
time, we should clearly define some use cases and features for our notification 


	
197
Functional requirements
service that will make it useful to our anticipated wide user base. A well-defined feature 
scope will allow us to discern and optimize for its non-functional requirements. After 
we design our initial system, we can discuss and design for further possible features. 
This question can also be a good exercise in designing an MVP. We can anticipate 
possible features and design our system to be composed of loosely coupled components 
to be adaptable to adding new functionality and services and evolve in response to user 
feedback and changing business requirements. 
9.1.1	
Not for uptime monitoring
Our notification service will likely be a layer on top of various messaging services (e.g., 
email, SMS, etc.). A service to send such a message (e.g., an email service) is a complex 
service in itself. In this question, we will use shared messaging services, but we will not 
design them. We will design a service for users to send messages via various channels.
Generalizing this approach beyond shared messaging services, we will also use other 
shared services for functionalities like storage, event streaming, and logging. We will 
also use the same shared infrastructure (bare metal or cloud infrastructure) that our 
organization uses to develop other services.
QUESTION    Can uptime monitoring be implemented using the same shared 
infrastructure or services as the other services that it monitors? 
Based on this approach, we assume that this service should not be used for uptime 
monitoring (i.e., trigger alerts on outages of other services). Otherwise, it cannot be 
built on the same infrastructure or use the same shared services as other services in our 
organization because outages that affect them will also affect this service, and outage 
alerts will not be triggered. An uptime monitoring service must run on infrastructure 
that is independent of the services that it monitors. This is one key reason external 
uptime monitoring services like PagerDuty are so popular.
All this being said, section 9.14 discusses a possible approach to using this service for 
uptime monitoring. 
9.1.2	
Users and data
Our notification service has three types of users:
¡ Sender: A person or service who CRUDs (create, read, update, and delete) notifications and sends them to recipients.
¡ Recipient: A user of an app who receives notifications. We also refer to the devices 
or apps themselves as recipients. 
¡ Admin: A person who has admin access to our notification service. An admin has 
various capabilities. They can grant permissions to other users to send or receive 
notifications, and they can also create and manage notification templates (section 9.5). We assume that we as developers of the notification service have admin 
access, although, in practice, only some developers may have admin access to the 
production environment. 


198
Chapter 9  Design a notification/alerting service 
We have both manual and programmatic senders. Programmatic users can send API 
requests, especially to send notifications. Manual users may go through a web UI for all 
their use cases, including sending notifications, as well as administrative features like 
configuring notifications and viewing sent and pending notifications. 
We can limit a notification’s size to 1 MB, more than enough for thousands of characters and a thumbnail image. Users should not send video or audio within a notification. Rather, they should include links in the notification to media content or any 
other big files, and the recipient systems should have features developed separately 
from our notification service to download and view that content. Hackers may attempt 
to impersonate the service and send notifications with links to malicious websites. To 
prevent this, a notification should contain a digital signature. The recipients can verify 
the signature with the certificate authority. For more information, refer to resources on 
cryptography.  
9.1.3	
Recipient channels
We should support the ability to send notifications via various channels, including the 
following. Our notification service needs to be integrated to services that send messages for each of these channels:
¡ Browser
¡ Email 
¡ SMS. For simplicity, we do not consider MMS. 
¡ Automated phone calls 
¡ Push notifications on Android, iOS, or browsers. 
¡ Customized notifications within apps, such as, for example, banking or finance 
apps with stringent privacy and security requirements use internal messaging 
and notification systems. 
9.1.4	
Templates
A particular messaging system provides a default template with a set of fields that a user 
populates before sending out the message. For example, an email has a sender email 
address field, a recipient email addresses field, a subject field, a body field, and a list 
of attachments; an SMS has a sender phone number field, a recipient phone numbers 
field, and a body field.
The same notification may be sent to many recipients. For example, an app may send 
an email or push notification containing a welcome message to any new user who has 
just signed up. The message can be identical for all users, such as, for example, “Welcome to Beigel. Please enjoy a 20% discount on your first purchase.”
The message may also have personalized parameters, such as the user’s name and 
the discount percentage; for example, “Welcome ${first_name}. Please enjoy a ${discount}% discount on your first purchase.” Another example is an order confirmation 
email, text, or push notification that an online marketplace app may wish to send a 


	
199
Functional requirements
customer just after they submit an order. The message may have parameters for the 
customer’s name, order confirmation code, list of items (an item can have many parameters), and prices. There may be many parameters in a message.
Our notification service may provide an API to CRUD templates. Each time a user 
wishes to send a notification, it can either create the entire message itself or select a particular template and fill in the values of that template.
A template feature also reduces traffic to our notification service. This is discussed 
later in this chapter.
We can provide many features to create and manage templates, and this can be a service in itself (a template service). We will limit our initial discussion to CRUD templates.
9.1.5	
Trigger conditions
Notifications can be triggered manually or programmatically. We may provide a 
browser app for users to create a notification, add recipients, and then send it out 
immediately. Notifications may also be sent out programmatically, and this can be configured either on the browser app or via an API. Programmatic notifications are configured to be triggered on a schedule or by API requests. 
9.1.6	
Manage subscribers, sender groups, and recipient groups
If a user wishes to send a notification to more than one recipient, we may need to 
provide features to manage recipient groups. A user may address a notification using a 
recipient group, instead of having to provide a list of recipients every time the former 
needs to send a notification. 
WARNING    Recipient groups contain PII (Personally-Identifiable Information), 
so they are subject to privacy laws such as GDPR and CCPA. 
Users should be able to CRUD recipient groups. We may also consider role-based access 
control (RBAC). For example, a group may have read and write roles. A user requires 
the group’s read role to view its members and other details and then the write role to 
add or remove members. RBAC for groups is outside the scope of our discussion.
A recipient should be able to opt into notifications and opt out of unwanted notifications; otherwise, they are just spam. We will skip this discussion in this chapter. It may be 
discussed as a follow-up topic. 
9.1.7	
User features
Here are other features we can provide:
¡ The service should identify duplicate notification requests from senders and not 
send duplicate notifications to recipients. 
¡ We should allow a user to view their past notification requests. An important 
use case is for a user to check if they have already made a particular notification request, so they will not make duplicate notification requests. Although 


200
Chapter 9  Design a notification/alerting service 
the notification service can also automatically identify and duplicate notification requests, we will not completely trust this implementation, since a user may 
define a duplicate request differently from the notification service. 
¡ A user will store many notification configurations and templates. It should be 
able to find configurations or templates by various fields, like names or descriptions. A user may also be able to save favorite notifications. 
¡ A user should be able to look up the status of notifications. A notification may be 
scheduled, in progress (similar to emails in an outbox), or failed. If a notification’s delivery is failed, a user should be able to see if a retry is scheduled and the 
number of times delivery has been retried. 
¡ (Optional) A priority level set by the user. We may process higher-priority notifications before lower-priority ones or use a weighted approach to prevent 
starvation. 
9.1.8	
Analytics
We can assume analytics is outside the scope of this question, though we can discuss it 
as we design our notification service. 
9.2	
Non-functional requirements
We can discuss the following non-functional requirements: 
¡ Scale: Our notification service should be able to send billions of notifications 
daily. At 1 MB/notification, our notification service will process and send petabytes of data daily. There may be thousands of senders and one billion recipients.
¡ Performance: A notification should be delivered within seconds. To improve the 
speed of delivering critical notifications, we may consider allowing users to prioritize certain notifications over others.
¡ High availability: Five 9s uptime.
¡ Fault-tolerant: If a recipient is unavailable to receive a notification, it should 
receive the notification at the next opportunity.
¡ Security: Only authorized users should be allowed to send notifications. 
¡ Privacy: Recipients should be able to opt out of notifications. 
9.3	
Initial high-level architecture 
We can design our system with the following considerations: 
¡ Users who request creation of notifications do so through a single service with 
a single interface. Users specify the desired channel(s) and other parameters 
through this single service/interface. 


	
201
Initial high-level architecture 
¡ However, each channel can be handled by a separate service. Each channel service 
provides logic specific to its channel. For example, a browser notification channel service can create browser notifications using the web notification API. Refer 
to documentation like “Using the Notifications API” (https://developer.mozilla 
.org/en-US/docs/Web/API/Notifications_API/Using_the_Notifications 
_API) and “Notification” (https://developer.mozilla.org/en-US/docs/Web/
API/notification). Certain browsers like Chrome also provide their own notifications API. Refer to “chrome.notifications” (https://developer.chrome.com/ 
docs/extensions/reference/notifications/) and “Rich Notifications API” 
(https://developer.chrome.com/docs/extensions/mv3/richNotifications/) 
for rich notifications with rich elements like images and progress bars. 
¡ We can centralize common channel service logic in another service, which we 
can call the “job constructor.” 
¡ Notifications via various channels may be handled by external third-party services, illustrated in figure 9.1. Android push notifications are made via Firebase 
Cloud Messaging (FCM). iOS push notifications are made via Apple Push notification service. We may also employ third-party services for email, SMS/texting, 
and phone calls. Making requests to third-party services means that we must limit 
the request rate and handle failed requests.
Client
External notification
services
Notification Service
Figure 9.1    Our Notification Service may make requests to external notification services, so the former 
must limit the request rate and handle failed requests.
¡ Sending notifications entirely via synchronous mechanisms is not scalable 
because the process consumes a thread while it waits for the request and response 
to be sent over the network. To support thousands of senders and billions of 
recipients, we should use asynchronous techniques like event streaming. 
Based on these considerations, figures 9.2 and 9.3 show our initial high-level architecture. To send a notification, a client makes a request to our notification service. 
The request is first processed by the frontend service or API gateway and then sent to 
the backend service. The backend service has a producer cluster, a notification Kafka 
topic, and a consumer cluster. A producer host simply produces a message on to the 
notification Kafka topic and returns 200 success. The consumer cluster consumes the 
messages, generates notification events, and produces them to the relevant channel 
queues. Each notification event is for a single recipient/destination. This asynchronous event driven approach allows the notification service to handle unpredictable 
traffic spikes. 


202
Chapter 9  Design a notification/alerting service 
Client
Frontend
Backend
Browser notification 
event queue
Android notification
event queue
iOS notification 
event queue
Email notification 
event queue
SMS notification 
event queue
Phone call notification 
event queue
Custom app notification 
event queue
Possible 
3rd
party Phone
call service
Possible 
3rd
party SMS
service
Possible 
3rd
party Email
service
Apple Push
Notification
Service
Firebase 
Cloud
Messaging 
(FCM)
Notification Service
Job 
Constructor
Browser 
notification 
service
Android 
notification 
service
iOS 
notification 
service
Email 
notification 
service
SMS 
notification 
service
Custom app 
notification 
service
Phone 
notification 
service
(Shared)
Logs
External 
notification 
services
Figure 9.2    High-level architecture of our notification service, illustrating all the possible requests when 
a client/user sends a notification. We collectively refer to the various Kafka consumers (each of which 
is a notification service for a specific channel) as channel services. We illustrate that the backend and 
channel services use a shared logging database, but all the components of our notification service 
should log to a shared logging service. 


	
203
Initial high-level architecture 
On the other side of the queues, we have a separate service for each notification channel. Some of them may depend on external services, such as Android’s Firebase Cloud 
Messaging (FCM) and iOS’s Apple Push Notification Service (APNs). The browser 
notification service may be further broken up into various browser types (e.g., Firefox 
and Chrome).
Notification 
queue
Producer
Consumer
Backend
Frontend
Various channel 
notification event 
queues & shared logs
Figure 9.3    Zoom-in of our backend service from figure 9.2. The backend service consists of a producer 
cluster, a notification Kafka topic, and a consumer cluster. In subsequent illustrations, we will omit the 
zoom-in diagram of the backend service.
Each notification channel must be implemented as a separate service (we can refer to 
it as a channel service) because sending notifications on a particular channel requires 
a particular server application, and each channel has different capabilities, configurations, and protocols. Email notifications use SMTP. To send an email notification via 
the email notification system, the user provides the sender email address, recipient 
email addresses, title, body, and attachments. There are also other email types like calendar events. A SMS gateway uses various protocols including HTTP, SMTP, and SMPP. 
To send an SMS message, the user provides an origin number, a destination number, 
and a string. 
In this discussion, let’s use the term “destination” or “address” to refer to a field that 
that identifies where to send a single notification object, such as a phone number, an 
email address, a device ID for push notifications, or custom destinations such as user 
IDs for internal messaging, and so on. 
Each channel service should concentrate on its core functionality of sending a notification to a destination. It should process the full notification content and deliver the 
notification to its destination. But we may need to use third-party APIs to deliver messages by certain channels. For example, unless our organization is a telecommunications company, we will use a telecommunications company’s API to deliver phone calls 
and SMS. For mobile push notifications, we will use Apple Push Notification Service for 
iOS notifications and Firebase Cloud Messaging for Android notifications. It is only for 
browser notifications and our custom app notifications that we can deliver messages 
without using third-party APIs. Wherever we need to use a third-party API, the corresponding channel service should be the only component in our notification service 
that directly makes requests to that API.


204
Chapter 9  Design a notification/alerting service 
Having no coupling between a channel service and the other services in our notification service makes our system more fault-tolerant and allows the following: 
¡ The channel service can be used by services other than our notification service. 
¡ The channel service can be scaled independently from the other services.
¡ The services can change their internal implementation details independently of 
each other and be maintained by separate teams with specialized knowledge. For 
example, the automated phone call service team should know how to send automated phone calls, and the email service team should know how to send email, 
but each team need not know about how the other team’s service works. 
¡ Customized channel services can be developed, and our notification service can 
send requests to them. For example, we may wish to implement notifications 
within our browser or mobile app that are displayed as custom UI components 
and not as push notifications. The modular design of channel services makes 
them easier to develop. 
We can use authentication (e.g., refer to the discussion of OpenID Connect in the 
appendix) on the frontend service to ensure that only authorized users, such as service 
layer hosts, can request channel services to send notifications. The frontend service 
handles requests to the OAuth2 authorization server. 
Why shouldn’t users simply use the notification systems of the channels they require? 
What are the benefits of the development and maintenance overhead of the additional 
layers? 
The notification service can provide a common UI (not shown in figure 13.1) for its 
clients (i.e., the channel services), so users can manage all their notifications across all 
channels from a single service and do not need to learn and manage multiple services. 
The frontend service provides a common set of operations: 
¡ Rate limiting—Prevents 5xx errors from notification clients being overwhelmed 
by too many requests. Rate limiting can be a separate common service, discussed 
in chapter 8. We can use stress testing to determine the appropriate limit. The 
rate limiter can also inform maintainers if the request rate of a particular channel consistently exceeds or is far below the set limit, so we can make an appropriate scaling decision. Auto-scaling is another option we can consider. 
¡ Privacy—Organizations may have specific privacy policies that regulate notifications sent to devices or accounts. The service layer can be used to configure and 
enforce these policies across all clients. 
¡ Security—Authentication and authorization for all notifications. 


	
205
Object store: Configuring and sending notifications 
¡ Monitoring, analytics, and alerting—The service can log notification events and 
compute aggregate statistics such as notification success and failure rates over 
sliding windows of various widths. Users can monitor these statistics and set alert 
thresholds on failure rates. 
¡ Caching—Requests can be made through a caching service, using one of the 
caching strategies discussed in chapter 8. 
We provision a Kafka topic for each channel. If a notification has multiple channels, we 
can produce an event for each channel and produce each event to the corresponding 
topic. We can also have a Kafka topic for each priority level, so if we have five channels 
and three priority levels, we will have 15 topics. 
The approach of using Kafka rather than synchronous request-response follows the 
cloud native principle of event-driven over synchronous. Benefits include less coupling, 
independent development of various components in a service, easier troubleshooting 
(we can replay messages from the past at any point in time), and higher throughput 
with no blocking calls. This comes with storage costs. If we process one billion messages 
daily, the storage requirement is 1 PB daily, or ~10 PB, with a one-week retention period. 
For a consistent load on the job constructor, each channel service consumer host has 
its own thread pool. Each thread can consume and process one event at a time. 
The backend and each channel service can log their requests for purposes such as 
troubleshooting and auditing. 
9.4	
Object store: Configuring and sending notifications 
The notification service feeds a stream of events into the channel services. Each event 
corresponds to a single notification task to a single addressee. 
QUESTION    What if a notification contains large files or objects? It is inefficient 
for multiple Kafka events to contain the same large file/object. 
In figure 9.3, the backend may produce an entire 1 MB notification to a Kafka topic. 
However, a notification may contain large files or objects. For example, a phone call 
notification may contain a large audio file, or an email notification may contain multiple video attachments. Our backend can first POST these large objects in an object 
store, which will return object IDs. Our backend can then generate a notification event 
that includes these object IDs instead of the original objects and produce this event to 
the appropriate Kafka topic. A channel service will consume this event, GET the objects 
from our object store, assemble the notification, and then deliver it to the recipient. In 
figure 9.4, we add our metadata service to our high-level architecture.


206
Chapter 9  Design a notification/alerting service 
Client
Frontend
Backend
Notification Service
Object 
Store
Browser notification 
event queue
Android notification
event queue
iOS notification 
event queue
Email notification 
event queue
SMS notification 
event queue
Phone call notification 
event queue
Custom app notification 
event queue
Possible 
3rd
party Phone
call service
Possible 
3rd
party SMS
service
Possible 
3rd
party Email
service
Apple Push
Notification
Service
Firebase 
Cloud
Messaging 
(FCM)
Job 
Constructor
Browser 
notification 
service
Android 
notification 
service
iOS 
notification 
service
Email 
notification 
service
SMS 
notification 
service
Custom app 
notification 
service
Phone 
notification 
service
(Shared)
Logs
External 
notification 
services
Figure 9.4    Our high-level architecture with a metadata service. Our backend service can POST large 
objects to the metadata service, so the notification events can be kept small. 
If a particular large object is being delivered to multiple recipients, our backend will 
POST it multiple times to our object store. From the second POST onwards, our object 
store can return a 304 Not Modified response. 


	
207
Notification templates 
9.5	
Notification templates 
An addressee group with millions of destinations may cause millions of events to be 
produced. This may occupy much memory in Kafka. The previous section discussed 
how we can use a metadata service to reduce the duplicate content in events and thus 
reduce their sizes. 
9.5.1	
Notification template service
Many notification events are almost duplicates with a small amount of personalization. 
For example, figure 9.5 shows a push notification that can be sent to millions of users 
that contains an image common to all recipients and a string that varies only by the 
recipient’s name. In another example, if we are sending an email, most of the email’s 
contents will be identical to all recipients. The email title and body may only be slightly 
different for each recipient (such as a different name or a different percentage of discount for each user), while any attachments will likely be identical for all recipients. 
Figure 9.5    Example of a push notification that contains an image common to all recipients and can have 
a string that only varies by the recipient’s name. The common content can be placed in a template such 
as “Hi ${name}! Welcome to Deliver & Dine.” A Kafka queue event can contain a key-value pair of the 
form (“name” and the recipient’s name, destination ID). Image from https://buildfire.com/what-is-a 
-push-notification/. 
In section 9.1.4, we discussed that templates are useful to users for managing such personalization. Templates are also useful to improve our notification service’s scalability. 
We can minimize the sizes of the notification events by placing all the common data 
into a template. Creation and management of templates can itself be a complex system. We can call it the notification template service, or template service for short. Figure 9.6 illustrates our high-level architecture with our template service. A client only 
needs to include a template ID in a notification, and a channel service will GET the 
template from the template service when generating the notification.


208
Chapter 9  Design a notification/alerting service 
Client
Frontend
Backend
Notification Service
Template 
Service
Object 
Store
Browser notification 
event queue
Android notification
event queue
iOS notification 
event queue
Email notification 
event queue
SMS notification 
event queue
Phone call notification 
event queue
Custom app notification 
event queue
Possible 
3rd
party Phone
call service
Possible 
3rd
party SMS
service
Possible 
3rd
party Email
service
Apple Push
Notification
Service
Firebase 
Cloud
Messaging 
(FCM)
Job 
Constructor
Browser 
notification 
service
Android 
notification 
service
iOS 
notification 
service
Email 
notification 
service
SMS 
notification 
service
Custom app 
notification 
service
Phone 
notification 
service
(Shared)
Logs
External 
notification 
services
Figure 9.6    High-level architecture including our template service. Notification service users can CRUD 
templates. The template service should have its own authentication and authorization and RBAC (rolebased access control). The job constructor should only have read access. Admins should have admin 
access so they can create, update, and delete templates or grant roles to other users.


	
209
Notification templates 
Combining this approach with our metadata service, an event need only contain the 
notification ID (which can also be used as the notification template key), any personalized data in the form of key-value pairs, and the destination. If the notification has no 
personalized content (i.e., it is identical for all its destinations), the metadata service 
contains essentially the entire notification content, and an event will only contain a 
destination and a notification content ID. 
A user can set up a notification template prior to sending notifications. A user can 
send CRUD requests on notification templates to the service layer, which forwards them 
to the metadata service to perform the appropriate queries on the metadata database. 
Depending on our available resources or ease-of-use considerations, we may also choose 
to allow users not to have to set up a notification template and simply send entire notification events to our service. 
9.5.2	
Additional features
We may decide that a template requires additional features such as the following. 
These additional features may be briefly discussed near the end of the interview as 
follow-up topics. It is unlikely there will be enough time during the interview for an 
in-depth discussion. A sign of engineering maturity and a good interview signal is the 
ability to foresee these features, while also demonstrating that one can fluently zoom 
in and out of the details of any of these systems, and clearly and concisely describe 
them to the interviewer. 
Authoring, access control, and change management
A user should be able to author templates. The system should store the template’s 
data, including its content and its creation details, such as author ID and created and 
updated timestamps. 
User roles include admin, write, read, and none. These correspond to the access permissions that a user has to a template. Our notification template service may need to be 
integrated with our organization’s user management service, which may use a protocol 
like LDAP. 
We may wish to record templates’ change history, including data such as the exact 
change that was made, the user who made it, and the timestamp. Going further, we 
may wish to develop a change approval process. Changes made by certain roles may 
need approval from one or more admins. This may be generalized to a shared approval 
service that can be used by any application where one or more users propose a write 
operation, and one or more other users approve or deny the operation. 
Extending change management further, a user may need to rollback their previous 
change or revert to a specific version. 


210
Chapter 9  Design a notification/alerting service 
Reusable and extendable template classes and functions
A template may consist of reusable sub-templates, each of which is separately owned 
and managed. We can refer to them as template classes.
A template’s parameters can be variables or functions. Functions are useful for 
dynamic behavior on the recipient’s device. 
A variable can have a data type (e.g., integer, varchar(255), etc.). When a client creates a notification from a template, our backend can validate the parameter values. Our 
notification service can also provide additional constraints/validation rules, such as a 
minimum or maximum integer value or string length. We can also define validation 
rules on functions. 
A template’s parameters may be populated by simple rules (e.g., a recipient name 
field or a currency symbol field) or by machine-learning models (e.g., each recipient 
may be offered a different discount). This will require integration with systems that 
supply data necessary to fill in the dynamic parameters. Content management and 
personalization are different functions owned by different teams, and the services and 
their interfaces should be designed to clearly reflect this ownership and division of 
responsibilities. 
Search
Our template service may store many templates and template classes, and some of 
them may be duplicates or very similar. We may wish to provide a search feature. Section 2.6 discusses how to implement search in a service. 
Other
There are endless possibilities. For example, how can we manage CSS and JavaScript 
in templates? 
9.6	
Scheduled notifications
Our notification service can use a shared Airflow service or job scheduler service to 
provide scheduled notifications. Referring to figure 9.7, our backend service should 
provide an API endpoint to schedule notifications and can generate and make the 
appropriate request to the Airflow service to create a scheduled notification.
When the user sets up or modifies a periodic notification, the Airflow job’s Python 
script is automatically generated and merged into the scheduler’s code repository. 
A detailed discussion of an Airflow service is outside the scope of this question. For 
the purpose of the interview, the interviewer may request that we design our own task 
scheduling system instead of using an available solution such as Airflow or Luigi. We 
can use the cron-based solution discussed in section 4.6.1.  


	
211
Scheduled notifications
Client
Frontend
Backend
Notification Service
Job 
Scheduler
Template 
Service
Object 
Store
Browser notification 
event queue
Android notification
event queue
iOS notification 
event queue
Email notification 
event queue
SMS notification 
event queue
Phone call notification 
event queue
Custom app notification 
event queue
Possible 
3rd
party Phone
call service
Possible 
3rd
party SMS
service
Possible 
3rd
party Email
service
Apple Push
Notification
Service
Firebase 
Cloud
Messaging 
(FCM)
Job 
Constructor
Browser 
notification 
service
Android 
notification 
service
iOS 
notification 
service
Email 
notification 
service
SMS 
notification 
service
Custom app 
notification 
service
Phone 
notification 
service
(Shared)
Logs
External 
notification 
services
Figure 9.7    High-level architecture with an Airflow/job scheduler service. The job scheduler service 
is for users to configure periodic notifications. At the scheduled times, the job scheduler service will 
produce notification events to the backend. 


212
Chapter 9  Design a notification/alerting service 
Periodic notifications may compete with ad hoc notifications because both can be 
limited by the rate limiter. Each time the rate limiter prevents a notification request 
from immediately proceeding, this should be logged. We should have a dashboard to 
display the rate of rate limiting events. We also need to add an alert that triggers when 
there are frequent rate limiting events. Based on this information, we can scale up our 
cluster sizes, allocate more budget to external notification services, or request or limit 
certain users from excessive notifications. 
9.7	
Notification addressee groups 
A notification may have millions of destinations/addresses. If our users must specify 
each of these destinations, each user will need to maintain its own list, and there may 
be much duplicated recipient data among our users. Moreover, passing these millions 
of destinations to the notification service means heavy network traffic. It is more convenient for users to maintain the list of destinations in our notification service and 
use that list’s ID in making requests to send notifications. Let’s refer to such a list as a 
“notification addressee group.” When a user makes a request to deliver a notification, 
the request may contain either a list of destinations (up to a limit) or a list of Addressee 
Group IDs. 
We can design an address group service to handle notification addressee groups. 
Other functional requirements of this service may include: 
¡ Access control for various roles like read-only, append-only (can add but cannot delete addresses), and admin (full access). Access control is an important 
security feature here because an unauthorized user can send notifications to our 
entire user base of over 1 billion recipients, which can be spam or more malicious 
activity.
¡ May also allow addressees to remove themselves from notification groups to prevent spam. These removal events may be logged for analytics. 
¡ The functionalities can be exposed as API endpoints, and all these endpoints are 
accessed via the service layer. 
We may also need a manual review and approval process for notification requests to 
a large number of recipients. Notifications in testing environments do not require 
approval, while notifications in the production environment require manual approval. 
For example, a notification request to one million recipients may require manual approval by an operations staff, 10 million recipients may require a manager’s 
approval, 100 million recipients may require a senior manager’s approval, and a notification to the entire user base may require director-level approval. We can design a system for senders to obtain approval in advance of sending notifications. This is outside 
the scope of this question.
Figure 9.8 illustrates our high-level architecture with an address group service. A 
user can specify an address group in a notification request. The backend can make GET 
requests to the address group service to obtain an address group’s user IDs. Because 
there can be over one billion user IDs in a group, a single GET response cannot contain 


	
213
Notification addressee groups 
all user IDs, but rather has a maximum number of user IDs. The Address Group Service must provide a GET /address-group/count/{name} endpoint that returns the 
count of addresses in this group, and a GET /address-group/{name}/start-index/
{start-index}/end-index/{end-index} endpoint so our backend can make GET 
requests to obtain batches of addresses. 
 
Figure 9.8    Zoom-in of figure 9.6, with the addition of an address group service. An address group 
contains a list of recipients. The address group service allows a user to send a notification to multiple 
users by specifying a single address group, instead of having to specify each and every recipient. 
We can use a choreography saga (section 5.6.1) to GET these addresses and generate 
notification events. This can handle traffic surges to our address group service. Figure 
9.9 illustrates our backend architecture to perform this task. 
Address Group
Request Topic
3. Request
addresses
2. Consume
4. Produce response
Address 
Group
Fetcher
1. Produce request
5. Consume response
Backend
Address Group Request Topic
Address 
Group
Service
Figure 9.9    Our backend architecture to construct notification events from an address group 
Referring to the sequence diagram in figure 9.10, a producer can create an event for 
such a job. A consumer consumes this event and does the following:
1	 Uses GET to obtain a batch of addresses from the address group service
2	 Generates a notification event from each address
3	 Produces it to the appropriate notification event Kafka topic


214
Chapter 9  Design a notification/alerting service 
par
par
Backend
Address
Group
Service
Notification
Kafka topic
Address Group
Fetcher
Addresses
batch request
2. Consume
addresses
request
Address Group
Response Topic
Address Group
Request Topic
3. GET address batch
Success response
4. Produce addresses batch
Success response
5. Consume addresses batch
Addresses batch
Produce a notification
Addresses batch
Addresses count
GET addresses count
1. Produce addresses request
Generate notifications
Figure 9.10    Sequence diagram for our backend service to construct notification events from an address 
group
Should we split the backend service into two services, so that step 5 onward is done 
by another service? We did not do this because the backend may not need to make 
requests to the address group service.
TIP    This backend produces to one topic and consumes from another. If you 
need a program that consumes from one topic and produces to another, consider using Kafka Streams (https://kafka.apache.org/10/documentation/
streams/). 


	
215
Unsubscribe requests
QUESTION   What if new users are added to a new address group while the address 
group fetcher is fetching its addresses? 
A problem with this that we will immediately discover is that a big address group 
changes rapidly. New recipients are constantly being added or removed from the 
group, due to various reasons:
¡ Someone may change their phone number or email address.
¡ Our app may gain new users and lose current users during any period.
¡ In a random population of one billion people, thousands of people are born and 
die every day.
When is a notification considered delivered to all recipients? If our backend attempts 
to keep fetching batches of new recipients to create notification events, given a sufficiently big group, this event creation will never end. We should deliver a notification 
only to recipients who were within an address group at the time the notification was 
triggered. 
A discussion of possible architecture and implementation details of an address group 
service is outside the scope of this question. 
9.8	
Unsubscribe requests
Every notification should contain a button, link, or other UI for recipients to unsubscribe from similar notifications. If a recipient requests to be removed from future 
notifications, the sender should be notified of this request. 
We may also add a notification management page in our app for our app users, 
like figure 9.11. App users can choose the categories of notifications that they wish to 
receive. Our notification service should provide a list of notification categories, and a 
notification request should have a category field that is a required field. 
Figure 9.11    Notification 
management in the 
YouTube Android app. 
We can define a list of 
notification categories, so 
our app users can choose 
which categories to 
subscribe to. 


216
Chapter 9  Design a notification/alerting service 
QUESTION    Should unsubscribe be implemented on the client or server? 
The answer is either to implement it on the server or on both sides. Do not implement 
it only on the client. If unsubscribe is implemented only on the client, the notification 
service will continue to send notifications to recipients, and the app on the recipient’s 
device will block the notification. We can implement this approach for our browser 
and mobile apps, but we cannot implement this on email, phone calls, or SMS. Moreover, it is a waste of resources to generate and send a notification only for it to be 
blocked by the client. However, we may still wish to implement notification blocking 
on the client in case the server-side implementation has bugs and continues to send 
notifications that should have been blocked. 
If unsubscribe is implemented on the server, the notification service will block notifications to the recipient. Our backend should provide an API endpoint to subscribe or 
unsubscribe from notifications, and the button/link should send a request to this API.
One way to implement notification blocking is to modify the Address Group Service API to accept category. The new GET API endpoints can be something like GET /
address-group/count/{name}/category/{category} and GET /address-group/
{name}/category/{category}/start-index/{start-index}/end-index/
{end-index}. The address group service will return only recipients who accept notifications of that category. Architecture and further implementation details are outside 
the scope of this question. 
9.9	
Handling failed deliveries
Notification delivery may fail due to reasons unrelated to our notification service: 
¡ The recipient’s device was uncontactable. Possible causes may include:
–	 Network problems.
–	 The recipient’s device may be turned off.
–	 Third-party delivery services may be unavailable.
–	 The app user uninstalled the mobile app or canceled their account. If the app 
user had canceled their account or uninstalled the mobile app, there should 
be mechanisms to update our address group service, but the update hasn’t yet 
been applied. Our channel service can simply drop the request and do nothing else. We can assume that the address group service will be updated in the 
future, and then GET responses from the address group service will no longer 
include this recipient. 
¡ The recipient has blocked this notification category, and the recipient’s device 
blocked this notification. This notification should not have been delivered, but it 
was delivered anyway, likely because of bugs. We should configure a low-urgency 
alert for this case.


	
217
Handling failed deliveries
Each of the subcases in the first case should be handled differently. Network problems 
that affect our data center are highly unlikely, and if it does happen, the relevant team 
should have already broadcasted an alert to all relevant teams (obviously via channels 
that don’t depend on the affected data center). It is unlikely that we will discuss this 
further in an interview. 
If there were network problems that only affected the specific recipient or the recipient’s device was turned off, the third-party delivery service will return a response to 
our channel service with this information. The channel service can add a retry count 
to the notification event, or it can increment the count if the retry field is already present (i.e., this delivery was already a retry). Next, it produces this notification to a Kafka 
topic that functions as a dead letter queue. A channel service can consume from the 
dead letter queue and then retry the delivery request. In figure 9.12, we add dead letter 
queues to our high-level architecture. If the retry fails three times, the channel service 
can log this and make a request to the address group service to record that the user is 
uncontactable. The address group service should provide an appropriate API endpoint 
for this. The address group service should also stop including this user in future GET 
requests. The implementation details are outside the scope of this question. 
 
 
 
Figure 9.12    Zoom-in of figure 9.6, with the addition of a browser notification dead letter queue. The 
dead letter queues for the other channel services will be similar. If the browser notification service 
encounters a 503 Service Unavailable error when delivering a notification, it produces/enqueues this 
notification event to its dead letter queue. It will retry the delivery later. If delivery fails after three 
attempts, the browser notification service will log the event (to our shared logging service). We may also 
choose to also configure a low-urgency alert for such failed deliveries. 
If a third-party delivery service is unavailable, the channel service should trigger a 
high-urgency alert, employ exponential backoff, and retry with the same event. The 
channel service can increase the interval between retries.


218
Chapter 9  Design a notification/alerting service 
Our notification service should also provide an API endpoint for the recipient app to 
request missed notifications. When the recipient email, browser, or mobile app is ready 
to receive notifications, it can make a request to this API endpoint. 
9.10	 Client-side considerations regarding duplicate notifications 
Channel services that send notifications directly to recipient devices must allow both 
push and pull requests. When a notification is created, a channel service should immediately push it to the recipient. However, the recipient client device may be offline or 
unavailable for some reason. When the device comes back online, it should pull notifications from the notifications service. This is applicable to channels that don’t use 
external notifications services, such as browser or custom app notifications. 
How can we avoid duplicate notifications? Earlier we discussed solutions to avoid 
duplicate notifications for external notification services (i.e., push requests). Avoiding duplicate notifications for pull requests should be implemented on the client side. 
Our service should not deny requests for the same notifications (perhaps other than 
rate limiting) because the client may have good reasons to repeat requests. The client should record notifications already shown (and dismissed) by the user, perhaps in 
browser localStorage or a mobile device’s SQLite database. When a client receives notifications in a pull (or perhaps also a push) request, it should look up against the device’s 
storage to determine whether any notification has already been displayed before displaying new notifications to the user. 
9.11	 Priority 
Notifications may have different priority levels. Referring to figure 9.13, we can decide 
how many priority levels we need, such as 2 to 5, and create a separate Kafka topic for 
each priority level. 
 
 
 
 
 
Figure 9.13    
Figure 9.12 with 
two priority levels 


	
219
Monitoring and alerting 
To process higher-priority notifications before lower-priority ones, a consumer host 
can simply consume from the higher-priority Kafka topics until they are empty, then 
consume from the lower-priority Kafka topics. For a weighted approach, each time a 
consumer host is ready to consume an event, it can first use weighted random selection 
to select a Kafka topic to consume from. 
QUESTION    Extend the system design to accommodate a different priority configuration for each channel.
9.12	 Search 
We may provide search for users to search and view existing notification/alerting setups. We can index on notification templates and notification address groups. Referring to section 2.6.1, a frontend search library like match-sorter should be sufficient 
for this use case. 
9.13	 Monitoring and alerting 
Besides what was discussed in section 2.5, we should monitor and send alerts for the 
following. 
Users should be able to track the state of their notifications. This can be provided via 
another service that reads from the log service. We can provide a notification service UI 
for users to create and manage notifications, including templates and tracking notifications’ statuses. 
We can create monitoring dashboards on various statistics. Besides the success and 
failure rates already mentioned earlier, other useful statistics are the number of events 
in the queue and event size percentiles over time, broken down by channel and priority, 
as well as OS statistics like CPU, memory, and disk storage consumption. High memory consumption and a large number of events in the queue indicate that unnecessary 
resource consumption, and we may examine the events to determine whether any data 
can be placed into a metadata service to reduce the events’ sizes in the queue. 
We can do periodic auditing to detect silent errors. For example, we can arrange 
with the external notification services we use to compare these two numbers: 
¡ The number of 200 responses received by our notification services that send 
requests to external notification services. 
¡ The number of valid notifications received by those external notification services. 
Anomaly detection can be used to determine an unusual change in the notification 
rate or message sizes, by various parameters such as sender, receiver, and channel. 


220
Chapter 9  Design a notification/alerting service 
9.14	 Availability monitoring and alerting on the notification/alerting 
service 
We discussed in section 9.1.1 that our notification service should not be used for 
uptime monitoring because it shares the same infrastructure and services as the services that it monitors. But what if we insist on finding a way for this notification service 
to be a general shared service for outage alerts? What if it itself fails? How will our alerting service alert users? One solution involves using external devices, such as servers 
located in various data centers. 
We can provide a client daemon that can be installed on these external devices. The 
service sends periodic heartbeats to these external devices, which are configured to 
expect these heartbeats. If a device does not receive a heartbeat at the expected time, it 
can query the service to verify the latter’s health. If the system returns a 2xx response, 
the device assumes there was a temporary network connectivity problem and takes 
no further action. If the request times out or returns an error, the device can alert its 
user(s) by automated phone calls, texting, email, push notifications, and/or other 
channels. This is essentially an independent, specialized, small-scale monitoring and 
alerting service that serves only one specific purpose and sends alerts to only a few users.
9.15	 Other possible discussion topics
We can also scale (increase or decrease) the amount of memory of the Kafka cluster 
if necessary. If the number of events in the queues monotonically increases over time, 
notifications are not being delivered, and we must either scale up the consumer cluster 
to process and deliver these notification events or implement rate limiting and inform 
the relevant users about their excessive use. 
We can consider auto-scaling for this shared service. However, auto-scaling solutions 
are tricky to use in practice. In practice, we can configure auto-scaling to automatically 
increase cluster sizes of the service’s various components up to a limit to avoid outages 
on unforeseen traffic spikes, while also sending alerts to developers to further increase 
resource allocation if required. We can manually review the instances where auto-scaling was triggered and refine the auto-scaling configurations accordingly.
A detailed discussion of a notification service can fill an entire book and include 
many shared services. To focus on the core components of a notification service and 
keep the discussion to a reasonable length, we glossed over many topics in this chapter. 
We can discuss these topics during any leftover time in the interview:
¡ A recipient should be able to opt into notifications and out of unwanted notifications; otherwise, they are just spam. We can discuss this feature. 
¡ How can we address the situation where we need to correct a notification that has 
already been sent to a large number of users? 


	
221
Final notes 
–	 If we discovered this error while the notification is being sent, we may wish to 
cancel the process and not send the notification to the remaining recipients. 
–	 For devices where the notifications haven’t yet been triggered, we can cancel 
notifications that haven’t been triggered.
–	 For devices where the notifications have already been triggered, we will need 
to send a follow-up notification to clarify this error. 
¡ Rather than rate-limiting a sender regardless of which channels it uses, design a 
system that also allows rate limiting on individual channels. 
¡ Possibilities for analytics include:
–	 Analysis of notification delivery times of various channels, which can be used 
to improve performance. 
–	 Notification response rate and tracking and analytics on user actions and 
other responses to notifications. 
–	 Integrating our notification system with an A/B test system. 
¡ APIs and architecture for the additional template service features we discussed 
in section 9.5.2.
¡ A scalable and highly available job scheduler service.
¡ Systems design of the address group service to support the features that we discussed in section 9.7. We can also discuss other features such as:
–	 Should we use a batch or streaming approach to process unsubscribe requests?
–	 How to manually resubscribe a recipient to notifications.
–	 Automatically resubscribe a recipient to notifications if the recipient’s device 
or account makes any other requests to any service in our organization. 
¡ An approval service for obtaining and tracking the relevant approvals to send 
notifications to a large number of recipients. We can also extend this discussion 
to system design of mechanisms to prevent abuse or send unwanted notifications. 
¡ Further details on the monitoring and alerts, including examples and elaboration of the exact metrics and alerts to define. 
¡ Further discussion on the client daemon solution.
¡ Design our various messaging services (e.g., design an email service, SMS service, 
automated phone call service, etc.).
9.16	 Final notes 
Our solution is scalable. Every component is horizontally scalable. Fault-tolerance is 
extremely important in this shared service, and we have constantly paid attention to it. 
Monitoring and availability are robust; there is no single point of failure, and the monitoring and alerting of system availability and health involves independent devices.


222
Chapter 9  Design a notification/alerting service 
Summary
¡ A service that must serve the same functionality to many different platforms 
can consist of a single backend that centralizes common processing and directs 
requests to the appropriate component (or another service) for each platform.
¡ Use a metadata service and/or object store to reduce the size of messages in a 
message broker queue.
¡ Consider how to automate user actions using templates.
¡ We can use a task scheduling service for periodic notifications.
¡ One way to deduplicate messages is on the receiver’s device.
¡ Communicate between system components via asynchronous means like sagas.
¡ We should create monitoring dashboards for analytics and tracking errors.
¡ Do periodic auditing and anomaly detection to detect possible errors that our 
other metrics missed.


223
10
Design a database 
batch auditing service
This chapter covers
¡ Auditing database tables to find invalid data
¡ Designing a scalable and accurate solution to 	
	 audit database tables
¡ Exploring possible features to answer an  
	 unusual question
Let’s design a shared service for manually defined validations. This is an unusually 
open-ended system design interview question, even by the usual standards of system 
design interviews, and the approach discussed in this chapter is just one of many 
possibilities. 
We begin this chapter by introducing the concept of data quality. There are many 
definitions of data quality. In general, data quality can refer to how suitable a dataset 
is to serve its purpose and may also refer to activities that improve the dataset’s suitability for said purpose. There are many dimensions of data quality. We can adopt 
the dimensions from https://www.heavy.ai/technical-glossary/data-quality: 
¡ Accuracy—How close a measurement is to the true value. 
¡ Completeness—Data has all the required values for our purpose.
¡ Consistency—Data in different locations has the same values, and the different 
locations start serving the same data changes at the same time. 


224
Chapter 10  Design a database batch auditing service 
¡ Validity—Data is correctly formatted, and values are within an appropriate range. 
¡ Uniqueness—No duplicate or overlapping data. 
¡ Timeliness—Data is available when it is required. 
Two approaches in validating data quality are anomaly detection, which we discussed 
in section 2.5.6, and manually defined validations. In this chapter, we will discuss only 
manually defined validations. For example, a certain table may be updated hourly and 
occasionally have no updates for a few hours, but it may be highly unusual for two 
updates to be more than 24 hours apart. The validation condition is “latest timestamp 
is less than 24 hours ago.” 
Batch auditing with manually defined validations is a common requirement. A transaction supervisor (section 5.5) is one of many possible use cases, though a transaction 
supervisor does not just check whether data is valid but also returns any data differences 
between the multiple services/databases that it compares, as well as the operations 
needed to restore consistency to those services/databases. 
10.1	 Why is auditing necessary?
The first impression of this question may be that it doesn’t make sense. We may argue 
that other than the case of a transaction supervisor, batch auditing may encourage bad 
practices.
For example, if we have a situation where data was invalid due to data loss in databases or file systems that are not replicated or backed up, then we should implement 
replication or backup instead of losing the data. However, replication or backup may 
take seconds or longer, and the leader host may fail before the data is successfully replicated or backed up. 
Preventing data loss
One technique that prevents data loss from occurring due to late replication is quorum 
consistency (i.e., write to a majority of hosts/nodes in the cluster before returning a success response to the client). In Cassandra, a write is replicated to an in-memory data 
structure called Memtable across multiple nodes before returning a success response. 
Writing to memory is also much faster than writing to disk. The Memtable is flushed to 
disk (called an SSTable) either periodically or when it reaches a certain size (e.g., 4 MB).
If the leader host recovers, the data may be recovered and then replicated to other 
hosts. However, this will not work in certain databases like MongoDB that, depending 
on its configuration, can deliberately lose data from a leader host to maintain consistency (Arthur Ejsmont, Web Scalability for Startup Engineers, McGraw Hill Education, 
2015, pp. 198–199. In a MongoDB database, if the write concern (https://www.mongodb.com/docs/manual/core/replica-set-write-concern/) is set to 1, all nodes must 
be consistent with the leader node. If a write to the leader node is successful, but the 
leader node fails before replication occurs, the other nodes use a consensus protocol 


	
225
Why is auditing necessary?
to select a new leader. If the former leader node recovers, it will roll back any data that 
is different from the new leader node, including such writes.
We can also argue that data should be validated at the time a service receives it, 
not after it has already been stored to a database or file. For example, when a service 
receives invalid data, it should return the appropriate 4xx response and not persist this 
data. The following 4xx codes are returned for write requests with invalid data. Refer to 
sources like https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_
error_responses for more information
¡ 400 Bad Request—This is a catch-all response for any request that the server perceives to be invalid. 
¡ 409 Conflict—The request conflicts with a rule. For example, an upload of a file 
that is older than the existing one on the server. 
¡ 422 Unprocessable Entity—The request entity has valid syntax but could not be processed. An example is a POST request with a JSON body containing invalid fields. 
One more argument against auditing is that validation should be done in the database 
and application, rather than an external auditing process. We can consider using database constraints as much as possible because applications change much faster than 
databases. It is easier to change application code than database schema (do database 
migrations). At the application level, the application should validate inputs and outputs, and there should be unit tests on the input and output validation functions. 
Database constraints
There are arguments that database constraints are harmful (https://dev.to/jonlauridsen/ 
database-constraints-considered-harmful-38), that they are premature optimizations, 
do not capture all data integrity requirements, and make the system more difficult to 
test and to adjust to changing requirements. Some companies like GitHub (https:// 
github.com/github/gh-ost/issues/331#issuecomment-266027731) and Alibaba (https:// 
github.com/alibaba/Alibaba-Java-Coding-Guidelines#sql-rules) forbid foreign key co­n­- 
stra­ints. 
In practice, there will be bugs and silent errors. Here is an example that the author has 
personally debugged. A POST endpoint JSON body had a date field that should con­
tain a future date value. POST requests were validated and then written to a SQL table. 
There was also a daily batch ETL job that processed objects marked with the current 
date. Whenever a client made a POST request, the backend validated that the cli­ent’s 
date value had the correct format and was set up to one week in the future. 
However, the SQL table contained a row with a date set five years in the future, 
and this went undetected for five years until the daily batch ETL job processed it, and 
the invalid result was detected at the end of a series of ETL pipelines. The engineers 
who wrote this code had left the company, which made the problem more difficult to 
debug. The author examined the git history and found that this one-week rule was not 


226
Chapter 10  Design a database batch auditing service 
implemented until months after the API was first deployed to production and deduced 
that an invalid POST request had written this offending row. It was impossible to confirm this as there were no logs for the POST request because the log retention period 
was two weeks. A periodic auditing job on the SQL table would have detected this error, 
regardless of whether the job was implemented and started running long after the data 
was written. 
Despite our best efforts to stop any invalid data from being persisted, we must assume 
that this will happen and be prepared for it. Auditing is another layer of validation 
checks. 
A common practical use case for batch auditing is to validate large (e.g., >1 GB) files, 
especially files from outside our organization over which we have not been able to control how they were generated. It is too slow for a single host to process and validate each 
row. If we store the data in a MySQL table, we may use LOAD DATA (https://dev.mysql 
.com/doc/refman/8.0/en/load-data.html), which is much faster than INSERT, then 
run SELECT statements to audit the data. A SELECT statement will be much faster 
and also arguably easier than running a script over a file, especially if the SELECT takes 
advantage of indexes. If we use a distributed file system like HDFS, we can use NoSQL 
options like Hive or Spark with fast parallel processing. 
Moreover, even if invalid values are found, we may decide that dirty data is better 
than no data and still store them in a database table.
Last, there are certain problems that only batch auditing can find, such as duplicate 
or missing data. Certain data validation may require previously ingested data; for example, anomaly detection algorithms use previously ingested data to process and spot 
anomalies in currently ingested data. 
10.2	 Defining a validation with a conditional statement on a SQL query’s 
result 
Terminology clarification: A table has rows and columns. An entry in a particular (row, 
column) coordinate can be referred to as a cell, element, datapoint, or value. In this 
chapter, we use these terms interchangeably. 
Let’s discuss how a manually defined validation can be defined by comparison operators on the results of a SQL query. The result of a SQL query is a 2D array, which 
we will name “result”. We can define a conditional statement on result. Let’s go over 
some examples. All these examples are daily validations, so we validate only yesterday’s 
rows, and our example queries have the WHERE clause “Date(timestamp) > Curdate() 
- INTERVAL 1 DAY”. In each example, we describe a validation, followed by its SQL 
query and then possible conditional statements. 
Manually defined validations can be defined on 
¡ Individual datapoints of a column—An example is the “latest timestamp is < 24 
hours old” that we discussed previously. 
SELECT COUNT(*) AS cnt 
FROM Transactions 
WHERE Date(timestamp) >= Curdate() - INTERVAL 1 DAY 


	
227
Defining a validation with a conditional statement on a SQL query’s result 
Possible true conditional statements are result[0][0] > 0 and result['cnt']
[0] > 0.
Let’s discuss another example. If a particular coupon code ID expires on a certain date, we can define a periodic validation on our transactions table that raises 
an alert if this code ID appears after this date. This may indicate that coupon 
code IDs are being recorded incorrectly. 
SELECT COUNT(*) AS cnt
FROM Transactions 
WHERE code_id = @code_id AND Date(timestamp) > @date  
‰AND Date(timestamp) = Curdate() - INTERVAL 1 DAY 
Possible true conditional statements are result[0][0] 
== 
0 and: 
result['cnt'][0] == 0. 
¡ Multiple datapoints of a column—For example, if an individual app user cannot 
make more than five purchases per day, we can define a daily validation on our 
transactions table that raises an alert if there are more than five rows for any 
user ID since the previous day. This may indicate bugs, that a user was erroneously able to make more than five purchases that day, or that purchases are being 
incorrectly recorded. 
SELECT user_id, count(*) AS cnt
FROM Transactions 
WHERE Date(timestamp) = Curdate() - INTERVAL 1 DAY 
GROUP BY user_id 
The conditional statement is result.length <= 5.
Another possibility: 
SELECT * 
FROM ( 
  SELECT user_id, count(*) AS cnt
FROM Transactions
  WHERE Date(timestamp) = Curdate() - INTERVAL 1 DAY 
  GROUP BY user_id 
) AS yesterday_user_counts 
WHERE cnt > 5; 
The conditional statement is result.length == 0.
¡ Multiple columns in a single row—For example, the total number of sales that uses a 
particular coupon code cannot exceed 100 per day. 
SELECT count(*) AS cnt
FROM Transactions 
WHERE Date(timestamp) = Curdate() - INTERVAL 1 DAY  
‰AND coupon_code = @coupon_code 
The conditional statement is result.length <= 100.
An alternative query and conditional statement are as follows: 


228
Chapter 10  Design a database batch auditing service 
SELECT *
FROM ( 
  SELECT count(*) AS cnt
FROM Transactions 
WHERE Date(timestamp) = Curdate() - INTERVAL 1 DAY  
‰AND coupon_code = @coupon_code 
) AS yesterday_user_counts 
WHERE cnt > 100; 
The conditional statement is result.length == 0.
¡ Multiple tables—For example, if we have a fact table sales_na to record sales in 
North America, that has a country_code column, we can create a dimension table 
country_codes that has a list of country codes for each geographical region. We 
can define a periodic validation that checks that all new rows have country_code 
values of countries within North America: 
SELECT * 
FROM sales_na S JOIN country_codes C ON S.country_code = C.id 
WHERE C.region != 'NA'; 
The conditional statement is result.length == 0. 
¡ A conditional statement on multiple queries—For example, we may wish to raise an 
alert if the number of sales on a day changes by more than 10% compared to the 
same day last week. We can run two queries and compare their results as follows. 
We append the query results to a result array, so this result array is 3D instead 
of 2D:
SELECT COUNT(*)
FROM sales
WHERE Date(timestamp) = Curdate()
SELECT COUNT(*)
FROM sales
WHERE Date(timestamp) = Curdate() - INTERVAL 7 DAY
The conditional statement is Math.abs(result[0][0][0] – result[1][0][0]) / 
result[0][0][0] < 0.1.
There are countless other possibilities for manually defined validations, such as: 
¡ A minimum number of new rows can be written each hour to a table. 
¡ A particular string column cannot contain null values, and string lengths must be 
between 1 and 255. 
¡ A particular string column must have values that match a particular regex. 
¡ A particular integer column should be nonnegative. 
Some of these types of constraints can also be implemented by function annotations in 
ORM libraries (e.g., @NotNull and @Length(min = 0, max = 255)) in Hibernate or 
constraint types in Golang’s SQL package. In this case, our auditing service serves as an 
additional layer of validation. Failed audits indicate silent errors in our service, which 
we should investigate. 


	
229
A simple SQL batch auditing service
This section’s examples were in SQL. We can generalize this concept to define validation queries in other query languages like HiveQL, Trino (formerly called PrestoSQL), or Spark. Though our design focuses on defining queries using database query 
languages, we can also define validation functions in general purpose programming 
languages. 
10.3	 A simple SQL batch auditing service
In this section, we first discuss a simple script for auditing a SQL table. Next, we discuss 
how we can create a batch auditing job from this script.
10.3.1	 An audit script
The simplest form of a batch auditing job is a script that does the following steps:
1	 Runs a database query
2	 Reads the result into a variable
3	 Checks the value of this variable against certain conditions
The example Python script in the following listing runs a MySQL query that checks if 
the latest timestamp of our transactions table is < 24 hours old and prints the result to 
console.
Listing 10.1     Python script and MySQL query to check the latest timestamp
import mysql
cnx = mysql.connector.connect(user='admin', password='password',
                         host='127.0.0.1',
                         database='transactions')
cursor = cnx.cursor()
query = """
SELECT COUNT(*) AS cnt 
FROM Transactions 
WHERE Date(timestamp) >= Curdate() - INTERVAL 1 DAY 
"""
cursor.execute(query)
results = cursor.fetchall()
cursor.close()
cnx.close()
# result[0][0] > 0 is the condition.
print(result[0][0] > 0) # result['cnt'][0] > 0 also works.
We may need to run several database queries and compare their results. Listing 10.2 is 
a possible example. 


230
Chapter 10  Design a database batch auditing service 
Listing 10.2     An example script that compares the results of several queries 
import mysql
queries = [
    {
    'database': 'transactions',
    
   'query': """
	
	
   SELECT COUNT(*) AS cnt 
        FROM Transactions 
        WHERE Date(timestamp) >= Curdate() - INTERVAL 1 DAY 
    """,
},
{
    `database': 'transactions`,
    'query': """
        SELECT COUNT(*) AS cnt 
        FROM Transactions 
        WHERE Date(timestamp) >= Curdate() - INTERVAL 1 DAY 
        """
    }
]
results = []
for query in queries:
     cnx = mysql.connector.connect(user='admin', password='password',
                             host='127.0.0.1',
                             database=query['database'])
        cursor = cnx.cursor()
     cursor.execute(query['query'])
     results.append(cursor.fetchall())
cursor.close()
cnx.close()
print(result[0][0][0] > result[1][0][0])
10.3.2	 An audit service
Next, let’s extend this to a batch auditing service. We can generalize the script to allow 
a user to specify
1	 The SQL databases and queries.
2	 The condition that will be run on the query result. 
Let’s implement a Python file template that we can name validation.py.template. 
Listing 10.3 is a possible implementation of this file. This is a simplified implementation. The batch auditing job is divided into two phases: 
1	 Run the database queries and use their results to determine whether the audit 
passed or failed.
2	 If the audit failed, trigger an alert.


	
231
A simple SQL batch auditing service
In a practical implementation, the login credentials will be supplied by a secrets management service, and the host is read from a configuration file. These details are outside the scope of this question. The user story for this service can be as follows:
1	 The user logs in to the service and creates a new batch auditing job.
2	 The user inputs the values for database, queries, and condition.
3	 Our service will create a validation.py file from this validation.py.template 
and replace the parameters like {database} with the user’s input values.
4	 Our service creates a new Airflow or cron job that imports validation.py and runs 
the validation function.
We may notice that these validation.py files are essentially functions. A batch ETL service stores functions rather than objects.
We commented in the validation.py.template that we should create an Airflow 
task for each database query. Our backend should generate such a validation.py file. 
This will be a good coding interview exercise but is outside the scope of a system design 
interview. 
Listing 10.3    A Python file template for an audit service
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BranchPythonOperator
import mysql.connector
import os
import pdpyras
# Example user inputs:
# {name} – ''
# {queries} – ['', '']
# {condition} – result[0][0][0] result[1][0][0]
def _validation():
  results = []
  # Database queries are expensive. An issue with running every query here
  # is that if a query fails, all queries need to be rerun. 
  # We can consider instead creating an Airflow task for each query.
  for query in {queries}:
    cnx = mysql.connector.connect(user='admin', password='password',
                               host='127.0.0.1',
                               database=query['database'])
    cursor = cnx.cursor()
    cursor.execute(query['query'])
  results.append(cursor.fetchall())
  cursor.close()
  cnx.close()
  # XCom is an Airflow feature to share data between tasks. 
  ti.xcom_push(key='validation_result_{name}', value={condition})
def _alert():
  # Some sample code to trigger a PagerDuty alert if the audit failed.
  # This is just an example and should not be taken as working code.


232
Chapter 10  Design a database batch auditing service 
  # We may also wish to send this result to our Backend Service. 
  # This is discussed later in this chapter. 
  result = ti.xcom_pull(key='validation_result_{name}')
  if result:
    routing_key = os.environ['PD_API_KEY']
    session = pdpyras.EventsAPISession(routing_key)
    dedup_key = session.trigger("{name} validation failed", "audit")
with DAG(
    {name},
    default_args={
       'depends_on_past': False,
       'email': ['zhiyong@beigel.com'],
       'email_on_failure': True,
       'email_on_retry': False,
       'retries': 1,
       'retry_delay': timedelta(minutes=5),
 },
 description={description},
 schedule_interval=timedelta(days=1),
 start_date=datetime(2023, 1, 1),
 catchup=False,
 tags=['validation', {name}],
) as dag:
 t1 = BranchPythonOperator(
     task_id='validation',
     python_callable=_validation
 )
 # Alerting is a separate Airflow task, so in case the alert fails,
 # the Airflow job does not rerun the expensive validation function.
 t2 = BranchPythonOperator(
     task_id='alert',
     python_callable=_alert
 )
 t1 >> t2
10.4	 Requirements 
Let’s design a system where users can define SQL, Hive, or Trino (formerly called 
Presto) queries for periodic batch audits of their database tables. Functional requirements are as follows: 
¡ CRUD audit jobs. An audit job has the following fields: 
–	 Interval, such as minute, hour, day, or custom time intervals 
–	 Owners 
–	 A validation database query in SQL or related dialects like HQL, Trino, 
Cassandra, etc.
–	 A conditional statement on the SQL query result 
¡ A failed job should trigger an alert 
¡ View logs of past and currently running jobs, including whether there were 
errors, and the results of their conditional statements. Users should also be able 


	
233
High-level architecture
to view the status and history of any triggered alerts, such as what time they were 
triggered and whether and, if so, what time they were marked as resolved.
¡ A job must complete within 6 hours. 
¡ A database query must complete within 15 minutes. Our system should disallow 
jobs with long-running queries.
Non-functional requirements are as follows: 
¡ Scale—We project that there will be less than 10000 jobs (i.e., 10000 database statements). The jobs and their logs are read only through our UI, so traffic is low. 
¡ Availability—This is an internal system that no other systems directly depend on. 
High availability is not required. 
¡ Security—Jobs have access control. A job can only be CRUD by its owners. 
¡ Accuracy—The audit job result should be accurate as defined by the job’s 
configuration. 
10.5	 High-level architecture
Figure 10.1 is an initial high-level architecture diagram of a hypothetical service for 
users to define periodic validation checks on their tables. We assume that the batch 
ETL service is an Airflow service or works similarly to Airflow. It stores the Python files 
of the batch jobs, runs them at their defined schedules, stores the status and history of 
these jobs, and returns Boolean values indicating if their audit conditions were true or 
false. Users will interact with our UI, which makes requests through our backend: 
1	 Users make requests to a shared batch ETL service to CRUD the batch auditing 
jobs, including checking on the status and history of these jobs. 
2	 Our shared batch ETL service is not an alerting service, so it does not have API 
endpoints to trigger alerts or to view the status and history of any triggered alerts. 
Users make requests to a shared alerting service via our UI and backend to view 
this information.
User
Backend
UI
Batch 
ETL 
Service
Alerting 
Service
Presto
Hive
Spark
SQL
Figure 10.1    Initial 
high-level architecture 
of a hypothetical 
service for users 
to define periodic 
validation checks on 
their data. 


234
Chapter 10  Design a database batch auditing service 
When a user submits a request to create a batch auditing job, the following steps occur:
1	 Our backend service creates the validation.py file by substituting user’s input values into the template. Since this template is just a short string, it can be stored in 
memory on every backend service host. 
2	 Our backend service sends a request to the batch ETL service with this file. The 
batch ETL service creates the batch ETL job and stores this file, then returns a 
200 success response to our backend service.
Our batch auditing service is essentially a wrapper over a shared Batch ETL Service. 
An audit job’s configuration has fields such as the job’s owners, a cron expression, 
the database type (Hive, Trino, Spark, SQL, etc.) and the query to execute. The main 
SQL table will store the audit jobs’ configurations, which we can name job_config. We 
can also create an owner table that maps jobs to their owners and has the columns 
job_id and owner_id.
Since validation queries can be defined in various SQL-like dialects, our batch ETL 
service is connected to various shared databases such as SQL, Hive, Trino, Spark, Cassandra, etc. If a job fails or there are any failed audits, the batch ETL service makes 
requests to a shared alerting service to alert the relevant persons. For security, we can 
use a shared OpenID Connect service for authentication, which is discussed in appendix B.
10.5.1	 Running a batch auditing job 
An audit job is periodically run with the configured time interval and has two main 
steps:
1	 Run the database query. 
2	 Run the conditional statement with the database query’s result. 
Referring to section 4.6.1, a batch ETL job is created as a script (e.g., Python script in 
an Airflow service). When the user creates an audit job, our backend can generate the 
corresponding Python script. This generation can utilize a template script that we had 
predefined and implemented. This template script can contain several sections where 
the appropriate parameters (interval, database query, and conditional statement) are 
substituted. 
The main scalability challenges are on the batch ETL service and possibly the alerting service, so a scalability discussion is about designing a scalable batch ETL service 
and scalable alerting service. Refer to chapter 9 for a detailed discussion on an alerting 
service.
Since the user’s audit job is mainly defined as a validation function that runs an 
SQL statement, we also suggest using a Function as a Service (FaaS) platform and take 
advantage of its built-in scalability. We can create safeguards against anomalous queries, 
such as a 15-minute limit on query execution time, or suspend the job if the query result 
is invalid.


	
235
High-level architecture
The result of each audit job run can be stored in our SQL database and accessed by 
users via our UI.
10.5.2	 Handling alerts
Should alerts regarding failed audits be triggered by our batch ETL service or by our 
backend? Our first thought may be that it is our batch ETL service that runs the auditing jobs, so it should trigger such alerts. However, this means that the alerting functionalities used by our batch auditing service are split between two of its components:
¡ Requests to trigger alerts are made by our batch ETL service.
¡ Requests to view alert status and history are made from our backend service.
This means that the configuration to connect to our alerting service must be made on 
both services, which is additional maintenance overhead. A future team maintaining 
this batch auditing service may have different engineers who are unfamiliar with the 
code, and if there are problems with alerts, they may initially erroneously believe that 
interactions with the alerting service are all on one service and may waste time debugging on the wrong service before they find out that the problem was on the other 
service. 
Thus, we may decide that all interactions with our alerting service should be on our 
backend service. A batch ETL job will only check if the condition is true or false and 
send this Boolean value to our backend service. If the value is false, our backend service 
will trigger an alert on our alerting service. 
However, this approach may cause a possible bug. If the backend service host handling generating and making alert request crashes or becomes unavailable, the alert 
may not be sent. Some possible ways to prevent this bug are the following:
¡ The request from our batch ETL service to our backend service can be blocking, 
and the backend service returns a 200 only after it has successfully sent the alert 
request. We can rely on the retry mechanisms of our batch ETL service (such as 
the retry mechanisms in Airflow) to ensure the alert request is made. However, 
this approach means that our batch ETL service is essentially still making the 
alert request, and tightly couples these two services. 
¡ Our batch ETL service can produce to a partitioned Kafka topic, and our backend service hosts can consume from these partitions, and checkpoint on each 
partition (possibly using SQL). However, this may cause duplicate alerts, as a 
backend service host may fail after making the alert request but before checkpointing. Our alerting service needs to be able to deduplicate alerts. 
Our current architecture does both logging and monitoring. It logs the audit results 
to SQL. It monitors these audit jobs; if a job fails, our batch auditing service triggers an 
alert. Only alerting is done by a shared service.
An alternative approach is to log the audit job results both to SQL and a shared 
logging service. We can use another SQL table for checkpointing every few results. 


236
Chapter 10  Design a database batch auditing service 
Referring to the sequence diagram in figure 10.2, each time a host recovers from a 
failure, it can query this SQL table to obtain the last checkpoint. Writing duplicate logs 
to SQL is not a problem because we can simply use “INSERT INTO <table> IF NOT 
EXISTS…” statements. Writing duplicate results to the logging service can be handled 
in three ways:
1	 Assume that the consequences of duplicate logs are trivial, and simply write them 
to the logging service. 
2	 The logging service should handle duplicates. 
3	 Query the logging service to determine whether a result exists before writing to 
it. This will double our traffic to the logging service. 
par
Batch ETL
Service
Logging
Service
Write result.
Response OK
Monitoring
Service
Monitor
SQL
Service
Backend
Service
Write
result.
Kafka
Results Topic
Produce
Response
OK
Consume
Alerting
Service
Response
OK
Trigger
alert
Response OK
Write checkpoint
Response
OK
Figure 10.2    Sequence diagram which illustrates logging in parallel to a logging service and SQL 
service. We can monitor and alert on the SQL service. 
Figure 10.3 shows our revised high-level architecture with our shared logging and 
monitoring services. Logging and alerting are decoupled from the batch ETL service. 
The developers of the batch ETL service need not be concerned with changes to the 
alerting service and vice versa, and the batch ETL service need not be configured to 
make requests to the alerting service. 


	
237
Constraints on database queries
User
Backend
UI
Logging 
Service
SQL
Monitoring
Service
Alerting
Service
Batch 
ETL Service
Spark
Presto
Hive
Figure 10.3    High-level architecture using shared services. Every service logs to the shared logging 
service, but we only illustrate its relationship with the backend and monitoring services.
10.6	 Constraints on database queries
Database queries are the most expensive and longest-running computations in many 
services, including this one. For reasons including the following, the batch ETL service 
should be constrained in the rate and duration of queries it is allowed to run:
¡ The various database services are shared services. Any user who runs long and 
expensive queries significantly decreases the service’s remaining capacity to 
serve queries by other users and increases the latency across the board. Queries 
consume CPU and memory on their hosts. Each connection to a database service also consumes a thread; the process on this thread executes the query and 
collects and returns the query results. We can allocate a thread pool containing 
a limited number of threads so there will never be too many concurrent queries.
¡ Our database services may be provided by third-party cloud providers who bill on 
usage, and expensive and long-running queries will cost a lot of money.
¡ The batch ETL service has a schedule of queries to execute. It must ensure that 
every query can be executed within its period. For example, an hourly query 
must complete within one hour.
We can implement techniques to parse a user’s query definition as they author it in a 
job configuration, or when they submit the query together with the rest of the job configuration to our backend. 
In this section, we discuss constraints we can implement on user queries to fulfill our 
system’s requirements and control costs.


238
Chapter 10  Design a database batch auditing service 
10.6.1	 Limit query execution time
A simple way to prevent expensive queries is to limit query execution time to 10 minutes when the owner is creating or editing a job configuration and to 15 minutes when 
the job is running. When a user is authoring or editing a query in a job configuration, 
our backend should require the user to run the query and validate that it takes less 
than 10 minutes before allowing the user to save the query string. This will ensure that 
users are trained to keep their queries within a 10-minute limit. An alternative is to 
present a nonblocking/asynchronous experience. Allow a user to save a query, execute 
the query, then alert the user via email or chat of whether their query ran successfully 
within 10 minutes, so their job configuration is accepted or rejected accordingly. A 
tradeoff of this UX is that owners may be reluctant to change their query strings, so 
possible bugs or improvements may not be addressed.
We may wish to prevent multiple users from concurrently editing a query and overwriting each other’s updates. Refer to section 2.4.2 for a discussion on preventing this.
If a query’s execution exceeds 15 minutes, terminate the query, disable the job until 
the owner edits and validates the query, and trigger a high-urgency alert to the owners. 
If a query’s execution exceeds 10 minutes, trigger a low-urgency alert to the job configuration’s owners to warn them of the consequences that their query may exceed 15 
minutes in the future. 
10.6.2	 Check the query strings before submission
Rather than making a user wait for minutes before saving a job configuration or 
informing the user 10 minutes after they saved a configuration that it was rejected, it 
will be more convenient to users if our UI can provide immediate feedback to them 
on their query strings as they are authoring them to prevent them from submitting 
job configurations with invalid or expensive queries. Such validation may include the 
following.
Do not allow full table scans. Allow queries to run on only tables that contain partition keys, and queries must contain filters on partition keys. We can also consider 
going a step further and limiting the number of partition key values within a query. To 
determine a table’s partition keys, our backend will need to run a DESCRIBE query on 
the relevant database service. Do not allow queries that contain JOINs, which can be 
extremely expensive.
After a user defines a query, we can display the query execution plan to the user, 
which will allow the user to tune the query to minimize its execution time. This feature 
should be accompanied by references to guides on tuning queries in the relevant database query language. Refer to https://www.toptal.com/sql-server/sql-database-tuning 
-for-developers for a guide on SQL query tuning. For guides to tuning Hive queries, 
refer to https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Explain 
or the chapter titled “Performance Considerations” in Dayang Du, Apache Hive Essentials, Packt Publishing, 2018.


	
239
Prevent too many simultaneous queries
10.6.3	 Users should be trained early
Our users who author the queries should be instructed in these constraints early, so 
they can learn to adapt to these constraints. We should also provide good UX and 
instructive documentation to guide our users in these constraints. Moreover, these 
constraints should preferably be defined and set in an early release of our database 
batch auditing service, rather than added months after the first release. If our users 
were allowed to submit expensive queries before we impose these constraints, they may 
resist and argue against these constraints, and it may be difficult or impossible to persuade them to change their queries.
10.7	 Prevent too many simultaneous queries
We should configure a limit for the number of simultaneous queries that the batch 
ETL service can execute. Each time a user submits a job configuration, which will contain a query to be run with a particular schedule, the backend can check the number of 
queries scheduled to be executed simultaneously on the same database and trigger an 
alert to our service’s developers if the number of simultaneous queries approaches the 
estimated capacity. We can monitor the waiting time of each query before it begins execution and trigger low-urgency alerts if the waiting time exceeds 30 minutes or another 
benchmark value that we decide on. We can also investigate designing load-testing 
schemes to estimate the capacity. Our revised high-level architecture is illustrated in 
figure 10.4.
User
Backend
UI
Backend
Spark
Presto
Hive
Query Service
Logging 
Service
SQL
Monitoring
Service
Alerting
Service
Batch 
ETL Service
Figure 10.4    Revised 
high-level architecture 
with a shared query 
service through which 
other services make 
database requests. 


240
Chapter 10  Design a database batch auditing service 
Figure 10.4 contains a new database query service. Since the databases are shared services, cross-cutting concerns such as the configured limit on the number of simultaneous queries should be stored on the database query service, not in our database 
auditing service.
Another possible optimization is that the batch ETL service can query the alerting 
service via our backend service before running a database query to check whether there 
are any unresolved alerts. If so, there is no need to proceed with the audit job. 
10.8	 Other users of database schema metadata
To assist users in authoring queries, our service can automatically derive job configurations from schema metadata. For example, WHERE filters are usually defined on 
partition columns, so the UI can present query templates that suggest these columns 
to the user or suggest to the user to author a query that only tests the latest partition. 
By default, if a new partition passes an audit, our service should not schedule any more 
audits for that partition. Our users may have reasons to rerun the same audit despite 
it passing. For example, an audit job may contain bugs and erroneously pass, and the 
job owner may need to edit the audit job and rerun passing audits. So, our service may 
allow users to manually rerun an audit or schedule a limited number of audits on that 
partition. 
Tables may have a freshness SLA on how often new roles are appended. This is 
related to the concept of data freshness, about how up-to-date or recent the data is. An 
audit on a table should not be done before the data is ready, as this is wasteful and will 
trigger false alerts. Perhaps the database query service can implement a feature to allow 
table owners to configure freshness SLAs on their tables, or we can develop a database 
metadata catalog/platform for our organization using a tool like Amundsen (https://
www.amundsen.io/), DataHub (https://datahubproject.io/), or Metacat (https://
github.com/Netflix/metacat). 
Another useful feature of a database metadata platform is to record incidents regarding its tables. A table owner or our service can update the database metadata platform 
that a particular table is experiencing problems. Our database query service can warn 
any person or service that queries this table about the failed audits. A user who queries 
a table may query the table again in the future, so a useful feature in our database metadata platform is to allow users to subscribe to changes in the table’s metadata or to be 
alerted to problems that affect the table.
Our batch ETL service can also monitor changes to database schema and respond 
accordingly. If a column’s name was changed, it should update this column name in 
audit job configuration query strings that contain it. If a column is deleted, it should 
disable all related jobs and alert their owners. 


	
241
Auditing a data pipeline
10.9	 Auditing a data pipeline
Figure 10.5 illustrates a data pipeline (such as an Airflow DAG) and its multiple tasks. 
Each task may write to certain table(s), which are read by the next stage. A job configuration can contain fields for “pipeline name” and “level,” which can be added columns 
in our job_config table. 
A
B
C
D
Level 1
Level 2
Level 3
Figure 10.5    A sample data pipeline that has multiple stages. We can create audit jobs for each stage. 
When a particular audit job fails, our service should do the following:
¡ Disable the downstream audits to save resources because it is a meaningless waste 
to execute audit jobs if their upstream jobs had failed. 
¡ Disable other jobs that contain queries to this table and their downstream jobs, 
too.
¡ Trigger high-urgency alerts to the owners of all disabled jobs and to the owners of 
all downstream jobs.
We should also update our database metadata platform that this table has a problem. Any data pipeline that uses this table should disable all tasks downstream of this 
table, or bad data from this table may propagate into downstream tables. For example, 
machine-learning pipelines can use audit results to determine whether they should 
run, so experiments are not run with bad data. Airflow already allows users to configure 
trigger rules (https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags 
.html#trigger-rules) so that each task runs only if all its dependencies or at least one 
dependency successfully finishes execution. Our new batch ETL service feature is an 
enhancement to Airflow and other workflow management platforms.
All this suggests that our batch ETL service can be generalized into a shared service, 
so it can provide this feature to batch ETL jobs across our organization.
When the user adds a new level to a pipeline, they also need to update the level values of all downstream tasks. As illustrated in figure 10.6, our backend can assist them by 
automatically incrementing the level numbers of downstream tasks.


242
Chapter 10  Design a database batch auditing service 
A
B
C
E
Level 1
Level 2
Level 3
D
Level 3 ° 4
Figure 10.6    When we add a new task “E” in between levels 2 and 3, we can automatically increment 
the number(s) of the appropriate level(s), so level 3 becomes level 4.
10.10	Logging, monitoring, and alerting 
Adding to what was discussed in section 2.5, we should monitor and send alerts for the 
following. The following logs may be useful to users and can be displayed on our UI: 
¡ The current job status (e.g., started, in progress, succeeded, failed) and the time 
this status was logged. 
¡ Failed batch ETL service database queries. The alert should also contain the reason for the failure, such as query time out or an error in query execution.
¡ As mentioned earlier, monitor the time taken to execute the database queries 
and raise alerts if this time exceeds a benchmark value we decide on.
¡ As mentioned earlier, alert job owners if upstream jobs fail.
¡ One-second P99 and 4xx and 5xx responses of our backend endpoints. 
¡ One-second P99 and 4xx and 5xx responses on requests to external services. 
¡ High traffic, defined by a request rate higher than our load limit, determined via 
load testing. 
¡ High CPU, memory, or I/O utilization. 
¡ High storage utilization in our SQL service (if we manage our own SQL service, 
rather than use a shared service). 
4xx responses should trigger high-urgency alerts, while other problems can trigger 
low-urgency alerts. 
10.11	Other possible types of audits
Besides the audits/tests discussed so far, we may also discuss other types of tests such as 
the following.
10.11.1	Cross data center consistency audits
It is common for the same data to be stored in multiple data centers. To ensure data 
consistency across data centers, our database batch auditing service may provide the 
ability to run sampling tests to compare data across data centers.


	
243
References 
10.11.2	Compare upstream and downstream data
Referring to section 7.7 on data migrations, a user may need to copy data from one 
table to another. They can create an audit job to compare the latest partitions in the 
upstream and downstream tables to ensure data consistency.
10.12	Other possible discussion topics 
Here are some other possible discussion topics during the interview:
¡ Design a scalable batch ETL service or a scalable alerting service. We will need a 
distributed event streaming platform like Kafka for both services. 
¡ Code a function that generates the Airflow Python job from validation.py 
.template and other appropriate templates, with a separate Airflow task for 
each query, though this is a coding question, not a system design question.
¡ An audit job alert database table owners of data integrity problems in their tables, 
but we did not discuss how they can troubleshoot and discover the causes of these 
problems. How can table owners troubleshoot data integrity problems? Can we 
enhance our audit service, or what are other possibilities to help them? 
¡ Certain audit jobs may fail on one run and then pass when the owner runs the 
same query while doing troubleshooting. How may owners troubleshoot such 
jobs, and what logging or features may our service provide to assist them?
¡ How may we find and deduplicate identical or similar audit jobs?
¡ Our database batch auditing service sends large numbers of alerts. A problem 
with a table may affect multiple audit jobs and trigger multiple alerts to the same 
user. How may we deduplicate alerts? Which parts of this alert deduplication logic 
will be implemented in our database batch auditing service, and which parts will 
be implemented in the shared alerting service?
¡ Our service can also allow tests to be triggered by certain events and not just 
run on a schedule. For example, we can track the number of rows changed after 
each query, sum these numbers, and run a test after a specified number of rows 
is changed. We can discuss possible events that can trigger tests and their system 
designs.
10.13	References 
This chapter was inspired by Uber’s Trust data quality platform, though many of the 
implementation details discussed in this chapter may be considerably different from 
Trust. A discussion of data quality at Uber can be found at https://eng.uber.com/ 
operational-excellence-data-quality/, though this article did not mention Trust by 
name. Refer to the article for an overview of Uber’s data quality platform, including 
a discussion of its constituent services and their interactions between each other and 
users. 


244
Chapter 10  Design a database batch auditing service 
Summary
¡ During a system design interview, we can discuss auditing as a common approach 
to maintaining data integrity. This chapter discussed a possible system design for 
batch auditing. 
¡ We can periodically run database queries to detect data irregularities, which may 
be due to various problems like unexpected user activity, silent errors, or malicious activity.
¡ We defined a common solution for detecting data irregularities that encompasses many use cases for these periodic database queries, and we designed a 
scalable, available, and accurate system.
¡ We can use task scheduling platforms like Airflow to schedule auditing jobs, 
rather than defining our own cron jobs, which are less scalable and more error 
prone. 
¡ We should define the appropriate monitoring and alerting to keep users 
informed of successful or failed audit jobs. The periodic database auditing service also uses the alerting service, discussed in chapter 9, and OpenID Connect, 
discussed in appendix B.
¡ We can provide a query service for users to make ad hoc queries. 


245
11
Autocomplete/typeahead
This chapter covers
¡ Comparing autocomplete with search
¡ Separating data collection and processing from 	
	 querying
¡ Processing a continuous data stream
¡ Dividing a large aggregation pipeline into  
	 stages to reduce storage costs
¡ Employing the byproducts of data processing 	
	 pipelines for other purposes
We wish to design an autocomplete system. Autocomplete is a useful question to 
test a candidate’s ability to design a distributed system that continuously ingests and 
processes large amounts of data into a small (few MBs) data structure that users can 
query for a specific purpose. An autocomplete system obtains its data from strings 
submitted by up to billions of users and then processes this data into a weighted trie. 
When a user types in a string, the weighted trie provides them with autocomplete 
suggestions. We can also add personalization and machine learning elements to our 
autocomplete system. 


246
Chapter 11  Autocomplete/typeahead
11.1	 Possible uses of autocomplete 
We first discuss and clarify the intended use cases of this system to ensure we determine 
the appropriate requirements. Possible uses of autocomplete include: 
¡ Complements a search service. While a user enters a search query, the autocomplete service returns a list of autocomplete suggestions with each keystroke. If the 
user selects a suggestion, the search service accepts it and returns a list of results. 
–	 General search, such as Google, Bing, Baidu, or Yandex. 
–	 Search within a specific document collection. Examples include Wikipedia 
and video-sharing apps. 
¡ A word processor may provide autocomplete suggestions. When a user begins 
typing a word, they may be provided autocomplete suggestions for common 
words that begin with the user’s currently entered prefix. Using a technique 
called fuzzy matching, the autocomplete feature can also be a spellcheck feature 
that suggests words with prefixes that closely match but are not identical to the 
user’s currently entered prefix.
¡ An integrated development environment (IDE) (for coding) may have an 
autocomplete feature. The autocomplete feature can record variable names or 
constant values within the project directory and provide them as autocomplete 
suggestions whenever the user declares a variable or constant. Exact matches are 
required (no fuzzy matching). 
An autocomplete service for each of these use cases will have different data sources 
and architecture. A potential pitfall in this interview (or other system design interviews 
in general) is to jump to conclusions and immediately assume that this autocomplete 
service is for a search service, which is a mistake you may make because you are most 
familiar with the autocomplete used in a search engine like Google or Bing. 
Even if the interviewer gives you a specific question like “Design a system that provides autocomplete for a general search app like Google,” you can spend half a minute 
discussing other possible uses of autocomplete. Demonstrate that you can think beyond 
the question and do not make hasty assumptions or jump to conclusions. 
11.2	 Search vs. autocomplete 
We must distinguish between autocomplete and search and not get their requirements 
mixed up. This way, we will design an autocomplete service rather than a search service. How is autocomplete similar and different from search? Similarities include the 
following: 
¡ Both services attempt to discern a user’s intentions based on their search string 
and return a list of results sorted by most likely match to their intention. 
¡ To prevent inappropriate content from being returned to users, both services 
may need to preprocess the possible results. 


	
247
Search vs. autocomplete 
¡ Both services may log user inputs and use them to improve their suggestions/
results. For example, both services may log the results that are returned and 
which the user clicks on. If the user clicks on the first result, it indicates that this 
result is more relevant to that user.
Autocomplete is conceptually simpler than search. Some high-level differences are 
described in table 11.1. Unless the interviewer is interested, do not spend more than 
a minute dwelling on these differences in the interview. The point is to demonstrate 
critical thinking and your ability to see the big picture. 
Table 11.1    Some differences between search and autocomplete 
Search
Autocomplete
Results are usually a list of webpage URLs 
or documents. These documents are preprocessed to generate an index. During a search 
query, the search string is matched to the 
index to retrieve relevant documents.
Results are lists of strings, generated based 
on user search strings.
P99 latency of a few seconds may be acceptable. Higher latency of up to a minute may be 
acceptable in certain circumstances.
Low latency of ~100 ms P99 desired for good 
user experience. Users expect suggestions 
almost immediately after entering each 
character.
Various result data types are possible, including strings, complex objects, files, or media.
Result data type is just string.
Each result is given a relevance score.
Does not always have a relevance score. For 
example, an IDE’s autocomplete result list 
may be lexicographically ordered.
Much effort is expended to compute relevance scores as accurately as possible, 
where accuracy is perceived by the user.
Accuracy requirements (e.g., user clicks on 
one of the first few suggestions rather than 
a later one) may not be as strict as search. 
This is highly dependent on business requirements, and high accuracy may be required in 
certain use cases.
A search result may return any of the input 
documents. This means every document 
must be processed, indexed, and possible to 
return in a search result. For lower complexity, 
we may sample the contents of a document, 
but we must process every single document.
If high accuracy is not required, techniques 
like sampling and approximation algorithms 
can be used for lower complexity.
May return hundreds of results.
Typically returns 5–10 results.
A user can click on multiple results, by 
clicking the “back” button and then clicking 
another result. This is a feedback mechanism 
we can draw many possible inferences from.
Different feedback mechanism. If none of the 
autocomplete suggestions match, the user 
finishes typing their search string and then 
submits it.


248
Chapter 11  Autocomplete/typeahead
11.3	 Functional requirements 
We can have the following Q&A with our interviewer to discuss the functional requirements of our autocomplete system.
11.3.1	 Scope of our autocomplete service
We can first clarify some details of our scope, such as which use cases and languages 
should be supported:
¡ Is this autocomplete meant for a general search service or for other use cases like 
a word processor or IDE? 
–	 It is for suggesting search strings in a general search service. 
¡ Is this only for English? 
–	 Yes. 
¡ How many words must it support?
–	 The Webster English dictionary has ~470K words (https://www.merriam 
-webster.com/help/faq-how-many-english-words), while the Oxford English 
dictionary has >171K words (https://www.lexico.com/explore/how-many 
-words-are-there-in-the-english-language). We don’t know how many of these 
words are at least 6 characters in length, so let’s not make any assumptions. 
We may wish to support popular words that are not in the dictionary, so let’s 
support a set of up to 100K words. With an average English word length of 4.7 
(rounded to 5) letters and 1 byte/letter, our storage requirement is only 5 MB. 
Allowing manual (but not programmatic) addition of words and phrases negligibly increase our storage requirement. 
NOTE    The IBM 350 RAMAC introduced in 1956 was the first computer with 
a 5 MB hard drive (https://www.ibm.com/ibm/history/exhibits/650/650_pr2 
.html). It weighed over a ton and occupied a footprint of 9 m (30 ft) by 15 m 
(50 ft). Programming was done in machine language and wire jumpers on a 
plugboard. There were no system design interviews back then. 
11.3.2	 Some UX details
We can clarify some UX (user experience) details of the autocomplete suggestions, 
such as whether the autocomplete suggestions should be on sentences or individual words or how many characters a user should enter before seeing autocomplete 
suggestions:


	
249
Functional requirements 
¡ Is the autocomplete on words or sentences? 
–	 We can initially consider just words and then extend to phrases or sentences if 
we have time. 
¡ Is there a minimum number of characters that should be entered before suggestions are displayed?
–	 3 characters sound reasonable. 
¡ Is there a minimum length for suggestions? It’s not useful for a user to get suggestions for 4 or 5-letter words after typing in 3 characters, since those are just 1 or 2 
more letters. 
–	 Let’s consider words with at least 6 letters. 
¡ Should we consider numbers or special characters, or just letters? 
–	 Just letters. Ignore numbers and special characters. 
¡ How many autocomplete suggestions should be shown at a time, and in what 
order? 
–	 Let’s display 10 suggestions at a time, ordered by most to least frequent. First, 
we can provide a suggestions API GET endpoint that accepts a string and 
returns a list of 10 dictionary words ordered by decreasing priority. Then we 
can extend it to also accept user ID to return personalized suggestions.
11.3.3	 Considering search history
We need to consider if the autocomplete suggestions should be based only on the 
user’s current input or on their search history and other data sources.
¡ Limiting the suggestions to a set of words implies that we need to process users’ 
submitted search strings. If the output of this processing is an index from which 
autocomplete suggestions are obtained, does previously processed data need to 
be reprocessed to include these manually added and removed words/phrases? 
–	 Such questions are indicative of engineering experience. We discuss with the 
interviewer that there will be a substantial amount of past data to reprocess. 
But why will a new word or phrase be manually added? It will be based on analytics of past user search strings. We may consider an ETL pipeline that creates 
tables easy to query for analytics and insights. 
¡ What is the data source for suggestions? Is it just the previously submitted queries, or are there other data sources, such as user demographics? 
–	 It’s a good thought to consider other data sources. Let’s use only the submitted queries. Maybe an extensible design that may admit other data sources in 
the future will be a good idea. 
¡ Should it display suggestions based on all user data or the current user data (i.e., 
personalized autocomplete)? 
–	 Let’s start with all user data and then consider personalization. 


250
Chapter 11  Autocomplete/typeahead
¡ What period should be used for suggestions? 
–	 Let’s first consider all time and then maybe consider removing data older than 
a year. We can use a cutoff date, such as not considering data before January 1 
of last year.
11.3.4	 Content moderation and fairness
We can also consider other possible features like content moderation and fairness: 
¡ How about a mechanism to allow users to report inappropriate suggestions? 
–	 That will be useful, but we can ignore it for now. 
¡ Do we need to consider if a small subset of users submitted most of the searches? 
Should our autocomplete service try to serve the majority of users by processing 
the same number of searches per user? 
–	 No, let’s consider only the search strings themselves. Do not consider which 
users made them.
11.4	 Non-functional requirements 
After discussing the functional requirements, we can have a similar Q&A to discuss the 
non-functional requirements. This may include a discussion of possible tradeoffs such 
as availability versus performance: 
¡ It should be scalable so it can be used by a global user base. 
¡ High availability is not needed. This is not a critical feature, so fault-tolerance can 
be traded off. 
¡ High performance and throughput are necessary. Users must see autocomplete 
suggestions within half a second. 
¡ Consistency is not required. We can allow our suggestions to be hours out of date; 
new user searches do not need to immediately update the suggestions. 
¡ For privacy and security, no authorization or authentication is needed to use 
autocomplete, but user data should be kept private. 
¡ Regarding accuracy, we can reason the following: 
–	 We may wish to return suggestions based on search frequency, so we can count 
the frequency of search strings. We can decide that such a count does not 
need to be accurate, and an approximation is sufficient in our first design 
pass. We can consider better accuracy if we have time, including defining accuracy metrics. 
–	 We will not consider misspellings or mixed-language queries. Spellcheck will 
be useful, but let’s ignore it in this question.


	
251
Planning the high-level architecture 
–	 Regarding potentially inappropriate words and phrases, we can limit the suggestions to a set of words, which will prevent inappropriate words, but not 
phrases. Let’s refer to them as “dictionary words,” even though they may 
include words that we added and not from a dictionary. If you like, we can 
design a mechanism for admins to manually add and remove words and 
phrases from this set.
–	 On how up to date the suggestions should be, we can have a loose requirement of 1 day.
11.5	 Planning the high-level architecture 
We can begin the design thought process of a system design interview by sketching a 
very high-level initial architecture diagram such as figure 11.1. Users submit search 
queries, which the ingestion system processes and then stores in the database. Users 
receive autocomplete suggestions from our database when they are typing their search 
strings. There may be other intermediate steps before a user receives their autocomplete suggestions, which we label as the query system. This diagram can guide our reasoning process. 
User
Ingestion System
Query system
(includes
autocomplete)
Database
Figure 11.1    A very high-level initial architecture of our autocomplete service. Users submit their strings 
to the ingestion system, which are saved to the database. Users send requests to the query system for 
autocomplete suggestions. We haven’t discussed where the data processing takes place. 
Next, we reason that we can break up the system into the following components: 
1	 Data ingestion 
2	 Data processing 
3	 Query the processed data to obtain autocomplete suggestions. 
Data processing is generally more resource-intensive than ingestion. Ingestion only 
needs to accept and log requests and must handle traffic spikes. So, to scale up, we split 
the data processing system from the ingestion system. This is an example of the Command Query Responsibility Segregation (CQRS) design pattern discussed in chapter 1. 
Another factor to consider is that the ingestion system can actually be the search service’s logging service, that can also be the organization’s shared logging service. 


252
Chapter 11  Autocomplete/typeahead
11.6	 Weighted trie approach and initial high-level architecture
Figure 11.2 shows our initial high-level architecture of our Autocomplete System. Our 
Autocomplete System is not a single service but a system where users only query one 
service (the autocomplete service) and do not directly interact with the rest of the 
system. The rest of the system serves to collect users’ search strings and periodically 
generate and deliver a weighted trie to our autocomplete service. 
The shared logging service is the raw data source from which our autocomplete service derives the autocomplete suggestions that it provides to its users. Search service 
users send their queries to the search service, which logs them to the logging service. 
Other services also log to this shared logging service. The autocomplete service may 
query the logging service for just the search service logs or other services’ logs, too, if we 
find those useful to improve our autocomplete suggestions. 
Word 
Service
Search 
Service
Logging 
Service
Word 
Processing 
ETL job
Weighted 
Trie 
Generator
Autocomplete 
Service
Other 
services
Word count 
table
Users of Search 
Service
Figure 11.2    Initial high-level architecture of our Autocomplete System. Users of our search service 
submit their search strings to the search service, and these strings are logged to a shared logging 
service. The Word Processing ETL job may be a batch or streaming job that reads and processes the 
logged search strings. The weighted trie generator reads the word counts and generates the weighted 
trie and then sends it to the autocomplete service, from which users obtain autocomplete suggestions.
The shared logging service should have an API for pulling log messages based on topic 
and timestamp. We can tell the interviewer that its implementation details, such as 
which database it uses (MySQL, HDFS, Kafka, Logstash, etc.), are irrelevant to our 
current discussion, since we are designing the autocomplete service, not our organization’s shared logging service. We add that we are prepared to discuss the implementation details of a shared logging service if necessary. 
Users retrieve autocomplete suggestions from the autocomplete service’s backend. 
Autocomplete suggestions are generated using a weighted trie, illustrated in figure 
11.3. When a user enters a string, the string is matched with the weighted trie. The 
result list is generated from the children of the matched string, sorted by decreasing 
weight. For example, a search string “ba” will return the result [“bay”, “bat”]. “bay” has a 
weight of 4 while “bat” has a weight of 2, so “bay” is before “bat.” 


	
253
Detailed implementation 
Figure 11.3    A weighted trie of the words “all”, “apes,” “bat,” and “bay.” (Source: https://courses 
.cs.duke.edu/cps100/spring16/autocomplete/trie.html.) 
We shall now discuss the detailed implementation of these steps. 
11.7	 Detailed implementation 
The weighted trie generator can be a daily batch ETL pipeline (or a streaming pipeline 
if real-time updates are required). The pipeline includes the word processing ETL job. 
In figure 11.2, the word processing ETL job and weighted trie generator are separate 
pipeline stages because the word processing ETL job can be useful for many other purposes and services, and having separate stages allows them to be implemented, tested, 
maintained, and scaled independently.
Our word count pipeline may have the following tasks/steps, illustrated as a DAG in 
figure 11.4: 
1	 Fetch the relevant logs from the search topic of the logging service (and maybe 
other topics) and place them in a temporary storage. 
2	 Split the search strings into words. 
3	 Filter out inappropriate words. 
4	 Count the words and write to a word count table. Depending on required accuracy, we can count every word or use an approximation algorithm like count-min 
sketch (described in section 17.7.1). 
5	 Filter for appropriate words and record popular unknown words.
6	 Generate the weighted trie from the word count table.
7	 Send the weighted trie to our backend hosts. 


254
Chapter 11  Autocomplete/typeahead
Generate  
and deliver 
weighted trie
Filter 
inappropriate 
words
Word count
Filter appropriate 
words
Record popular 
unknown words
Figure 11.4   DAG of our word count pipeline. Recording popular unknown words and filtering appropriate 
words can be done independently. 
We can consider various database technologies for our raw search log:
¡ An Elasticsearch index partitioned by day, part of a typical ELK stack, with a 
default retention period of seven days. 
¡ The logs of each day can be an HDFS file (i.e., partitioned by day). User searches 
can be produced to a Kafka topic with a retention period of a few days (rather 
than just one day, in case we need to look at older messages for any reason). At a 
certain set time each day, the first pipeline stage will consume messages until it 
reaches a message with a timestamp more recent than the set time (this means 
it consumes one additional message, but this slight imprecision is fine) or until 
the topic is empty. The consumer creates a new HDFS directory for the partition 
corresponding to that date and appends all messages to a single file within that 
directory. Each message can contain a timestamp, user ID, and the search string. 
HDFS does not offer any mechanism to configure a retention period, so for those 
choices, we will need to add a stage to our pipeline to delete old data.
¡ SQL is infeasible because it requires all the data to fit into a single node. 
Let’s assume that the logging service is an ELK service. As mentioned in section 4.3.5, 
HDFS is a common storage system for the MapReduce programming model. We use 
the MapReduce programming model to parallelize data processing over many nodes. 
We can use Hive or Spark with HDFS. If using Hive, we can use Hive on Spark (https://
spark.apache.org/docs/latest/sql-data-sources-hive-tables.html), so both our Hive or 
Spark approaches are actually using Spark. Spark can read and write from HDFS into 
memory and process data in memory, which is much faster than processing on disk. In 
subsequent sections, we briefly discuss implementations using Elasticsearch, Hive, and 
Spark. A thorough discussion of code is outside the scope of a system design interview, 
and a brief discussion suffices. 
This is a typical ETL job. In each stage, we read from the database storage of the previous stage, process the data, and write to the database storage to be used by the next 
stage. 


	
255
Detailed implementation 
11.7.1	 Each step should be an independent task
Referring again to the batch ETL DAG in figure 11.4, why is each step an independent 
stage? When we first develop an MVP, we can implement the weighted trie generation as 
a single task and simply chain all the functions. This approach is simple, but not maintainable. (Complexity and maintainability seem to be correlated, and a simple system is 
usually easier to maintain, but here we see an example where there are tradeoffs.) 
We can implement thorough unit testing on our individual functions to minimize 
bugs, implement logging to identify any remaining bugs that we encounter in production, and surround any function that may throw errors with try-catch blocks and 
log these errors. Nonetheless, we may miss certain problems, and if any error in our 
weighted trie generation crashes the process, the entire process needs to restart from 
the beginning. These ETL operations are computationally intensive and may take 
hours to complete, so such an approach has low performance. We should implement 
these steps as separate tasks and use a task scheduler system like Airflow, so each task 
only runs after the previous one successfully completes. 
11.7.2	 Fetch relevant logs from Elasticsearch to HDFS
For Hive, we can use a CREATE EXTERNAL TABLE command (https://www.elastic 
.co/guide/en/elasticsearch/hadoop/current/hive.html#_reading_data_from_ 
elasticsearch) to define a Hive table on our Elasticsearch topic. Next, we can write the 
logs to HDFS using a Hive command like INSERT OVERWRITE DIRECTORY '/path/
to/output/dir' SELECT * FROM Log WHERE created_at = date_sub(current_
date, 1);. (This command assumes we want yesterday’s logs.)
For Spark, we can use the SparkContext esRDD method (https://www.elastic 
.co/guide/en/elasticsearch/hadoop/current/spark.html#spark-read) to connect to 
our Elasticsearch topic, followed by a Spark filter query (https://spark.apache.org/ 
docs/latest/api/sql/index.html#filter) to read the data for the appropriate 
dates, and then write to HDFS using the Spark saveAsTextFile function (https://
spark.apache.org/docs/latest/api/scala/org/apache/spark/api/java/JavaRDD 
.html#saveAsTextFile(path:String):Unit).
During an interview, even if we don’t know that Hive or Spark has Elasticsearch integrations, we can tell our interviewer that such integrations may exist because these are 
popular mainstream data platforms. If such integrations don’t exist, or if our interviewer asks us to, we may briefly discuss how to code a script to read from one platform 
and write to another. This script should take advantage of each platform’s parallel processing capabilities. We may also discuss partitioning strategies. In this step, the input/
logs may be partitioned by service, while the output is partitioned by date. During this 
stage, we can also trim whitespace from both ends of the search strings. 
11.7.3	 Split the search strings into words and other simple operations
Next, we split the search strings by whitespace with the split function. (We may also 
need to consider common problems like the users omitting spaces (e.g., “HelloWorld”) 
or using other separators like a period, dash, or comma. In this chapter, we assume that 


256
Chapter 11  Autocomplete/typeahead
these problems are infrequent, and we can ignore them. We may wish to do analytics 
on the search logs to find out how common these problems actually are.) We will refer 
to these split strings as “search words.” Refer to https://cwiki.apache.org/confluence/ 
display/Hive/LanguageManual+UDF#LanguageManualUDF-StringFunctions for Hive’s 
split function and https://spark.apache.org/docs/latest/api/sql/index.html#split for 
Spark’s split function. We read from the HDFS file in the previous step and then split 
the strings.
At this stage, we can also perform various simple operations that are unlikely to 
change over the lifetime of our system, such as filtering for strings that are at least six 
characters long and contain only letters (i.e., no numbers or special characters ), and 
lowercasing all strings so we will not have to consider case in further processing. We 
then write these strings as another HDFS file. 
11.7.4	 Filter out inappropriate words
We will consider these two parts in filtering for appropriate words or filtering out inappropriate words:
1	 Managing our lists of appropriate and inappropriate words. 
2	 Filtering our list of search words against our lists of appropriate and inappropriate words. 
Words service
Our words service has API endpoints to return sorted lists of appropriate or inappropriate words. These lists will be at most a few MB and are sorted to allow binary search. 
Their small size means that any host that fetches the lists can cache them in memory in 
case the words service is unavailable. Nonetheless, we can still use our typical horizontally scaled architecture for our words service, consisting of stateless UI and backend 
services, and a replicated SQL service as discussed in section 3.3.2. Figure 11.5 shows 
our high-level architecture of our words service, which is a simple application to read 
and write words to a SQL database. The SQL tables for appropriate and inappropriate 
words may contain a string column for words, and other columns that provide information such as the timestamp when the word was added to the table, the user who 
added this word, and an optional string column for notes such as why the word was 
appropriate or inappropriate. Our words service provides a UI for admin users to view 
the lists of appropriate and inappropriate words and manually add or remove words, 
all of which are API endpoints. Our backend may also provide endpoints to filter words 
by category or to search for words. 
UI
SQL
Backend
Figure 11.5    High-level architecture of our words service


	
257
Detailed implementation 
Filtering out inappropriate words
Our word count ETL pipeline requests our words service for the inappropriate words 
and then writes this list to an HDFS file. We might already have an HDFS file from a 
previous request. Our words service admins might have deleted certain words since 
then, so the new list might not have the words that are present in our old HDFS file. 
HDFS is append-only, so we cannot delete individual words from the HDFS file but 
instead must delete the old file and write a new file. 
With our HDFS file of inappropriate words, we can use the LOAD DATA command to 
register a Hive table on this file and then filter out inappropriate words with a simple 
query such as the following and then write the output to another HDFS file. 
We can determine which search strings are inappropriate words using a distributed 
analytics engine such as Spark. We can code in PySpark or Scala or use a Spark SQL 
query to JOIN the users’ words with the appropriate words. 
In an interview, we should spend less than 30 seconds on an SQL query to scribble 
down the important logic as follows. We can briefly explain that we want to manage our 
50 minutes well, so we do not wish to spend precious minutes to write a perfect SQL 
query. The interviewer will likely agree that this is outside the scope of a system design 
interview, that we are not there to display our SQL skills, and allow us to move on. A possible exception is if we are interviewing for a data engineer position: 
¡ Filters, such as WHERE clauses 
¡ JOIN conditions 
¡ Aggregations, such as AVG, COUNT, DISTINCT, MAX, MIN, PERCENTILE, 
RANK, ROW_NUMBER, etc. 
SELECT word FROM words WHERE word NOT IN (SELECT word from inappropriate_
words);
Since our inappropriate words table is small, we can use a map join (mappers in a 
MapReduce job perform the join. Refer to https://cwiki.apache.org/confluence/ 
display/hive/languagemanual+joins) for faster performance:
SELECT /*+ MAPJOIN(i) */ w.word FROM words w LEFT OUTER JOIN inappropriate_
words i ON i.word = w.word WHERE i.word IS NULL;
Broadcast hash join in Spark is analogous to map join in Hive. A broadcast hash join 
occurs between a small variable or table that can fit in memory of each node (in Spark, 
this is set in the spark.sql.autoBroadcastJoinThreshold property, which is 10 MB 
by default), and a larger table that needs to be divided among the nodes. A broadcast 
hash join occurs as follows:
1	 Create a hash table on the smaller table, where the key is the value to be joined 
on and the value is the entire row. For example, in our current situation, we are 
joining on a word string, so a hash table of the inappropriate_words table that 
has the columns (“word,” “created_at,” “created_by”) may contain entries like 


258
Chapter 11  Autocomplete/typeahead
{(“apple”, (“apple”, 1660245908, “brad”)), (“banana”, (“banana”, 1550245908, 
“grace”)), (“orange”, (“orange”, 1620245107, “angelina”)) . . . }.
2	 Broadcast/copy this hash table to all nodes performing the join operation. 
3	 Each node JOINs the smaller table to the node’s portion of the larger table.
If both tables cannot fit in memory, a shuffled sort merge join is done, where both 
datasets are shuffled, the records are sorted by key, and a merge join is done where 
both sides are iterated and joined based on the join key. This approach assumes that 
we don’t need to keep statistics on inappropriate words. Here are some resources for 
further reading on Spark joins: 
¡ https://spark.apache.org/docs/3.3.0/sql-performance-tuning.html#join 
-strategy-hints-for-sql-queries or https://spark.apache.org/docs/3.3.0/rdd 
-programming-guide.html#broadcast-variables. The official Spark documentation for the various Spark JOIN strategies to improve JOIN performance. It states 
the various JOIN strategies available but does not discuss their detailed mechanisms. Refer to the resources below for thorough discussions. 
¡ https://spark.apache.org/docs/3.3.0/sql-performance-tuning.html#join 
-strategy-hints-for-sql-queries
¡ Damiji, J. et al. A Family of Spark Joins. In Learning Spark, 2nd Edition. O’Reilly 
Media, 2020.
¡ Chambers, B. and Zaharia, M. Joins. In Spark: The Definitive Guide: Big Data Processing Made Simple. O’Reilly Media, 2018.
¡ https://docs.qubole.com/en/latest/user-guide/engines/hive/hive-mapjoin 
-options.html
¡ https://towardsdatascience.com/strategies-of-spark-join-c0e7b4572bcf 
11.7.5	 Fuzzy matching and spelling correction
A final processing step before we count the words is to correct misspellings in users’ 
search words. We can code a function that accepts a string, uses a library with a fuzzy 
matching algorithm to correct possible misspelling, and returns either the original 
string or fuzzy-matched string. (Fuzzy matching, also called approximate string matching, is the technique of finding strings that match a pattern approximately. An overview of fuzzy matching algorithms is outside the scope of this book.) We can then use 
Spark to run this function in parallel over our list of words divided into evenly sized 
sublists and then write the output to HDFS. 
This spelling correction step is its own independent task/stage because we have multiple fuzzy matching algorithms and libraries or services to choose from, so we may 
choose a particular algorithm to optimize for our requirements. Keeping this stage 
separate allows us to easily switch between a library or service for fuzzy matching, as 
changes to this pipeline stage will not affect the other stages. If we use a library, we may 
need to update it to keep up with changing trends and popular new words. 


	
259
Detailed implementation 
11.7.6	 Count the words
We are now ready to count the words. This can be a straightforward MapReduce operation, or we can use an algorithm like count-min sketch (refer to section 17.7.1). 
The Scala code below implements the MapReduce approach. This code was slightly 
modified from https://spark.apache.org/examples.html. We map the words in the 
input HDFS file to (String, Int) pairs called counts, sort by descending order of 
counts and then save it as another HDFS file: 
val textFile = sc.textFile("hdfs://...")
val counts = textFile.map(word => (word, 1)).reduceByKey(_ + _).map(item => 
item.swap).sortByKey(false).map(item => item.swap)
counts.saveAsTextFile("hdfs://...")
11.7.7	 Filter for appropriate words
The word-counting step should significantly reduce the number of words to be filtered. 
Filtering for appropriate words is very similar to filtering for inappropriate words in 
section 11.7.4. 
We can use a simple Hive command such as SELECT word FROM counted_words 
WHERE word IN (SELECT word FROM appropriate_words); to filter for appropriate words, or a Map Join or broadcast hash join such as SELECT /*+ MAPJOIN(a) 
*/ c.word FROM counted_words c JOIN appropriate_words a on c.word = 
a.word;.
11.7.8	 Managing new popular unknown words
After counting the words in the previous step, we may find new popular words in the 
top 100, which were previously unknown to us. In this stage, we write these words to 
the Words Service, which can write them to a SQL unknown_words table. Similar to 
section 11.7.4, our words service provides UI features and backend endpoints to allow 
operations staff to manually choose to add these words to the lists of appropriate or 
inappropriate words. 
As illustrated in our word count batch ETL job DAG in figure 11.4, this step can be 
done independently and in parallel with the filtering for appropriate words. 
11.7.9	 Generate and deliver the weighted trie
We now have the list of top appropriate words to construct our weighted trie. This list is 
only a few MB, so the weighted trie can be generated on a single host. The algorithm to 
construct a weighted trie is outside the scope of a system design interview. It is a possible coding interview question. A partial Scala class definition is as follows, but we code 
in the language of our backend: 
class TrieNode(var children: Array[TrieNode], var weight: Int) { 
  // Functions for  
  // - create and return a Trie node. 
  // - insert a node into the Trie. 
  // - getting the child with the highest weight. 
} 


260
Chapter 11  Autocomplete/typeahead
We serialize the weighted trie to JSON. The trie is a few MB in size, which may be too 
large to be downloaded to the client each time the search bar is displayed to the user 
but is small enough to replicate to all hosts. We can write the trie to a shared object 
store such as AWS S3 or a document database such as MongoDB or Amazon DocumentDB. Our backend hosts can be configured to query the object store daily and 
fetch the updated JSON string. The hosts can query at random times, or they can be 
configured to query at the same time with some jitter to prevent a large number of 
simultaneous requests from overwhelming the object store.  
If a shared object is large (e.g., gigabytes), we should consider placing it in a CDN. 
Another advantage of this small trie is that a user can download the entire trie when 
they load our search app, so the trie lookup is client-side rather than server-side. This 
greatly reduces the number of requests to our backend, which has advantages such as 
the following:
¡ If the network is unreliable or slow, a user may sporadically not get suggestions as 
they enter their search string, which is a poor user experience. 
¡ When the trie is updated, a user that is in the middle of typing in a search string 
may notice the change. For example, if the strings in the old trie were related in 
some way, the new trie may not possess these relationships, and the user notices 
this sudden change. Or if the user does backspace on a few characters, they may 
notice the suggestions are different from before. 
If we have a geographically distributed user base, network latency becomes unacceptable, given our requirement for high performance. We can provision hosts in multiple data centers, though this may be costly and introduce replication lag. A CDN is a 
cost-effective choice. 
Our autocomplete service should provide a PUT endpoint to update its weighted 
trie, which this stage will use to deliver the generated weighted trie to our autocomplete 
service. 
11.8	 Sampling approach
If our autocomplete does not require high accuracy, we should do sampling, so most 
of the operations to generate the weighted trie can be done within a single host, which 
has many advantages including the following: 
¡ The trie will be generated much faster.
¡ As the trie can be generated much faster, it will be easier test code changes before 
deploying them to the production environment. The overall system will be easier 
to develop, debug, and maintain. 
¡ Consumes much less hardware resources, including processing, storage, and 
network. 


	
261
Handling storage requirements
Sampling can be done at most steps: 
1	 Sampling the search strings from the logging service. This approach has the lowest accuracy but also the lowest complexity. We may need a large sample to obtain 
a statistically significant number of words, which are at least six characters long. 
2	 Sampling words after splitting the search strings to individual words and filtering 
for words that are at least six characters long. This approach avoids the computational expense of filtering for appropriate words, and we may not need as large a 
sample as the previous approach. 
3	 Sampling words after filtering for appropriate words. This approach has the 
highest accuracy but also the highest complexity. 
11.9	 Handling storage requirements
Based on our high-level architecture, we can create tables with the following columns, 
using each table to populate the next: 
1	 Raw search requests with timestamp, user ID, and search string. This table can be 
used for many other purposes besides autocomplete (e.g., analytics to discover 
user interests and trending search terms). 
2	 After splitting the raw search strings, the individual words can be appended to a 
table that contains columns for date and word.
3	 Determine which search strings are dictionary words and generate a table that 
contains date (copied from the previous table), user ID, and dictionary word. 
4	 Aggregate the dictionary words into a table of word counts. 
5	 Create a weighted trie to provide autocomplete suggestions. 
Let’s estimate the amount of storage required. We assume one billion users; each user 
submits 10 searches daily with an average of 20 characters per search. Each day, there 
may be approximately 1B * 10 * 20 = 200 GB of search strings. We may delete old data 
once a month, so at any time we have up to 12 months of data, so the search log will 
need 200 GB * 365 = 73 TB just for the search strings column. If we wish to reduce storage costs, we can consider various ways. 
One way is to trade off accuracy, by using approximation and sampling techniques. 
For example, we may sample and store only ~10% of user searches and generate the trie 
only on this sample. 
Another way is illustrated in figure 11.6. Figure 11.6 illustrates a batch ETL job that 
aggregates and roll up data at various periods to reduce the amount of data stored. At 
each stage, we can overwrite the input data with the rolled-up data. At any time, we will 
have up to one day of raw data, four weeks of data rolled up by week, and 11 months of 
data rolled up by month. We can further reduce storage requirements by keeping only 
the top 10% or 20% most frequent strings from each rollup job. 


262
Chapter 11  Autocomplete/typeahead
Rolled-up
hourly
(batch_table)
Aggregated  
events
(HDFS)
Rollup
by 
hour
Rolled-up
daily
(batch_table)
Rollup
by 
day
Rolled-up
weekly
(batch_table)
Rollup
by 
week
Rolled-up
monthly
(batch_table)
Rollup
by 
month
Figure 11.6    Flow diagram of our batch pipeline. We have a rollup job that progressively rolls up by 
increasing time intervals to reduce the number of rows processed in each stage. 
This approach also improves scalability. Without the rollup job, a word count batch 
ETL job will need to process 73 TB of data, which will take many hours and be monetarily expensive. The rollup job reduces the amount of data processed for the final 
word count used by the weighted trie generator.
We can set a short retention period on logging service, such as 14–30 days, so its storage requirement will be just 2.8–6 TB. Our daily weighted trie generator batch ETL job 
can be done on the weekly or monthly rolled up data. Figure 11.7 illustrates our new 
high-level architecture with the rollup jobs. 
Logging 
Service
Word count
table
Weighted 
Trie
Generator
Search
Service
Word 
Processing
ETL job
Autocomplete
Service
Other 
services
Users of 
Search
Service
Appropriate
words
Rollup Jobs
Rolled up
word counts
Word Service
Figure 11.7    High-level architecture of our Autocomplete System with the rollup jobs. By aggregating/
rolling up word counts over progressively larger intervals, we can reduce overall storage requirements, 
and the cluster size of the word processing ETL job. 


	
263
Handling phrases instead of single words
11.10	Handling phrases instead of single words
In this section, we discuss a couple of considerations for extending our system to handle phrases instead of single words. The trie will become bigger, but we can still limit it 
to a few MB by keeping only the most popular phrases. 
11.10.1	Maximum length of autocomplete suggestions
We can keep to our previous decision that autocomplete suggestions should have a 
minimum length of five characters. But what should be the maximum length of autocomplete suggestions? A longer maximum length will be most useful to users but comes 
with cost and performance tradeoffs. Our system will need more hardware resources 
or take longer to log and process longer strings. The trie may also become too big. 
We must decide on the maximum length. This may vary by language and culture. 
Certain languages like Arabic are more verbose than English. We only consider English 
in our system, but we should be ready to extend to other languages if this becomes a 
functional requirement.
One possible solution is to implement a batch ETL pipeline to find the 90th percentile length of our users’ search strings and use this as the maximum length. To calculate a median or percentile, we sort the list and then pick the value in the appropriate 
position. Calculating median or percentile in a distributed system is outside the scope 
of this book. We may instead simply sample the search strings and compute the 90th 
percentile. 
We may also decide that doing analytics for this decision is overengineering, and we 
can instead apply simple heuristics. Start with 30 characters and change this number 
according to user feedback, performance, and cost considerations.
11.10.2	Preventing inappropriate suggestions
We will still need to filter out inappropriate words. We may decide the following:
¡ If a phrase contains a single inappropriate word, we filter out the entire phrase. 
¡ No longer filter for appropriate words but give autocomplete suggestions for any 
word or phrase.
¡ Do not correct misspelled words in phrases. Assume that misspellings are sufficiently uncommon that they will not appear in autocomplete suggestions. We 
also assume that popular phrases will mostly be spelled correctly, so they will 
appear in autocomplete suggestions.
The difficult challenge is the need to filter out inappropriate phrases, not just inappropriate words. This is a complex problem to which even Google has not found a complete solution (https://algorithmwatch.org/en/auto-completion-disinformation/), 
due to the sheer vastness of the problem space. Possible inappropriate autocomplete 
suggestions include:


264
Chapter 11  Autocomplete/typeahead
¡ Discrimination or negative stereotypes on religion, gender, and other groups.
¡ Misinformation, including political misinformation such as conspiracy theories 
on climate change or vaccination or misinformation driven by business agendas. 
¡ Libel against prominent individuals, or defendants in legal proceedings where 
no verdict has been reached. 
Current solutions use a combination of heuristics and machine learning. 
11.11	Logging, monitoring, and alerting 
Besides the usual actions in chapter 9, we should log searches that don’t return any 
autocomplete results, which is indicative of bugs in our trie generator. 
11.12	Other considerations and further discussion
Here are other possible requirements and discussion points that may come up as the 
interview progresses: 
¡ There are many common words longer than three letters, such as “then,” “continue,” “hold,” “make,” “know,” and “take.” Some of these words may consistently 
be in the list of most popular words. It may be a waste of computational resources 
to keep counting popular words. Can our Autocomplete System keep a list of 
such words, and use approximation techniques to decide which ones to return 
when a user enters an input?
¡ As mentioned earlier, these user logs can be used for many other purposes 
besides autocomplete. For example, this can be a service that provides trending 
search terms, with applications to recommender systems. 
¡ Design a distributed logging service. 
¡ Filtering inappropriate search terms. Filtering inappropriate content is a general 
consideration of most services. 
¡ We can consider other data inputs and processing to create personalized 
autocomplete.
¡ We can consider a Lambda architecture. A Lambda architecture contains a fast 
pipeline, so user queries can quickly propagate to the weighted trie generator, 
such as in seconds or minutes, so the autocomplete suggestions are updated 
quickly with a tradeoff in accuracy. A Lambda architecture also contains a slow 
pipeline for accurate but slower updates. 
¡ Graceful degradation for returning outdated suggestions if upstream components are down. 
¡ A rate limiter in front of our service to prevent DoS attacks.
¡ A service that is related but distinct from autocomplete is a spelling suggestion 
service, where a user receives word suggestions if they input a misspelled word. 
We can design a spelling suggestion service that uses experimentation techniques 
such as A/B testing or multi-armed bandit to measure the effect of various fuzzy 
matching functions on user churn. 


	
265
Summary
Summary
¡ An autocomplete system is an example of a system that continuously ingests and 
processes large amount of data into a small data structure that users query for a 
specific purpose. 
¡ Autocomplete has many use cases. An autocomplete service can be a shared service, used by many other services.
¡ Autocomplete has some overlap with search, but they are clearly for different 
purposes. Search is for finding documents, while autocomplete is for suggesting 
what the user intends to input. 
¡ This system involves much data preprocessing, so the preprocessing and querying should be divided into separate components and then they can be independently developed and scaled. 
¡ We can use the search service and logging service as data inputs for our autocomplete service. Our autocomplete service can process the search strings that 
these services record from users and offer autocomplete suggestions from these 
strings. 
¡ Use a weighted trie for autocomplete. Lookups are fast and storage requirements 
are low. 
¡ Break up a large aggregation job into multiple stages to reduce storage and processing costs. The tradeoff is high complexity and maintenance. 
¡ Other considerations include other uses of the processed data, sampling, filtering content, personalization, Lambda architecture, graceful degradation, and 
rate limiting.


266
12
Design Flickr
This chapter covers
¡ Selecting storage services based on  
	 non-functional requirements
¡ Minimizing access to critical services
¡ Utilizing sagas for asynchronous processes
In this chapter, we design an image sharing service like Flickr. Besides sharing files/
images, users can also append metadata to files and other users, such as access control, comments, or favorites. 
Sharing and interacting with images and video are basic functionalities in virtually 
every social application and is a common interview topic. In this chapter, we discuss 
a distributed system design for image-sharing and interaction among a billion users, 
including both manual and programmatic users. We will see that there is much more 
than simply attaching a CDN. We will discuss how to design the system for scalable 
preprocessing operations that need to be done on uploaded content before they are 
ready for download. 


	
267
Non-functional requirements 
12.1	 User stories and functional requirements 
Let’s discuss user stories with the interviewer and scribble them down: 
¡ A user can view photos shared by others. We refer to this user as a viewer.
¡ Our app should generate and display thumbnails of 50 px width. A user should 
view multiple photos in a grid and can select one at a time to view the full-resolution version. 
¡ A user can upload photos. We refer to this user as a sharer. 
¡ A sharer can set access control on their photos. A question we may ask is whether 
access control should be at the level of individual photos or if a sharer may only 
allow a viewer to view either all the former’s photos or none. We choose the latter 
option for simplicity. 
¡ A photo has predefined metadata fields, which have values provided by the 
sharer. Example fields are location or tags. 
¡ An example of dynamic metadata is the list of viewers who have read access to the 
file. This metadata is dynamic because it can be changed. 
¡ Users can comment on photos. A sharer can toggle commenting on and off. A 
user can be notified of new comments. 
¡ A user can favorite a photo. 
¡ A user can search on photo titles and descriptions. 
¡ Photos can be programmatically downloaded. In this discussion, “view a photo” 
and “download a photo” are synonymous. We do not discuss the minor detail of 
whether users can download photos onto device storage. 
¡ We briefly discuss personalization. 
These are some points that we will not discuss:
¡ A user can filter photos by photo metadata. This requirement can be satisfied by 
a simple SQL path parameter, so we will not discuss it. 
¡ Photo metadata that is recorded by the client, such as location (from hardware 
such as GPS), time (from the device’s clock), and details of the camera (from the 
operating system). 
¡ We will not discuss video. Discussions of many details of video (such as codecs) 
require specialized domain knowledge that is outside the scope of a general system design interview. 
12.2	 Non-functional requirements 
Here are some questions we may discuss on non-functional requirements: 
¡ How many users and downloads via API do we expect? 
–	 Our system must be scalable. It should serve one billion users distributed 
across the world. We expect heavy traffic. Assume 1% of our users (10 million) 


268
Chapter 12  Design Flickr
upload 10 high-resolution (10 MB) images daily. This works out to 1 PB of 
uploads daily, or 3.65 EB over 10 years. The average traffic is over 1 GB/second, but we should expect traffic spikes, so we should plan for 10 GB/second. 
¡ Do the photos have to be available immediately after upload? Does deletion need 
to be immediate? Must privacy setting changes take immediate effect?
–	 Photos can take a few minutes to be available to our entire user base. We 
can trade off certain non-functional characteristics for lower cost, such as 
consistency or latency, and likewise for comments. Eventual consistency is 
acceptable. 
–	 Privacy settings must be effective sooner. A deleted photo does not have to be 
erased from all our storage within a few minutes; a few hours is permissible. 
However, it should be inaccessible to all users within a few minutes. 
¡ High-resolution photos require high network speeds, which may be expensive. 
How may we control costs? 
–	 After some discussion, we have decided that a user should only be able to 
download one high-resolution photo at a time, but multiple low-resolution 
thumbnails can be downloaded simultaneously. When a user is uploading 
files, we can upload them one at a time. 
Other non-functional requirements are 
¡ High availability, such as five 9s availability. There should be no outages that prevent users from downloading or uploading photos. 
¡ High performance and low latency of 1-second P99 for thumbnails downloads; 
this is not needed for high-resolution photos. 
¡ High performance is not needed for uploads. 
A note regarding thumbnails is that we can use the CSS img tag with either the width 
(https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-width) 
or height attributes to display thumbnails from full-resolution images. Mobile apps 
have similar markup tags. This approach has high network costs and is not scalable. 
To display a grid of thumbnails on the client, every image needs to be downloaded 
in its full resolution. We can suggest to the interviewer to implement this in our MVP 
(minimum viable product). When we scale up our service to serve heavy traffic, we can 
consider two possible approaches to generate thumbnails.
The first approach is for the server to generate a thumbnail from the full-resolution 
image each time a client requests a thumbnail. This will be scalable if it was computationally inexpensive to generate a thumbnail. However, a full-resolution image file 
is tens of MB in size. A viewer will usually request a grid of >10 thumbnails in a single 
request. Assuming a full-resolution image is 10 MB (it can be much bigger), this means 
the server will need to process >100 MB of data in much less than one second to fulfill a 
1-second P99. Moreover, the viewer may make many such requests within a few seconds 
as they scroll through thumbnails. This may be computationally feasible if the storage 


	
269
High-level architecture 
and processing are done on the same machine, and that machine uses SSD hard disks 
and not spinning hard disks. But this approach will be prohibitively expensive. Moreover, we will not be able to do functional partitioning of processing and storage into 
separate services. The network latency of transferring many GBs between the processing and storage services every second will not allow 1-second P99. So, this approach is 
not feasible overall. 
The only scalable approach is to generate and store a thumbnail just after the file is 
uploaded and serve these thumbnails when a viewer requests them. Each thumbnail 
will only be a few KBs in size, so storage costs are low. We can also cache both thumbnails 
and full-resolution image files on the client, to be discussed in section 12.7. We discuss 
this approach in this chapter. 
12.3	 High-level architecture 
Figure 12.1 shows our initial high-level architecture. Both sharers and viewers make 
requests through a backend to upload or download image files. The backend communicates with an SQL service. 
CDN
Backend
SQL
Users
File Storage 
Service
upload image files
download image files
Figure 12.1    Our initial high-level architecture of our image-sharing service. Our users can download 
image files directly from a CDN. Uploads to the CDN can be buffered via a separate distributed file 
storage service. We can store other data such as user information or image file access permissions in 
SQL. 
The first is a CDN for image files and image metadata (each image metadata is a formatted JSON or YAML string). This is most likely a third-party service. 
Due to reasons including the following, we may also need a separate distributed file 
storage service for sharers to upload their image files, and this service handles interactions with the CDN. We can refer to this as our file storage service.
¡ Depending on our SLA contract with our CDN provider, our CDN may take up 
to a few hours to replicate images to its various data centers. During that time, it 
may be slow for our viewers to download this image, especially if there is a high 
rate of download requests because many viewers wish to download it. 
¡ The latency of uploading an image file to the CDN may be unacceptably slow 
to a sharer. Our CDN may not be able to support many sharers simultaneously 


270
Chapter 12  Design Flickr
uploading images. We can scale our file storage service as required to handle 
high upload/write traffic. 
¡ We can either delete files from the file storage service after they are uploaded to 
the CDN, or we may wish to retain them as a backup. A possible reason to choose 
the latter may be that we don’t want to completely trust the CDN’s SLA and may 
wish to use our file storage service as a backup for our CDN should the latter 
experience outages. A CDN may also have a retention period of a few weeks or 
months, after which it deletes the file and downloads it again if required from 
a designated origin/source. Other possible situations may include the sudden 
requirement to disconnect our CDN because we suddenly discover that it has 
security problems. 
12.4	 SQL schema
We use an SQL database for dynamic data that is shown on the client apps, such as 
which photos are associated to which user. We can define the following SQL table 
schema in listing 12.1. The Image table contains image metadata. We can assign each 
sharer its own CDN directory, which we track using the ImageDir table. The schema 
descriptions are included in the CREATE statement. 
Listing 12.1    SQL CREATE statements for the Image and ImageDir tables
CREATE TABLE Image (
cdn_path VARCHAR(255) PRIMARY KEY COMMENT="Image file path on the
➥ CDN.",
cdn_photo_key VARCHAR(255) NOT NULL UNIQUE COMMENT="ID assigned by the
➥ CDN.",
file_key VARCHAR(255) NOT NULL UNIQUE COMMENT="ID assigned by our File
➥ Storage Service. We may not need this column if we delete the image from
➥ our File Storage Service after it is uploaded to the CDN.",
resolution ENUM(‘thumbnail’, ‘hd’) COMMENT="Indicates the image is a
➥ thumbnail or high resolution",
owner_id VARCHAR(255) NOT NULL COMMENT="ID of the user who owns the
➥ image.",
is_public BOOLEAN NOT NULL DEFAULT 1 COMMENT="Indicates if the image is
➥ public or private.",
INDEX thumbnail (Resolution, UserId) COMMENT="Composite index on the
➥ resolution and user ID so we can quickly find thumbnail or high
➥ resolution images that belong to a particular user."
) COMMENT="Image metadata.";
CREATE TABLE ImageDir (
cdn_dir VARCHAR(255) PRIMARY KEY COMMENT="CDN directory assigned to the
➥ user.",
user_id INTEGER NOT NULL COMMENT="User ID."
) COMMENT="Record the CDN directory assigned to each sharer.";
As fetching photos by user ID and resolution is a common query, we index our tables 
by these fields. We can follow the approaches discussed in chapter 4 to scale SQL reads. 


	
271
Organizing directories and files on the CDN 
We can define the following schema to allow a sharer to grant a viewer permission 
to view the former’s photos and a viewer to favorite photos. An alternative to using two 
tables is to define an is_favorite Boolean column in the Share table, but the tradeoff 
is that it will be a sparse column that uses unnecessary storage: 
CREATE TABLE Share (
  id            INT PRIMARY KEY
  cdn_photo_key VARCHAR(255),
  user_id       VARCHAR(255)
);
CREATE TABLE Favorite (
  id INT PRIMARY KEY
  cdn_photo_key VARCHAR(255) NOT NULL UNIQUE,
  user_id VARCHAR(255) NOT NULL UNIQUE
);
12.5	 Organizing directories and files on the CDN 
Let’s discuss one way to organize CDN directories. A directory hierarchy can be user > 
album > resolution > file. We can also consider date because a user may be more interested in recent files. 
Each user has their own CDN directory. We may allow a user to create albums, where 
each album has 0 or more photos. Mapping of albums to photos is one-to-many; that 
is, each photo can only belong to one album. On our CDN, we can place photos not in 
albums in an album called “default.” So, a user directory may have one or more album 
directories. 
An album directory can store the several files of the image in various resolutions, 
each in its own directory, and a JSON image metadata file. For example, a directory 
“original” may contain an originally-uploaded file “swans.png,” and a directory “thumbnail” may contain the generated thumbnail “swans_thumbnail.png.” 
A CdnPath value template is <album_name>/<resolution>/<image_name.extension>. The user ID or name is not required because it is contained in the UserId field. 
For example, a user with username “alice” may create an album named “nature,” 
inside which they place an image called “swans.png.” The CdnPath value is “nature/
original/swans.png.” The corresponding thumbnail has CdnPath “nature/thumbnail/
swans_thumbnail.png.” The tree command on our CDN will show the following. “bob” 
is another user: 
$ tree ~ | head -n 8 
. 
├── alice 
│   └── nature 
│       ├── original 
│       │   └── swans.png 
│       └── thumbnail 
│           └── swans_thumbnail.png 
├── bob 
In the rest of this discussion, we use the terms “image” and “file” interchangeably. 


272
Chapter 12  Design Flickr
12.6	 Uploading a photo 
Should thumbnails be generated on the client or server? As stated in the preface, we 
should expect to discuss various approaches and evaluate their tradeoffs. 
12.6.1	 Generate thumbnails on the client 
Generating thumbnails on the client saves computational resources on our backend, 
and the thumbnail is small, so it contributes little to network traffic. A 100 px thumbnail is about 40 KB, a negligible addition to a high-resolution photo, which may be a 
few MB to 10s of MB in size. 
Before the upload process, the client may check if the thumbnail has already been 
uploaded to the CDN. During the upload process, the following steps occur, illustrated 
in figure 12.2:
1	 Generate the thumbnail. 
2	 Place both files into a folder and then compress it with an encoding like Gzip 
or Brotli. Compression of a few MB to 10s of MB saves significant network traffic, but our backend will expend CPU and memory resources to uncompress the 
directory. 
3	 Use a POST request to upload the compressed file to our CDN directory. The 
request body is a JSON string that describes the number and resolution of images 
being uploaded. 
4	 On the CDN, create directories as necessary, unzip the compressed file, and write 
the files to disk. Replicate it to the other data centers (refer to the next question). 
Generate 
thumbnail
Zip and 
compress
Upload to CDN
Replication
Figure 12.2    Process for a client to upload a photo to our image-sharing service
NOTE    As alluded to in the preface, in the interview, we are not expected to 
know the details of compression algorithms, cryptographically secure hashing 
algorithms, authentication algorithms, pixel-to-MB conversion, or the term 
“thumbnail.” We are expected to reason intelligently and communicate clearly. 
The interviewer expects us to be able to reason that thumbnails are smaller than 
high-resolution images, that compression will help in transferring large files over 
a network and that authentication and authorization are needed for files and 
users. If we don’t know the term “thumbnail,” we can use clear terms like “a grid 
of small preview photos” or “small grid photos” and clarify that “small” refers to a 
small number of pixels, which means small file size. 


	
273
Uploading a photo 
Disadvantages of client-side generation
However, the disadvantages of client-side processing are non-trivial. We do not have 
control of the client device or detailed knowledge of its environment, making bugs 
difficult to reproduce. Our code will also need to anticipate many more failure scenarios that can occur on clients compared to servers. For example, image processing may 
fail because the client ran out of hard disk space because the client was consuming 
too much CPU or memory on other applications, or because the network connection 
suddenly failed. 
We have no control over many of these situations that may occur on a client. We may 
overlook failure scenarios during implementation and testing, and debugging is more 
difficult because it is harder to replicate the situation that occurred on a client’s device 
than on a server that we own and have admin access to. 
Many possible factors such as the following may affect the application, making it difficult to determine what to log:
¡ Generating on the client requires implementing and maintaining the thumbnail 
generation in each client type (i.e., browser, Android, and iOS). Each uses a different language, unless we use cross-platform frameworks like Flutter and React 
Native, which come with their own tradeoffs.
¡ Hardware factors, such as a CPU that is too slow or insufficient memory, may 
cause thumbnail generation to be unacceptably slow. 
¡ The specific OS version of the operating system running on the client may have 
bugs or security problems that make it risky to process images on it or cause problems that are very difficult to anticipate or troubleshoot. For example, if the OS 
suddenly crashes while uploading images, it may upload corrupt files, and this 
will affect viewers. 
¡ Other software running on the client may consume too much CPU or memory, 
and cause thumbnail generation to fail or be unacceptably slow. Clients may also 
be running malicious software, such as viruses that interfere with our application. It is impractical for us to check if clients contain such malicious software, 
and we cannot ensure that clients are following security best practices. 
¡ Related to the previous point, we can follow security best practices on our own systems to guard against malicious activity, but have little influence over our clients 
in ensuring they do the same. For this reason, we may wish to minimize data storage and processing in our clients and store and process data only on the server. 
¡ Our clients’ network configurations may interfere with file uploads, such as 
blocked ports, hosts, or possibly VPNs. 
¡ Some of our clients may have unreliable network connectivity. We may need logic 
to handle sudden network disconnects. For example, the client should save a 
generated thumbnail to device storage before uploading it to our server. Should 
the upload fail, the client will not need to generate the thumbnail again before 
retrying the upload. 


274
Chapter 12  Design Flickr
¡ Related to the previous point, there may be insufficient device storage to save the 
thumbnail. In our client implementation, we need to remember to check that 
there is sufficient device storage before generating the thumbnail, or our sharers 
may experience a poor user experience of waiting for the thumbnail to be generated and then experience an error due to lack of storage. 
¡ Also related to the same point, client-side thumbnail generation may cause our 
app to require more permissions, such as the permission to write to local storage. 
Some users may be uncomfortable with granting our app write access to their 
devices’ storage. Even if we do not abuse this permission, external or internal 
parties may compromise our system, and hackers may then go through our system to perform malicious activities on our users’ devices. 
A practical problem is that each individual problem may affect only a small number of 
users, and we may decide that it is not worth to invest our resources to fix this problem 
that affects these few users, but cumulatively all these problems may affect a non-trivial 
fraction of our potential user base. 
A more tedious and lengthy software release lifecycle
Because client-side processing has higher probability of bugs and higher cost of remediation, we will need to spend considerable resources and time to test each software 
iteration before deployment, which will slow down development. We cannot take 
advantage of CI/CD (continuous integration/continuous deployment) like we can in 
developing services. We will need to adopt a software release lifecycle like that shown 
in figure 12.3. Each new version is manually tested by internal users and then gradually 
released to progressively larger fractions of our user base. We cannot quickly release 
and roll back small changes. Since releases are slow and tedious, each release will contain many code changes. 
Figure 12.3    An example software 
release lifecycle. A new version is 
manually tested by internal users 
during the alpha phase and then it 
is released to progressively larger 
fractions of our users in each 
subsequent phase. The software 
release lifecycles of some companies 
have more stages than illustrated 
here. By Heyinsun (https://
commons.wikimedia.org/w/index 
.php?curid=6818861), CC BY 3.0 
(https://creativecommons.org/
licenses/by/3.0/deed.en). 


	
275
Uploading a photo 
In a situation where releasing/deploying code changes (either to clients or servers) is 
slow, another possible approach to preventing bugs in a new release is to include the 
new code without removing the old code in the following manner, illustrated in figure 
12.4. This example assumes we are releasing a new function, but this approach can 
generalize to new code in general: 
1	 Add the new function. Run the new function on the same input as the old function, but continue to use the output of the old function instead of the new function. Surround the usages of the new function in try-catch statements, so an 
exception will not crash the application. In the catch statement, log the exception and send the log to our logging service, so we can troubleshoot and debug it. 
2	 Debug the function and release new versions until no more bugs are observed. 
3	 Switch the code from using the old function to the new function. Surround the 
code in try catch blocks, where the catch statement will log the exception and use 
our old function as a backup. Release this version and observe for problems. If 
problems are observed, switch the code back to using the old function (i.e., go 
back to the previous step). 
4	 When we are confident that the new function is sufficiently mature (we can never 
be sure it is bug-free), remove the old function from our code. This cleanup is for 
code readability and maintainability. 
Add new function but
use old function.
Bug detected?
Switch from old to 
new function.
Bug detected?
Remove the 
old function.
Debug and release.
Yes
No
Yes
No
Figure 12.4    
Flowchart of a 
software release 
process that 
releases new code 
in stages, only 
gradually removing 
the old code


276
Chapter 12  Design Flickr
A limitation of this approach is that it is difficult to introduce non-backward-compatible code. Another disadvantage is that the code base is bigger and less maintainable. 
Moreover, our developer team needs the discipline to follow this process all the way 
through, rather than be tempted to skip steps or disregard the last step. 
The approach also consumes more computational resources and energy on the client, which may be a significant problem for mobile devices. 
Finally, this extra code increases the client app’s size. This effect is trivial for a few 
functions, but can add up if much logic requires such safeguards. 
12.6.2	 Generate thumbnails on the backend 
We just discussed the tradeoffs of generating thumbnails on the client. Generating on 
a server requires more hardware resources, as well as engineering effort to create and 
maintain this backend service, but the service can be created with the same language 
and tools as other services. We may decide that the costs of the former outweigh the 
latter. 
This section discusses the process of generating thumbnails on the backend. There 
are three main steps:
1	 Before uploading the file, check if the file has been uploaded before. This prevents costly and unnecessary duplicate uploads. 
2	 Upload the file to the file storage service and CDN.
3	 Generate the thumbnail and upload it to the file storage service and CDN. 
When the file is uploaded to the backend, the backend will write the file to our file 
storage service and CDN and then trigger a streaming job to generate the thumbnail. 
The main purpose of our file storage service is as a buffer for uploading to CDN, so 
we can implement replication between hosts within our data center but not on other 
data centers. In the event of a significant data center outage with data loss, we can also 
use the files from the CDN for recovery operations. We can use the file storage service 
and CDN as backups for each other. 
For scalable image file uploads, some of the image file upload steps can be asynchronous, so we can use a saga approach. Refer to section 5.6 for an introduction to saga.
Choreography saga approach
Figure 12.5 illustrates the various services and Kafka topics in this choreography saga. 
The detailed steps are as follows. The step numbers are labeled on both figures: 
1	 The user first hashes the image and then makes a GET request to the backend 
check if the image has already been uploaded. This may happen because the user 
successfully uploaded the image in a previous request, but the connection failed 
while the file storage service or backend was returning success, so the user may be 
retrying the upload. 


	
277
Uploading a photo 
2	 Our backend forwards the request to the file storage service. 
3	 Our file storage service returns a response that indicates if the file had already 
been successfully uploaded. 
4	 Our backend returns this response to the user. 
5	 This step depends on whether the file has already been successfully uploaded.
a	 If this file has not been successfully uploaded before, the user uploads this file 
to our file storage service via the backend. (The user may compress the file 
before uploading it.)
b	 Alternatively, if the file has already been successfully uploaded, our backend 
can produce a thumbnail generation event to our Kafka topic. We can skip to 
step 8. 
6	 Our file storage service writes the file to the object storage service.
7	 After successfully writing the file, our file storage service produces an event to our 
CDN Kafka topic and then returns a success response to the user via the backend. 
8	 Our file storage service consumes the event from step 6, which contains the 
image hash. 
9	 Similar to step 1, our file storage service makes a request to the CDN with the 
image hash to determine whether the image had already been uploaded to the 
CDN. This could have happened if a file storage service host had uploaded the 
image file to the CDN before, but then failed before it wrote the relevant checkpoint to the CDN topic. 
10	 Our file storage service uploads the file to the CDN. This is done asynchronously 
and independently of the upload to our file storage service, so our user experience is unaffected if upload to the CDN is slow. 
11	 Our file storage service produces a thumbnail generation event that contains the 
file ID to our thumbnail generation Kafka topic and receives a success response 
from our Kafka service. 
12	 Our backend returns a success response to the user that the latter’s image file is 
successfully uploaded. It returns this response only after producing the thumbnail generation event to ensure that this event is produced, which is necessary to 
ensure that the thumbnail generation will occur. If producing the event to Kafka 
fails, the user will receive a 504 Timeout response. The user can restart this process from step 1. What if we produce the event multiple times to Kafka? Kafka’s 
exactly once guarantee ensures that this will not be a problem. 
13	 Our thumbnail generation service consumes the event from Kafka to begin 
thumbnail generation. 


278
Chapter 12  Design Flickr
14	 The thumbnail generation service fetches the file from the file storage service, 
generates the thumbnails, and writes the output thumbnails to the object storage 
service via the file storage service. 
Why doesn’t the thumbnail generation service write directly to the CDN? 
¡ The thumbnail generation service should be a self-contained service that 
accepts a request to generate a thumbnail, pulls the file from the file storage 
service, generates the thumbnail, and writes the result thumbnail back to the 
file storage service. Writing directly to other destinations such as the CDN 
introduces additional complexity, e.g., if the CDN is currently experiencing 
heavy load, the thumbnail generation service will have to periodically check 
if the CDN is ready to accept the file, while also ensuring that the former itself 
does not run out of storage in the meanwhile. It is simpler and more maintainable if writes to the CDN are handled by the file storage service. 
¡ Each service or host that is allowed to write to the CDN is an additional security maintenance overhead. We reduce the attack surface by not allowing the 
thumbnail generation service to access the CDN. 
15	 The thumbnail generation service writes a ThumbnailCdnRequest to the CDN 
topic to request the file storage service to write the thumbnails to the CDN. 
16	 The file storage service consumes this event from the CDN topic and fetches the 
thumbnail from the object storage service. 
17	 The file storage service writes the thumbnail to the CDN. The CDN returns the 
file’s key. 
18	 The file storage service inserts this key to the SQL table (if the key does not 
already exist) that holds the mapping of user ID to keys. Note that steps 16–18 are 
blocking. If the file storage service host experiences an outage during this insert 
step, its replacement host will rerun from step 16. The thumbnail size is only a 
few KB, so the computational resources and network overhead of this retry are 
trivial. 
19	 Depending on how soon our CDN can serve these (high-resolution and thumbnail) image files, we can delete these files from our file storage service immediately, or we can implement a periodic batch ETL job to delete files that were 
created an hour ago. Such a job may also query the CDN to ensure the files 
have been replicated to various data centers, before deleting them from our file 
storage service, but that may be overengineering. Our file storage service may 
retain the file hashes, so it can respond to requests to check if the file had been 
uploaded before. We may implement a batch ETL job to delete hashes that were 
created more than one hour ago. 


	
279
Uploading a photo 
CDN
8, 16
CDN Topic
SQL
5b
11
5a
Backend 
Service
9, 10, 17
7, 15
18
6, 14
File Storage 
Service
13
Thumbnail Generation Topic
14
Thumbnail 
Generation 
Service
Object Storage 
Service
Figure 12.5    Choreography of thumbnail generation, starting from step 5a. The arrows indicate the step 
numbers described in the main text. For clarity, we didn’t illustrate the user. Some of the events that the 
file storage service produces and consumes to the Kafka topics are to signal it to transfer image files 
between the object storage service and the CDN. There are also events to trigger thumbnail generation, 
and to write CDN metadata to the SQL service. 
Identify the transaction types
Which are the compensable transactions, pivot transaction, and retriable transactions? 
The steps before step 11 are the compensable transactions because we have not sent 
the user a confirmation response that the upload has succeeded. Step 11 is the pivot 
transaction because we will then confirm with the user that the upload has succeeded, 
and retry is unnecessary. Steps 12–16 are retriable transactions. We have the required 
(image file) data to keep retrying these (thumbnail generation) transactions, so they are 
guaranteed to succeed. 
If instead of just a thumbnail and the original resolution, we wish to generate multiple 
images, each with a different resolution and then the tradeoffs of both approaches 
become more pronounced. 
What if we use FTP instead of HTTP POST or RPC to upload photos? FTP writes to 
disk, so any further processing will incur the latency and CPU resources to read it from 
disk to memory. If we are uploading compressed files, to uncompress a file, we first 
need to load it from disk to memory. This is an unnecessary step that does not occur if 
we used a POST request or RPC. 


280
Chapter 12  Design Flickr
The upload speed of the file storage service limits the rate of thumbnail generation 
requests. If the file storage service uploads files faster than the thumbnail generation 
service can generate and upload thumbnails, the Kafka topic prevents the thumbnail 
generation service from being overloaded with requests.
Orchestration saga approach
We can also implement the file upload and thumbnail generation process as an orchestration saga. Our backend service is the orchestrator. Referring to figure 12.6, the steps 
in the orchestration saga of thumbnail generation are as follows:
1	 The first step is the same as in the choreography approach. The client makes a 
GET request to the backend to check if the image has already been uploaded. 
2	 Our backend service uploads the file to the object store service (not shown on 
figure 12.6) via the file storage service. Our file storage service produces an event 
to our file storage response topic to indicate that the upload succeeded. 
3	 Our backend service consumes the event from our file storage response topic.
4	 Our backend service produces an event to our CDN topic to request the file to be 
uploaded to the CDN. 
5	 (a) Our file storage service consumes from our CDN topic and (b) uploads the 
file to the CDN. This is done as a separate step from uploading to our object store 
service, so if the upload to the CDN fails, repeating this step does not involve a 
duplicate upload to our object store service. An approach that is more consistent 
with orchestration is for our backend service to download the file from the file 
storage service and then upload it to the CDN. We can choose to stick with the 
orchestration approach throughout or deviate from it here so the file does not 
have to move between three services. Keep in mind that if we do choose this deviation, we will need to configure the file storage service to make requests to the 
CDN. 
6	 Our file storage service produces an event to our CDN response topic to indicate 
that the file was successfully uploaded to the CDN. 
7	 Our backend service consumes from our CDN response topic. 
8	 Our backend service produces to our thumbnail generation topic to request 
that our thumbnail generation service generate thumbnails from the uploaded 
image. 
9	 Our thumbnail generation service consumes from our thumbnail generation 
topic.
10	 Our thumbnail generation service fetches the file from our file storage service, 
generates the thumbnails, and writes them to our file storage service.
11	 Our thumbnail generation service produces an event to our file storage topic to 
indicate that thumbnail generation was successful. 
12	 Our file storage service consumes the event from our file storage topic and 
uploads the thumbnails to the CDN. The same discussion in step 4, about orchestration versus network traffic, also applies here. 


	
281
Uploading a photo 
3
File Storage Topic
4
8
13
Backend 
Service 
Orchestrator
2
5b, 14b
6
File Storage 
Service
5a
File Storage 
Response Topic
10
11
Thumbnail 
Generation 
Service
CDN
7
Thumbnail 
Generation Topic
9
Thumbnail Generation 
Response Topic
12
Thumbnail Generation 
Response Topic
14a
Thumbnail Generation 
Response Topic
Figure 12.6    Orchestration of thumbnail generation, starting from step 2. Figure 12.5 illustrated the 
object storage service, which we omit on this diagram for brevity. For clarity, we also don’t illustrate the 
user. 
12.6.3	 Implementing both server-side and client-side generation
We can implement both server-side and client-side thumbnail generation. We can first 
implement server-side generation, so we can generate thumbnails for any client. Next, 
we can implement client-side generation for each client type, so we realize the benefits of client-side generation. Our client can first try to generate the thumbnail. If it 
fails, our server can generate it. With this approach, our initial implementations of 
client-side generation do not have to consider all possible failure scenarios, and we can 
choose to iteratively improve our client-side generation. 
This approach is more complex and costly than just server-side generation, but may 
be cheaper and easier than even just client-side generation because the client-side generation has the server-side generation to act as a failover, so client-side bugs and crashes 
will be less costly. We can attach version codes to clients, and clients will include these 
version codes in their requests. If we become aware of bugs in a particular version, we 
can configure our server-side generation to occur for all requests sent by these clients. 
We can correct the bugs and provide a new client version, and notify affected users to 
update their clients. Even if some users do not perform the update, this is not a serious 
problem because we can do these operations server-side, and these client devices will 
age and eventually stop being used. 


282
Chapter 12  Design Flickr
12.7	 Downloading images and data 
The images and thumbnails have been uploaded to the CDN, so they are ready for 
viewers. A request from a viewer for a sharer’s thumbnails is processed as follows: 
1	 Query the Share table for the list of sharers who allow the viewer to view the former’s images. 
2	 Query the Image table to obtain all CdnPath values of thumbnail resolutions 
images of the user. Return the CdnPath values and a temporary OAuth2 token to 
read from the CDN. 
3	 The client can then download the thumbnails from the CDN. To ensure that the 
client is authorized to download the requested files, our CDN can use the token 
authorization mechanism that we will introduce in detail in section 13.3. 
Dynamic content may be updated or deleted, so we store them on SQL rather than on 
the CDN. This includes photo comments, user profile information, and user settings. 
We can use a Redis cache for popular thumbnails and popular full-resolution images. 
When a viewer favorites an image, we can take advantage of the immutable nature of 
the images to cache both the thumbnails and the full-resolution image on the client 
if it has sufficient storage space. Then a viewer’s request to view their grid of favorite 
images will not consume any server resources and will also be instantaneous. 
For the purpose of the interview, if we were not allowed to use an available CDN and 
then the interview question becomes how to design a CDN, which is discussed in the 
next chapter. 
12.7.1	 Downloading pages of thumbnails
Consider the use case where a user views one page of thumbnails at a time, and each 
page is maybe 10 thumbnails. Page 1 will have thumbnails 1–10, page 2 will have 
thumbnails 11–20, and so on. If a new thumbnail (let’s call it thumbnail 0) is ready 
when the user is on page 1, and the user goes to page 2, how can we ensure that the 
user’s request to download page 2 returns a response that contains thumbnails 11–20 
instead of 10–19? 
One technique is to version the pagination like GET thumbnails?page=<page 
>&page_version=<page_version>. If page_version is omitted, the backend can substitute the latest version by default. The response to this request should contain page_ 
version, so the user can continue using the same page_version value for subsequent 
requests as appropriate. This way, a user can smoothly flip through pages. When the 
user returns to page 1, they can omit page_version and the latest page 1 of thumbnails 
will be displayed.
However, this technique only works if thumbnails are added to or deleted from the 
beginning of the list. If thumbnails are added to or deleted from other positions in 
the list while the user is flipping through pages, the user will not see the new thumbnails or continue to see the deleted thumbnails. A better technique is for the client to 


	
283
Some other services 
pass the current first item or last item to the backend. If the user is flipping forward, use GET thumbnails?previous_last=<last_item>. If the user is flipping 
backward, use GET thumbnails?previous_first=<first_item>. Why this is so is left as 
a simple exercise to the reader.
12.8	 Monitoring and alerting 
Besides what was discussed in section 2.5, we should monitor and alert on both file 
uploads and downloads, and requests to our SQL database. 
12.9	 Some other services 
There are many other services we may discuss in no particular order of priority, including monetization such as ads and premium features, payments, censorship, personalization, etc. 
12.9.1	 Premium features
Our image-sharing service can offer a free tier, with all the functionalities we have discussed so far. We can offer sharers premium features such as the following.
Sharers can state that their photos are copyrighted and that viewers must pay to 
download their full-resolution photos and use them elsewhere. We can design a system for sharers to sell their photos to other users. We will need to record the sales and 
keep track of photo ownership. We may provide sellers with sales metrics, dashboards, 
and analytics features for them to make better business decisions. We may provide recommender systems to recommend sellers what type of photos to sell and how to price 
them. All these features may be free or paid. 
We can offer a free tier of 1,000 photos for free accounts and larger allowances for 
various subscription plans. We will also need to design usage and billing services for 
these premium features. 
12.9.2	 Payments and taxes service
Premium features require a payments service and a tax service to manage transactions 
and payments from and to users. As discussed in section 15.1, payments are very complex topics and generally not asked in a system design interview. The interviewer may 
ask them as a challenge topic. The same concerns apply to taxes. There are many possible types of taxes, such as sales, income, and corporate taxes. Each type can have many 
components, such as country, state, county, and city taxes. There can be tax-exemption 
rules regarding income level or a specific product or industry. Tax rates may be progressive. We may need to provide relevant business and income tax forms for the locations where the photos were bought and sold. 
12.9.3	 Censorship/content moderation
Censorship, also commonly called content moderation, is important in any application where users share data with each other. It is our ethical (and in many cases also 


284
Chapter 12  Design Flickr
legal) responsibility to police our application and remove inappropriate or offensive 
content, regardless of whether the content is public or only shared with select viewers. 
We will need to design a system for content moderation. Content moderation can 
be done both manually and automatically. Manual methods include mechanisms for 
viewers to report inappropriate content and for operations staff to view and delete this 
content. We may also wish to implement heuristics or machine-learning approaches 
for content moderation. Our system must also provide administrative features such as 
warning or banning sharers and make it easy for operations staff to cooperate with local 
law enforcement authorities. 
12.9.4	 Advertising
Our clients can display ads to users. A common way is to add a third-party ads SDK to 
our client. Such an SDK is provided by an ad network (e.g., Google Ads). The ad network provides the advertiser (i.e., us) with a console to select categories of ads that we 
prefer or do not desire. For example, we may not wish to show mature ads or ads from 
competitor companies. 
Another possibility is to design a system to display ads for our sharers internally 
within our client. Our sharers may wish to display ads within our client to boost their 
photo sales. One use case of our app is for viewers to search for photos to purchase to 
use for their own purposes. When a viewer loads our app’s homepage, it can display 
suggested photos, and sharers may pay for their photos to appear on the homepage. We 
may also display “sponsored” search results when a viewer searches for photos. 
We may also provide users with paid subscription packages in exchange for an ad-free 
experience. 
12.9.5	 Personalization
As our service scales to a large number of users, we will want to provide personalized 
experiences to cater to a wide audience and increase revenue. Based on the user’s 
activity both within the app and from user data acquired from other sources, a user can 
be provided with personalized ads, search, and content recommendations. 
Data science and machine-learning algorithms are usually outside the scope of a system design interview, and the discussion will be focused on designing experimentation 
platforms to divide users into experiment groups, serve each group from a different 
machine-learning model, collect and analyze results, and expand successful models to 
a wider audience. 


	
285
Other possible discussion topics
12.10	Other possible discussion topics
Other possible discussion topics include the following: 
¡ We can create an Elasticsearch index on photo metadata, such as title, description, and tags. When a user submits a search query, the search can do fuzzy matching on tags as well as titles and descriptions. Refer to section 2.6.3 for a discussion 
on creating an Elasticsearch cluster. 
¡ We discussed how sharers can grant view access to their images to viewers. We 
can discuss more fine-grained access control to images, such as access control 
on individual images, permissions to download images in various resolutions, or 
permission for viewers to share images to a limited number of other viewers. We 
can also discuss access control to user profiles. A user can either allow anyone to 
view their profile or grant access to each individual. Private profiles should be 
excluded from search results. 
¡ We can discuss more ways to organize photos. For example, sharers may add 
photos to groups. A group may have photos from multiple sharers. A user may 
need to be a group member to view and/or share photos to it. A group may have 
admin users, who can add and remove users from the group. We can discuss various ways to package and sell collections of photos and the related system design. 
¡ We can discuss a system for copyright management and watermarking. A user 
may assign a specific copyright license to each photo. Our system may attach 
an invisible watermark to the photo and may also attach additional watermarks 
during transactions between users. These watermarks can be used to track ownership and copyright infringement. 
¡ The user data (image files) on this system is sensitive and valuable. We may discuss 
possible data loss, prevention, and mitigation. This includes security breaches 
and data theft. 
¡ We can discuss strategies to control storage costs. For example, we can use different storage systems for old versus new files or for popular images versus other 
images.
¡ We can create batch pipelines for analytics. An example is a pipeline to compute 
the most popular photos, or uploaded photo count by hour, day, and month. 
Such pipelines are discussed in chapter 17. 
¡ A user can follow another user and be notified of new photos and/or comments.
¡ We can extend our system to support audio and video streaming. Discussing 
video streaming requires domain-specific expertise that is not required in a general system design interview, so this topic may be asked in interviews for specific 
roles where said expertise is required, or it may be asked as an exploratory or 
challenge question. 


286
Chapter 12  Design Flickr
Summary
¡ Scalability, availability, and high download performance are required for a file- 
or image-sharing service. High upload performance and consistency are not 
required.
¡ Which services are allowed to write to our CDN? Use a CDN for static data, but 
secure and limit write access to sensitive services like a CDN. 
¡ Which processing operations should be put in the client vs. the server? One consideration is that processing on a client can save our company hardware resources 
and cost, but may be considerably more complex and incur more costs from this 
complexity.
¡ Client-side and server-side have their tradeoffs. Server-side is generally preferred 
where possible for ease of development/upgrades. Doing both allows the low 
computational cost of client-side and the reliability of server-side. 
¡ Which processes can be asynchronous? Use techniques like sagas for those processes to improve scalability and reduce hardware costs.


287
13
Design a Content 
Distribution Network
This chapter covers
¡ Discussing the pros, cons, and unexpected 	
	 situations
¡ Satisfying user requests with frontend 
	 metadata storage architecture
¡ Designing a basic distributed storage system
A CDN (Content Distribution Network) is a cost-effective and geographically distributed file storage service that is designed to replicate files across its multiple data 
centers to serve static content to a large number of geographically distributed users 
quickly, serving each user from the data center that can serve them fastest. There 
are secondary benefits, such as fault-tolerance, allowing users to be served from 
other data centers if any particular data center is unavailable. Let’s discuss a design 
for a CDN, which we name CDNService.


288
Chapter 13  Design a Content Distribution Network 
13.1	 Advantages and disadvantages of a CDN 
Before we discuss the requirements and system design for our CDN, we can first discuss 
the advantages and disadvantages of using a CDN, which may help us understand our 
requirements. 
13.1.1	 Advantages of using a CDN 
If our company hosts services on multiple data centers, we likely have a shared object 
store that is replicated across these data centers for redundancy and availability. This 
shared object store provides many of the benefits of a CDN. We use a CDN if our geographically distributed userbase can benefit from the extensive network of data centers 
that a CDN provides. 
The reasons to consider using a CDN were discussed in section 1.4.4, and some are 
repeated here: 
¡ Lower latency—A user is served from a nearby data center, so latency is lower. 
Without a third-party CDN, we will need to deploy our service to multiple data 
centers, which carries considerable complexity, such as monitoring to ensure 
availability. Lower latency may also carry other benefits, such as improving SEO 
(search engine optimization). Search engines tend to penalize slow web pages 
both directly and indirectly. An example of an indirect penalty is that users may 
leave a website if it loads slowly; such a website can be described as having a high 
bounce rate, and search engines penalize websites with high bounce rates. 
¡ Scalability—With a third-party provider, we do not need to scale our system ourselves. The third party takes care of scalability. 
¡ Lower unit costs—A third-party CDN usually provides bulk discount, so we will 
have lower unit costs as we serve more users and higher loads. It can provide 
lower costs as it has economies of scale from serving traffic for many companies 
and spread the costs of hardware and appropriately skilled technical personnel 
over this larger volume. The fluctuating hardware and network requirements of 
multiple companies can normalize each other and result in more stable demand 
versus serving just a single company. 
¡ Higher throughput—A CDN provides additional hosts to our service, which allows 
us to serve a larger number of simultaneous users and higher traffic. 
¡ Higher availability—The additional hosts can serve as a fallback should our service’s hosts fail, especially if the CDN is able to keep to its SLA. Being geographically distributed across multiple data centers is also beneficial for availability, as 
a disaster that causes an outage on a single data center will not affect other data 
centers located far away. Moreover, unexpected traffic spikes to a single data center can be redirected and balanced across the other data centers. 


	
289
Advantages and disadvantages of a CDN 
13.1.2	 Disadvantages of using a CDN 
Many sources discuss the advantages of a CDN, but few also discuss the disadvantages. 
An interview signal of an engineer’s maturity is their ability to discuss and evaluate 
tradeoffs in any technical decision and anticipate challenges by other engineers. The 
interviewer will almost always challenge your design decisions and probe if you have 
considered various non-functional requirements. Some disadvantages of using a CDN 
include the following: 
¡ The additional complexities of including another service in our system. Examples of such complexities include: 
–	 An additional DNS lookup 
–	 An additional point of failure 
¡ A CDN may have high unit costs for low traffic. There may also be hidden costs, 
like costs per GB of data transfer because CDNs may use third-party networks. 
¡ Migrating to a different CDN may take months and be costly. Reasons to migrate 
to another CDN include: 
–	 A particular CDN may not have hosts located near our users. If we acquire a 
significant user base in a region not covered by your CDN, we may need to 
migrate to a more suitable CDN. 
–	 A CDN company may go out of business. 
–	 A CDN company may provide poor service, such as not fulfilling its SLA, which 
affects our own users; provide poor customer support; or experience incidents 
like data loss or security breaches. 
¡ Some countries or organizations may block the IP addresses of certain CDNs. 
¡ There may be security and privacy concerns in storing your data on a third party. 
We can implement encryption at rest so the CDN cannot view our data, which 
will incur additional cost and latency (from encrypting and decrypting data). 
The design and implementation must be implemented or reviewed by qualified 
security engineers, which adds additional costs and communication overhead to 
our team. 
¡ Another possible security concern is that it’s possible to insert malicious code 
into JavaScript libraries, and we cannot personally ensure the security and integrity of these remotely hosted libraries. 
¡ The flip side of allowing a third-party to ensure high availability is that if technical 
problems occur with the CDN occur, we do not know how long it will take for the 
CDN company to fix them. Any service degradation may affect our customers, 
and the communication overhead of communicating with an external company 
may be greater than communication within our company. The CDN company 
may provide an SLA, but we cannot be sure that it will be honored, and migrating to another CDN is costly, as we just discussed. Moreover, our SLA becomes 
dependent on a third party. 


290
Chapter 13  Design a Content Distribution Network 
¡ The configuration management of a CDN or any third-party tool/service in general may be insufficiently customizable for certain of our use cases, leading to 
unexpected problems. The next section discusses an example. 
13.1.3	 Example of an unexpected problem from using a CDN to serve images 
This section discusses an example of an unexpected problem that can occur from 
using a CDN or third-party tools or services in general. 
A CDN may read a GET request’s User-Agent (https://developer.mozilla.org/
en-US/docs/Web/HTTP/Headers/User-Agent) header to determine if the request is 
from a web browser, and if so, return images in WebP (https://developers.google.com/
speed/webp) format instead of the format it was uploaded in (such as PNG or JPEG). 
In some services, this may be ideal, but other browser applications that want images to 
be returned in their original formats have three choices: 
1	 Override the User-Agent header in our web application. 
2	 Configure the CDN to serve WebP images for certain services and images in the 
original formats for other services. 
3	 Route the request through a backend service.
Regarding solution 1, as of publication of this book, Chrome web browser does not 
allow applications to override the User-Agent header, while Firefox does (Refer to 
https://bugs.chromium.org/p/chromium/issues/detail?id=571722, https://bugzilla 
.mozilla.org/show_bug.cgi?id=1188932, and https://stackoverflow.com/a/42815264.) 
Solution 1 will limit our users to specific web browsers, which may be infeasible. 
Regarding solution 2, the CDN may not provide the ability to customize this setting 
for individual services. It may only allow the setting to serve images in WebP format to 
be broadly turned on or off across all our services. Even if it does provide such individualized configuration, the relevant infrastructure team in our company that manages 
CDN configurations may be unable or unwilling to set this configuration for individual 
services in our company. This problem may be more prevalent in large companies. 
Solution 3 requires developers to expose an API endpoint just to fetch the original 
image from the CDN. This solution should be best avoided because it negates most of 
all the benefits of a CDN. It adds additional latency and complexity (including documentation and maintenance overhead). The backend host may be geographically far 
from the user, so the user loses the benefit from the CDN of being served from a nearby 
data center. This backend service will need to scale with demand for the images; if the 
request rate for the images is high, both the CDN and the backend service need be 
scaled up. Rather than adopting this solution, it makes more sense to store the files in 
a cheaper object store whose hosts are in the same data center as our backend service. 
Unfortunately, I have personally seen this “solution” used in big companies because the 
application and the CDN were owned by different teams, and management was uninterested in fostering cooperation between them.


	
291
CDN authentication and authorization
13.2	 Requirements 
Functional requirements are simple. Authorized users should be able to create directories, upload files with 10 GB file size limit, and download files. 
NOTE    We will not discuss content moderation. Content moderation is essential 
in any application where users see content created by others. We assume that it is 
the responsibility of the organizations that use our CDN, not the responsibility of 
the company that provides the CDN. 
Most of the non-functional requirements are the advantages of a CDN: 
¡ Scalable—The CDN may scale to support petabytes of storage and download volumes of terabytes per day. 
¡ High availability—Four or five 9s uptime required. 
¡ High performance—A file should be downloaded from the data center that can 
serve it fastest to the requestor. However, synchronization may take time, so 
upload performance is less important, as long as the file is available on at least 
one data center before synchronization is complete. 
¡ Durable—A file must not be corrupted. 
¡ Security and privacy—The CDN serves requests and sends files to destinations outside the data center. Files should only be downloaded and uploaded by authorized users. 
13.3	 CDN authentication and authorization
As discussed in appendix B, the purpose of authentication is to verify a user’s identity, 
while the purpose of authorization is to ensure that a user accessing a resource (such as 
a file in our CDN) has permission to do so. These measures prevent hotlinking, in which 
a site or service accesses CDN assets without permission. Our CDN incurs the costs of 
serving these users without getting paid for it, and unauthorized file or data access may 
be a copyright violation.
TIP    Refer to appendix B for an introduction to authentication and authorization. 
CDN authentication and authorization can be done with either cookie-based authentication or token-based authentication. As discussed in section B.4, token-based authentication uses less memory, can use third-party services with more security expertise, 
and allow fine-grained access control. Besides these benefits, token authentication for 
our CDN also allows requestors to be restricted to allowed IP addresses or specific user 
accounts. 
In this section, we discuss a typical implementation for CDN authentication and 
authorization. The following sections discuss a possible CDN system design that we may 
discuss during an interview, including how this authentication and authorization process can be done in our design. 


292
Chapter 13  Design a Content Distribution Network 
13.3.1	 Steps in CDN authentication and authorization
In this discussion, we refer to a CDN customer as a site or service that uploads assets to 
a CDN and then directs its users/clients to the CDN. We refer to a CDN user as a client 
that downloads assets from a CDN. 
The CDN issues each customer a secret key and provides an SDK or library to generate access tokens from the following information. Referring to figure 13.1, the access 
token generation process is as follows: 
1	 The user sends an authentication request to the customer app. The customer app 
may perform the authentication using an authentication service. (The details of 
the authentication mechanism are irrelevant for the CDN access token generation process. Refer to appendix B for an introduction to various authentication 
protocols like Simple Login and OpenID Connect.)
2	 The customer app generates an access token using the SDK, with the following 
inputs:
a	 Secret key—The customer’s secret key. 
b	 CDN URL—The CDN URL that the generated access token is valid for.
c	 Expiry—The access token’s expiry timestamp, after which the user needs a new 
access token. When a user makes a request to the CDN with an expired token, 
the CDN can return a 302 response to redirect the user to the customer. The 
customer generates a new access token and then returns this access token to 
the user with a 302 response to retry the request on the CDN. 
d	 Referrer—This is a Referrer HTTP request header. 
Referrer header and security
When a client/user makes an HTTP request to a CDN, it should include the customer’s 
URL as its Referrer HTTP header. The CDN only allows authorized referrers, so this prevents unauthorized referrers from using the CDN. 
However, this is not a legitimate security mechanism. Clients can easily spoof Referrer 
headers by simply using a different URL as the Referrer header. A site/service can 
spoof a referrer header by impersonating an authorized site/service and fool clients to 
believe that the latter are communicating with the authorized site/service.
e	 Allowed IPs—This may be a list of IP address ranges that are authorized to 
download CDN assets. 
f	 Allowed countries or regions—We may include a blacklist or whitelist of countries/regions. This “Allowed IPs” field already indicates which countries/
regions are allowed, but we can still include this field for convenience. 
3	 The customer app stores the token and then returns this token to the user. For 
additional security, the token can be stored in an encrypted form. 


	
293
CDN authentication and authorization
4	 Whenever a customer app gives a user a CDN URL, and the user makes a 
GET request for this CDN asset, the GET request should be signed with the 
access token. This is called URL signing. An example of a signed URL is 
http://12345.r.cdnsun.net/photo.jpeg?secure=DMF1ucDxtHCxwYQ 
(from 
https://cdnsun.com/knowledgebase/cdn-static/setting-a-url-signing-protect 
-your-cdn-content). “secure=DMF1ucDxtHCxwYQ” is a query parameter to send 
the access token to the CDN. The CDN performs authorization. It verifies that 
the user’s token is valid and that the asset can be downloaded with that token, as 
well as with the user’s IP or country/region. Finally, the CDN returns the asset to 
the user. 
5	 When a user logs out, the customer app destroys the user’s token. The user will 
need to generate another token when logging in. 
CDN
Authentication
Service
Store token.
Success.
Authenticate.
Access token.
Authenticate.
Success.
Customer App
User
Request CDN asset using token.
Success.
Log out
Access token.
CDN asset.
Generate access token.
Success.
Delete token.
Figure 13.1    Sequence diagram of token generation process, followed by using the token to request 
CDN assets, and destroying the token upon user logout. The process of destroying the token can be 
asynchronous as illustrated here, or it can be synchronous because logouts are not frequent events. 


294
Chapter 13  Design a Content Distribution Network 
Deleting the token can be asynchronous as illustrated in figure 13.1, or it can be synchronous because logouts are not frequent events. If token deletion is asynchronous, 
there is a risk that tokens will not be deleted if the customer app host handling this 
deletion suddenly fails. One solution is to simply ignore this problem and allow some 
tokens to not be destroyed. Another solution is to use an event-driven approach. The 
customer app host can produce a token deletion event to a Kafka queue, and a consumer cluster can consume these events and delete the tokens on the CDN. A third 
solution is to implement token deletion as synchronous/blocking. If token deletion 
fails because the customer app host suddenly fails, the user/client will receive a 500 
error, and the client can retry the logout request. This approach will result in higher 
latency for the logout request, but this may be acceptable. 
Refer to sources like https://docs.microsoft.com/en-us/azure/cdn/cdn-token-auth, 
https://cloud.ibm.com/docs/CDN?topic=CDN-working-with-token-authentication, 
https://blog.cdnsun.com/protecting-cdn-content-with-token-authentication-and-url 
-signing for more information on CDN token authentication and authorization. 
13.3.2	 Key rotation
A customer’s key may be periodically changed, just in case a hacker manages to steal 
the key, the damage can be limited as it will only be useful to him until the key is 
changed. 
The key is rotated rather than suddenly changed. Key rotation is a key renewal process, which contains a period where both the old and new keys are valid. It will take time 
for a new key to be disseminated to all the customer’s systems, so the customer may continue using both the old and new key in the meantime. At a set expiry time, the old key 
will expire, and users cannot access CDN assets with expired keys. 
It is also useful to establish this procedure for cases where we know that a hacker has 
stolen the key. The CDN can rotate the key and set a short time to expiration for the old 
key. The customer can switch to the new key as soon as possible. 
13.4	 High-level architecture 
Figure 13.2 shows high-level architecture of our CDN. We adopt a typical API gateway-metadata-storage/database architecture. A user request is handled by an API gateway, which is a layer/service that makes requests to various other services. (Refer to 
section 1.4.6 for an overview of API gateway.) These include SSL termination, authentication and authorization, rate limiting (refer to chapter 8), and logging to a shared 
logging service for purposes such as analytics and billing. We can configure the API 
gateway to look up the metadata service to determine which storage service host to 
read or write to for any user. If the CDN asset is encrypted at rest, the metadata service can also record this, and we can use a secrets management service to manage the 
encryption keys. 


	
295
Storage service 
API Gateway
Storage 
Service
Users
Metadata 
Service
Logging 
Service
Secrets 
Management
Service
Rate Limiting 
Service
Origin
Figure 13.2    High-level architecture of our CDN. User requests are routed through an API gateway, which 
makes requests to the appropriate services, including rate limiting and logging. Assets are stored on a 
storage service, and the metadata service keeps track of the storage service hosts and file directories 
that store each asset. If the assets are encrypted, we use a secrets management service to manage 
the encryption keys. If the requested asset is missing, the API gateway retrieves it from the origin (i.e., 
our service; this is configured in the metadata service), adds it to the storage service, and updates the 
metadata service. 
We can generalize the operations into reads (download) vs. writes (directory creation, 
upload, and file deletion). For simplicity of the initial design, every file can be replicated to every data center. Otherwise, our system will have to handle complexities such 
as: 
¡ The metadata service will track which data centers contain which files. 
¡ A file distribution system that periodically uses user query metadata to determine 
the optimal file distribution across the data centers. This includes the number 
and locations of replicas. 
13.5	 Storage service 
The storage service is a cluster of hosts/nodes which contain the files. As discussed 
in section 4.2, we should not use a database to store large files. We should store files 
in the hosts’ filesystems. Files should be replicated for availability and durability, with 
each file assigned to multiple (e.g., three) hosts. We need availability monitoring and a 
failover process that updates the metadata service and provisions replacement nodes. 
The host manager can be in-cluster or out-cluster. An in-cluster manager directly 
manages nodes, while an out-cluster manager manages small independent clusters of 
nodes, and each small cluster manages itself. 


296
Chapter 13  Design a Content Distribution Network 
13.5.1	 In-cluster 
We can use a distributed file system like HDFS, which includes ZooKeeper as the 
in-cluster manager. ZooKeeper manages leader election and maintains a mapping 
between files, leaders, and followers. An in-cluster manager is a highly sophisticated 
component that also requires reliability, scalability, and high performance. An alternative that avoids such a component is an out-cluster manager. 
13.5.2	 Out-cluster 
Each cluster managed by an out-cluster manager consists of three or more nodes distributed across several data centers. To read or write a file, the metadata service identifies the cluster it is or should be stored in and then reads or writes the file from a 
randomly selected node in the cluster. This node is responsible for replication to other 
nodes in the cluster. Leader election is not required, but mapping files to clusters is 
required. The out-cluster manager maintains a mapping of files to clusters. 
13.5.3	 Evaluation 
In practice, out-cluster manager is not really simpler than in-cluster manager. Table 
13.1 compares these two approaches. 
Table 13.1    Comparison of in-cluster manager and out-cluster manager
In-cluster manager
Out-cluster manager
Metadata service does not 
make requests to the in-cluster 
manager.
Metadata service makes requests 
to the out-cluster manager.
Manages file assignment within 
individual roles in the cluster.
Manages file assignment to a 
cluster, but not to individual 
nodes.
Needs to know about every node 
in the cluster.
May not know about each individual node, but needs to know 
about each cluster.
Monitors heartbeats from nodes.
Monitors health of each independent cluster.
Deals with host failures. Nodes 
may die, and new nodes may be 
added to the cluster.
Tracks each cluster’s utilization 
and deals with overheated clusters. New files may no longer be 
assigned to clusters that reach 
their capacity limits. 


	
297
Common operations 
13.6	 Common operations 
When the client makes a request with our CDN service’s domain (e.g., cdnservice.flickr 
.com) rather than an IP address, GeoDNS (refer to sections 1.4.2 and 7.9) assigns the 
IP address of the closest host, where a load balancer directs it an API gateway host. As 
described in section 6.2, the API gateway performs a number of operations, including 
caching. The frontend service and its associated caching service can assist with caching 
frequently accessed files. 
13.6.1	 Reads: Downloads 
For a download, the next step is to select a storage host to serve this request. The metadata service aids in this selection by maintaining and providing the following metadata. It can use Redis and/or SQL: 
¡ The storage service hosts which contain the files. Some or all the hosts may be on 
other data centers, so that information must be stored, too. Files take time to be 
replicated across hosts. 
¡ The metadata service of each data center keeps track of the current load of its 
hosts. A host’s load can be approximated by the sum of the sizes of the files it is 
currently serving. 
¡ For purposes such as estimating how much time a file takes to download from a 
host or to distinguish between files with the same name (but this is usually done 
with MD5 or SHA hash). 
¡ File ownership and access control. 
¡ Health status of hosts. 
Download process
Figure 13.3 is a sequence diagram of the steps taken by the API gateway to download a 
file, assuming the CDN does contain this asset. We omit some steps such as SSL termination, authentication and authorization, and logging.
1	 Query the rate limiting service to check if the request exceeds the client’s rate 
limit. We assume that rate limiter allows the request through. 
2	 Query the metadata service to get the storage service hosts that contain this asset. 
3	 Select a storage host and stream the asset to the client. 
4	 Update the metadata service with the load increase of the storage host. If the 
metadata service records the asset’s size, this step can be done in parallel with 
step 3. Otherwise, the API gateway will need to measure the asset’s size, to update 
the metadata service with the correct load increase. 


298
Chapter 13  Design a Content Distribution Network 
API Gateway
Request file.
Asset.
Check rate limit.
Metadata Service
Storage Service
Client
Rate Limiting
Service
OK.
Asset.
GET metadata.
GET asset.
Metadata, including storage host ID.
Figure 13.3    Sequence diagram of a client making a CDN download. We assume rate limiter allows the 
request through. The sequence is straightforward if the asset is present. 
An alert reader may note that the last step of the API gateway updating the load to the 
metadata service can be done asynchronously. If the API gateway host experiences an 
outage during this update, the metadata service may not receive it. We can choose to 
ignore this error and allow the user to use the CDN more than the former is allowed 
to. Alternatively, the API gateway host can produce this event to a Kafka topic. Either 
the metadata service can consume from this topic, or we can use a dedicated consumer 
cluster to consume from the topic and then update the metadata service. 
The CDN may not contain this asset. It may have deleted it for reasons including the 
following:
¡ There may be a set retention period for assets, such as a few months or years, and 
this period had passed for that asset. The retention period may also be based on 
when the asset was last accessed. 
¡ A less likely reason is that the asset was never uploaded because the CDN ran out 
of storage space (or had other errors), but the customer believed that the asset 
was successfully uploaded. 
¡ Other errors in the CDN. 
Referring to figure 13.4, if the CDN does not have the asset, it will need to download it 
from the origin, which is a backup location provided by the customer. This will increase 
latency. It will then need to store it by uploading it to the storage service and updating 
the metadata service. To minimize latency, the storage process can be done in parallel 
with returning the asset to the client. 


	
299
Common operations 
API
Gateway
Request file.
Check
rate limit.
Metadata
Service
Storage
Service
Client
Origin
GET asset
Asset.
par
Rate Limiting
Service
OK.
Asset
POST asset.
Response, including asset key.
POST asset metadata
Response OK.
Response OK.
Metadata, including
storage host ID.
GET metadata.
Update load.
Figure 13.4    Sequence diagram of a CDN download process if the CDN does not contain the requested 
asset. The CDN will need to download the asset from the origin (a backup location provided by the 
customer), and return it to the user, as well as store the asset for future requests. POST asset metadata 
and upload load can be done as a single request, but we can keep them as separate requests for 
simplicity. 
Download process with encryption at rest
What if we needed to store assets in encrypted form? Referring to figure 13.5, we can 
store the encryption keys in a secrets management service (which requires authentication). When an API gateway host is initialized, it can authenticate with the secrets 
management service, which will pass the former a token for future requests. Referring 
to figure 13.5, when an authorized user requests an asset, the host can first obtain the 
asset’s encryption key from the secrets management service, fetch the encrypted asset 


300
Chapter 13  Design a Content Distribution Network 
from the storage service, decrypt the asset, and return it to the user. If the asset is large, 
it may be stored in multiple blocks in the storage service, and each block will need to 
be separately fetched and decrypted. 
API
Gateway
Check
rate limit.
Storage
Service
Metadata
Service
Secrets Management
Service
Client
Rate Limiting
Service
Key.
GET key.
Asset.
Request
file.
OK.
GET metadata.
Metadata, including
storage host ID.
GET asset.
Asset.
Decrypt asset.
Plaintext asset.
Figure 13.5    Sequence diagram of downloading an asset that is encrypted at rest, assuming the asset 
is present in the CDN. If the asset is large, it may be stored in multiple blocks in the storage service, and 
each block will need to be separately fetched and decrypted. 
Figure 13.6 illustrates the process that occurs if a request is made to fetch an encrypted 
asset that the CDN does not possess. Similar to figure 13.5, the API gateway will need to 
fetch the asset from the origin. Next, the API gateway can parallelly return the asset to 
the user while storing it in the storage service. The API gateway can generate a random 
encryption key, encrypt the asset, write the asset to the storage service, and write the 
key to the secrets management service. 


	
301
Common operations 
API
Gateway
Request file.
Check
rate limit.
Metadata
Service
Storage
Service
Client
Origin
GET asset
Asset.
Rate Limiting
Service
OK.
Asset
POST asset.
Response, including asset key.
Secrets
Management
Service
POST key.
Response OK.
par
GET metadata.
Metadata, including
storage host ID.
Encrypt asset.
Ciphertext asset.
Update load.
Response OK.
Figure 13.6    Sequence diagram of the steps to download an encrypted file. POST asset and POST key 
can also be done in parallel. 
13.6.2	 Writes: Directory creation, file upload, and file deletion 
A file is identified by its ID, not its content. (We cannot use file names as identifiers 
because different users can give different files the same name. Even an individual user 
may give the same name to different files.) We consider files with different IDs but 
the same contents to be different files. Should identical files with different owners 
be stored separately, or should we attempt to save storage by keeping only one copy 
of a file? To save storage in this manner, we will have to build an additional layer of 


302
Chapter 13  Design a Content Distribution Network 
complexity to manage groups of owners, so that any owner may see that a file is accessible by other owners that they recognize, rather than owners that belong to other 
groups. We assume that the number of identical files is a small fraction of all the files, 
so this may be over-engineering. Our initial design should store such files separately, 
but we must remember that there are no absolute truths in system design (thus system 
design is an art, not a science). We can discuss with our interviewer that as the total 
amount of storage our CDN uses becomes large, the cost savings of saving storage by 
deduplicating the files may be worth the additional complexity and cost. 
A file can be GB or TB in size. What if file upload or download fails before it is complete? It will be wasteful to upload or download the file from the beginning. We should 
develop a process similar to checkpointing or bulkhead to divide a file into chunks, so a 
client only needs to repeat the upload or download operations on the chunks that have 
not completed. Such an upload process is known as multipart upload, and we can also 
apply the same principles to downloads, too. 
We can design a protocol for multipart uploads. In such a protocol, uploading a 
chunk can be equivalent to uploading an independent file. For simplicity, chunks can 
be of fixed size, such as 128 MB. When a client begins a chunk upload, it can send an 
initial message that contains the usual metadata such as the user ID, the filename, and 
size. It can also include the number of the chunk about to be uploaded. In multipart 
upload, the storage host will now need to allocate a suitable address range on the disk 
to store the file and record this information. When it starts receiving a chunk upload, 
it should write the chunk to the appropriate addresses. The metadata service can track 
which chunk uploads have completed. When the client completes uploading the final 
chunk, the metadata service marks the file as ready for replication and download. If a 
chunk upload fails, the client can reupload just this chunk instead of the entire file. 
If the client stops uploading the file before all chunks are successfully uploaded, 
these chunks will uselessly occupy space in our storage host. We can implement a simple cron job or a batch ETL job that periodically deletes these chunks of incompletely 
uploaded files. Other possible discussion topics include:
¡ Allowing the client to choose the chunk size. 
¡ Replicating the file as it is being uploaded, so the file can be ready for download 
sooner across the CDN. This introduces additional complexity and is unlikely to 
be required, but we can discuss such a system should such high performance be 
required.
¡ A client can start playing a media file as soon as it downloads the first chunk. We 
will briefly discuss this in section 13.9. 
NOTE    The multipart upload with checkpointing that we discussed here is 
unrelated to multipart/form-data HTML encoding. The latter is for uploading 
form data that contains files. Refer to sources such as https://swagger.io/docs/ 
specification/describing-request-body/multipart-requests/ and https://developer 
.mozilla.org/en-US/docs/Web/HTTP/Methods/POST for more details. 


	
303
Common operations 
Another question is how to handle adding, updating (the contents), and deleting files 
on this distributed system. Section 4.3 discussed replication of update and delete operations, their complications, and some solutions. We can discuss some possible solutions adopted from that section: 
¡ A single-leader approach that designates a particular data center to perform 
these operations and propagate the changes to the other data centers. This 
approach may be adequate for our requirements, especially if we do not require 
the changes to be rapidly available on all data centers. 
¡ The multi-leader approaches discussed, including tuples. (Refer to Martin Kleppmann’s book Designing Data-Intensive Systems for a discussion on tuples.)
¡ The client acquires a lock on this file in every data center, performs this operation on every data center, and then releases the locks. 
In each of these approaches, the frontend updates the metadata service with the file’s 
availability on the data centers. 
Do not keep file copies on all data centers 
Certain files may be used mostly by particular regions (e.g., audio or text files in human 
languages predominantly used in a particular region), so not all data centers need to 
contain a copy of the files. We can set replication criteria to determine when a file 
should be copied to a particular data center (e.g., number of requests or users for this 
file within the last month). However, this means that the file needs to be replicated 
within a data center for fault-tolerance. 
Certain contents are separated into multiple files because of application requirements to serve certain file combinations to certain users. For example, a video file may 
be served to all users, and it has an accompanying audio file in a particular language. 
This logic can be handled at the application level rather than by the CDN. 
Rebalancing the batch ETL job 
We have a periodic (hourly or daily) batch job to distribute files across the various data 
centers and replicate files to the appropriate number of hosts to meet demand. This 
batch job obtains the file download logs of the previous period from the logging service, determines the request counts of the files, and uses these numbers to adjust the 
numbers of storage hosts for each file. Next, it creates a map of which files should be 
added to or deleted from each node and then uses this map to make the corresponding shuffling. 
For real-time syncing, we can develop the metadata service further to constantly analyze file locations and access and redistribute files. 
Cross data center replication is a complex topic, and you are unlikely to discuss this 
in deep detail during a system design interview, unless you are interviewing for roles 
that request such expertise. In this section, we discuss a possible design to update the 
file mappings in the metadata service and the files in the storage service. 


304
Chapter 13  Design a Content Distribution Network 
NOTE    Refer to sources like https://serverfault.com/questions/831790/how-to 
-manage-failover-in-zookeeper-across-datacenters-using-observers, https://
zookeeper.apache.org/doc/r3.5.9/zookeeperObservers.html, and https://
stackoverflow.com/questions/41737770/how-to-deploy-zookeeper-across 
-multiple-data-centers-and-failover for more information on how to configure 
cross data center replication on ZooKeeper. Refer to https://solr.apache.org/
guide/8_11/cross-data-center-replication-cdcr.html for a guide on how cross 
data center replication can be configured in Solr, a search platform that uses 
ZooKeeper to manage its nodes.
Let’s discuss an approach to write new file metadata to the metadata service and shuffle the files accordingly between the data centers (in the in-cluster approach) or hosts 
(in the out-cluster approach) of the storage service. Our approach will need to make 
requests to the storage service to transfer files between its hosts across various data 
centers. To prevent inconsistency between the metadata service and storage service in 
case of failed write requests, the metadata service should only update its file location 
metadata when it receives a success response from the storage service, indicating that 
the files are successfully written to their new locations. The storage service relies on its 
manager (in-cluster or out-cluster) to ensure consistency within its own nodes/hosts. 
This ensures the metadata service does not return file locations before the files have 
been successfully written to those locations.
Moreover, files should be deleted from their previous nodes only after they are successfully written to their new locations, so if file writes to the new locations fail, the files 
continue to exist at their old locations, and the metadata service can continue to return 
these old file locations when it receives requests for those files.
We can use a saga approach (refer to section 5.6). Figure 13.7 illustrates a choreography approach, while figure 13.8 illustrates an orchestration approach where the metadata service is the orchestrator. 
The steps in figure 13.7 are as follows:
1	 The shuffling job produces an event to the shuffling topic, which corresponds to 
moving a file from certain locations to others. This event may also contain information such as the recommended replication factor of this file, corresponding to 
the number of leader nodes that should contain this file. 
2	 The storage service consumes this event and writes the file to their new locations.
3	 The storage service produces an event to the metadata topic to request the metadata service to update its file location metadata.
4	 The metadata service consumes from the metadata topic and updates the file 
location metadata.
5	 The metadata service produces an event to the file deletion topic to request the 
storage service to delete the files from their old locations.
6	 The storage service consumes this event and deletes the file from its old locations.


	
305
Common operations 
1
Shuffling job
5
Metadata Service
3
Storage Service
2
Shuffling Topic
6
File Deletion Topic
4
Metadata Topic
Figure 13.7    A choreography saga to update the metadata service and storage service
Identify the transaction types
Which are the compensable transactions, pivot transaction, and retriable trans­actions?
All transactions before step 6 can be compensated. Step 6 is the pivot transaction 
because the file deletion is irreversible. It is the final step, so there are no retriable 
transactions.
That being said, we can implement file deletion as soft delete (mark data as deleted, but 
not actually delete it). We can periodically hard delete (delete data from our storage hardware with no intention to use or recover it again) data from our database. In this case, all 
the transactions are compensable, and there will be no pivot transaction. 
1
Shuffling
job
3
7
Metadata 
Service
5
Storage 
Service
2
Shuffling Topic
4
File Creation Topic
6
Response Topic
8
File Deletion Topic
Figure 13.8    An orchestration saga to update the metadata service and storage service
The steps in figure 13.8 are as follows: 
1	 This is the same step as step 1 of the choreography approach previously discussed.
2	 The metadata service consumes this event.
3	 The metadata service produces an event to the file creation topic to request the 
storage service to create the file at the new locations.
4	 The storage service consumes this event and writes the files to their new locations.


306
Chapter 13  Design a Content Distribution Network 
5	 The storage service produces an event to the response topic to inform the metadata service that the file writes were successfully completed.
6	 The metadata service consumes this event.
7	 The metadata service produces an event to the file deletion topic to request the 
storage service to delete the file from its old locations.
8	 The storage service consumes this event and deletes the file from its old locations.
13.7	 Cache invalidation
As a CDN is for static files, cache invalidation is much less of a concern. We can fingerprint the files as discussed in section 4.11.1. We discussed various caching strategies 
(section 4.8) and designing a system to monitor the cache for stale files. This system 
will have to anticipate high traffic. 
13.8	 Logging, monitoring, and alerting 
In section 2.5, we discussed key concepts of logging, monitoring, and alerting that one 
must mention in an interview. Besides what was discussed in section 2.5, we should 
monitor and send alerts for the following: 
¡ Uploaders should be able to track the state of their files, whether the upload is in 
progress, completed, or failed.
¡ Log CDN misses and then monitors and triggers low-urgency alerts for them. 
¡ The frontend service can log the request rate for files. This can be done on a 
shared logging service. 
¡ Monitor for unusual or malicious activity. 
13.9	 Other possible discussions on downloading media files 
We may wish media files to be playable before they are fully downloaded. A solution 
is to divide the media file into smaller files, which can be downloaded in sequence 
and assembled into a media file that is a partial version of the original. Such a system 
requires a client-side media player that can do such assembly while playing the partial 
version. The details may be beyond the scope of a system design interview. It involves 
piercing together the files’ byte strings. 
As the sequence is important, we need metadata that indicates which files to download first. Our system splits a file into smaller files and assigns each small file with a 
sequence number. We also generate a metadata file that contains information on the 
order of the files and their total number. How can the files be efficiently downloaded in 
a particular sequence? We can also discuss other possible video streaming optimization 
strategies. 


	
307
Summary
Summary
¡ A CDN is a scalable and resilient distributed file storage service, which is a utility 
that is required by almost any web service that serves a large or geographically 
distributed user base. 
¡ A CDN is geographically distributed file storage service that allows each user to 
access a file from the data center that can serve them the fastest.
¡ A CDN’s advantages include lower latency, scalability, lower unit costs, higher 
throughput, and higher availability.
¡ A CDN’s disadvantages include additional complexity, high unit costs for low 
traffic and hidden costs, expensive migration, possible network restrictions, security and privacy concerns, and insufficient customization capabilities.
¡ A storage service can be separate from a metadata service that keeps track of 
which storage service hosts store particular files. The storage service’s implementation can focus on host provisioning and health.
¡ We can log file accesses and use this data to redistribute or replicate files across 
data centers to optimize latency and storage.
¡ CDNs can use third-party token-based authentication and authorization with key 
rotation for secure, reliable, and fine-grained access control. 
¡ A possible CDN high-level architecture can be a typical API gateway-metadata-storage/database architecture. We customize and scale each component to 
suit our specific functional and non-functional requirements. 
¡ Our distributed file storage service can be managed in-cluster or out-cluster. 
Each has its tradeoffs. 
¡ Frequently accessed files can be cached on the API gateway for faster reads.
¡ For encryption at rest, a CDN can use a secrets management service to manage 
encryption keys. 
¡ Large files should be uploaded with a multipart upload process that divides the 
file into chunks and manages the upload of each chunk separately. 
¡ To maintain low latency of downloads while managing costs, a periodic batch job 
can redistribute files across data centers and replicate them to the appropriate 
number of hosts.


308
14
Design a text 
messaging app
This chapter covers
¡ Designing an app for billions of clients to send 	
	 short messages 
¡ Considering approaches that trade off latency 	
	 vs. cost
¡ Designing for fault-tolerance
Let’s design a text messaging app, a system for 100K users to send messages to each 
other within seconds. Do not consider video or audio chat. Users send messages at 
an unpredictable rate, so our system should be able to handle these traffic surges. 
This is the first example system in this book that considers exactly-once delivery. 
Messages should not be lost, nor should they be sent more than once. 


	
309
Requirements
14.1	 Requirements
After some discussion, we determined the following functional requirements: 
¡ Real-time or eventually-consistent? Consider either case. 
¡ How many users may a chatroom have? A chatroom can contain between two to 
1,000 users. 
¡ Is there a character limit for a message? Let’s make it 1000 UTF-8 characters. At 
up to 32 bits/character, a message is up to 4 KB in size. 
¡ Notification is a platform-specific detail that we need not consider. Android, 
iOS, Chrome, and Windows apps each have their platform-specific notification 
library. 
¡ Delivery confirmation and read receipt. 
¡ Log the messages. Users can view and search up to 10 MB of their past messages. 
With one billion users, this works out to 10 PB of storage.
¡ Message body is private. We can discuss with the interviewer if we can view any 
message information, including information like knowing that a message was 
send from one user to another. However, error events such as failure to send a 
message should trigger an error that is visible to us. Such error logging and monitoring should preserve user privacy. End-to-end encryption will be ideal. 
¡ No need to consider user onboarding (i.e., the process of new users signing on to 
our messaging app). 
¡ No need to consider multiple chatrooms/channels for the same group of users. 
¡ Some chat apps have template messages that users can select to quickly create 
and send, such as “Good morning!” or “Can’t talk now, will reply later.” This can 
be a client-side feature that we do not consider here. 
¡ Some messaging apps allow users to see if their connections are online. We do 
not consider this. 
¡ We consider sending text only, not media like voice messages, photos, or videos. 
Non-functional requirements: 
¡ Scalability: 100K simultaneous users. Assume each user sends a 4 KB message 
every minute, which is a write rate of 400 MB/min. A user can have up to 1,000 
connections, and a message can be sent to up to 1,000 recipients, each of whom 
may have up to five devices. 
¡ High availability: Four nines availability. 
¡ High performance: 10-second P99 message delivery time. 
¡ Security and privacy: Require user authentication. Messages should be private. 
¡ Consistency: Strict ordering of messages is not necessary. If multiple users send 
messages to each other more or less simultaneously, these messages can appear 
in different orders to different users. 


310
Chapter 14  Design a text messaging app 
14.2	 Initial thoughts 
At first glance, this seems to be similar to the notification/alerting service we discussed 
in chapter 9. Looking closer, we see some differences, listed in table 14.1. We cannot 
naively reuse our notification/alerting service’s design, but we can use it as a starting 
point. We identify similar requirements and their corresponding design components 
and use the differences to increase or reduce our design’s complexity as appropriate. 
Table 14.1    Differences between our messaging app and our notification/alerting service
Messaging app
Notification/alerting service
All messages are equal priority and 
have a 10-second P99 delivery time.
Events can have different priority levels.
Messages are delivered from one client 
to others, all within a single channel on 
a single service. No need to consider 
other channels or services.
Multiple channels, such as email, SMS, 
automated phone calls, push notifications, or notifications within apps.
Only a manual trigger condition.
An event can be manually, programmatically, or periodically triggered.
No message templates. (Except perhaps message suggestions.)
Users can create and manage notification templates.
Due to end-to-end encryption, we cannot see the user’s messages, so there 
is less freedom to identify and deduplicate common elements into functions 
to reduce computational resource 
consumption. 
No end-to-end encryption. We have 
more freedom to create abstractions, 
such as a template service.
Users may request for old messages.
Most notifications only need to be sent 
once. 
Delivery confirmation and read receipt 
are part of the app. 
We may not have access to most notification channels, such as email, texting, 
push notifications, etc., so delivery and 
read confirmations may not be possible. 
14.3	 Initial high-level design
A user first selects the recipient (by name) of their message from a list of recipients. 
Next, they compose a message on a mobile, desktop, or browser app and then hit a 
Send button. The app first encrypts the message with the recipient’s public key and 
then makes a request to our messaging service to deliver the message. Our messaging 
service sends the message to the recipient. The recipient sends delivery confirmation 
and read receipt messages to the sender. This design has the following implications:
¡ Our app needs to store each recipient’s metadata, including names and public 
keys. 
¡ Our messaging service needs to maintain an open WebSocket connection to 
each recipient. 


	
311
Initial high-level design
¡ If there is more than one recipient, the sender needs to encrypt the message with 
each recipient’s public key. 
¡ Our messaging service needs to handle unpredictable traffic surges from many 
senders suddenly deciding to send messages within a short period. 
Referring to figure 14.1, we create separate services to serve different functional 
requirements and optimize for their different nonfunctional requirements. 
¡ Sender service: Receives messages from senders and immediately delivers them to 
recipients. It also records these messages in the message service, described next. 
¡ Message service: Senders can make requests to this service for their sent messages, 
while recipients can make requests to this service for both their received and 
unreceived messages. 
¡ Connection service: For storage and retrieval of users’ active and blocked connections, add other users to one’s contact list, block other users from sending messages. The connection service also stores connection metadata, such as names, 
avatars, and public keys. 
Figure 14.1 illustrates our high-level architecture with the relationships between our 
services. Users make requests to our services via an API gateway. Our sender service 
makes requests to our message service to record messages, including messages that 
failed to be delivered to recipients. It also makes requests to our connection service to 
check if a recipient has blocked the message sender. We discuss more details in subsequent sections. 
Sender
Message 
Service
Recipient
Sender
Service
Connection 
Service
Recipient
Recipient
API 
Gateway
Text Messaging Service
Figure 14.1    High-level architecture with the relationships between our services. A recipient can make 
requests to send delivery confirmations and read receipts, which are sent to the sender. Any user (sender 
or receiver) can request the message service for old or undelivered messages. 


312
Chapter 14  Design a text messaging app 
14.4	 Connection service
The connection service should provide the following endpoints:
¡ GET /connection/user/{userId}: GET all of a user’s connections and their metadata, including both active and blocked connections and active connections’ 
public keys. We may also add additional path or query parameters for filtering by 
connection groups or other categories. 
¡ POST /connection/user/{userId}/recipient/{recipientId}: New connection request 
from a user with userId to another user with recipientId. 
¡ PUT /connection/user/{userId}/recipient/{recipientId}/request/{accept}: Accept is a 
Boolean variable to accept or reject a connection request.  
¡ PUT /connection/user/{userId}/recipient/{recipientId}/block/{block}: Block is a Boolean variable to block or unblock a connection. 
¡ DELETE /connection/user/{userId}/recipient/{recipientId}: Delete a connection. 
14.4.1	 Making connections 
Users’ connections (including both active and blocked connections) should be stored 
on users’ devices (i.e., in their desktop or mobile apps) or in browser cookies or 
localStorage, so the connection service is a backup for this data in case a user changes 
devices or to synchronize this data across a user’s multiple devices. We do not expect 
heavy write traffic or a large amount of data, so we can implement it as a simple stateless backend service that stores data in a shared SQL service. 
14.4.2	 Sender blocking
We refer to a blocked connection as a blocked sender connection if a user has blocked 
this sender and a blocked recipient connection if a user is blocked by this recipient. In 
this section, we discuss an approach to blocking senders to maximize our messaging 
app’s performance and offline functionality. Referring to figure 14.2, we should implement blocking at every layer—that is, on the client (both the sender’s and recipient’s 
devices) and on the server. The rest of this section discusses some relevant considerations of this approach. 
Sender's app
blocks
Text Messaging 
Service
blocks
Recipient's app
blocks
Figure 14.2    Blocking should be implemented at every layer. When a blocked sender attempts to send 
a message, his device should block it. If this blocking fails and the message went to the server, the 
server should block it. If the server failed to block the message and it reached the recipient’s device, the 
recipient’s device should block it. 


	
313
Connection service
Reduce traffic
To reduce traffic to the server, blocked recipient connections should be stored on a 
user’s device, so the device can prevent the user from interacting with this recipient, 
and the server does not have to block such undesired interactions. Whether we wish to 
inform a user that another user has blocked them is a UX design decision that is up to us. 
Allow immediate blocking/unblocking 
When a user submits a request on the client to block a sender, the client should also 
send the relevant PUT request to block the sender. However, in case this particular 
endpoint is unavailable, the client can also record that it had blocked the sender, so it 
can hide any messages from the blocked sender and not display new message notifications. The client performs the analogous operations for unblocking a sender. These 
requests can be sent to a dead letter queue on the device and then sent to the server 
when that endpoint is available again. This is an example of graceful degradation. Limited functionality is maintained even when part of a system fails. 
This may mean that a user’s other devices may continue to receive messages from the 
intended blocked sender or may block messages from the intended unblocked sender.
Our connection service can keep track of which devices have synchronized their 
connections with our service. If a synchronized device sends a message to a recipient 
that has blocked the sender, this indicates a possible bug or malicious activity, and our 
connection service should trigger an alert to the developers. We discuss this further in 
section 14.6. 
Hacking the app
There is no practical way to prevent a sender from attempting to hack into the app to 
delete data about recipients that have blocked them. If we encrypt the blocked recipients on the sender’s device, the only secure way to store the key is on the server, which 
means that the sender’s device needs to query the server to view blocked recipients, 
and this defeats the purpose of storing this data on the sender’s device. This security 
concern is another reason to implement blocking at every layer. A detailed discussion 
of security and hacking is outside the scope of this book. 
Possible consistency problem
A user may send the same blocking or unblocking requests from multiple devices. At 
first, it seemed that this would not cause any problems because the PUT request is 
idempotent. However, inconsistency may result. Our graceful degradation mechanism 
had made this feature more complex. Referring to figure 14.3, if a user makes a blocking request and then an unblocking request on one device and also makes a blocking 
request on another device, it is unclear if the final state is to block or unblock the 
sender. As stated in other places in this book, attaching a device’s timestamp to the 
request to determine the requests’ order is not a solution because the devices’ clocks 
cannot be perfectly synchronized. 


314
Chapter 14  Design a text messaging app 
Device 0
Device 1
Connection
Service
Block request 
sent in this range
Block request
Unblock request sent in this range
Figure 14.3    If multiple 
devices can send requests 
to the connection service, 
inconsistency may result. If 
device 0 makes a blocking 
request followed by an 
unblocking request, while 
device 1 makes a blocking 
request after device 0, it is 
unclear if the user’s intention 
is to block or unblock. 
Allowing only one device to be connected at a time does not solve this problem 
because we allow these requests to be queued on a user’s device if the request to the 
server could not be made. Referring to figure 14.4, a user may connect to one device 
and make some requests that are queued, then connect to another device and make 
other requests that are successful, and then the first device may successfully make the 
requests to the server. 
Device 0
Log in
Requests sent 
in this range
Log out
Device 1
Connection
Service
Requests 
sent in this
range
Log out
Log in
Figure 14.4    Inconsistency 
may occur even if a device 
needs to be logged in for a 
request to be made because 
a request may be queued on 
a device, then sent to the 
connection service after the 
user logged out. 


	
315
Connection service
This general consistency problem is present when an app offers offline functionality 
that involves write operations. 
One solution is to ask the user to confirm the final state of each device. (This is the 
approach followed by this app written by the author: https://play.google.com/store/
apps/details?id=com.zhiyong.tingxie.) The steps may be as follows:
1	 A user does such a write operation on one device, which then updates the server.
2	 Another device synchronizes with the server and finds that its state is different 
from the server.
3	 The device presents a UI to the user that asks the user to confirm the final state. 
Another possible solution is to place limits on the write operations (and offline functionality) in a way to prevent inconsistency. In this case, when a device sends a block 
request, it should not be allowed to unblock until all other devices have synchronized 
with the server, and vice versa for unblock requests. 
A disadvantage of both approaches is that the UX is not as smooth. There is a 
tradeoff between usability and consistency. The UX will be better if a device can send 
arbitrary write operations regardless of its network connectivity, which is impossible to 
keep consistent. 
Public keys
When a device installs (or reinstalls) our app and starts our app for the first time, it 
generates a public-private key pair. It should store its public key in the connection service. The connection service should immediately update the user’s connections with 
the new public key via their WebSocket connections.
As a user may have up to 1,000 connections, each with five devices, a key change may 
require up to 5,000 requests, and some of these requests may fail because the recipients may be unavailable. Key changes will likely be rare events, so this should not cause 
unpredicted traffic surges, and the connection service should not need to use message 
brokering or Kafka. A connection who didn’t receive the update can receive it in a later 
GET request.
If a sender encrypts their message with an outdated public key, it will appear as gibberish after the recipient decrypts it. To prevent the recipient device from displaying 
such errors to the recipient user, the sender can hash the message with a cryptographic 
hash function such as SHA-2 and include this hash as part of the message. The recipient 
device can hash the decrypted message and display the decrypted message to the recipient user only if the hashes match. The sender service (discussed in detail in the next 
section) can provide a special message endpoint for a recipient to request the sender 
to resend the message. The recipient can include its public key, so the sender will not 
repeat this error and can also replace its outdated public key with the new one. 
One way to prevent such errors is that a public key change should not be effective 
immediately. The request to change a public key can include a grace period (such as 
seven days) during which both keys are valid. If a recipient receives a message encrypted 
with the old key, it can send a special message request to the Sender Service containing 
the new key, and the sender service requests the sender to update the latter’s key. 


316
Chapter 14  Design a text messaging app 
14.5	 Sender service
The sender service is optimized for scalability, availability, and performance of a single 
function, which is to receive messages from senders and deliver them to recipients 
in near real time. It should be made as simple as possible to optimize debuggability 
and maintainability of this critical function. If there are unpredicted traffic surges, it 
should be able to buffer these messages in a temporary storage, so it can process and 
deliver them when it has sufficient resources. 
Figure 14.5 is the high-level architecture of our sender service. It consists of two services with a Kafka topic between them. We name them the new message service and the 
message-sending service. This approach is similar to our notification service backend 
in section 9.3. However, we don’t use a metadata service here because the content is 
encrypted, so we cannot parse it to replace common components with IDs. 
Message Topic
New Message 
Service
Message-Sending 
Service
Sender Service
Sender
Receivers
Receivers
Receivers
Figure 14.5    High-level architecture of our sender service. A sender sends its message to the sender 
service via an API gateway (not illustrated). 
A message has the fields sender ID, a list of up to 1,000 recipient IDs, body string, and 
message sent status enum (the possible statuses are “message sent,” “message delivered,” and “message read”). 
14.5.1	 Sending a message
Sending a message occurs as follows. On the client, a user composes a message with 
a sender ID, recipient IDs, and a body string. Delivery confirmation and read receipt 
are initialized to false. The client encrypts the body and then sends the message to the 
sender service. 
The new message service receives a message request, produces it to the new message Kafka topic, then returns 200 success to the sender. A message request from one 
sender may contain up to 5,000 recipients, so it should be processed asynchronously 
this way. The new message service may also perform simple validations, such as whether 
the request was properly formatted, and return 400 error to invalid requests (as well as 
trigger the appropriate alerts to developers). 
Figure 14.6 illustrates the high-level architecture of our message-sending service. 
The message generator consumes from the new message Kafka topic and generates a 
separate message for each recipient. The host may fork a thread or maintain a thread 


	
317
Sender service
pool to generate a message. The host produces the message to a Kafka topic, which we 
call the recipient topic. The host may also write a checkpoint to a distributed in-memory database such as Redis. If the host fails while generating messages, its replacement 
can look up this checkpoint, so it doesn’t generate duplicate messages. 
New Message Topic
Message
Generator
Recipient Topic
Message 
Consumer 
Service
Host 
Assigner
Service
Message 
Service
Recipient
Message-Sending Service
Redis
Figure 14.6    High-level architecture of our message-sending service. The message consumer service 
may go through other services to send the message to the recipient, instead of directly sending it to the 
recipient as illustrated here. 
The message consumer service consumes from the recipient topic and then does the 
following steps. 
1	 Check if the sender should have been blocked. The message-sending service 
should store this data, instead of having to make a request to the connection 
service for every message. If a message has a blocked sender, it indicates that 
the client-side blocking mechanism has failed, possibly due to bugs or malicious 
activity. In this case, we should trigger an alert to developers. 
2	 Each message-sending service host has WebSocket connections with a number of 
recipients. We can experiment with this number to determine a good balance. 
Using a Kafka topic allows each host to serve a larger number of recipients, since 
it can consume from the Kafka topic only when it is ready to deliver a message. 
The service can use a distributed configuration service like ZooKeeper to assign 
hosts to devices. This ZooKeeper service can be behind another service that provides the appropriate API endpoints for returning the host that serves a particular recipient. We can call this the host assigner service. 
a	 The message-sending service host that is handling the current message can 
query the host assigner service for the appropriate host and then request that 
host to deliver the message to the recipient. Refer to section 14.6.3 for more 
details. 


318
Chapter 14  Design a text messaging app 
b	 In parallel, the message-sending service should also log the message to the 
message service, which is discussed further in the next section. Section 14.6 
has a more detailed discussion of the message-sending service. 
3	 The sender service sends the message to the recipient client. If the message cannot be delivered to the recipient client (most likely because the recipient device 
is off or doesn’t have internet connectivity), we can simply drop the message 
because it has already been recorded in the message service and can be retrieved 
by the device later. 
4	 The receiver can ensure that the message isn’t a duplicate and then display it to 
the user. The receiver app can also trigger a notification on the user’s device. 
5	 When the user reads the message, the app can send a read receipt message to the 
sender, which can be delivered in a similar manner. 
Steps 1–4 are illustrated in our sequence diagram in figure 14.7.
Recipient topic
Get assigned host.
Message
Consumer Service
Host Assigner
Service
Message Service
Recipient
POST /log
Response OK.
Send message.
Message sent.
Assigned host.
Message
request.
Get message
request.
par
Generate message. Verify blocked status.
Figure 14.7    Sequence diagram of consuming a message from the recipient Kafka topic and then 
sending it to our recipient
EXERCISE    How can these steps be performed with choreography saga or orchestration saga? Draw the relevant choreography and orchestration saga diagrams. 


	
319
Sender service
How can a device only retrieve its unreceived messages? One possibility we may think of 
is for the message service to record which of the user’s devices hasn’t received that message and use this to provide an endpoint for each device to retrieve only its unreceived 
messages. This approach assumes that the message service never needs to deliver the 
same message more than once to each device. Messages may be delivered but then lost. 
A user may delete their messages, but then wish to read them again. Our messaging 
app may have bugs, or the device may have problems, which cause the user to lose their 
messages. For such a use case, the Message Service API may expose a path or query 
parameter for devices to query for messages newer than their latest message. A device 
may receive duplicate messages, so it should check for duplicate messages. 
As mentioned earlier, the message service can have a retention period of a few weeks, 
after which it deletes the message. 
When a recipient device comes online, it can query the messaging service for new 
messages. This request will be directed to its host, which can query the metadata service 
for the new messages and return them to the recipient device. 
The message-sending service also provides an endpoint to update blocked/
unblocked senders. The connection service makes requests to the message-sending 
service to update blocked/unblocked senders. The connection service and ­message- 
sending ­service are separate to allow independent scaling; we expect more traffic on 
the latter than the former. 
14.5.2	 Other discussions
We may go through the following questions: 
¡ What happens if a user sends a backend host a message, but the backend host 
dies before it responds to the user that it has received it? 
If a backend host dies, the client will receive a 5xx error. We can implement the usual 
techniques for failed requests, such as exponential retry and backoff and a dead letter queue. The client can retry until a producer host successfully enqueues the message and returns a 200 response to the backend host which can likewise return a 200 
response to the sender. 
If a consumer host dies, we can implement an automatic or manual failover process 
such that another consumer host can consume the message from that Kafka partition 
and then update that partition’s offset: 
¡ What approach should be taken to solve message ordering? 
We can use consistent hashing, so that messages to a particular receiver are produced 
to a particular Kafka partition. This ensures that messages to a particular receiver are 
consumed and received in order. 
If a consistent hashing approach causes certain partitions to be overloaded with messages, we can increase the number of partitions and alter the consistent hashing algorithm to evenly spread the messages across the larger number of partitions. Another 
way is to use an in-memory database like Redis to store a receiver to partition mapping, 


320
Chapter 14  Design a text messaging app 
and adjust this mapping as needed to prevent any particular partition from becoming 
overburdened. 
Finally, the client can also ensure that messages arrive in order. If messages arrive out 
of order, it can trigger low-urgency alerts for further investigation. The client can also 
deduplicate messages: 
¡ What if messages were n:n/many:many instead of 1:1? 
We can limit the number of people in a chatroom. 
The architecture is scalable. It can scale up or down cost-efficiently. It employs shared 
services such as an API gateway and a shared Kafka service. Using Kafka allows it to handle traffic spikes without outages. 
Its main disadvantage is latency, particularly during traffic spikes. Using pull mechanisms such as queues allows eventual consistency, but they are unsuitable for real-time 
messaging. If we require real-time messaging, we cannot use a Kafka queue, but must 
instead decrease the ratio of hosts to devices and maintain a large cluster of hosts. 
14.6	 Message service
Our message service serves as a log of messages. Users may make requests to it for the 
following purposes:
¡ If a user just logged in to a new device or the device’s app storage was cleared, 
the device will need to download its past messages (both its sent and received 
messages).
¡ A message may be undeliverable. Possible reasons include being powered off, 
being disabled by the OS, or no network connectivity to our service. When the 
client is turned on, it can request the message service for messages that were sent 
to it while it was unavailable. 
For privacy and security, our system should use end-to-end encryption, so messages 
that pass through our system are encrypted. An additional advantage of end-to-end 
encryption is that messages are automatically encrypted both in transit and at rest. 
End-to-end encryption
We can understand end-to-end encryption in three simple steps: 
1	 A receiver generates a public-private key pair. 
2	 A sender encrypts a message with the receiver’s public key and then sends the 
receiver the message. 
3	 A receiver decrypts a message with their private key. 
After the client successfully receives the messages, the message service can have a 
retention period of a few weeks, after which it deletes the messages to save storage and 
for better privacy and security. This deletion prevents hackers from exploiting possible 


	
321
Message-sending service
security flaws in our service to obtain message contents. It limits the amount of data 
that hackers can steal and decrypt from our system should they manage to steal private 
keys from users’ devices. 
However, a user may have multiple devices running this messaging app. What if we 
want the message to be delivered to all devices? 
One way is to retain the messages in the undelivered message service and perhaps 
have a periodic batch job to delete data from the dead letter queue older than a set age. 
Another way is to allow a user to log in to only one phone at any time and provide a 
desktop app that can send and receive messages through the user’s phone. If the user 
logs in through another phone, they will not see their old messages from their previous 
phone. We can provide a feature that lets users backup their data to a cloud storage service (such as Google Drive or Microsoft OneDrive) so they can download it to another 
phone. 
Our message service expects high write traffic and low read traffic, which is an ideal 
use case for Cassandra. The architecture of our message service can be a stateless backend service and a shared Cassandra service. 
14.7	 Message-sending service
Section 14.5 discussed the sender service, which contains a new message service to 
filter out invalid messages and then buffer the messages in a Kafka topic. The bulk of 
the processing and the message delivery is carried out by the message-sending service, 
which we discuss in detail in this section. 
14.7.1	 Introduction
The sender service cannot simply send messages to the receiver without the latter first 
initiating a session with the former because the receiver devices are not servers. It is 
generally infeasible for user’s devices to be servers for reasons including the following:
¡ Security: Nefarious parties can send malicious programs to devices, such as hijacking them for DDoS attacks. 
¡ Increased network traffic to devices: Devices will be able to receive network traffic 
from others without first initiating a connection. This may cause their owners to 
incur excessive fees for this increased traffic. 
¡ Power consumption: If every app required the device to be a server, the increased 
power consumption will considerably reduce battery life. 
We can use a P2P protocol like BitTorrent, but it comes with the tradeoffs discussed 
earlier. We will not discuss this further. 
The requirement for devices to initiate connections means that our messaging service must constantly maintain a large number of connections, one for each client. We 
require a large cluster of hosts, which defeats the purpose of using a message queue. 


322
Chapter 14  Design a text messaging app 
Using WebSocket will also not help us because open WebSocket connections also consume host memory. 
The consumer cluster may have thousands of hosts to serve up to 100K simultaneous 
receivers/users. This means that each backend host must maintain open WebSocket 
connections with a number of users, as shown in figure 14.1. This statefulness is inevitable. We will need a distributed coordination service such as ZooKeeper to assign hosts 
to users. If a host goes down, ZooKeeper should detect this and provision a replacement 
host. 
Let’s consider a failover procedure when a message-sending service host dies. A 
host should emit heartbeats to its devices. If the host dies, its devices can request our 
message-­sending service for new WebSocket connections. Our container orchestration 
system (such as Kubernetes) should provision a new host, use ZooKeeper to determine 
its devices, and open WebSocket connections with these devices. 
Before the old host died, it may have successfully delivered the message to some but 
not all the recipients. How can the new host avoid redelivering the same message and 
cause duplicates? 
One way is to do checkpointing after each message. We can use an in-memory database such as Redis and partition the Redis cluster for strong consistency. The host can 
write to Redis each time after a message is successfully delivered to a recipient. The host 
also reads from Redis before delivering a message, so the host will not deliver duplicate 
messages. 
Another way is to simply resend the messages to all recipients and rely on the recipient’s devices to deduplicate the message. 
A third way is for the sender to resend the message if it does not receive an acknowledgment after a few minutes. This message may be processed and delivered by another 
consumer host. If this problem persists, it can trigger an alert to a shared monitoring 
and alerting service to alert developers of this problem. 
14.7.2	 High-level architecture 
Figure 14.8 shows the high-level architecture of the message-sending service. The main 
components are:
1	 The messaging cluster. This is a large cluster of hosts, each of which is assigned to 
a number of devices. Each individual device can be assigned an ID. 
2	 The host assigner service. This is a backend service that uses a ZooKeeper service 
to maintain a mapping of device IDs to hosts. Our cluster management system 
such as Kubernetes may also use the ZooKeeper service. During failover, Kubernetes updates the ZooKeeper service to remove the record of the old host and 
add records concerning any newly-provisioned hosts. 
3	 The connection service, discussed earlier in this chapter. 
4	 The message service, which was illustrated in figure 14.6. Every message that is 
received or sent to a device is also logged in the message service. 


	
323
Message-sending service
Backend
Messaging 
Cluster
Host 
Assigner
Connection
Services
Host 0
Host 1
Host n
Message 
Service
Message Topic
Message-Sending Service
ZooKeeper
Figure 14.8    High-level architecture of the message-sending service that assigns clients to dedicated 
hosts. Message backup is not illustrated. 
Every client is connected to our sender service via WebSocket, so hosts can send messages to client with near real-time latency. This means that we need a sizable number of hosts in the messaging cluster. Certain engineering teams have managed to 
establish millions of concurrent connections on a single host (https://migratorydata 
.com/2013/10/10/scaling-to-12-million-concurrent-connections-how-migratorydata 
-did-it/). Every host will also need to store its connections’ public keys. Our messaging 
service needs an endpoint for its connections to send their hosts’ the formers’ new 
public keys as necessary. 
However, this does not mean that a single host can simultaneously process messages 
to and from millions of clients. Tradeoffs must be made. Messages that can be delivered 
in a few seconds have to be small, limited to a few hundred characters of text. We can 
create a separate messaging service with its own host cluster for handling files such as 
photos and videos and scale this service independently of the messaging service that 
handles text. During traffic spikes, users can continue to send messages to each other 
with a few seconds of latency, but sending a file may take minutes. 
Each host may store messages up to a few days old, periodically deleting old messages 
from memory. Referring to figure 14.9, when a host receives a message, it may store the 
message in its memory, while forking a thread to produce the message to a Kafka queue. 
A consumer cluster can consume from the queue and write the message to a shared 
Redis service. (Redis has fast writes, but we can still use Kafka to buffer writes for higher 


324
Chapter 14  Design a text messaging app 
fault-tolerance.) When a client requests old messages, this request is passed through 
the backend to its host, and the host reads these old messages from the shared Redis 
service. This overall approach prioritizes reads over writes, so read requests can have 
low latency. Moreover, since write traffic will be much greater than read traffic, using a 
Kafka queue ensures that traffic spikes do not overwhelm the Redis service. 
Kafka queue
Redis
DB
Messaging
Cluster
Consumer
cluster
Writes
Reads
Figure 14.9    Interaction between the messaging cluster and Redis database. We can use a Kafka queue 
to buffer reads for higher fault-tolerance. 
The host assigner service can contain the mapping of client/chatroom IDs to hosts, 
keeping this mapping in a Redis cache. We can use consistent hashing, round robin, 
or weighted round robin to assign IDs to hosts, but this may quickly lead to a hot shard 
problem (certain hosts process a disproportionate load). The metadata service can 
contain information on the traffic of each host, so the host assigner service can use 
this information to decide which host to assign a client or chatroom to, to avoid the 
hot shard problem (certain hosts process a disproportionate load). We can balance 
the hosts such that each host can serve the same proportion of clients that have heavy 
traffic and clients with light traffic. 
The metadata service can also contain information on each user’s devices. 
A host can log its request activity (i.e., messaging processing activity) to a logging service, which may store it in HDFS. We can run a periodic batch job to rebalance hosts by 
reassigning clients and hosts and updating the metadata service. To improve the load 
rebalancing further, we can consider using more sophisticated statistical approaches 
such as machine learning. 
14.7.3	 Steps in sending a message 
We can now discuss step 3a in section 14.5.1 in more detail. When the backend service 
sends a message to another individual device or to a chatroom, the following steps can 
occur separately for the text and file contents of that message: 
1	 The backend host makes a request to the host assigner service, which does a 
lookup to ZooKeeper to determine which host serves the recipient individual 
client or chatroom. If there is no host assigned yet, ZooKeeper can assign a host. 
2	 The backend host sends the message to those hosts, which we refer to as recipient 
hosts. 


	
325
Message-sending service
14.7.4	 Some questions 
We may expect questions from the interviewer about statefulness. This design breaks 
the tenets of cloud native, which extols eventual consistency. We can discuss that this 
is unsuitable for this use case of a text messaging app, particularly for group chats. 
Cloud native makes certain tradeoffs, like higher write latency and eventual consistency for low read latency, higher availability, etc., which may not be fully applicable 
to our requirements of low write latency and strong consistency. Some other questions 
that may be discussed are as follows: 
¡ What happens if a server dies before it delivers the message to the receiver or the “sent” notification to a sender? We have discussed how to handle the situation where any of 
a receiver’s devices are offline. How do we ensure that “sent” notifications are 
delivered to a sender? One approach is for the client and recipient hosts to store 
recent “message sent” events. We can use Cassandra for its fast writes. If a sender 
did not receive a response after some time, it can query our messaging service 
to determine if the message was sent. The client or recipient host can return a 
successful response to the sender. Another approach is to treat a “sent” notification as a separate message. A recipient host can send a “sent” notification to the 
sender device. 
¡ What approach should be taken to solve message ordering? Each message has a timestamp from the sender client. It may be possible that later messages may be successfully processed and delivered before earlier messages. If a recipient device 
displays messages in order, and a user is viewing their device, earlier messages can 
suddenly appear before later ones, which may confuse the user. A solution is for 
an earlier message to be discarded if a later message has already been delivered 
to a recipient’s device. When a recipient client receives a message, it can determine if there are any messages with later timestamps, and if so, return a 422 error 
with a suitable error message. The error can propagate to the sender’s device. 
The user who sent the message can decide to send the message again with the 
knowledge that it will appear after a later message that was successfully delivered.
¡ What if messages were n:n/many:many instead of 1:1? We will limit the number of 
people in a chatroom. 
14.7.5	 Improving availability 
In the high-level architecture in figure 14.8, each client is assigned to a single host. 
Even if there is a monitoring service that receives heartbeats from hosts, it will take at 
least tens of seconds to recover from a host failure. The host assigner needs to execute 
a complicated algorithm to redistribute clients across hosts. 
We can improve availability by having a pool of hosts on standby that do not usually 
serve clients, but only send heartbeats. When a host fails, the host assigner can immediately assign all its clients to a standby host. This will reduce the downtime to seconds, 
which we can discuss with the interviewer whether this is acceptable. 


326
Chapter 14  Design a text messaging app 
A design that minimizes downtime is to create mini clusters. Assign one or two secondary hosts to each host. We can call the latter the primary host. This primary host will 
constantly forward all its requests to its secondary hosts, ensuring that the secondary 
hosts are up to date with the primary host and are always ready to take over as primary 
host. When a primary host fails, failover to a secondary host can happen immediately. 
We can use Terraform to define this infrastructure. Define a Kubernetes cluster of 3 
pods. Each pod has one node. Overall, this approach may be too costly and complex. 
14.8	 Search 
Each user can only search on their own messages. We may implement search-to-search 
directly in text messages, and not build a reverse index on each client, avoiding the 
costs of design, implementation, and maintenance of a reverse index. The storage size 
of an average client’s messages will probably be far less than 1 GB (excluding media 
files). It is straightforward to load these messages into memory and search them. 
We may search on media file names, but not on the content of the files themselves. 
Search on byte strings is outside the scope of this book. 
14.9	 Logging, monitoring, and alerting 
In section 2.5, we discussed key concepts of logging, monitoring, and alerting that one 
must mention in an interview. Besides what was discussed in section 2.5, we should log 
the following:
¡ Log requests between services, such as the API gateway to the backend service. 
¡ Log message sent events. To preserve user privacy, we can log certain details but 
not others. 
¡ For user privacy, never log the contents of a message, including all its fields (i.e., 
sender, receiver, body, delivery confirmation, and read receipt). 
¡ Log if a message was sent within a data center or from one data center to another.
¡ Log error events, such as errors in sending messages, delivery confirmation 
events, and read receipt events. 
Besides what was discussed in section 2.5, we should monitor and send alerts for the 
following: 
¡ As usual, we monitor errors and timeouts. We monitor utilization of various services for scaling decisions. We monitor the storage consumption of the Undelivered Message Service. 
¡ A combination of no errors on the backend service and a consistently small storage utilization in the undelivered message service indicates that we may investigate decreasing the sender service cluster size. 
¡ We also monitor for fraud and anomalous situations, such as a client sending a 
high rate of messages. Programmatic sending is not allowed. Consider placing 
a rate limiter in front of the API gateway or backend service. Block such clients 
completely from sending or receiving messages while we investigate the problem. 


	
327
Other possible discussion topics 
14.10	Other possible discussion topics 
Here are some other possible discussion topics for this system: 
¡ For one user to send messages to another, the former must first request the latter 
for permission. The latter may accept or block. The latter may change their mind 
and grant permission after blocking.
¡ A user can block another user at any time. The latter cannot select the former to 
send messages to. These users cannot be in the same chatroom. Blocking a user 
will remove oneself from any chatroom containing that user.
¡ What about logging in from a different device? We should only allow one device 
to log in at a time.
¡ Our system does not ensure that messages are received in the order they were 
sent. Moreover, if a chatroom has multiple participants who send messages close 
in time, the other participants may not receive the messages in order. The messages may arrive in different orders for various participants. How do we design a 
system that ensures that messages are displayed in order? What assumptions do 
we make? If participant A sends a message while their device is not connected 
to the internet, and other participants connected to the internet send messages 
shortly after, what order should the messages be displayed on others’ devices, 
and what order should they appear on participant A’s device? 
¡ How may we expand our system to support file attachments or audio and video 
chat? We can briefly discuss the new components and services. 
¡ We did not discuss message deletion. A typical messaging app may provide users 
the ability to delete messages, after which it should not receive them again. We 
should allow a user to delete messages even when their device is offline, and these 
deletes should be synchronized with the server. This synchronization mechanism 
can be a point for further discussion. 
¡ We can further discuss the mechanism to block or unblock users in greater detail. 
¡ What are the possible security and privacy risks with our current design and possible solutions? 
¡ How can our system support synchronization across a user’s multiple devices? 
¡ What are the possible race conditions when users add or remove other users 
to a chat? What if silent errors occur? How can our service detect and resolve 
inconsistencies? 
¡ We did not discuss messaging systems based on peer-to-peer (P2P) protocols like 
Skype or BitTorrent. Since a client has a dynamic rather than static IP address 
(static IP address is a paid service to the client’s internet service provider), the client can run a daemon that updates our service whenever its IP address changes. 
What are some possible complications? 
¡ To reduce computational resources and costs, a sender can compress its message 
before encrypting and sending it. The recipients can uncompress the message 
after they receive and decrypt it. 


328
Chapter 14  Design a text messaging app 
¡ Discuss a system design for user onboarding. How can a new user join our messaging app? How may a new user add or invite contacts? A user can manually type 
in contacts or add contacts using Bluetooth or QR codes. Or our mobile app can 
access the phone’s contact list, which will require the corresponding Android or 
iOS permissions. Users may invite new users by sending them a URL to download 
or sign on to our app. 
¡ Our architecture is a centralized approach. Every message needs to go through 
our backend. We can discuss decentralized approaches, such as P2P architecture, 
where every device is a server and can receive requests from other devices. 
Summary
¡ The main discussion of a simple text messaging app system design is about how to 
route large numbers of messages between a large number of clients.
¡ A chat system is similar to a notification/alerting service. Both services send messages to large numbers of recipients.
¡ A scalable and cost-efficient technique to handle traffic spikes is to use a message 
queue. However, latency will suffer during traffic spikes.
¡ We can decrease latency by assigning fewer users to a host, with the tradeoff of 
higher costs. 
¡ Either solution must handle host failures and reassign a host’s users to other 
hosts.
¡ A recipient’s device may be unavailable, so provide a GET endpoint to retrieve 
messages. 
¡ We should log requests between services and the details of message sent events 
and error events.
¡ We can monitor usage metrics to adjust cluster size and monitor for fraud.


329
15
Design Airbnb
This chapter covers
¡ Designing a reservation system
¡ Designing systems for operations staff to  
	 manage items and reservations
¡ Scoping a complex system
The question is to design a service for landlords to rent rooms for short-term stays 
to travelers. This may be both a coding and system design question. A coding discussion will be in the form of coding and object-oriented programming (OOP) solution of multiple classes. In this chapter, we assume this question can be applied to 
reservation systems in general, such as 
¡ Movie tickets 
¡ Air tickets 
¡ Parking lots 
¡ Taxis or ridesharing, though this has different non-functional requirements 
and different system design. 


330
Chapter 15  Design Airbnb
15.1	 Requirements
Before we discuss requirements, we can discuss the kind of system that we are designing. Airbnb is: 
1	 A reservation app, so there is a type of user who makes reservations on finite 
items. Airbnb calls them “guests.” There is also a type of user who creates listings 
of these items. Airbnb calls them “hosts.” 
2	 A marketplace app. It matches people who sell products and services to people 
who buy them. Airbnb matches hosts and guests. 
3	 It also handles payments and collects commissions. This means there are internal users who do customer support and operations (commonly abbreviated as 
“ops”), to mediate disputes and monitor and react to fraud. This distinguishes 
Airbnb from simpler apps like Craigslist. The majority of employees in companies like Airbnb are customer support and operations. 
At this point, we may clarify with the interviewer whether the scope of the interview is 
limited to hosts and guests or includes the other types of users. In this chapter, we discuss hosts, guests, operations, and analytics. 
A host’s use cases include the following. This list can be very long, so we will limit our 
discussion to the following use cases.
¡ Onboarding and updates to add, update, and delete listings. Updates may 
include small tasks like changing listing photos. There may be much intricate 
business logic. For example, a listing may have a minimum and/or maximum 
booking duration, and pricing may vary by day of week or other criteria. The 
app may display pricing recommendations. Listings may be subject to local regulations. For example, San Francisco’s short-term rental law limits rentals where 
the host is not present in the unit to a maximum of 90 days per year. Certain 
listing changes may also require approval from operations staff before they are 
published. 
¡ Handle bookings—for example accept or reject booking requests: 
–	 A host may be able to view a guest’s ratings and reviews by other hosts, before 
accepting or rejecting the guest’s booking request. 
–	 Airbnb may provide additional options such as automated acceptances under 
certain host-specified criteria, such as guests with a high average rating. 
–	 Cancel a booking after accepting it. This may trigger monetary penalties or 
suspension listing privileges. The exact rules may be complicated. 
¡ Communicate with guests, such as via in-app messaging. 
¡ Post a rating and review of a guest and view the guest’s rating and review. 
¡ Receive payment from the guest (minus Airbnb’s commission). 
¡ Receive tax filing documents. 
¡ Analytics, such as viewing earnings, ratings, and review contents over time. 


	
331
Requirements
¡ Communicate with operations staff, including requests for mediation (such as 
requesting guests to pay for damages) or reporting fraud. 
A guest’s use cases include the following: 
¡ Search and view listings. 
¡ Submit a booking request and payment and check the statuses of booking 
requests. 
¡ Communicate with hosts. 
¡ Post a rating and review of a listing and view the host’s rating and review. 
¡ Communicate with operations staff, analogous to hosts. 
Ops’ use cases include
¡ Reviewing listing requests and removing inappropriate listings.
¡ Communicating with customers for purposes such as dispute mediation, offering 
alternative listings, and sending refunds. 
We will not discuss payments in detail because payments are complex. A payment solution must consider numerous currencies and regulations (including taxes) that differ 
by country, state, city, and other levels of government and are different for various 
products and services. We may impose different transaction fees by payment type (e.g., 
a maximum transaction amount for checks or a discount for payments made via gift 
cards to encourage the purchase of gift cards). The mechanisms and regulations on 
refunds differ by payment type, product, country, customer, and numerous other factors. There are hundreds or thousands of ways to accept payments, such as 
¡ Cash. 
¡ Various debit and credit card processors like MasterCard, Visa, and many others. 
Each has their own API. 
¡ Online payment processors like PayPal or Alipay. 
¡ Check/cheque. 
¡ Store credit.
¡ Payment cards or gift cards that may be specific to certain combinations of companies and countries. 
¡ Cryptocurrency. 
Going back to our discussion on requirements, after approximately 5–10 minutes of 
rapid discussion and scribbling, we clarify the following functional requirements: 
¡ A host may list a room. Assume a room is for one person. Room properties are 
city and price. The host may provide up to 10 photos and a 25 MB video for a 
room. 
¡ A guest may filter rooms by city, check-in, and check-out date. 


332
Chapter 15  Design Airbnb
¡ A guest may book a room with a check-in and check-out date. Host approval for 
booking is not required. 
¡ A host or guest may cancel a booking at any time before it begins. 
¡ A host or guest may view their list of bookings. 
¡ A guest can have only one room booked for any particular date. 
¡ Rooms cannot be double-booked. 
¡ For simplicity, unlike the actual Airbnb, we exclude the following features: 
–	 Let a host manually accept or reject booking requests. 
–	 Cancel a booking (by the guest or host) after it is made is out of scope. 
–	 We can briefly discuss notifications (such as push or email) to guests and hosts 
but will not go into depth. 
–	 Messaging between users, such as between guests and hosts and between ops 
and guests/hosts. 
The following are outside the scope of this interview. It is good to mention these possible functional requirements to demonstrate your critical thinking and attention to 
detail. 
¡ Other fine details of a place, such as: 
–	 Exact address. Only a city string is necessary. Ignore other location details like 
state and country. 
–	 We assume every listing only permits one guest. 
–	 Whole place vs. private room vs. shared room. 
–	 Details of amenities, such as private versus shared bathrooms or kitchen 
details. 
–	 Child-friendly. 
–	 Pet-friendly.
¡ Analytics.
¡ Airbnb may provide hosts with pricing recommendations. A listing may set a 
minimum and maximum price/night, and Airbnb may vary the price within this 
range. 
¡ Additional pricing options and properties, such as cleaning fees and other fees, 
different prices on peak dates (e.g., weekends and holidays) or taxes. 
¡ Payments or refunds, including cancellation penalties. 
¡ Customer support, including dispute mediation. A good clarifying question is 
whether we need to discuss how ops reviews listing requests. We can also ask if 
the customer support that is out of scope refers to just the booking process or 
also includes customer support during the listing process. We can clarify that the 
term “customer” refers to both hosts and guests. In this interview, we assume that 
the interviewer may request to briefly discuss listing reviews by ops. 


	
333
Design decisions 
¡ Insurance. 
¡ Chat or other communication between any parties, such as host and guest. This 
is out of scope because it is a messaging service or notifications service (which we 
discussed in other chapters) and not a reservation service. 
¡ Signup and login. 
¡ Compensation of hosts and guests for outages. 
¡ User reviews, such as a guest reviewing their stay or a host reviewing their guest’s 
behavior. 
If we need to discuss API endpoints for listing and booking rooms, they can be as 
follows: 
¡ findRooms(cityId, checkInDate, checkOutDate) 
¡ bookRoom(userId, roomId, checkInDate, checkOutDate) 
¡ cancelBooking(bookingId) 
¡ viewBookings(hostId) 
¡ viewBookings(guestId) 
Our non-functional requirements are as follows: 
¡ Scalable to 1 billion rooms or 100 million daily bookings. Past booking data can 
be deleted. No programmatically generated user data. 
¡ Strong consistency for bookings, or more precisely listing availability, so there 
will be no double bookings or bookings on unavailable dates in general. Eventual 
consistency for other listing information such as description or photos may be 
acceptable. 
¡ High availability because there are monetary consequences of lost bookings. 
However, as we explain later in section 15.2.5, we cannot completely prevent lost 
bookings if we wish to prevent double bookings. 
¡ High performance is unnecessary. P99 of a few seconds is acceptable. 
¡ Typical security and privacy requirements. Authentication required. User data is 
private. Authorization is not a requirement for the functionalities in this interview’s scope. 
15.2	 Design decisions 
As we discuss the design for listing and booking rooms, we soon come across a couple 
of questions. 
1	 Should we replicate rooms to multiple data centers? 
2	 How should the data model represent room availability? 


334
Chapter 15  Design Airbnb
15.2.1	 Replication 
Our Airbnb system is similar to Craigslist in that the products are localized. A search 
can be only done on one city at a time. We can take advantage of this to allocate a data 
center host to a city with many listings or to multiple cities that have fewer listings. 
Because write performance is not critical, we can use single-leader replication. To minimize read latency, the secondary leader and the followers can be geographically spread 
out across data centers. We can use a metadata service to contain a mapping of city to 
leader and follower host IP addresses, for our service to look up the geographically 
closest follower host to fetch the rooms of any particular city or to write to the leader 
host corresponding to that city. This mapping will be tiny in size and only modified by 
admins infrequently, so we can simply replicate it on all data centers, and admins can 
manually ensure data consistency when updating the mapping. 
We can use a CDN to store the room photos and videos, and as usual other static content like JavaScript and CSS. 
Contrary to usual practice, we may choose not to use an in-memory cache. In search 
results, we only display available rooms. If a room is highly desirable, it will soon be 
reserved and no longer displayed in searches. If a room keeps being displayed in 
searches, it is likely to be undesirable, and we may choose not to incur the costs and 
additional complexity of providing a cache. Another way of stating this is that cache 
freshness is difficult to maintain, and the cached data quickly becomes stale. 
As always, these decisions are debatable, and we should be able to discuss their 
tradeoffs. 
15.2.2	 Data models for room availability 
We should quickly brainstorm various ways to represent room availability in our data 
model and discuss their tradeoffs. In an interview, one must display the ability to evaluate multiple approaches and not just propose one approach: 
¡ (room_id, date, guest_id) table—This is conceptually simple, with the tradeoff 
of containing multiple rows that differ only by date. For example, if room 1 is 
booked by guest 1 for the whole of January, there will be 31 rows. 
¡ (room_id, guest_id, check_in, check_out) table—This is more compact. When a guest 
submits a search with a check-in and check-out date, we require an algorithm to 
determine if there are overlapping dates. Should we code this algorithm in the 
database query or in the backend? The former will be more difficult to maintain 
and test. But if backend hosts have to fetch this room availability data from the 
database, this incurs I/O costs. The code for both approaches can be asked in 
coding interviews. 
There are many possible database schemas. 


	
335
High-level architecture 
15.2.3	 Handling overlapping bookings 
If multiple users attempt to book the same room with overlapping dates, the first user’s 
booking should be granted, and our UI should inform the other users that this room is 
no longer available for the dates they selected and guide them through finding another 
available room. This may be a negative UX experience, so we may want to briefly brainstorm a couple of alternative approaches. You may suggest other possibilities. 
15.2.4	 Randomize search results 
We can randomize the order of the search results to reduce such occurrences, though 
that may interfere with personalization (such as recommender systems.) 
15.2.5	 Lock rooms during booking flow 
When a user clicks on a search result to view the details of a room and possibly submit 
a booking request, we can lock these dates for the room for a few minutes. During this 
time, searches by other users with overlapping dates will not return this room in the 
result list. If this room is locked after other users have already received their search 
results, clicking on the room’s details should present a notification of the lock and 
possibly its remaining duration if those users wish to try again, just in case that user did 
not book that room. 
This means that we will lose some bookings. We may decide that preventing double 
bookings is worth the tradeoff of losing bookings. This is a difference between Airbnb 
and hotels. A hotel can allow overbooking of its cheaper rooms because it can expect a 
few cancellations to occur. If the cheaper rooms are overbooked on a particular date, 
the hotel can upgrade the excess guests to more expensive rooms. Airbnb hosts cannot 
do this, so we cannot allow double bookings. 
Section 2.4.2 describes a mechanism to prevent concurrent update conflicts from 
multiple users from simultaneously updating a shared configuration.
15.3	 High-level architecture 
From the previous section’s requirements discussion, we draw our high-level architecture, shown in figure 15.1. Each service serves a group of related functional requirements. This allows us to develop and scale the services separately: 
¡ Booking service—For guests to make bookings. This service is our direct revenue 
source and has the most stringent non-functional requirements for availability 
and latency. Higher latency directly translates to lower revenue. Downtime on 
this service has the most serious effect on revenue and reputation. However, 
strong consistency may be less important, and we can trade off consistency for 
availability and latency. 
¡ Listing service—For hosts to create and manage listings. It is important but less 
critical than the booking and listing services. It is a separate service because it 
has different functional and non-functional requirements than the booking and 
availability services, so it should not share resources with them. 


336
Chapter 15  Design Airbnb
¡ Availability service—The availability service keeps track of listing availability and 
is used by both the booking and listing services. The availability and latency 
requirements are as stringent as the booking service. Reads must be scalable, but 
writes are less frequent and may not require scalability. We discuss this further in 
section 15.8. 
¡ Approval service—Certain operations like adding new listings or updating certain 
listing information may require ops approval prior to publishing. We can design 
an approval service for these use cases. We name the service the “approval service” rather than the more ambiguous-sounding “review service.” 
¡ Recommender service—Provides personalized listing recommendations to guests. 
We can see it as an internal ads service. A detailed discussion is out of scope in 
the interview, but we can include it in the diagram and discuss it just for a short 
moment. 
¡ Regulations service—As discussed earlier, the listing service and booking service 
need to consider local regulations. The regulations service can provide an API 
to the listing service, so the latter can provide hosts with the appropriate UX 
for creating listings that comply with local regulations. The listing service and 
regulation service can be developed by separate teams, so each team member 
can concentrate on gaining domain expertise relevant to their respective service. 
Dealing with regulations may be initially outside the scope of an interview, but 
the interviewer may be interested to see how we handle it. 
¡ Other services: Collective label for certain services for internal uses like analytics, 
which are mostly outside the scope of this interview. 
API Gateway
Booking 
Service
Listing
Service
Client (web and
mobile apps)
CDN
Recommender
Service
Elasticsearch
Logging/Kafka
Availability 
Service
Payment 
Service
Metadata 
Service
Figure 15.1    High-level architecture. As usual, instead of an API gateway, we can use a service mesh in 
our listing and booking services. 


	
337
Create or update a listing 
15.4	 Functional partitioning 
We can employ functional partitioning by geographical region, similar to the approach 
discussed with Craigslist in section 7.9. Listings can be placed in a data center. We 
deploy our application into multiple data centers and route each user to the data center that serves their city. 
15.5	 Create or update a listing 
Creating a listing can be divided into two tasks. The first task is for the host to obtain 
their appropriate listing regulations. The second task is for the host to submit a listing request. In this chapter, we refer to both creating and updating listings as listing 
requests. 
Figure 15.2 is a sequence diagram of obtaining the appropriate regulations. The 
sequence is as follows:  
1	 The host is currently on the client (a webpage mobile app component) that provides a button to create a new listing. When the host clicks on the button, the app 
sends a request to the listing service that contains the user’s location. (The host’s 
location can be obtained by asking the host to manually provide it or by asking 
the host to grant permission to access their location.) 
2	 The listing service forwards their location to the regulation service (refer to section 15.10.1). The regulation service responds with the appropriate regulations. 
3	 The listing service returns the regulations to the client. The client may adjust the 
UX to accommodate the regulations. For example, if there is a rule that a booking must last at least 14 days, the client will immediately display an error to the 
host if they enter a minimum booking period of less than 14 days. 
:Listing Service
New Listing
Request regulations.
Regulations.
:Regulation Service
Regulations.
Figure 15.2    Sequence diagram of obtaining the appropriate listing regulations
Figure 15.3 is a sequence diagram of a simplified listing request. The host enters their 
listing information and submits it. This is sent as a POST request to the listing service. 
The listing service does the following: 


338
Chapter 15  Design Airbnb
1	 Validates the request body. 
2	 Writes to a SQL table for listings, which we can name the Listing table. New listings and certain updates need manual approval by the Ops staff. The Listing SQL 
table can contain a Boolean column named “Approved” that indicates if a listing 
has been approved by ops. 
3	 If Ops approval is required, it sends a POST request to the Approval service to 
notify Ops to review the listing. 
4	 Sends the client a 200 response. 
:Listing Service
dispatch
Validation
:SQL Service
Write new listing.
Response OK.
:Approval Service
Listing request
complete.
Response OK. Request received. 
Review request.
Figure 15.3    Sequence diagram of a simplified request to create or update a listing
Referring to figure 15.4, steps 2 and 3 can be done in parallel using CDC. All steps are 
idempotent. We can use INSERT IGNORE on SQL tables to prevent duplicate writes 
(https://stackoverflow.com/a/1361368/1045085). We can also use transaction log 
tailing, discussed in section 5.3.
Approval Service
SQL topic
Listing Service
SQL Service
SQL consumer
Approval Topic
Approval 
consumer
Figure 15.4    Using CDC for a distributed transaction to the SQL service and approval service
This is a simplified design. In a real implementation, the listing process may consist 
of multiple requests to the listing service. The form to create a listing may be divided 
into multiple parts, and a host may fill and submit each part separately, and each submission is a separate request. For example, adding photos to a listing may be done one 


	
339
Approval service 
at a time. A host may fill in a listing’s title, type, and description and submit it as one 
request and then fill in pricing details and submit it as another request, and so on. 
Another point to note is to allow a host to make additional updates to their listing 
request while it is pending review. Each update should UPDATE the corresponding 
listing table row. 
We will not discuss notifications in detail because the exact business logic for notifications may be intricate and often change. Notifications can be implemented as a batch 
ETL job that makes requests to the listing service and then requests a shared notifications service to send notifications. The batch job can query for incomplete listings then
¡ Notify hosts to remind them that they have not completed the listing process. 
¡ Notify ops of incomplete listings, so ops staff can contact hosts to encourage and 
guide them to complete the listing process. 
15.6	 Approval service 
The interviewer may be more interested in the booking process, so this discussion on 
the approval service may be brief. 
The approval service is an internal application with low traffic and can have a simple 
architecture. Referring to figure 15.5, the design consists of a client web application 
and a backend service, which makes requests to the listings service and a shared SQL 
service. We assume that manual approval is required for all requests; for example, we 
cannot automate any approvals or rejections. 
Client
Backend
Listings Service
SQL
Figure 15.5    High-level architecture of the approval service, for Ops personnel to review certain 
operations, such as adding or updating listings
The approval service provides a POST endpoint for the listing service to submit listing 
requests that require review. We can write these requests to a SQL table we call “listing_request,” which contains the following columns: 
¡ id—An ID. The primary key. 
¡ listing_id—The listing ID in the Listing table in the listing service. If both tables 
were in the same service, this would be a foreign key. 
¡ created_at—Timestamp that this listing request was created or updated. 


340
Chapter 15  Design Airbnb
¡ listing_hash—We may include this column as part of an additional mechanism to 
ensure that an Ops staff member does not submit an approval or rejection of a 
listing request that changed while they were reviewing it. 
¡ status—An enum of the listing request, which can be one of the values “none,” 
“assigned,” and “reviewed.” 
¡ last_accessed—Timestamp that this listing request was last fetched and returned to 
an Ops staff member. 
¡ review_code—An enum. May be simply “APPROVED” for approved listing requests. 
There may be multiple enums that correspond to categories of reasons to reject 
a listing request. Examples include VIOLATE_LOCAL_REGULATIONS, 
BANNED_HOST, ILLEGAL_CONTENT, SUSPICIOUS, FAIL_QUALITY_
STANDARDS, etc. 
¡ reviewer_id—The ID of the operations staff member who was assigned this listing 
request. 
¡ review_submitted_at—Timestamp that the Ops staff member submitted their 
approval or rejection. 
¡ review_notes—An Ops staff member may author some notes on why this listing 
request was approved or rejected. 
Assuming we have 10,000 Operations staff, and each staff member reviews up to 5000 
new or updated listings weekly, Ops will write 50 million rows weekly to the SQL table. 
If each row occupies 1 KB, the approval table will grow by 1 KB * 50M * 30 days = 1.5 
TB monthly. We can keep 1–2 months of data in the SQL table and run a periodic 
batch job to archive old data into object storage. 
We can also design endpoints and an SQL table for each ops staff to obtain and perform their assigned work/reviews. An Ops staff member can first make a GET request 
containing their ID to fetch a listing request from the listing_request table. To prevent 
multiple staff from being assigned the same listing request, the backend can run an 
SQL transaction with the following steps: 
1	 If a staff member has already been assigned a listing request, return this assigned 
request. SELECT a row with status “assigned” and with the staff member's ID as 
the reviewer_id. 
2	 If there is no assigned listing request, SELECT the row with the minimum created_at timestamp that has status “none”. This will be the assigned listing request. 
3	 UPDATE the status to “assigned,” and the reviewer_id to the ops staff member’s 
ID. 
The backend returns this listing request to the Ops staff, who will review it and approve 
or reject it. Figure 15.6 is a sequence diagram of a synchronous approval process. 
Approval or rejection is a POST request to the Approval, which triggers the following 
steps:


	
341
Approval service 
1	 UPDATE the row into the listing_request table. UPDATE the columns status, 
review_code, review_submitted_at, and review_notes. 
There is a possible race condition where a host may update their listing request 
while an Ops staff member is reviewing it, so the POST request should contain the 
listing hash that the approval service had earlier returned to the Ops staff member, and the backend should ensure this hash is identical to the present hash. If 
the hashes are different, return the updated listing request to the Ops staff member, who will need to repeat the review. 
We may try to identify this race condition by checking if listing_request.last_
accessed timestamp is more recent than listing_request.review_submitted_at. 
However, this technique is unreliable because the clocks of the various hosts that 
timestamp columns are not perfectly synchronized. Also, the time may have been 
changed for any multitude of reasons such as daylight savings, server restarts, the 
server clock may be periodically synchronized with a reference server, etc. In distributed systems, it is not possible to rely on clocks to ensure consistency (Martin 
Kleppmann,  Designing Data-Intensive Applications (O’Reilly, 2017)). 
Lamport clock and vector clock
Lamport clock (https://martinfowler.com/articles/patterns-of-distributed-systems/
lamport-clock.html) is a technique for ordering events in a distributed system. Vector 
clock is a more sophisticated technique. For more details, refer to chapter 11 of the book 
by George Coulouris, Jean Dollimore, Tim Kindberg, and Gordon Blair, Distributed Systems: Concepts and Design, Pearson, 2011.
2	 Send a PUT request to the Listing Service, which will UPDATE the listing_
request.status and listing_request.reviewed_at columns. Again, first SELECT the 
hash and verify that it is identical to the submitted hash. Wrap both SQL queries 
in a transaction. 
3	 Send a POST request to the Booking Service, so the booking service may begin 
showing this listing to guests. An alternative approach is described in figure 15.7. 
4	 The backend also requests a shared notification service (chapter 9) to notify the 
host of the approval or rejection. 
5	 Finally, the backend sends a 200 response to the client. These steps should be 
written in an idempotent manner, so any or all steps can be repeated if a host fails 
during any step. 
Discuss how this POST request can be idempotent in case it fails before all steps are 
completed and we must retry the same request. For example: 


342
Chapter 15  Design Airbnb
¡ The backend can query the notification service to check if a particular notification request has already been made, before making the notification request. 
¡ To prevent duplicate rows in the approval table, the SQL row insertion can use a 
“IF NOT EXISTS” operator. 
As we can see, this synchronous request involves requests to multiple services and may 
have long latency. A failed request to any service will introduce inconsistency. 
:Client
:Approval
Service
Approve.
2. Update
listing request.
Get listing
requests.
:Listing Service
:Notification
Service
1. Approve.
:Booking Service
Listing requests.
3. Show listing to guests.
4. Send notification
Response OK.
Response OK.
Response OK.
Response OK.
Figure 15.6    Sequence diagram of fetching listing requests followed by a synchronous approval of a 
listing request. The approval service can be a saga orchestrator.  
Should we use change data capture (CDC) instead? Figure 15.7 illustrates this asynchronous approach. In an approval request, the approval service produces to a Kafka 
queue and returns 200. A consumer consumes from the Kafka queue and makes the 
requests to all these other services. The rate of approvals is low, so the consumer can 
employ exponential backoff and retry to avoid rapidly polling the Kafka queue when 
the latter is empty, and poll only once per minute when the queue is empty. 


	
343
Approval service 
2. Produce.
1. Approval request.
3. Response OK.
Approval 
Service
Kafka queue
Consumer
Consumer
Listing
Service
Booking
Service
Notification
Service
4. Consume approval event.
5. Update services.
The notification service should notify the host only after the listing and booking services are updated, so it consumes from two Kafka topics, one corresponding to each 
service. When the notification service consumes an event from one topic corresponding to a particular listing approval event, it must wait for the event from the other 
service that corresponds to the same listing approval event, and then it can send the 
notification. So, the notification service needs a database to record these events. This 
database is not shown in figure 15.7. 
As an additional safeguard against silent errors that may cause inconsistency between 
the services, we can implement a batch ETL job to audit the three services. This job can 
trigger an alert to developers if it finds inconsistency. 
We use CDC rather than saga for this process because we do not expect any of the services to reject the request, so there will not be any required compensating transactions. 
The listing service and booking service have no reason to prevent the listing from going 
live, and the notification service has no reason not to send the user a notification. 
But what if a user cancels their account just before their listing is approved? We will 
need a CDC process to either deactivate or delete their listings and make requests to 
other services as appropriate. If the various services involved in the approval process of 
figure 15.6 receive the user deletion request just before the approval request, they can 
either record that the listing is invalid or delete the listing. Then the approval request 
will not cause the listing to become active. We should discuss with our interviewer on 
the tradeoffs of various approaches and other relevant concerns that come to mind. 
They will appreciate this attention to detail. 
Figure 15.7     
An asynchronous 
approach to approving 
a listing request, using 
change data capture. 
Since all requests are 
retriable, we do not need 
to use a saga.


344
Chapter 15  Design Airbnb
There may be other requested features. For example, a listing review may involve 
more than one Ops staff member. We can bring up these points and discuss them if the 
interviewer is interested. 
An Ops staff may specialize in reviewing listing requests of certain jurisdictions, so 
how may we assign their appropriate listing requests? Our application is already functionally partitioned by geographical region, so if a staff member can review listing 
requests of listings in a particular data center, nothing else is required in our design. 
Otherwise, we can discuss some possibilities: 
¡ A JOIN query between the listing_request table and the listing table to fetch listing requests with a particular country or city. Our listing_request table and listing 
table are in different services, so we will need a different solution: 
–	 Redesign our system. Combine the listing and approval services, so both tables 
are in the same service. 
–	 Handle the join logic in the application layer, which carries disadvantages 
such as I/O cost of data transfer between services. 
–	 Denormalize or duplicate the listing data, by adding a location column to listing_request table or duplicating the listing table in the approvals service. A 
listing’s physical location does not change, so there is low risk of inconsistency 
due to denormalization or duplication, though inconsistency can happen, 
such as from bugs or if the initially entered location was wrong then corrected. 
¡ A listing ID can contain a city ID, so one can determine the listing’s city by the 
listing ID. Our company can maintain a list of (ID, city), which can be accessed by 
any service. This list should be append-only so we will not need to do expensive 
and error-prone data migrations. 
As stated here, approved listings will be copied to the booking service. Because the 
booking service may have high traffic, this step may have the highest failure rate. As 
per our usual approaches, we can implement exponential backoff and retry or a dead 
letter queue. The traffic from our approval service to the booking service is negligible 
compared to traffic from guests, so we will not try to reduce the probability of booking 
service downtime by reducing traffic from the approval service. 
Last, we can also discuss automation of some approvals or rejections. We can define 
rules in a SQL table “Rules,” and a function can fetch these rules and apply them on 
the listing contents. We can also use machine learning; we can train machine-learning models in a machine-learning service, and place selected model IDs into the Rules 
table, so the function can send the listing contents along with the model IDs to the 
machine learning service, which will return approval, rejection, or inconclusive (i.e., 
requires manual review). The listing_request.reviewer_id can be a value like “AUTO-
MATED,” while the listing_request.review_code value of an inconclusive review can be 
“INCONCLUSIVE.” 


	
345
Booking service 
15.7	 Booking service 
The steps of a simplified booking/reservation process are as follows: 
1	 A guest submits a search query for the listing that matches the following and 
receives a list of available listings. Each listing in the result list may contain a 
thumbnail and some brief information. As discussed in the requirements section, 
other details are out of scope. 
–	 City 
–	 Check-in date 
–	 Check-out date 
2	 The guest may filter the results by price and other listing details. 
3	 The guest clicks on a listing to view more details, including high-resolution photos and videos if any. From here, the guest may go back to the result list. 
4	 The guest has decided on which listing to book. They submit a booking request 
and receive a confirmation or error. 
5	 If the guest receives a confirmation, they are then directed to make payment. 
6	 A guest may change their mind and submit a cancellation request. 
Similar to the listing service discussed earlier, we may choose to send notifications 
such as 
¡ Notify guests and hosts after a booking is successfully completed or canceled.
¡ If a guest filled in the details of a booking request but didn’t complete the booking request, remind them after some hours or days to complete the booking 
request. 
¡ Recommend listings to guests based on various factors like their past bookings, 
listings they have viewed, their other online activity, their demographic, etc. The 
listings can be selected by a recommender system. 
¡ Notifications regarding payments. Regarding payment, we may choose to escrow 
payments before the host accepts or request payment only after the host accepts. 
The notification logic will vary accordingly. 
Let’s quickly discuss scalability requirements. As discussed earlier, we can functionally 
partition listings by city. We can assume that we have up to one million listings in a particular city. We can make a generous overestimate of up to 10 million daily requests for 
search, filtering, and listing details. Even assuming that these 10 million requests are 
concentrated in a single hour of the day, this works out to less than 3,000 queries per 
second, which can be handled by a single or small number of hosts. Nonetheless, the 
architecture discussed in this section will be capable of handling much larger traffic. 


346
Chapter 15  Design Airbnb
Figure 15.8 is a high-level architecture of the booking service. All queries are processed by a backend service, which queries either the shared Elasticsearch or SQL services as appropriate. 
Client
Backend
Elasticsearch
service
SQL
Logging service
Availability
service
CDN
Figure 15.8    High-level architecture of the booking service
Search and filter requests are processed on the Elasticsearch service. The Elasticsearch 
service may also handle pagination (https://www.elastic.co/guide/en/elasticsearch/
reference/current/paginate-search-results.html), so it can save memory and CPU 
usage by returning only a small number of results at a time. Elasticsearch supports 
fuzzy search, which is useful to guests who misspell locations and addresses. 
A request to CRUD details of a listing is formatted into a SQL query using an ORM 
and made against the SQL service. Photos and videos are downloaded from the CDN. 
A booking request is forwarded to the availability service, which is discussed in detail in 
the next section. Write operations to the booking service’s SQL database are by 
1	 Booking requests. 
2	 The approval service as described in the previous section. The approval service 
makes infrequent updates to listing details. 
3	 Requests to cancel bookings and make the listings available again. This occurs if 
payments fail. 
Our SQL service used by this booking service can use the leader-follower architecture 
discussed in section 4.3.2. The infrequent writes are made to the leader host, which will 
replicate them to the follower hosts. The SQL service may contain a Booking table with 
the following columns: 


	
347
Booking service 
¡ id—A primary key ID assigned to a booking. 
¡ listing_id—The listing’s ID assigned by the Listing service. If this table was in the 
listing service, this column would be a foreign key. 
¡ guest_id—The ID of the guest who made the booking. 
¡ check_in—Check-in date. 
¡ check_out—Check-out date.
¡ timestamp—The time this row was inserted or updated. This column can be just 
for record-keeping. 
The other write operations in this process are to the availability service: 
1	 The booking or cancellation request will alter a listing’s availability on the relevant dates. 
2	 We may consider locking the listing for five minutes at step 3 in the booking 
process (request more of a listing’s details) because the guest may make a booking request. This means that the listing will not be shown to other guests who 
made search queries with dates that overlap the current guest’s. Conversely, we 
may unlock the listing early (before the five minutes are up) if the guest makes 
a search or filtering request, which indicates that they are unlikely to book this 
listing. 
The Elasticsearch index needs to be updated when a listing’s availability or details 
change. Adding or updating a listing requires write requests to both the SQL service 
and Elasticsearch service. As discussed in chapter 5, this can be handled as a distributed transaction to prevent inconsistency should failures occur during writes to either 
service. A booking request requires writes to the SQL services in both the booking service and availability service (discussed in the next section) and should also be handled 
as a distributed transaction. 
If the booking causes the listing to become ineligible for further listings, the booking 
service must update its own database to prevent further bookings and also update the 
Elasticsearch service so this listing stops appearing in searches. 
The Elasticsearch result may sort listings by decreasing guest ratings. The results may 
also be sorted by a machine learning experiment service. These considerations are out 
of scope.
Figure 15.9 is a sequence diagram of our simplified booking process. 


348
Chapter 15  Design Airbnb
:Client
:Elasticsearch
Search/filter
listings.
:Booking
Make
booking.
:Payment
Get listing details.
Booking request
:Availability
Listings.
Listing details.
Check
availability.
True
If booking confirmed, make payment.
Booking canceled.
Booking failed.
Booking confirmed.
False
Booking failed.
alt
alt
[Listing available]
[Listing unavailable]
[Payment successful.]
Payment confirmed.
[Payment failed.]
Cancel booking.
Figure 15.9    Sequence diagram of our simplified booking process. Many details are glossed over. 
Examples: Getting the listing details may involve a CDN. We don’t give hosts the option to manually 
accept or reject booking requests. Making payment will involve a large number of requests to multiple 
services. We did not illustrate requests to our notification service. 
Last, we may consider that many guests may search for listings and view the details of 
many listings before making a booking request, so we can consider splitting the search 
and view functions vs. the booking function into separate services, so they can scale 
separately. The service to search and view listings will receive more traffic and be allocated more resources than the service to make booking requests. 


	
349
Availability service 
15.8	 Availability service 
The availability service needs to avoid situations like the following: 
¡ Double bookings.
¡ A guest’s booking may not be visible to the host. 
¡ A host may mark certain dates as unavailable, but a guest may book those dates. 
¡ Our customer support department will be burdened by guest and host complaints from these poor experiences. 
The availability service provides the following endpoints: 
¡ Given a location ID, listing type ID, check-in date, and check-out date, GET available listings. 
¡ Lock a listing from a particular check-in date to check-out date for a few (e.g., 
five) minutes. 
¡ CRUD a reservation, from a particular check-in date to check-out date. 
Figure 15.10 is the high-level architecture of the availability service. It consists of a 
backend service, which makes requests to a shared SQL service. The shared SQL service has a leader-follower architecture, illustrated in figures 4.1 and 4.2. 
Backend service
Client
SQL
Figure 15.10    High-level architecture of the availability service
The SQL service can contain an availability table, which can have the following columns. There is no primary key: 
¡ listing_id—The listing’s ID assigned by the listing service. 
¡ date—The availability date. 
¡ booking_id—The booking/reservation ID assigned by the booking service when a 
booking is made. 
¡ available—A string field that functions as an enum. It indicates if the listing is 
available, locked, or booked. We may save space by deleting the row if this (listing_id, date) combination is not locked or booked. However, we aim to achieve 
high occupancy, so this space saving will be insignificant. Another disadvantage 
is that our SQL service should provision sufficient storage for all possible rows, so 
if we save space by not inserting rows unless required, we may not realize that we 
have insufficient storage provisioned until we have a high occupancy rate across 
our listings. 
¡ timestamp—The time this row was inserted or updated. 


350
Chapter 15  Design Airbnb
We discussed a listing lock process in the previous section. We can display a six-minute 
timer on the client (web or mobile app). The timer on the client should have a slightly 
longer duration than the timer on the backend because the clocks on the client and 
the backend host cannot be perfectly synchronized. 
This lock listing mechanism can reduce, but not completely prevent, multiple guests 
from making overlapping booking requests. We can use SQL row locking to prevent 
overlapping bookings. (Refer to https://dev.mysql.com/doc/refman/8.0/en/glossary 
.html#glos_exclusive_lock and https://www.postgresql.org/docs/current/explicit 
-locking.html#LOCKING-ROWS.) The backend service must use an SQL transaction 
on the leader host. First, make a SELECT query to check if the listing is available on 
the requested dates. Second, make an INSERT or UPDATE query to mark the listing 
accordingly. 
A consistency tradeoff of the leader-follower SQL architecture is that a search result 
may contain unavailable listings. If a guest attempts to book an unavailable listing, the 
booking service can return a 409 response. We do not expect the effect on user experience to be too severe because a user can expect that a listing may be booked while 
they are viewing it. However, we should add a metric to our monitoring service to monitor such occurrences, so we will be alerted and can react as necessary if this occurs 
excessively. 
Earlier in this chapter, we discussed why we will not cache popular (listing, date) 
pairs. If we do choose to do so, we can implement a caching strategy suited for readheavy loads; this is discussed in section 4.8.1. 
How much storage is needed? If each column occupies 64 bits, a row will occupy 40 
bytes. One million listings will occupy 7.2 GB for 180 days of data, which can easily fit on 
a single host. We can manually delete old data as required to free up space. 
An alternative SQL table schema can be similar to the Booking table discussed in 
the previous section, except that it may also contain a column named “status” or “availability” that indicates if the listing is locked or booked. The algorithm to find if a listing 
is available between a certain check-in and check-out date can be a coding interview 
question. You may be asked to code a solution in a coding interview, but not in a system 
design interview. 
15.9	 Logging, monitoring, and alerting 
Besides what was discussed in section 2.5, such as CPU, memory, disk usage of Redis, 
and disk usage of Elasticsearch, we should monitor and send alerts for the following.
We should have anomaly detection for an unusual rate of bookings, listings, or cancellations. Other examples include an unusually high rate of listings being manually or 
programmatically flagged for irregularities.
Define end-to-end user stories, such as the steps that a host takes to create a listing or 
the steps a guest takes to make a booking. Monitor the rate of completed vs. non-completed user stories/flows, and create alerts for unusually high occurrences of situations 


	
351
Other possible discussion topics 
where users do not go through an entire story/flow. Such a situation is also known as a 
low funnel conversion rate.
We can define and monitor the rate of undesirable user stories, such as booking 
requests either not being made or being canceled after communication between guests 
and hosts.
15.10	Other possible discussion topics 
The various services and business logic discussed in this chapter read like a smattering of topics and a gross oversimplification of a complex business. In an interview, we 
may continue designing more services and discussing their requirements, users, and 
inter-service communication. We may also consider more details of the various user 
stories and the corresponding intricacies in their system design: 
¡ A user may be interested in listings that do not exactly match their search criteria. 
For example, the available check-in date and/or check-out date may be slightly 
different, or listings in nearby cities may also be acceptable. How may we design 
a search service that returns such results? May we modify the search query before 
submitting it to Elasticsearch, or how may we design an Elasticsearch index that 
considers such results as relevant? 
¡ What other features may we design for hosts, guests, Ops, and other users? For 
example, can we design a system for guests to report inappropriate listings? Can 
we design a system that monitors host and guest behavior to recommend possible 
punitive actions such as restrictions on using the service or account deactivation? 
¡ Functional requirements defined earlier as outside the scope of the interview. 
Their architecture details, such as whether the requirements are satisfied in our 
current services or should be separate services. 
¡ We did not discuss search. We may consider letting guests search for listings by 
keywords. We will need to index our listings. We may use Elasticsearch or design 
our own search service. 
¡ Expand the product range, such as offering listings suited to business travelers. 
¡ Allow double-booking, similar to hotels. Upgrade guests if rooms are unavailable, since more expensive rooms tend to have high vacancy. 
¡ Chapter 17 discusses an example analytics system. 
¡ Show users some statistics (e.g., how popular a listing is). 
¡ Personalization, such as a recommender system for rooms. For example, a recommender service can recommend new listings so they will quickly have guests, 
which will be encouraging to new hosts. 
¡ A frontend engineer or UX designer interview may include discussion of UX 
flows. 
¡ Fraud protection and mitigation. 


352
Chapter 15  Design Airbnb
15.10.1	Handling regulations 
We can consider designing and implementing a dedicated regulation service to provide 
a standard API for communicating regulations. All other services must be designed to 
interact with this API, so they are flexible to changing regulations or at least be more 
easily redesigned in response to unforeseen regulations. 
In the author’s experience, designing services to be flexible to changing regulations 
is a blind spot in many companies, and considerable resources are spent on re-architecture, implementation, and migration each time regulations change.
Exercise
A possible exercise is to discuss differences in regulations requirements between Airbnb 
and Craigslist. 
Data privacy laws are a relevant concern to many companies. Examples include COPPA 
(https://www.ftc.gov/enforcement/rules/rulemaking-regulatory-reform-proceedings/ 
childrens-online-privacy-protection-rule), GDPR (https://gdpr-info.eu/), and CCPA 
(https://oag.ca.gov/privacy/ccpa). Some governments may require companies to 
share data on activities that occur in their jurisdictions or that data on their citizens 
cannot leave the country. 
Regulations may affect the core business of the company. In the case of Airbnb, there 
are regulations directly on hosts and guests. Examples of such regulations may include 
¡ A listing may only be hosted for a maximum number of days in a year. 
¡ Only properties constructed before or after a certain year can be listed. 
¡ Bookings cannot be made on certain dates, such as certain public holidays. 
¡ Bookings may have a minimum or maximum duration in a specific city. 
¡ Listings may be disallowed altogether in certain cities or addresses. 
¡ Listing may require safety equipment such as carbon monoxide detectors, fire 
detectors, and fire escapes. 
¡ There may be other livability and safety regulations. 
Within a country, certain regulations may be specific to listings that meet certain conditions, and the specifics may differ by each specific country, state, city, or even address 
(e.g., certain apartment complexes may impose their own rules).


	
353
Summary
Summary
¡ Airbnb is a reservation app, a marketplace app, and a customer support and 
operations app. Hosts, guests, and Ops are the main user groups.
¡ Airbnb’s products are localized, so listings can be grouped in data centers by 
geography.
¡ The sheer number of services involved in listing and booking is impossible to 
comprehensively discuss in a system design interview. We can list a handful of 
main services and briefly discuss their functionalities.
¡ Creating a listing may involve multiple requests from the Airbnb host to ensure 
the listing complies with local regulations.
¡ After an Airbnb host submits a listing request, it may need to be manually 
approved by an Ops/admin member. After approval, it can be found and booked 
by guests.
¡ Interactions between these various services should be asynchronous if low latency 
is unnecessary. We employ distributed transactions techniques to allow asynchronous interactions.
¡ Caching is not always a suitable strategy to reduce latency, especially if the cache 
quickly becomes stale.
¡ Architecture diagrams and sequence diagrams are invaluable in designing a 
complex transaction.


354
16
Design a news feed
This chapter covers
¡ Designing a personalized scalable system
¡ Filtering out news feed items
¡ Designing a news feed to serve images and text
Design a news feed that provides a user with a list of news items, sorted by approximate reverse chronological order that belong to the topics selected by the user. A 
news item can be categorized into 1–3 topics. A user may select up to three topics of 
interest at any time. 
This is a common system design interview question. In this chapter, we use the 
terms “news item” and “post” interchangeably. In social media apps like Facebook or 
Twitter, a user’s news feed is usually populated by posts from friends/connections. 
However, in this news feed, users get posts written by other people in general, rather 
than by their connections. 


	
355
Requirements 
16.1	 Requirements 
These are the functional requirements of our news feed system, which as usual we can 
discuss/uncover via an approximately five-minute Q&A with the interviewer. 
¡ A user can select topics of interest. There are up to 100 tags. (We will use the term 
“tag” in place of “news topic” to prevent ambiguity with the term “Kafka topic.”)
¡ A user can fetch a list of English-language news items 10 at a time, up to 1,000 
items. 
¡ Although a user need only fetch up to 1,000 items, our system should archive all 
items. 
¡ Let’s first allow users to get the same items regardless of their geographical 
location and then consider personalization, based on factors like location and 
language.
¡ Latest news first; that is, news items should be arranged in reverse chronological 
order, but this can be an approximation.
¡ Components of a news item: 
–	 A new item will usually contain several text fields, such as a title with perhaps a 
150-character limit and a body with perhaps a 10,000-character limit. For simplicity, we can consider just one text field with a 10,000-character limit. 
–	 UNIX timestamp that indicates when the item was created. 
–	 We initially do not consider audio, images, or video. If we have time, we can 
consider 0–10 image files of up to 1 MB each. 
TIP    The initial functional requirements exclude images because images add 
considerable complexity to the system design. We can first design a system that 
handles only text and then consider how we can expand it to handle images and 
other media. 
¡ We can consider that we may not want to serve certain items because they contain 
inappropriate content.
The following are mostly or completely out of scope of the functional requirements: 
¡ Versioning is not considered because an article can have multiple versions. An 
author may add additional text or media to an article or edit the article to correct 
errors. 
¡ We initially do not need to consider analytics on user data (such as their topics of 
interest, articles displayed to them, and articles they chose to read) or sophisticated recommender systems. 
¡ We do not need any other personalization or social media features like sharing 
or commenting. 
¡ We need not consider the sources of the news items. Just provide a POST API 
endpoint to add news items. 


356
Chapter 16  Design a news feed
¡ We initially do not need to consider search. We can consider search after we satisfy our other requirements. 
¡ We do not consider monetization such as user login, payments, or subscriptions. 
We can assume all articles are free. We do not consider serving ads along with 
articles. 
The non-functional requirements of our news feed system can be as follows: 
¡ Scalable to support 100K daily active users each making an average of 10 requests 
daily, and one million news items/day. 
¡ High performance of one-second P99 is required for reads. 
¡ User data is private. 
¡ Eventual consistency of up to a few hours is acceptable. Users need not be able 
to view or access an article immediately after it is uploaded, but a few seconds is 
desirable. Some news apps have a requirement that an item can be designated 
as “breaking news,” which must be delivered immediately with high priority, but 
our news feed need not support this feature. 
¡ High availability is required for writes. High availability for reads is a bonus but 
not required, as users can cache old news on their devices. 
16.2	 High-level architecture 
We first sketch a very high-level architecture of our news feed system, shown in figure 
16.1. The sources of the news items submit news items to an ingestion service in our 
backend, and then they are written to a database. Users query our news feed service, 
which gets the news items from our database and returns them to our users. 
News
items
Sources
Ingestion
News Feed
Users
News feed system
Figure 16.1    Initial very high-level architecture of our news feed. News sources submit news items to an 
ingestion service, which processes them and persists them to a database. On the other side, users query 
our news feed service, which gets news items from our database. 
A few observations we can make from this architecture: 
¡ The ingestion service must be highly available and handle heavy and unpredictable traffic. We should consider using an event streaming platform like Kafka. 
¡ The database needs to archive all items but only provide up to 1,000 items to a 
user. This suggests that we can use one database to archive all items and others 
to serve the required items. We can choose a database technology best suited for 


	
357
High-level architecture 
each use case. A news item has 10,000 characters, which equals 10 KB. If they are 
UTF-8 characters, the size of the text will be 40 KB: 
–	 For serving 1,000 items and 100 tags, the total size of all news items is 1 GB, 
which can easily fit in a Redis cache. 
–	 For archival, we can use a distributed sharded file system like HDFS. 
¡ If eventual consistency of up to a few hours is acceptable, a user’s device may not 
need to update its news items more frequently than hourly, reducing the load on 
our News feed service. 
Figure 16.2 shows our high-level architecture. The queue and HDFS database are 
an example of CDC (Change Data Capture, refer to section 5.3), while the ETL job 
that reads from HDFS and writes to Redis is an example of CQRS (Command Query 
Responsibility Segregation, refer to section 1.4.6). 
User
Source/
Client
Ingestor
Queue
Producer
ETL jobs
Consumer
HDFS
API 
Gateway
News Feed Service
Metadata 
Service
Moderation
Service
Redis
Queue
Backend
Notification
Service
Figure 16.2    High-level architecture of our news feed service. A client submits a post to our news feed 
service. Our ingestor receives the post and performs some simple validations. If the validations pass, 
our ingestor produces it to a Kafka queue. Our consumer cluster consumes the post and writes it to 
HDFS. Our batch ETL jobs process the posts and produce them to another Kafka queue. They may also 
trigger notifications via a notification service. User requests for posts go through our API gateway, which 
may retrieve users’ tags from our metadata service and then retrieve posts from our Redis table via our 
backend service. When backend hosts are idle, they consume from the queue and update the Redis table.
Our news feed service’s sources push new posts to the ingestor. The ingestor performs 
validation tasks that can be done on the news item alone; it does not perform validations that depend on other news items or other data in general. Examples of such 
validation tasks: 


358
Chapter 16  Design a news feed
¡ Sanitize the values to avoid SQL injection. 
¡ Filtering and censorship tasks, such as detecting inappropriate language. There 
can be two sets of criteria: one for immediate rejection, where items that satisfy 
these criteria are immediately rejected, and another criteria where items that 
satisfy these criteria are flagged for manual review. This flag can be appended to 
the item before it is produced to the queue. We discuss this further in the next 
section. 
¡ A post is not from a blocked source/user. The ingestor obtains the list of blocked 
users from a moderation service. These blocked users are added to the moderation service either manually by our operations staff or automatically, after certain 
events. 
¡ Required fields have non-zero length. 
¡ A field that has a maximum length does not contain a value that exceeds that 
length. 
¡ A field that cannot contain certain characters (such as punctuation) does not 
have a value containing such characters. 
These validation tasks can also be done on our app in the source’s client before it submits a post to the ingestor. However, in case any validation tasks are skipped due to any 
bugs or malicious activity on the client, the ingestor can repeat these validations. If any 
validation fails in the ingestor, it should trigger an alert to the developers to investigate 
why the client and ingestor return different validation results. 
Requests from certain sources may need to pass through an authentication and authorization service before they reach the ingestor. This is not shown in figure 16.2. Refer to 
appendix B for a discussion of OAuth authentication and OpenID authorization. 
We use a Kafka queue to handle this unpredictable traffic. If the ingestor validations 
pass, the ingestor produces the post to the Kafka queue and returns 200 Success to the 
source. If any validation fails, the ingestor returns 400 Bad Request to the source and 
may also include an explanation of the validations that failed. 
The consumer just polls from the queue and writes to HDFS. We need at least two 
HDFS tables: one for raw news items submitted by the consumer and one for news 
items that are ready to be served to users. We may also need a separate table for items 
that require manual review before they are served to users. A detailed discussion of a 
manual review system is likely outside the scope of the interview. These HDFS tables are 
partitioned by tag and hour. 
Users make GET /post requests to our API gateway, which queries our metadata 
service for the user’s tags and then queries the appropriate news items from a Redis 
cache via our backend service. The Redis cache key can be a (tag, hour) tuple, and a 
value can be the corresponding list of news items. We can represent this data structure 
as {(tag, hour), [post]}, where tag is a string, hour is an integer, and post is an 
object that contains a post ID string and a body/content string. 
The API gateway also has its usual responsibilities as described in section 6.1, such as 
handling authentication and authorization, and rate limiting. If the number of hosts 


	
359
High-level architecture 
increases to a large number, and the usual responsibilities of the frontend have different hardware resources compared to querying the metadata service and Redis service, 
we can split the latter two functionalities away into a separate backend service, so we can 
scale these capabilities independently. 
Regarding the eventual consistency requirement and our observation that a user’s 
device may not need to update its news items more frequently than hourly, if a user 
requests an update within an hour of their previous request, we can reduce our service 
load in at least either of these two approaches: 
1	 Their device can ignore the request. 
2	 Their device can make the request, but do not retry if the response is a 504 
timeout. 
The ETL jobs write to another Kafka queue. When backend hosts are not serving user 
requests for posts, they can consume from the Kafka queue and update the Redis table. 
The ETL jobs fulfill the following functions: 
Before the raw news items are served to users, we may first need to run validation or 
moderation/censorship tasks that depend on other news items or other data in general. For simplicity, we will collectively refer to all such tasks as “validation tasks.” Referring to figure 16.3, these can be parallel ETL tasks. We may need an additional HDFS 
table for each task. Each table contains the item IDs that passed the validations. Examples are as follows:
¡ Finding duplicate items. 
¡ If there is a limit on the number of news items on a particular tag/subject that 
can be submitted within the last hour, there can be a validation task for this. 
¡ Determine the intersection of the item IDs from the intermediate HDFS tables. 
This is the set of IDs that passed all validations. Write this set to a final HDFS 
table. Read the IDs from the final HDFS table and then copy the corresponding 
news items to overwrite the Redis cache. 
Validation task 1
Validation task 2
Validation task n
Intersection task
Redis refresh task
Figure 16.3    ETL job DAG. 
The validation tasks run 
in parallel. Each validation 
task outputs a set of valid 
post IDs. When the tasks are 
done, the intersection task 
determines the intersection 
of all these sets, which are 
the IDs of posts that users 
can be served. 


360
Chapter 16  Design a news feed
We may also have ETL jobs to trigger notifications via a notification service. Notification channels may include our mobile and browser apps, email, texting, and social 
media. Refer to chapter 9 for a detailed discussion on a notification service. We will not 
discuss this in detail in this chapter.
Notice the key role of moderation in our news feed service, as illustrated in figure 
16.2 and discussed in the context of our ETL jobs. We may also need to moderate 
the posts for each specific user, e.g., as discussed earlier, blocked users should not be 
allowed to make requests. Referring to figure 16.4, we can consider unifying all this 
moderation into a single moderation service. We discussed this further in section 16.4. 
User
Source/
Client
Ingestor
Queue
Producer
ETL jobs
Consumer
HDFS
API 
Gateway
News Feed Service
Redis
Queue
Backend
Notification
Service
Moderation
Service
Metadata 
Service
Figure 16.4    High-level architecture of our news feed system with all content moderation centralized in a 
moderation service. Developers can define all content moderation logic in this service. 	
16.3	 Prepare feed in advance
In our design in figure 16.2, each user will need one Redis query per (tag, hour) pair. 
Each user may need to make many queries to obtain their relevant or desired items, 
causing high read traffic and possibly high latency on our news feed service. 
We can trade off higher storage for lower latency and traffic by preparing a user’s 
feed in advance. We can prepare two hash maps, {user ID, post ID} and {post ID, post}. 
Assuming 100 tags with 1K 10K-character items each, the latter hash map occupies 
slightly over 1 GB. For the former hash map, we will need to store one billion user IDs 
and up to 100*1000 possible post IDs. An ID is 64 bits. Total storage requirement is up 
to 800 TB, which may be beyond the capacity of a Redis cluster. One possible solution 
is to partition the users by region and store just two to three regions per data center, so 
there are up to 20M users per data center, which works out to 16 TB. Another possible 
solution is to limit the storage requirement to 1 TB by limiting it to a few dozen post IDs, 
but this does not fulfill our 1,000-item requirement. 


	
361
Prepare feed in advance
Another possible solution is to use a sharded SQL implementation for the {user ID, 
post ID} pair, as discussed in section 4.3. We can shard this table by hashed user ID, so 
user IDs are randomly distributed among the nodes, and the more intensive users are 
randomly distributed too. This will prevent hot shard problems. When our backend 
receives a request for a user ID’s posts, it can hash the user ID and then make a request 
to the appropriate SQL node. (We will discuss momentarily how it finds an appropriate 
SQL node.) The table that contains the {post ID, post} pairs can be replicated across 
every node, so we can do JOIN queries between these two tables. (This table may also 
contain other dimension columns for timestamp, tag, etc.) Figure 16.5 illustrates our 
sharding and replication strategy. 
User table
partition 0
Post table copy
User table
partition 1
User table
partition n
Post table copy
Post table copy
Post table
copy
copy
copy
JOIN
JOIN
JOIN
Figure 16.5    Illustration of our sharding and replication strategy. The table with {hashed user ID, post ID} 
is sharded and distributed across multiple leader hosts and replicated to follower hosts. The table with 
{post ID, post} is replicated to every host. We can JOIN on post ID. 
Referring to figure 16.6, we can divide the 64-bit address space of hashed user IDs 
among our clusters. Cluster 0 can contain any hashed user IDs in [0, (264 – 1)/4), 
cluster 1 can contain any hashed user IDs in [(264 – 1)/4, (264 – 1)/2), cluster 2 can 
contain any hashed user IDs in [(264 – 1)/2, 3 * (264 – 1)/4), and cluster 3 can contain 
any hashed user IDs in [3 * (264 – 1)/4, 264 – 1). We can start with this even division. As 
traffic will be uneven between clusters, we can balance the traffic by adjusting the number and sizes of the divisions. 
0
(264–1) / 4
(264–1) / 2
3 * (264–1) / 4
264–1
Cluster 0
Cluster 1
Cluster 2
Cluster 3
Figure 16.6    Consistent hashing 
of hashed user IDs to cluster 
names. We can divide clusters 
across the 64-bit address space. 
In this illustration, we assume 
we have four clusters, so each 
cluster takes one-quarter of the 
address space. We can start with 
even divisions and then adjust the 
number and sizes of divisions to 
balance the traffic between them.


362
Chapter 16  Design a news feed
How does our backend find an appropriate SQL node? We need a mapping of hashed 
user IDs to cluster names. Each cluster can have multiple A records, one for each follower, so a backend host is randomly assigned to a follower node in the appropriate 
cluster. 
We need to monitor traffic volume to the clusters to detect hot shards and rebalance 
the traffic by resizing clusters appropriately. We can adjust the host’s hard disk capacity 
to save costs. If we are using a cloud vendor, we can adjust the VM (virtual machine) size 
that we use. 
Figure 16.7 illustrates the high-level architecture of our news feed service with this 
design. When a user makes a request, the backend hashes the user ID as just discussed. 
The backend then does a lookup to ZooKeeper to obtain the appropriate cluster name 
and sends the SQL query to the cluster. The query is sent to a random follower node, 
executed there, and then the result list of posts is returned to the user. 
User
Source/
Client
Ingestor
Queue
Producer
ETL jobs
Consumer
HDFS
API 
Gateway
News Feed Service
Queue
Backend
Notification
Service
Moderation 
Service
SQL 
cluster 0
SQL
Service
SQL 
cluster 1
SQL 
cluster n
ZooKeeper
Metadata
Service
Figure 16.7    High-level architecture of our news feed service with user feeds prepared in advance. 
Differences from figure 16.4 are bolded. When a user request arrives at our backend, our backend first 
obtains the appropriate SQL cluster name and then queries the appropriate SQL cluster for the posts. Our 
backend can direct user requests to a follower node that contains the requested user ID. Alternatively, as 
illustrated here, we can separate the routing of SQL requests into an SQL service. 
If our only client is a mobile app (i.e., no web app), we can save storage by storing 
posts on the client. We can then assume that a user only needs to fetch their posts 
once and delete their rows after they are fetched. If a user logs in to a different mobile 
device, they will not see the posts that they had fetched on their previous device. This 


	
363
Prepare feed in advance
occurrence may be sufficiently uncommon, and so it is acceptable to us, especially 
because news quickly becomes outdated, and a user will have little interest in a post a 
few days after it is published. 
Another way is to add a timestamp column and have an ETL job that periodically 
deletes rows that are older than 24 hours.
We may decide to avoid sharded SQL by combining both approaches. When a user 
opens the mobile app, we can use a prepared feed to serve only their first request for 
their posts and only store the number of post IDs that can fit into a single node. If the 
user scrolls down, the app may make more requests for more posts, and these requests 
can be served from Redis. Figure 16.8 illustrates the high-level architecture of this 
approach with Redis. This approach has tradeoffs of higher complexity and maintenance overhead for lower latency and cost. 
User
Source/
Client
Ingestor
Queue
Producer
ETL jobs
Consumer
HDFS
API 
Gateway
News Feed Service
Queue
Backend
Moderation
Service
SQL 
cluster 0
SQL
Service
SQL 
cluster 1
SQL 
cluster n
ZooKeeper
Redis
Notification
Service
Metadata 
Service
Figure 16.8    High-level architecture with both a prepared feed and Redis service. The difference from 
figure 16.7 is the added Redis service, which is bolded.
Let’s discuss a couple of ways a client can avoid fetching the same posts from Redis 
more than once: 
1	 A client can include the post IDs that it currently has in its GET /post request, so 
our backend can return posts that the client hasn’t fetched. 
2	 Our Redis table labels posts by hour. A client can request its posts of a certain 
hour. If there are too many posts to be returned, we can label posts by smaller 


364
Chapter 16  Design a news feed
time increments (such as blocks of 10 minutes per hour). Another possible way 
is to provide an API endpoint that returns all post IDs of a certain hour and a 
request body on the GET /post endpoint that allows users to specify the post IDs 
that it wishes to fetch. 
16.4	 Validation and content moderation
In this section, we discuss concerns about validation and possible solutions. Validation 
may not catch all problems, and posts may be erroneously delivered to users. Content 
filtering rules may differ by user demographic. 
Refer to section 15.6 for a discussion of an approval service for Airbnb, which is 
another approach to validation and content moderation. We will briefly discuss this 
here. Figure 16.9 illustrates our high-level architecture with an approval service. Certain ETL jobs may flag certain posts for manual review. We can send such posts to our 
approval service for manual review. If a reviewer approves a post, it will be sent to our 
Kafka queue to be consumed by our backend and served to users. If a reviewer rejects a 
post, our approval service can notify the source/client via a messaging service. 
User
Source/
Client
Ingestor
Queue
Producer
ETL jobs
Consumer
HDFS
API 
Gateway
News Feed Service
Queue
Backend
Approval 
Service
Moderation
Service
SQL 
cluster 0
SQL
Service
SQL 
cluster 1
SQL 
cluster n
ZooKeeper
Redis
Notification
Service
Metadata 
Service
Figure 16.9    ETL jobs can flag certain posts for manual approval. These posts can be sent to our 
approval service (in bold; this service is added to figure 16.8) for manual review, instead of being 
produced by a Kafka queue. (If we have a high rate of posts flagged for review, our approval service itself 
may need to contain a Kafka queue.) If a reviewer approves a post, it will be sent back to our Kafka 
queue via an ETL job to be consumed by our backend (or it can send the post directly to our backend). If 
a reviewer rejects a post, our approval service can notify the source/client via a messaging service, not 
illustrated in this figure. 


	
365
Validation and content moderation
16.4.1	 Changing posts on users’ devices
Certain validations are difficult to automate. For example, a post may be truncated. 
For simplicity, consider a post with just one sentence: “This is a post.” A truncated 
post can be: “This is a.” A post with spelling mistakes is easy to detect, but this post has 
no spelling mistakes but is clearly invalid. Such problems are difficult for automated 
validation. 
Certain inappropriate content, like inappropriate words is easy to detect, but much 
inappropriate content like age-inappropriate content, bomb threats, or fake news is 
extremely difficult to automatically screen for. 
In any system design, we should not try to prevent all errors and failures. We should 
assume that mistakes and failures are inevitable, and we should develop mechanisms 
to make it easy to detect, troubleshoot, and fix them. Certain posts that should not be 
delivered may be accidentally delivered to users. We need a mechanism to delete such 
posts on our news feed service or overwrite them with corrected posts. If users’ devices 
cache posts, they should be deleted or overwritten with the corrected versions. 
To do this, we can modify our GET /posts endpoint. Each time a user fetches posts, 
the response should contain a list of corrected posts and a list of posts to be deleted. 
The client mobile app should display the corrected posts and delete the appropriate 
posts.
One possible way is to add an “event” enum to a post, with possible values REPLACE 
and DELETE. If we want to replace or delete an old post on a client, we should create a 
new post object that has the same post ID as the old post. The post object should have 
an event with the value REPLACE for replacement or DELETE for deletion. 
For our news feed service to know which posts on a client need to be modified, the 
former needs to know which posts the client has. Our news feed service can log the IDs 
of posts that clients downloaded, but the storage requirement may be too big and costly. 
If we set a retention period on clients (such as 24 hours or 7 days) so they automatically 
delete old posts, we can likewise delete these old logs, but storage may still be costly. 
Another solution is for clients to include their current post IDs in GET /post requests, 
our backend can process these post IDs to determine which new posts to send (as we 
discussed earlier) and also determine which posts need to be changed or deleted. 
In section 16.4.3, we discuss a moderation service where one of the key functions is 
that admins can view currently available posts on the news feed service and make moderation decisions where posts are changed or deleted. 
16.4.2	 Tagging posts
We can assume an approval or rejection is applied to an entire post. That is, if any 
part of a post fails validation or moderation, we simply reject the entire post instead 
of attempting to serve part of it. What should we do with posts that fail validation? We 
may simply drop them, notify their sources, or manually review them. The first choice 
may cause poor user experience, while the third choice may be too expensive if done 
at scale. We can choose the second option. 


366
Chapter 16  Design a news feed
We can expand the intersection task of figure 16.3 to also message the responsible 
source/user if any validation fails. The intersection task can aggregate all failed validations and send them to the source/user in a single message. It may use a shared 
messaging service to send messages. Each validation task can have an ID and a short 
description of the validation. A message can contain the IDs and descriptions of failed 
validations for the user to reference if it wishes to contact our company to discuss any 
necessary changes to their post or to dispute the rejection decision. 
Another requirement we may need to discuss is whether we need to distinguish rules 
that apply globally versus region-specific rules. Certain rules may apply only to specific 
countries because of local cultural sensitivities or government laws and regulations. 
Generalizing this, a user should not be shown certain posts depending on their stated 
preferences and their demographic, such as age or region. Furthermore, we cannot 
reject such posts in the ingestor because doing so will apply these validation tasks to all 
users, not just specific users. We must instead tag the posts with certain metadata that 
will be used to filter out specific posts for each user. To prevent ambiguity with tags for 
user interests, we can refer to such tags as filter tags, or “filters” for short. A post can 
have both tags and filters. A key difference between tags and filters is that users configure their preferred tags, while filters are completely controlled by us. As discussed in 
the next subsection, this difference means that filters will be configured in the moderation service, but tags are not. 
We assume that when a new tag/filter is added or a current tag/filter is deleted, this 
change will only apply to future posts, and we do not need to relabel past posts.
A single Redis lookup is no longer sufficient for a user to fetch their posts. We’ll need 
three Redis hash tables, with the following key-value pairs: 
¡ {post ID, post}: For fetching posts by ID
¡ {tag, [post ID]}: For filtering post IDs by tag 
¡ {post ID, [filter]}: For filtering out posts by filter
Multiple key-value lookups are needed. The steps are as follows:
1	 A client makes a GET /post request to our news feed service.
2	 Our API gateway queries our metadata service for a client’s tags and filters. Our 
client can also store its own tags and filters and provide them in a GET /post 
request, and then we can skip this lookup. 
3	 Our API gateway queries Redis to obtain the post IDs with the user’s tags and 
filters. 
4	 It queries Redis for the filter of each post ID and excludes this post ID from the 
user if it contains any of the user’s filters. 
5	 It queries Redis for the post of each post ID and then returns these posts to the 
client. 


	
367
Validation and content moderation
Note that the logic to filter out post IDs by tags must be done at the application level. An alternative is to use SQL tables instead of Redis tables. We can create a post table with (post_
id, post) columns, a tag table with (tag, post_id) columns, and a filter table with (filter, 
post_id) columns, and do a single SQL JOIN query to obtain a client’s posts:
SELECT post 
FROM post p JOIN tag t ON p.post_id = t.post_id 
LEFT JOIN filter f ON p.post_id = f.post_id 
WHERE p.post_id IS NULL
Section 16.3 discussed preparing users’ feeds in advance by preparing the Redis table 
with {user_id, post_id}. Even with the post filtering requirements discussed in this section, we can have an ETL job that prepares this Redis table. 
Last, we note that with a region-specific news feed, we may need to partition the 
Redis cache by region or introduce an additional “region” column in the Redis key. We 
can also do this if we need to support multiple languages. 
16.4.3	 Moderation service
Our system does validation at four places: the client, ingestor, ETL jobs, and in the 
backend during GET /post requests. We implement the same validations in the various 
browser and mobile apps and in the ingestor, even though this means duplicate development and maintenance and higher risk of bugs. The validations add CPU processing overhead but reduce traffic to our news feed service, which means a smaller cluster 
size and lower costs. This approach is also more secure. If hackers bypass client-side 
validations by making API requests directly to our news feed service, our server-side 
validations will catch these invalid requests. 
Regarding the server-side validations, the ingestor, ETL jobs, and backend have different validations. However, referring to figure 16.4, we can consider consolidating and 
abstracting them into a single service that we can call the moderation service. 
As alluded to in the previous subsection about tags vs. filters, the general purpose of 
the moderation service is for us (not users) to control whether users will see submitted 
posts. Based on our discussion so far, the moderation service will provide the following 
features for admins:
1	 Configure validation tasks and filters. 
2	 Execute moderation decisions to change or delete posts. 
Consolidating moderation into a single service ensures that teams working on various services within our news feed service do not accidentally implement duplicate validations and allows non-technical staff in content moderation teams to perform all 
moderation tasks without having to request engineering assistance. The moderation 
service also logs these decisions for reviews, audits, or rollback (reverse a moderation 
decision).


368
Chapter 16  Design a news feed
Using tools to communicate
In general, communicating with engineering teams and getting engineering work prioritized is difficult, particularly in large organizations, and any tools that allow one to perform their work without this communication are generally good investments. 
This moderation request can be processed in the same manner as other write requests 
to our news feed service. Similar to the ETL jobs, the moderation service produces to 
the news feed topic, and our news feed service consumes this event and writes the relevant data to Redis.
16.5	 Logging, monitoring, and alerting 
In section 2.5, we discussed key concepts of logging, monitoring, and alerting that one 
must mention in an interview. Besides what was discussed in section 2.5, we should 
monitor and send alerts for the following: 
¡ Unusually large or small rate of traffic from any particular source.
¡ An unusually large rate of items that fail validation, across all items and within 
each individual source.
¡ Negative user reactions, such as users flagging articles for abuse or errors.
¡ Unusually long processing of an item across the pipeline. This can be monitored 
by comparing the item’s timestamp when it was uploaded to the current time 
when the item reaches the Redis database. Unusually long processing may indicate that certain pipeline components need to be scaled up, or there may be 
inefficient pipeline operations that we should reexamine. 
16.5.1	 Serving images as well as text 
Let’s allow a news item to have 0–10 images of up to 1 MB each. We will consider a 
post’s images to be part of a post object, and a tag or filter applies to the entire post 
object, not to individual properties like a post’s body or any image. 
This considerably increases the overhead of GET /post requests. Image files are considerably different from post body strings: 
¡ Image files are much larger than bodies, and we can consider different storage 
technologies for them. 
¡ Image files may be reused across posts. 
¡ Validation algorithms for image files will likely use image processing libraries, 
which are considerably different from validation of post body strings. 


	
369
Logging, monitoring, and alerting 
16.5.2	 High-level architecture  
We first observe that the 40 KB storage requirement of an article’s text is negligible 
compared to the 10 MB requirement for its images. This means that uploading or processing operations on an article’s text is fast, but uploading or processing images takes 
more time and computational resources. 
Figure 16.10 shows our high-level architecture with a media service. Media upload 
must be synchronous because the source needs to be informed if the upload succeeded 
or failed. This means that the ingestor service’s cluster will be much bigger than before 
we added media to articles. The media service can store the media on a shared object 
service, which is replicated across multiple data centers, so a user can access the media 
from the data center closest to them. 
User
Source/
Client
Ingestor
Queue
Producer
ETL jobs
Consumer
HDFS
API 
Gateway
News Feed Service
Media 
Service
Queue
Backend
Approval
Service
Moderation
Service
SQL 
cluster 0
SQL
Service
SQL 
cluster 1
SQL 
cluster n
ZooKeeper
Redis
Notification
Service
Metadata 
Service
Figure 16.10    Adding a media service (in bold; this service is added to figure 16.9), which allows our 
news items to contain audio, images and videos. A separate media service also makes it easier to 
manage and analyze media separately of its news items. 


370
Chapter 16  Design a news feed
Figure 16.11 is a sequence diagram of a source uploading an article. Because media 
uploads require more data transfer than metadata or text, the media uploads should 
complete before producing the article’s metadata and text onto the Kafka queue. If 
the media uploads succeed but producing to the queue fails, we can return a 500 error 
to the source. During a file upload process to the media service, the ingestor can first 
hash the file and send this hash to the media service to check if the file has already 
been uploaded. If so, the media service can return a 304 response to the ingestor, and 
a costly network transfer can be avoided. We note that in this design, the consumer 
cluster can be much smaller than the Media service cluster. 
:Source
:Ingestor
:Media service
:Kafka topic
Upload article.
Response OK.
Upload media.
Response OK.
Produce text and metadata to queue.
Response OK.
Figure 16.11    Sequence diagram of a source uploading an article. Media is almost always larger than 
text, so our ingestor first uploads media to our Media Service. After our ingestor successfully uploads  
the media, it produces the text and metadata to our Kafka topic, to be consumed and written to HDFS  
as discussed in this chapter. 
What if the ingestor host fails after the media was successfully uploaded but before 
it can produce to the Kafka topic? It makes sense to keep the media upload rather 
than delete it because the media upload process is resource-intensive. The source will 
receive an error response and can try the upload again. This time, the media service 
can return a 304 as discussed in the previous paragraph, and then the ingestor can 
produce the corresponding event. The source may not retry. In that case, we can periodically run an audit job to find media that do not have accompanying metadata and 
text in HDFS and delete this media. 
If our users are widely geographically distributed, or user traffic is too heavy for our 
media service, we can use a CDN. Refer to chapter 13 for a discussion on a CDN system 
design. The authorization tokens to download images from the CDN can be granted by 
the API gateway, using a service mesh architecture. Figure 16.12 shows our high-level 
architecture with a CDN. A new item will contain text fields for content such as title, 
body, and media URLs. Referring to figure 16.12, a source can upload images to our 
image service and text content to our news feed service. A client can
¡ Download article text and media URLs from Redis. 
¡ Download media from the CDN. 


	
371
Logging, monitoring, and alerting 
User
Source/
Client
Ingestor
Queue
Producer
ETL jobs
Consumer
HDFS
API 
Gateway
News Feed Service
Media
Service
Queue
Backend
Approval
Service
Moderation
Service
SQL 
cluster 0
SQL
Service
SQL 
cluster 1
SQL 
cluster n
ZooKeeper
Redis
Notification
Service
CDN
Metadata
Service
Figure 16.12    Using a CDN (in bold; this service is added to figure 16.10) to host media. Users will 
download images directly from our CDN, gaining the benefits of a CDN such as lower latency and higher 
availability. 
The main differences with figure 16.10 are the following: 
¡ The media service writes media to the CDN, and users download media from the 
CDN. 
¡ ETL jobs and the approval service make requests to the media service. 
We use both a media service and a CDN because some articles will not be served to 
users, so some images don’t need to be stored on the CDN, which will reduce costs. 
Certain ETL jobs may be automatic approvals of articles, so these jobs need to inform 
the media service that the article is approved, and the media service should upload the 
article’s media to the CDN to be served to users. The approval service makes similar 
requests to the media service. 


372
Chapter 16  Design a news feed
We may discuss the tradeoffs of handling and storing text and media in separate 
services vs. a single service. We can refer to chapter 13 to discuss more details of hosting 
images on a CDN, such as the tradeoffs of hosting media on a CDN. 
Taking this a step further, we can also host complete articles on our CDN, including 
all text and media. The Redis values can be reduced to article IDs. Although an article’s 
text is usually much smaller than its media, there can still be performance improvements from placing it on a CDN, particularly for frequent requests of popular articles. 
Redis is horizontally scalable but inter data center replication is complex. 
In the approval service, should the images and text of an article be reviewed separately or together? For simplicity, reviewing an article can consist of reviewing both its 
text and accompanying media as a single article. 
How can we review media more efficiently? Hiring review staff is expensive, and a 
staff will need to listen to an audio clip or watch a video completely before making a 
review decision. We can consider transcribing audio, so a reviewer can read rather than 
listen to audio files. This will allow us to hire hearing-impaired staff, improving the company’s inclusivity culture. A staff can play a video file at 2x or 3x speed when they review 
it and read the transcribed audio separately from viewing the video file. We can also 
consider machine learning solutions to review articles. 
16.6	 Other possible discussion topics 
Here are other possible discussion topics that may come up as the interview progresses, 
which may be suggested by either the interviewer or candidate: 
¡ Create hashtags, which are dynamic, rather than a fixed set of topics. 
¡ Users may wish to share news items with other users or groups. 
¡ Have a more detailed discussion on sending notifications to creators and readers. 
¡ Real-time dissemination of articles. ETL jobs must be streaming, not batch. 
¡ Boosting to prioritize certain articles over others. 
We can consider the items that were out-of-scope in the functional requirements 
discussion: 
¡ Analytics. 
¡ Personalization. Instead of serving the same 1,000 news items to all users, serve 
each user a personalized set of 100 news items. This design will be substantially 
more complex. 
¡ Serving articles in languages other than English. Potential complications, such as 
handling UTF or language transations. 
¡ Monetizing the news feed. Topics include: 
–	 Design a subscription system. 
–	 Reserve certain posts for subscribers. 
–	 An article limit for non-subscribers. 
–	 Ads and promoted posts. 


	
373
Summary
Summary
¡ When drawing the initial high-level architecture of the news feed system, consider the main data of interest and draw the components that read and write this 
data to the database.
¡ Consider the non-functional requirements of reading and writing the data and 
then select the appropriate database types and consider the accompanying services, if any. These include the Kafka service and Redis service. 
¡ Consider which operations don’t require low latency and place them in batch 
and streaming jobs for scalability.
¡ Determine any processing operations that must be performed before and after 
writes and reads and wrap them in services. Prior operations may include compression, content moderation, and lookups to other services to get relevant IDs 
or data. Post operations may include notifications and indexing. Examples of 
such services in our news feed system include the ingestor service, consumer service, ETL jobs, and backend service.
¡ Logging, monitoring, and alerting should be done on failures and unusual 
events that we may be interested in.


374
17
Design a dashboard 
of top 10 products on 
Amazon by sales volume
This chapter covers
¡ Scaling an aggregation operation on a large 	
	 data stream
¡ Using a Lambda architecture for fast  
	 approximate results and slow accurate results
¡ Using Kappa architecture as an alternative to 	
	 Lambda architecture 
¡ Approximating an aggregation operation for 	
	 faster speed
Analytics is a common discussion topic in a system design interview. We will always 
log certain network requests and user interactions, and we will perform analytics 
based on the data we collect. 
The Top K Problem (Heavy Hitters) is a common type of dashboard. Based on the 
popularity or lack thereof of certain products, we can make decisions to promote 
or discontinue them. Such decisions may not be straightforward. For example, if a 
product is unpopular, we may decide to either discontinue it to save the costs of selling it, or we may decide to spend more resources to promote it to increase its sales.


	
375
Requirements 
The Top K Problem is a common topic we can discuss in an interview when discussing analytics, or it may be its own standalone interview question. It can take on endless 
forms. Some examples of the Top K Problem include 
¡ Top-selling or worst-selling products on an ecommerce app by volume (this question) or revenue. 
¡ The most-viewed or least-viewed products on an ecommerce app. 
¡ Most downloaded apps on an apps store. 
¡ Most watched videos on a video app like YouTube. 
¡ Most popular (listened to) or least popular songs on a music app like Spotify. 
¡ Most traded stocks on an exchange like Robinhood or E*TRADE. 
¡ Most forwarded posts on a social media app, such as the most retweeted Twitter 
tweets or most shared Instagram post. 
17.1	 Requirements 
Let’s ask some questions to determine the functional and non-functional requirements. We assume that we have access to the data centers of Amazon or whichever 
ecommerce app we are concerned with 
¡ How do we break ties? 
High accuracy may not be important, so we can choose any item in a tie: 
¡ Which time intervals are we concerned with? 
Our system should be able to aggregate by certain specified intervals such as hour, day, 
week, or year: 
¡ The use cases will influence the desired accuracy (and other requirements like 
scalability). What are the use cases of this information? What is the desired accuracy and desired consistency/latency? 
That’s a good question. What do you have in mind? 
It will be resource-intensive to compute accurate volumes and ranking in real time. 
Perhaps we can have a Lambda architecture, so we have an eventually consistent solution that offers approximate sales volumes and rankings within the last few hours and 
accurate numbers for time periods older than a few hours. 
We can also consider trading off accuracy for higher scalability, lower cost, lower 
complexity, and better maintainability. We expect to compute a particular Top K list 
within a particular period at least hours after that period has passed, so consistency is 
not a concern. 
Low latency is not a concern. We can expect that generating a list will require many 
minutes: 
¡ Do we need just the Top K or top 10, or the volumes and ranking of an arbitrary 
number of products? 


376
Chapter 17  Design a dashboard of top 10 products on Amazon by sales volume  
Similar to the previous question, we can accept a solution that provides the approximate volumes and ranking of the top 10 products within the last few hours, and volumes and ranking of any arbitrary number of products for time periods older than a 
few hours, potentially up to years. It’s also fine if our solution can display more than 10 
products: 
¡ Do we need to show the sale counts on the Top K list or just the product sales 
rankings?
We will show both the rankings and counts. This seems like a superfluous question, but 
there might be possible design simplifications if we don’t need to display certain data: 
¡ Do we need to consider events that occur after a sale? A customer may request a 
refund, an exchange for the same or different product(s), or a product may be 
recalled. 
This is a good question that demonstrates one’s industry experience and attention to 
detail. Let’s assume we can consider only the initial sales events and disregard subsequent events like disputes or product recalls: 
¡ Let’s discuss scalability requirements. What is the sales transaction rate? What 
is the request rate for our Heavy Hitters dashboard? How many products do we 
have? 
Assume 10 billion sales events per day (i.e., heavy sales transaction traffic). At 1 KB/
event, the write rate is 10 TB/day. The Heavy Hitters dashboard will only be viewed by 
employees, so it will have low request rate. Assume we have ~1M products. 
We do not have other non-functional requirements. High availability or low latency 
(and the corresponding complexities they will bring to our system design) are not 
required.
17.2	 Initial thoughts
Our first thought may be to log the events to a distributed storage solution, like HDFS 
or Elasticsearch, and run a MapReduce, Spark, or Elasticsearch query when we need to 
compute a list of Top K products within a particular period. However, this approach is 
computationally intensive and may take too long. It may take hours or days to compute 
a list of Top K products within a particular month or year. 
If we don’t have use cases for storing our sales event logs other than generating this 
list, it will be wasteful to store these logs for months or years just for this purpose. If we 
log millions of requests per second, it can add up to PBs/year. We may wish to store a 
few months or years of raw events for various purposes, including serving customer disputes and refunds, for troubleshooting or regulatory compliance purposes. However, 
this retention period may be too short for generating our desired Top K list. 
We need to preprocess our data prior to computing these Top K lists. We should periodically perform aggregation and count the sales of our products, bucketing by hour, 
day, week, month, and year. Then we can perform these steps when we need a Top K list:


	
377
Initial high-level architecture
1	 If needed, sum the counts of the appropriate buckets, depending on the desired 
period. For example, if we need the Top K list of a period of one month, we simply use that month’s bucket. If we need a particular three-month period, we sum 
the counts of the one-month buckets of that period. This way, we can save storage 
by deleting events after we sum the counts.
2	 Sort these sums to obtain the Top K list. 
We need to save the buckets because the sales can be very uneven. In an extreme situation, a product “A” may have 1M sales within a particular hour during a particular 
year, and 0 sales at all other times during that year, while sales of all other products may 
sum to far less than 1M total sales in that year. Product A will be in the Top K list of any 
period that includes that hour. 
The rest of this chapter is about performing these operations at scale in a distributed 
manner.
17.3	 Initial high-level architecture
We first consider Lambda architecture. Lambda architecture is an approach to handling massive quantities of data by using both batch and streaming methods (Refer to 
https://www.databricks.com/glossary/lambda-architecture or https://www.snowflake 
.com/guides/lambda-architecture.) Referring to figure 17.1, our lambda architecture 
consists of two parallel data processing pipelines and a serving layer that combines the 
results of these two pipelines: 
1	 A streaming layer/pipeline that ingests events in real time from all data centers 
where sales transactions occur and uses an approximation algorithm to compute 
the sales volumes and rankings of the most popular products. 
2	 A batch layer, or batch pipelines that run periodically (hourly, daily, weekly, and 
yearly) to compute accurate sales volumes and rankings. For our users to see the 
accurate numbers as they become available, our batch pipeline ETL job can contain a task to overwrite the results of the streaming pipeline with the batch pipeline’s whenever the latter are ready. 
Data 
source
Batch 
pipelines
Streaming
pipelines
batch_table
streaming_table
Dashboard
Figure 17.1    A high-level sketch of our Lambda architecture. Arrows indicate the direction of requests. 
Data flows through our parallel streaming and batch pipelines. Each pipeline writes its final output to a 
table in a database. The streaming pipeline writes to the speed_table while the batch pipeline writes to 
the batch_table. Our dashboard combines data from the speed_table and batch_table to generate the 
Top K lists. 


378
Chapter 17  Design a dashboard of top 10 products on Amazon by sales volume  
Following an EDA (Event Driven Architecture) approach, the sales backend service 
sends events to a Kafka topic, which can be used for all downstream analytics such as 
our Top K dashboard. 
17.4	 Aggregation service 
An initial optimization we can make to our Lambda architecture is to do some aggregation on our sales events and pass these aggregated sales events to both our streaming 
and batch pipelines. Aggregation can reduce the cluster sizes of both our streaming 
and batch pipelines. We sketch a more detailed initial architecture in figure 17.2. Our 
streaming and batch pipelines both write to an RDBMS (SQL), which our dashboard 
can query with low latency. We can also use Redis if all we need is simple key-value lookups, but we will likely desire filter and aggregation operations for our dashboard and 
other future services. 
Sales 
backend
Batch
pipeline
Streaming
pipeline
Dashboard
SQL
Shared Logging
Service (e.g. 
ELK or Kafka)
Aggregation
HDFS
Figure 17.2    Our Lambda architecture, consisting of an initial aggregation service and streaming and 
batch pipelines. Arrows indicate the direction of requests. The sales backend logs events (including 
sales events) to a shared logging service, which is the data source for our dashboard. Our aggregation 
service consumes sales events from our shared logging service, aggregates them, and flushes these 
aggregated events to our streaming pipeline and to HDFS. Our batch pipeline computes the counts from 
our HDFS data and writes it to the SQL batch_table. Our streaming pipeline computes the counts faster 
and less accurately than our batch pipeline and writes it to the SQL speed_table. Our dashboard uses a 
combination of data from batch_table and speed_table to generate the Top K lists. 
NOTE    Event Driven Architecture (EDA) uses events to trigger and communicate between decoupled services (https://aws.amazon.com/event-driven 
-architecture/). Refer to other sources for more information, such as section 5.1 
or page 295 of Web Scalability for Startup Engineers (2015) by Artur Ejsmont for an 
introduction to event-driven architecture. 
We discussed aggregation and its benefits and tradeoffs in section 4.5. Our aggregation 
service consists of a cluster of hosts that subscribe to the Kafka topic that logs sales 
events, aggregates the events, and flushes/writes the aggregated events to HDFS (via 
Kafka) and to our streaming pipeline.


	
379
Aggregation service 
17.4.1	 Aggregating by product ID 
For example, a raw sales event may contain fields like (timestamp, product ID) while 
an aggregated event may be of the form (product_id, start_time, end_time, count, 
aggregation_host_id). We can aggregate the events since their exact timestamps are 
unimportant. If certain time intervals are important (e.g., hourly), we can ensure that 
(start_time, end_time) pairs are always within the same hour. For example, (0100, 
0110) is ok, but (0155, 0205) is not. 
17.4.2	 Matching host IDs and product IDs 
Our aggregation service can partition by product ID, so each host is responsible for 
aggregating a certain set of IDs. For simplicity, we can manually maintain a map of 
(host ID, product ID). There are various implementation options for this configuration, including 
1	 A configuration file included in the service’s source code. Each time we change 
the file, we must restart the entire cluster. 
2	 A configuration file in a shared object store. Each host of the service reads this 
file on startup and stores in memory the product IDs that it is responsible for. 
The service also needs an endpoint to update its product IDs. When we change 
the file, we can call this endpoint on the hosts that will consume different product IDs. 
3	 Storing the map as a database table in SQL or Redis. 
4	 Sidecar pattern, in which a host makes a fetch request to the sidecar. The sidecar 
fetches an event of the appropriate product IDs and returns it to the host. 
We will usually choose option 2 or 4 so we will not need to restart the entire cluster for 
each configuration change. We choose a file over a database for the following reasons: 
¡ It is easy to parse a configuration file format such as YAML and JSON directly 
into a hash map data structure. More code is required to achieve the same effect 
with a database table. We will need to code with an ORM framework, code the 
database query and the data access object, and match the data access object with 
the hash map. 
¡ The number of hosts will likely not exceed a few hundred or a few thousand, so 
the configuration file will be tiny. Each host can fetch the entire file. We do not 
need a solution with the low latency read performance of a database. 
¡ The configuration does not change frequently enough to justify the overhead of 
a database like SQL or Redis. 


380
Chapter 17  Design a dashboard of top 10 products on Amazon by sales volume  
17.4.3	 Storing timestamps 
If we need the exact timestamps to be stored somewhere, this storage should be handled by the sales service and not by an analytics or Heavy Hitters service. We should 
maintain separation of responsibility. There will be numerous analytics pipelines being 
defined on the sales events besides Heavy Hitters. We should have full freedom to 
develop and decommission these pipelines without regard to other services. In other 
words, we should be careful in deciding if other services should be dependencies of 
these analytics services. 
17.4.4	 Aggregation process on a host 
An aggregation host contains a hash table with key of product ID and value of count. 
It also does checkpointing on the Kafka topic that it consumes, writing checkpoints to 
Redis. The checkpoints consist of the IDs of the aggregated events. The aggregation 
service can have more hosts than the number of partitions in the Kafka topic, though 
this is unlikely to be necessary since aggregation is a simple and fast operation. Each 
host repeatedly does the following: 
1	 Consume an event from the topic. 
2	 Update its hash table. 
An aggregation host may flush its hash table with a set periodicity or when its memory 
is running out, whichever is sooner. A possible implementation of the flush process is 
as follows: 
1	 Produce the aggregated events to a Kafka topic that we can name “Flush.” If the 
aggregated data is small (e.g., a few MB), we can write it as a single event, consisting of a list of product ID aggregation tuples with the fields (“product ID,” “earliest timestamp,” “latest timestamp,” “number of sales”), such as, for example, 
[(123, 1620540831, 1620545831, 20), (152, 1620540731, 1620545831, 18), . . . ]. 
2	 Using change data capture (CDC, refer to section 5.3), each destination has a 
consumer that consumes the event and writes to it: 
a	 Write the aggregated events to HDFS. 
b	 Write a tuple checkpoint to Redis with the status “complete” (e.g., {“hdfs”: 
“1620540831, complete”}). 
c	 Repeat steps 2a–c for the streaming pipeline. 
If we did not have this “Flush” Kafka topic, and a consumer host fails while writing an 
aggregated event to a particular destination, the aggregation service will need to reaggregate those events. 
Why do we need to write two checkpoints? This is just one of various possible algorithms to maintain consistency. 
If a host fails during step 1, another host can consume the flush event and perform 
the writes. If the host fails during step 2a, the write to HDFS may have succeeded or 


	
381
Batch pipeline 
failed, and another host can read from HDFS to check if the write succeeded or if it 
needs to be retried. Reading from HDFS is an expensive operation. As a host failure 
is a rare event, this expensive operation will also be rare. If we are concerned with this 
expensive failure recovery mechanism, we can implement the failure recovery mechanism as a periodic operation to read all “processing” checkpoints between a minute and 
a few minutes old. 
The failure recovery mechanism should itself be idempotent in case it fails while in 
progress and has to be repeated. 
We should consider fault-tolerance. Any write operation may fail. Any host in the 
aggregation service, Redis service, HDFS cluster, or streaming pipeline can fail at any 
time. There may be network problems that interrupt write requests to any host on a service. A write event response code may be 200 but a silent error actually occurred. Such 
events will cause the three services to be in an inconsistent state. Therefore, we write a 
separate checkpoint for HDFS and our streaming pipeline. The write event should have 
an ID, so the destination services may perform deduplication if needed. 
In such situations where we need to write an event to multiple services, what are the 
possible ways to prevent such inconsistency? 
1	 Checkpoint after each write to each service, which we just discussed. 
2	 We can do nothing if our requirements state that inconsistency is acceptable. 
For example, we may tolerate some inaccuracy in the streaming pipeline, but the 
batch pipeline must be accurate. 
3	 Periodic auditing (also called supervisor). If the numbers do not line up, discard 
the inconsistent results and reprocess the relevant data. 
4	 Use distributed transaction techniques such as 2PC, Saga, Change Data Capture, 
or Transaction Supervisor. These were discussed in chapter 4 and appendix D. 
As discussed in section 4.5, the flip side of aggregation is that real-time results are 
delayed by the time required for aggregation and flushing. Aggregation may be unsuitable for if our dashboard requires low-latency updates. 
17.5	 Batch pipeline 
Our batch pipeline is conceptually more straightforward than the streaming pipeline, 
so we can discuss it first. 
Figure 17.3 shows a simplified flow diagram of our batch pipeline. Our batch pipeline consists of a series of aggregation/rollup tasks by increasing intervals. We roll up by 
hour, then day, then week, and then month and year. If we have 1M product IDs: 
1	 Rollup by hour will result in 24M rows/day or 168M rows/week. 
2	 Rollup by month will result in 28–31M rows/month or 336–372M rows/year. 
3	 Rollup by day will result in 7M rows/week or 364M rows/year. 


382
Chapter 17  Design a dashboard of top 10 products on Amazon by sales volume  
Aggregated
events
(HDFS)
Rolled-up
hourly
(batch_table)
Rolled-up
daily
(batch_table)
Rolled-up
weekly
(batch_table)
Rolled-up
monthly
(batch_table)
Rollup
by 
hour
Rollup
by 
day
Rollup
by 
week
Rollup
by 
month
Figure 17.3    Simplified flow diagram of the rollup tasks in our batch pipeline. We have a rollup job that 
progressively rolls up by increasing time intervals to reduce the number of rows processed in each stage. 
Let’s estimate the storage requirements. 400M rows each with 10 64-bit columns 
occupy 32 GB. This can easily fit into a single host. The hourly rollup job may need to 
process billions of sales events, so it can use a Hive query to read from HDFS and then 
write the resulting counts to the SQL batch_table. The rollups for other intervals use 
the vast reduction of the number of rows from the hourly rollup, and they only need to 
read and write to this SQL batch_table. 
In each of these rollups, we can order the counts by descending order, and write the 
Top K (or perhaps K*2 for flexibility) rows to our SQL database to be displayed on our 
dashboard. 
Figure 17.4 is a simple illustration of our ETL DAG for one stage in our batch pipeline (i.e., one rollup job). We will have one DAG for each rollup (i.e., four DAG in 
total). An ETL DAG has the following four tasks. The third and fourth are siblings. We 
use Airflow terminology for DAG, task, and run:
1	 For any rollup greater than hourly, we need a task to verify that the dependent 
rollup runs have successfully completed. Alternatively, the task can verify that 
the required HDFS or SQL data is available, but this will involve costly database 
queries. 
2	 Run a Hive or SQL query to sum the counts in descending order and write the 
result counts to the batch_table. 
3	 Delete the corresponding rows on the speed_table. This task is separate from task 
2 because the former can be rerun without having to rerun the latter. Should task 
3 fail while it is attempting to delete the rows, we should rerun the deletion without having to rerun the expensive Hive or SQL query of step 2.
4	 Generate or regenerate the appropriate Top K lists using these new batch_table 
rows. As discussed later in section 17.5, these Top K lists most likely have already 
been generated using both our accurate batch_table data and inaccurate speed_
table table, so we will be regenerating these lists with only our batch_table. This 
task is not costly, but it can also be rerun independently if it fails, so we implement it as its own task. 


	
383
Streaming pipeline 
Verify dependent 
rollups.
Counting
Delete appropriate 
speed_table rows.
Generate top K list.
Figure 17.4    An ETL DAG for one rollup job. The constituent tasks are to verify that dependent rollups 
have completed, perform the rollup/counting and persist the counts to SQL, and then delete the 
appropriate speed_table rows because they are no longer needed. 
Regarding task 1, the daily rollup can only happen if all its dependent hourly rollups 
have been written to HDFS, and likewise for the weekly and monthly rollups. One daily 
rollup run is dependent on 24 hourly rollup runs, one weekly rollup run is dependent 
on seven daily rollup runs, and one monthly rollup run is dependent on 28–30 daily rollup runs depending on the month. If we use Airflow, we can use ExternalTaskSensor 
(https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/external 
_task_sensor.html#externaltasksensor) instances with the appropriate execution 
_date parameter values in our daily, weekly, and monthly DAGs to verify that the 
dependent runs have successfully completed. 
17.6	 Streaming pipeline 
A batch job may take many hours to complete, which will affect the rollups for all intervals. For example, the Hive query for the latest hourly rollup job may take 30 minutes to complete, so the following rollups and by extension their Top K lists will be 
unavailable:
¡ The Top K list for that hour. 
¡ The Top K list for the day that contains that hour will be unavailable.
¡ The Top K lists for the week and month that contains that day will be unavailable. 
The purpose of our streaming pipeline is to provide the counts (and Top K lists) that 
the batch pipeline has not yet provided. The streaming pipeline must compute these 
counts much faster than the batch pipeline and may use approximation techniques. 
After our initial aggregation, the next steps are to compute the final counts and sort 
them in descending order, and then we will have our Top K lists. In this section, we 
approach this problem by first considering an approach for a single host and then find 
how to make it horizontally scalable. 
17.6.1	 Hash table and max-heap with a single host 
Our first attempt is to use a hash table and sort by frequency counts using a max-heap 
of size K. Listing 17.1 is a sample top K Golang function with this approach. 


384
Chapter 17  Design a dashboard of top 10 products on Amazon by sales volume  
Listing 17.1    Sample Golang function to compute Top K list
type HeavyHitter struct { 
  identifier string 
  frequency int 
} 
func topK(events []String, int k) (HeavyHitter) { 
  frequencyTable := make(map[string]int) 
  for _, event := range events { 
    value := frequencyTable[event] 
    if value == 0 { 
      frequencyTable[event] = 1 
    } else { 
      frequencyTable[event] = value + 1 
    } 
  } 
  pq = make(PriorityQueue, k) 
  i := 0 
  for key, element := range frequencyTable { 
    pq[i++] = &HeavyHitter{ 
      identifier: key, 
      frequency: element 
    } 
    if pq.Len() > k { 
      pq.Pop(&pq).(*HeavyHitter) 
    } 
  } 
  /*  
   * Write the heap contents to your destination. 
   * Here we just return them in an array. 
   */ 
  var result [k]HeavyHitter 
  i := 0 
  for pq.Len() > 0 { 
    result[i++] = pq.Pop(&pq).(*HeavyHitter) 
  } 
  return result 
}
In our system, we can run multiple instances of the function in parallel for our various 
time buckets (i.e., hour, day, week, month, and year). At the end of each period, we can 
store the contents of the max-heap, reset the counts to 0, and start counting for the 
new period. 


	
385
Streaming pipeline 
17.6.2	 Horizontal scaling to multiple hosts and multi-tier aggregation 
Figure 17.5 illustrates horizontal scaling to multiple hosts and multi-tier aggregation. The two hosts in the middle column sum the (product, hour) counts from their 
upstream hosts in the left column, while the max-heaps in the right column aggregate 
the (product, hour) counts from their upstream hosts in the middle column. 
(A, 0) = 1
(A, 1) = 3
(B, 0) = 3
(C, 0) = 3
(B, 0) = 1
(C, 0) = 2
(D, 0) = 3
(A, 0) = 2
(B, 0) = 1
(C, 1) = 1
(D, 1) = 4
(A, 0) = 1
(A, 1) = 3
(B, 0) = 4
(C, 0) = 5
(D, 0) = 3
(A, 0) = 2
(B, 0) = 1
(C, 1) = 1
(D, 0) = 4
Max-heap (hour 0)
(C, 0) = 5
(D, 0) = 7
Max-heap (day)
C = 6
D = 7
Max-heap (week)
Max-heap (year)
Max-heap (hour 1)
(A, 1) = 3
(C, 1) = 1
events
events
events
events
Figure 17.5    If the traffic to the final hash table host is too high, we can use a multi-tier approach for our 
streaming pipeline. For brevity, we display a key in the format (product, hour). For example, “(A, 0)” refers 
to product A at hour 0. Our final layer of hosts can contain max heaps, one for each rollup interval. This 
design is very similar to a multi-tier aggregation service discussed in section 4.5.2. Each host has an 
associated Kafka topic, which we don’t illustrate here. 
In this approach, we insert more tiers between the first layer of hosts and the final 
hash table host, so no host gets more traffic than it can process. This is simply shifting the complexity of implementing a multi-tier aggregation service from our aggregation service to our streaming pipeline. The solution will introduce latency, as also 
described in section 4.5.2. We also do partitioning, following the approach described 
in section 4.5.3 and illustrated in figure 4.6. Note the discussion points in that section 
about addressing hot partitions. We partition by product ID. We may also partition by 
sales event timestamp.
Aggregation
Notice that we aggregate by the combination of product ID and timestamp. Before reading on, think about why. 


386
Chapter 17  Design a dashboard of top 10 products on Amazon by sales volume  
Why do we aggregate by the combination of product ID and timestamp? This is because 
a Top K list has a period, with a start time and an end time. We need to ensure that 
each sales event is aggregated in its correct time ranges. For example, a sales event that 
occurred at 2023-01-01 10:08 UTC should be aggregated in
1	 The hour range of [2023-01-01 10:08 UTC, 2023-01-01 11:00 UTC).
2	 The day range of [2023-01-01, 2023-01-02).
3	 The week range of [2022-12-28 00:00 UTC, 2023-01-05 00:00 UTC). 2022-12-28 
and 2023-01-05 are both Mondays.
4	 The month range of [2023-01-01, 2013-02-01). 
5	 The year range of [2023, 2024). 
Our approach is to aggregate by the smallest period (i.e., hour). We expect any event 
to take only a few seconds to go through all the layers in our cluster, so it is unlikely for 
any key in our cluster that is more than an hour old. Each product ID has its own key. 
With the hour range appended to each key, it is unlikely that the number of keys will 
be greater than the number of product IDs times two. 
One minute after the end of a period—for example, at 2023-01-01 11:01 UTC for 
[2023-01-01 10:08 UTC, 2023-01-01 11:00 UTC) or 2023-01-02 00:01 UTC for [2023-
01-01, 2023-01-02)—the respective host in the final layer (whom we can refer to as final 
hosts) can write its heap to our SQL speed_table, and then our dashboard is ready to display the corresponding Top K list for this period. Occasionally, an event may take more 
than a minute to go through all the layers, and then the final hosts can simply write 
their updated heaps to our speed_table. We can set a retention period of a few hours or 
days for our final hosts to retain old aggregation keys, after which they can delete them. 
An alternative to waiting one minute is to implement a system to keep track of the 
events as they pass through the hosts and trigger the final hosts to write their heaps to 
the speed_table only after all the relevant events have reached the final hosts. However, 
this may be overly complex and also prevents our dashboard from displaying approximations before all events have been fully processed. 
17.7	 Approximation 
To achieve lower latency, we may need to limit the number of layers in our aggregation 
service. Figure 17.6 is an example of such a design. We have layers that consist of just 
max-heaps. This approach trades off accuracy for faster updates and lower cost. We can 
rely on the batch pipeline for slower and highly accurate aggregation. 
Why are max-heaps in separate hosts? This is to simplify provisioning new hosts when 
scaling up our cluster. As mentioned in section 3.1, a system is considered scalable if 
it can be scaled up and down with ease. We can have separate Docker images for hash 
table hosts and the max-heap host, since the number of hash table hosts may change 
frequently while there is never more than one active max-heap host (and its replicas). 


	
387
Approximation 
A = 1
B = 4
C = 5
D = 3
A = 2
B = 1
C = 1
D = 4
Max-heap
C = 5
D = 3
A = 1
B = 3
C = 3
B = 1
C = 2
D = 3
A = 2
B = 1
C = 1
D = 4
B = 6
C = 14
events
events
events
events
A = 4
B = 3
C = 4
D = 3
A = 1
B = 3
C = 5
D = 3
A = 4
B = 1
C = 2
B = 2
C = 2
D = 3
A = 1
C = 5
B = 3
D = 3
Max-heap
B = 6
C = 9
events
events
events
events
Figure 17.6    Multi-tier with max-heaps. The aggregation will be faster but less accurate. For brevity, we 
don’t display time buckets in this figure. 
However, the Top K list produced by this design may be inaccurate. We cannot have a 
max-heap in each host and simply merge the max-heaps because if we do so, the final 
max-heap may not actually contain the Top K products. For example, if host one had a 
hash table {A: 7, B: 6, C: 5}, and host B had a hash table {A: 2, B: 4, C: 5}, and our maxheap is of size 2, host 1’s max-heap will contain {A: 7, B: 6} and host 2’s max-heap will 
contain {B: 4, C: 5}. The final combined max-heap will be {A: 7, B: 10}, which erroneously leaves C out of the top two list. The correct final max-heap should be {B: 10, C: 
11}. 


388
Chapter 17  Design a dashboard of top 10 products on Amazon by sales volume  
17.7.1	 Count-min sketch 
The previous example approaches require a large amount of memory on each host for 
a hash table of the same size as the number of products (in our case ~1M). We can consider trading off accuracy for lower memory consumption by using approximations. 
Count-min sketch is a suitable approximation algorithm. We can think of it as a 
two-dimensional (2D) table with a width and a height. The width is usually a few thousand while the height is small and represents a number of hash functions (e.g., 5). The 
output of each hash function is bounded to the width. When a new item arrives, we 
apply each hash function to the item and increment the corresponding cell. 
Let’s walk through an example of using count-min sketch with a simple sequence “A 
C B C C.” C is the most common letter and occurs three times. Tables 17.1–17.5 illustrate a count-min sketch table. We bold the hashed value in each step to highlight it. 
1	 Hash the first letter “A” with each of the five hash functions. Table 17.1 illustrates 
that each hash function hashes “A” to a different value.
Table 17.1    Sample count-min sketch table after adding a single letter “A”
1
1
1
1
1
2	 Hash the second letter “C.” Table 17.2 illustrates that the first four hash functions 
hash “C” to a different value than “A.” The fifth hash function has a collision. The 
hashed values of “A” and “C” are identical, so that value is incremented. 
Table 17.2    Sample count-min sketch table after adding “A C”
1
1
1
1
1
1
1
1
2 (collision)
3	 Hash the third letter “B.” Table 17.3 illustrates that the fourth and fifth hash 
functions have collisions.


	
389
Approximation 
Table 17.3    Sample count-min sketch table after adding “A C B”
1
1
1
1
1
1
1
1
1
2 (collision)
1
3 (collision)
4	 Hash the fourth letter “C.” Table 17.4 illustrates that only the fifth hash function 
has a collision.
Table 17.4    Sample count-min sketch table after adding “A C B C”
1
1
2
1
2
1
2
1
1
2
2
4 (collision)
5	 Hash the fifth letter “C.” The operation is identical to the previous step. Table 
17.5 is the count-min sketch table after a sequence “A C B C C.” 
Table 17.5    Sample count-min sketch table after a sequence “A C B C C”
1
1
3
1
3
1
3
1
1
2
3
5 (collision)
To find the item with the highest number of occurrences, we first take the maximum 
of each row {3, 3, 3, 3, 5} and then the minimum of these maximums “3.” To find the 
item with the second highest number of occurrences, we first take the second highest 
number in each row {1, 1, 1, 2, 5} and then the minimum of these numbers “1.” And so 
on. By taking the minimum, we decrease the chance of overestimation.
There are formulas that help to calculate the width and height based on our desired 
accuracy and the probability we achieve that accuracy. This is outside the scope of this 
book. 
The count-min sketch 2D array replaces the hash table in our previous approaches. 
We will still need a heap to store a list of heavy hitters, but we replace a potentially 
big hash table with a count-min sketch 2D array of predefined size that remains fixed 
regardless of the data set size. 


390
Chapter 17  Design a dashboard of top 10 products on Amazon by sales volume  
17.8	 Dashboard with Lambda architecture
Referring to figure 17.7, our dashboard may be a browser app that makes a GET 
request to a backend service, which in turn runs a SQL query. The discussion so far has 
been about a batch pipeline that writes to batch_table and a streaming pipeline that 
writes to speed_table, and the dashboard should construct the Top K list from both 
tables. 
Dashboard 
browser app
Backend
SQL
Figure 17.7    Our dashboard has a simple architecture, consisting of a browser app that makes GET 
requests to a backend service, which in turn makes SQL requests. The functional requirements of our 
browser app may grow over time, from simply displaying the top 10 lists of a particular period (e.g., the 
previous month), to include larger lists, more periods, filtering, or aggregation (like percentile, mean, 
mode, max, min). 
However, SQL tables do not guarantee order, and filtering and sorting the batch_table 
and speed_table may take seconds. To achieve P99 of <1 second, the SQL query should 
be a simple SELECT query against a single view that contains the list of rankings and 
counts, which we refer to as the top_1000 view. This view can be constructed by selecting the top 1,000 products from the speed_table and batch_table in each period. It 
can also contain an additional column that indicates whether each row is from the 
speed_table or batch_table. When a user requests a Top K dashboard for a particular 
interval, our backend can query this view to obtain as much data from the batch table 
as possible and fill in the blanks with the speed table. Referring to section 4.10, our 
browser app and backend service can also cache the query responses. 
Exercise
As an exercise, define the SQL query for the top_1000 view. 
17.9	 Kappa architecture approach
Kappa architecture is a software architecture pattern for processing streaming data, performing both batch and streaming processing with a single technology stack (https://
hazelcast.com/glossary/kappa-architecture). It uses an append-only immutable log 
like Kafka to store incoming data, followed by stream processing and storage in a database for users to query. 
In this section, we compare Lambda and Kappa architecture and discuss a Kappa 
architecture for our dashboard. 


	
391
Kappa architecture approach
17.9.1	 Lambda vs. Kappa architecture
Lambda architecture is complex because the batch layer and streaming layer each 
require their own code base and cluster, along with associated operational overhead 
and the complexity and costs of development, maintenance, logging, monitoring, and 
alerting. 
Kappa architecture is a simplification of Lambda architecture, where there is only 
a streaming layer and no batch layer. This is akin to performing both streaming and 
batch processing on a single technology stack. The serving layer serves the data computed from the streaming layer. All data is read and transformed immediately after it is 
inserted into the messaging engine and processed by streaming techniques. This makes 
it suitable for low-latency and near real-time data processing like real-time dashboards 
or monitoring. As discussed earlier regarding the Lambda architecture streaming layer, 
we may choose to trade off accuracy for performance. But we may also choose not to 
make this tradeoff and compute highly accurate data. 
Kappa architecture originated from the argument that batch jobs are never 
needed, and streaming can handle all data processing operations and requirements. 
Refer to  https://www.oreilly.com/radar/questioning-the-lambda-architecture/ and 
https://www.kai-waehner.de/blog/2021/09/23/real-time-kappa-architecture 
-mainstream-replacing-batch-lambda/, which discuss the disadvantages of batch and 
how streaming does not have them. 
In addition to the points discussed in these reference links, another disadvantage of 
batch jobs compared to streaming jobs is the former’s much higher development and 
operational overheads because a batch job that uses a distributed file system like HDFS 
tends to take at least minutes to complete even when running on a small amount of 
data. This is due to HDFS’s large block size (64 or 128 MB compared to 4 KB for UNIX 
file systems) to trade off low latency for high throughput. On the other hand, a streaming job processing a small amount of data may only take seconds to complete. 
Batch job failures are practically inevitable during the entire software development 
lifecycle from development to testing to production, and when a batch job fails, it must 
be rerun. One common technique to reduce the amount of time to wait for a batch job 
is to divide it into stages. Each stage outputs data to intermediate storage, to be used as 
input for the next stage. This is the philosophy behind Airflow DAGs. As developers, 
we can design our batch jobs to not take more than 30 minutes or one hour each, but 
developers and operations staff will still need to wait 30 minutes or one hour to see if a 
job succeeded or failed. Good test coverage reduces but does not eliminate production 
problems. 
Overall, errors in batch jobs are more costly than in streaming jobs. In batch jobs, a 
single bug crashes an entire batch job. In streaming, a single bug only affects processing 
of that specific event. 
Another advantage of Kappa vs. Lambda architecture is that the relative simplicity 
of the former, which uses a single processing framework while the latter may require 
different frameworks for its batch and streaming pipelines. We may use frameworks like 
Redis, Kafka, and Flink for streaming. 


392
Chapter 17  Design a dashboard of top 10 products on Amazon by sales volume  
One consideration of Kappa architecture is that storing a large volume of data in an 
event-streaming platform like Kafka is costly and not scalable beyond a few PBs, unlike 
HDFS, which is designed for large volumes. Kafka provides infinite retention with log 
compaction (https://kafka.apache.org/documentation/#compaction), so a Kafka 
topic saves storage by only storing the latest value for each message key and delete all 
earlier values for that key. Another approach is to use object storage like S3 for longterm storage of data that is seldom accessed. Table 17.6 compares Lambda and Kappa 
architecture. 
Table 17.6    Comparison between Lambda and Kappa architecture
Lambda
Kappa
Separate batch and streaming 
pipelines. Separate clusters, 
code bases, and processing 
frameworks. Each needs its own 
infrastructure, monitoring, logs, 
and support. 
Single pipeline, cluster, code 
base, and processing framework. 
Batch pipelines allow faster performance with processing large 
amounts of data. 
Processing large amounts of 
data is slower and more expensive than Lambda architecture. 
However, data is processed as 
soon as it is ingested, in contrast 
to batch jobs which run on a 
schedule, so the latter may provide data sooner. 
An error in a batch job may 
require all the data to be reprocessed from scratch. 
An error in a streaming job only 
requires reprocessing of its 
affected data point. 
17.9.2	 Kappa architecture for our dashboard
A Kappa architecture for our Top K dashboard can use the approach in section 17.3.2, 
where each sales event is aggregated by its product ID and time range. We do not store 
the sales event in HDFS and then perform a batch job. A count of 1M products can easily fit in a single host, but a single host cannot ingest 1B events/day; we need multi-tier 
aggregation. 
A serious bug may affect many events, so we need to log and monitor errors and 
monitor the rate of errors. It will be difficult to troubleshoot such a bug and difficult to 
rerun our streaming pipeline on a large number of events, so we can define a critical 
error rate and stop the pipeline (stop the Kafka consumers from consuming and processing events) if the error rate exceeded this defined critical error rate. 
Figure 17.8 illustrates our high-level architecture with Kappa architecture. It is simply our Lambda architecture illustrated in figure 17.2 without the batch pipeline and 
aggregation service. 


	
393
Other possible discussion topics 
Sales
backend
Streaming 
pipeline
Dashboard
SQL
Shared Logging
Service 
(e.g. ELK or Kafka)
Figure 17.8    Our high-level architecture that uses Kappa architecture. It is simply our Lambda 
architecture in figure 17.2 without the batch pipeline and aggregation service. 
17.10	Logging, monitoring, and alerting 
Besides what was discussed in section 2.5, we should monitor and send alerts for the 
following.
Our shared batch ETL platform should already be integrated with our logging, monitoring, and alerting systems. We will be alerted to unusually long run time or failures of 
any of the tasks within our rollup job. 
The rollup tasks write to HDFS tables. We can use the data quality monitoring tools 
described in chapter 10 to detect invalid datapoints and raise alerts. 
17.11	Other possible discussion topics 
Partition these lists by other characteristics, such as country or city. What design 
changes will we need to return the Top K products by revenue instead of sales volume? 
How can we track the Top K products by change in sales volume and/or revenue? 
It may be useful to look up rankings and statistics of certain products with names or 
descriptions that match patterns. We can design a search system for such use cases. 
We may discuss programmatic users of the Top K lists, such as machine learning and 
experimentation services. We had assumed a low request rate and that high availability 
and low latency were not required. These assumptions will no longer hold as programmatic users introduce new non-functional requirements.
Can our dashboard display approximations for the Top K lists before the events are 
fully counted, or perhaps even before the events occur? 
A considerable complication with counting sales is disputes, such as customer 
requests for refunds or exchanges. Should sale numbers include disputes in progress? 
Do we need to correct the past data to consider refunds, returns, or exchanges? How do 
we recount sales events if refunds are granted or rejected or if there are exchanges for 
the same product or other product(s)? 
We may offer a warranty of several years, so a dispute may occur years after the sale. 
Database queries may need to search for sales events that occurred years before. Such 
jobs may run out of memory. This is a challenging problem that is still faced by many 
engineers to this day.
There may be drastic events, such as a product recall. For example, we may need 
to recall a toy because it was suddenly found to be unsafe to children. We may discuss 
whether the counts of sales events should be adjusted if such problems occur. 
Besides regenerating the Top K lists for the previous reasons, we may generalize this 
to regenerating the Top K lists from any data change.


394
Chapter 17  Design a dashboard of top 10 products on Amazon by sales volume  
Our browser app only displays the Top K list. We can extend our functional requirements, such as displaying sales trends or predicting future sales of current or new 
products. 
17.12	References 
This chapter used material from the Top K Problem (Heavy Hitters) (https://youtu.be/ 
kx-XDoPjoHw) presentation in the System Design Interview YouTube channel by 
Mikhail Smarshchok.
Summary
¡ When accurate large-scale aggregation operations take too long, we can run a 
parallel streaming pipeline that uses approximation techniques to trade off accuracy for speed. Running a fast, inaccurate and a slow, accurate pipeline in parallel 
is called Lambda architecture.
¡ One step in large-scale aggregation is to partition by a key that we will later aggregate over.
¡ Data that is not directly related to aggregation should be stored in a different 
service, so it can be easily used by other services.
¡ Checkpointing is one possible technique for distributed transactions that involve 
both destinations with cheap read operations (e.g., Redis) and expensive read 
operations (e.g., HDFS).
¡ We can use a combination of heaps and multi-tier horizontal scaling for approximate large-scale aggregation operations.
¡ Count-min sketch is an approximation technique for counting.
¡ We can consider either Kappa or Lambda architecture for processing a large 
data stream. 


395
A
Monoliths 
vs. microservices
This appendix evaluates monoliths vs. microservices. The author’s personal experience is that it seems many sources describe the advantages of microservice over 
monolith architecture but do not discuss the tradeoffs, so we will discuss them here. 
We use the terms “service” and “microservice” interchangeably. 
Microservice architecture is about building a software system as a collection of loosely-coupled and independently developed, deployed, and scaled services. Monoliths 
are designed, developed, and deployed as a single unit. 
A.1	
Advantages of monoliths 
Table A.1 discusses the advantages of monoliths over services. 


396
Appendix A  Monoliths vs. microservices 
Table A.1    Advantages of monoliths over services
Monolith
Service
Faster and easier to develop at first 
because it is a single application. 
Developers need to handle serialization and deserialization in 
every service, and handle requests and responses between the 
services.
Before we begin development, we first need to decide where the 
boundaries between the services should be, and our chosen 
boundaries may turn out to be wrong. Redeveloping services to 
change their boundaries is usually impractical. 
A single database means it uses less 
storage, but this comes with tradeoffs.
Each service should have its own database, so there may be 
duplication of data and overall greater storage requirements.
With a single database and fewer data 
storage locations in general, it may 
be easier to comply with data privacy 
regulations.
Data is scattered in many locations, which makes it more difficult to ensure that data privacy regulations are complied with 
throughout the organization.
Debugging may be easier. A developer 
can use breakpoints to view the function call stack at any line of code and 
understand all logic that is happening 
at that line.
Distributed tracing tools like Jaegar or Zipkin are used to understand request fan-out, but they do not provide many details, 
such as the function call stack of the services involved in the 
request. Debugging across services is generally harder than in a 
monolith or individual service.
Related to the previous point, being 
able to easily view all the code in a 
single location and trace function calls 
may make the application/system as a 
whole generally easier to understand 
than in a service architecture.
A service’s API is presented as a black box. While not having to 
understand an API’s details may make it easier to use, it may 
become difficult to understand many of the fine details of the 
system.
Cheaper to operate and better performance. All processing occurs within the 
memory of a single host, so there are 
no data transfers between hosts, which 
are much slower and more expensive. 
A system of services that transfer large amounts of data 
between each other can incur very high costs from the data 
transfers between hosts and data centers. Refer to https://
www.primevideotech.com/video-streaming/scaling-up-the 
-prime-video-audio-video-monitoring-service-and-reducing 
-costs-by-90 for a discussion on how an Amazon Prime Video 
reduced the infrastructure costs of a system by 90% by merging 
most (but not all) of their services in a distributed microservices 
architecture into a monolith.
A.2	
Disadvantages of monoliths 
Monoliths have the following disadvantages compared to microservices: 
¡ Most capabilities cannot have their own lifecycles, so it is hard to practice Agile 
methodologies. 
¡ Need to redeploy the entire application to apply any changes. 
¡ Large bundle size. High resource requirements. Long startup time. 
¡ Must be scaled as a single application. 
¡ A bug or instability in any part of a monolith can cause failures in production. 


	
397
Advantages of services 
¡ Must be developed with a single language, so it cannot take advantage of the 
capabilities offered by other languages and their frameworks in addressing 
requirements of various use cases. 
A.3	
Advantages of services 
The advantages of services over monoliths include the following:
1	 Agile and rapid development and scaling of product requirements/business 
functionalities.
2	 Modularity and replaceability.
3	 Failure isolation and fault-tolerance.
4	 More well-defined ownership and organizational structure. 
A.3.1	
Agile and rapid development and scaling of product requirements and business 
functionalities
Designing, implementing, and deploying software to satisfy product requirements is 
slower with a monolith than a service because the monolith has a much bigger codebase and more tightly coupled dependencies. 
When we develop a service, we can focus on a small set of related functionalities and 
the service’s interface to its users. Services communicate via network calls through the 
service interfaces. In other words, services communicate via their defined APIs over 
industry-standard protocols such as HTTP, gRPC, and GraphQL. Services have obvious 
boundaries in the form of their APIs, while monoliths do not. In a monolith, it is far 
more common for any particular piece of code to have numerous dependencies scattered throughout the codebase, and we may have to consider the entire system when 
developing in a monolith. 
With cloud-based container native-infrastructure, a service can be developed and 
deployed much quicker than comparable features in a monolith. A service that provides a well-defined and related set of capabilities may be CPU-intensive or memory-intensive, and we can select the optimal hardware for it, cost-efficiently scaling it up or 
down as required. A monolith that provides many capabilities cannot be scaled in a 
manner to optimize for any individual capability. 
Changes to individual services are deployed independently of other services. Compared to a monolith, a service has a smaller bundle size, lower resource requirements, 
and faster startup time. 
A.3.2	
Modularity and replaceability 
The independent nature of services makes them modular and easier to replace. We 
can implement another service with the same interface and swap out the existing service with the new one. In a monolith, other developers may be changing code and 
interfaces at the same time as us, and it is more difficult to coordinate such development vs. in a service. 


398
Appendix A  Monoliths vs. microservices 
We can choose technologies that best suit the service’s requirements (e.g., a specific 
programming language for a frontend, backend, mobile, or analytics service). 
A.3.3	
Failure isolation and fault-tolerance 
Unlike a monolith, a microservices architecture does not have a single point of failure. Each service can be separately monitored, so any failure can be immediately 
narrowed down to a specific service. In a monolith, a single runtime error may crash 
the host, affecting all other functionalities. A service that adopts good practices for 
fault-tolerance can adapt to high latency and unavailability of the other services that 
it is dependent on. Such best practices are discussed in section 3.3, including caching 
other services’ responses or exponential backoff and retry. The service may also return 
a sensible error response instead of crashing.
Certain services are more important than others. For example, they may have a more 
direct effect on revenue or are more visible to users. Having separate services allows us 
to categorize them by importance and allocate development and operations resources 
accordingly. 
A.3.4	
Ownership and organizational structure 
With their well-defined boundaries, mapping the ownership of services to teams is 
straightforward compared to monoliths. This allows concentration of expertise and 
domain knowledge; that is, a team that owns a particular service can develop a strong 
understanding of it and expertise in developing it. The flip side is that developers are 
less likely to understand other services and possess less understanding and ownership 
of the overall system, while a monolith may force developers to understand more of 
the system beyond the specific components that they are responsible to develop and 
maintain. For example, if a developer requires some changes in another service, they 
may request the relevant team to implement those changes rather than doing so themselves, so development time and communication overhead are higher. Having those 
changes done by developers familiar with the service may take less time and have a 
lower risk of bugs or technical debt. 
The nature of services with their well-defined boundaries also allows various service 
architectural styles to provide API definition techniques, including OpenAPI for REST, 
protocol buffers for gRPC, and Schema Definition Language (SDL) for GraphQL. 
A.4	
Disadvantages of services 
The disadvantages of services compared to monoliths include duplicate components 
and the development and maintenance costs of additional components. 
A.4.1	
Duplicate components 
Each service must implement inter-service communication and security, which is 
mostly duplicate effort across services. A system is as strong as its weakest point, and the 
large number of services exposes a large surface area that must be secured, compared 
to a monolith. 


	
399
Disadvantages of services 
Developers in different teams who are developing duplicate components may also 
duplicate mistakes and the efforts needed to discover and fix these mistakes, which is 
development and maintenance waste. This duplication of effort and waste of time also 
extends to users and operations staff of the duplicate services who run into the bugs 
caused by these mistakes, and expend duplicate effort into troubleshooting and communicating with developers. 
Services should not share databases, or they will no longer be independent. For 
example, a change to a database schema to suit one service will break other services. 
Not sharing databases may cause duplicate data and lead to an overall higher amount 
and cost of storage in the system. This may also make it more complex and costly to 
comply with data privacy regulations. 
A.4.2	
Development and maintenance costs of additional components 
To navigate and understand the large variety of services in our organization, we will 
need a service registry and possibly additional services for service discovery. 
A monolithic application has a single deployment lifecycle. A microservice application has numerous deployments to manage, so CI/CD is a necessity. This includes 
infrastructure like containers (Docker), container registry, container orchestration 
(Kubernetes, Docker Swarm, Mesos), CI tools such as Jenkins, and CD tools, which may 
support deployment patterns like blue/green deployment, canary, and A/B testing. 
When a service receives a request, it may make requests to downstream services in 
the process of handling this request, which in turn may make requests to further downstream services. This is illustrated in figure A.1. A single request to Netflix’s homepage 
causes a request to fan out to numerous downstream services. Each such request adds 
networking latency. A service’s endpoint may have a one-second P99 SLA, but if multiple endpoints are dependencies of each other (e.g., service A calls service B, which calls 
service C, and so on), the original requester may experience high latency. 
Figure A.1    Illustration of request fan-out to downstream services that occurs on a request to get 
Netflix’s homepage. Image from https://www.oreilly.com/content/application-caching-at-netflix-the 
-hidden-microservice/. 


400
Appendix A  Monoliths vs. microservices 
Caching is one way to mitigate this, but it introduces complexity, such as having to consider cache expiry and cache refresh policies to avoid stale data, and the overhead of 
developing and maintaining a distributed cache service. 
A service may need the additional complexity and development and maintenance 
costs of implementing exponential backoff and retry (discussed in section 3.3.4) to 
handle outages of other services that it makes requests to. 
Another complex additional component required by microservices architecture is distributed tracing, which is used for monitoring and troubleshooting microservices-based distributed systems. Jaeger and Zipkin are popular distributed tracing 
solutions. 
Installing/updating a library on a monolith involves updating a single instance of 
that library on the monolith. With services, installing/updating a library that is used 
in multiple services will involve installing/updating it across all these services. If an 
update has breaking changes, each service’s developers manually update their libraries 
and update broken code or configurations caused by backward incompatibility. Next, 
they must deploy these updates using their CI/CD (continuous integration/continuous deployment) tools, possibly to several environments one at a time before finally 
deploying to the production environment. They must monitor these deployments. 
Along the way in development and deployment, they must troubleshoot any unforeseen problems. This may come down to copying and pasting error messages to search 
for solutions on Google or the company’s internal chat application like Slack or Microsoft Teams. If a deployment fails, the developer must troubleshoot and then retry the 
deployment and wait for it again to succeed or fail. Developers must handle complex 
scenarios (e.g., persistent failures on a particular host) All of this is considerable developer overhead. Moreover, this duplication of logic and libraries may also add up to a 
non-trivial amount of additional storage. 
A.4.3	
Distributed transactions 
Services have separate databases, so we may need distributed transactions for consistency across these databases, unlike a monolith with a single relational database that 
can make transactions against that database. Having to implement distributed transactions is yet another source of cost, complexity, latency, and possible errors and failures. 
Chapter 5 discussed distributed transactions. 
A.4.4	
Referential integrity 
Referential integrity refers to the accuracy and consistency of data within a relationship. 
If a value of one attribute in a relation references a value of another attribute and then 
the referenced value must exist. 
Referential integrity in a monolith’s single database can be easily implemented using 
foreign keys. Values in a foreign key column must either be present in the primary 
key that is referenced by the foreign key, or they must be null (https://www.interfacett 
.com/blogs/referential-integrity-options-cascade-set-null-and-set-default). Referential 
integrity is more complicated if the databases are distributed across services. For 


	
401
Disadvantages of services 
referential integrity in a distributed system, a write request that involves multiple services must succeed in every service or fail/abort/rollback in every service. The write 
process must include steps such as retries or rollbacks/compensating transactions. 
Refer to chapter 5 for more discussion of distributed transactions. We may also need a 
periodic audit across the services to verify referential integrity. 
A.4.5	
Coordinating feature development and deployments that span multiple services 
If a new feature spans multiple services, development and deployment need to be 
coordinated between them. For example, one API service may be dependent on others. In another example, the developer team of a Rust Rocket (https://rocket.rs/) 
RESTful API service may need to develop new API endpoints to be used by a React UI 
service, which is developed by a separate team of UI developers. Let’s discuss the latter 
example. 
In theory, feature development can proceed in parallel on both services. The API 
team need only provide the specification of the new API endpoints. The UI team can 
develop the new React components and associated node.js or Express server code. Since 
the API team has not yet provided a test environment that returns actual data, the server 
code or mock or stub responses from the new API endpoints and use them for development. This approach is also useful for authoring unit tests in the UI code, including spy 
tests (refer to https://jestjs.io/docs/mock-function-api for more information). 
Teams can also use feature flags to selectively expose incomplete features to development and staging environments, while hiding them from the production environment. 
This allows other developers and stakeholders who rely on these new features to view 
and discuss the work in progress. 
In practice, the situation can be much more complicated. It can be difficult to understand the intricacies of a new set of API endpoints, even by developers and UX designers with considerable experience in working with that API. Subtle problems can be 
discovered by both the API developers and UI developers during the development of 
their respective services, the API may need to change, and both teams must discuss a 
solution and possibly waste some work that was already done: 
¡ The data model may be unsuitable for the UX. For example, if we develop a 
version control feature for templates of a notifications system (refer to section 
9.5), the UX designer may design the version control UX to consider individual 
templates. However, a template may actually consist of subcomponents that are 
versioned separately. This confusion may not be discovered until both UI and 
API development are in progress. 
¡ During development, the API team may discover that the new API endpoints 
require inefficient database queries, such as overly large SELECT queries or 
JOIN operations between large tables. 
¡ For REST or RPC APIs (i.e., not GraphQL), users may need to make multiple 
API requests and then do complex post-processing operations on the responses 
before the data can be returned to the requester or displayed on the UI. Or the 


402
Appendix A  Monoliths vs. microservices 
provided API may fetch much more data than required by the UI, which causes 
unnecessary latency. For APIs that are developed internally, the UI team may 
wish to request some API redesign and rework for less complex and more efficient API requests. 
A.4.6	
Interfaces 
Services can be written in different languages and communicate with each other via a 
text or binary protocol. In the case of text protocols like JSON or XML, these strings 
need to be translated to and from objects. There is additional code required for validation and error and exception handling for missing fields. To allow graceful degradation, our service may need to process objects with missing fields. To handle the case of 
our dependent services returning such data, we may need to implement backup steps 
such as caching data from dependent services and returning this old data, or perhaps 
also return data with missing fields ourselves. This may cause implementation to differ 
from documentation.
A.5	
References
This appendix uses material from the book Microservices for the Enterprise: Designing, 
Developing, and Deploying by Kasun Indrasiri and Prabath Siriwardena (2018, Apress).


403
B
OAuth 2.0 authorization 
and OpenID Connect 
authentication1
B.1	
Authorization vs. authentication 
Authorization is the process of giving a user (a person or system) permission to access 
a specific resource or function. Authentication is identity verification of a user. OAuth 
2.0 is a common authorization algorithm. (The OAuth 1.0 protocol was published 
in April 2010, while OAuth 2.0 was published in October 2012.) OpenID Connect is 
an extension to OAuth 2.0 for authentication. Authentication and authorization/
access control are typical security requirements of a service. OAuth 2.0 and OpenID 
Connect may be briefly discussed in an interview regarding authorization and 
authentication. 
A common misconception online is the idea of “login with OAuth2.” Such online 
resources mix up the distinct concepts of authorization and authentication. This 
section is an introduction to authorization with OAuth2 and authentication with 
OpenID Connect and makes their authorization versus authentication distinction 
clear. 
1	 This section uses material from the video “OAuth 2.0 and OpenID Connect (in plain English),” http:// 
oauthacademy.com/talk, an excellent introductory lecture by Nate Barbettini, and https://auth0.com/docs. 
Also refer to https://oauth.net/2/ for more information.


404
Appendix B  OAuth 2.0 authorization and OpenID Connect authentication 
B.2	
Prelude: Simple login, cookie-based authentication
The most basic type of authentication is commonly referred to as simple login, basic 
authentication, or forms authentication. In simple login, a user enters an (identifier, password) pair. Common examples are (username, password) and (email, password). 
When a user submits their username and password, the backend will verify that the 
password is correct for the associated username. Passwords should be salted and 
hashed for security. After verification, the backend creates a session for this user. The 
backend creates a cookie that will be stored in both the server’s memory and in the 
user’s browser. The UI will set a cookie in the user’s browser, such as Set-Cookie: sessionid=f00b4r; Max-Age: 86400;. This cookie contains a session ID. Further requests 
from the browser will use this session ID for authentication, so the user does not have 
to enter their username and password again. Each time the browser makes a request to 
the backend, the browser will send the session ID to the backend, and the backend will 
compare this sent session ID to its own copy to verify the user’s identity. 
This process is called cookie-based authentication. A session has a finite duration, after 
which it expires/times out and the user must reenter their username and password. 
Session expiration has two types of timeouts: absolute and inactivity. Absolute timeout 
terminates the session after a specified period has elapsed. Inactivity timeout terminates 
the solution after a specified period during which a user has not interacted with the 
application. 
B.3	
Single sign-on 
Single sign-on (SSO) allows one to log in to multiple systems with a single master 
account, such as an Active Directory account. SSO is typically done with a protocol 
called Security Assertion Markup Language (SAML). The introduction of mobile apps 
in the late 2000s necessitated the following: 
¡ Cookies are unsuitable for devices, so a new mechanism was needed for longlived sessions, where a user remains logged into a mobile app even after they 
close the app. 
¡ A new use case called delegated authorization. The owner of a set of resources can 
delegate access to some but not all of these resources to a designated client. For 
example, one may grant a certain app permission to see certain kinds of their 
Facebook user information, such as their public profile and birthday, but not 
post on your wall. 
B.4	
Disadvantages of simple login 
The disadvantages of simple login include complexity, lack of maintainability, and no 
partial authorization. 


	
405
Disadvantages of simple login 
B.4.1	
Complexity and lack of maintainability 
Much of a simple login (or session-based authentication in general) is implemented by 
the application developer, including the following: 
¡ The login endpoint and logic, including the salting and hashing operations 
¡ The database table of usernames and salted+hashed passwords 
¡ Password creation and reset, including 2FA operations such as password reset 
emails 
This means that the application developer is responsible for observing security best 
practices. In OAuth 2.0 and OpenID Connect, passwords are handled by a separate 
service. (This is true of all token-based protocols. OAuth 2.0 and OpenID Connect are 
token-based protocols.) The application developer can use a third-party service that 
has good security practices, so there is less risk of passwords being hacked.
Cookies require a server to maintain state. Each logged-in user requires the server to 
create a session for it. If there are millions of sessions, the memory overhead may be too 
expensive. Token-based protocols have no memory overhead. 
The developer is also responsible for maintaining the application to stay in compliance with relevant user privacy regulations such as the General Data Protection Regulation (GDPR), California Consumer Privacy Act (CCPA), and the Health Insurance 
Portability and Accountability Act (HIPAA). 
B.4.2	
No partial authorization 
Simple login does not have the concept of partial access control permissions. One may 
wish to grant another party partial access to the former’s account for specific purposes. 
Granting complete access is a security risk. For example, one may wish to grant a budgeting app like Mint permission to see their bank account balance, but not other permissions like transferring money. This is impossible if the bank app only has simple 
login. The user must pass their bank app account’s username and password to Mint, 
giving Mint complete access to their bank account, just for Mint to view their bank 
balance. 
Another example was Yelp before the development of OAuth. As illustrated in figure 
B.1, at the end of one’s Yelp user registration, Yelp will request the user for their Gmail 
login, so it can send a referral link or invite link to their contact list. The user has to 
grant Yelp complete access to their Gmail account just to send a single referral email to 
each of their contacts. 


406
Appendix B  OAuth 2.0 authorization and OpenID Connect authentication 
Figure B.1    Screenshot of Yelp’s browser app referral feature prior to OAuth, reflecting a shortcoming of 
no partial authorization in simple login. The user is requested to enter their email address and password, 
granting Yelp full permissions to their email account even though Yelp only wishes to send a single email 
to each of their contacts. Image from http://oauthacademy.com/talk. 
OAuth 2.0 adoption is now widespread, so most apps do not use such practices anymore. A significant exception is the banking industry. As of 2022, most banks have not 
adopted OAuth. 
B.5	
OAuth 2.0 flow 
This section describes an OAuth 2.0 flow, how an app like Google can use OAuth 2.0 
for users to authorize apps like Yelp to access resources belonging to a Google user, 
such as send emails to a user’s Google contacts. 
Figure B.2 illustrates the steps in an OAuth 2.0 flow between Yelp and Google. We 
closely follow figure B.2 in this chapter.
Yes
No
Allow Yelp to access your
public profile and contacts?
accounts.google.com
yelp.com/callback
contacts.google.com
Email
Password
accounts.google.com
yelp.com
Client
Resource
owner
Authorization Server
Redirect URL:
yelp.com/callback
Request resources
with access token.
Exchange
authorization
code for
access token.
Go to redirect
URI with 
authorization code.
Request consent
from resource owner.
Figure B.2    Illustration of OAuth2 flow, discussed in detail through this section. Front-channel 
communications are represented by solid lines. Back-channel communications are represented by 
dashed lines. 


	
407
OAuth 2.0 flow 
B.5.1	
OAuth 2.0 terminology 
¡ Resource owner—The user who owns the data or controls certain operations that 
the application is requesting for. For example, if you have contacts in your Google account, you are the resource owner of that data. You can grant permission to 
an application to access that data. In this section, we refer to a resource owner as 
a user for brevity. 
¡ Client—The application that is requesting the resources. 
¡ Authorization server—The system the user uses to authorize the permission, such 
as accounts.google.com. 
¡ Resource server—API of the system that holds the data the client wants, such as the 
Google Contacts API. Depending on the system, the authorization server and 
resource server may be the same or separate systems. 
¡ Authorization grant—The proof of the user’s consent to the permission necessary 
to access the resources. 
¡ Redirect URI, also called callback—The URI or destination when the authorization 
server redirects back to the client. 
¡ Access token—The key that the client uses to get the authorized resource. 
¡ Scope—The authorization server has a list of scopes that it understands (e.g., read 
a user’s Google contacts list, read emails, or delete emails). A client may request a 
certain set of scopes, depending on its required resources. 
B.5.2	
Initial client setup 
An app (like Mint or Yelp) has to do a one-time setup with the authorization server 
(like Google) to become a client and enable users to use OAuth. When Mint requests 
Google to create a client Google provides:
¡ Client ID, which is typically a long, unique string identifier. This is passed with 
the initial request on the front channel. 
¡ Client secret, which is used during token exchange. 
1. Get authorization from the user 
The flow begins with the (Google) resource owner on the client app (Yelp). Yelp 
displays a button for a user to grant access to certain data on their Google account. 
Clicking that button puts the user through an OAuth flow, a set of steps that results 
in the application having authorization and being able to access only the requested 
information. 
When the user clicks on the button, the browser is redirected to the authorization 
server (e.g., a Google domain, which may be accounts.google.com, or a Facebook or 
Okta authorization server). Here, the user is prompted to log in (i.e., enter their email 
and password and click Login). They can see in their browser’s navigation bar that they 


408
Appendix B  OAuth 2.0 authorization and OpenID Connect authentication 
is in a Google domain. This is a security improvement, as they provide their email and 
password to Google, rather than another app like Mint or Yelp. 
In this redirect, the client passes configuration information to the authorization 
server via a query with a URL like “https://accounts.google.com/o/oauth2/v2/
auth?client_id=yelp&redirect_uri=https%3A%2F%2Foidcdebugger.com%2Fdebug&-
scope=openid&response_type=code&response_mode=query&state=foobar&nonce=uwtukpm946m”. The query parameters are: 
¡ client_id—Identifies the client to the authorization server; for example, tells Google that Yelp is the client. 
¡ redirect_uri (also called callback URI)—The redirect URI. 
¡ scope—The list of requested scopes. 
¡ response_type—The type of authorization grant the client wants. There are a few 
different types, to be described shortly. For now, we assume the most common 
type, called an authorization code grant. This is a request to the authorization 
server for a code. 
¡ state—The state is passed from the client to the callback. As discussed in step 4 
below, this prevents cross-site request forgery (CSRF) attacks. 
¡ nonce—Stands for “number used once.” A server-provided random value used 
to uniquely label a request to prevent replay attacks (outside the scope of this 
book). 
2. User consents to client’s scope 
After they log in, the authorization server prompts the user to consent to the client’s 
requested list of scopes. In our example, Google will present them with a prompt that 
states the list of resources that the other app is requesting (such as their public profile 
and contact list) and a request for confirmation that they consent to granting these 
resources to that app. This ensures they are not tricked into granting access to any 
resource that they did not intend to grant.
Regardless of whether they click “no” or “yes,” the browser is redirected back to the 
app’s callback URI with different query parameters depending on the user’s decision. If 
they click “no,” the app is not granted access. The redirect URI may be something like 
“https://yelp.com/callback?error=access_denied&error_description=The user did 
not consent.” If they click “yes,” the app can request the user’s granted resources from 
a Google API such as the Google Contacts API. The authorization server redirects to 
the redirect URI with the authorization code. The redirect URI may be something like 
https://yelp.com/callback?code=3mPDQbnIOyseerTTKPV&state=foobar, where the 
query parameter “code” is the authorization code. 
3. Request access token 
The client sends a POST request to the authorization server to exchange the authorization code for an access token, which includes the client’s secret key (that only the 
client and authorization server know). Example: 


	
409
OAuth 2.0 flow 
POST www.googleapis.com/oauth2/v4/token 
Content-Type: application/x-www-form-urlencoded 
code=3mPDQbnIOyseerTTKPV&client_id=yelp&client_secret=secret123&grant_
type=authorization_code 
The authorization server validates the code and then responds with the access token, 
and the state that it received from the client. 
4. Request resources 
To prevent CSRF attacks, the client verifies that the state it sent to the server is identical to the state in the response. Next, the client uses the access token to request the 
authorized resources from the resource server. The access token allows the client to 
access only the requested scope (e.g., read-only access to the user’s Google contacts). 
Requests for other resources outside the scope or in other scopes will be denied (e.g., 
deleting contacts or accessing the user’s location history): 
ET api.google.com/some/endpoint 
Authorization: Bearer h9pyFgK62w1QZDox0d0WZg 
B.5.3	
Back channel and front channel 
Why do we get an authorization code and then exchange it for the access token? Why 
don’t we just use the authorization code, or just get the access token immediately? 
We introduce the concepts of a back channel and a front channel, which are network 
security terminology. 
Front-channel communication is communication between two or more parties that are 
observable within the protocol. Back-channel communication is communication that is 
not observable to at least one of the parties within the protocol. This makes back channel more secure than front channel. 
An example of a back channel or highly secure channel is a SSL-encrypted HTTP 
request from the client’s server to a Google API server. An example of a front channel 
is a user’s browser. A browser is secure but has some loopholes or places where data may 
leak from the browser. If you have a secret password or key in your web application and 
put it in the HTML or JavaScript of a web app, this secret is visible to someone who views 
the page source. The hacker can also open the network console or Chrome Developer 
Tools and see and modify the JavaScript. A browser is considered to be a front channel 
because we do not have complete trust in it, but we have complete trust in the code that 
is running on our backend servers. 
Consider a situation where the client is going over to the authorization server. This is 
happening in the front channel. The full-page redirects, outgoing requests, redirect to 
the authorization server, and content of the request to the authorization server are all 
being passed through the browser. The authorization code is also transmitted through 
the browser (i.e., the front channel). If this authorization code was intercepted, for 
example, by a malicious toolbar or a mechanism that can log the browser requests, the 
hacker cannot obtain the access code because the token exchange happens on the back 
channel. 


410
Appendix B  OAuth 2.0 authorization and OpenID Connect authentication 
The token exchange happens between the backend and the authorization channel, 
not the browser. The backend also includes its secret key in the token exchange, which 
the hacker does not know. If the transmission of this secret key is via the browser, the 
hacker can steal it, so the transmission happens via the back channel. 
The OAuth 2.0 flow is designed to take advantage of the best characteristics of the 
front channel and back channel to ensure it is highly secure. The front channel is used 
to interact with the user. The browser presents the user the login screen and consent 
screen because it is meant to interact directly with the user and present these screens. 
We cannot completely trust the browser with secret keys, so the last step of the flow (i.e., 
the exchange, happens on the back channel, which is a system we trust). 
The authorization server may also issue a refresh token to allow a client to obtain a 
new access token if the access token is expired, without interacting with the user. This is 
outside the scope of this book. 
B.6	
Other OAuth 2.0 flows 
We described the authorization code flow, which involves both back channel and front 
channel. The other flows are the implicit flow (front channel only), resource owner 
password credentials (back channel only), and client credentials (back channel only). 
An implicit flow is the only way to use OAuth 2.0 if our app does not have a backend. 
Figure B.3 illustrates an example of implicit flow. All communications are front channel only. The authorization server returns the access code directly, with no authorization code and no exchange step. 
Yes
No
contacts.google.com
Email
Password
Yelp pure React app
Client
Authorization Server
yelp.com/callback
Hello!
Request resources
with access token.
Allow Yelp to access your
public profile and contacts?
accounts.google.com
accounts.google.com
Request consent
from resource owner.
Redirect URL:
yelp.com/callback
Response type: token
Scope: profile contacts
Go to redirect URI
with token.
Resource
owner
Figure B.3    Illustration of an OAuth2 implicit flow. All communications are front channel. Note that the 
request to the authorization server has response type “token” instead of “code.”


	
411
OpenID Connect authentication 
Implicit flow carries a security tradeoff because the access token is exposed to the 
browser.
The resource owner password flow or resource owner password credentials flow is 
used for older applications and is not recommended for new applications. The backend server uses its credentials to request the authorization server for an access token. 
The client credentials flow is sometimes used when you’re doing a machine-to-machine 
or service communications. 
B.7	
OpenID Connect authentication 
The Login with Facebook button was introduced in 2009, followed by the Login with 
Google button and similar buttons by many other companies like Twitter, Microsoft, 
and LinkedIn. One could login to a site with your existing credentials with Facebook, 
Google, or other social media. These buttons became ubiquitous across the web. The 
buttons served the login use cases well and were built with OAuth 2.0 even though 
OAuth 2.0 was not designed to be used for authentication. Essentially, OAuth 2.0 was 
being used for its purpose beyond delegated authorization. 
However, using OAuth for authentication is bad practice because there is no way 
of getting user information in OAuth. If you log in to an app with OAuth 2.0, there is 
no way for that app to know who just logged in or other information like your email 
address and name. OAuth 2.0 is designed for permissions scopes. All it does is verify that 
your access token is scoped to a particular resource set. It doesn’t verify who you are. 
When the various companies built their social login buttons, using OAuth under the 
hood, they all had to add custom hacks on top of OAuth to allow clients to get the user’s 
information. If you read about these various implementations, keep in mind that they 
are different and not interoperable. 
To address this lack of standardization, OpenID Connect was created as a standard 
for adopting OAuth 2.0 for authentication. OpenID Connect is a thin layer on top of 
OAuth 2.0 that allows it to be used for authentication. OpenID Connect adds the following to OAuth 2.0: 
¡ ID token—The ID token represents the user’s ID and has some user information. 
This token is returned by the authorization server during token exchange. 
¡ User info endpoint—If the client wants more information than contained in the 
ID token returned by the authorization server, the client can request more user 
information from the user info endpoint. 
¡ Standard set of scopes.
So, the only technical difference between OAuth 2.0 and OpenID Connect is that 
OpenID Connect returns both an access code and ID token, and OpenID Connect 
provides a user info endpoint. A client can request the authorization server for an 
OpenID scope in addition to its desired OAuth 2.0 scopes and obtain both an access 
code and ID token. 


412
Appendix B  OAuth 2.0 authorization and OpenID Connect authentication 
Table B.1 summarizes the use cases of OAuth 2.0 (authorization) vs. OpenID Connect (authentication). 
Table B.1    Use cases of OAuth 2.0 (authorization) vs. OpenID Connect (authentication)
OAuth2 (authorization)
OpenID Connect (authentication)
Grant access to your API.
User login
Get access to user data in other systems.
Make your accounts available in other systems.
An ID token consists of three parts: 
¡ Header—Contains several fields, such as the algorithm used to encode the 
signature. 
¡ Claims—The ID token body/payload. The client decodes the claims to obtain the 
user information. 
¡ Signature—The client can use the signature to verify that the ID token has not 
been changed. That is, the signature can be independently verified by the client 
application without having to contact the authorization server. 
The client can also use the access token to request the authorization server’s user info 
endpoint for more information about the user, such as the user’s profile picture. Table 
B.2 describes which grant type to use for your use case. 
Table B.2    Which grant type to use for your use case
Web application with server backend
Authorization code flow
Native mobile app
Authorization code flow with PKCE 
(Proof Key for Code Exchange) (outside 
the scope of this book)
JavaScript Single-Page App (SPA) with 
API backend
Implicit flow
Microservices and APIs
Client credentials flow


413
C
The C4 model (https://c4model.com/) is a system architecture diagram technique 
created by Simon Brown to decompose a system into various levels of abstraction. 
This section is a brief introduction to the C4 model. The website has good introductions and in-depth coverage of the C4 model, so we will only briefly go over the 
C4 model here; readers should refer to the website for more details. The C4 model 
defines four levels of abstraction.
A context diagram represents the system as a single box, surrounded by its users 
and other systems that it interacts with. Figure C.1 is an example context diagram 
of a new internet banking system that we wish to design on top of our existing mainframe banking system. Its users will be our personal banking customers, who will use 
our internet banking system via UI apps we develop for them. Our internet banking 
system will also use our existing email system. In figure C.1, we draw our users and 
systems as boxes and connect them with arrows to represent the requests between 
them. 
C4 Model


414
Appendix C  C4 Model
Personal Banking Customer
(Person)
A customer of the bank, with
personal bank accounts.
Email System
(Software System)
The internal Microsoft
Exchange email system
Mainframe Banking System
(Software System)
Stores all of the core banking
information about customers,
acounts, transactions, etc.
Internet Banking System
(Software System)
Allows costumers to view 
information about their bank
accounts, and make payments
Views account balances, and makes payments using
Sends emails to
Sends email using
Gets account information from, and makes payments using
Figure C.1    A context diagram. Image from https://c4model.com/, licensed under https://
creativecommons.org/licenses/by/4.0/. In this case, we want to design an internet banking system. 
Its users are our personal banking customers, who are people using our internet banking system via the 
latter’s UI apps. Our internet banking system makes requests to our legacy mainframe banking system. It 
also uses our existing email system to email our users. Many of the other shared services it may use are 
not available yet, and may be discussed as part of this design. 
A container diagram is defined on c4model.com as “a separately runnable/deployable 
unit that executes code or stores data.” We can also understand containers as the services that make up our system. Figure C.2 is an example container diagram. We break 
up our internet banking system that we represented as a single box in figure C.1. 
A web/browser user can download our single-page (browser) app from our web 
application service and then make further requests through this single-page app. A 
mobile user can download our mobile app from an app store and make all requests 
through this app. 
Our browser and mobile apps make requests to our (backend) API application/service. Our backend service makes requests to its Oracle SQL database, mainframe banking system, and our email system. 
A component diagram is a collection of classes behind an interface to implement a 
functionality. Components are not separately deployable units. Figure 6.3 is an example 
component diagram of our (backend) API application/service from figure 6.2, illustrating its interfaces and classes, and their requests with other services.
Our browser and mobile apps make requests to our backend, which are routed to the 
appropriate interfaces:


	
415
﻿
Personal Banking Customer
(Person)
A costumer of the bank, with
personal bank account
Web Application
(Container: Java and 
Spring MVC)
Delivers the static
content and the Internet
banking single page
application
Single-Page Application
(Container: JavaScript
and Angular)
Provides all of the Internet
banking functionality to
customers via their web
browser.
Mobile App
(Container: Xamarin)
Provides a limited 
subset of the Internet
banking functionality to
customers via their
mobile device.
Email System
(Softwear System)
The internal
Microsoft Exchange
email system
Mainframe
Banking System
(Softwear System)
Stores all of the core
banking information
about customers,
accounts, transactions,
etc.
API Application
(Container: Java and Spring MVC)
Provides Internet banking
functionality via a JSON/HTTPS API.
Database
(Container: OracleDatabase Schema)
Stores user registration information,
hashed authentication credentials,
access logs, etc.
Internet Banking System
(Softwear System)
Visits
(HTTPS)
Sends emails to
View account 
balances, and makes 
payments using
Delivers to the
customer’s web browser.
Database requests
(JDBC)
API calls
(JSON/HTTPS)
Sends email using
API calls
(JSON/HTTPS)
Figure C.2     A container diagram. Adapted from https://c4model.com/, licensed under https://
creativecommons.org/licenses/by/4.0/.
Our sign-in controller receives sign in requests. Our reset password controller receives 
password reset requests. Our security component has functions to process these security-related functionalities from the sign-in controller and reset password controller. It 
persists data to an Oracle SQL database.


416
Appendix C  C4 Model
Our email component is a client that makes requests to our email system. Our reset 
password controller uses our email component to send password reset emails to our 
users. 
Our account summary controller provides users with their bank account balance 
summaries. To obtain this information, it calls functions in our mainframe banking system façade, which in turn makes requests to our mainframe banking system. There may 
also be other components in our backend service, not illustrated in figure C.3, which 
use our mainframe banking system façade to make requests to our mainframe banking 
system.
Single-Page Application
(Container: JavaScript and Angular)
Provides all off the Internet banking
functionality to customers via their
web browser.
Mobile App
(Container: Xamarin)
Provides a limited subset of the
Internet banking functionality to 
customers via their mobile device. 
Sign In Controller
(Component: Spring MVC
Rest Controller)
Allows users to sign in to the
Internet Banking System
Uses
Reset Password 
Controller
(Component: Spring 
MVC Rest Controller)
Allows users to reset
their passwords with a
single use URL.
Security Component
(Component: Spring Bean)
Provides functionality
related to signing in,
changing passwords, etc.
Email Component
(Component: Spring Bean)
Sends emails to users.
Accounts Summary Controller
(Component: Spring MVC
Rest Controller)
Provides customers with a
summary of their bank accounts.
Mainframe Banking 
System Facade
(Component: Spring Bean)
A facade onto the 
mainframe banking system.
Mainframe Banking System
(Softwear System)
Stores all of the core banking
information about customers,
accounts, transactions, etc.
Email System
(Software System)
The internal Microsoft
Exchange email system.
Database
(Container: Oracle
Database Schema)
Stores user registration 
information, hashed
authentication credentials,
access logs, etc.
API calls
(JSON/HTTPS)
API Application (Container)
Uses
Uses
Uses
Sends email using
Reads from and writes to
(JDBC)
Uses
(XML/HTTPS)
Figure C.3    A component diagram. Image adapted from https://c4model.com/, licensed under https://
creativecommons.org/licenses/by/4.0/.


	
417
﻿
A code diagram is a UML class diagram. (Refer to other sources such as https://www.uml 
.org/ if you are unfamiliar with UML.) You may use object-oriented programming 
(OOP) design patterns in designing an interface. 
Figure C.4 is an example code diagram of our mainframe banking system façade 
from figure C.3. Employing the façade pattern, our MainframeBankingSystem 
Facade interface is implemented in our MainframeBankingSystemFacadeImpl class. 
We employ the factory pattern, where a MainframeBankingSystemFacadeImpl object 
creates a GetBalanceRequest object. We may use the template method pattern to define 
an AbstractRequest interface and GetBalanceRequest class, define an Internet 
BankingSystemException interface and a MainframeBankingSystemException 
class, and define an AbstractResponse interface and GetBalanceResponse class. A 
MainframeBankingSystemFacadeImpl object may use a BankingSystemConnection 
connection pool to connect and make requests to our mainframe banking system and 
throw a MainframeBankingSystemException object when it encounters an error. (We 
didn’t illustrate dependency injection in figure C.4.) 
MainframeBankingSystemFacadeImpl
GetBalanceResponse
MainframeBankingSystemException
InternetBankingSystemException
AbstractRequest
BankingSystemConnection
AbstractResponse
GetBalanceRequest
com.bigbankpic.internetbanking.component.mainframe
+uses
+creates
+parses
+throws
+sends
+receives
MainframeBankingSystemFacade
Figure C.4    A code (UML class) diagram. Image adapted from https://c4model.com/, licensed under 
https://creativecommons.org/licenses/by/4.0/. 
Diagrams drawn during an interview or in a system’s documentation tend not to contain only components of a specific level, but rather usually mix components of levels 
1–3.
The value of the C4 model is not about following this framework to the letter, but 
rather about recognizing its levels of abstraction and fluently zooming in and out of a 
system design.


418
D
We discuss two-phase commit (2PC) here as a possible distributed transactions technique, but emphasize that it is unsuitable for distributed services. If we discuss distributed transactions during an interview, we can briefly discuss 2PC as a possibility 
and also discuss why it should not be used for services. This section will cover this 
material. 
Figure D.1 illustrates a successful 2PC execution. 2PC consists of two phases 
(hence its name), the prepare phase and the commit phase. The coordinator first 
sends a prepare request to every database. (We refer to the recipients as databases, 
but they may also be services or other types of systems.) If every database responds 
successfully, the coordinator then sends a commit request to every database. If any 
database does not respond or responds with an error, the coordinator sends an abort 
request to every database.
Two-phase commit (2PC)


	
419
﻿
Figure D.1    A successful 2PC execution. This figure illustrates two databases, but the same phases 
apply to any number of databases. Figure adapted from Designing Data-Intensive Applications by Martin 
Kleppmann, 2017, O’Reilly Media. 
2PC achieves consistency with a performance tradeoff from the blocking requirements. A weakness of 2PC is that the coordinator must be available throughout the 
process, or inconsistency may result. Figure D.2 illustrates that a coordinator crash 
during the commit phase may cause inconsistency, as certain databases will commit, 
but the rest will abort. Moreover, coordinator unavailability completely prevents any 
database writes from occurring.  


420
Appendix D  Two-phase commit (2PC)
Figure D.2    A coordinator crash during the commit phase will cause inconsistency. Figure adapted from 
Designing Data-Intensive Applications by Martin Kleppmann, O’Reilly Media, 2017. 
Inconsistency can be avoided by participating databases neither committing nor aborting transactions until their outcome is explicitly decided. This has the downside that 
those transactions may hold locks and block other transactions for a long time until 
the coordinator comes back.
2PC requires all databases to implement a common API to interact with the coordinator. The standard is called X/Open XA (eXtended Architecture), which is a C API 
that has bindings in other languages too. 
2PC is generally unsuitable for services, for reasons including the following: 
¡ The coordinator must log all transactions, so during a crash recovery it can compare its log to the databases to decide on synchronization. This imposes additional storage requirements. 
¡ Moreover, this is unsuitable for stateless services, which may interact via HTTP, 
which is a stateless protocol. 


	
421
﻿
¡ All databases must respond for a commit to occur (i.e., the commit does not 
occur if any database is unavailable). There is no graceful degradation. Overall, 
there is lower scalability, performance, and fault-tolerance. 
¡ Crash recovery and synchronization must be done manually because the write is 
committed to certain databases but not others. 
¡ The cost of development and maintenance of 2PC in every service/database 
involved. The protocol details, development, configuration, and deployment 
must be coordinated across all the teams involved in this effort. 
¡ Many modern technologies do not support 2PC. Examples include NoSQL 
databases, like Cassandra and MongoDB, and message brokers, like Kafka and 
RabbitMQ. 
¡ 2PC reduces availability, as all participating services must be available for commits. Other distributed transaction techniques, such as Saga, do not have this 
requirement. 
Table D.1 briefly compares 2PC with Saga. We should avoid 2PC and prefer other techniques like Saga, Transaction Supervisor, Change Data Capture, or checkpointing for 
distributed transactions involving services. 
Table D.1    2PC vs. Saga
2PC
Saga
XA is an open standard, but an 
implementation may be tied to 
a particular platform/vendor, 
which may cause lock-in.
Universal. Typically implemented 
by producing and consuming 
messages to Kafka topics. (Refer 
to chapter 5.)
Typically for immediate 
transactions.
Typically for long-running 
transactions.
Requires a transaction to be 
committed in a single process.
A transaction can be split into 
multiple steps.

## Examples & Scenarios

- 5	 Report fraud and misleading posts (e.g., a possible clickbait technique is to state
a low price on the post but a higher price in the description).
The non-functional requirements are as follows:
¡ Scalable—Up to 10 million users in a single city.
¡ High availability—99.9% uptime.
¡ High performance—Viewers should be able to view posts within seconds of creation. Search and viewing posts should have 1 second P99.
¡ Security—A poster should log in before creating a post. We can use an authentication library or service. Appendix B discusses OpenID Connect, which is a popular authentication mechanism. We will not discuss this further in the rest of this
chapter.
Most of the required storage will be for Craigslist posts. The amount of required storage is low:
¡ We may show a Craigslist user only the posts in their local area. This means that

- our script can checkpoint using this field. For example, if we checkpoint by date,
our script first transfers the records with the earliest date, checkpoints this date,
increments the date, transfers the records with this date, and so on, until the
transfer is complete.
This script must read/write the fields of the data objects to the appropriate tables and
columns. The more features we add before a data migration, the more complex the
migration script will be. More features mean more classes and properties. There will be
more database tables and columns, we will need to author a larger number of ORM/
SQL queries, and these query statements will also be more complex and may have
JOINs between tables.

- (e.g., sfbay.craigslist.org, shanghai.craiglist.org, etc). If we go to craigslist.org in our
browser, the following steps occur. An example is shown on figure 7.6.
1	 Our internet service provider does a DNS lookup for craigslist.org and returns its
IP address. (Browsers and OS have DNS caches, so the browser can use its DNS
cache or the OS’s DNS cache for future DNS lookups, which is faster than sending this DNS lookup request to the ISP.)
2	 Our browser makes a request to the IP address of craigslist.org. The server determines our location based on our IP address, which is contained in the address,
and returns a 3xx response with the subdomain that corresponds to our location.
This returned address can be cached by the browser and other intermediaries
along the way, such as the user’s OS and ISP.
3	 Another DNS lookup is required to obtain the IP address of this subdomain.

- ensure compliance with our latency SLA (e.g., 1-second P99) and prevent 504 timeout
errors, we can cache popular posts.
We can implement an LRU cache using Redis. The key can be a post ID, and the
value is the entire HTML page of a post. We may implement an image service in front
of the object store, so it can contain its own cache mapping object identifiers to images.
The static nature of posts limits potential cache staleness, though a poster may
update their post. If so, the host should refresh the corresponding cache entry.

- certain SQL implementations offer methods for fast INSERT for example, SQL Server’s
ExecuteNonQuery achieves thousands of INSERTs per second. Another solution is to
use batch commits instead of individual INSERT statements, so there is no log flush overhead for each INSERT statement.

- each market. For example, possibly the main reason that Craigslist does not provide
payments is that the business logic to handle payments can be different in each city.

- a cloud service. For example, we can use the following AWS services for each of the
services in figure 7.9. Other cloud vendors like Azure or GCP provide similar services:
¡ SQL: RDS (https://aws.amazon.com/rds/)
¡ Object Store: S3 (https://aws.amazon.com/s3/)
¡ Cache: ElastiCache (https://aws.amazon.com/elasticache/)
¡ CDN: CloudFront (https://www.amazonaws.cn/en/cloudfront/)
¡ Notification service: Simple Notification Service (https://aws.amazon.com/sns)
¡ Search: CloudSearch (https://aws.amazon.com/cloudsearch/)
¡ Logging, monitoring, and alerting: CloudWatch (https://aws.amazon.com/
cloudwatch/)

- we decide to add a new required field (e.g., subtitle), we can change the fields without
a SQL database migration. We don’t need to modify the fields in old posts, which have a
retention period and will be automatically deleted. The Post table is simplified, replacing a post’s fields with the post’s CDN URL. The columns become “id, ts, poster_id,
location_id, post_url”.
Observability
Any discussion of maintainability must emphasize the importance of observability, discussed in detail in section 2.5. We must invest in logging, monitoring, alerting, automated testing and adopt good SRE practices, including good monitoring dashboards,
runbooks, and automation of debugging.

- etc., and allow posters to place up to a certain number of tags (e.g., three) on a listing.
We can create a SQL dimension table for tags. Our Post table can have a column for a
comma-separated tag list. An alternative is to have an associative/junction table “post_
tag,” as shown in figure 7.10.
post
id
PK
other columns...
tag
id

- filters to view posts that are more relevant to their interests. For example, “real estate”
may have the following nested subcategories.
¡ Real estate > Transaction type > Rent
¡ Real estate > Transaction type > Sale
¡ Housing type > Apartment
¡ Housing type > Single-family house
¡ Housing type > Townhouse
7.19.5	 Analytics and recommendations
We can create daily batch ETL jobs that query our SQL database and populate dashboards for various metrics:
¡ Number of items by tag.

- For example, if a user has two saved search terms, “san francisco studio apartment”
and “systems design interview book,” the notification may contain the following. (You
certainly do not write down all of this during an interview. You can scribble down some
quick snippets and verbally describe what they mean.)
[
{
"search_term": "san francisco studio apartment",
"results": [
{
"link": "sfbay.craigslist.org/12345",

- CQRS techniques to ensure that writes succeed. For example, we can have separate
regulation services for admins and viewers that scale separately and periodic synchronization between them.
If we need to ensure that no forbidden content is posted on our Craigslist, we may
need to discuss systems that detect forbidden words or phrases, or perhaps machine
learning approaches.
A final thought is that Craigslist does not attempt to customize its listings based on
country. A good example was how it removed its Personals section in 2018 in response
to new regulations passed in the United States. It did not attempt to keep this section in
other countries. We can discuss the tradeoffs of such an approach.
Summary

- For example, consider a social media service we designed. A user may subscribe to
updates associated with a particular hashtag. If a user makes too many subscription
requests within a certain period, the social media service may respond to the user, “you
have made too many subscription requests within the last few minutes.” If we did rate
limiting, we will simply drop the user’s requests and return 429 (Too Many Requests)
or return nothing, and the client decides the response is 500. This will be a poor user
experience. If the request is sent by a browser or mobile app, the app can display to the
user that they sent too many requests, providing a good user experience.
Another example is services that charge subscription fees for certain request rates
(e.g., different subscription fees for 1,000 or 10,000 hourly requests). If a client exceeds

- attempt to attack our rate limiter, for example, by spoofing requests from another user
service to rate limit it. Our user services may also violate privacy by requesting data
about rate limiter requestors from other user services.
For these reasons, we will implement security and privacy in our rate limiter’s system
design.
8.4.5
Availability and fault-tolerance
We may not require high availability or fault-tolerance. If our service has less than three
nines availability and is down for an average of a few minutes daily, user services can
simply process all requests during that time and not impose rate limiting. Moreover,

- value itself does not need to be precise. For example, if the limit is 10 requests in 10
seconds, it is acceptable to occasionally rate limit a user at 8 or 12 requests in 10 seconds. If we have an SLA that requires us to provide a minimum request rate, we can set
a higher rate limit (e.g., 12+ requests in 10 seconds).
8.4.7
Consistency
The previous discussion on accuracy leads us to the related discussion on consistency. We do not need strong consistency for any of our use cases. When a user service
updates a rate limit, this new rate limit need not immediately apply to new requests; a
few seconds of inconsistency may be acceptable. Eventual consistency is also acceptable for viewing logged events such as which users were rate-limited or performing
analytics on these logs. Eventual rather than strong consistency will allow a simpler and
cheaper design.

- endpoint ID, and the desired rate limit (e.g., a maximum of 10 requests in 10 seconds).
Putting these requirements together, we need the following:
¡ A database with fast reads and writes for counts. The schema will be simple; it
is unlikely to be much more complex than (user ID, service ID). We can use an
in-memory database like Redis.
¡ A service where rules can be defined and retrieved, which we call the Rules
service.
¡ A service that makes requests to the Rules service and the Redis database, which
we can call the Backend service.
The two services are separate because requests to the Rules service for adding or modifying rules should not interfere with requests to the rate limiter that determine if a

- may be able to make requests at a higher rate than the set rate limit. For example, if two
hosts each receive requests close in time, each one will subtract a token and have nine
tokens left, then synchronize with other hosts. Even though there were two requests, all
hosts will synchronize to nine tokens.
Cloud Bouncer
Cloud Bouncer, (https://yahooeng.tumblr.com/post/111288877956/cloud-bouncer
-distributed-rate-limiting-at-yahoo), which was developed at Yahoo in 2014, is an example of a distributed rate-limiting library that is based on a token bucket.
8.9.2
Leaky bucket
A leaky bucket has a maximum number of tokens, leaks at a fixed rate, and stops

- Fixed window counters are implemented as key-value pairs. A key can be a combination of a client ID and a timestamp (e.g., user0_1628825241), while the value is the
request count. When a client makes a request, its key is incremented if it exists or created if it does not exist. The request is accepted if the count is within the set rate limit
and rejected if the count exceeds the set rate limit.
The window intervals are fixed. For example, a window can be between the [0, 60)
seconds of each minute. After a window has passed, all keys expire. For example, the
key “user0_1628825241” is valid from 3:27:00 AM GMT to 3:27:59 AM GMT because
1628825241 is 3:27:21 AM GMT, which is within the minute of 3:27 AM GMT.
QUESTION    How much can the request rate exceed the set rate limit?

- the set rate limit. For example, referring to figure 8.13, if the rate limit is five requests
in one minute, a client can make up to five requests in [8:00:00 AM, 8:01:00 AM) and
up to another five requests in [8:01:00 AM, 8:01:30 AM). The client has actually made
10 requests in a one-minute interval, twice the set rate limit of five requests per minute
(figure 8.14).
Token
Token
Token
Token
Token

- 1	 Determine the appropriate keys to query. For example, if our rate limit had
a 10-second expiry, the corresponding keys for user0 at 1628825250 will be
[“user0_1628825241”, “user0_1628825242”, …, “user0_1628825250”].
2	 Make requests for these keys. If we are storing key-value pairs in Redis instead of
the host’s memory, we can use the MGET (https://redis.io/commands/mget/)
command to return the value of all specified keys. Although the MGET command is O(N) where N is the number of keys to retrieve, making a single request
instead of multiple requests has lower network latency and resource overhead.
3	 If no keys are found, create a new key-value pair, such as, for example,
(user0_1628825250, 1). If one key is found, increment its value. If more than one
key is found (due to race conditions), sum the values of all the returned keys and

## Tables & Comparisons

| Local machine Old data store New data store
Get checkpoint
loop
GET
Data record
POST
Success |  |  |  |  | New data store |  |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
| loop |  |  | GET
Data record
POST
Succes | s |  |  |
|  |  |  |  |  |  |  |

| Client Backend SQL Object Store
POST /post.
Write post.
Post ID.
Success
loop
POST /file
Success |  |  |  |  |  | Object Store |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
| loop |  |  |  | POST /file
Success |  |  |  |
|  |  |  |  |  |  |  |  |

|  |  |  |  |  |  | Object Store |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
| loop |  |  | POS |  | T /file
cess |  |  |
|  |  |  |  | POS | T /file |  |  |
|  |  |  | Suc |  |  |  |  |
|  |  |  |  |  |  |  |  |

| New/updated post | Post Producer Service
Post
producer 0
Post
Load balancer producer 1
Post
producer n | Post writer/
consumer
Post topic
SQL leader |
| --- | --- | --- |
|  |  |  |

| post |  |
| --- | --- |
| PK | id |
|  | other columns... |
| tag |  |
| PK | id |
|  | other columns... |

| post_tag |  |
| --- | --- |
| FK | post_id |
| FK | tag_id |

| Rate limiting | Add new hosts | Use level 7 load balancer |
| --- | --- | --- |
| Handles traffic spikes by
returning 429 Too Many
Requests responses to the
users with high request
rates.
Handles DoS attacks
by providing misleading
responses.
Can rate limit users who
make expensive requests. | Adding new hosts may be
too slow to respond to traf-
fic spikes. Our service may
crash by the time the new
hosts are ready to serve
traffic.
Processes malicious
requests, which we should
not do.
Causes our service to incur
the costs of processing
expensive requests. | Not a solution to handle
traffic spikes.
Not a solution.
Can reject expensive
requests but may be too
costly and complex as a
standalone solution. |

| From Frontend | Backend
Host 0
Level 7
Load Host 1
balancer
Host N |  |
| --- | --- | --- |
|  |  |  |

|  | Backend
Host 0
Level 7
Load Host 1
balancer
Host N |  |  |
| --- | --- | --- | --- |
|  |  |  |  |

| From Frontend | Backend
Host 0
Level 4
Load Host 1
balancer
Host N |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |

| Stateless backend design | Stateful backend design | Storing counts in every host |
| --- | --- | --- |
| Stores counts in a distributed
database.
Stateless, so a user can be
routed to any host.
Scalable. We rely on the distrib-
uted database to serve both high
read and high write traffic.
Efficient storage consumption.
We can configure our desired
replication factor in our distrib-
uted database.
Eventually consistent. A host
making a rate limiting decision
may do so before synchroniza-
tion is complete, so this decision
may be slightly inaccurate.
Backend is stateless, so we use
the highly available and fault-tol-
erant properties of the distrib-
uted database.
Dependent on external database
service. Outages of such ser-
vices may affect our service, and
remediating such outages may
be outside our control. | Stores each user’s count in a
backend host.
Requires a level 7 load balancer
to route each user to its assigned
host.
Scalable. A load balancer is an
expensive and vertically scalable
component that can handle a
high request rate.
Lowest storage consumption
because there is no backup by
default. We can design a stor-
age service with an in-cluster
or out-cluster approach, as
discussed in section 13.5. With-
out backup, it is the cheapest
approach.
Most accurate and consistent
since a user always makes
requests to the same hosts.
Without backup, any host fail-
ure will result in data loss of
all the user counts it contains.
This is the lowest availability
and fault-tolerant of the three
designs. However, these factors
may be inconsequential because
they are not non-functional
requirements. If the rate limiter
cannot obtain an accurate count,
it can simply let the request
through.
Not dependent on external data-
base services. Load balancer
needs to process every request
to determine which host to send
it to. This also requires reshuf-
fling to prevent hot shards. | Store every user’s counts in
every host.
Every host has every user’s
counts, so a user can be routed
to any host.
Not scalable because each host
needs to store the counts of
every user. Need to divide users
into separate instances of this
service and require another
component (such as a frontend)
to route users to their assigned
instances.
Most expensive approach. High
storage consumption. Also, high
network traffic from n–n com-
munication between hosts to
synchronize counts.
Least accurate and consistent
approach because it takes time
to synchronize counts between
all hosts.
Hosts are interchangeable, so
this is the most highly available
and fault-tolerant of the three
designs.
Not dependent on external
database services like Redis.
Avoids risk of service outage
from outages of such down-
stream services. Also, it’s easier
to implement, particularly in big
organizations where provisioning
or modifying database services
may involve considerable
bureaucracy. |

|  |  |
| --- | --- |
| 10 to | k |

| :User service :Host :Leader host
User request
Steps 1–3
par
User request
Rate limit decision |  |  |  |  |  |  | :Leader host |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
| par |  |  |  |  |  | User request |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  | Rate limit decision |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |

|  |  |
| --- | --- |
| . Produce re |  |

| Address Group Address Group Address Address Group Notification
Backend
Fetcher Request Topic Group Response Topic Kafka topic
Service
GET addresses count
Addresses count |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | GET addresses count |  |  |  |  |  |  |
|  |  |  |  | Addresses count |  |  |  |  |  |  |
| par |  |  |  | ddresses request
s response
2. Consume
addresses
request
Addresses
batch request
3. GET addr
Addresses
4. Prod
S
5. Consume add
Addresse
e notifications |  |  | ess batch
batch | atch |  |  |
|  |  |  |  |  | 4. Prod |  | uce addresses b | atch |  |  |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  | S | uccess response |  |  |  |
|  |  |  |  |  |  |  | resses batch
s batch |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |
| par |  |  |  | Pro |  |  |  | n |  |  |
|  |  |  |  |  |  | ro | duce a notificatio | n |  |  |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| par |  |  | esult.
se OK
ckpoint
se OK |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

| Search | Autocomplete |
| --- | --- |
| Results are usually a list of webpage URLs
or documents. These documents are prepro-
cessed to generate an index. During a search
query, the search string is matched to the
index to retrieve relevant documents.
P99 latency of a few seconds may be accept-
able. Higher latency of up to a minute may be
acceptable in certain circumstances.
Various result data types are possible, includ-
ing strings, complex objects, files, or media.
Each result is given a relevance score.
Much effort is expended to compute rel-
evance scores as accurately as possible,
where accuracy is perceived by the user.
A search result may return any of the input
documents. This means every document
must be processed, indexed, and possible to
return in a search result. For lower complexity,
we may sample the contents of a document,
but we must process every single document.
May return hundreds of results.
A user can click on multiple results, by
clicking the “back” button and then clicking
another result. This is a feedback mechanism
we can draw many possible inferences from. | Results are lists of strings, generated based
on user search strings.
Low latency of ~100 ms P99 desired for good
user experience. Users expect suggestions
almost immediately after entering each
character.
Result data type is just string.
Does not always have a relevance score. For
example, an IDE’s autocomplete result list
may be lexicographically ordered.
Accuracy requirements (e.g., user clicks on
one of the first few suggestions rather than
a later one) may not be as strict as search.
This is highly dependent on business require-
ments, and high accuracy may be required in
certain use cases.
If high accuracy is not required, techniques
like sampling and approximation algorithms
can be used for lower complexity.
Typically returns 5–10 results.
Different feedback mechanism. If none of the
autocomplete suggestions match, the user
finishes typing their search string and then
submits it. |

| Thumbnail
Generation
Service
13
Backend
5b
Service
14
CDN Topic
5a
7, 15
8, 16
File Storage Object Storage
6, 14
Service Service
9, 10, 17
18
11 CDN
SQL |  |  |
| --- | --- | --- |
|  | 1 | 3 |

| Requ | est CDN asset using t | oken. |
| --- | --- | --- |
|  | CDN asset.
Delete
Succ |  |

| In-cluster manager | Out-cluster manager |
| --- | --- |
| Metadata service does not
make requests to the in-cluster
manager.
Manages file assignment within
individual roles in the cluster.
Needs to know about every node
in the cluster.
Monitors heartbeats from nodes.
Deals with host failures. Nodes
may die, and new nodes may be
added to the cluster. | Metadata service makes requests
to the out-cluster manager.
Manages file assignment to a
cluster, but not to individual
nodes.
May not know about each indi-
vidual node, but needs to know
about each cluster.
Monitors health of each indepen-
dent cluster.
Tracks each cluster’s utilization
and deals with overheated clus-
ters. New files may no longer be
assigned to clusters that reach
their capacity limits. |

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Metadata, includi | n | g | storage host ID. |  |  |
|  |  | GET asset.
Asset. |  |  |  |

| API Rate Limiting Metadata Storage
Client Origin
Gateway Service Service Service
Request file. Check
rate limit.
OK.
GET metadata.
Metadata, including
storage host ID.
GET asset
Asset
par
Asset.
POST asset.
Response, including asset key.
POST asset metadata
Response OK.
Update load.
Response OK. |  |  |  |  |  |  |  |  |  |  |  |  |  | Origin |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  | Metadat
storag |  | a
e | , i
h | ncludin
ost ID. |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  | GET as
Asset |  |  |  |  |  |
| par |  |  | Asset. |  |  |  |  |  |  | POST asset. |  | et key. |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  | POST asset. |  |  |  |  |
|  |  |  |  |  |  | Respons
POST asse
Respon
Update |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  | Respons |  |  | e, including ass |  | et key. |  |  |  |
|  |  |  |  |  |  |  |  |  |  | t metadata
se OK. |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  | load.
se OK. |  |  |  |  |  |
|  |  |  |  |  |  |  |  | Upda | te |  |  |  |  |  |  |
|  |  |  |  |  |  | Respon |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

| API Rate Limiting Metadata Storage Secrets
Client Origin
Gateway Service Service Service Management
Service
Request file. Check
rate limit.
OK.
GET metadata.
Metadata, including
storage host ID.
GET asset
Asset
par Asset.
Encrypt asset.
Ciphertext asset.
POST asset.
Response, including asset key.
POST key.
Response OK.
Update load.
Response OK. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Origin |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  | Check
rate limit. |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  | Metadat
storag |  | a,
e | including
host ID. |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  | GET asset |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  | Asset |  |  |  |  |
| par |  |  | Asset. |  |  | Encryp
Cipher |  |  | t asset.
text asset.
POST asset. |  |  |  |  | t key. |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  | Respon |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  | Respon |  | se, including asse |  |  |  |  | t key. |  |  |  |  |
|  |  |  |  |  |  |  |  |  | POST k |  |  |  |  | ey. |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  | POST k |  | ey. |  |  |  |  |
|  |  |  |  |  |  |  |  |  | Response |  |  |  |  | OK. |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  | Response |  |  | OK. |  |  |  |  |
|  |  |  |  |  |  | Upda |  |  | te load.
nse OK. |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  | Upda | te | load. |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  | Respo |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  | ns | e OK. |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

| Messaging app | Notification/alerting service |
| --- | --- |
| All messages are equal priority and
have a 10-second P99 delivery time.
Messages are delivered from one client
to others, all within a single channel on
a single service. No need to consider
other channels or services.
Only a manual trigger condition.
No message templates. (Except per-
haps message suggestions.)
Due to end-to-end encryption, we can-
not see the user’s messages, so there
is less freedom to identify and dedupli-
cate common elements into functions
to reduce computational resource
consumption.
Users may request for old messages.
Delivery confirmation and read receipt
are part of the app. | Events can have different priority levels.
Multiple channels, such as email, SMS,
automated phone calls, push notifica-
tions, or notifications within apps.
An event can be manually, programmat-
ically, or periodically triggered.
Users can create and manage notifica-
tion templates.
No end-to-end encryption. We have
more freedom to create abstractions,
such as a template service.
Most notifications only need to be sent
once.
We may not have access to most notifi-
cation channels, such as email, texting,
push notifications, etc., so delivery and
read confirmations may not be possible. |

| Device 0 |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  | Block request
sent in this range |  |  |
|  | Unblock reques | t s |  |  |  |
|  |  |  | ent in this range |  |  |
|  |  |  |  |  |  |

|  | Connection
Service |  |
| --- | --- | --- |
|  |  |  |
| Log out
Requests
sent in this
range |  |  |
|  |  |  |

| Message Host Assigner
Recipient topic Message Service Recipient
Consumer Service Service
Get message
request.
Message
request.
Generate message. Verify blocked status.
par Get assigned host.
Assigned host.
POST /log
Response OK.
Send message.
Message sent. |  |  |  |  |  |  |  | Recipient |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | s | sage. Verify blocke | d |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
| par |  |  | Get assign
Assigne |  | ed host.
d host.
POST /log |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | Response OK. |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | Send me
Messag | ssage.
e sent. |  |  |  |

|  |  |  |
| --- | --- | --- |
| 3. Show listi |  | ng to guests. |

|  |  |  |
| --- | --- | --- |
| 4. Send notification |  |  |

| :Client :Elasticsearch :Booking :Availability :Payment
Search/filter
listings.
Listings.
Get listing details.
Listing details.
Booking request Check
availability.
[Listing available]
alt True
Make
booking.
Booking confirmed.
[Listing unavailable]
False
Booking failed.
If booking confirmed, make payment.
[Payment successful.]
alt
Payment confirmed.
[Payment failed.]
Cancel booking.
Booking canceled.
Booking failed. |  |  |  |  |  |  |  |  |  |  |  |  | :Payment |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | Booking |  | request |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| alt |  |  | [Listing a
Booking c |  | a | v |  |  | True
Make
booking. |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | [Listing un
Bookin |  | un | a |  |  | False |  |  |  |  |  |  |  |
|  |  |  |  |  |  | If booking confirm |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  | If booking confirm | ed, make payment. |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| alt |  |  | [Payment s
[Paymen |  | t s | u |  | confirmed. |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  | co | nfirmed. |  |  |  |  |  |  |  |
|  |  |  |  |  |  | t failed.]
Bookin |  | Cancel
Booking c
g failed. |  |  | booking.
anceled. |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

| User table
Post table copy JOIN
partition 0
copy
User table
Post table copy Post table copy JOIN
partition 1
copy
User table
Post table copy JOIN
partition n | Post table copy |  | User table
partition 0 |
| --- | --- | --- | --- |
|  | Post table copy |  | User table
partition n |
|  |  | JOIN |  |

|  | Media
Service
Ingestor
Producer Consumer
Queue
Moderation
Service HDFS
API
Backend ETL jobs
Gateway
Queue
Metadata
Service
SQL Approval Notification
ZooKeeper
Service Service Service
Redis
SQL SQL SQL
cluster 0 cluster 1 cluster n |
| --- | --- |
| Source/
Client
User |  |

|  | CDN
Media
Service
Ingestor
Producer Consumer
Queue
Moderation
Service HDFS
API
Backend ETL jobs
Gateway
Queue
Metadata
Service
SQL Approval Notification
ZooKeeper
Service Service Service
Redis
SQL SQL SQL
cluster 0 cluster 1 cluster n |
| --- | --- |
| Source/
Client
User |  |

|  |  |
| --- | --- |
|  | events |
|  | events |
|  | events |
|  | events |

|  |  |
| --- | --- |
|  | events |
|  | events |
|  | events |
|  | events |
|  | events |
|  | events |
|  | events |
|  | events |

| 1 |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | 1 |  |  |  |  |
|  |  |  |  | 1 |  |
|  | 1 |  |  |  |  |
|  | 1 |  |  |  |  |

| 1 |  |  |  | 1 |  |
| --- | --- | --- | --- | --- | --- |
|  | 1 |  | 1 |  |  |
| 1 |  |  |  | 1 |  |
|  | 1 |  | 1 |  |  |
|  | 2 (collision) |  |  |  |  |

| 1 |  | 1 |  | 1 |  |
| --- | --- | --- | --- | --- | --- |
|  | 1 |  | 1 |  | 1 |
| 1 | 1 |  |  | 1 |  |
|  | 2 (collision) |  | 1 |  |  |
|  | 3 (collision) |  |  |  |  |

| 1 |  | 1 |  | 2 |  |
| --- | --- | --- | --- | --- | --- |
|  | 1 |  | 2 |  | 1 |
| 2 | 1 |  |  | 1 |  |
|  | 2 |  | 2 |  |  |
|  | 4 (collision) |  |  |  |  |

| 1 |  | 1 |  | 3 |  |
| --- | --- | --- | --- | --- | --- |
|  | 1 |  | 3 |  | 1 |
| 3 | 1 |  |  | 1 |  |
|  | 2 |  | 3 |  |  |
|  | 5 (collision) |  |  |  |  |

| Lambda | Kappa |
| --- | --- |
| Separate batch and streaming
pipelines. Separate clusters,
code bases, and processing
frameworks. Each needs its own
infrastructure, monitoring, logs,
and support.
Batch pipelines allow faster per-
formance with processing large
amounts of data.
An error in a batch job may
require all the data to be repro-
cessed from scratch. | Single pipeline, cluster, code
base, and processing framework.
Processing large amounts of
data is slower and more expen-
sive than Lambda architecture.
However, data is processed as
soon as it is ingested, in contrast
to batch jobs which run on a
schedule, so the latter may pro-
vide data sooner.
An error in a streaming job only
requires reprocessing of its
affected data point. |

| Monolith | Service |
| --- | --- |
| Faster and easier to develop at first
because it is a single application.
A single database means it uses less
storage, but this comes with tradeoffs.
With a single database and fewer data
storage locations in general, it may
be easier to comply with data privacy
regulations.
Debugging may be easier. A developer
can use breakpoints to view the func-
tion call stack at any line of code and
understand all logic that is happening
at that line.
Related to the previous point, being
able to easily view all the code in a
single location and trace function calls
may make the application/system as a
whole generally easier to understand
than in a service architecture.
Cheaper to operate and better perfor-
mance. All processing occurs within the
memory of a single host, so there are
no data transfers between hosts, which
are much slower and more expensive. | Developers need to handle serialization and deserialization in
every service, and handle requests and responses between the
services.
Before we begin development, we first need to decide where the
boundaries between the services should be, and our chosen
boundaries may turn out to be wrong. Redeveloping services to
change their boundaries is usually impractical.
Each service should have its own database, so there may be
duplication of data and overall greater storage requirements.
Data is scattered in many locations, which makes it more diff-i
cult to ensure that data privacy regulations are complied with
throughout the organization.
Distributed tracing tools like Jaegar or Zipkin are used to under-
stand request fan-out, but they do not provide many details,
such as the function call stack of the services involved in the
request. Debugging across services is generally harder than in a
monolith or individual service.
A service’s API is presented as a black box. While not having to
understand an API’s details may make it easier to use, it may
become difficult to understand many of the fine details of the
system.
A system of services that transfer large amounts of data
between each other can incur very high costs from the data
transfers between hosts and data centers. Refer to https://
www.primevideotech.com/video-streaming/scaling-up-the
-prime-video-audio-video-monitoring-service-and-reducing
-costs-by-90 for a discussion on how an Amazon Prime Video
reduced the infrastructure costs of a system by 90% by merging
most (but not all) of their services in a distributed microservices
architecture into a monolith. |

| OAuth2 (authorization) | OpenID Connect (authentication) |
| --- | --- |
| Grant access to your API.
Get access to user data in other systems. | User login
Make your accounts available in other systems. |

| Web application with server backend | Authorization code flow |
| --- | --- |
| Native mobile app
JavaScript Single-Page App (SPA) with
API backend
Microservices and APIs | Authorization code flow with PKCE
(Proof Key for Code Exchange) (outside
the scope of this book)
Implicit flow
Client credentials flow |

| 2PC | Saga |
| --- | --- |
| XA is an open standard, but an
implementation may be tied to
a particular platform/vendor,
which may cause lock-in.
Typically for immediate
transactions.
Requires a transaction to be
committed in a single process. | Universal. Typically implemented
by producing and consuming
messages to Kafka topics. (Refer
to chapter 5.)
Typically for long-running
transactions.
A transaction can be split into
multiple steps. |

