import re

class Channel:
    def __init__(self, config, tgclient, tgbot, logging):
        self.name = config["name"]
        self.regex = re.compile(str(config["filter"]), re.IGNORECASE)
        self.forward_commands = str(config["forward_commands"]) == "1"
        self.tgclient = tgclient
        self.tgbot = tgbot
        self.logging = logging
        self.command_forwarded = False

    def set_chat_id(self, chatid):
        self.chat_id = chatid

    def test_filter(self, message):
        if (self.command_forwarded == True):
            self.command_forwarded = False
            return True

        return self.regex.match(message) != None

    async def forward_message(self, message):
        self.logging.debug(
            "Incoming message to forward; forward_commands = " + str(self.forward_commands))
        if (self.forward_commands == True):
            self.logging.debug("Forwarding message to monitored chat")
            self.command_forwarded = True
            await self.tgclient.send_message(self.chat_id, message)
