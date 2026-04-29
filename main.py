import discord
from discord import app_commands
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")
DONO_ID = 1498844150202896446
CHAVE_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class LojaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💸 Comprar Drip Cliente", style=discord.ButtonStyle.green, custom_id="comprar_drip")
    async def comprar(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed_dm = discord.Embed(
                title="💎 Pagamento Drip Cliente",
                description=f"**Chave PIX:** `{CHAVE_PIX}`\n\n**Valores:**\n1 Dia: R$ 15,00\n3 Dias: R$ 25,00\n7 Dias: R$ 45,00\n\n**Envie o comprovante AQUI nessa DM após pagar.**\nColoca na mensagem qual plano tu quer: 1, 3 ou 7 dias.",
                color=0x9b59b6
            )
            await interaction.user.send(embed=embed_dm)
            await interaction.response.send_message("Te chamei na DM! Confere lá ✅", ephemeral=True)
        except:
            await interaction.response.send_message("Não consegui te chamar na DM. Libera tua DM e tenta de novo!", ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(LojaView())
    await bot.tree.sync()
    print(f"Bot online: {bot.user}")
    print(f"Sincronizou {len(bot.tree.get_commands())} comando(s)")

@bot.tree.command(name="loja", description="Mostra os planos do Drip Cliente")
async def loja(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛒 LOJA DRIP CLIENTE",
        description="**Escolha teu plano:**",
        color=0x9b59b6
    )
    embed.add_field(name="📅 1 Dia", value="**R$ 15,00**", inline=True)
    embed.add_field(name="📅 3 Dias", value="**R$ 25,00**", inline=True)
    embed.add_field(name="📅 7 Dias", value="**R$ 45,00**", inline=True)
    embed.set_footer(text="Clique no botão abaixo para comprar")

    await interaction.response.send_message(embed=embed, view=LojaView())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Se for DM e tiver anexo = comprovante
    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        dono = await bot.fetch_user(DONO_ID)

        embed = discord.Embed(title="🚨 NOVO COMPROVANTE", color=0xe74c3c)
        embed.add_field(name="Cliente", value=f"**Nome:** {message.author.display_name}\n**User:** {message.author}\n**ID:** `{message.author.id}`", inline=False)
        embed.add_field(name="Mensagem", value=message.content or "Sem texto", inline=False)
        embed.set_image(url=message.attachments[0].url)
        embed.set_footer(text="Confirma o PIX e libera o acesso manualmente")

        await dono.send(embed=embed)
        await message.channel.send("✅ Comprovante recebido! O dono foi avisado e vai liberar teu acesso em breve.")

    await bot.process_commands(message)

bot.run(TOKEN)
