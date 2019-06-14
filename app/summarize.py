import json
import urllib

import requests

from app.slack import summarize_in_thread
from app import settings


def summarize(message):
    """
    Get link from the slack message, summarize it using summry.
    """

    # requester_id = message["user"]["id"]
    # requester = "<@{}>".format(requester_id)
    requester = message["user"]["username"]

    url = message["actions"][0]["value"]

    # make summry call
    params = {
        "SM_API_KEY": settings.SUMMRY_API_KEY,
        "SM_URL": url
    }
    res = requests.get("https://api.smmry.com", params=params)
    data = res.json()

    # sm_char_count = data.get("sm_api_character_count")
    sm_reduced_perc = data.get("sm_api_content_reduced")
    sm_title = data.get("sm_api_title")
    sm_content = data.get("sm_api_content")

    if not sm_reduced_perc or not sm_content:
        text = """Sorry, {}, I've failed to get a good enough summary of this article. It's best if you visit the page directly.\n {}""".format(requester, url)
        return text

    text = "Hello {} :wave:, \n I've tried to summarize this for you. I believe I've reduced the original content by {}. Here you go!".format(requester, sm_reduced_perc)
    if sm_title and sm_content:
        text += "\n\n *{}* \n\n {}".format(sm_title, sm_content)
        return text

    if sm_content:
        text += "\n\n {}".format(sm_content)
        return text


def main(event, context):
    print("=========== printing event ===========")
    print(event)

    print("======== printing parsed body ========")
    message = event["body"]
    message = message.replace("payload=", "")
    message = json.loads(urllib.parse.unquote(message))
    print(json.dumps(message, indent=4))

    summary = summarize(message)
    summarize_in_thread(message, summary)

    body = {
        "message": "Hello, world"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
