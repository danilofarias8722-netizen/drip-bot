@discord.ui.button(label="Comprar Drip Cliente", style=discord.ButtonStyle.green, emoji="💸")
async def comprar(self, interaction: discord.Interaction, button: Button):
    try:
        embed_dm = discord.Embed(title="💎 PAGAMENTO PIX - DRIP CLIENTE", color=0x00ff00)
        embed_dm.add_field(name="Chave PIX Copia e Cola", value="`d3169985-198b-4ca4-a119-de573d45d2ee`", inline=False)
        embed_dm.add_field(name="1 Dia", value="R$ 15,00", inline=True)
        embed_dm.add_field(name="3 Dias", value="R$ 25,00", inline=True)
        embed_dm.add_field(name="7 Dias", value="R$ 45,00", inline=True)
        embed_dm.set_footer(text="Depois de pagar, manda o print do comprovante aqui na DM")
        
        await interaction.user.send(embed=embed_dm)
        await interaction.response.send_message("Te chamei na DM! Confere lá 📩", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("Libera tua DM irmão", ephemeral=True)
