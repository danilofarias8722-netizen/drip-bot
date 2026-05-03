import discord
from discord.ui import View, Button, Select
import asyncio
from discord.ext import commands
import os # Importante pro Railway

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# CONFIGURAÇÕES - JÁ CONFIGURADO COM SEUS IDs
CARGO_STAFF_ID = 1500251010461863977
SEU_ID_DISCORD = 1498844150202896446
ID_CANAL_COMPROVANTES = 1500110296402886687
PIX = "d3169985-198b-4ca4-a119-de573d45d2ee"

# Guarda o último produto que o cliente clicou
ultimo_produto = {}

@bot.event
async def on_ready():
    print(f'Bot online: {bot.user}')

# COMANDO TICKET
@bot.command()
async def ticket(ctx):
    embed = discord.Embed(
        title="Central de atendimento dnzx store",
        description="Após solicitar um atendimento, aguarde um integrante da equipe responde-lo(a). O atendimento é realizado de forma privada, contudo, somente integrantes da equipe terá acesso ao atendimento. Tenha ciência que a nossa equipe não se encontra presente 24 horas por dia, contudo, dentro dos horários citados acima nossa equipe se encontra disponibilizada a atende-lo(a).\n\nSelecione uma opção abaixo para abrir um ticket",
        color=discord.Color.blue()
    )

    select = Select(
        placeholder="Clique aqui para ver as opções",
        options=[
            discord.SelectOption(label="Suporte", description="Tirar dúvidas", emoji="❓"),
            discord.SelectOption(label="Compra", description="Problemas com compra", emoji="🛒"),
            discord.SelectOption(label="Denúncia", description="Denunciar usuário", emoji="🚨")
        ],
        custom_id="abrir_ticket_select"
    )

    view = View()
    view.add_item(select)
    await ctx.send(embed=embed, view=view)

# COMANDO LOJA - AGORA IGUAL AO SEU PRINT COM OS BOTÕES
@bot.command()
async def loja(ctx):
    embed = discord.Embed(
        title="🛒 Realizar Compra",
        description="**Escolha seu pack abaixo:**\n\n✅ Entrega rápida via DM\n✅ Arquivos de referência em.png\n✅ 100% seguro\n\nClique no botão do pack que deseja comprar:\n\nApós pagar, envie o comprovante na DM do bot",
        color=discord.Color.dark_grey()
    )

    view = View()
    view.add_item(Button(label="HUD 3 Dedos - R$ 13,58", style=discord.ButtonStyle.blurple, custom_id="hud_3"))
    view.add_item(Button(label="HUD 4 Dedos - R$ 27,67", style=discord.ButtonStyle.blurple, custom_id="hud_4"))
    view.add_item(Button(label="Sensi + HUD - R$ 41,71", style=discord.ButtonStyle.blurple, custom_id="sensi_hud"))
    view.add_item(Button(label="Completo - R$ 91,20", style=discord.ButtonStyle.blurple, custom_id="pack_completo"))

    await ctx.send(embed=embed, view=view)

# COMANDO CONTAS
@bot.command()
async def contas(ctx):
    embed = discord.Embed(
        title="🛒 Realizar Compra",
        description="**Escolha sua conta abaixo:**\n\n✅ Entrega rápida via DM\n✅ Conta full acesso\n✅ 100% segura\n\nClique no botão da conta que deseja comprar:\n\nApós pagar, envie o comprovante na DM do bot",
        color=discord.Color.dark_grey()
    )

    view = View()
    view.add_item(Button(label="Conta Nível 15 - R$ 1,50", style=discord.ButtonStyle.green, custom_id="comprar_nv15"))
    view.add_item(Button(label="Conta Nível 20 - R$ 1,50", style=discord.ButtonStyle.green, custom_id="comprar_nv20"))

    await ctx.send(embed=embed, view=view)

# COMANDO PACKS - MESMA COISA DO!LOJA
@bot.command()
async def packs(ctx):
    embed = discord.Embed(
        title="🛒 Realizar Compra",
        description="**Escolha seu pack abaixo:**\n\n✅ Entrega rápida via DM\n✅ Arquivos de referência em.png\n✅ 100% seguro\n\nClique no botão do pack que deseja comprar:\n\nApós pagar, envie o comprovante na DM do bot",
        color=discord.Color.dark_grey()
    )

    view = View()
    view.add_item(Button(label="HUD 3 Dedos - R$ 13,58", style=discord.ButtonStyle.blurple, custom_id="hud_3"))
    view.add_item(Button(label="HUD 4 Dedos - R$ 27,67", style=discord.ButtonStyle.blurple, custom_id="hud_4"))
    view.add_item(Button(label="Sensi + HUD - R$ 41,71", style=discord.ButtonStyle.blurple, custom_id="sensi_hud"))
    view.add_item(Button(label="Completo - R$ 91,20", style=discord.ButtonStyle.blurple, custom_id="pack_completo"))

    await ctx.send(embed=embed, view=view)

# SISTEMA DE COMPROVANTE NA DM - MANDA PRO CANAL 1500110296402886687
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Se for DM e tiver anexo = comprovante
    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        canal_comprovantes = bot.get_channel(ID_CANAL_COMPROVANTES)

        # Pega o produto que o cara comprou
        produto_info = ultimo_produto.get(message.author.id)

        if not produto_info:
            produto_nome = "⚠️ Cliente não clicou no botão"
            produto_valor = "Verificar com cliente"
            produto_id = "SEM-ID"
            cor = discord.Color.orange()
        else:
            produto_nome = produto_info['nome']
            produto_valor = produto_info['valor']
            produto_id = produto_info['id']
            cor = discord.Color.yellow()

        embed = discord.Embed(
            title="📸 Novo Comprovante Recebido",
            description=f"**Cliente:** {message.author.mention}\n**ID:** {message.author.id}\n**Produto:** {produto_nome}\n**Valor:** R$ {produto_valor}\n**ID:** {produto_id}",
            color=cor
        )
        embed.set_image(url=message.attachments[0].url)
        embed.set_footer(text="Clique em Aprovar ou Reprovar")

        view = View()
        view.add_item(Button(label="✅ Aprovar", style=discord.ButtonStyle.green, custom_id=f"aprovar_{message.author.id}"))
        view.add_item(Button(label="❌ Reprovar", style=discord.ButtonStyle.red, custom_id=f"reprovar_{message.author.id}"))

        await canal_comprovantes.send(embed=embed, view=view)

        if not produto_info:
            await message.reply("**⚠️ ATENÇÃO!**\n\nVocê enviou o comprovante mas não clicou no botão do produto antes.\n\n**Informe aqui na DM qual produto você comprou** ou abra um ticket com `!ticket` pra resolvermos.")
        else:
            await message.reply("**✅ Comprovante recebido!**\n\nAguarde a confirmação do pagamento. Você será notificado em breve.")

    await bot.process_commands(message)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:

        # LÓGICA DO TICKET
        if interaction.data["custom_id"] == "abrir_ticket_select":
            categoria = interaction.data["values"][0]

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                interaction.guild.get_role(CARGO_STAFF_ID): discord.PermissionOverwrite(view_channel=True, send_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
            }

            canal = await interaction.guild.create_text_channel(
                name=f"ticket-{interaction.user.name}",
                overwrites=overwrites,
                reason=f"Ticket aberto por {interaction.user}"
            )

            view = View()
            view.add_item(Button(label="Fechar Ticket", style=discord.ButtonStyle.red, emoji="🔒", custom_id="fechar_ticket"))

            embed = discord.Embed(
                title=f"Ticket - {categoria}",
                description=f"Olá {interaction.user.mention}, explique seu problema.\nA equipe já foi notificada.",
                color=discord.Color.green()
            )

            await canal.send(embed=embed, view=view)
            await interaction.response.send_message(f"Ticket criado em {canal.mention}", ephemeral=True)

        # LÓGICA FECHAR TICKET
        elif interaction.data["custom_id"] == "fechar_ticket":
            await interaction.response.defer()
            try:
                await interaction.channel.send("Fechando ticket em 5 segundos...")
                await asyncio.sleep(5)
                await interaction.channel.delete(reason=f"Ticket fechado por {interaction.user}")
            except discord.Forbidden:
                await interaction.followup.send("**❌ ERRO: Sem permissão pra apagar canal!**", ephemeral=True)
            except Exception as e:
                await interaction.followup.send(f"**❌ Erro:** `{e}`", ephemeral=True)

        # SALVA QUAL PRODUTO O CARA QUER COMPRAR
        elif interaction.data["custom_id"] == "comprar_nv15":
            ultimo_produto[interaction.user.id] = {"nome": "Conta Nível 15", "valor": "1,50", "id": "CONTA-LVL15"}
            await interaction.response.send_message(
                f"**🛒 Conta Nível 15 - R$ 1,50**\n\n**PIX:** {PIX}\n**Valor:** R$ 1,50\n\nApós pagar, mande o comprovante aqui na DM que eu já libero sua conta!",
                ephemeral=True
            )

        elif interaction.data["custom_id"] == "comprar_nv20":
            ultimo_produto[interaction.user.id] = {"nome": "Conta Nível 20", "valor": "1,50", "id": "CONTA-LVL20"}
            await interaction.response.send_message(
                f"**🛒 Conta Nível 20 - R$ 1,50**\n\n**PIX:** {PIX}\n**Valor:** R$ 1,50\n\nApós pagar, mande o comprovante aqui na DM que eu já libero sua conta!",
                ephemeral=True
            )

        elif interaction.data["custom_id"] == "hud_3":
            ultimo_produto[interaction.user.id] = {"nome": "HUD 3 Dedos", "valor": "13,58", "id": "HUD-3D"}
            await interaction.response.send_message(
                f"**🛒 HUD 3 Dedos - R$ 13,58**\n\n**PIX:** {PIX}\n**Valor:** R$ 13,58\n\nApós pagar, mande o comprovante aqui na DM que eu já libero o pack!",
                ephemeral=True
            )

        elif interaction.data["custom_id"] == "hud_4":
            ultimo_produto[interaction.user.id] = {"nome": "HUD 4 Dedos", "valor": "27,67", "id": "HUD-4D"}
            await interaction.response.send_message(
                f"**🛒 HUD 4 Dedos - R$ 27,67**\n\n**PIX:** {PIX}\n**Valor:** R$ 27,67\n\nApós pagar, mande o comprovante aqui na DM que eu já libero o pack!",
                ephemeral=True
            )

        elif interaction.data["custom_id"] == "sensi_hud":
            ultimo_produto[interaction.user.id] = {"nome": "Sensi + HUD", "valor": "41,71", "id": "SENSI-HUD"}
            await interaction.response.send_message(
                f"**🛒 Sensi + HUD - R$ 41,71**\n\n**PIX:** {PIX}\n**Valor:** R$ 41,71\n\nApós pagar, mande o comprovante aqui na DM que eu já libero o pack!",
                ephemeral=True
            )

        elif interaction.data["custom_id"] == "pack_completo":
            ultimo_produto[interaction.user.id] = {"nome": "Completo", "valor": "91,20", "id": "PACK-COMPLETO"}
            await interaction.response.send_message(
                f"**🛒 Completo - R$ 91,20**\n\n**PIX:** {PIX}\n**Valor:** R$ 91,20\n\nApós pagar, mande o comprovante aqui na DM que eu já libero o pack!",
                ephemeral=True
            )

        # APROVAR COMPROVANTE
        elif interaction.data["custom_id"].startswith("aprovar_"):
            cliente_id = int(interaction.data["custom_id"].split("_")[1])
            cliente = await bot.fetch_user(cliente_id)

            try:
                await cliente.send("**✅ Pagamento Aprovado!**\n\nSeu pedido foi confirmado. Em instantes você receberá o produto no seu privado.\n\nObrigado pela compra!")
                await interaction.response.send_message(f"**✅ Aprovado!**\n\nCliente {cliente.mention} foi notificado. Lembre de enviar o produto na DM dele.", ephemeral=True)
                embed = interaction.message.embeds[0]
                embed.color = discord.Color.green()
                embed.title = "✅ Comprovante Aprovado"
                await interaction.message.edit(embed=embed, view=None)
            except:
                await interaction.response.send_message("**❌ Erro:** Não consegui mandar DM pro cliente. Ele pode estar com DM fechada.", ephemeral=True)

        # REPROVAR COMPROVANTE
        elif interaction.data["custom_id"].startswith("reprovar_"):
            cliente_id = int(interaction.data["custom_id"].split("_")[1])
            cliente = await bot.fetch_user(cliente_id)

            try:
                await cliente.send("**❌ Pagamento Reprovado**\n\nNão conseguimos confirmar seu pagamento.\n\nMotivos possíveis:\n• Comprovante inválido\n• Valor incorreto\n• Pagamento não identificado\n\nAbra um ticket com `!ticket` para resolver.")
                await interaction.response.send_message(f"**❌ Reprovado!**\n\nCliente {cliente.mention} foi notificado.", ephemeral=True)
                embed = interaction.message.embeds[0]
                embed.color = discord.Color.red()
                embed.title = "❌ Comprovante Reprovado"
                await interaction.message.edit(embed=embed, view=None)
            except:
                await interaction.response.send_message("**❌ Erro:** Não consegui mandar DM pro cliente.", ephemeral=True)

# PEGA O TOKEN DAS VARIABLES DO RAILWAY - SEGURO
bot.run(os.getenv("DISCORD_TOKEN"))
