# reddit bot that messages me every time there is a post on r/askreddit/hot that has 10000+ comments

import praw
import OAuth2Util
import time

user_agent = "AskReddit tracker 1.0 by /u/TheMaou"
r = praw.Reddit(user_agent)
o = OAuth2Util.OAuth2Util(r)  										# connect via OAuth2
o.refresh(force=True) 												# automatically refresh token when necessary

already_received = []
subreddit = r.get_subreddit('askreddit')
popularity_threshold = 10000

while True:
	try:
		for submission in subreddit.get_hot(limit=25): 					# look at most recent 25 posts in r/askreddit/hot
			if (submission.id not in already_received and 
			submission.num_comments >= popularity_threshold):
				msg = '[AskReddit Thread](%s)' % submission.short_link
				r.send_message('TheMaou', 'Popular AskReddit Thread!', msg)
				already_received.append(submission.id)
		time.sleep(1800) 												# execute every 30 minutes
	except KeyboardInterrupt:											 
		print ("Shutting down.")
		break
	except praw.errors.HTTPException as e:
		exc = e._raw
		print ("Something bad happened! HTTPError", exc.status_code)
	except Exception as e:
		print("Something bad happened!", e)
		traceback.print_exc()