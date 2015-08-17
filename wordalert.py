# WordAlert:1.1 (by /u/twistitup)
# Made with Python 3.4.0

import praw, oaux, time, collections, requests, traceback

### User configuration ###

TARGET_STRING = "" # what you want to search for
RECIPIENT = "" # without /u/
SUBJECT = TARGET_STRING + " has been spotted!"
MESSAGE = TARGET_STRING + " has been spotted! Here is the url "
SLEEP_TIME = 300

### End of user configuration ###

def searchAndReply():
    for submission in r.get_new(limit = None):
        if (str.lower(TARGET_STRING) in str.lower(submission.selftext)
                and submission.id not in submissionsDone):
            r.send_message(RECIPIENT, SUBJECT, MESSAGE + submission.url)
            print("Alert sent!")
            submissionsDone.append(submission.id)
    comments = r.get_comments('all', limit = None)
    for comment in comments:
        if (str.lower(TARGET_STRING) in str.lower(comment.body)
                and comment.id not in commentsDone
                and comment.submission.id not in submissionsDone):
            r.send_message(RECIPIENT, SUBJECT, MESSAGE + comment.permalink)
            print("Alert sent!")
            commentsDone.append(comment.id)

if __name__ == "__main__":
    r = oaux.login()
    submissionsDone = collections.deque(maxlen = 100)
    commentsDone = collections.deque(maxlen = 100)
    while True:
        try:
            searchAndReply()
            time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            print("Shutting down.")
            break
        except Exception as e:
            print("Something bad happened!", e)
            traceback.print_exc()
            print("Sleeping", SLEEP_TIME, "seconds.")
            time.sleep(SLEEP_TIME)
