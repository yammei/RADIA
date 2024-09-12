import os
import sys
import discord
from dotenv import load_dotenv

cli_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(cli_path)

from cli.gt_api import API
api = API()

class Session:
    # Contains session information, bot configurations, and response logic.
    def __init__(self):
        # Access credentials from .env file.
        load_dotenv(".env")
        self.DIS_TOK: str = os.getenv("DIS_TOK")

        # Intents setup.
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)

        # Assign event-handlers.
        @self.client.event
        async def on_ready() -> None:
            print(f'Logged in as {self.client.user}')

        @self.client.event
        async def on_message(message) -> None:
            # Prevent the bot from self-feedback interactions.
            if message.author == self.client.user:
                return

            # Response logic for various message prefixes.
            if message.content[:5] == "grep!":
                prompt: str = message.content[5:]
                await message.reply(f"Hi, how can I help you?\nAsk me a question using the prefix ``grep?`` followed by your question!", mention_author=False)
            elif message.content[:5] == "grep?":
                prompt: str = message.content[5:]
                posted_message = await message.reply(f"<a:typing:1283792220108882024> **Greptile** generating response...", mention_author=False)
                response: str = await self.greptile_API_query(prompt)
                await posted_message.edit(content=f"Hi <@{message.author.id}>!\n{response}")
            else:
                return


    async def greptile_API_query(self, prompt: str) -> any:
        if api.check(source="discord"):
            api.load(source="discord")
            print(prompt)
            response: str = await api.discordQuery(prompt=prompt)
            print(f"Returning from greptile_API_query().")
            return response if len(response) < 2000 else response[:1900]+"..."
        else:
            return "Unable to access Greptile API. Please verify all credentials are valid/active.\n Please refer to the setup documentation on how to use Greptile API CLI & Discord Integration: https://github.com/yammei/greptile-ai/blob/main/README.md"

    # Attempts to activate bot online using your Discord token, DIS_TOK.
    def run(self) -> None:
        if self.DIS_TOK is None:
            print(f"Discord token was not provided. Please provide a Discord token to utilize the bot.")
        else:
            try:
                self.client.run(self.DIS_TOK)
            except Exception as e:
                print(f"Error: {e}")