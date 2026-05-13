import discord
from discord.ext import commands
import asyncio

# ===== IDS CONFIGURADOS =====
ID_CANAL_PAGAMENTO = 1500110296402886687
ID_CARGO_ATENDENTE = 1500251010461863977
ID_CATEGORIA_CARRINHO = 1504149916249886833

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== CARRINHO =====
carrinhos = {}

class CarrinhoView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="Finalizar Compra", style=discord.ButtonStyle.green, emoji="🛒")
    async def finalizar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Esse carrinho não é seu!", ephemeral=True)
        
        total = sum(item['preco'] for item in carrinhos[self.user_id])
        itens = "\n".join([f"• {item['nome']} - R$ {item['preco']:.2f}" for item in carrinhos[self.user_id]])
        
        canal_pagamento = bot.get_channel(ID_CANAL_PAGAMENTO)
        embed = discord.Embed(title="🛒 Novo Pedido", description=f"**Cliente:** {interaction.user.mention}\n\n**Itens:**\n{itens}\n\n**Total: R$ {total:.2f}**", color=discord.Color.green())
        await canal_pagamento.send(content=f"<@&{ID_CARGO_ATENDENTE}>", embed=embed)
        
        del carrinhos[self.user_id]
        await interaction.response.edit_message(content="✅ Pedido enviado! Um atendente vai te chamar no privado.", embed=None, view=None)

    @discord.ui.button(label="Limpar Carrinho", style=discord.ButtonStyle.red, emoji="🗑️")
    async def limpar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Esse carrinho não é seu!", ephemeral=True)
        del carrinhos[self.user_id]
        await interaction.response.edit_message(content="🗑️ Carrinho limpo!", embed=None, view=None)

# ===== FUNÇÃO PRA ADD NO CARRINHO =====
async def add_carrinho(interaction, nome, preco):
    if interaction.user.id not in carrinhos:
        carrinhos[interaction.user.id] = []
    
    carrinhos[interaction.user.id].append({"nome": nome, "preco": preco})
    total = sum(item['preco'] for item in carrinhos[interaction.user.id])
    itens = "\n".join([f"• {item['nome']} - R$ {item['preco']:.2f}" for item in carrinhos[interaction.user.id]])
    
    embed = discord.Embed(title="🛒 Seu Carrinho", description=f"{itens}\n\n**Total: R$ {total:.2f}**", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed, view=CarrinhoView(interaction.user.id), ephemeral=True)

# ===== VIEWS DOS PRODUTOS =====
class PacksView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="HUD 3 Dedos - R$ 13,58", style=discord.ButtonStyle.blurple)
    async def hud3(self, i, b): await add_carrinho(i, "HUD 3 Dedos", 13.58)
    
    @discord.ui.button(label="HUD 4 Dedos - R$ 27,67", style=discord.ButtonStyle.blurple)
    async def hud4(self, i, b): await add_carrinho(i, "HUD 4 Dedos", 27.67)
    
    @discord.ui.button(label="Sensi + HUD - R$ 41,71", style=discord.ButtonStyle.blurple)
    async def sensi(self, i, b): await add_carrinho(i, "Sensi + HUD", 41.71)
    
    @discord.ui.button(label="Completo - R$ 91,20", style=discord.ButtonStyle.blurple)
    async def completo(self, i, b): await add_carrinho(i, "Completo", 91.20)
    
    @discord.ui.button(label="HS Pescoço - R$ 1,00", style=discord.ButtonStyle.gray)
    async def pescoco(self, i, b): await add_carrinho(i, "HS Pescoço", 1.00)
    
    @discord.ui.button(label="HS Peito - R$ 2,00", style=discord.ButtonStyle.gray)
    async def peito(self, i, b): await add_carrinho(i, "HS Peito", 2.00)

class ContasView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Conta Nível 15 - R$ 1,50", style=discord.ButtonStyle.green)
    async def lvl15(self, i, b): await add_carrinho(i, "Conta Nível 15", 1.50)
    
    @discord.ui.button(label="Conta Nível 20 - R$ 1,50", style=discord.ButtonStyle.green)
    async def lvl20(self, i, b): await add_carrinho(i, "Conta Nível 20", 1.50)

class HgView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="HG 1 DIA - R$ 10,00", style=discord.ButtonStyle.red)
    async def hg1(self, i, b): await add_carrinho(i, "HG 1 DIA", 10.00)
    
    @discord.ui.button(label="HG 7 DIAS - R$ 30,00", style=discord.ButtonStyle.red)
    async def hg7(self, i, b): await add_carrinho(i, "HG 7 DIAS", 30.00)
    
    @discord.ui.button(label="HG 10 DIAS - R$ 35,00", style=discord.ButtonStyle.red)
    async def hg10(self, i, b): await add_carrinho(i, "HG 10 DIAS", 35.00)
    
    @discord.ui.button(label="HG 30 DIAS - R$ 98,00", style=discord.ButtonStyle.red)
    async def hg30(self, i, b): await add_carrinho(i, "HG 30 DIAS", 98.00)

class ProxyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="PROXY 1 DIA - R$ 6,00", style=discord.ButtonStyle.blurple)
    async def prox1(self, i, b): await add_carrinho(i, "PROXY IOS 1 DIA", 6.00)
    
    @discord.ui.button(label="PROXY 7 DIAS - R$ 22,00", style=discord.ButtonStyle.blurple)
    async def prox7(self, i, b): await add_carrinho(i, "PROXY IOS 7 DIAS", 22.00)
    
    @discord.ui.button(label="PROXY 30 DIAS - R$ 48,00", style=discord.ButtonStyle.blurple)
    async def prox30(self, i, b): await add_carrinho(i, "PROXY IOS 30 DIAS", 48.00)

class PremiumView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="MONITE 1D BA - R$ 19,00", style=discord.ButtonStyle.green)
    async def mon1ba(self, i, b): await add_carrinho(i, "PAINEL MONITE 1 DIA BA", 19.00)
    
    @discord.ui.button(label="MONITE 7D BA - R$ 39,90", style=discord.ButtonStyle.green)
    async def mon7ba(self, i, b): await add_carrinho(i, "PAINEL MONITE 7 DIAS BA", 39.90)
    
    @discord.ui.button(label="MONITE 30D BA - R$ 89,90", style=discord.ButtonStyle.green)
    async def mon30ba(self, i, b): await add_carrinho(i, "PAINEL MONITE 30 DIAS BA", 89.90)
    
    @discord.ui.button(label="MONITE 1D PR - R$ 27,90", style=discord.ButtonStyle.green)
    async def mon1pr(self, i, b): await add_carrinho(i, "PAINEL MONITE 1 DIA PR", 27.90)
    
    @discord.ui.button(label="MONITE 7D PR - R$ 59,90", style=discord.ButtonStyle.green)
    async def mon7pr(self, i, b): await add_carrinho(i, "PAINEL MONITE 7 DIAS PR", 59.90)
    
    @discord.ui.button(label="MONITE 30D PR - R$ 99,90", style=discord.ButtonStyle.green)
    async def mon30pr(self, i, b): await add_carrinho(i, "PAINEL MONITE 30 DIAS PR", 99.90)

class HologramaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Holograma - R$ 2,50", style=discord.ButtonStyle.blurple)
    async def holo(self, i, b): await add_carrinho(i, "Holograma", 2.50)

class FecharTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Fechar Ticket", style=discord.ButtonStyle.red, emoji="🔒")
    async def fechar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Fechando ticket em 5 segundos...", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()@bot.event
async def on_ready():
    print(f'Bot online: {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Sync {len(synced)} comandos')
    except Exception as e:
        print(e)

# ===== COMANDOS =====
@bot.tree.command(name="packs", description="Ver packs de HUD e HS")
async def packs(interaction: discord.Interaction):
    embed = discord.Embed(title="📦 PACKS DNZX STORE", description="Escolha seu pack abaixo:", color=discord.Color.gold())
    await interaction.response.send_message(embed=embed, view=PacksView())

@bot.tree.command(name="contas", description="Ver contas disponíveis")
async def contas(interaction: discord.Interaction):
    embed = discord.Embed(title="👤 CONTAS DNZX STORE", description="Escolha sua conta:", color=discord.Color.green())
    await interaction.response.send_message(embed=embed, view=ContasView())

@bot.tree.command(name="hg", description="Ver planos HG")
async def hg(interaction: discord.Interaction):
    embed = discord.Embed(title="🎯 PLANOS HG", description="Escolha seu plano:", color=discord.Color.red())
    await interaction.response.send_message(embed=embed, view=HgView())

@bot.tree.command(name="proxy", description="Ver planos PROXY IOS")
async def proxy(interaction: discord.Interaction):
    embed = discord.Embed(title="🌐 PROXY IOS", description="Escolha seu plano:", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed, view=ProxyView())

@bot.tree.command(name="premium", description="Ver painéis MONITE")
async def premium(interaction: discord.Interaction):
    embed = discord.Embed(title="💎 PAINÉIS PREMIUM", description="Escolha seu painel:", color=discord.Color.purple())
    await interaction.response.send_message(embed=embed, view=PremiumView())

@bot.tree.command(name="holograma", description="Comprar Holograma")
async def holograma(interaction: discord.Interaction):
    embed = discord.Embed(title="✨ HOLOGRAMA", description="Clique para adicionar ao carrinho:", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed, view=HologramaView())

@bot.tree.command(name="pescoco", description="Comprar HS Pescoço")
async def pescoco(interaction: discord.Interaction):
    await add_carrinho(interaction, "HS Pescoço", 1.00)

@bot.tree.command(name="peito", description="Comprar HS Peito")
async def peito(interaction: discord.Interaction):
    await add_carrinho(interaction, "HS Peito", 2.00)

@bot.tree.command(name="ticket", description="Abrir um ticket de suporte")
async def ticket(interaction: discord.Interaction):
    guild = interaction.guild
    user = interaction.user
    cargo = guild.get_role(ID_CARGO_ATENDENTE)
    categoria = guild.get_channel(ID_CATEGORIA_CARRINHO)

    for channel in guild.text_channels:
        if channel.name == f"ticket-{user.name}".lower():
            return await interaction.response.send_message(f"Você já tem um ticket aberto: {channel.mention}", ephemeral=True)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, attach_files=True),
        cargo: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
    }

    nome_canal = f"ticket-{user.name}".lower()
    canal_ticket = await guild.create_text_channel(name=nome_canal, category=categoria, overwrites=overwrites)
    
    embed = discord.Embed(title="🎫 Ticket de Suporte Aberto", description=f"Olá {user.mention}!\n\nDescreva seu problema que um atendente vai te ajudar.\n\nPara fechar o ticket, use o botão abaixo.", color=discord.Color.blue())
    embed.set_footer(text="DNZX STORE")
    
    await canal_ticket.send(content=f"{user.mention} {cargo.mention}", embed=embed, view=FecharTicketView())
    await interaction.response.send_message(f"Ticket criado! {canal_ticket.mention}", ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))
