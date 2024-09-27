<a name="readme-top"></a>
<!-- ABOUT THE PROJECT -->
## About

This is a way to automate posting quotes to social media services (X and Mastodon for now, others to follow maybe), written in Python. 

I was originally looking for something that could randomly pull quotes from a list and then tweet them, not repeating any until the list was run and then do it all over again. Forever.

**I am not a programmer. I read a book on Python and then did this.**

The implementations in this code are probably not the best implementations or even good ones, but they've been running for at least four years and have given me zero problems. I'm making this public so I can easily pull it and because there aren't a whole lot of things out there like it.

Uses for this:

- Posting anything to social media in a sequential manner (e.g. if you wanted to post a book or song line-by-line).
- Posting stuff in a random, non-repeatable manner.
- Scheduling posts in a difficult way.

Uses in the wild:
- [X Dune Quote Bot](https://x.com/dunequotebot)
- [Mastodon Dune Quote Bot](https://botsin.space/@dune)

Let me know if, against your better judgement, you use this.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

Updated to Python3.12.6 on 9/27/2024.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Everything on here assumes you're running a Unix-like system (e.g. Linux/MacOS). It won't work on Windows.

### Prerequisites

Python! Install Python if you haven't already. Your default install should be fine. 

Also, get pip if you don't have it:

```sh
sudo apt install python3-pip
```

And, to run this in a virtual environment, you'll need the package to do that:

```sh
sudo apt install python3-venv
```

### Installation

It's recommended that you run Python in a virtual environment. You can also not, though. It's your machine.

1. Clone the repo
```sh
git clone https://github.com/jason-weiser/pastaquote.git
```
2. (optional) Set up a virtual environment
```sh
cd pastaquote
python3 -m venv venv
source venv/bin/activate
```
3. Install the required pip modules:
```sh
pip3 install -r requirements.txt
```
4. Copy the config.yaml file:
```sh
cp bot/config.sample.yaml bot/config.yaml
```

5. Get your API keys. Currently, this bot supports posting via the API to X, Mastodon, and Bluesky. Threads to follow if they add the functionality. 
	- Follow [this link](https://assets.jasonweiser.com/files/archive/x-api.html) to learn how to do it for X. I archived the page because I kept getting prompted for a login when I was reading it which was super annoying.
 		- Of note: You *may* need to add a new project and add your app to the project in the [https://developer.x.com](https://developer.x.com) area. Docs are unclear, but I was getting a lot of errors until I did this (seemingly) meaningless thing. 
	- [This link](https://dev.to/bitsrfr/getting-started-with-the-mastodon-api-41jj) has a good description of how to do so in Mastodon under the "Find your access token" header.
  - [This link](https://bossagyu.com/en/blog/024-bluesky-api/) will show you how to get your app password for Bluesky. Basically it's just hamburger menu in top left > Settings > App Passwords. For username use the username for your profile without the @

6. Set up your .txt file full of posts. This can either be a file on your system (must have read permissions), or it can be a webpage. See https://assets.jasonweiser.com/files/data/dune_quotes.txt for an example of the file. It's just a file where each thing you want to post is a new line. Either save this to your server or to a publicly-available webpage.

7. Update the config.yaml with your credentials:
```yaml
SETUP:
  TYPE: "random"
  LIST_LOCATION: "/home/username/quotes_to_post.txt"
  
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
```
**Of Note**:
- You decide here whether you're posting in a sequential list or from random, non-repeating selections in a list.
- Please match things in quotations and things not in quotation exactly, filling it in with your own details but keeping the format.
- You can point it to a webpage that has a .txt file or a local file via a path it has read access to. Either work. Just replace the webpage above. 
- If you want hashtags, please change `False` to `True` (no quotes) and add however many hashtags you want. These will go on all *future* posts.
- The config will not enforce character limits by default, but instead will throw up warnings. If you mark "SKIP_TOO_LONG" to True, it will skip any that are too long for that particular service. You can see a list of any posts that are too long in the log.

8. Run the initialization
```sh
python3 bot/bot.py --init
```
9. If that didn't throw out any errors, try your first post!
```sh
python3 bot/bot.py --post
```
10. You schedule via cronjob, so you do that how many times a day you want with the following text. This will be for every hour, for example.
	- If you use a virtual environment: `01 */1 * * * /path/to/your/venv/bin/python path/to/pastaquote/bot/bot.py --post`
	- Using your regular Python install: `01 */1 * * * python3 path/to/pastaquote/bot/bot.py --post`
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Adding quotes to the bot

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

### Updating

To update, simply download the new release and copy the contents of the folder to your current working directory.
It will keep your numbering, current list position, and everything else.

<!-- DISCLAIMER -->
## Disclaimer

I'm not responsible for what you post with this. Please don't use it to post anything hateful or harassing. Just because you use this tool does not mean I endorse it in any way. 

Also not responsible if you use this for infringement or any other illegal activity. Please use at your own risk/discretion.

Additionally, like I said above, I'm not a programmer. This comes with no warranties and I accept no liabilities for you choosing to use this.
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] Add Mastodon
- [x] Add hashtags
- [x] Add method by which you can add to actively-running list without having to reload the list
- [ ] Add Bluesky
- [ ] Add Threads if that's even possible
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
