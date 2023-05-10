
# imports from this project
from secret_things import bot_token

from discord import app_commands
from discord.ext import commands
import discord

from cog_file import TestCog
cog_classes = [TestCog]

class MyBot(commands.Bot):
    def __init__(self, description:str, cog_classes:list, starting_message=None) -> None:

        self.starting_message = starting_message
        self.cog_classes = cog_classes
        
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        
        super().__init__(command_prefix='-', description=description, intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        
        # add cogs
        for cog in self.cog_classes:
            await self.add_cog(cog(self))

if __name__ == '__main__':

    description = 'bot for testing discord.py code'
    bot = MyBot(
        description=description,
        cog_classes=cog_classes,
        starting_message='yo im a bot'
    )

    bot.run(bot_token)

