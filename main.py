@bot.command()
@commands.has_permissions(administrator=True)
async def loja(ctx):
    if ctx.channel.id!= CANAL_VENDAS_ID:
        return await ctx.send("Use esse comando no canal de vendas!", delete_after=5)

    embed = discord.Embed(
        title="🛒 Realizar Compra",
        description="**Escolha seu pack abaixo:**\n\n✅ Entrega rápida via DM\n✅ Arquivos de referência em .png\n✅ 100% seguro\n\nClique no botão do pack que deseja comprar:",
        color=COR_EMBED
    )
    embed.set_footer(text="Após pagar, envie o comprovante na DM do bot")

    await ctx.send(embed=embed, view=ProdutoView())
    await ctx.message.delete()
