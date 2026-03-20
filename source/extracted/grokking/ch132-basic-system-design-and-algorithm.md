# 3. Basic System Design and Algorithm

> Source: System Design - Grokking (Notes), Chapter 132, Pages 34-34

## Key Concepts

- Designing Typeahead Suggestion
Let's design a real-time suggestion service, which will recommend terms to users as they enter text for
searching.
Similar Services: Auto-suggestions, Typeahead search
D

## Content

Designing Typeahead Suggestion
Let's design a real-time suggestion service, which will recommend terms to users as they enter text for
searching.
Similar Services: Auto-suggestions, Typeahead search
Difficulty: Medium
1. What is Typeahead Suggestion?
Typeahead suggestions enable users to search for known and frequently searched terms. As the user
types into the search box, it tries to predict the query based on the characters the user has entered and
gives a list of suggestions to complete the query. Typeahead suggestions help the user to articulate
their search queries better. It’s not about speeding up the search process but rather about guiding the
users and lending them a helping hand in constructing their search query.
2. Requirements and Goals of the System
Functional Requirements: As the user types in their query, our service should suggest top 10 terms
starting with whatever the user has typed.
Non-function Requirements: The suggestions should appear in real-time. The user should be able
to see the suggestions within 200ms.
3. Basic System Design and Algorithm
The problem we are solving is that we have a lot of ‘strings’ that we need to store in such a way that
users can search with any prefix. Our service will suggest next terms that will match the given prefix.
For example, if our database contains the following terms: cap, cat, captain, or capital and the user has
typed in ‘cap’, our system should suggest ‘cap’, ‘captain’ and ‘capital’.
Since we’ve got to serve a lot of queries with minimum latency, we need to come up with a scheme that
can efficiently store our data such that it can be queried quickly. We can’t depend upon some database
for this; we need to store our index in memory in a highly efficient data structure.
One of the most appropriate data structures that can serve our purpose is the Trie (pronounced “try”).
A trie is a tree-like data structure used to store phrases where each node stores a character of the
phrase in a sequential manner. For example, if we need to store ‘cap, cat, caption, captain, capital’ in
the trie, it would look like:
Now if the user has typed ‘cap’, our service can traverse the trie to go to the node ‘P’ to find all the
terms that start with this prefix (e.g., cap-tion, cap-ital etc).
We can merge nodes that have only one branch to save storage space. The above trie can be stored like
this:
Should we have case insensitive trie? For simplicity and search use-case, let’s assume our data is
case insensitive.
How to find top suggestion? Now that we can find all the terms for a given prefix, how can we find
the top 10 terms for the given prefix? One simple solution could be to store the count of searches that

## Examples & Scenarios

- For example, if our database contains the following terms: cap, cat, captain, or capital and the user has
typed in ‘cap’, our system should suggest ‘cap’, ‘captain’ and ‘capital’.
Since we’ve got to serve a lot of queries with minimum latency, we need to come up with a scheme that
can efficiently store our data such that it can be queried quickly. We can’t depend upon some database
for this; we need to store our index in memory in a highly efficient data structure.
One of the most appropriate data structures that can serve our purpose is the Trie (pronounced “try”).
A trie is a tree-like data structure used to store phrases where each node stores a character of the
phrase in a sequential manner. For example, if we need to store ‘cap, cat, caption, captain, capital’ in
the trie, it would look like:
Now if the user has typed ‘cap’, our service can traverse the trie to go to the node ‘P’ to find all the

- terms that start with this prefix (e.g., cap-tion, cap-ital etc).
We can merge nodes that have only one branch to save storage space. The above trie can be stored like
this:
Should we have case insensitive trie? For simplicity and search use-case, let’s assume our data is
case insensitive.
How to find top suggestion? Now that we can find all the terms for a given prefix, how can we find
the top 10 terms for the given prefix? One simple solution could be to store the count of searches that

