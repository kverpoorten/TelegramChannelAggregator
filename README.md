
# TelegramChannelAggregator

**The problem**: you have many Telegram bots that are all sending you messages; you are however only interested in a subset of those messages.

**The solution**: Run this TelegramChannelAggregator Bot which can filter out only specific messages from many chats, which are then all sent to one single chat. 
This allows you to mute all other chats and only keep notifications enabled for this single chat that contains only interesting messages.

## Download and install

You need run Python 3.7 or higher.

Do a `git clone` with the steps described below.

```
$ sudo apt install git
$ git clone https://github.com/kverpoorten/TelegramChannelAggregator
$ cd TelegramChannelAggregator
$ pip3 install -r requirements.txt
```

## Configuration of the bot

Create a copy of the file `config.example.ini` and rename that copy to `config.ini`

Then you can edit that config file.

### Telegram 
There are two sets of Telegram related settings we need. 
First we need the Telegram App ID and Hash so we can monitor incoming message from the channels you select.
Second we need a bot token and chat id so the bot can send the filtered messages to you in a single chat.

#### Telegram api_id and api_hash
To get the Telegram Api ID and hash you have to create an application.

These are the steps to do that:
-   Login to your Telegram account [here](https://my.telegram.org/) with the phone number of the developer account to use.
-   Visit the [API development tools](https://my.telegram.org/apps)
-   Create a new application window will appear. Fill in your application details. There is no need to enter any URL, and only the first two fields (App title and Short name) can be changed later.
-   Click on Create application at the end. Remember that your API hash is secret and Telegram won’t let you revoke it. Don’t post it anywhere!

Fill these in here inside config.ini:
```
api_id = 1234566
api_hash = o6la4h1158ylt4mzhnpio6la
```

#### Telegram bot_token and chat_id
The other set of values are used to sent notifications to you in the aggregation chat.
-   First you need to create a bot to get a bot_token
-   Open telegram and search for 'BotFather' start a conversation
-   Type: `/newbot`
-   Answer the questions it asks after doing this (which get the name of it, etc).
-   When you've completed step 2, you will be provided a bot_token that looks something like this: 123456789:alphanumeric_characters.
-   Type /start now in the same dialog box to enable and instantiate your brand new bot.

Then you need the chat id, you can do that by opening the following url
```
https://api.telegram.org/bot<YourBOTToken>/getUpdates
```
where you replace `<YourBOTToken>` with the bot_token 'BotFather' gave you for your bot (e.g.: `https://api.telegram.org/bot123456789:alphanumeric_characters/getUpdates`

Send again a message to your bot, and then refresh the url. You will see a message like below:
```
{
   "ok":true,
   "result":[
      {
         "update_id":123123123,
         "message":{
            "message_id":3,
            "from":{
               "id":321321321,
               "is_bot":false,
               "first_name":"Kristof",
               "username":"my_username",
               "language_code":"en"
            },
            "chat":{
               "id":987654321,
               "first_name":"Kristof",
               "username":"my_username",
               "type":"private"
            },
            "date":1647691662,
            "text":"test"
         }
      }
   ]
}
```

Take the chat id from this message (in this example that is **987654321**).

Fill these in here inside config.ini:
```
aggregator_bot_token = 123456789:alphanumeric_characters
aggregator_bot_chat_id = 987654321
```

### Channels
You can define as many channels as you want in the configuration. For each channel you define a name and a filter.

The bot will monitor each of the defined channels, and only forward message that match the filter to your aggregation chat.

Define a channel in the config as follows
```
[channel-anything-you-want-here]
name = The Name of the channel in Telegram
filter = a regular expression to filter incoming messages
```
The section for each channel needs to start with `channel-` 

The name is the exact name of the channel in Telegram.

The filter is a [regular expression](https://docs.python.org/3/howto/regex.html) which is used to filter all incoming messages in that channel.
For example if you want to filter messages that contain either the word "buying" or the word "selling" the filter expression would be `buying|selling`.

## First run
The first time you start the bot, make sure to do it on the command line as follows:
```
$ python3 ./TelegramChannelAggregator.py
```
The first time it starts, it will ask you to enter your mobile phone number (the one you use for Telegram). Then you will receive a one time code in Telegram which you have to enter as well.
This only happens the first time to initialize the Telegram connection for your bot.

At startup the bot will send you a message on Telegram showing which chats it is monitoring and which filters are used for each of these channels, it looks something like this:
```
TelegramChannelAggregator Bot started and monitoring 2 chats:  
1. "MyInterestingChannel-1" with filter "money|profit"  
2. "MyInterestingChannel-2" with filter "selling|buying"
```

## Start Automatically
If you want the script to run automatically after a reboot and you want it to keep running after you close the console, this can be done by installing it as a service

Example service files `TelegramChannelAggregator.service`is provided. You need to edit the paths and your user inside them to reflect your install. 
Then install the service as describe below.
```
$ sudo cp TelegramChannelAggregator.service /etc/systemd/system/
```
To start the script:
```
$ sudo systemctl start TelegramChannelAggregator.service
```
To make sure the script starts automatically at boot:
```
$ sudo systemctl enable TelegramChannelAggregator.service
```
To disable it starting automatically at boot
```
$ sudo systemctl disable TelegramChannelAggregator.service
```
How to check status:
```
$ sudo systemctl status TelegramChannelAggregator.service
● TelegramChannelAggregator.service - TelegramChannelAggregator Bot
     Loaded: loaded (/etc/systemd/system/TelegramChannelAggregator.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2022-03-19 20:20:14 UTC; 3s ago
   Main PID: 203325 (python3)
      Tasks: 1 (limit: 2339)
     Memory: 29.4M
     CGroup: /system.slice/TelegramChannelAggregator.service
             └─203325 /usr/bin/python3 /home/kristof/TelegramChannelAggregator/TelegramChannelAggregator.py

Mar 19 20:20:14 ubuntu-kristof python3[203325]: 2022-03-19 20:20:14 INFO     Connection to 149.154.167.92:443/TcpFull complete!
Mar 19 20:20:14 ubuntu-kristof python3[203325]: 2022-03-19 20:20:14 INFO     Connecting to 149.154.167.92:443/TcpFull...
Mar 19 20:20:14 ubuntu-kristof python3[203325]: 2022-03-19 20:20:14 INFO     Connection to 149.154.167.92:443/TcpFull complete!
Mar 19 20:20:14 ubuntu-kristof python3[203325]: 2022-03-19 20:20:14 INFO     *** TelegramChannelAggregator Bot started ***
Mar 19 20:20:15 ubuntu-kristof python3[203325]: 2022-03-19 20:20:15 INFO     Monitoring chat "MyInterestingChannel-1" with filter "money|profit"
Mar 19 20:20:15 ubuntu-kristof python3[203325]: 2022-03-19 20:20:15 INFO     Monitoring chat "MyInterestingChannel-2" with filter "buying|selling"
Mar 19 20:20:15 ubuntu-kristof python3[203325]: 2022-03-19 20:20:15 INFO     Disconnecting from 149.154.167.92:443/TcpFull...
Mar 19 20:20:15 ubuntu-kristof python3[203325]: 2022-03-19 20:20:15 INFO     Disconnection from 149.154.167.92:443/TcpFull complete!
Mar 19 20:20:15 ubuntu-kristof python3[203325]: 2022-03-19 20:20:15 INFO     Connecting to 149.154.167.92:443/TcpFull...
Mar 19 20:20:15 ubuntu-kristof python3[203325]: 2022-03-19 20:20:15 INFO     Connection to 149.154.167.92:443/TcpFull complete!


```

How to check logs:
```
$ sudo journalctl -u TelegramChannelAggregator.service 
```

How to edit an already installed service file:
```
$ sudo systemctl edit --full TelegramChannelAggregator.service 
```

## Debugging

Set loglevel to DEBUG in config.ini to output more debug information
```
[logging]
loglevel = DEBUG
```
