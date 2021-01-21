# Pràctica de LP

## Getting Started

### Setup

Install requirements

```
pip3 install -r requirements.txt
```

### Compiler

To run the compiler we need a valid input.txt file

```
cd c/
python3 test.py input.txt
```

This saves a graph file in c/ that contains all the elements of the quiz

### Telegram Bot

First we need to move the graph created to /bot/enquestes, and rename it to whatever we want it to be called inside the chat

```
mv ./c/graf ./bot/enquestes/E
```

And then run the bot

```
cd bot/
python3 bot.py
```

And go to url to test it
