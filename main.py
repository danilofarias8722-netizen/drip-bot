import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime
import os  # ← ADICIONA ESSA LINHA AQUI

# ===== CONFIGURAÇÕES DNZX STORE =====
NOME_LOJA = "DNZX STORE"
ID_CATEGORIA_TICKETS = 1504149916249886833
ID_CARGO_STAFF = 1500251010461863977
CHAVE_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# ===== VIEWS PIX E PAGAMENTO =====
class PixView(discord.ui.View):
    def __init__(self, produto: str, valor: float, user: discord.User):
        super().__init__(timeout=None)
        self.produto = produto
        self.valor = valor
        self.user = user

    @discord.ui.button(label="Código copia e cola", style=discord.ButtonStyle.gray, emoji="📋")
    async def copiar_codigo(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
        await interaction.response.send_message(f"**Chave PIX Copia e Cola:**\n`{CHAVE_PIX}`", ephemeral=True)

    @discord.ui.button(label="Cancelar Compra", style=discord.ButtonStyle.red, emoji="❌")
    async def cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode cancelar.", ephemeral=True)
        await interaction.response.send_message("❌ Compra cancelada. Fechando ticket em 5 segundos...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

class PagamentoView(discord.ui.View):
    def __init__(self, produto: str, valor: float, user: discord.User):
        super().__init__(timeout=None)
        self.produto = produto
        self.valor = valor
        self.user = user

    @discord.ui.button(label="Pagar com Pix", style=discord.ButtonStyle.gray, emoji="💠")
    async def pagar_pix(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
        
        embed = discord.Embed(
            title="Pagamento via PIX criado",
            description=f"**Código copia e cola**\n```{CHAVE_PIX}```\n\n**Produto:** {self.produto}\n**Valor:** R$ {self.valor:.2f}\n\n⚠️ **Após pagar:**\n1. Envie o comprovante AQUI no ticket\n2. Aguarde a confirmação da staff\n3. Receba seu produto na DM",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        embed.set_footer(text=f"© {NOME_LOJA} #5K - 2026 | Hoje às {datetime.now().strftime('%H:%M')}")
        
        view = PixView(self.produto, self.valor, self.user)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Pagar com Cartão", style=discord.ButtonStyle.gray, emoji="💳", disabled=True)
    async def pagar_cartao(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ Pagamento com cartão temporariamente indisponível. Use PIX.", ephemeral=True)

    @discord.ui.button(label="Pagar com Saldo", style=discord.ButtonStyle.gray, emoji="💰", disabled=True)
    async def pagar_saldo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ Sistema de saldo em manutenção. Use PIX.", ephemeral=True)

    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.gray, emoji="⬅️")
    async def voltar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
        
        embed = discord.Embed(
            title="Detalhes da sua compra",
            description=f"Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real. Você pode **alterar quantidades**, **aplicar cupons** ou **concluir sua compra** usando os botões abaixo.\n\n**Produtos no Carrinho (1x)**\n`1x {self.produto} | R$ {self.valor:.2f}`\n\n**Valor à vista**\n`R$ {self.valor:.2f}`",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        embed.set_author(name=f"{NOME_LOJA} APP", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.set_footer(text=f"{NOME_LOJA} #5K | Hoje às {datetime.now().strftime('%H:%M')}")
        
        view = CarrinhoView(self.produto, self.valor, self.user)
        await interaction.response.edit_message(embed=embed, view=view)# ===== VIEW CARRINHO =====
class CarrinhoView(discord.ui.View):
    def __init__(self, produto: str, valor: float, user: discord.User):
        super().__init__(timeout=None)
        self.produto = produto
        self.valor = valor
        self.user = user

    @discord.ui.button(label="Ir para pagamento", style=discord.ButtonStyle.green, emoji="💳")
    async def pagamento(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
        
        embed = discord.Embed(
            title="Escolha a sua forma de pagamento",
            description=f"Dê uma última olhada na sua compra e escolha como deseja pagar para concluir de forma prática.",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        embed.set_footer(text=f"{NOME_LOJA} #5K | Hoje às {datetime.now().strftime('%H:%M')}")
        
        view = PagamentoView(self.produto, self.valor, self.user)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Editar quantidade", style=discord.ButtonStyle.blurple, emoji="📝")
    async def editar_qtd(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
        await interaction.response.send_message("❌ No momento só aceitamos 1 unidade por compra. Para comprar mais, abra outro carrinho.", ephemeral=True)

    @discord.ui.button(label="Usar cupom de desconto", style=discord.ButtonStyle.gray, emoji="🎟️")
    async def cupom(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Só o dono do carrinho pode usar.", ephemeral=True)
        await interaction.response.send_message("❌ Sistema de cupons em manutenção. Fale com a staff.", ephemeral=True)

# ===== FUNÇÃO CRIAR TICKET =====
async def criar_ticket(interaction: discord.Interaction, produto: str, valor: float):
    guild = interaction.guild
    categoria = guild.get_channel(ID_CATEGORIA_TICKETS)
    
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        guild.get_role(ID_CARGO_STAFF): discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
    }
    
    canal = await guild.create_text_channel(
        name=f"🛒-{interaction.user.name}",
        category=categoria,
        overwrites=overwrites
    )
    
    embed = discord.Embed(
        title="Detalhes da sua compra",
        description=f"Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real. Você pode **alterar quantidades**, **aplicar cupons** ou **concluir sua compra** usando os botões abaixo.\n\n**Produtos no Carrinho (1x)**\n`1x {produto} | R$ {valor:.2f}`\n\n**Valor à vista**\n`R$ {valor:.2f}`",
        color=discord.Color.from_rgb(255, 0, 0)
    )
    embed.set_author(name=f"{NOME_LOJA} APP", icon_url=guild.icon.url if guild.icon else None)
    embed.set_footer(text=f"{NOME_LOJA} #5K | Hoje às {datetime.now().strftime('%H:%M')}")
    
    view = CarrinhoView(produto, valor, interaction.user)
    await canal.send(content=f"{interaction.user.mention} | <@&{ID_CARGO_STAFF}>", embed=embed, view=view)
    
    await interaction.response.send_message(f"✅ Ticket criado: {canal.mention}", ephemeral=True)

# ===== COMANDOS =====
@bot.tree.command(name="hg", description="Abrir loja do DNZX STORE")
async def hg(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"🛒 {NOME_LOJA} - VIPs",
        description="**Escolha um VIP abaixo:**\n\n🥉 **VIP Bronze** - R$ 5,00\n🥈 **VIP Prata** - R$ 10,00\n🥇 **VIP Ouro** - R$ 15,00\n💎 **VIP Diamante** - R$ 25,00",
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"{NOME_LOJA} | Sistema de vendas automático")
    
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="VIP Bronze", style=discord.ButtonStyle.green, custom_id="bronze"))
    view.add_item(discord.ui.Button(label="VIP Prata", style=discord.ButtonStyle.gray, custom_id="prata"))
    view.add_item(discord.ui.Button(label="VIP Ouro", style=discord.ButtonStyle.blurple, custom_id="ouro"))
    view.add_item(discord.ui.Button(label="VIP Diamante", style=discord.ButtonStyle.red, custom_id="diamante"))
    
    await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        custom_id = interaction.data["custom_id"]
        
        if custom_id == "bronze":
            await criar_ticket(interaction, "VIP Bronze", 5.00)
        elif custom_id == "prata":
            await criar_ticket(interaction, "VIP Prata", 10.00)
        elif custom_id == "ouro":
            await criar_ticket(interaction, "VIP Ouro", 15.00)
        elif custom_id == "diamante":
            await criar_ticket(interaction, "VIP Diamante", 25.00)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{NOME_LOJA} online! Logado como {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))
