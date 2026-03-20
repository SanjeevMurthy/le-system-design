# c. Dynamic size grids

> Source: System Design - Grokking (Notes), Chapter 201, Pages 55-55

## Key Concepts

- Let’s assume that GridID (a four bytes number) would uniquely identify grids in our system.
What could be a reasonable grid size? Grid size could be equal to the distance we would like to
query since 

## Content

Let’s assume that GridID (a four bytes number) would uniquely identify grids in our system.
What could be a reasonable grid size? Grid size could be equal to the distance we would like to
query since we also want to reduce the number of grids. If the grid size is equal to the distance we want
to query, then we only need to search within the grid which contains the given location and
neighboring eight grids. Since our grids would be statically defined (from the fixed grid size), we can
easily find the grid number of any location (lat, long) and its neighboring grids.
In the database, we can store the GridID with each location and have an index on it, too, for faster
searching. Now, our query will look like:
Select * from Places where Latitude between X-D and X+D and Longitude between Y-D and Y+D
and GridID in (GridID, GridID1, GridID2, ..., GridID8)
This will undoubtedly improve the runtime of our query.
Should we keep our index in memory?  Maintaining the index in memory will improve the
performance of our service. We can keep our index in a hash table where ‘key’ is the grid number and
‘value’ is the list of places contained in that grid.
How much memory will we need to store the index?  Let’s assume our search radius is 10 miles;
given that the total area of the earth is around 200 million square miles, we will have 20 million grids.
We would need a four bytes number to uniquely identify each grid and, since LocationID is 8 bytes, we
would need 4GB of memory (ignoring hash table overhead) to store the index.
(4 * 20M) + (8 * 500M) ~= 4 GB
This solution can still run slow for those grids that have a lot of places since our places are not
uniformly distributed among grids. We can have a thickly dense area with a lot of places, and on the
other hand, we can have areas which are sparsely populated.
This problem can be solved if we can dynamically adjust our grid size such that whenever we have a
grid with a lot of places we break it down to create smaller grids. A couple of challenges with this
approach could be: 1) how to map these grids to locations and 2) how to find all the neighboring grids
of a grid
of a grid.
c. Dynamic size grids
Let’s assume we don’t want to have more than 500 places in a grid so that we can have a faster
searching. So, whenever a grid reaches this limit, we break it down into four grids of equal size and
distribute places among them. This means thickly populated areas like downtown San Francisco will
have a lot of grids, and sparsely populated area like the Pacific Ocean will have large grids with places
only around the coastal lines.
What data-structure can hold this information? A tree in which each node has four children
can serve our purpose. Each node will represent a grid and will contain information about all the
places in that grid. If a node reaches our limit of 500 places, we will break it down to create four child
nodes under it and distribute places among them. In this way, all the leaf nodes will represent the grids
that cannot be further broken down. So leaf nodes will keep a list of places with them. This tree
structure in which each node can have four children is called a QuadTree
How will we build a QuadTree? We will start with one node that will represent the whole world in
one grid. Since it will have more than 500 locations, we will break it down into four nodes and
distribute locations among them. We will keep repeating this process with each child node until there
are no nodes left with more than 500 locations.
How will we find the grid for a given location?  We will start with the root node and search
downward to find our required node/grid. At each step, we will see if the current node we are visiting
has children. If it has, we will move to the child node that contains our desired location and repeat this
process. If the node does not have any children, then that is our desired node.
How will we find neighboring grids of a given grid?  Since only leaf nodes contain a list of
locations, we can connect all leaf nodes with a doubly linked list. This way we can iterate forward or
backward among the neighboring leaf nodes to find out our desired locations. Another approach for
finding adjacent grids would be through parent nodes. We can keep a pointer in each node to access its
parent, and since each parent node has pointers to all of its children, we can easily find siblings of a
node. We can keep expanding our search for neighboring grids by going up through the parent

