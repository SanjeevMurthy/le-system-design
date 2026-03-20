# 5. System APIs

> Source: System Design - Grokking (Notes), Chapter 224, Pages 61-61

## Key Concepts

- 3. Some Design Considerations
1. For simplicity, let’s assume our service does not require any user authentication.
2. The system will not handle partial ticket orders. Either user gets all the ticket

## Content

3. Some Design Considerations
1. For simplicity, let’s assume our service does not require any user authentication.
2. The system will not handle partial ticket orders. Either user gets all the tickets they want or they
get nothing.
3. Fairness is mandatory for the system.
4. To stop system abuse, we can restrict users from booking more than ten seats at a time.
5. We can assume that traffic would spike on popular/much-awaited movie releases and the seats
would fill up pretty fast. The system should be scalable and highly available to keep up with the
surge in traffic.
4. Capacity Estimation
Traffic estimates: Let’s assume that our service has 3 billion page views per month and sells 10
million tickets a month.
Storage estimates: Let’s assume that we have 500 cities and, on average each city has ten cinemas.
If there are 2000 seats in each cinema and on average, there are two shows every day.
Let’s assume each seat booking needs 50 bytes (IDs, NumberOfSeats, ShowID, MovieID,
SeatNumbers, SeatStatus, Timestamp, etc.) to store in the database. We would also need to store
information about movies and cinemas; let’s assume it’ll take 50 bytes. So, to store all the data about
all shows of all cinemas of all cities for a day:
500 cities * 10 cinemas * 2000 seats * 2 shows * (50+50) bytes = 2GB / day
To store five years of this data, we would need around 3.6TB.
5. System APIs
We can have SOAP or REST APIs to expose the functionality of our service. The following could be the
definition of the APIs to search movie shows and reserve seats.
SearchMovies(api_dev_key, keyword, city, lat_long, radius, start_datetime, end_dat
etime, postal_code, 
includeSpellcheck, results_per_page, sorting_order)
Parameters:
api_dev_key (string): The API developer key of a registered account. This will be used to, among
other things, throttle users based on their allocated quota.
keyword (string): Keyword to search on.
city (string): City to filter movies by.
lat_long (string): Latitude and longitude to filter by. radius (number): Radius of the area in
which we want to search for events.
start_datetime (string): Filter movies with a starting datetime.
end_datetime (string): Filter movies with an ending datetime.
postal code (string): Filter movies by postal code / zipcode.
p
_
(
g)
y p
/
p
includeSpellcheck (Enum: “yes” or “no”): Yes, to include spell check suggestions in the
response.
results_per_page (number): Number of results to return per page. Maximum is 30.
sorting_order (string): Sorting order of the search result. Some allowable values : ‘name,asc’,
‘name,desc’, ‘date,asc’, ‘date,desc’, ‘distance,asc’, ‘name,date,asc’, ‘name,date,desc’, ‘date,name,asc’,
‘date,name,desc’.
Returns: (JSON)
Here is a sample list of movies and their shows:
[
  {
    "MovieID": 1,
    "ShowID": 1,
    "Title": "Cars 2",
    "Description": "About cars",
    "Duration": 120,
    "Genre": "Animation",
    "Language": "English",
    "ReleaseDate": "8th Oct. 2014",
    "Country": USA,
    "StartTime": "14:00",
    "EndTime": "16:00",
    "Seats": 
    [
      {  
        "Type": "Regular"
        "Price": 14.99
        "Status: "Almost Full"
      },
      {  
        "Type": "Premium"
        "Price": 24.99
        "Status: "Available"
      }
    ]
  },
  {
    "MovieID": 1,
    "ShowID": 2,
    "Title": "Cars 2",
    "Description": "About cars",
    "Duration": 120,
    "Genre": "Animation",
    "Language": "English",
    "ReleaseDate": "8th Oct. 2014",
    "Country": USA,
    "StartTime": "16:30",
    "EndTime": "18:30",
    "Seats": 
    [
        {  
"T
"
"R
l
"

