Build image:

```docker build -t seedtrace-image -f Dockerfile .```

Run container:

```docker run --rm --name seedtrace-container  -p 80:80 -it seedtrace-image```

URL -  http://127.0.0.1/

Request example:
```
{
  getFilms(
  Title: "mirror",
   Type:"series",
    Year: 2021,
     first: 3
     )
  {
    totalCount
    pageInfo{
      hasNextPage
      startCursor
      endCursor
    }
    edges {
      cursor
      node{
        Title
        Type
        Year
      }
    }
  }
}
```