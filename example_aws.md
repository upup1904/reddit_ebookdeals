make a spot instance Ubunto 20.04, i used t3.micro
allocate an elastic ip  - 54.156.48.95
give it security group allowing ssh

connect to it and run:


```
sudo apt update && sudo apt -y upgrade

python3 --version
```

For me that gets 3.8.10

```
sudo apt install -y  python3.8-venv
sudo apt install -y python3-pip
sudo apt install -y firefox-geckodriver
python3 -m pip install pip -U
git clone https://github.com/upup1904/reddit_ebookdeals.git frugal
cd frugal
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python form_it.py  https://go.ereaderiq.com/us/s/1/B0722D6PCG
```

if you installed a different linux you might need to edit form_it.py to look for geckodriver in a different location

For post_it, you have to set up an app for your reddit account,
that is just a formality which makes sure you're not running something
by mistake, I believe.

While  you are logged in go to

https://www.reddit.com/prefs/apps

click on "create another app", it will brin gup a dialog

* Give it any name you want.  
* Choose "script"
* Give it any descript you want
* For both urls, put in any url you want, e.g. https://reddit.commit
* Click "create"

On the resulting screent, you'll get two strings or random chars.
"secret" is prominent.  On my browser, the "id" is kind of
inconspicous, it's in small print under the app name, with no label.
Anyway, you need the id and secret below:


Make a directory /secrets
and a file:
/secrets/einkcheap.dev

(einkcheap is the name of the account I use to post and it's hardcoded
in the script but  the filename is arbitrary and doesn't have any
effect)

the contents of the file:

```
[ebooks]
username = your_reddit_name_here
password = your_regular_reddit_passowrd
client_secret = 6TZfd4A-p0O0yy77_uWa1cZrd66INw
client_id= vJdomwyqJ8xb1w
```

The first scrpt writes out to /tmp/dealt.txt
and the second script posts that file, using the configurations
above, to /ebookdeals

- - -  -

The script file, frugal.sh, is just a sample.  It calls form_it, shows what it's about to
post, and if you hit <enter> it posts it (using the configs set up below)  But you
could coordinate the two scripts however you want.








