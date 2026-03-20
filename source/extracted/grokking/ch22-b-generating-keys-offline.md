# b. Generating keys offline #

> Source: System Design - Grokking (Notes), Chapter 22, Pages 5-5

## Key Concepts

- understand the data flow among various components and later would guide towards
data partitioning.
A few observations about the nature of the data we will store:
1. We need to store billions of record

## Content

understand the data flow among various components and later would guide towards
data partitioning.
A few observations about the nature of the data we will store:
1. We need to store billions of records.
2. Each object we store is small (less than 1K).
3. There are no relationships between records—other than storing which user created a URL.
4. Our service is read-heavy.
Database Schema: #
We would need two tables: one for storing information about the URL mappings, and one for the user’s
data who created the short link.
URL
Hash: varchar(16)
PK
OriginalURL: varchar(512)
CreationDate: datetime
ExpirationDate: datatime
UserID: int
User
UserID: int
PK
Name: varchar(20)
Email: varchar(32)
CreationDate: datetime
LastLogin: datatime
What kind of database should we use?  Since we anticipate storing billions of rows, and we don’t
need to use relationships between objects – a NoSQL store like DynamoDB, Cassandra or Riak is a
better choice. A NoSQL choice would also be easier to scale. Please see SQL vs NoSQL for more details.
6. Basic System Design and Algorithm
#
The problem we are solving here is, how to generate a short and unique key for a given URL.
In the TinyURL example in Section 1, the shortened URL is “http://tinyurl.com/jlg8zpc”. The last
seven characters of this URL is the short key we want to generate. We’ll explore two solutions here:
a. Encoding actual URL #
We can compute a unique hash (e.g., MD5 or SHA256, etc.) of the given URL. The hash can then be
encoded for displaying. This encoding could be base36 ([a-z ,0-9]) or base62 ([A-Z, a-z, 0-9]) and if we
add ‘+’ and ‘/’ we can use Base64 encoding. A reasonable question would be, what should be the length
of the short key? 6, 8, or 10 characters?
Using base64 encoding, a 6 letters long key would result in 64^6 = ~68.7 billion possible strings
Using base64 encoding, an 8 letters long key would result in 64^8 = ~281 trillion possible strings
With 68.7B unique strings, let’s assume six letter keys would suffice for our system.
If we use the MD5 algorithm as our hash function, it’ll produce a 128-bit hash value. After base64
encoding, we’ll get a string having more than 21 characters (since each base64 character encodes 6 bits
of the hash value). Now we only have space for 8 characters per short key, how will we choose our key
then? We can take the first 6 (or 8) letters for the key. This could result in key duplication, to resolve
that, we can choose some other characters out of the encoding string or swap some characters.
What are the different issues with our solution? We have the following couple of problems
with our encoding scheme:
1. If multiple users enter the same URL, they can get the same shortened URL, which is not
acceptable.
2. What if parts of the URL are URL-encoded? e.g., http://www.educative.io/distributed.php?
id=design, and http://www.educative.io/distributed.php%3Fid%3Ddesign are identical except for
the URL encoding.
Workaround for the issues: We can append an increasing sequence number to each input URL to
make it unique, and then generate a hash of it. We don’t need to store this sequence number in the
databases, though. Possible problems with this approach could be an ever-increasing sequence
number. Can it overflow? Appending an increasing sequence number will also impact the performance
of the service.
Another solution could be to append user id (which should be unique) to the input URL. However, if
the user has not signed in, we would have to ask the user to choose a uniqueness key. Even after this, if
we have a conflict, we have to keep generating a key until we get a unique one.
Request flow for shortening of a URL
1 of 9
b. Generating keys offline #
We can have a standalone Key Generation Service (KGS) that generates random six-letter strings
beforehand and stores them in a database (let’s call it key-DB). Whenever we want to shorten a URL,
we will just take one of the already-generated keys and use it. This approach will make things quite
simple and fast. Not only are we not encoding the URL, but we won’t have to worry about duplications
or collisions. KGS will make sure all the keys inserted into key-DB are unique
Can concurrency cause problems? As soon as a key is used, it should be marked in the database
to ensure it doesn’t get reuse. If there are multiple servers reading keys concurrently, we might get a
scenario where two or more servers try to read the same key from the database. How can we solve this
concurrency problem?
Servers can use KGS to read/mark keys in the database. KGS can use two tables to store keys: one for
keys that are not used yet, and one for all the used keys. As soon as KGS gives keys to one of the
servers, it can move them to the used keys table. KGS can always keep some keys in memory so that it
can quickly provide them whenever a server needs them.
For simplicity, as soon as KGS loads some keys in memory, it can move them to the used keys table.
This ensures each server gets unique keys If KGS dies before assigning all the loaded keys to some

## Examples & Scenarios

- We can compute a unique hash (e.g., MD5 or SHA256, etc.) of the given URL. The hash can then be
encoded for displaying. This encoding could be base36 ([a-z ,0-9]) or base62 ([A-Z, a-z, 0-9]) and if we
add ‘+’ and ‘/’ we can use Base64 encoding. A reasonable question would be, what should be the length
of the short key? 6, 8, or 10 characters?
Using base64 encoding, a 6 letters long key would result in 64^6 = ~68.7 billion possible strings
Using base64 encoding, an 8 letters long key would result in 64^8 = ~281 trillion possible strings
With 68.7B unique strings, let’s assume six letter keys would suffice for our system.
If we use the MD5 algorithm as our hash function, it’ll produce a 128-bit hash value. After base64
encoding, we’ll get a string having more than 21 characters (since each base64 character encodes 6 bits
of the hash value). Now we only have space for 8 characters per short key, how will we choose our key

- 2. What if parts of the URL are URL-encoded? e.g., http://www.educative.io/distributed.php?
id=design, and http://www.educative.io/distributed.php%3Fid%3Ddesign are identical except for
the URL encoding.
Workaround for the issues: We can append an increasing sequence number to each input URL to
make it unique, and then generate a hash of it. We don’t need to store this sequence number in the
databases, though. Possible problems with this approach could be an ever-increasing sequence
number. Can it overflow? Appending an increasing sequence number will also impact the performance
of the service.
Another solution could be to append user id (which should be unique) to the input URL. However, if
the user has not signed in, we would have to ask the user to choose a uniqueness key. Even after this, if

## Tables & Comparisons

| URL |  |  | User |  |
| --- | --- | --- | --- | --- |
| PK | Hash: varchar(16) |  | PK | UserID: int |
|  | OriginalURL: varchar(512)
CreationDate: datetime
ExpirationDate: datatime
UserID: int |  |  | Name: varchar(20)
Email: varchar(32)
CreationDate: datetime
LastLogin: datatime |

