import requests


def insertSubscribe(conferenceId: int, authorization: str):
    query = """
        mutation insertSubscribe($conferenceId: Int!) {
            insert_slideshare_ConferenceSubscriber_one(object: {conferenceId: $conferenceId}) {
                id
            }
        }
    """
    variables = {"conferenceId": conferenceId}
    headers = {"Authorization": authorization}
    url = "https://adequate-guinea-56.hasura.app/v1/graphql"
    r = requests.post(
        url, json={"query": query, "variables": variables}, headers=headers
    )

    if "errors" in r.json():
        raise Exception(r.json()["errors"])

    return r.text
