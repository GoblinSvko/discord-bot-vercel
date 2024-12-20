import discord
import os
import re
import urllib.parse
from discord.ext import commands

# Token bota zaciągany z zmiennej środowiskowej
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Konfiguracja intencji bota
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Funkcja do konwersji linków
def convert_to_acbuy(kakobuy_link):
    match = re.search(r"url=([^\s&]+)", kakobuy_link)
    if match:
        encoded_weidian_url = match.group(1)
        decoded_weidian_url = urllib.parse.unquote(encoded_weidian_url)
        print(f"Zdekodowany URL: {decoded_weidian_url}")

        # Wyciąganie `itemID`
        item_id_match = re.search(r"itemID=(\d+)", decoded_weidian_url)
        if item_id_match:
            item_id = item_id_match.group(1)
            return f"https://www.allchinabuy.com/en/page/buy/?nTag=Home-search&from=search-input&_search=url&position=&url=weidian.com%252Fitem.html%253FitemID%253D{item_id}"
    return None


@bot.event
async def on_ready():
    print(f"Bot zalogowany jako {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    kakobuy_links = re.findall(r"https?://www\.kakobuy\.com/item/details\?url=[^\s]+", message.content)
    for kakobuy_link in kakobuy_links:
        acbuy_link = convert_to_acbuy(kakobuy_link)
        if acbuy_link:
            await message.reply(f"Oto Twój link ACBUY: {acbuy_link}")
        else:
            await message.reply("Nie udało się przekonwertować linku.")

    await bot.process_commands(message)


# Funkcja uruchamiająca bota na platformie Vercel
async def handler(request):
    if not bot.is_ready():
        await bot.start(DISCORD_TOKEN)
    return {"statusCode": 200, "body": "Bot działa!"}
