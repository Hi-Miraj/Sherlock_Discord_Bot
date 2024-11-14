import os
import discord
from huggingface_hub import InferenceClient

# Set up Hugging Face client with your API key
HUGGINGFACE_API_KEY = os.getenv("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")  # or replace with your API key directly
client = InferenceClient(api_key=HUGGINGFACE_API_KEY)

# Discord bot setup
class QwenDiscordBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Check if the message is a question (prefixing with "!ask")
        if message.content.startswith("!ask"):
            question = message.content[len("!ask "):].strip()

            if not question:
                await message.channel.send("Please provide a question.")
                return

            # Display loading message
            loading_message = await message.channel.send("Thinking...")

            try:
                # Generate response using Qwen2.5-Coder-32B-Instruct model
                messages = [{"role": "user", "content": question}]
                stream = client.chat.completions.create(
                    model="Qwen/Qwen2.5-Coder-32B-Instruct",
                    messages=messages,
                    max_tokens=500,
                    stream=True
                )

                # Collect response in chunks
                response = ""
                for chunk in stream:
                    response += chunk.choices[0].delta.content

                # Send the generated response back to the Discord channel
                await loading_message.edit(content=response)

            except Exception as e:
                await loading_message.edit(content=f"An error occurred: {e}")

# Define the bot intents
intents = discord.Intents.default()
intents.message_content = True

# Instantiate and run the bot
bot = QwenDiscordBot(intents=intents)
bot.run(os.getenv("DISCORD_TOKEN"))  # Ensure your Discord token is saved as DISCORD_TOKEN
