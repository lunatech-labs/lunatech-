import json
from datetime import date

import requests

from app.slack import notify_slack


def fetch_top_links(subreddit, period="day"):
    """
    Retrieves the json object from reddit, for given period and subreddit.

    `subreddit`: Subreddit to parse. Provide with the format 'r/programming'
    `period`: Period to parse. (top daily, weekly etc.) Possible options are;
         'day', 'week', 'month', 'year', 'all'
    """

    base = "https://www.reddit.com"
    content_format = ".json"
    category = "top"
    user_agent = "lunatech-slack-news:v0.1 (by /u/jeffisabelle)"
    headers = {"User-Agent": user_agent}

    # Generate url to fetch json, eg.;
    # https://www.reddit.com/r/programming/top.json?t=day.json
    url = '{}/{}/{}{}?t={}'.format(
        base, subreddit, category, content_format, period)
    r = requests.get(url, headers=headers)
    return r.json()


def parse_and_post(subreddit, period="day", count=1):
    """
    Just parses the fetched json document, and calls the slack notifier.
    """
    data = fetch_top_links(subreddit, period)["data"]

    # if the count is 3, get top 3 link from reddit
    for order in range(count):

        top = data["children"][order]["data"]  # highest voted link data
        domain = top["domain"]
        subreddit = top["subreddit_name_prefixed"]
        title = top["title"]
        url = top["url"]
        ups = top["ups"]
        thumbnail = top["thumbnail"]
        if not thumbnail:
            thumbnail = "https://i.imgur.com/StGee5q.png"

        post_id = top["id"]
        comments_url = 'https://redd.it/{}'.format(post_id)
        comments_count = top["num_comments"]

        notify_slack(
            source="reddit", author_name=domain, title=title, title_link=url,
            thumb_url=thumbnail, subreddit=subreddit, ups=ups,
            comments_url=comments_url, comments_count=comments_count
        )

    return True


def schedule():
    weekday = date.today().weekday()
    weekdays = {
        0: "monday",
        1: "tuesday",
        2: "wednesday",
        3: "thursday",
        4: "friday",
        5: "saturday",
        6: "sunday"
    }

    day = weekdays[weekday]

    # schedule r/programming for everyday
    parse_and_post("r/programming", "day")

    if day == "monday":
        parse_and_post("r/scala", "week")
    elif day == "tuesday":
        parse_and_post("r/linux", "week")
    elif day == "wednesday":
        parse_and_post("r/devops", "week")
    elif day == "thursday":
        parse_and_post("r/netsec", "week")
    elif day == "friday":
        parse_and_post("r/programmerhumor", "week", 3)
    elif day == "saturday":
        parse_and_post("r/dataisbeautiful", "week", 3)


def main(event, context):
    schedule()
    info = {
        "status_code": 200,
        "message": "notifications have been sent to slack"
    }
    return json.dumps(info)
