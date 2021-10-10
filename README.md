These are python / bash scripts to post links to r/ebookdeals

It works from the command line and posts a link to the amazon book page

```$ frugal.sh https://www.amazon.com/dp/B01HXGL4CG```

You can use the urls from the "Get it" links on ereaderiq.com

This is free to use for whatever. I'm hoping it will inspire someone to make a
GUI for posting to r/ebookdeals, and add support for other ebook vendors.

Pull requests welcome, see [contributing](contributing.md).  If you
aren't a github user, can pm me on reddit, earthsophagus.

Files:

form_it.py  -- goes to amazon and tries to dig out price, author, title.  Rules
of sub are those components have to be in subject line in a certain order.
It writes to /tmp/deal.txt


post_it.py -- uses praw to the contents of /tmp/deal.txt to
r/ebookdeals.  In reddit, you have to enable an "app" in your posting
account (see belo), and post_it.py reads connection details from a
file you create on your machine: /secrets/einkcheap.env

delete_it.py  -- sometimes I realize I've posted a link someone else already did,
this lets me delete my post

frugal.sh -- shell script to activate virtual environment and do the post,
will have to be modified for your directory set up

example_aws.txt -- running it on an aws spot instance, mostly as a demo
that the package/instructions are complete.  You'd normally run this on
your pc.  But maybe you want to adapt it to use via web.


This does not use Amazon api.  You need to sell amazon stuff to get api keys.
Instead it pulls the whole page and parses it with BeautifulSoup.  So it's fairly
slow.  Sometimes it can't find an element, and the script tries to warn you.


## Enabling the app for your reddit account

This section is for post_it.py, it is not relevant to form_it.py.  This
explains how to get the id and secret for /secrets/einkcheap.env 

While  you are logged in to reddit, go to:

https://www.reddit.com/prefs/apps

click on "create another app"; it will bring up a dialog:

* Give the app any name you want (e.g. ebdeals). 
* Choose "script"
* Give it any description you want
* For both urls, put in any url you want, e.g. https://reddit.commit
* Click "create"

The name and description are for your own use, so you remember why you
have this years later.  The urls are irrelevant for an individual
script, but you have to fill them in.  The page says that after
configuring the app you need to register it, but, for a script, you
don't.

After you've filled out that form, it will tell you you have a new app
and give you two strings of random chars.  "secret" is prominent.  On
my browser, the "id" is kind of inconspicous, it's in small print
under the app name, with no label.






