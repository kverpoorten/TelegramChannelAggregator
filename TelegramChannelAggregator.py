import configparser
import logging
from pprint import pprint

from channel import Channel
from telethon import TelegramClient, events

config = configparser.ConfigParser()
config.read("config.ini")


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=config["logging"]["loglevel"],
    datefmt="%Y-%m-%d %H:%M:%S",
)

client = TelegramClient(
    'tgsession',
    config["telegram"]["api_id"],
    config["telegram"]["api_hash"],
)

bot = TelegramClient(
    'bot',
    config["telegram"]["api_id"],
    config["telegram"]["api_hash"],
).start(bot_token=config["telegram"]["aggregator_bot_token"])
bot_chat_id = config["telegram"]["aggregator_bot_token"].split(":")[0]

chats_to_monitor = {}


@client.on(events.NewMessage(incoming=True))
async def tg_incoming_message_handler(event):
    logging.debug("Incoming telegram message from " + str(event.message.sender_id))
    if (event.message.sender_id in chats_to_monitor):
        logging.debug("Received Message from chat to monitor: " + event.message.message)
        logging.debug("Testing message with filter \'" + chats_to_monitor[event.message.sender_id].regex.pattern + "\"")

        if (chats_to_monitor[event.message.sender_id].test_filter(event.message.message.lower()) == True):
            logging.debug("Found a match! Forwarding message to aggregation chat")
            await send_tg_message(event.message)


@client.on(events.NewMessage(outgoing=True))
async def tg_outgoing_message_handler(event):
    logging.debug("Outgoing telegram message from " + str(event.message.sender_id))
    if (str(event.input_chat.user_id) == bot_chat_id):
        logging.debug("The following command was sent to the bot: " + event.message.message + "; checking if we should forward it...")
        for chat_id in chats_to_monitor:
            channel = chats_to_monitor[chat_id]
            await channel.forward_message(event.message.message)


async def send_tg_message(message):
    await bot.send_message(int(config["telegram"]["aggregator_bot_chat_id"]), message)


async def main():
    logging.info("*** TelegramChannelAggregator Bot started ***")
    
    channels_by_name = {}
    for section in config:
        if (section.startswith("channel-")):
            channels_by_name[config[section]["name"]] = Channel(
                config[section], client, bot, logging)

    async for dialog in client.iter_dialogs():
        if (dialog.name in channels_by_name):
            logging.info("Monitoring chat \"" + dialog.name + "\" with filter \"" + channels_by_name[dialog.name].regex.pattern + "\"")
            chats_to_monitor[dialog.id] = channels_by_name[dialog.name]
            chats_to_monitor[dialog.id].set_chat_id(dialog.id)

    startup_message = "TelegramChannelAggregator Bot started and monitoring " + str(len(chats_to_monitor)) + " chats:"
    count = 1
    for chat_id in chats_to_monitor:
        channel = chats_to_monitor[chat_id]
        startup_message += "\n    " + str(count) + ". \"" + channel.name + "\" with filter \"" + channel.regex.pattern + "\""
        count += 1

    await send_tg_message(startup_message)
   

with client:
    client.loop.run_until_complete(main())


client.start()
client.run_until_disconnected()