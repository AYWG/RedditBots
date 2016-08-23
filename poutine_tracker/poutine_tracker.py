# reddit bot that messages me every post on r/food/new that contains "poutine" in the title

import praw
import OAuth2Util
import time

user_agent = "Poutine tracker 1.0 by /u/TheMaou"
r = praw.Reddit(user_agent)
o = OAuth2Util.OAuth2Util(r)  											# connect via OAuth2
o.refresh(force=True) 													# automatically refresh token when necessary

already_received = []
subreddit = r.get_subreddit('food')

while True:
	try:
		for submission in subreddit.get_new(limit=25): 					# look at most recent 25 posts in r/food/new
			title_text = submission.title.lower() 						# get the submission title
			has_poutine = 'poutine' in title_text 		
			if submission.id not in already_received and has_poutine:	# only send a msg if title has 'poutine' in it and I haven't received it before
				msg = '[yummy poutine](%s)' % submission.short_link
				r.send_message('TheMaou', 'Poutine Post!', msg)
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
