@bot.tree.command(name="loja", description="Abre a loja")
async def loja(interaction: discord.Interaction):
    await interaction.response.send_message("Loja aberta!")
