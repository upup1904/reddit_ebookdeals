# delete an id posted in error-- called bby unfrugal.sh

import praw
import configparser
import sys

config = configparser.ConfigParser()
try:
    config.read(["/secrets/einkcheap.env"])
except Exception:
    print("parsing config file faied.  Probably % in url")
    raise


username = config['ebooks']['username']
pwd = config['ebooks']['password']
secret = config['ebooks']['client_secret']
id = config['ebooks']['client_id']

r = praw.Reddit(user_agent="/u/einkcheap test",
                client_secret=secret,
                client_id=id,
                username=username,
                password=pwd)

post_id = sys.argv[1]

target = praw.models.Submission(r, id=post_id)
result = target.delete()
print(f"result is {result}")

