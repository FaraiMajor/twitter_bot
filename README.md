<p align="center">
  <h1 align="center">Farai's Twitter bot</h1>
  <p align="center">A Python twitter bot that uses chatGPT to generate random tweets.<p>
  <p align="center">
      <a href="https://github.com/FaraiMajor/twitter_bot/blob/main/LICENSE"/>
      <img src="https://img.shields.io/github/license/madrenodriza/markovtweets.svg" />
    </a>
      <a href="https://www.python.org/">
    	<img src="https://img.shields.io/badge/built%20with-Python3-red.svg" />
    </a>

This ia a twitter bot that uses OpenAI API(chatGPT) to create a tweet using a random trending twitter topic every hour.The trending topics are  twitter's current trending list for that hour. the script will get the topics, store them and select one randomly for use with chatGPT

## Installations
in your terminal clone this repo with then cd to that folder or open with any IDE i.e vs-code
```bash
git clone <SSH KEY>
```
```bash
cd <to folder>
```
```bash
pip install tweepy
```

##Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the neccesary dependencies.

```bash
pip install tweepy
```
```bash
pip install geocoder
```
```bash
pip install schedule
```
```bash
pip install pandas
```
```bash
pip install openai
```

##Instructions to run the program

-make a developer account with Twitter and get your api keys and access tokens
-go to openAI API section, create an account and generate API keys
Use these keys in the program

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT LICENSE](https://choosealicense.com/licenses/mit/)
