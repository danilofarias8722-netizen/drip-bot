import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CANAL_COMPROVANTES = 1500110296402886687
DONO_ID = 1498844150202896446

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} online!')

@bot.command()
async def holograma(ctx):
    embed = discord.Embed(title="🔥 HOLOGRAMA FF - R$ 2,50 🔥", description="✅ Entrega automática via ID\n⚡ Pix na hora = item na hora", color=0x00ff00)
    embed.add_field(name="💰 Pix", value="`d3169985-198b-4ca4-a119-de573d45d2ee`", inline=False)
    embed.add_field(name="📩 Como comprar", value="1. Faz o Pix\n2. Manda o comprovante na MINHA DM\n3. Envia teu ID do FF", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def packs(ctx):
    embed = discord.Embed(title="📦 PACKS", color=0x0099ff)
    embed.add_field(name="Valores", value="**1 dia:** R$ 15,00\n**3 dias:** R$ 30,00\n**7 dias:** R$ 45,00\n**30 dias:** R$ 100,00", inline=False)
    embed.add_field(name="Pix", value="`d3169985-198b-4ca4-a119-de573d45d2ee`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def premium(ctx):
    embed = discord.Embed(title="👑 PREMIUM", color=0xffd700)
    embed.add_field(name="Valores", value="**1 dia:** R$ 15,96\n**7 dias:** R$ 38,69\n**30 dias:** R$ 68,98", inline=False)
    embed.add_field(name="Vantagens", value="✅ 10% off em tudo\n✅ Suporte prioritário", inline=False)
    embed.add_field(name="Pix", value="`d3169985-198b-4ca4-a119-de573d45d2ee`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def conta(ctx):
    embed = discord.Embed(title="🎮 CONTAS FF", color=0x9966ff)
    embed.add_field(name="Valores", value="**Nível 15:** R$ 1,50\n**Nível 20:** R$ 1,50", inline=False)
    embed.add_field(name="Pix", value="`d3169985-198b-4ca4-a119-de573d45d2ee`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def proxy(ctx):
    embed = discord.Embed(title="🌐 PROXY", color=0xff6600)
    embed.add_field(name="Valores", value="**1 dia:** R$ 18,48\n**7 dias:** R$ 36,16\n**30 dias:** R$ 71,00", inline=False)
    embed.add_field(name="Pix", value="`d3169985-198b-4ca4-a119-de573d45d2ee`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ticket(ctx):
    await ctx.send(f"📩 **SUPORTE**\nAbre o ticket mandando tua dúvida na minha DM!\nPix: `d3169985-198b-4ca4-a119-de573d45d2ee`")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        canal = bot.get_channel(CANAL_COMPROVANTES)
        if canal:
            dono = await bot.fetch_user(DONO_ID) # Pega teu usuário
            embed = discord.Embed(title="💰 NOVO COMPROVANTE RECEBIDO", description=f"**Cliente:** {message.author.mention}\n**ID:** `{message.author.id}`", color=0xffd700)
            embed.set_image(url=message.attachments[0].url)
            await canal.send(content=f"{dono.mention} @here", embed=embed) # 👈 TE MARCA AQUI
            await message.channel.send("✅ Comprovante recebido! Já vou conferir e te chamar.")

    await bot.process_commands(message)

bot.run(TOKEN)
