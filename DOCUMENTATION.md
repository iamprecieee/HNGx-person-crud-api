# Person CRUD REST API Documentation

This documentation provides details on how to use the Person CRUD REST API. The API allows you to manage person records with basic CRUD (Create, Read, Update, Delete) operations.

For instructions for setting up and deploying the API locally, please refer to the [README.md](https://github.com/iamprecieee/person-crud-api/blob/main/README.md) file.

## Standard Formats for Requests and Responses

### Person Model

- `id` (integer): Unique identifier for a person.
- `name` (string): Name of the person (unique).


### Endpoint: List Persons

- **URL**: `/api`
- **Method**: `GET`
- **Request**:

    ```
  curl -X GET http://localhost:5000/api
    ```

- **Response (200 OK)**:

  ```
  [
    {
      "id": 1,
      "name": "John Doe"
    },
    {
      "id": 2,
      "name": "Jane Smith"
    }
  ]


### Endpoint: Create a Person

- **URL**: `/api`
- **Method**: `POST`
- **Request**:

```
curl -X POST -H "Content-Type: application/json" -d '{"name": "New Person"}' http://localhost:5000/api```

```
    {
      "name": "New Person"
    }

- **Response (200 OK)**:

  ```
  {
    "name": "John Doe"
  }

 "Person created successfully."


### Endpoint: Retrieve a Person by ID

- **URL**: `/api/<user_id>`
- **Method**: `GET`
- **Request**:

```
curl -X GET http://localhost:5000/api/1
```

- **Response (200 OK)**:

  ```
  {
      "id": 1,
      "name": "John Doe"
  }


### Endpoint: Update a Person by ID

- **URL**: `/api/<user_id>`
- **Method**: `PUT`
- **Request**:

```
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Updated Name"}' http://localhost:5000/api/1
```

- **Response (200 OK)**:

  ```
  {
      "id": 1,
      "name": "Updated Name"
  }


### Endpoint: Delete a Person by ID

- **URL**: `/api/<user_id>`
- **Method**: `DELETE`
- **Request**:

```
curl -X DELETE http://localhost:5000/api/1
```

- **Response (200 OK)**:
  
  ```"Person deleted successfully."```



## Limitations

Error responses include standard HTTP status codes and descriptive error messages for common scenarios, but more detailed error handling can be added as needed.
