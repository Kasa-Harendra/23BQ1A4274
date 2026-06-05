# Stage 1
- **End point for fetching notifications after login** 
  ```GET /api/v1/notifcations```
  --
  **Request Header** 
  ```Authorization: Bearer <token>```

  **Query Params**:
  - ``limit (int)`` : Max no of notifications to be fetched. [Max: 50] 

  **Request Response**
  ```
  [
    {
      "Id": "6dcsa39-37tcubj2-23t7cb",
      "Type": "Mid-Sem",
      "Message": "Results out",
      "is_viewed": true
    },
    {
      "Id": "6dcsa39-37tejj2-23t7cb",
      "Type": "Farewell",
      "Message": "Welcome All",
      "is_viewed": false
    }
  ]
  ```
  
  **End point for marking notification as viewed** 
  ```POST /api/v1/notifcations/{notification_id}/viewed```
  --
  **Request Header** 
  ```Authorization: Bearer <token>```

  **Response**
  ```
  {
      "id": "a2138sa-783bj4-42h3jb",
      "notification_id": "6dcsa39-37tejj2-23t7cb",
      "student_id": "32678-qj3j13-21bnbj"
      "is_viewed": true
  }
  ```

# Stage 2
- The data passsed in this API can be stored in Relational Databases like PostgresSQL (or) MySQL
  This is because it allows to define consistent schema and enfore strict constraints on the data that is being saved.

- DB schema:
  **students**
  ```
  id: BigInt
  name: String(30)
  notifications
  ```

  **notifications**
  ```
  id: UUID
  type: String
  message: String
  created_at: Date
  ```

  **notification_student_table**:
  ```
  id: UUID
  student_id: ForeignKey(users.id)
  notification_id: ForeignKey(notifications.id)
  is_viewed: Boolean 
  ```

  ```relationship(users, backpopulates="notifications")```
  This is done to directly access the notifications of the users using student ID directly from the user record.
  This allows faster retreival of notifications

# Stage 3
- The query shown is accurate but it is extremely slow because the traversing 5000000 notifications while matching the student_ID
  and getting the records and then sorting them again is extremely time taking.

- I suggest backpopulating the students.notifications field in order to directly acess the notifications from the user ID itself potentially eliminating the time taken to traverse whole notifications table and fecting the records directly.
One other alternative is **indexing the student_Id** in the notifications table

- Yes **indexing the student ID** allows directly lokking up all the records belonging to the student. ut adding indexes for every column adds overhead during insertion, deletion, updation.

- Query to get all the placement notifications in the past 7 days.
  ``` MySQL
  SELECT * FROM notifications
  WHERE notificationType = "Placement" AND created_at >= DATE_SUM(NOW(), INTERVAL 7 DAY);
  ```
