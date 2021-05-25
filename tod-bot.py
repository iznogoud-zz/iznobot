from io import TextIOWrapper
import praw
import csv

# import random
import time

# random.seed()

DAY_IN_SECONDS = 24 * 60 * 60


def get_topics(topics_file):
    with open(topics_file, "r", newline="") as csvfile:
        csv_data = csv.DictReader(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

        field_names = csv_data.fieldnames
        topics = [r for r in csv_data]

        return field_names, topics


def update_topics(topics_file, field_names, topics):
    with open(topics_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for r in topics:
            writer.writerow(r)


def submit_new_tod(bot, subreddit, topic_title, topic_description, topic_flair):
    print(f"SR: {subreddit} => {topic_title} :: {topic_description}")
    s = bot.subreddit(subreddit).submit(topic_title, topic_description)
    for f in s.flair.choices():
        if f["flair_text"] == topic_flair:
            s.flair.select(f["flair_template_id"])


def main():
    pt = praw.Reddit("botpt")
    pt.validate_on_submit = True
    tp_file_name = pt.config.custom["topics_file"]
    subreddit = pt.config.custom["subreddit"]
    topic_flair = pt.config.custom["topic_flair"]
    topic_id = 0
    field_names, topics = get_topics(tp_file_name)

    while True:
        submit_new_tod(pt, subreddit, topics[topic_id]["Topic"], topics[topic_id]["Description"], topic_flair)
        topic_id = 0 if topic_id + 1 > len(topics) else topic_id + 1
        time.sleep(DAY_IN_SECONDS)


if __name__ == "__main__":
    main()
