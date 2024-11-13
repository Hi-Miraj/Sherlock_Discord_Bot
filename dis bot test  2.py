import discord
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Command for saying hello
        if message.content.lower() == '!hello':
            await message.channel.send(f'Hello, {message.author.mention}!')

        # Command to check bot latency
        elif message.content.lower() == '!ping':
            latency = round(self.latency * 1000)  # Convert to milliseconds
            await message.channel.send(f'Pong! Latency is {latency} ms.')

        # Respond to any message containing the word "bot"
        elif 'bot' in message.content.lower():
            await message.channel.send("I'm here and listening! Type `!help` to see commands.")

        # Help command to list available commands
        elif message.content.lower() == '!help':
            commands = """
            Here are the commands you can use:
            - `!hello` - Greet the bot
            - `!ping` - Check the bot's latency
            - `!help` - Display this help message
            """
            await message.channel.send(commands)

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

client.run(os.getenv("DISCORD_TOKEN"))
