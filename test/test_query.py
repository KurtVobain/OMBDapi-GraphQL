def test_create_user(client):
    query = """
        {
          getFilms(
          Title: "mirror",
          Type: "series",
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
    """
    result = client.execute(query)
    assert len(result['data']['getFilms']['edges']) == 5

