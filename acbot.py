import praw
from difflib import SequenceMatcher
from flask import Flask, render_template

app = Flask(__name__)


def check_submissions():
    pt = praw.Reddit("botac")
    pt.validate_on_submit = True
    sr_list = pt.config.custom["ac_sr"].split("|")
    fl_list = pt.config.custom["ac_tbc_flair_txt"].split("|")

    results = []

    for sr_name in sr_list:
        idx = 1
        submissions = []
        for s in pt.subreddit(sr_name).search(query=f"title:Streak", sort="new", time_filter="day", limit=None):
            submissions.append(s)
        for s in submissions:
            print(f"{sr_name} processing {idx}/{len(submissions)} {s.shortlink}")
            idx += 1
            s_text = s.selftext
            try:
                s_author = s.author.name
            except Exception as e:
                s_author = "deleted"

            for c in s.comments:
                c_text = c.body

                similarity = SequenceMatcher(None, s_text, c_text).ratio()

                try:
                    author = c.author.name
                except Exception as e:
                    author = "deleted"

                if similarity > 0.15:
                    action = "MARK_CORRECTED"
                elif similarity > 0.04:
                    action = "INVESTIGATE"
                else:
                    action = "IGNORE"

                results.append(
                    [
                        s.title,
                        s.shortlink,
                        s_author,
                        f"https://reddit.com{c.permalink}",
                        author,
                        f"{similarity * 100:.2f}",
                        action,
                        sr_name,
                    ]
                )

    return results


@app.route("/")
def acbot():
    return render_template("submissions.html", my_list=check_submissions())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
