<a name="readme-top"></a>
<!-- ABOUT THE PROJECT -->
## About

This is a way to automate posting quotes to social media services (X, Mastodon, and Bluesky for now, others to follow maybe), written in Python. 

I was originally looking for something that could randomly pull quotes from a list and then tweet them, not repeating any until the list was run and then do it all over again. Forever.

**I am not a programmer. I read a book on Python and then did this.**

The implementations in this code are probably not the best implementations or even good ones, but they've been running for at least four years and have given me zero problems. I'm making this public so I can easily pull it and because there aren't a whole lot of things out there like it.

Uses for this:

- Posting anything to social media in a sequential manner (e.g. if you wanted to post a book or song line-by-line).
- Posting stuff in a random, non-repeatable manner.
- Scheduling posts in a difficult way.

Uses in the wild:
- [Mastodon Dune Quote Bot](https://mastodon.social/@dunequotes)
- [Bluesky Dune Quote Bot](https://bsky.app/profile/dunequotes.bsky.social)
- [Threads Dune Quote Bot](https://www.threads.com/@muaddibspeaks)
- RETIRED:[X Dune Quote Bot](https://x.com/dunequotebot)

Basically this is just a tool I made because I wanted a Dune quote bot to exist.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

Tested with Python3.14.10 on 11/04/2026.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Everything on here assumes you're running a Unix-like system (e.g. Linux/MacOS). It won't work on Windows.

### Prerequisites

Python! Install Python if you haven't already. Your default install should be fine.

I think it comes installed on Debian/Ubuntu. To install it on MacOS with [homebrew](https://brew.sh)run:
```sh
brew install python@3.14
```
Also, get pip if you don't have it:

```sh
sudo apt install python3-pip
```

And, to run this in a virtual environment, you'll need the package to do that:

Debian/Ubuntu
```sh
sudo apt install python3-venv
```
MacOS
```sh
brew install virtualenv
```

## Installation

It's *highly* recommended that you run Python in a virtual environment. In fact, Debian and Ubuntu will throw up a lot of warnings if you don't.

### Clone the repo
```sh
git clone https://github.com/jason-weiser/pastaquote.git
```
### (optional) Set up a virtual environment
```sh
cd pastaquote
python3.14 -m venv venv
source venv/bin/activate
```
### Install the required pip modules:
```sh
pip install -r requirements.txt
```
### Copy the config.yaml file:
```sh
cp bot/config.sample.yaml bot/config.yaml
```
### Set up your .txt file full of posts. 

This can either be a file on your system (must have read permissions), or it can be a webpage. See https://assets.jasonweiser.com/files/data/dune_quotes.txt for an example of the file. It's just a file where each thing you want to post is a new line. Either save this to your server or to a publicly-available webpage.

If you're setting up Threads, make sure the location is present in `config.yaml` **before** attempting to get your token. Everything else can be set up later.

### Get your API keys. 

Currently, this bot supports posting via the API to X, Mastodon, and Bluesky. Threads to follow if they add the functionality. 

#### Setting up Twitter/X
> [!IMPORTANT]  
> X/Twitter support is depreciated and will be removed at v0.6, so please fork that release if you want to keep that functionality.

Follow [this link](https://assets.jasonweiser.com/files/archive/x-api.html) to learn how to do it for X. I archived the page because I kept getting prompted for a login when I was reading it which was super annoying.

Of note: You *may* need to add a new project and add your app to the project in the [https://developer.x.com](https://developer.x.com) area. Docs are unclear, but I was getting a lot of errors until I did this (seemingly) meaningless thing. 

#### Setting up Mastodon

Current as of 2026: Find your user profile in the bottom-left. Click the three dots and go to Settings. Then, go to Development. Click **New Application** and name it whatever you want. As far as I know, all you need to allow in Scopes is `write:statuses`. Hit `Submit`.

**Click on the name of your app** on the **Development** page. You'll see your access token. This is what goes in config.yaml.

#### Setting up Bluesky

[This link](https://bossagyu.com/en/blog/024-bluesky-api/) will show you how to get your app password for Bluesky. Basically it's just the gear on the left-hand menu > Privacy and Security > App Passwords. For username use the username for your profile without the @. for most people this will look like `username.bsky.social`.

#### Setting up Threads

Oof. Ok. Threads isn't like the others, where you get an access token or a secret key and it's done. Threads has a token you need to request from them before it expires in 60 days. The process to get a token from them is annoying and cumbersome, but it *seems* like it will be pretty seamless once everything is up and running. [This is a solid walkthrough if you want pictures](https://blog.nevinpjohn.in/posts/threads-api-public-authentication/).

1. **Get a Threads account** by *any means necessary*. That sounds ominous but they used to require an Instagram account and I'm not sure if they still do.

2. **Create a Meta developer app**. I know... At least it's not Xitter, though? Go to [https://developers.facebook.com](https://developers.facebook.com) (so I think you probably need a Facebook account. Maybe tarry a bit and take in the misinformation and AI slop while you're there). 

Go to **My Apps** and then **Create App** Choose **Access Threads API** under use-case, pick an alluring name, and you're done with this step.

3. **Configure the App**. Go to the **left sidebar**, then **use cases**, then **customize** on the **Access the Threads API**. 

Under 'Permissions and features' add **threads_content_publish** ('threads_basic' is the default). Then, go to **Settings** and add  a **Redirect Callback URL**. As far as I can see this should be https and it probably can't be `localhost`. I used my main website. Nothing needs to be running there. You'll just use it to copy the auth token from the URL. If you don't own a domain, feel free to use `https://jasonweiser.com/`. I don't see these links at all, so no worries about me stealing your tokens or whatever. 

Copy the **Threads App ID** and **Threads App Secret** into your config as `APP_ID` and `APP_SECRET`, respectively. Additionally, copy the URL you used into the `REDIRECT_URI` **EXACTLY** as it is on the site. 

Then, back on the Meta dashboard, you can click **Finish Customization** and confirm.

4. **Add a bot account as a tester.** In the sidebar, to to **App roles -> Roles -> Testers -> Add People**. Choose **Threads Tester** and enter the bot's Threads username. 

After that **log onto Threads as the bot account** (whichever account you want to actually post - this can be different from the Facebook admin account used to manage everything). 

**Logged into Threads as the bot** you have to accept the invite you sent yourself under **(hamburger menu at the top left-ish) Settings -> More settings -> Website permissions -> invites**.

5. **Authorize the app and get the code**. While logged into threads **as the bot account**, visit the following link, but fill in the details with your data:
```
https://threads.net/oauth/authorize?client_id=APP_ID&redirect_uri=REDIRECT_URI&scope=threads_basic,threads_content_publish&response_type=code
```
Approve the request, and you'll be redirected to a different page using your redirect URL. Go to the address bar, and you'll find `?code=` followed by a loooooooong string that ends in `#_`. Copy **everything after the `=` and before the `#` at the end**. Meta puts the `#_` on every code and it is *not* part of the actual code. That is your authorization code. 

6. **Get your long-lived Token**. The authorization code **expires in one hour** so you'll want to do the next part immediately. Copy the code into your config.yaml under `CODE`. Assuming you're still using the Python virtual environment, run:

```python
python3 bot/bot.py --threads-token
```
This will save the token in `data/threads-token.json` (technically it gets a short-lived token which then gets you the long-lived token which is saved there, but don't worry about it). If you post at least once every 60 days, the token should stay good forever, as the script checks the age and auto-renews with the current valid token if said token is older than seven days. If you let it lapse, change your password, or have it revoked for any reason, you'll need to repeat steps 5 and 6 to get a new authorization code.

### Update the config.yaml with your credentials:
```yaml
SETUP:
  TYPE: "random"
  LIST_LOCATION: "/home/username/quotes_to_post.txt"
PLATFORMS: 
  TWITTER:
    ENABLE_TWITTER: False
    TWITTER_CONSUMER_KEY: "gibberishgibberishgibberish"
    TWITTER_CONSUMER_SECRET: "gibberishgibberishgibberish"
    TWITTER_ACCESS_TOKEN: "gibberishgibberishgibberish"
    TWITTER_ACCESS_TOKEN_SECRET: "gibberishgibberishgibberish"
    CHARACTER_LIMIT: 280
    SKIP_TOO_LONG: False
    ENABLE_HASHTAGS: False
    HASHTAGS: ["Hashtag","Hashtag"]

  MASTODON:
    ENABLE_MASTODON: True
    MASTO_ACCESS_TOKEN: "gibberishgibberishgibberish"
    MASTO_BASE_URL: "https://example.com"
    CHARACTER_LIMIT: 500
    SKIP_TOO_LONG: False
    ENABLE_HASHTAGS: True
    HASHTAGS: ["Hashtag","Hashtag"]

  BLUESKY:
    ENABLE_PLATFORM: False
    USERNAME: "yourusername.bsky.social"
    PASSWORD: "12ab-3c4d-e57f-8gh9"
    CHARACTER_LIMIT: 300
    SKIP_TOO_LONG: False
    ENABLE_HASHTAGS: False
    HASHTAGS: ["Hashtag","Hashtag"]

  THREADS:
    ENABLE_PLATFORM: False
    BASE: "https://graph.threads.net/v1.0"
    USER_ID: "me"
    APP_ID: "12345678910111"
    APP_SECRET: "1023a45b6cd7890ef12ghi3j456kl789"
    REDIRECT_URI: "https://example.com/"
    CHARACTER_LIMIT: 500
    SKIP_TOO_LONG: False
    ENABLE_HASHTAGS: False
    HASHTAGS: ["Hashtag","Hashtag"]
```
**Of Note**:
- You decide here whether you're posting in a sequential list or from random, non-repeating selections in a list.
- Please match things in quotations and things not in quotation exactly, filling it in with your own details but keeping the format.
- You can point it to a webpage that has a .txt file or a local file via a path it has read access to. Either work. Just replace the webpage above. 
- If you want hashtags, please change `False` to `True` (no quotes) and add however many hashtags you want. These will go on all *future* posts.
- The config will not enforce character limits by default, but instead will throw up warnings. If you mark "SKIP_TOO_LONG" to True, it will skip any that are too long for that particular service. You can see a list of any posts that are too long in the log.

### Run the initialization
```sh
python3 bot/bot.py --init
```
### If that didn't throw out any errors, try your first post!
```sh
python3 bot/bot.py --post
```
### You schedule via cronjob, so you do that how many times a day you want with the following text. This will be for every hour, for example.

- If you use a virtual environment: `01 */1 * * * /path/to/your/venv/bin/python path/to/pastaquote/bot/bot.py --post`
- Using your regular Python install: `01 */1 * * * python3 path/to/pastaquote/bot/bot.py --post`
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Adding quotes to the bot

There are two ways to add quotes to the bot. The first is the method mentioned above:
(from the pastaquote folder)
```sh
venv/bin/python path/to/pastaquote/bot/bot.py --init
```

This will, however, reset numbering for sequential lists and completely reload the list a randomized bot is using, leading to the possibility of near-repeats.

I've added the functionality to add to a running list without resetting the numbering or reloading it. Update your text file by adding lines and run the following:

```sh
venv/bin/python bot/bot.py --add
```
This will add the lines, prompting you for approval with each line if you choose. It will not restart the list or the numbering.

If you don't want to approve each line, add a "-y" to the command above:

```sh
venv/bin/python bot/bot.py --add -y
```
This way you can schedule that as well. All lines added will be logged.

## Updating

To update, simply download the new release and copy the contents of the folder to your current working directory.
It will keep your numbering, current list position, and everything else.

<!-- DISCLAIMER -->
## Disclaimer

I'm not responsible for what you post with this. Please don't use it to post anything hateful or harassing. Just because you use this tool does not mean I endorse your content in any way. 

Also not responsible if you use this for infringement or any other illegal activity. Please use at your own risk/discretion.

Additionally, like I said above, I'm not a programmer. This comes with no warranties and I accept no liabilities for you choosing to use this.
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] Add Mastodon
- [x] Add hashtags
- [x] Add method by which you can add to actively-running list without having to reload the list
- [x] Add Bluesky
- [x] Add Threads if that's even possible
- [ ] Add Docker container (requires me learning Docker)
- [ ] Add webpage/GUI (requires me learning Flask and/or Javascript)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing & Issues

Any contributions you make are **greatly appreciated**. You'll probably have to walk me through it, though. I'm pretty new.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/Feature`)
3. Commit your Changes (`git commit -m 'Add some Feature'`)
4. Push to the Branch (`git push origin feature/Feature`)
5. Open a Pull Request

Please let me know when ("when" not "if") you find an issue.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Jason Weiser 
[@weiser@mstdn.social](https://mstdn.social/@weiser) | jason@jasonweiser.com | https://jasonweiser.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>
