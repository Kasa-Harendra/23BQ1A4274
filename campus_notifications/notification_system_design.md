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

