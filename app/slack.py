import html
import json

import requests
import randomcolor

from app import settings


def summarize_in_thread(message, summary):
    message_ts = message["container"]["message_ts"]
    # message_ts = message["actions"][0]["action_ts"]
    # response_url = message["response_url"]

    print(message_ts)

    payload = {
        "text": summary,
        "thread_ts": message_ts
    }

    webhook_url = settings.SLACK_HOOK_URL
    response = requests.post(webhook_url, data=json.dumps(payload))
    print(response.text)
    return response


def notify_slack(source, author_name, title, title_link, thumb_url,  **kwargs):
    """
    Builds a slack message with attachments.
    """
    footer = "lunatech-news"
    icon = "https://platform.slack-edge.com/img/default_application_icon.png"
    color = get_random_color(source)

    title = html.unescape(title)
    if len(title) > 150:
        title = title[:150] + "...."

    # slack's named urls
    # <fakeLink.toHotelPage.com|Windsor Court Hotel>
    text = "*<{}|{}>* - `{}`".format(title_link, title, author_name)
    payload = {
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        ],
        "attachments": [
            {
                "color": color,
                "fields": [],
                "thumb_url": thumb_url,
                "footer": footer,
                "footer_icon": icon
            }
        ]
    }

    attach_fields(source, payload, **kwargs)
    image_attached = attach_main_image(payload, title_link, title)
    if source == "reddit" and not image_attached:
        attach_summarize_button(payload, title_link)

    print(json.dumps(payload, indent=4))
    webhook_url = settings.SLACK_HOOK_URL
    response = requests.post(webhook_url, data=json.dumps(payload))
    print(response.text)
    return response


def attach_main_image(payload, title_link, title):
    image_extensions = (".png", ".jpg", ".jpeg", ".gif")
    if title_link.lower().endswith(image_extensions):
        image_block = {
            "type": "image",
            "image_url": title_link,
            "alt_text": title,
            "title": {
                "type": "plain_text",
                "text": title
            }
        }
        payload["blocks"].pop(1)
        payload["blocks"].insert(1, image_block)
        # payload["attachments"][0]["image_url"] = title_link
        return True

    return False


def attach_summarize_button(payload, title_link):
    accessory = {
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": "Summarize Content"
        },
        "value": title_link
    }
    payload["blocks"][1]["accessory"] = accessory
    return True


def attach_fields(source, payload, **kwargs):
    if source == "reddit":
        values = {
            "Subreddit": kwargs.get("subreddit"),
            "Upvotes": kwargs.get("ups"),
            "Comments #": kwargs.get("comments_count"),
            "Comments": kwargs.get("comments_url")
        }

        fields = []
        for field in ["Subreddit", "Upvotes", "Comments #", "Comments"]:
            fields.append({
                "title": field,
                "value": values[field],
                "short": True
            })

    if source == "stackexchange":
        values = {
            "Site": kwargs.get("site_name"),
            "Upvotes": kwargs.get("ups"),
            "Tags": kwargs.get("tags")
        }
        fields = []
        for field in ["Site", "Upvotes", "Tags"]:
            short = True
            if field == "Tags":
                short = False

            fields.append({
                "title": field,
                "value": values[field],
                "short": short
            })

    payload["attachments"][0]["fields"] += fields
    return True


def get_random_color(source):
    """
    return a random color based on a base color.
    reddit links will use greenish colors, whereas
    stackexchange links will use blueish colors.
    """
    hue = "blue"
    if source == "reddit":
        hue = "green"

    color_generator = randomcolor.RandomColor()
    color = color_generator.generate(hue=hue)[0]
    return color
