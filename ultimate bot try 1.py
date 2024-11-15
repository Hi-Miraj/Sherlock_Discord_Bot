import discord
import random

# Create your bot client
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Core Fun Commands
        if message.content == '/joke':
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "Why don’t skeletons fight each other? They don’t have the guts."
            ]
            await message.channel.send(random.choice(jokes))

        elif message.content == '/roast':
            members = [member.name for member in message.guild.members if not member.bot]
            random_member = random.choice(members)
            roasts = [
                f"{random_member}, you’re as useless as the ‘g’ in lasagna.",
                f"{random_member}, you bring everyone so much joy when you leave the room.",
                f"{random_member}, I would agree with you but then we’d both be wrong."
            ]
            await message.channel.send(random.choice(roasts))

        elif message.content == '/compliment':
            compliments = [
                "You're an amazing person!",
                "You light up the room!",
                "You're the reason someone smiled today!"
            ]
            await message.channel.send(random.choice(compliments))

        # Show all commands when "/" is typed
        elif message.content == '/':
            command_list = (
                "Here are my commands:\n"
                "`/joke` - Tells a random joke\n"
                "`/roast` - Roasts a random server member\n"
                "`/compliment` - Gives a random compliment"
            )
            await message.channel.send(command_list)

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Instantiate and run the bot
client = MyClient(intents=intents)
client.run("DISCORD_TOKEN")
