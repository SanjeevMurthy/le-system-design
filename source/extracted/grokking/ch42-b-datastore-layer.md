# b. Datastore layer

> Source: System Design - Grokking (Notes), Chapter 42, Pages 10-10

## Key Concepts

- Where “api_paste_key” is a string representing the Paste Key of the paste to be retrieved. This API will
return the textual data of the paste.
deletePaste(api_dev_key, api_paste_key)
A successful dele

## Content

Where “api_paste_key” is a string representing the Paste Key of the paste to be retrieved. This API will
return the textual data of the paste.
deletePaste(api_dev_key, api_paste_key)
A successful deletion returns ‘true’, otherwise returns ‘false’.
6. Database Design
A few observations about the nature of the data we are storing:
1. We need to store billions of records.
2. Each metadata object we are storing would be small (less than 1KB).
3. Each paste object we are storing can be of medium size (it can be a few MB).
4. There are no relationships between records, except if we want to store which user created what
Paste.
5. Our service is read-heavy.
Database Schema:
We would need two tables, one for storing information about the Pastes and the other for users’ data.
Here, ‘URlHash’ is the URL equivalent of the TinyURL and ‘ContentKey’ is a reference to an external
object storing the contents of the paste; we’ll discuss the external storage of the paste contents later in
the chapter.
7. High Level Design
At a high level, we need an application layer that will serve all the read and write requests. Application
layer will talk to a storage layer to store and retrieve data. We can segregate our storage layer with one
database storing metadata related to each paste, users, etc., while the other storing the paste contents
in some object storage (like Amazon S3). This division of data will also allow us to scale them
individually.
Client
Object storage
Application server
Metadata storage
8. Component Design
a. Application layer
Our application layer will process all incoming and outgoing requests. The application servers will be
talking to the backend data store components to serve the requests.
How to handle a write request?  Upon receiving a write request, our application server will
generate a six-letter random string, which would serve as the key of the paste (if the user has not
provided a custom key). The application server will then store the contents of the paste and the
generated key in the database. After the successful insertion, the server can return the key to the user.
One possible problem here could be that the insertion fails because of a duplicate key. Since we are
generating a random key, there is a possibility that the newly generated key could match an existing
one. In that case, we should regenerate a new key and try again. We should keep retrying until we don’t
see failure due to the duplicate key. We should return an error to the user if the custom key they have
provided is already present in our database.
Another solution of the above problem could be to run a standalone Key Generation Service (KGS)
that generates random six letters strings beforehand and stores them in a database (let’s call it key-
DB). Whenever we want to store a new paste, we will just take one of the already generated keys and
use it. This approach will make things quite simple and fast since we will not be worrying about
duplications or collisions. KGS will make sure all the keys inserted in key-DB are unique. KGS can use
two tables to store keys, one for keys that are not used yet and one for all the used keys. As soon as KGS
gives some keys to an application server, it can move these to the used keys table. KGS can always keep
some keys in memory so that whenever a server needs them, it can quickly provide them. As soon as
KGS loads some keys in memory, it can move them to the used keys table, this way we can make sure
each server gets unique keys. If KGS dies before using all the keys loaded in memory, we will be
wasting those keys. We can ignore these keys given that we have a huge number of them.
Isn’t KGS a single point of failure?  Yes, it is. To solve this, we can have a standby replica of KGS
and whenever the primary server dies it can take over to generate and provide keys.
Can each app server cache some keys from key-DB?  Yes, this can surely speed things up.
Although in this case, if the application server dies before consuming all the keys, we will end up losing
those keys. This could be acceptable since we have 68B unique six letters keys, which are a lot more
than we require.
How does it handle a paste read request?  Upon receiving a read paste request, the application
service layer contacts the datastore. The datastore searches for the key, and if it is found, returns the
paste’s contents. Otherwise, an error code is returned.
b. Datastore layer
We can divide our datastore layer into two:

