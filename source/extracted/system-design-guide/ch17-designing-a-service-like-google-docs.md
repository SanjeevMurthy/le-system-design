# Chapter 13: Designing a Service Like Google Docs

> Source: System Design Guide for Software Professionals, Chapter 17, Pages 296-330

## Key Concepts

- 13
Designing a Service Like Google Docs
In the era of digital collaboration, file-sharing platforms have transformed the way people work
together, and Google Docs stands out as one of the most powerfu
- foundation for the entire design process and ensure that the system meets the needs of its users.
Let’s explore the key functional requirements:
The user registration and authentication requirements a

## Content

13
Designing a Service Like Google Docs
In the era of digital collaboration, file-sharing platforms have transformed the way people work
together, and Google Docs stands out as one of the most powerful and intuitive services. With
millions of active users, Google Docs has revolutionized the way people create, edit, and share
documents online.
Designing a service such as Google Docs presents a unique set of challenges and opportunities. It
requires a robust and scalable architecture that can handle real-time collaboration and a vast
amount of user-generated content while providing a seamless and efficient user experience. In
this chapter, we will explore the system design of a Google Docs-like service, delving into the
key components, design decisions, and best practices involved in building a scalable and
efficient file-sharing platform. By the end of this chapter, you will have a comprehensive
understanding of the system design principles and techniques involved in building a service such
as Google Docs. Let us start with the functional requirements of a service such as Google Docs.
In this chapter, we will cover the following topics:
Functional requirements
Non-functional requirements
Data model
Scale calculations
High-level design
Low-level design
Additional considerations and best practices
Let us start by exploring the functional and non-functional requirements of a file-sharing system
such as Google Docs.
Functional requirements
Before diving into the system design, it is crucial to define the functional requirements that
specify what the file-sharing service should be capable of doing. These requirements lay the


foundation for the entire design process and ensure that the system meets the needs of its users.
Let’s explore the key functional requirements:
The user registration and authentication requirements are as follows:
Users should be able to create new accounts by providing necessary information such as a username, email, and
password
The system should securely store user credentials and authenticate users upon login
User sessions should be managed efficiently to allow seamless access to the service
The document creation, editing, and deletion requirements can be summed up as follows:
Users should be able to create new documents within the file-sharing service
The system should provide a rich text editor with formatting options, allowing users to create and edit documents
collaboratively
Users should have the ability to delete documents they own or have appropriate permissions for
Real-time collaboration and synchronization is a further requirement:
Multiple users should be able to edit the same document simultaneously, with their changes synchronized in real
time
The system should handle concurrent edits efficiently, ensuring data consistency and avoiding conflicts
Users should be able to see the presence of other collaborators and their current cursor positions within the
document
Sharing and access control should be implemented as follows:
Users should be able to share documents with other users or external parties by generating shareable links or
granting specific access permissions
The system should support different access levels, such as view-only, comment-only, or edit permissions
Document owners should have the ability to manage collaborators, revoke access, and modify sharing settings
The version history and revision management features should include the following:
The file-sharing service should automatically save document revisions and maintain a version history
Users should be able to view and restore previous versions of a document
The system should provide a clear audit trail of changes made to a document, including the timestamp and the
user responsible for each revision
Commenting and suggestion features should be implemented as follows:
Users should have the ability to add comments to specific parts of a document, facilitating discussions and
feedback


The system should support suggesting edits or changes, allowing collaborators to propose modifications without
directly editing the document
Comments and suggestions should be easily visible and manageable within the document interface
Search and organization features should include the following:
The file-sharing service should provide a powerful search functionality, enabling users to search for documents
based on titles, content, or metadata
Users should be able to organize their documents into folders or categories for better management and
accessibility
These functional requirements provide a comprehensive overview of the core features that a filesharing service such as Google Docs should offer. By fulfilling these requirements, the system
will enable users to create, collaborate, and share documents seamlessly, enhancing productivity
and facilitating effective teamwork.
In the next section, we will explore the non-functional requirements that ensure the service
remains scalable, reliable, and performant while meeting the functional requirements discussed
previously.
Non-functional requirements
While functional requirements define what the system should do, non-functional requirements
specify how the system should perform and behave. These requirements are critical in ensuring
that the file-sharing service remains scalable, available, and reliable under various conditions.
Let’s discuss the key non-functional requirements:
Scalability should be accounted for as follows:
The system should be designed to handle a large number of users and documents, accommodating growth and
peak usage
Horizontal scalability should be achieved by adding more servers and distributing the load across them
The architecture should allow for easy scaling of individual components, such as the Document Service or
Collaboration Service, independently
High availability and reliability should be secured as follows:
The file-sharing service should be highly available, ensuring minimal downtime and quick recovery from
failures


Redundancy should be implemented at various levels, including server redundancy, database replication, and
geo-redundancy
The system should be designed to handle server failures, network outages, and data center disasters without
significant impacts on the user experience
The service should have low latency:
The service should provide real-time collaboration and synchronization with minimal latency
Users should be able to see each other’s changes instantly, enabling a seamless and interactive collaboration
experience
Techniques such as caching, efficient data retrieval, and optimized communication protocols should be
employed to reduce latency
Data consistency and integrity should be secured as follows:
The system should ensure the consistency and integrity of document data across all replicas and collaborators
Changes made by multiple users should be properly synchronized and merged to maintain a consistent document
state
Conflict resolution mechanisms should be in place to handle simultaneous edits and prevent data corruption
By addressing these non-functional requirements, the file-sharing service can ensure a reliable,
scalable, and performant user experience. It is essential to consider these requirements
throughout the design process and make architectural decisions that align with these goals.
In the next section, we will explore the data model that forms the foundation of the file-sharing
service, defining the entities and relationships necessary to support the functional requirements.
Data model
The data model is a crucial component of the file-sharing service, as it defines the structure and
relationships of the data entities involved. A well-designed data model ensures efficient storage,
retrieval, and manipulation of data while supporting the functional requirements of the system.
Let’s dive into the key entities and their relationships:
The User entity represents the users of the file-sharing service, storing their basic information such as username, email,
password hash, account creation, and last login timestamps. Each user is uniquely identified by their user_id.
The Document entity represents the documents created and shared within the service. It contains the document title,
content, owner_id (referencing the User who created it), creation and update timestamps, and current version number.


The Revision entity stores the revision history of documents. Each revision is associated with a specific document and
the user who made the changes. It includes the revised content and the timestamp of the revision.
The CollaboratorPermission entity defines the access permissions granted to users for a specific document. It
associates a user with a document and specifies the permission level (e.g., view, edit, or comment) and the timestamp when
the permission was granted.
The Comment entity represents comments made by users on specific documents. It contains the comment content, the
associated document and user, and the creation timestamp.
The Suggestion entity represents suggested changes or edits to a document. It includes the suggested content, associated
document and user, status of the suggestion (e.g., pending, accepted, or rejected), and creation timestamp.
The Folder entity allows users to organize their documents into folders. It contains the folder name, associated user, and
creation timestamp.
The FolderDocument entity represents the relationship between folders and documents, indicating which documents are
contained within each folder.
Figure 13.1 illustrates the comprehensive data model for a Google Docs-like service. It
showcases key entities such as User, Document, Revision, and Folder, along with their attributes
and the relationships between them, providing a clear overview of the system’s data structure
and interconnections.
Figure 13.1: An overview of the entity relationship diagram for a Google Docs-like service data model


Let us talk about the different many-many, one-many, and many-one relationships in this data
model next.
Relationships
There are several one-to-many and many-to-many relationships between the entities in this
model. Let us highlight them.
The one-to-many relationships are as follows:
User to document: A user can own multiple documents
Document to revision: A document can have multiple revisions
Document to comment: A document can have multiple comments
Document to suggestion: A document can have multiple suggestions
User to folder: A user can have multiple folders
The many-to-many relationships are as follows:
User to document (through CollaboratorPermission): A user can collaborate on multiple documents, and a
document can have multiple collaborators
Folder to document (through FolderDocument): A folder can contain multiple documents, and a document can be
present in multiple folders
By designing the data model with these entities and relationships, the file-sharing service can
efficiently store and retrieve data related to users, documents, revisions, collaborations,
comments, suggestions, and folder organization. The data model supports the functional
requirements and enables the system to handle the complex interactions between users and
documents.
In the next section, we will perform scale calculations to estimate the storage, bandwidth, and
processing requirements of the file-sharing service based on the anticipated user base and usage
patterns.
Scale calculations
To design a scalable file-sharing service, it is essential to estimate the storage, bandwidth, and
processing requirements based on the expected user base and usage patterns. These calculations


help in making informed decisions about the infrastructure and resources needed to support the
service. Let’s perform some scale calculations.
Assumptions
Here are some initial assumptions that we will use in our design and scale calculations:
Total number of users: 10 million
Average number of documents per user: 100
Average document size: 50 KB
Average number of revisions per document: 10
Average revision size: 50 KB
Average number of collaborators per document: 5
Average number of comments per document: 20
Average comment size: 1 KB
Average number of folders per user: 10
Storage requirements
Here are the storage requirements for the system based on our previous assumptions:
The document storage requirements are as follows:
Total documents: 10 million users × 100 documents/user = 1 billion documents
Total document storage: 1 billion documents × 50 KB/document = 50 TB
The revision storage requirements are as follows:
Total revisions: 1 billion documents × 10 revisions/document = 10 billion
revisions
Total revision storage: 10 billion revisions × 50 KB/revision = 500 TB
The comment storage requirements are as follows:
Total comments: 1 billion documents × 20 comments/document = 20 billion comments
Total comment storage: 20 billion comments × 1 KB/comment = 20 TB
The user and metadata storage requirements are as follows:


User metadata: 10 million users × 1 KB/user = 10 GB
Folder metadata: 10 million users × 10 folders/user × 1 KB/folder = 100 GB
CollaboratorPermission metadata: 1 billion documents × 5 collaborators/document × 1 KB/permission
= 5 TB
The total storage requirements are as follows: 50 TB (documents) + 500 TB (revisions) + 20 TB
(comments) + 5 TB (permissions) + 110 GB (user and folder metadata) ≈ 575 TB
Bandwidth considerations
Based on our assumptions, here are the bandwidth needs for uploads and downloads:
The document upload bandwidth needs are as follows:
Average document uploads per day: 10 million users × 1 document/user/day × 50
KB/document = 500 GB/day
The document download bandwidth needs are as follows:
Average document downloads per day: 10 million users × 10 documents/user/day × 50
KB/document = 5 TB/day
The collaboration and synchronization bandwidth needs are as follows:
Average collaboration updates per day: 10 million users × 10 documents/user/day × 5
collaborators/document × 10 KB/update = 5 TB/day
Total daily Bandwidth: 500 GB (uploads) + 5 TB (downloads) + 5 TB (collaboration)
≈ 10.5 TB/day
Processing requirements
In our service, we need to process, render, format, and synchronize documents. Here are the
estimates for these features for our service:
The document rendering and formatting estimate is as follows:
Peak document renders per second: 10 million users × 10 documents/user/day ÷ 86400 seconds/day ≈ 1200
renders/second
The revision comparison and merging estimate is as follows:
Peak revision comparisons per second: 10 million users × 10 documents/user/day × 1 revision/document/day ÷
86400 seconds/day ≈ 1200 comparisons/second


The real-time collaboration and synchronization estimates are as follows:
Peak concurrent collaborators: 10 million users × 10% concurrent usage × 5 collaborators/document ≈ 5
million concurrent collaborators
Peak collaboration updates per second: 5 million collaborators × 1 update/collaborator/minute ÷ 60
seconds/minute ≈ 83,000 updates/second
These calculations provide an estimate of the storage, bandwidth, and processing requirements
for the file-sharing service based on the given assumptions. It’s important to note that these
numbers can vary based on actual usage patterns and the growth of the user base. The
infrastructure should be designed to handle peak loads and should be easily scalable to
accommodate future growth.
In the next section, we will propose a high-level design architecture that takes these scale
requirements into account and leverages various building blocks to create a scalable and efficient
system.
High-level design
Now that we have a clear understanding of the functional and non-functional requirements, as
well as the scale calculations, let’s dive into the high-level design of the file-sharing service. The
goal is to create an architecture that is scalable, reliable, and efficient in handling the vast amount
of documents, revisions, and user interactions. Figure 13.2 shows the high-level design of the
file-sharing system, which includes load balancers, API gateways, microservices for document
management, collaboration, access control, caches, databases, and storage systems.


Figure 13.2: The high-level system design of a file-sharing service
Let us discuss the software components and modules shown in this Figure 13.2.
Software components and modules of high-level
design
The following are the different components and modules:
Client-server architecture:The file-sharing service will follow a client-server architecture, where clients (such as web
browsers or mobile apps) communicate with the server-side components through APIs. The server-side components will
handle the core functionality, data storage, and processing.
Load balancer: To distribute the incoming traffic evenly across multiple servers, a load balancer will be placed in front of
the server-side components. The load balancer will ensure that requests are efficiently routed to the appropriate servers
based on factors such as server load, request type, and geographic location.
API Gateway: An API Gateway will act as the entry point for all client requests. It will handle request routing,
authentication, rate limiting, and request/response transformation. The API Gateway will expose well-defined APIs for
various functionalities, such as document creation, editing, collaboration, and access control.


Microservices architecture: To promote modularity, scalability, and maintainability, the server-side components will be
designed as microservices. Each microservice will be responsible for a specific domain or functionality.
The main microservices in the file-sharing service will be as follows:
Document service:
Handles document creation, retrieval, update, and deletion operations
Manages document metadata and storage
Communicates with the storage system to persist and retrieve document content
Collaboration service:
Enables real-time collaboration and synchronization between multiple users
Handles Operational Transformation (OT) and conflict resolution for concurrent editing
Manages active user information and updates for collaborators
Revision service:
Manages revision history and version control for documents
Stores and retrieves document revisions
Performs diff and merge operations for document revisions
Access control service:
Handles user authentication and authorization
Manages access permissions and sharing settings for documents
Enforces access control policies for document operations
Notification service:
Sends notifications and updates to users regarding document changes, comments, and collaboration events
Integrates with email, push notifications, and real-time messaging systems
Caching:
To improve performance and reduce the load on the backend services, a distributed caching layer (e.g., Redis)
will be employed. The caching layer will store frequently accessed data, such as document metadata, user
sessions, and commonly retrieved document content. Caching will help in serving data quickly and reducing the
number of requests to the database and storage systems.


Databases:
The file-sharing service will use a combination of databases to store structured and unstructured data:
Relational database (e.g., PostgreSQL):
Stores metadata information such as user profiles, document metadata, access permissions, and collaboration
details
Provides ACID properties and supports complex querying and transactions
NoSQL database (e.g., MongoDB):
Stores document revisions and content
Provides scalability and flexibility for handling large amounts of unstructured data
Storage system:
Document content, revisions, and attachments will be stored in a distributed storage system (e.g., Amazon S3 or
Google Cloud Storage). Document types could be text files, videos, images, multimedia files, and so on. We may
need to implement intelligent chunking or use multi-part APIs for some of these cloud storage services in order
to support large sizes and parallelized uploads. The storage system will provide scalable and durable storage for
large files, allowing for efficient retrieval and delivery to users.
Real-time communication:
To enable real-time collaboration and synchronization, WebSocket connections can be established between the
clients and the Collaboration Service. WebSocket allows for bidirectional communication, enabling instant
updates and synchronization of document changes among collaborators.
Monitoring and logging:
Comprehensive monitoring and logging mechanisms will be implemented to track the health and performance of
the system. Metrics such as request latency, error rates, and resource utilization will be collected and visualized
using tools such as Prometheus and Grafana. Centralized logging solutions (e.g., ELK stack) will be used to
aggregate and analyze logs from all components.
Security and privacy:
Security and privacy measures will be implemented throughout the system. User authentication and
authorization will be handled using secure protocols such as OAuth. Sensitive data, such as passwords and
access tokens, will be securely hashed and stored. Data encryption will be applied to protect user data both in
transit and at rest. Regular security audits and penetration testing will be conducted to identify and address
potential vulnerabilities.


This high-level design provides an overview of the key components and their interactions in
the file-sharing service. It takes the scale requirements into account and employs various
building blocks to create a scalable and efficient architecture.
In the subsequent sections, we will explore the low-level design of critical components, such as
the Document Service, Collaboration Service, and Access Control Service, to gain a deeper
understanding of their functionalities and interactions.
Low-level design
We will now cover the low-level design of several microservices that, together, form our service.
Let us begin by evaluating the design of the document service.
Designing the document service
The Document Service is a critical component of the file-sharing system, responsible for
handling document-related operations such as creation, retrieval, update, and deletion. It
manages document metadata and interacts with the storage system to persist and retrieve
document content. Let’s dive into the low-level design of the Document Service. Let us first look
at the API endpoints exposed by the service.
The Document Service exposes the following API endpoints:
POST /documents: Create a new document
Request body: Document metadata (title, owner, etc.) and initial content
Response: Created document object with assigned document ID
GET /documents/{documentId}: Retrieve a document by its ID
Response: Document object with metadata and content
PUT /documents/{documentId}: Update a document’s metadata or content
Request body: Updated document metadata and/or content
Response: Updated document object
DELETE /documents/{documentId}: Delete a document by its ID
Response: Success or error message


GET /documents/{documentId}/revisions: Retrieve the revision history of a document
Response: List of revision objects associated with the document.
Now, we will dive into the data models for this service.
Data models
Figure 13.3 illustrates the relationship between the Document and Revision entities, showing their
attributes and the one-to-many relationship between them.
Figure 13.3: An overview of the entity relationship diagram for the Document Service
Now, let us look at the different workflows for creating, retrieving, updating, and deleting
documents.
Document creation flow
Figure 13.4 shows the step-by-step process of creating a new document, including metadata
storage and content upload.


Figure 13.4: A document creation flow sequence
Here is the flow:
1. The client sends a POST request to the /documents endpoint with the document metadata and initial content.
2. The Document Service validates the request and generates a unique document ID.
3. The Document Service stores the document metadata in the relational database.
4. The initial content is stored in the storage system (e.g., S3), and the content URL is obtained.
5. The Document Service updates the document metadata with the content URL.
6. The created document object is returned to the client with the assigned document ID.
Let us now look at the retrieval flow.
Document retrieval flow
Figure 13.5 illustrates the process of retrieving a document, including fetching metadata from
the database and content from the storage system.


Figure 13.5: Document retrieval flow sequence diagram
Here is the flow:
1. The client sends a GET request to the /documents/{documentId} endpoint.
2. The Document Service retrieves the document metadata from the relational database based on the document ID.
3. If the document exists, the Document Service fetches the document content from the storage system using the content URL.
4. The document object, including metadata and content, is returned to the client.
Let us now look at the document update flow
Document update flow
Figure 13.6 illustrates the process of updating a document, showing how the system handles
updates to metadata and/or content.


Figure 13.6: Document update flow sequence diagram
Here is the flow:
1. The client sends a PUT request to the /documents/{documentId} endpoint with the updated document metadata
and/or content.
2. The Document Service validates the request and retrieves the existing document metadata from the relational database.
3. If the document exists, the Document Service updates the document metadata in the database.
4. If the content is provided in the request, the Document Service stores the updated content in the storage system and updates
the content URL in the document metadata.
5. The updated document object is returned to the client.
Document deletion flow
Figure 13.7 shows the steps involved in deleting a document, including checks for document
existence and removal from both database and storage.


Figure 13.7: A document deletion flow sequence
Here is the flow:
1. The client sends a DELETE request to the /documents/{documentId} endpoint.
2. The Document Service retrieves the document metadata from the relational database based on the document ID.
3. If the document exists, the Document Service deletes the document metadata from the database.
4. The Document Service deletes the associated document content from the Storage System.
5. 5. A success message is returned to the client.
Let us now talk about how to get previous revisions of the content.
Revision history retrieval flow
Figure 13.8 illustrates the process of retrieving the revision history for a document, showing how
the system fetches and returns the list of revisions.


Figure 13.8: A revision history retrieval flow sequence
Here is the flow:
1. The client sends a GET request to the /documents/{documentId}/revisions endpoint.
2. The Document Service retrieves the revision history associated with the specified document ID from the relational
database.
3. The list of revision objects, including metadata and content URLs, is returned to the client.
So far, we have discussed different document service flows. Let us now shift our attention to
some performance and reliability considerations, specifically ones concerning caching and
integrations.
The following are some of the performance and reliability considerations:
Caching: To improve the performance of document retrieval, the Document Service can utilize a distributed caching layer
(e.g., Redis). Frequently accessed documents can be cached along with their metadata and content. When a document is
requested, the Document Service first checks the cache. If the document is found in the cache, it is served directly from
there. If the document is not found in the cache, the Document Service retrieves it from the database and storage system,
stores it in the cache for future requests, and returns it to the client.
In addition to server-side caching, the system can leverage the user’s browser cache to
enhance performance and enable offline functionality. The client-side application can store
local updates in the browser’s cache (e.g., using IndexedDB or LocalStorage) and synchronize
these updates with the server at regular intervals. This approach provides several benefits:


Improved responsiveness: Users experience faster updates as changes are immediately reflected in the local
cache
Offline support: Users can continue working on documents even when they are disconnected from the internet
Resilience: If the user experiences a brief network interruption, their work is not lost and can be synchronized
once the connection is restored
Reduced server load: By batching updates and synchronizing periodically, the system can reduce the number of
real-time server requests
When implementing this strategy, it’s important to handle conflict resolution for cases where
multiple users may have made offline changes to the same document. The system should
employ appropriate merging strategies or provide user interfaces for manual conflict
resolution when necessary.
Error handling and consistency: The Document Service implements error handling mechanisms to gracefully handle and
propagate errors to the client. It includes appropriate error codes and messages in the API responses. The service also
ensures data consistency by using transactions and atomic operations when modifying document metadata in the database. In
case of failures during content storage or retrieval, the service retries the operations or returns appropriate error responses to
the client.
Integration with other services: The Document Service integrates with other services in the file-sharing system, such as
the Collaboration Service and Access Control Service. When a document is created or updated, the Document Service
notifies the Collaboration Service to handle real-time synchronization and presence updates. The Access Control Service is
consulted to enforce access permissions and sharing settings for document operations.
Scalability and performance: To ensure scalability and high performance, the Document Service can be deployed as a
stateless microservice. Multiple instances of the service can run behind a load balancer to distribute the incoming requests.
The relational database can be scaled horizontally using techniques such as sharding or partitioning based on document ID
ranges. The storage system, such as S3, inherently provides scalability and durability for storing and retrieving document
content.
By following this low-level design, the Document Service can efficiently handle documentrelated operations, ensure data consistency, and integrate with other services in the filesharing system. The service is designed to be scalable, performant, and resilient to handle a
large number of concurrent users and document interactions.
In the next section, we will explore the low-level design of the Collaboration Service, which
enables real-time collaboration and synchronization between multiple users working on the same
document.
Designing the Collaboration Service


The Collaboration Service is responsible for enabling real-time collaboration and
synchronization between multiple users working on the same document. It handles OT, conflict
resolution, and presence management to provide a seamless collaborative editing experience.
Figure 13.9 illustrates the key components of the Collaboration Service and its interactions with
clients, other services, and infrastructure components.
Figure 13.9: The Collaboration Service design
Let us now discuss the API endpoints exposed by the service and the flow.
The Collaboration Service exposes the following API endpoints:
POST /collaborate/{documentId}: Join a collaborative editing session for a document
Request body: User ID and session information
Response: Collaboration session details and initial document state


WebSocket/collaborate/{documentId}: Establish a WebSocket connection for real-time collaboration
Clients send and receive collaboration-related events through the WebSocket connection
POST /presence/{documentId}: Update user presence information for a document
Request body: User ID and presence status (e.g., online, offline, or idle)
Response: Success or error message
We will now discuss the collaboration flow with the help of a sequence diagram
Collaboration flow
Figure 13.10 shows the key steps in the collaboration process, including joining a session, realtime editing, and presence management.
Figure 13.10: A collaboration flow sequence
Here are the steps:


1. When a user wants to collaborate on a document, the client sends a POST request to the
/collaborate/{documentId} endpoint.
2. The Collaboration Service validates the request and checks the user’s access permissions for the document.
3. If the user is authorized to collaborate, the Collaboration Service creates a new collaboration session and returns the
session details and initial document state to the client.
4. The client establishes a WebSocket connection with the Collaboration Service using the
/collaborate/{documentId} endpoint.
5. The Collaboration Service manages the WebSocket connections for all clients collaborating on the same document.
6. As users make changes to the document, the client sends collaboration events (e.g., insert, delete, or format) through the
WebSocket connection.
7. The Collaboration Service receives the collaboration events and applies OT techniques to resolve conflicts and maintain a
consistent document state across all collaborators.
8. The transformed events are broadcast to all connected clients through their respective WebSocket connections.
9. The clients receive the collaboration events and update their local document state accordingly, ensuring real-time
synchronization.
We have explained the high-level collaboration workflow; let’s dive into some nuances of
collaboration, specifically those surrounding OT and presence management, next.
OT
OT is a technique used to achieve real-time collaboration while maintaining document
consistency. The Collaboration Service implements OT algorithms to handle concurrent editing
operations and resolve conflicts. The basic idea behind OT is to transform incoming operations
based on the current document state and the history of previously applied operations. This
ensures that the final document state is consistent across all collaborators, regardless of the order
in which the operations were received.
The Collaboration Service maintains a server-side document state and applies incoming
operations to it. It also keeps track of the operation history for each client. When a client sends a
new operation, the Collaboration Service transforms the operation based on the client’s operation
history and the server-side document state. The transformed operation is then applied to the
server-side document state and broadcast to all other clients.
Presence management


The Collaboration Service also manages user presence information to provide real-time
awareness of collaborators’ online status. When a user joins a collaboration session, the client
sends a presence update to the /presence/{documentId} endpoint. The Collaboration Service
updates the user’s presence status and notifies other collaborators about the change.
The Collaboration Service maintains a presence map that associates each document with the list
of collaborators and their presence status. It periodically checks for inactive or disconnected
clients and updates their presence status accordingly. Clients can also explicitly notify the
Collaboration Service when they go offline or become idle.
Scalability and performance
To ensure scalability and high performance, the Collaboration Service can be deployed as a
stateless microservice. Multiple instances of the service can run behind a load balancer to
distribute the incoming requests and WebSocket connections. The service can utilize a
distributed caching layer (e.g., Redis) to store the server-side document state and presence
information. This allows for quick access and synchronization across multiple service instances.
The Collaboration Service can also leverage message queues (e.g., Apache Kafka) to handle the
broadcasting of collaboration events to connected clients. This decouples the event processing
from the WebSocket connection handling and allows for asynchronous processing and
scalability.
Integration with other services
The Collaboration Service integrates with the Document Service to retrieve and update document
content. When a collaboration session is initiated, the Collaboration Service fetches the initial
document state from the Document Service. As users make changes to the document, the
Collaboration Service sends the updated content to the Document Service for persistence.
The Collaboration Service also interacts with the Access Control Service to enforce access
permissions and ensure that only authorized users can collaborate on a document. It verifies the
user’s access rights before allowing them to join a collaboration session.
Error handling and resilience
The Collaboration Service implements error-handling mechanisms to handle and recover from
various failure scenarios. It includes appropriate error logging and monitoring to detect and


diagnose issues. In case of network disruptions or service failures, the Collaboration Service
attempts to reconnect clients and synchronize the document state.
To ensure data integrity and consistency, the Collaboration Service implements transaction
management and atomic operations when updating the server-side document state and presence
information. It also includes data validation and sanitization to prevent malicious or invalid
collaboration events from compromising the document state.
Security considerations
The Collaboration Service enforces security measures to protect the confidentiality and integrity
of collaborative editing sessions. It uses secure communication protocols (e.g., HTTPS or WSS)
to encrypt data in transit. Access control mechanisms are implemented to ensure that only
authorized users can join collaboration sessions and access document content.
The Collaboration Service also implements rate limiting and throttling to prevent abuse and
protect against denial-of-service attacks. It monitors and logs collaboration activities for auditing
and security analysis purposes.
By following this low-level design, the Collaboration Service enables real-time collaboration and
synchronization between multiple users, providing a seamless and interactive editing experience.
The service is designed to handle concurrent editing operations, resolve conflicts, and maintain
document consistency. It integrates with other services, such as the Document Service and
Access Control Service, to provide a comprehensive collaborative editing solution.
In the next section, we will explore the low-level design of the Access Control Service, which
handles user authentication, authorization, and access management for the file-sharing system.
Designing the Access Control Service
The Access Control Service is responsible for managing user authentication, authorization, and
access permissions in the file-sharing system. It ensures that only authorized users can access
and perform actions on documents based on their assigned roles and permissions. Figure 13.11
illustrates the key components of the Access Control Service and its interactions with clients,
databases, and other services in the system.


Figure 13.11: Access control service design
Let us discuss the API endpoints this service will expose next. The Access Control Service
exposes the following API endpoints:
POST /auth/login: Authenticate a user and generate an access token
Request body: User credentials (e.g., username and password)
Response: Access token and user information upon successful authentication
POST /auth/logout: Invalidate a user’s access token and log them out
Request body: Access token
Response: Success or error message
GET /permissions/{documentId}: Get the access permissions for a document
Request parameters: Document ID
Response: List of user permissions for the document
POST /permissions/{documentId}: Grant or update access permissions for a document
Request body: User ID, document ID, and permission level (e.g., read, write, or owner)


Response: Success or error message
DELETE/permissions/{documentId}/{userId}: Revoke access permissions for a user in a document
Request parameters: Document ID and user ID
Response: Success or error message
Now that we have discussed the API endpoints, let us understand different authentication and
authorization flows
Authentication flow
Figure 13.12 shows the steps involved in user authentication, from credential submission to
access token generation
Figure 13.12: An authentication flow sequence
Here is the flow:
1. When a user logs in, the client sends a POST request to the /auth/login endpoint with the user’s credentials.
2. The Access Control Service verifies the credentials against the user database.


3. If the credentials are valid, the Access Control Service generates an access token (e.g., JSON Web Token (JWT)) that
contains the user’s ID, role, and other relevant information.
4. The access token is returned to the client along with the user’s information.
5. The client includes the access token in the headers of subsequent requests to authenticate and authorize the user.
Authorization flow
Figure 13.13 illustrates the process of authorizing a user’s request, including token verification
and permission checking.
Figure 13.13: An authorization flow sequence
Here is the flow:
1. When a client makes a request to access a document or performs an action, it includes the access token in the request
headers.
2. The Access Control Service intercepts the request and verifies the validity and integrity of the access token.


3. If the access token is valid, the Access Control Service extracts the user’s ID and role from the token.
4. The Access Control Service retrieves the access permissions for the user on the requested document from the permissions
database.
5. Based on the user’s role and permissions, the Access Control Service determines whether the user is authorized to perform
the requested action.
6. If the user is authorized, the request is forwarded to the appropriate service (e.g., Document Service) for further processing.
7. If the user is not authorized, the Access Control Service returns an appropriate error response.
Permission management
Figure 13.14 shows the steps involved in granting or updating permissions for a document,
including the validation of the requester’s permissions.
Figure 13.14: A permission management sequence
Here is the flow:


1. Document owners or users with appropriate permissions can grant or update access permissions for other users on a
document.
2. The client sends a POST request to the /permissions/{documentId} endpoint with the user ID, document ID, and
permission level.
3. The Access Control Service validates the request and verifies that the requesting user has sufficient permissions to grant or
update permissions.
4. If the request is valid, the Access Control Service updates the permissions database with the new or updated permission
entry.
5. The Access Control Service returns a success message to the client.
Revoking permissions
Figure 13.15 shows the steps involved in revoking a user’s permissions for a document,
including the validation of the requester’s permissions and the removal of the permission entry
from the database.
Figure 13.15: A revoking permissions sequence
Here is the flow:


1. Document owners or users with appropriate permissions can revoke access permissions for a user on a document.
2. The client sends a DELETE request to the /permissions/{documentId}/{userId} endpoint with the document
ID and user ID.
3. The Access Control Service validates the request and verifies that the requesting user has sufficient permissions to revoke
permissions.
4. If the request is valid, the Access Control Service removes the permission entry from the permissions database.
5. The Access Control Service returns a success message to the client.
Database design
The Access Control Service uses a database to store user information, access tokens, and
permissions.
Figure 13.16 illustrates the structure of the database tables used by the Access Control Service,
showing the relationships between Users, AccessTokens, Permissions, and Documents.
Figure 13.16: An entity-relationship diagram for an Access Control Service database
Some key points from the entity-relationship diagram are as follows:
A User can have multiple AccessTokens and Permissions
A Document can have multiple Permissions associated with it
The Permission table acts as a junction table, connecting Users and Documents with specific permission levels
The AccessToken table allows for the management of active sessions and token expiration
We will now look at how caching can help improve the performance of this service.


Caching and performance
To improve the performance of the Access Control Service, it can utilize a caching layer (e.g.,
Redis) to store frequently accessed permissions and user information. When a request is made to
check permissions, the Access Control Service first checks the cache. If the permissions are
found in the cache, they are served directly from there, reducing the load on the database.
The Access Control Service can also implement rate limiting and throttling mechanisms to
prevent abuse and protect against unauthorized access attempts. It can monitor and log access
control activities for auditing and security analysis purposes.
By following this low-level design, the Access Control Service provides a robust and secure
mechanism for managing user authentication, authorization, and access permissions in the filesharing system. It ensures that only authorized users can access and perform actions on
documents based on their assigned roles and permissions. The service integrates with other
components of the system to enforce access control throughout the application.
In the next section, we will discuss additional considerations and best practices for designing and
implementing the file-sharing system, taking into account factors such as performance
optimization, data consistency, and fault tolerance.
Additional considerations and best practices
When designing and implementing a file-sharing system such as Google Docs, there are several
additional considerations and best practices to keep in mind. These considerations ensure that the
system is robust, performant, and provides a seamless user experience. Let’s explore some of
these key aspects:
Performance optimization:
Implement caching mechanisms at various levels of the system to reduce latency and improve response times.
This can include caching frequently accessed documents, user permissions, and metadata.
Utilize Content Delivery Networks (CDNs) to serve static assets, such as images and client-side scripts, from
geographically distributed servers closer to the users.
Optimize database queries and indexes to minimize the response time for common operations, such as document
retrieval and permission checks.
Employ lazy loading techniques to load document content and collaborators incrementally as needed, reducing
the initial load time.


Implement pagination and limit the number of results returned by API endpoints to avoid overloading the system
and improve performance.
Data consistency and concurrency:
Ensure that the system maintains data consistency across all services and components, especially in scenarios
involving concurrent editing and real-time collaboration.
Implement optimistic concurrency control mechanisms, such as version numbers or timestamps, to detect and
resolve conflicts when multiple users are editing the same document simultaneously.
Use distributed locking or synchronization techniques to prevent data inconsistencies and ensure atomic
operations when necessary.
Employ eventual consistency models where appropriate, allowing for temporary inconsistencies in favor of
higher availability and performance.
Fault tolerance and resilience:
Design the system to be resilient to failures and to be able to recover gracefully from errors and exceptions.
Implement error handling and logging mechanisms to capture and diagnose issues promptly.
Use circuit breakers and retry mechanisms to handle temporary failures and prevent cascading failures across
services.
Employ redundancy and replication techniques to ensure high availability and minimize the impact of hardware
or network failures.
Regularly backup data and implement disaster recovery procedures to protect against data loss and ensure
business continuity.
Scalability and elasticity:
Design the system to be horizontally scalable, allowing for the addition of more instances of services as the user
base and traffic grow.
Utilize auto-scaling techniques to automatically adjust the number of service instances based on the incoming
load, ensuring optimal resource utilization and cost efficiency.
Implement load balancing mechanisms to evenly distribute the workload across multiple instances of services.
Use message queues and asynchronous processing to decouple services and handle spikes in traffic or resourceintensive tasks.
Continuous Integration and Continuous Deployment (CI/CD):
Implement a robust CI/CD pipeline to automate the building, testing, and deployment processes for the filesharing system.
Use version control systems (e.g., Git) to manage the codebase and enable collaborative development.


Automate unit tests, integration tests, and end-to-end tests to catch bugs and ensure the stability and reliability of
the system.
Utilize containerization technologies (e.g., Docker) and orchestration platforms (e.g., Kubernetes) to streamline
the deployment and management of services.
Implement blue-green deployments, canary releases, or rolling updates to minimize downtime and risk during
deployments.
By considering these additional aspects and best practices, the file-sharing system can be
designed and implemented to be performant, scalable, secure, and user-friendly. It is important to
continuously monitor, measure, and iterate on the system based on user feedback, performance
metrics, and changing requirements to ensure its long-term success and adoption.
Summary
In this chapter, we explored the system design of a file-sharing service such as Google Docs,
covering various aspects such as functional and non-functional requirements, data modeling,
scalability considerations, and architectural components. We delved into the high-level design,
laying out the overall architecture and the interaction between different services and components.
Throughout the chapter, we emphasized the importance of scalability, performance, and user
experience. The system has been designed to handle a large number of users, documents, and
concurrent editing operations by leveraging distributed architectures, caching mechanisms, and
real-time collaboration techniques. We learned that the use of microservices architecture allows
for the independent scaling and deployment of individual components, ensuring flexibility and
maintainability.
We also discussed the critical role of data consistency and integrity in a file-sharing system. The
use of OT algorithms and conflict resolution techniques ensures that documents remain
consistent across multiple collaborators and editing sessions. The data model has been designed
to efficiently store and retrieve document metadata, revisions, and permissions, enabling fast
access and modification.
Furthermore, we discussed additional considerations and best practices that contribute to the
success and user adoption of a file-sharing system. We learned that performance optimization
techniques, such as caching and lazy loading, help in delivering a responsive and smooth user
experience. Collaboration features, such as real-time editing, comments, and suggestions, foster
teamwork and productivity, as we learned in this chapter. We also learned that CI/CD practices


enable rapid iteration and delivery of new features and bug fixes. In the next chapter, we will
look into designing a service such as Netflix.

## Examples & Scenarios

- associates a user with a document and specifies the permission level (e.g., view, edit, or comment) and the timestamp when
the permission was granted.
The Comment entity represents comments made by users on specific documents. It contains the comment content, the
associated document and user, and the creation timestamp.
The Suggestion entity represents suggested changes or edits to a document. It includes the suggested content, associated
document and user, status of the suggestion (e.g., pending, accepted, or rejected), and creation timestamp.
The Folder entity allows users to organize their documents into folders. It contains the folder name, associated user, and
creation timestamp.
The FolderDocument entity represents the relationship between folders and documents, indicating which documents are
contained within each folder.

- To improve performance and reduce the load on the backend services, a distributed caching layer (e.g., Redis)
will be employed. The caching layer will store frequently accessed data, such as document metadata, user
sessions, and commonly retrieved document content. Caching will help in serving data quickly and reducing the
number of requests to the database and storage systems.

- Relational database (e.g., PostgreSQL):
Stores metadata information such as user profiles, document metadata, access permissions, and collaboration
details
Provides ACID properties and supports complex querying and transactions
NoSQL database (e.g., MongoDB):
Stores document revisions and content
Provides scalability and flexibility for handling large amounts of unstructured data
Storage system:
Document content, revisions, and attachments will be stored in a distributed storage system (e.g., Amazon S3 or
Google Cloud Storage). Document types could be text files, videos, images, multimedia files, and so on. We may

- using tools such as Prometheus and Grafana. Centralized logging solutions (e.g., ELK stack) will be used to
aggregate and analyze logs from all components.
Security and privacy:
Security and privacy measures will be implemented throughout the system. User authentication and
authorization will be handled using secure protocols such as OAuth. Sensitive data, such as passwords and
access tokens, will be securely hashed and stored. Data encryption will be applied to protect user data both in
transit and at rest. Regular security audits and penetration testing will be conducted to identify and address
potential vulnerabilities.

- 4. The initial content is stored in the storage system (e.g., S3), and the content URL is obtained.
5. The Document Service updates the document metadata with the content URL.
6. The created document object is returned to the client with the assigned document ID.
Let us now look at the retrieval flow.
Document retrieval flow
Figure 13.5 illustrates the process of retrieving a document, including fetching metadata from
the database and content from the storage system.

- (e.g., Redis). Frequently accessed documents can be cached along with their metadata and content. When a document is
requested, the Document Service first checks the cache. If the document is found in the cache, it is served directly from
there. If the document is not found in the cache, the Document Service retrieves it from the database and storage system,
stores it in the cache for future requests, and returns it to the client.
In addition to server-side caching, the system can leverage the user’s browser cache to
enhance performance and enable offline functionality. The client-side application can store
local updates in the browser’s cache (e.g., using IndexedDB or LocalStorage) and synchronize
these updates with the server at regular intervals. This approach provides several benefits:

- Request body: User ID and presence status (e.g., online, offline, or idle)
Response: Success or error message
We will now discuss the collaboration flow with the help of a sequence diagram
Collaboration flow
Figure 13.10 shows the key steps in the collaboration process, including joining a session, realtime editing, and presence management.
Figure 13.10: A collaboration flow sequence
Here are the steps:

- 6. As users make changes to the document, the client sends collaboration events (e.g., insert, delete, or format) through the
WebSocket connection.
7. The Collaboration Service receives the collaboration events and applies OT techniques to resolve conflicts and maintain a
consistent document state across all collaborators.
8. The transformed events are broadcast to all connected clients through their respective WebSocket connections.
9. The clients receive the collaboration events and update their local document state accordingly, ensuring real-time
synchronization.
We have explained the high-level collaboration workflow; let’s dive into some nuances of
collaboration, specifically those surrounding OT and presence management, next.
OT

- distributed caching layer (e.g., Redis) to store the server-side document state and presence
information. This allows for quick access and synchronization across multiple service instances.
The Collaboration Service can also leverage message queues (e.g., Apache Kafka) to handle the
broadcasting of collaboration events to connected clients. This decouples the event processing
from the WebSocket connection handling and allows for asynchronous processing and
scalability.
Integration with other services
The Collaboration Service integrates with the Document Service to retrieve and update document
content. When a collaboration session is initiated, the Collaboration Service fetches the initial
document state from the Document Service. As users make changes to the document, the

- of collaborative editing sessions. It uses secure communication protocols (e.g., HTTPS or WSS)
to encrypt data in transit. Access control mechanisms are implemented to ensure that only
authorized users can join collaboration sessions and access document content.
The Collaboration Service also implements rate limiting and throttling to prevent abuse and
protect against denial-of-service attacks. It monitors and logs collaboration activities for auditing
and security analysis purposes.
By following this low-level design, the Collaboration Service enables real-time collaboration and
synchronization between multiple users, providing a seamless and interactive editing experience.
The service is designed to handle concurrent editing operations, resolve conflicts, and maintain
document consistency. It integrates with other services, such as the Document Service and

- Request body: User credentials (e.g., username and password)
Response: Access token and user information upon successful authentication
POST /auth/logout: Invalidate a user’s access token and log them out
Request body: Access token
Response: Success or error message
GET /permissions/{documentId}: Get the access permissions for a document
Request parameters: Document ID
Response: List of user permissions for the document
POST /permissions/{documentId}: Grant or update access permissions for a document
Request body: User ID, document ID, and permission level (e.g., read, write, or owner)

- 3. If the credentials are valid, the Access Control Service generates an access token (e.g., JSON Web Token (JWT)) that
contains the user’s ID, role, and other relevant information.
4. The access token is returned to the client along with the user’s information.
5. The client includes the access token in the headers of subsequent requests to authenticate and authorize the user.
Authorization flow
Figure 13.13 illustrates the process of authorizing a user’s request, including token verification
and permission checking.
Figure 13.13: An authorization flow sequence
Here is the flow:
1. When a client makes a request to access a document or performs an action, it includes the access token in the request

- 6. If the user is authorized, the request is forwarded to the appropriate service (e.g., Document Service) for further processing.
7. If the user is not authorized, the Access Control Service returns an appropriate error response.
Permission management
Figure 13.14 shows the steps involved in granting or updating permissions for a document,
including the validation of the requester’s permissions.
Figure 13.14: A permission management sequence
Here is the flow:

- To improve the performance of the Access Control Service, it can utilize a caching layer (e.g.,
Redis) to store frequently accessed permissions and user information. When a request is made to
check permissions, the Access Control Service first checks the cache. If the permissions are
found in the cache, they are served directly from there, reducing the load on the database.
The Access Control Service can also implement rate limiting and throttling mechanisms to
prevent abuse and protect against unauthorized access attempts. It can monitor and log access
control activities for auditing and security analysis purposes.
By following this low-level design, the Access Control Service provides a robust and secure
mechanism for managing user authentication, authorization, and access permissions in the filesharing system. It ensures that only authorized users can access and perform actions on
documents based on their assigned roles and permissions. The service integrates with other

- Use version control systems (e.g., Git) to manage the codebase and enable collaborative development.

- Utilize containerization technologies (e.g., Docker) and orchestration platforms (e.g., Kubernetes) to streamline
the deployment and management of services.
Implement blue-green deployments, canary releases, or rolling updates to minimize downtime and risk during
deployments.
By considering these additional aspects and best practices, the file-sharing system can be
designed and implemented to be performant, scalable, secure, and user-friendly. It is important to
continuously monitor, measure, and iterate on the system based on user feedback, performance
metrics, and changing requirements to ensure its long-term success and adoption.
Summary
In this chapter, we explored the system design of a file-sharing service such as Google Docs,

