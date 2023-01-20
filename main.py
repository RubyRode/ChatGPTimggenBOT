import os
import discord
import flask
import openai
from dotenv import load_dotenv

openai.organization = "TOKEN"
OPENAI_BOT_TOKEN = "TOKEN"
DISCORD_BOT_TOKEN = "TOKEN"
openai.api_key = OPENAI_BOT_TOKEN

# response = openai.Image.create(
#   prompt="A cute baby sea otter",
#   n=2,
#   size="1024x1024"
# )
#
# image_url = response['data'][0]['url']
# print(image_url)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# prev_message = None


@client.event
async def on_message(message):
    if message.content.startswith("!txt_comp"):
        try:
            prompt = message.content[10:]  # Get the text after !complete_text
            completions = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=2048, n=1,stop=None)
            text = completions.choices[0].text
            await message.reply(text)
        except openai.OpenAIError as e:
            await message.channel.send("Error: " + str(e))

    if message.content.startswith("!img_gen"):
        try:
            prompt = message.content[9:]  # Get the text after !generate_image
            await message.reply(f"Image: '{prompt}' is in process...")
            response = openai.Image.create(prompt=prompt, n=2, size="1024x1024")
            await message.reply(response['data'][0]['url'])
        except openai.OpenAIError as e:
            await message.channel.send("Error: " + str(e))

    if message.content.startswith("!help_gpt") and message.author != client.user:
        try:
            await message.reply("!help_gpt - show this message\n!img_gen - generate an image 1024x1024 from prompt\n!txt_comp - generate a text from request.")
        except openai.OpenAIError as e:
            await message.channel.send("Error: " + str(e))


client.run(DISCORD_BOT_TOKEN)
