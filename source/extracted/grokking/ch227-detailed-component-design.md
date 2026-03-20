# 8. Detailed Component Design

> Source: System Design - Grokking (Notes), Chapter 227, Pages 62-62

## Key Concepts

- "Type": "Regular"
          "Price": 14.99
          "Status: "Full"
      },
        {  
          "Type": "Premium"
        "Price": 24.99
        "Status: "Almost Full"
      }
    ]
  },
 ]
Reserv

## Content

"Type": "Regular"
          "Price": 14.99
          "Status: "Full"
      },
        {  
          "Type": "Premium"
        "Price": 24.99
        "Status: "Almost Full"
      }
    ]
  },
 ]
ReserveSeats(api_dev_key, session_id, movie_id, show_id, seats_to_reserve[])
Parameters:
api_dev_key (string): same as above
session_id (string): User’s session ID to track this reservation. Once the reservation time expires,
user’s reservation on the server will be removed using this ID.
movie_id (string): Movie to reserve.
show_id (string): Show to reserve.
seats_to_reserve (number): An array containing seat IDs to reserve.
Returns: (JSON)
Returns the status of the reservation, which would be one of the following: 1) “Reservation Successful”
2) “Reservation Failed - Show Full,” 3) “Reservation Failed - Retry, as other users are holding reserved
seats”.
6. Database Design
Here are a few observations about the data we are going to store:
1. Each City can have multiple Cinemas.
2. Each Cinema will have multiple halls.
3. Each Movie will have many Shows and each Show will have multiple Bookings.
4. A user can have multiple bookings.
Movie
MovieID: int
PK
Title: varchar(256)
Description: varchar(512)
Duration: datetime
Language: varchar(16)
ReleaseDate: datetime
Country: varchar(64)
Genre: varchar(20)
Show
ShowID: int
PK
Date: datetime
StartTime: datetime
EndTime: datetime
CinemaHallID: int
FK
MovieID: int
FK
Cinema
CinemaID: int
PK
Name: varchar(64)
User
UserID: int
PK
Name: varchar(64)
Password: varchar(20)
Email: varchar(64)
Phone: varchar(16)
Booking
BookingID: int
PK
NumberOfSeats: int
Timestamp: datetime
Status: int (enum)
UserID: int
FK
ShowID: int
FK
Show_Seat
ShowSeatID: int
PK
Status: int (enum)
Cinema_Hall
CinemaHallID: int
PK
Name: varchar(64)
Payment
PaymentID: int
PK
Amount: number
City
CityID: int
PK
Name: varchar(64)
State: varchar(64)
ZipCode: varchar(16)
(
)
TotalCinemaHalls: int
CityID: int
FK
Status: int (enum)
Price: number
CinemaSeatID: int
FK
ShowID: int
FK
BookingID: int
FK
Cinema_Seat
CinemaSeatID: int
PK
SeatNumber: int
Type: int (enum)
CinemaHallID: int
FK
(
)
TotalSeats: int
CinemaID: int
FK
Timestamp: datetime
DiscountCouponID: int
RemoteTransactionID: int
PaymentMethod: int (enum)
BookingID: int
FK
7. High Level Design
At a high-level, our web servers will manage users’ sessions and application servers will handle all the
ticket management, storing data in the databases as well as working with the cache servers to process
reservations.
Clients
Web
Servers
Load
Balancers
Application Servers to handle 
Ticket Management
Cache Servers
Databases
8. Detailed Component Design
First, let’s try to build our service assuming it is being served from a single server.
Ticket Booking Workflow: The following would be a typical ticket booking workflow:
1. The user searches for a movie.
2. The user selects a movie.
3. The user is shown the available shows of the movie.
4. The user selects a show.
5. The user selects the number of seats to be reserved.
6. If the required number of seats are available, the user is shown a map of the theater to select
seats. If not, the user is taken to ‘step 8’ below.
7. Once the user selects the seat, the system will try to reserve those selected seats.
8. If seats can’t be reserved, we have the following options:
Show is full; the user is shown the error message.
The seats the user wants to reserve are no longer available, but there are other seats available, so
the user is taken back to the theater map to choose different seats.

## Tables & Comparisons

|  |  |
| --- | --- |
|  |  |
|  | ( ) |
| FK | TotalCinemaHalls: int
CityID: int |
|  |  |
| City |  |
| PK | CityID: int |
|  | Name: varchar(64)
State: varchar(64)
ZipCode: varchar(16) |

|  |  |
| --- | --- |
|  |  |
|  | ( ) |
| FK | TotalSeats: int
CinemaID: int |

|  |  |
| --- | --- |
|  |  |
|  |  |
| FK
FK
FK | Status: int (enum)
Price: number
CinemaSeatID: int
ShowID: int
BookingID: int |

|  |  |
| --- | --- |
|  |  |
|  |  |
| FK | Timestamp: datetime
DiscountCouponID: int
RemoteTransactionID: int
PaymentMethod: int (enum)
BookingID: int |

| Cinema_Seat |  |
| --- | --- |
| PK | CinemaSeatID: int |
| FK | SeatNumber: int
Type: int (enum)
CinemaHallID: int |

| Movie |  |  | Show |  |  | Booking |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PK | MovieID: int |  | PK | ShowID: int |  | PK | BookingID: int |
|  | Title: varchar(256)
Description: varchar(512)
Duration: datetime
Language: varchar(16)
ReleaseDate: datetime
Country: varchar(64)
Genre: varchar(20) |  | FK
FK | Date: datetime
StartTime: datetime
EndTime: datetime
CinemaHallID: int
MovieID: int |  | FK
FK | NumberOfSeats: int
Timestamp: datetime
Status: int (enum)
UserID: int
ShowID: int |

| User |  |
| --- | --- |
| PK | UserID: int |
|  | Name: varchar(64)
Password: varchar(20)
Email: varchar(64)
Phone: varchar(16) |

| Cinema |  |
| --- | --- |
| PK | CinemaID: int |
|  | Name: varchar(64) |
|  |  |
|  |  |
|  |  |

| Cinema_Hall |  |
| --- | --- |
| PK | CinemaHallID: int |
|  | Name: varchar(64) |
|  |  |

| Show_Seat |  |
| --- | --- |
| PK | ShowSeatID: int |
|  |  |
|  | Status: int (enum) |

| Payment |  |
| --- | --- |
| PK | PaymentID: int |
|  | Amount: number |
|  |  |

