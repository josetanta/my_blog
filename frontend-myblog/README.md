# my-blog Project create with Flask

- Para este proyecto se hara con react para el frontend

## Estructura del API Rest

```json
{
  "user": {
    "data": {
      "address": "address",
      "email": "email",
      "image": "image",
      "slug": "slug",
      "status": true,
      "upload": "upload.jpg",
      "username": "username"
    },
    "paths": {
      "comments": "/api/v1/users/1/comments",
      "posts": "/api/v1/users/1/posts",
      "self": "/api/v1/users/1"
    },
    "urls": {
      "comments": "http://<url>/api/v1/users/1/comments",
      "posts": "http://<url>/api/v1/users/1/posts",
      "self": "http://<url>/api/v1/users/1"
    }
  }
}
```
