import discord
from discord.ext import commands
import asyncio
import os

# CONFIGURAÇÃO
ID_CATEGORIA_CARRINHO = 1504149916249886833 # Categoria onde vai criar carrinho/ticket
ID_CARGO_ATENDENTE = 1500251010461863977 # Cargo Dono👑 que vai ver os tickets
CHAVE_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== FUNÇÃO PRA CRIAR CARRINHO COM PRODUTO =====
async def criar_carrinho_produto(interaction: discord.Interaction, produto: str, valor: str):
    await interaction.response.defer(ephemeral=True)
    
    guild = interaction.guild
    user = interaction.user
    
    # Checa se já tem carrinho aberto
    for channel in guild.text_channels:
        if channel.name == f"carrinho-{user.name}".lower():
            embed = discord.Embed(
                title=f"🛒 Pedido Adicionado - {produto}",
                description=f"**Valor:** {valor}\n\n**Chave Pix:**\n```{CHAVE_PIX}```\n\nManda o comprovante aqui nesse canal.",
                color=discord.Color.green()
            )
            await channel.send(content=user.mention, embed=embed)
            return await interaction.followup.send(f"Você já tem um carrinho aberto: {channel.mention}\nAdicionei seu pedido lá.", ephemeral=True)
    
    categoria = guild.get_channel(ID_CATEGORIA_CARRINHO)
    cargo = guild.get_role(ID_CARGO_ATENDENTE)
    
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, attach_files=True),
        cargo: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
    }
    
    nome_canal = f"carrinho-{user.name}".lower()
    
    canal = await guild.create_text_channel(
        name=nome_canal,
        category=categoria,
        overwrites=overwrites
    )
    
    embed = discord.Embed(
        title=f"🛒 Pedido - {produto}",
        description=f"**Valor:** {valor}\n\n**Chave Pix:**\n```{CHAVE_PIX}```\n\n**Próximos passos:**\n1. Pague o valor acima no Pix\n2. Mande o comprovante aqui nesse canal\n3. Aguarde nossa equipe confirmar\n\nEntrega rápida via DM após confirmação.",
        color=discord.Color.gold()
    )
    embed.set_footer(text="Use os botões abaixo pra gerenciar o carrinho")
    
    await canal.send(content=f"{user.mention} {cargo.mention}", embed=embed, view=CarrinhoView())
    await interaction.followup.send(f"Carrinho criado com seu pedido: {canal.mention}", ephemeral=True)

# ===== VIEWS DE PAGAMENTO - CRIAM CARRINHO AUTO =====
class PacksView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="HUD 3 Dedos - R$ 13,58", style=discord.ButtonStyle.blurple, custom_id="pack_hud3")
    async def hud3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await criar_carrinho_produto(interaction, "HUD 3 Dedos", "R$ 13,58")
    
    @discord.ui.button(label="HUD 4 Dedos - R$ 27,67", style=discord.ButtonStyle.blurple, custom_id="pack_hud4")
    async def hud4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await criar_carrinho_produto(interaction, "HUD 4 Dedos", "R$ 27,67")
    
    @discord.ui.button(label="Sensi + HUD - R$ 41,71", style=discord.ButtonStyle.blurple, custom_id="pack_sensi")
    async def sensi(self, interaction: discord.Interaction, button: discord.ui.Button):
        await criar_carrinho_produto(interaction, "Sensi + HUD", "R$ 41,71")
    
    @discord.ui.button(label="Completo - R$ 91,20", style=discord.ButtonStyle.blurple, custom_id="pack_completo")
    async def completo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await criar_carrinho_produto(interaction, "Completo", "R$ 91,20")

class ContasView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Conta Nível 15 - R$ 1,50", style=discord.ButtonStyle.green, custom_id="conta_nv15")
    async def conta15(self, interaction: discord.Interaction, button: discord.ui.Button):
        await criar_carrinho_produto(interaction, "Conta Nível 15", "R$ 1,50")
    
    @discord.ui.button(label="Conta Nível 20 - R$ 1,50", style=discord.ButtonStyle.green, custom_id="conta_nv20")
    async def conta20(self, interaction: discord.Interaction, button: discord.ui.Button):
        await criar_carrinho_produto(interaction, "Conta Nível 20", "R$ 1,50")

class HologramaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Comprar Holograma - R$ 2,50", style=discord.ButtonStyle.gray, emoji="💎", custom_id="comprar_holograma")
    async def comprar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await criar_carrinho_produto(interaction, "Pack Holograma Pro", "R$ 2,50")

class PescocoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Comprar HS Pescoço - R$ 1,00", style=discord.ButtonStyle.green, custom_id="comprar_pescoco")
    async def comprar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await criar_carrinho_produto(interaction, "HS Pescoço OFC", "R$ 1,00")

class PeitoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Comprar HS Peito - R$ 2,00", style=discord.ButtonStyle.green, custom_id="comprar_peito")
    async def comprar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await criar_carrinho_produto(interaction, "HS Peito OFC", "R$ 2,00")

# ===== SISTEMA DE CARRINHO =====
class CarrinhoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Finalizar Carrinho", style=discord.ButtonStyle.green, emoji="✅", custom_id="finalizar_carrinho")
    async def finalizar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Fechando carrinho em 5 segundos...", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()

    @discord.ui.button(label="Cancelar Carrinho", style=discord.ButtonStyle.red, emoji="❌", custom_id="cancelar_carrinho")
    async def cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Cancelando carrinho em 3 segundos...", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.channel.delete()

# ===== SISTEMA DE TICKET =====
class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Suporte", description="Tirar dúvidas", emoji="❓"),
            discord.SelectOption(label="Compra", description="Problemas com compra", emoji="🛒"),
            discord.SelectOption(label="Denúncia", description="Denunciar usuário", emoji="🚨")
        ]
        super().__init__(placeholder="Clique aqui para ver as opções", min_values=1, max_values=1, options=options, custom_id="select_ticket")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        guild = interaction.guild
        user = interaction.user
        categoria_escolhida = self.values[0]
        
        for channel in guild.text_channels:
            if channel.name.startswith(f"ticket-{user.name}".lower()):
                return await interaction.followup.send(f"Você já tem um ticket aberto: {channel.mention}", ephemeral=True)
        
        categoria = guild.get_channel(ID_CATEGORIA_CARRINHO)
        cargo = guild.get_role(ID_CARGO_ATENDENTE)
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, attach_files=True),
            cargo: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }
        
        nome_canal = f"ticket-{categoria_escolhida.lower()}-{user.name}".lower()
        
        canal = await guild.create_text_channel(
            name=nome_canal,
            category=categoria,
            overwrites=overwrites
        )
        
        embed = discord.Embed(
            title=f"🎫 Ticket - {categoria_escolhida}",
            description=f"Olá {user.mention}! Você abriu um ticket de **{categoria_escolhida}**.\n\nDescreva seu problema detalhadamente que nossa equipe vai te atender em breve.",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Use o botão abaixo para fechar o ticket")
        
        view = discord.ui.View(timeout=None)
        btn_fechar = discord.ui.Button(label="Fechar Ticket", style=discord.ButtonStyle.red, emoji="🔒", custom_id="fechar_ticket")
        
        async def fechar_callback(interaction_btn: discord.Interaction):
            await interaction_btn.response.send_message("Fechando ticket em 3 segundos...", ephemeral=True)
            await asyncio.sleep(3)
            await interaction_btn.channel.delete()
        
        btn_fechar.callback = fechar_callback
        view.add_item(btn_fechar)
        
        await canal.send(content=f"{user.mention} {cargo.mention}", embed=embed, view=view)
        await interaction.followup.send(f"Ticket criado: {canal.mention}", ephemeral=True)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())# ===== COMANDOS DE VENDA =====
@bot.tree.command(name="packs", description="Mostra os packs disponíveis")
async def packs(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📦 Packs Disponíveis",
        description="**Escolha seu pack abaixo:**\n\nClicou = carrinho criado automático com seu pedido!",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, view=PacksView())

@bot.tree.command(name="contas", description="Mostra as contas disponíveis")
async def contas(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎮 Contas Disponíveis",
        description="**Escolha sua conta abaixo:**\n\nClicou = carrinho criado automático!",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, view=ContasView())

@bot.tree.command(name="holograma", description="Pack Holograma Pro")
async def holograma(interaction: discord.Interaction):
    embed = discord.Embed(
        title="💎 Pack Holograma Pro",
        description="**Valor: R$ 2,50**\n\nClique no botão abaixo pra comprar. Carrinho abre sozinho!",
        color=discord.Color.purple()
    )
    await interaction.response.send_message(embed=embed, view=HologramaView())

@bot.tree.command(name="pescoco", description="HS Pescoço OFC")
async def pescoco(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎯 HS Pescoço OFC",
        description="**Valor: R$ 1,00**\n\nClique no botão abaixo pra comprar. Carrinho abre sozinho!",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, view=PescocoView())

@bot.tree.command(name="peito", description="HS Peito OFC")
async def peito(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎯 HS Peito OFC",
        description="**Valor: R$ 2,00**\n\nClique no botão abaixo pra comprar. Carrinho abre sozinho!",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, view=PeitoView())

@bot.tree.command(name="carrinho", description="Abre um carrinho vazio")
async def carrinho(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    guild = interaction.guild
    user = interaction.user
    
    for channel in guild.text_channels:
        if channel.name == f"carrinho-{user.name}".lower():
            return await interaction.followup.send(f"Você já tem um carrinho aberto: {channel.mention}", ephemeral=True)
    
    categoria = guild.get_channel(ID_CATEGORIA_CARRINHO)
    cargo = guild.get_role(ID_CARGO_ATENDENTE)
    
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, attach_files=True),
        cargo: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
    }
    
    nome_canal = f"carrinho-{user.name}".lower()
    
    canal = await guild.create_text_channel(
        name=nome_canal,
        category=categoria,
        overwrites=overwrites
    )
    
    embed = discord.Embed(
        title="🛒 Carrinho Vazio",
        description=f"Olá {user.mention}! Seu carrinho foi criado.\n\nUse os comandos `/packs`, `/contas`, etc pra adicionar produtos ou fale o que deseja comprar.\n\n**Chave Pix:**\n```{CHAVE_PIX}```",
        color=discord.Color.gold()
    )
    
    await canal.send(content=f"{user.mention} {cargo.mention}", embed=embed, view=CarrinhoView())
    await interaction.followup.send(f"Carrinho criado: {canal.mention}", ephemeral=True)

@bot.tree.command(name="ticket", description="Abre um ticket de suporte")
async def ticket(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎫 Sistema de Tickets",
        description="Selecione abaixo a categoria do seu ticket:",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, view=TicketView(), ephemeral=True)

@bot.tree.command(name="painel", description="Painel com todos os produtos [ADM]")
async def painel(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Sem permissão.", ephemeral=True)
    
    embed = discord.Embed(
        title="🛍️ Painel de Vendas DNZX",
        description="**Bem-vindo à loja DNZX!**\n\nClique nos botões abaixo pra comprar. O carrinho abre automático com seu pedido!",
        color=discord.Color.gold()
    )
    
    # Cria view com todos os produtos
    view = discord.ui.View(timeout=None)
    
    # Botões de Pack
    btn_pack1 = discord.ui.Button(label="HUD 3 Dedos - R$ 13,58", style=discord.ButtonStyle.blurple, custom_id="painel_pack1")
    btn_pack2 = discord.ui.Button(label="HUD 4 Dedos - R$ 27,67", style=discord.ButtonStyle.blurple, custom_id="painel_pack2")
    btn_pack3 = discord.ui.Button(label="Completo - R$ 91,20", style=discord.ButtonStyle.blurple, custom_id="painel_pack3")
    
    async def pack_callback(interaction_btn: discord.Interaction):
        if interaction_btn.data["custom_id"] == "painel_pack1":
            await criar_carrinho_produto(interaction_btn, "HUD 3 Dedos", "R$ 13,58")
        elif interaction_btn.data["custom_id"] == "painel_pack2":
            await criar_carrinho_produto(interaction_btn, "HUD 4 Dedos", "R$ 27,67")
        elif interaction_btn.data["custom_id"] == "painel_pack3":
            await criar_carrinho_produto(interaction_btn, "Completo", "R$ 91,20")
    
    btn_pack1.callback = pack_callback
    btn_pack2.callback = pack_callback
    btn_pack3.callback = pack_callback
    
    view.add_item(btn_pack1)
    view.add_item(btn_pack2)
    view.add_item(btn_pack3)
    
    await interaction.response.send_message(embed=embed, view=view)

# ===== COMANDO DE CUPOM =====
@bot.tree.command(name="cupom", description="Aplica um cupom de desconto no carrinho")
async def cupom(interaction: discord.Interaction, codigo: str):
    if not interaction.channel.name.startswith("carrinho-"):
        return await interaction.response.send_message("Use esse comando dentro de um carrinho.", ephemeral=True)
    
    codigo = codigo.upper()
    
    if codigo not in CUPONS:
        return await interaction.response.send_message(f"❌ Cupom `{codigo}` inválido ou expirado.", ephemeral=True)
    
    if interaction.channel.id in carrinhos_com_cupom:
        return await interaction.response.send_message("❌ Você já usou um cupom nesse carrinho.", ephemeral=True)
    
    desconto = CUPONS[codigo]
    
    # Pega a última mensagem do bot com valor
    async for msg in interaction.channel.history(limit=20):
        if msg.author == bot.user and msg.embeds:
            embed_antigo = msg.embeds[0]
            if "Valor:" in embed_antigo.description:
                # Extrai valor
                linhas = embed_antigo.description.split("\n")
                for linha in linhas:
                    if "Valor:" in linha:
                        valor_str = linha.split("**Valor:** ")[1].split("\n")[0]
                        valor_num = float(valor_str.replace("R$ ", "").replace(",", "."))
                        valor_novo = valor_num * (1 - desconto / 100)
                        
                        # Marca cupom como usado
                        carrinhos_com_cupom[interaction.channel.id] = codigo
                        
                        # Edita embed com desconto
                        embed_novo = discord.Embed(
                            title=embed_antigo.title,
                            description=f"**Valor Original:** R$ {valor_num:.2f}\n**Cupom {codigo}:** -{desconto}%\n**Valor com Desconto:** R$ {valor_novo:.2f}\n\n**Chave Pix:**\n```{CHAVE_PIX}```\n\n1. Pague o valor com desconto\n2. Mande o comprovante aqui\n3. Aguarde confirmação",
                            color=discord.Color.green()
                        )
                        embed_novo.set_footer(text=f"Cupom {codigo} aplicado com sucesso!")
                        
                        await msg.edit(embed=embed_novo)
                        return await interaction.response.send_message(f"✅ Cupom `{codigo}` aplicado! {desconto}% de desconto.", ephemeral=True)
    
    await interaction.response.send_message("❌ Não achei nenhum pedido nesse carrinho pra aplicar desconto.", ephemeral=True)

# Comando pra ADM criar cupom
@bot.tree.command(name="criarcupom", description="Cria um cupom de desconto [ADM]")
async def criarcupom(interaction: discord.Interaction, codigo: str, desconto: int):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Só ADM pode criar cupom.", ephemeral=True)
    
    if desconto < 1 or desconto > 99:
        return await interaction.response.send_message("❌ Desconto deve ser entre 1 e 99%.", ephemeral=True)
    
    CUPONS[codigo.upper()] = desconto
    await interaction.response.send_message(f"✅ Cupom `{codigo.upper()}` criado com {desconto}% de desconto!", ephemeral=True)

# ===== EVENTOS =====
@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos")
    except Exception as e:
        print(e)

# Registra as views persistentes
@bot.event
async def setup_hook():
    bot.add_view(PacksView())
    bot.add_view(ContasView())
    bot.add_view(HologramaView())
    bot.add_view(PescocoView())
    bot.add_view(PeitoView())
    bot.add_view(CarrinhoView())
    bot.add_view(TicketView())

bot.run(os.getenv("DISCORD_TOKEN"))
