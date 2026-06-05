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

  **Request Response**
  ```
  {
      "Id": "6dcsa39-37tejj2-23t7cb",
      "Type": "Farewell",
      "Message": "Welcome All",
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

# Stage 3
