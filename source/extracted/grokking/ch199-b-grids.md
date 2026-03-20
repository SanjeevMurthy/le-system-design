# b. Grids

> Source: System Design - Grokking (Notes), Chapter 199, Pages 54-54

## Key Concepts

- Each Place can have the following fields:
1. LocationID (8 bytes): Uniquely identifies a location.
2. Name (256 bytes)
3. Latitude (8 bytes)
4. Longitude (8 bytes)
5. Description (512 bytes)
6. Catego

## Content

Each Place can have the following fields:
1. LocationID (8 bytes): Uniquely identifies a location.
2. Name (256 bytes)
3. Latitude (8 bytes)
4. Longitude (8 bytes)
5. Description (512 bytes)
6. Category (1 byte): E.g., coffee shop, restaurant, theater, etc.
Although a four bytes number can uniquely identify 500M locations, with future growth in mind, we
will go with 8 bytes for LocationID.
Total size: 8 + 256 + 8 + 8 + 512 + 1 => 793 bytes
We also need to store reviews, photos, and ratings of a Place. We can have a separate table to store
reviews for Places:
1. LocationID (8 bytes)
2. ReviewID (4 bytes): Uniquely identifies a review, assuming any location will not have more than
2^32 reviews.
3. ReviewText (512 bytes)
4. Rating (1 byte): how many stars a place gets out of ten.
Similarly, we can have a separate table to store photos for Places and Reviews.
5. System APIs
We can have SOAP or REST APIs to expose the functionality of our service. The following could be the
definition of the API for searching:
search(api_dev_key, search_terms, user_location, radius_filter, maximum_results_to
_return, 
    category_filter, sort, page_token)
Parameters:
api_dev_key (string): The API developer key of a registered account. This will be used to, among other
things, throttle users based on their allocated quota.
search_terms (string): A string containing the search terms.
user_location (string): Location of the user performing the search.
radius_filter (number): Optional search radius in meters.
maximum_results_to_return (number): Number of business results to return.
category_filter (string): Optional category to filter search results, e.g., Restaurants, Shopping Centers,
etc.
sort (number): Optional sort mode: Best matched (0 - default), Minimum distance (1), Highest rated
(2).
page_token (string): This token will specify a page in the result set that should be returned.
Returns: (JSON)
A JSON containing information about a list of businesses matching the search query. Each result entry
will have the business name, address, category, rating, and thumbnail.
6. Basic System Design and Algorithm
At a high level, we need to store and index each dataset described above (places, reviews, etc.). For
users to query this massive database, the indexing should be read efficient, since while searching for
the nearby places users expect to see the results in real-time.
Given that the location of a place doesn’t change that often, we don’t need to worry about frequent
updates of the data. As a contrast, if we intend to build a service where objects do change their location
frequently, e.g., people or taxis, then we might come up with a very different design.
Let’s see what are different ways to store this data and also find out which method will suit best for our
use cases:
a. SQL solution
One simple solution could be to store all the data in a database like MySQL. Each place will be stored
in a separate row, uniquely identified by LocationID. Each place will have its longitude and latitude
stored separately in two different columns, and to perform a fast search; we should have indexes on
both these fields.
To find all the nearby places of a given location (X, Y) within a radius ‘D’, we can query like this:
Select * from Places where Latitude between X-D and X+D and Longitude between Y-D and Y+D
The above query is not completely accurate, as we know that to find the distance between two points
we have to use the distance formula (Pythagorean theorem), but for simplicity let’s take this.
How efficient would this query be?  We have estimated 500M places to be stored in our service.
Since we have two separate indexes, each index can return a huge list of places and performing an
intersection on those two lists won’t be efficient. Another way to look at this problem is that there
could be too many locations between ‘X-D’ and ‘X+D’, and similarly between ‘Y-D’ and ‘Y+D’. If we can
somehow shorten these lists, it can improve the performance of our query.
b. Grids
We can divide the whole map into smaller grids to group locations into smaller sets. Each grid will
store all the Places residing within a specific range of longitude and latitude. This scheme would enable
us to query only a few grids to find nearby places. Based on a given location and radius, we can find all
the neighboring grids and then query these grids to find nearby places.

## Examples & Scenarios

- 6. Category (1 byte): E.g., coffee shop, restaurant, theater, etc.
Although a four bytes number can uniquely identify 500M locations, with future growth in mind, we
will go with 8 bytes for LocationID.
Total size: 8 + 256 + 8 + 8 + 512 + 1 => 793 bytes
We also need to store reviews, photos, and ratings of a Place. We can have a separate table to store
reviews for Places:
1. LocationID (8 bytes)
2. ReviewID (4 bytes): Uniquely identifies a review, assuming any location will not have more than
2^32 reviews.
3. ReviewText (512 bytes)

- category_filter (string): Optional category to filter search results, e.g., Restaurants, Shopping Centers,
etc.
sort (number): Optional sort mode: Best matched (0 - default), Minimum distance (1), Highest rated
(2).
page_token (string): This token will specify a page in the result set that should be returned.
Returns: (JSON)
A JSON containing information about a list of businesses matching the search query. Each result entry
will have the business name, address, category, rating, and thumbnail.
6. Basic System Design and Algorithm
At a high level, we need to store and index each dataset described above (places, reviews, etc.). For

- frequently, e.g., people or taxis, then we might come up with a very different design.
Let’s see what are different ways to store this data and also find out which method will suit best for our
use cases:
a. SQL solution
One simple solution could be to store all the data in a database like MySQL. Each place will be stored
in a separate row, uniquely identified by LocationID. Each place will have its longitude and latitude
stored separately in two different columns, and to perform a fast search; we should have indexes on
both these fields.
To find all the nearby places of a given location (X, Y) within a radius ‘D’, we can query like this:
Select * from Places where Latitude between X-D and X+D and Longitude between Y-D and Y+D

