import discord
from discord.ext import commands
import asyncio
from collections import defaultdict

# ===== IDS CONFIGURADOS =====
ID_CANAL_PAGAMENTO = 1500110296402886687
ID_CARGO_ATENDENTE = 1500251010461863977
ID_CATEGORIA_CARRINHO = 1504149916249886833

# -------- CONFIG DO BOT --------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Dicionário pra guardar o carrinho de cada user
carrinhos = defaultdict(list)

# -------- FUNÇÃO DO CARRINHO --------
async def add_carrinho(interaction: discord.Interaction, produto: str, preco: float):
    user_id = interaction.user.id
    carrinhos[user_id].append({"nome": produto, "preco": preco})

    total = sum(item["preco"] for item in carrinhos[user_id])
    lista_itens = "\n".join([f"• {item['nome']} - R$ {item['preco']:.2f}" for item in carrinhos[user_id]])

    embed = discord.Embed(
        title="🛒 Seu Carrinho",
        description=f"{lista_itens}\n\n**Total: R$ {total:.2f}**",
        color=discord.Color.green()
    )

    class CarrinhoView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=300)

        @discord.ui.button(label="Finalizar Compra", style=discord.ButtonStyle.success, emoji="✅")
        async def finalizar(self, interaction: discord.Interaction, button: discord.ui.Button):
            total_final = sum(item["preco"] for item in carrinhos[user_id])
            itens_final = "\n".join([f"• {item['nome']} - R$ {item['preco']:.2f}" for item in carrinhos[user_id]])

            canal_pagamento = bot.get_channel(ID_CANAL_PAGAMENTO)
            if canal_pagamento:
                embed_pedido = discord.Embed(
                    title="📦 Novo Pedido",
                    description=f"**Cliente:** {interaction.user.mention}\n"
                                f"**ID:** `{interaction.user.id}`\n\n"
                                f"**Itens:**\n{itens_final}\n\n"
                                f"**Total: R$ {total_final:.2f}**",
                    color=discord.Color.blue()
                )
                await canal_pagamento.send(content=f"<@&{ID_CARGO_ATENDENTE}>", embed=embed_pedido)

            embed_pix = discord.Embed(
                title="💰 Pagamento via PIX",
                description=f"**Itens:**\n{itens_final}\n\n"
                            f"**Total a pagar: R$ {total_final:.2f}**\n\n"
                            f"Chave PIX: `sua_chave_pix_aqui`\n"
                            f"Nome: DNZX STORE\n\n"
                            f"Após pagar, envie o comprovante aqui na DM do bot.",
                color=discord.Color.gold()
            )

            carrinhos[user_id].clear()
            await interaction.response.edit_message(embed=embed_pix, view=None)

        @discord.ui.button(label="Limpar Carrinho", style=discord.ButtonStyle.danger, emoji="🗑️")
        async def limpar(self, interaction: discord.Interaction, button: discord.ui.Button):
            carrinhos[user_id].clear()
            await interaction.response.edit_message(
                embed=discord.Embed(title="🛒 Carrinho Limpo", description="Todos os itens foram removidos.", color=discord.Color.red()),
                view=None
            )

    await interaction.response.send_message(embed=embed, view=CarrinhoView(), ephemeral=True)

# -------- COMANDO /PREMIUM --------
class PremiumSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="PAINEL MONITE 1 DIA", description="R$ 19,00 | Estoque: 198", value="monite_1d"),
            discord.SelectOption(label="PAINEL MONITE 7 DIAS", description="R$ 39,90 | Estoque: 198", value="monite_7d"),
            discord.SelectOption(label="PAINEL MONITE 30 DIAS", description="R$ 89,90 | Estoque: 199", value="monite_30d"),
            discord.SelectOption(label="PAINEL MONITE 1 DIA PRO", description="R$ 27,90 | Estoque: 199", value="monite_1d_pro"),
            discord.SelectOption(label="PAINEL MONITE 7 DIAS PRO", description="R$ 59,90 | Estoque: 199", value="monite_7d_pro"),
            discord.SelectOption(label="PAINEL MONITE 30 DIAS PRO", description="R$ 99,90 | Estoque: 199", value="monite_30d_pro"),
        ]
        super().__init__(placeholder="Selecione o painel", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        precos = {
            "monite_1d": 19.00, "monite_7d": 39.90, "monite_30d": 89.90,
            "monite_1d_pro": 27.90, "monite_7d_pro": 59.90, "monite_30d_pro": 99.90
        }
        nomes = {
            "monite_1d": "PAINEL MONITE 1 DIA", "monite_7d": "PAINEL MONITE 7 DIAS", "monite_30d": "PAINEL MONITE 30 DIAS",
            "monite_1d_pro": "PAINEL MONITE 1 DIA PRO", "monite_7d_pro": "PAINEL MONITE 7 DIAS PRO", "monite_30d_pro": "PAINEL MONITE 30 DIAS PRO"
        }
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class PremiumView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PremiumSelect())

@bot.tree.command(name="premium", description="Comprar Painel Monite")
async def premium(interaction: discord.Interaction):
    embed = discord.Embed(title="💎 Painéis Monite", description="Selecione seu plano abaixo:", color=discord.Color.purple())
    await interaction.response.send_message(embed=embed, view=PremiumView())

# -------- COMANDO /PROXY --------
class ProxySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="PROXY IOS 1 DIA", description="R$ 6,00 | Estoque: 25", value="proxy_1d"),
            discord.SelectOption(label="PROXY IOS 7 DIAS", description="R$ 22,00 | Estoque: 27", value="proxy_7d"),
            discord.SelectOption(label="PROXY IOS 30 DIAS", description="R$ 48,00 | Estoque: 25", value="proxy_30d"),
        ]
        super().__init__(placeholder="Selecione o proxy", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        precos = {"proxy_1d": 6.00, "proxy_7d": 22.00, "proxy_30d": 48.00}
        nomes = {"proxy_1d": "PROXY IOS 1 DIA", "proxy_7d": "PROXY IOS 7 DIAS", "proxy_30d": "PROXY IOS 30 DIAS"}
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class ProxyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ProxySelect())

@bot.tree.command(name="proxy", description="Comprar Proxy iOS")
async def proxy(interaction: discord.Interaction):
    embed = discord.Embed(title="🌐 Proxy iOS", description="Selecione seu plano abaixo:", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed, view=ProxyView())

# -------- COMANDO /HG --------
class HgSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="HG 1 DIA", description="R$ 10,00 | Estoque: 100", value="hg_1d"),
            discord.SelectOption(label="HG 7 DIAS", description="R$ 30,00 | Estoque: 100", value="hg_7d"),
            discord.SelectOption(label="HG 10 DIAS", description="R$ 35,00 | Estoque: 30", value="hg_10d"),
            discord.SelectOption(label="HG 30 DIAS", description="R$ 98,00 | Estoque: 15", value="hg_30d"),
        ]
        super().__init__(placeholder="Selecione o plano HG", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        precos = {"hg_1d": 10.00, "hg_7d": 30.00, "hg_10d": 35.00, "hg_30d": 98.00}
        nomes = {"hg_1d": "HG 1 DIA", "hg_7d": "HG 7 DIAS", "hg_10d": "HG 10 DIAS", "hg_30d": "HG 30 DIAS"}
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class HgView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HgSelect())

@bot.tree.command(name="hg", description="Comprar HG")
async def hg(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚡ Planos HG",
        description="Selecione seu plano abaixo:",
        color=discord.Color.orange()
    )
    await interaction.response.send_message(embed=embed, view=HgView())

# -------- COMANDO /HOLOGRAMA --------
class HologramaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Comprar Holograma - R$ 2,50", style=discord.ButtonStyle.gray, emoji="💎")
    async def comprar_holograma(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_carrinho(interaction, "Pack Holograma Pro", 2.50)

@bot.tree.command(name="holograma", description="Comprar Pack Holograma Pro")
async def holograma(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎮 Pack Holograma Pro",
        description="**Otimize sua gameplay no iOS**\n\n"
                    "✅ Sensibilidade de precisão testada\n"
                    "✅ HUD limpo pra melhor visão\n"
                    "✅ Config de rede pra ping baixo\n"
                    "✅ Tutorial de tracking e puxada\n"
                    "✅ Suporte incluso\n\n"
                    "**Preço: R$ 2,50**\n\n"
                    "Após pagar, envie o comprovante na DM do bot",
        color=discord.Color.dark_grey()
    )
    await interaction.response.send_message(embed=embed, view=HologramaView())# -------- COMANDO /PACKS --------
class PacksSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="PACK SENSI PRO", description="R$ 8,00 | Estoque: 50", value="pack_sensi"),
            discord.SelectOption(label="PACK HUD CUSTOM", description="R$ 5,00 | Estoque: 50", value="pack_hud"),
            discord.SelectOption(label="PACK FULL iOS", description="R$ 12,00 | Estoque: 50", value="pack_full"),
        ]
        super().__init__(placeholder="Selecione o pack", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        precos = {"pack_sensi": 8.00, "pack_hud": 5.00, "pack_full": 12.00}
        nomes = {"pack_sensi": "PACK SENSI PRO", "pack_hud": "PACK HUD CUSTOM", "pack_full": "PACK FULL iOS"}
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class PacksView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PacksSelect())

@bot.tree.command(name="packs", description="Comprar Packs de Config")
async def packs(interaction: discord.Interaction):
    embed = discord.Embed(title="📦 Packs de Config", description="Selecione seu pack abaixo:", color=discord.Color.teal())
    await interaction.response.send_message(embed=embed, view=PacksView())

# -------- COMANDO /CONTAS --------
class ContasSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="CONTA FF LVL 50", description="R$ 25,00 | Estoque: 10", value="conta_lvl50"),
            discord.SelectOption(label="CONTA FF VETERANA", description="R$ 80,00 | Estoque: 5", value="conta_vet"),
            discord.SelectOption(label="CONTA FF FULL SKIN", description="R$ 150,00 | Estoque: 3", value="conta_fullskin"),
        ]
        super().__init__(placeholder="Selecione a conta", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        precos = {"conta_lvl50": 25.00, "conta_vet": 80.00, "conta_fullskin": 150.00}
        nomes = {"conta_lvl50": "CONTA FF LVL 50", "conta_vet": "CONTA FF VETERANA", "conta_fullskin": "CONTA FF FULL SKIN"}
        await add_carrinho(interaction, nomes[self.values[0]], precos[self.values[0]])

class ContasView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ContasSelect())

@bot.tree.command(name="contas", description="Comprar Contas")
async def contas(interaction: discord.Interaction):
    embed = discord.Embed(title="👤 Contas Free Fire", description="Selecione a conta abaixo:", color=discord.Color.dark_red())
    await interaction.response.send_message(embed=embed, view=ContasView())

# -------- COMANDO /PESCOCO --------
class PescocoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Comprar Pescoço - R$ 3,50", style=discord.ButtonStyle.blurple, emoji="🎯")
    async def comprar_pescoco(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_carrinho(interaction, "Pack Pescoço", 3.50)

@bot.tree.command(name="pescoco", description="Comprar Pack Pescoço")
async def pescoco(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎯 Pack Pescoço",
        description="**Config otimizada pra mira no pescoço**\n\n"
                    "✅ Sensibilidade ajustada\n"
                    "✅ HUD personalizado\n"
                    "✅ Tutorial incluso\n"
                    "✅ Suporte incluso\n\n"
                    "**Preço: R$ 3,50**",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, view=PescocoView())

# -------- COMANDO /PEITO --------
class PeitoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Comprar Peito - R$ 3,50", style=discord.ButtonStyle.blurple, emoji="🎯")
    async def comprar_peito(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_carrinho(interaction, "Pack Peito", 3.50)

@bot.tree.command(name="peito", description="Comprar Pack Peito")
async def peito(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎯 Pack Peito",
        description="**Config otimizada pra mira no peito**\n\n"
                    "✅ Sensibilidade ajustada\n"
                    "✅ HUD personalizado\n"
                    "✅ Tutorial incluso\n"
                    "✅ Suporte incluso\n\n"
                    "**Preço: R$ 3,50**",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, view=PeitoView())

# -------- COMANDO /TICKET --------
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.green, emoji="🎫")
    async def abrir_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        categoria = bot.get_channel(ID_CATEGORIA_CARRINHO)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.get_role(ID_CARGO_ATENDENTE): discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        canal = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=categoria,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="🎫 Ticket Aberto",
            description=f"Olá {interaction.user.mention}, descreva sua dúvida ou problema.\nUm atendente responderá em breve.",
            color=discord.Color.green()
        )

        class FecharTicket(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)

            @discord.ui.button(label="Fechar Ticket", style=discord.ButtonStyle.red, emoji="🔒")
            async def fechar(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.channel.delete()

        await canal.send(content=f"{interaction.user.mention} <@&{ID_CARGO_ATENDENTE}>", embed=embed, view=FecharTicket())
        await interaction.response.send_message(f"Ticket criado: {canal.mention}", ephemeral=True)

@bot.tree.command(name="ticket", description="Abrir um ticket de suporte")
async def ticket(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎫 Sistema de Tickets",
        description="Clique no botão abaixo para abrir um ticket e falar com o suporte.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, view=TicketView())

# -------- EVENTO ON_READY --------
@bot.event
async def on_ready():
    print(f"Bot logado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizado {len(synced)} comandos")
    except Exception as e:
        print(e)

# -------- RODAR O BOT --------
bot.run(os.getenv("DISCORD_TOKEN"))
