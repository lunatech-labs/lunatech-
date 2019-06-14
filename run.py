from app import reddit, stackexchange
# from app import summarize
# from events import summary_event


if __name__ == '__main__':
    test = "reddit"
    # test = "stackexchange"
    # test = "summary"

    if test == "reddit":
        # reddit.parse_and_post("r/programmerhumor", "week", 3)
        # reddit.parse_and_post("r/dataisbeautiful", "week", 3)
        # reddit.parse_and_post("r/programming", "year", 3)
        reddit.schedule()

    if test == "stackexchange":
        stackexchange.parse_and_post("serverfault", period="month", count=3)
        # stackexchange.parse_and_post("superuser", period="month", count=1)
        # stackexchange.parse_and_post("unix", period="month", count=1)
        # stackexchange.parse_and_post("softwareengineering", period="month", count=1)

    if test == "summary":
        context = {}
        # summarize.main(event=summary_event, context=context)
