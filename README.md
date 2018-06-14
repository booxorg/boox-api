# Boox API

The API returns `JSON` objects as a response with the following format:
```
{
    'status' : 'error' | 'success',
    'message' ; 'The human readable message',
    'response' : <method dependent value, contains the main data>
}
```

### `/genres`
Returns all the available and allowed Genres for adding books
| Parameter name | Description | Type |
|----------------|-------------|------|
| None | None | None |

| Return value  | Description | Type |
|---------------|-------------|------|
| genres | Contains a list of strings naming all the allowed Genres | List of strings |

### `/book`
Returns all the information about a book given its id
| Parameter name | Description | Type |
|----------------|-------------|------|
| token | User identification token | String |
| id | Book id to search | Integer |

| Return value  | Description | Type |
|----------------|-------------|------|
| user_id | ID of the book's owner | Integer |
| username | Username of the book's owner | String |
| title | Book's title | String |
| goodreads_id | Id of the book as stated by Goodreads API | Integer |
| id | Id of the book in BooX database | Integer |
| isbn | Book's ISBN | String |
| genre | Book's genre | String |
| expires | Expiration date of the offer | Date |
| author | Book's author |

### `/book/search`
Returns all the information about a book given its full or partial title. Will Fetch Goodreads API
| Parameter name | Description | Type |
|----------------|-------------|------|
| token | User identification token | String |
| query | Book search query | String |

| Return value  | Description | Type |
|----------------|-------------|------|
| goodreads_id | Id of the book as stated by Goodreads API | Integer |
| title | Book's title | String |
| isbn | Book's ISBN | String |
| image_url | Big image URL of the book cover | String |
| small_image_url | Small image URL of the book cover | String |
| author | Book's author | String |
| publication_date | `dd-mm-yyyy` publication date format | Date |

### `/book/create`
Adds a new book to the offers database, using its goodreads_id, genre and expires
| Parameter name | Description | Type |
|----------------|-------------|------|
| token | User identification token | String |
| expires | Expiration date of the offer `dd-mm-yyyy` format | Date |
| genre | Book's genre | String |
| goodreads_id | Id of the book as stated by Goodreads API | Integer |

| Return value  | Description | Type |
|----------------|-------------|------|
| goodreads_id | Id of the book as stated by Goodreads API | Integer |
| book_id | Id of the newly added book | Integer |
| user_id | Owner id | Integer |
| author_id | Author id | Integer |

### `/search`
Searches books in the database, using multiple filters as `authors`, `genres`,`location`
| Parameter name | Description | Type |
|----------------|-------------|------|
| token | User identification token | String |
| keywords | Keywords separated by commas for searching | String |
| authors | Author names separated by commas | String |
| genres | Genre names separated by commas | String |
| before | The expire date should come `before` this one, to get a match | Date |
| after | The expire date should comd `after` this one, to get a match | Date |

| Return value  | Description | Type |
|----------------|-------------|------|
| user_id | ID of the book's owner | Integer |
| username | Username of the book's owner | String |
| title | Book's title | String |
| goodreads_id | Id of the book as stated by Goodreads API | Integer |
| id | Id of the book in BooX database | Integer |
| isbn | Book's ISBN | String |
| genre | Book's genre | String |
| expires | Expiration date of the offer | Date |
| author | Book's author |
