import json
from datetime import datetime

from stackapi import StackAPI

from app import settings
from app.slack import notify_slack


def parse_and_post(site_name, period="month", count=1):
    key = settings.STACK_EXCHANGE_KEY
    site = StackAPI(site_name, key=key, max_pages=1, page_size=count)
    data = site.fetch("questions", sort=period)

    for order in range(count):
        top = data["items"][order]
        owner_name = top["owner"]["display_name"]
        title = top["title"]
        url = top["link"]
        ups = top["score"]
        tags = ", ".join(top["tags"])
        thumb_url = top["owner"]["profile_image"]

        notify_slack(
            source="stackexchange", author_name=owner_name, title=title,
            title_link=url, thumb_url=thumb_url, ups=ups,
            site_name=site_name, tags=tags
        )


def schedule():
    day = datetime.today().day
    if day == 1:
        parse_and_post("stackoverflow", period="month", count=3)
    elif day == 6:
        parse_and_post("superuser", period="month", count=3)
    elif day == 12:
        parse_and_post("serverfault", period="month", count=3)
    elif day == 18:
        parse_and_post("unix", period="month", count=3)
    elif day == 24:
        parse_and_post("softwareengineering", period="month", count=3)


def main(event, context):
    schedule()

    info = {
        "status_code": 200,
        "message": "notifications have been sent to slack"
    }
    return json.dumps(info)


if __name__ == '__main__':
    event = {}
    context = {}
    # parse_and_post("serverfault", period="month", count=3)
    # parse_and_post("superuser", period="month", count=1)
    # parse_and_post("unix", period="month", count=1)
    # parse_and_post("softwareengineering", period="month", count=1)

    main(event, context)
