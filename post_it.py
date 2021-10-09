import praw
import configparser

config = configparser.ConfigParser()
try:
    config.read(["/secrets/einkcheap.env", "/tmp/deal.txt"])
except Exception:
    print("parsing config file faied.  Probably % in url")
    raise


username = config['ebooks']['username']
pwd = config['ebooks']['password']
secret = config['ebooks']['client_secret']
id = config['ebooks']['client_id']
deal = config['deal']['sale']
booktitle, bookurl = deal.split("|^|")


r = praw.Reddit(user_agent="ebookdeal_poster by /u/earthsophagus",
                client_secret=secret,
                client_id=id,
                username=username,
                password=pwd)


subreddit = r.subreddit('ebookdeals')

print("submitting to sub")
subm = subreddit.submit(title=booktitle, url=bookurl)
print(f"success: {subm.id}")  # or it would have raised an error

print("to delete it:")
print(f"unfrugal.sh {subm.id}")
exit(0)
