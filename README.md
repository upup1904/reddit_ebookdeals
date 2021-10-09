These are python / bash scripts to post links to r/ebookdeals

It works from the command line and posts a link to the amazon book page

```$ frugal.sh https://www.amazon.com/dp/B01HXGL4CG```

You can use the urls from the "Get it" links on ereaderiq.com

This is free to use for whatever. I'm hoping it will inspire someone to make a
GUI for posting to r/ebookdeals, and add support for other ebook vendors.

Pull requests welcome.

form_it.py  -- goes to amazon and tries to dig out price, author, title.  Rules
of sub are those components have to be in subject line in a certain order.

post_it.py -- uses praw to post your stuff.  You have to enable praw in
your posting account (if someone can send me directions for this readme, that
would be great -- either a pull request or pm earthsophagus on reddit)

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





