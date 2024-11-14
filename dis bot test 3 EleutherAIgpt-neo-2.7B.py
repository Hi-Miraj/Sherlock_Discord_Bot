import discord
import requests
import os

# Set your Hugging Face and Discord tokens here or in environment variables
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "YOUR_HUGGINGFACE_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_DISCORD_TOKEN")

# Set up headers for Hugging Face API
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}


# Function to send a prompt to GPT-Neo and get the generated response
def query_huggingface(prompt):
    payload = {"inputs": prompt}
    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.json().get('error', 'Unknown error')}"


# Set up Discord bot client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Command to trigger GPT-Neo response
    if message.content.startswith("!ask"):
        # Extract the prompt after the command
        prompt = message.content[len("!ask"):].strip()

        # Ensure there's a prompt
        if not prompt:
            await message.channel.send("Please provide a prompt after `!ask`.")
            return

        # Query Hugging Face GPT-Neo model
        response = query_huggingface(prompt)

        # Send the response back in Discord
        await message.channel.send(response)


# Run the bot
client.run(DISCORD_TOKEN)
