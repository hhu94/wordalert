# WordAlert:1.0 (by /u/twistitup)
# Made with Python 3.4.0

import praw, oaux, time, collections, random, requests, traceback

TARGET_WORD = "" # lowercase
RECIPIENT = "" # without /u/
SUBJECT = TARGET_WORD + " has been spotted!"
MESSAGE = TARGET_WORD + " has been spotted! Here is the url "
SLEEP_TIME = 300

def searchAndReply():
    for submission in r.get_new(limit = None):
        if (TARGET_WORD in str.lower(submission.selftext)
                and submission.id not in submissionsDone):
            r.send_message(RECIPIENT, SUBJECT, MESSAGE + submission.url)
            print("Alert sent!")
            submissionsDone.append(submission.id)
    comments = r.get_comments('all', limit = None)
    for comment in comments:
        if (TARGET_WORD in str.lower(comment.body)
                and comment.id not in commentsDone
                and comment.submission.id not in submissionsDone):
            r.send_message(RECIPIENT, SUBJECT, MESSAGE + comment.permalink)
            print("Alert sent!")
            commentsDone.append(comment.id)

if __name__ == "__main__":
    r = oaux.login()
    last_refresh_time = time.time()
    submissionsDone = collections.deque(maxlen = 100)
    commentsDone = collections.deque(maxlen = 100)
    while True:
        try:
            last_refresh_time = oaux.checkRefresh(r, last_refresh_time)
            searchAndReply()
            time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            print("Shutting down.")
            break
        except praw.errors.HTTPException as e:
            exc = e._raw
            print("Something bad happened! HTTPError", exc.status_code)
            if exc.status_code == 503:
                print("Let's wait til reddit comes back! Sleeping",
                    SLEEP_TIME, "seconds.")
                time.sleep(SLEEP_TIME)
        except Exception as e:
            print("Something bad happened!", e)
            traceback.print_exc()
            print("Sleeping", SLEEP_TIME, "seconds.")
            time.sleep(SLEEP_TIME)
