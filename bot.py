import discord
import os

client = discord.Client()

# Funkcja wywoływana przez Vercel jako endpoint API
def handler(request, context)
    @client.event
    async def on_ready()
        print(f'Zalogowano jako {client.user}')

    @client.event
    async def on_message(message)
        if message.content.startswith('!ping')
            await message.channel.send('Pong!')

    # Token Discorda (przechowywany w zmiennych środowiskowych)
    token = os.getenv('DISCORD_TOKEN')
    client.run(token)

    return 'Bot uruchomiony na Vercel', 200