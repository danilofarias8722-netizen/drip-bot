import discord
from discord.ext import commands
import asyncio

# CONFIGURAÇÃO
ID_CATEGORIA_CARRINHO = 1504149916249886833 # Categoria onde vai criar carrinho/ticket
ID_CARGO_ATENDENTE = 1500251010461863977 # Cargo Dono👑 que vai ver os tickets
CHAVE_PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== VIEWS DE PAGAMENTO =====
class PacksView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="HUD 3 Dedos - R$ 13,58", style=discord.ButtonStyle.blurple, custom_id="pack_hud3")
    async def hud3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.enviar_pix(interaction, "HUD 3 Dedos", "R$ 13,58")
    
    @discord.ui.button(label="HUD 4 Dedos - R$ 27,67", style=discord.ButtonStyle.blurple, custom_id="pack_hud4")
    async def hud4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.enviar_pix(interaction, "HUD 4 Dedos", "R$ 27,67")
    
    @discord.ui.button(label="Sensi + HUD - R$ 41,71", style=discord.ButtonStyle.blurple, custom_id="pack_sensi")
    async def sensi(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.enviar_pix(interaction, "Sensi + HUD", "R$ 41,71")
    
    @discord.ui.button(label="Completo - R$ 91,20", style=discord.ButtonStyle.blurple, custom_id="pack_completo")
    async def completo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.enviar_pix(interaction, "Completo", "R$ 91,20")

    async def enviar_pix(self, interaction: discord.Interaction, produto: str, valor: str):
        embed = discord.Embed(
            title=f"💰 Pagamento - {produto}",
            description=f"**Valor:** {valor}\n\n**Chave Pix:**\n```{CHAVE_PIX}```\n\nApós pagar, envie o comprovante na DM do bot ou abra um carrinho com `/carrinho`",
            color=discord.Color.green()
        )
        embed.set_footer(text="Entrega rápida via DM após confirmação")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class ContasView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Conta Nível 15 - R$ 1,50", style=discord.ButtonStyle.green, custom_id="conta_nv15")
    async def conta15(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.enviar_pix(interaction, "Conta Nível 15", "R$ 1,50")
    
    @discord.ui.button(label="Conta Nível 20 - R$ 1,50", style=discord.ButtonStyle.green, custom_id="conta_nv20")
    async def conta20(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.enviar_pix(interaction, "Conta Nível 20", "R$ 1,50")

    async def enviar_pix(self, interaction: discord.Interaction, produto: str, valor: str):
        embed = discord.Embed(
            title=f"💰 Pagamento - {produto}",
            description=f"**Valor:** {valor}\n\n**Chave Pix:**\n```{CHAVE_PIX}```\n\nApós pagar, envie o comprovante na DM do bot ou abra um carrinho com `/carrinho`",
            color=discord.Color.green()
        )
        embed.set_footer(text="Entrega rápida via DM após confirmação")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class HologramaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Comprar Holograma - R$ 2,50", style=discord.ButtonStyle.gray, emoji="💎", custom_id="comprar_holograma")
    async def comprar(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💰 Pagamento - Pack Holograma Pro",
            description=f"**Valor:** R$ 2,50\n\n**Chave Pix:**\n```{CHAVE_PIX}```\n\nApós pagar, envie o comprovante na DM do bot ou abra um carrinho com `/carrinho`",
            color=discord.Color.green()
        )
        embed.set_footer(text="Entrega rápida via DM após confirmação")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class PescocoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Comprar HS Pescoço - R$ 1,00", style=discord.ButtonStyle.green, custom_id="comprar_pescoco")
    async def comprar(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💰 Pagamento - HS Pescoço OFC",
            description=f"**Valor:** R$ 1,00\n\n**Chave Pix:**\n```{CHAVE_PIX}```\n\nApós pagar, envie o comprovante na DM do bot ou abra um carrinho com `/carrinho`",
            color=discord.Color.green()
        )
        embed.set_footer(text="Entrega rápida via DM após confirmação")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class PeitoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Comprar HS Peito - R$ 2,00", style=discord.ButtonStyle.green, custom_id="comprar_peito")
    async def comprar(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💰 Pagamento - HS Peito OFC",
            description=f"**Valor:** R$ 2,00\n\n**Chave Pix:**\n```{CHAVE_PIX}```\n\nApós pagar, envie o comprovante na DM do bot ou abra um carrinho com `/carrinho`",
            color=discord.Color.green()
        )
        embed.set_footer(text="Entrega rápida via DM após confirmação")
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
@bot.tree.command(name="packs", description="Mostra os packs de HUD e sensi")
async def packs(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📦 Realizar Compra",
        description="**Escolha seu pack abaixo:**\n\n✅ Entrega rápida via DM\n✅ Pack vitalício\n✅ Suporte incluso\n\nClique no botão do pack que deseja comprar:",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, view=PacksView())

@bot.command(name="packs")
async def packs_prefix(ctx):
    embed = discord.Embed(
        title="📦 Realizar Compra",
        description="**Escolha seu pack abaixo:**\n\n✅ Entrega rápida via DM\n✅ Pack vitalício\n✅ Suporte incluso\n\nClique no botão do pack que deseja comprar:",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=PacksView())

@bot.tree.command(name="contas", description="Mostra as contas disponíveis")
async def contas(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛒 Realizar Compra",
        description="**Escolha sua conta abaixo:**\n\n✅ Entrega rápida via DM\n✅ Conta full acesso\n✅ 100% segura\n\nClique no botão da conta que deseja comprar:\n\nApós pagar, envie o comprovante na DM do bot",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, view=ContasView())

@bot.command(name="contas")
async def contas_prefix(ctx):
    embed = discord.Embed(
        title="🛒 Realizar Compra",
        description="**Escolha sua conta abaixo:**\n\n✅ Entrega rápida via DM\n✅ Conta full acesso\n✅ 100% segura\n\nClique no botão da conta que deseja comprar:\n\nApós pagar, envie o comprovante na DM do bot",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=ContasView())

@bot.tree.command(name="holograma", description="Mostra o Pack Holograma Pro")
async def holograma(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Pack Holograma Pro",
        description="**Otimize sua gameplay no iOS**\n\n✅ Sensibilidade de precisão testada\n✅ HUD limpo pra melhor visão\n✅ Config de rede pra ping baixo\n✅ Tutorial de tracking e puxada\n✅ Suporte incluso\n\n**Preço: R$ 2,50**\n\nApós pagar, envie o comprovante na DM do bot",
        color=discord.Color.dark_gray()
    )
    await interaction.response.send_message(embed=embed, view=HologramaView())

@bot.command(name="holograma")
async def holograma_prefix(ctx):
    embed = discord.Embed(
        title="🤖 Pack Holograma Pro",
        description="**Otimize sua gameplay no iOS**\n\n✅ Sensibilidade de precisão testada\n✅ HUD limpo pra melhor visão\n✅ Config de rede pra ping baixo\n✅ Tutorial de tracking e puxada\n✅ Suporte incluso\n\n**Preço: R$ 2,50**\n\nApós pagar, envie o comprovante na DM do bot",
        color=discord.Color.dark_gray()
    )
    await ctx.send(embed=embed, view=HologramaView())

@bot.tree.command(name="pescoco", description="Mostra o HS Pescoço OFC")
async def pescoco(interaction: discord.Interaction):
    embed = discord.Embed(
        title="💀 HS Pescoço OFC - R$ 1,00",
        description="**Pack de sensibilidade pra puxar pro HS**\n\n✅ Mira sobe direto pra cabeça\n✅ Mais taxa de capa\n✅ Config agressiva\n✅ Tutorial de puxada incluso\n\n**Valor único: R$ 1,00**\n\nApós pagar, envie o comprovante na DM do bot",
        color=discord.Color.light_gray()
    )
    await interaction.response.send_message(embed=embed, view=PescocoView())

@bot.command(name="pescoco")
async def pescoco_prefix(ctx):
    embed = discord.Embed(
        title="💀 HS Pescoço OFC - R$ 1,00",
        description="**Pack de sensibilidade pra puxar pro HS**\n\n✅ Mira sobe direto pra cabeça\n✅ Mais taxa de capa\n✅ Config agressiva\n✅ Tutorial de puxada incluso\n\n**Valor único: R$ 1,00**\n\nApós pagar, envie o comprovante na DM do bot",
        color=discord.Color.light_gray()
    )
    await ctx.send(embed=embed, view=PescocoView())

@bot.tree.command(name="peito", description="Mostra o HS Peito OFC")
async def peito(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎯 HS Peito OFC - R$ 2,00",
        description="**Pack de sensibilidade focada no peito**\n\n✅ Melhor dano consistente\n✅ Ideal pra quem erra a capa\n✅ Config testada no meta\n✅ Suporte pra ajustar\n\n**Valor único: R$ 2,00**\n\nApós pagar, envie o comprovante na DM do bot",
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed, view=PeitoView())

@bot.command(name="peito")
async def peito_prefix(ctx):
    embed = discord.Embed(
        title="🎯 HS Peito OFC - R$ 2,00",
        description="**Pack de sensibilidade focada no peito**\n\n✅ Melhor dano consistente\n✅ Ideal pra quem erra a capa\n✅ Config testada no meta\n✅ Suporte pra ajustar\n\n**Valor único: R$ 2,00**\n\nApós pagar, envie o comprovante na DM do bot",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed, view=PeitoView())

# ===== COMANDO TICKET =====
@bot.tree.command(name="ticket", description="Abre o painel de tickets")
async def ticket(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Central de atendimento dnzx store",
        description="Após solicitar um atendimento, aguarde um integrante da equipe responde-lo(a). O atendimento é realizado de forma privada, contudo, somente integrantes da equipe terá acesso ao atendimento. Tenha ciência que a nossa equipe não se encontra presente 24 horas por dia, contudo, dentro dos horários citados acima nossa equipe se encontra disponibilizada a atende-lo(a).\n\nSelecione uma opção abaixo para abrir um ticket",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, view=TicketView())

@bot.command(name="ticket")
async def ticket_prefix(ctx):
    embed = discord.Embed(
        title="Central de atendimento dnzx store",
        description="Após solicitar um atendimento, aguarde um integrante da equipe responde-lo(a). O atendimento é realizado de forma privada, contudo, somente integrantes da equipe terá acesso ao atendimento. Tenha ciência que a nossa equipe não se encontra presente 24 horas por dia, contudo, dentro dos horários citados acima nossa equipe se encontra disponibilizada a atende-lo(a).\n\nSelecione uma opção abaixo para abrir um ticket",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=TicketView())

# ===== SISTEMA DE CARRINHO =====
@bot.tree.command(name="carrinho", description="Abre um carrinho privado pra compra")
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
        title=f"🛒 Carrinho de {user.display_name}",
        description="Esse é seu carrinho privado.\n\n**Como funciona:**\n1. Fale o que deseja comprar\n2. Nossa equipe vai confirmar valor + Pix\n3. Após pagar, mande o comprovante aqui\n4. Entrega via DM\n\nUse os botões abaixo pra finalizar.",
        color=discord.Color.gold()
    )
    
    await canal.send(content=f"{user.mention} {cargo.mention}", embed=embed, view=CarrinhoView())
    await interaction.followup.send(f"Carrinho criado: {canal.mention}", ephemeral=True)

@bot.tree.command(name="fechar", description="Fecha o carrinho atual")
async def fechar(interaction: discord.Interaction):
    if interaction.channel.name.startswith("carrinho-"):
        await interaction.response.send_message("Fechando carrinho em 3 segundos...", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.channel.delete()
    else:
        await interaction.response.send_message("Use esse comando dentro de um carrinho.", ephemeral=True)

@bot.tree.command(name="add", description="Adiciona alguém no carrinho")
async def add(interaction: discord.Interaction, membro: discord.Member):
    if not interaction.channel.name.startswith("carrinho-"):
        return await interaction.response.send_message("Use esse comando dentro de um carrinho.", ephemeral=True)
    
    await interaction.channel.set_permissions(membro, view_channel=True, send_messages=True, read_message_history=True)
    await interaction.response.send_message(f"{membro.mention} foi adicionado ao carrinho.", ephemeral=True)

@bot.tree.command(name="remover", description="Remove alguém do carrinho")
async def remover(interaction: discord.Interaction, membro: discord.Member):
    if not interaction.channel.name.startswith("carrinho-"):
        return await interaction.response.send_message("Use esse comando dentro de um carrinho.", ephemeral=True)
    
    await interaction.channel.set_permissions(membro, overwrite=None)
    await interaction.response.send_message(f"{membro.mention} foi removido do carrinho.", ephemeral=True)

@bot.tree.command(name="painel", description="Envia o painel de abrir carrinho")
async def painel(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛒 Abrir Carrinho",
        description="Clique no botão abaixo pra abrir um carrinho privado e fazer sua compra com segurança.",
        color=discord.Color.green()
    )
    
    view = discord.ui.View(timeout=None)
    button = discord.ui.Button(label="Abrir Carrinho", style=discord.ButtonStyle.green, emoji="🛒", custom_id="abrir_carrinho_btn")
    button.callback = carrinho.callback
    view.add_item(button)
    
    await interaction.response.send_message(embed=embed, view=view)

# ===== EVENTOS =====
@bot.event
async def on_ready():
    bot.add_view(CarrinhoView())
    bot.add_view(PacksView())
    bot.add_view(ContasView())
    bot.add_view(HologramaView())
    bot.add_view(PescocoView())
    bot.add_view(PeitoView())
    bot.add_view(TicketView())
    
    view_painel = discord.ui.View(timeout=None)
    button = discord.ui.Button(label="Abrir Carrinho", style=discord.ButtonStyle.green, emoji="🛒", custom_id="abrir_carrinho_btn")
    button.callback = carrinho.callback
    view_painel.add_item(button)
    bot.add_view(view_painel)
    
    await bot.tree.sync()
    print(f'Bot {bot.user} online!')
    print(f'Categoria: {ID_CATEGORIA_CARRINHO}')
    print(f'Cargo Atendente: {ID_CARGO_ATENDENTE}')

# ===== INICIAR BOT =====
bot.run("SEU_TOKEN_AQUI")
