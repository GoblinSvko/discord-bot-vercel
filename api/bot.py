import discord
from discord.ext import commands
import re
import urllib.parse
from dotenv import load_dotenv
import os

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

# Pobieranie tokenu z pliku .env
TOKEN = os.getenv("DISCORD_TOKEN")

# Sprawdzanie, czy token jest poprawnie załadowany
if TOKEN is None:
    print("Token nie został załadowany! Sprawdź plik .env.")
    exit()

PREFIX = "!"

# Tworzenie instancji bota z odpowiednimi intentami
intents = discord.Intents.default()
intents.messages = True  # Włączanie intencji odczytu wiadomości
intents.message_content = True  # Konieczne dla odczytu treści wiadomości

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Funkcja do konwersji linku
def convert_to_acbuy(kakobuy_link):
    # Wyodrębnienie parametru 'url' z linku Kakobuy
    match = re.search(r"url=([^\s&]+)", kakobuy_link)
    if match:
        encoded_weidian_url = match.group(1)  # Zakodowany link
        decoded_weidian_url = urllib.parse.unquote(encoded_weidian_url)  # Dekodowanie linku
        print(f"Zdekodowany URL: {decoded_weidian_url}")  # Debug

        # Szukanie 'itemID' w zdekodowanym URL
        item_id_match = re.search(r"itemID=(\d+)", decoded_weidian_url)
        if item_id_match:
            item_id = item_id_match.group(1)
            print(f"Znaleziony itemID: {item_id}")  # Debug
            # Generowanie linku ACBUY
            acbuy_link = f"https://www.allchinabuy.com/en/page/buy/?nTag=Home-search&from=search-input&_search=url&position=&url=weidian.com%252Fitem.html%253FitemID%253D{item_id}"
            return acbuy_link
    return None

# Event: Wykrywanie wiadomości z linkiem Kakobuy
@bot.event
async def on_message(message):
    if message.author.bot:  # Ignorowanie wiadomości botów
        return

    print(f"Odebrano wiadomość: {message.content}")  # Debug

    # Sprawdzenie, czy wiadomość zawiera link Kakobuy
    kakobuy_links = re.findall(r"https?://www\.kakobuy\.com/item/details\?url=[^\s]+", message.content)
    print(f"Znalezione linki Kakobuy: {kakobuy_links}")  # Debug

    for kakobuy_link in kakobuy_links:
        acbuy_link = convert_to_acbuy(kakobuy_link)
        if acbuy_link:
            await message.reply(f"Oto Twój link ACBUY: {acbuy_link}")
        else:
            await message.reply("Nie udało się przekonwertować linku.")

    await bot.process_commands(message)  # Przetwarza komendy bota

# Uruchomienie bota
bot.run(TOKEN)
