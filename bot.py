import discord
from discord.ext import commands
import responses
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('API_TOKEN')


intents = discord.Intents.default()
intents.message_content = True


client = commands.Bot(command_prefix='!', intents=intents)

# Define the send_message() function to handle sending responses
async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)    # Get a response based on the user message
        if is_private:                                     # Send the response as a private message or in the channel
            await message.author.send(response)
        else:
            await message.channel.send(response)

    except discord.Forbidden:   # Need to complete error handling as this except block is not adequate or final.
        print("Error: The bot doesn't have permission to send messages in the specified channel or to the user.")

    except discord.HTTPException:
        print("Error: Failed to send the message due to an HTTP error.")

    except Exception as error:
        print(f"An error occurred: {type(error).__name__}: {error}")


def run_discord_bot():
    @client.event
    async def on_ready():
        print(f'Connected and ready to use. Logged in as {client.user.name}')

    # Define the on_message() event handler
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')  # prints the information to the console (helps with debugging)

        if user_message.startswith('?'):
            user_message = user_message[1:].strip()
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)


