# OMDB GraphQL

Application for wrapping  API OMBD with GranpGL according to Relay specification.

More info about OMBDapi [here](https://www.omdbapi.com/).

The application is deployed on Google Cloud.
You can look at it [here](https://seedtrace-zau7cpuw7q-uc.a.run.app/).

# Table of content
* [Setup](#setup)
    * [Build image](#run-container)
    * [Run container](#run-container)
* [Usage Example](#usage-example)
    * [How to make request](#make-first-request) 
    * [Available parameters](#available-parameters)
* [Technologies](#technologies)


# Setup
### Build image

Execute at the root directory:

```
docker build -t seedtrace-image -f Dockerfile .
```

### Run container
Replace ```<INSERT TOKEN HERE>``` by your OMDB apikey and execute:

```
docker run --rm --name seedtrace-container -e OMDB_API_TOKEN=<INSERT TOKEN HERE> -p 80:80 -it seedtrace-image
```

# Usage Example

### Make first request

Follow the link -  http://127.0.0.1/

On the left side of the screen, enter the sample request below

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

Available fields for each node:
 * Title
 * Year
 * imdbID
 * Type
 * Poster

### Available parameters
#### getFilms

| Parameter |  Required  |         	Valid options |                 Description|
|-----------|:----------:|-----------------------:|----------------------------:|
| Title     |    Yes     |                        |   Movie title to search for | 
| Type      |  Optional  | movie, series, episode |    Type of result to return |
| Year      | Optional   |                        |            	Year of release |

# Technologies
* [FastAPI](https://fastapi.tiangolo.com/)
* [Graphene](https://graphene-python.org/)
* [GraphQL](https://graphql.org/)
* [uvicorn](https://www.uvicorn.org/)
* [Docker](https://www.docker.com/)
* [Google Cloud](https://cloud.google.com/)
