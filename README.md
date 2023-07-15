<a name="readme-top"></a>
<!-- ABOUT THE PROJECT -->
## About

This is a way to automate posting quotes to social media services (Twitter and Mastodon for now, others to follow maybe), written in Python. 

I was originally looking for something that could randomly pull quotes from a list and then tweet them, not repeating any until the list was run and then do it all over again. Forever.

**I am not a programmer. I read a book on Python and then did this.**

The implementations in this code are probably not the best implementations or even good ones, but they've been running for at least four years and have given me zero problems. I'm making this public so I can easily pull it and because there aren't a whole lot of things out there like it.

Uses for this:

- Posting anything to social media in a sequential manner (e.g. if you wanted to post a book or song line-by-line).
- Posting stuff in a random, non-repeatable manner.
- Scheduling posts in a difficult way.

Uses in the wild:
- [Twitter Dune Quote Bot](https://twitter.com/dunequotebot)
- [Mastodon Dune Quote Bot](https://botsin.space/@dune)

Let me know if, against your better judgement, you use this.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

Built with Python3.11, but it has been tested back to Python3.8.5. Past that, I don't know. Once again, I'm not a programmer.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Everything on here assumes you're running Ubuntu/Debian. If you aren't, you probably know more than I do about how to install python.

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
git clone https://github.com/jason-weiser/Postaquote.git
```
2. (optional) Set up a virtual environment
```sh
cd Postaquote
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

5. Get your API keys. Currently, this bot supports posting via the API to Twitter and Mastodon. Bluesky and Threads to follow if they add the functionality. 
	- Follow [this link](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) to learn how to do it for Twitter. Also, good luck.
	- And [this link](https://dev.to/bitsrfr/getting-started-with-the-mastodon-api-41jj) has a good description of how to do so under the "Find your access token" header.

6. Set up your .csv file full of posts. See https://assets.jasonweiser.com/files/data/dune_quotes.csv for an example. You can post whatever you want, **but "quotes" has to be in the first line**. Either save this to your server or to a publicly-available webpage.

7. Update the config.yaml with your credentials:
```
SETUP:
  TYPE: "random"
  CSV_LOCATION: "https://assets.jasonweiser.com/files/data/dune_quotes.csv"
  
TWITTER:
  ENABLE_TWITTER: False
  TWITTER_CONSUMER_KEY: "gibberishgibberishgibberish"
  TWITTER_CONSUMER_SECRET: "gibberishgibberishgibberish"
  TWITTER_ACCESS_TOKEN: "gibberishgibberishgibberish"
  TWITTER_ACCESS_TOKEN_SECRET: "gibberishgibberishgibberish"
  ENABLE_HASHTAGS: False
  HASHTAGS: ["Hashtag","Hashtag"]

MASTODON:
  ENABLE_MASTODON: True
  MASTO_ACCESS_TOKEN: "gibberishgibberishgibberish"
  MASTO_BASE_URL: "https://example.com"
  ENABLE_HASHTAGS: True
  HASHTAGS: ["Hashtag","Hashtag"]
```
**Of Note**:
- You decide here whether you're posting in a sequential list or from random, non-repeating selections in a list.
- Please match things in quotations and things not in quotation exactly, filling it in with your own details but keeping the format.
- You can point it to a webpage that has a .csv file or a local file via a path it has read access to. Either work. Just replace the webpage above. 
- If you want hashtags, please change `False` to `True` (no quotes) and add however many hashtags you want. These will go on all *future* posts.

8. Run the initialization
```sh
python3 bot/bot.py --init
```
9. If that didn't throw out any errors, try your first post!
```sh
python3 bot/bot.py --post
```
10. You schedule via cronjob, so you do that how many times a day you want with the following text. This will be for every hour, for example.
	- If you use a virtual environment: `01 */1 * * * /path/to/your/venv/bin/python path/to/Postaquote/bot/bot.py --post`
	- Using your regular Python install: `01 */1 * * * python3 path/to/Postaquote/bot/bot.py --post`
<p align="right">(<a href="#readme-top">back to top</a>)</p>



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
- [ ] Add Docker container (requires me learning Docker)
- [ ] Add webpage/GUI (requires me learning Flask and/or Javascript)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an  place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/Feature`)
3. Commit your Changes (`git commit -m 'Add some Feature'`)
4. Push to the Branch (`git push origin feature/Feature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Jason Weiser 
[@jason@weiser.social](https://weiser.social/@jason) | jason@jasonweiser.com | https://jasonweiser.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>
