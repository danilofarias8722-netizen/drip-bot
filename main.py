@bot.event
async def on_ready():
    print('Bot online!')
    await bot.tree.sync()  # ESSA LINHA REGISTRA O /loja
    print('Comandos registrados!')
