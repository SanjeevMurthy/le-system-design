# 11. Personalization

> Source: System Design - Grokking (Notes), Chapter 140, Pages 37-37

## Key Concepts

- Stuck? Get help on   
DISCUSS
on the prefixes.
9. Fault Tolerance
What will happen when a trie server goes down? As discussed above we can have a masterslave configuration; if the master dies, the sla

## Content

Stuck? Get help on   
DISCUSS
on the prefixes.
9. Fault Tolerance
What will happen when a trie server goes down? As discussed above we can have a masterslave configuration; if the master dies, the slave can take over after failover. Any server that comes back
up, can rebuild the trie based on the last snapshot.
10. Typeahead Client
We can perform the following optimizations on the client side to improve user’s experience:
1. The client should only try hitting the server if the user has not pressed any key for 50ms.
2. If the user is constantly typing, the client can cancel the in-progress requests.
3. Initially, the client can wait until the user enters a couple of characters.
4. Clients can pre-fetch some data from the server to save future requests.
5. Clients can store the recent history of suggestions locally. Recent history has a very high rate of
being reused.
6. Establishing an early connection with the server turns out to be one of the most important
factors. As soon as the user opens the search engine website, the client can open a connection with
the server. So when a user types in the first character, the client doesn’t waste time in establishing
the connection.
7. The server can push some part of their cache to CDNs and Internet Service Providers (ISPs) for
efficiency.
11. Personalization
Users will receive some typeahead suggestions based on their historical searches, location, language,
etc. We can store the personal history of each user separately on the server and also cache them on the
client. The server can add these personalized terms in the final set before sending it to the user.
Personalized searches should always come before others.
←    Back
Designing Youtube…
Next    →
Designing an API R…
Completed
Send feedback
51 Recommendations

