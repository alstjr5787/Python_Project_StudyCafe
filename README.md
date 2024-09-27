# Python_Project_User_Admin

This is a Python GUI-based attendance system that allows users to select and use seats in a study café with features such as signup, login, seat reservation, and checkout.

In this project, I developed this application to enable users to utilize the study café autonomously. Users can register and log into the system, and they can reserve or release seats through an intuitive GUI built with PyQt. This application communicates with a backend server to handle user data and seat status.

### TECHNOLOGY USED:

1. **PyQt** - Used for the entire graphical user interface.
2. **Requests** - Used for handling HTTP requests to the server for user signup, login, and seat management.
3. **JSON** -Utilized for data exchange between the application and the server.


FEATURES:

The feature of this study café program is that there are no fixed seats. When a seat is reserved, the usage time automatically ends after 2 hours. This method was chosen to prevent one person from consistently using a specific seat for an extended period. If a user wants to continue using a seat, they must rebook it after the time has expired. Additionally, the program can receive real-time data from the server to check which seats are available and when the scheduled end times are.

# SCREENSHOTS
![image](https://github.com/user-attachments/assets/e02826df-62ce-46f6-a27e-7a419fbfcabc)

### Table: `cafe_seat`

```sql
CREATE TABLE `cafe_seat` (
  `id` int NOT NULL,
  `start_time` datetime NOT NULL,
  `status` enum('true','false') NOT NULL,
  `scheduled_end_time` datetime DEFAULT NULL,
  `user_id` varchar(50) DEFAULT NULL
);
```
### Table: `cafe_user`

```sql
CREATE TABLE `cafe_user` (
  `id` int NOT NULL,
  `member_id` varchar(255) NOT NULL,
  `member_password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `account_status` varchar(20) DEFAULT 'active',
  `suspension_end_date` datetime DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

