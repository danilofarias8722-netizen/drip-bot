import discord
from discord.ext import commands
from discord.ui import View, Button
import asyncio
import qrcode
import io
from datetime import datetime
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ================== CONFIGURAÇÕES - EDITA AQUI ==================
PIX = "d3169985-198b-4ca4-a119-de573d45d2ee" # SUA CHAVE PIX
ID_CANAL_COMPROVANTES = 1500110296402886687 # CANAL ONDE CHEGA O COMPROVANTE
ID_CANAL_LOGS = 1500110296402886687 # MESMO CANAL PRA LOGS
# ================================================================

# ARMAZENA PRODUTO DO CLIENTE
ultimo_produto = {}

# ARQUIVOS/TEXTOS DOS PRODUTOS - COLOCA OS SEUS AQUI
PRODUTOS_ENTREGA = {
    "HS-PEITO-200": "=== HS PEITO OFC ===\n\nSensibilidade:\nGeral: 100\nPonto Vermelho: 100\n2x: 100\n4x: 100\nAWM: 50\n\nTutorial:\n1. Cola tudo no FF\n2. Testa no treino\n3. Ajusta conforme sua pegada\n\nSuporte: abre ticket",
    "HS-PESCOCO-100": "=== HS PESCOCO OFC ===\n\nSensibilidade:\nGeral: 100\nPonto Vermelho: 100\n2x: 95\n4x: 90\nAWM: 50\n\nTutorial: Puxa pra cima que gruda na cabeça\n\nSuporte: abre ticket",
    "FF-PREMIUM-1D": "=== FF-PREMIUM 1 DIA ===\n\nChave: FF24H-DNZ-XYZ123\nDNS: 1.1.1.1 / 1.0.0.1\nAPN: timbrasil.br\n\nValidade: 24h após ativação\nTutorial: https://youtu.be/seu_video",
    "FF-PREMIUM-7D": "=== FF-PREMIUM 7 DIAS ===\n\nChave: FF7D-DNZ-XYZ123\nDNS: 1.1.1.1 / 1.0.0.1\nAPN: timbrasil.br\n\nValidade: 7 dias",
    "FF-PREMIUM-30D": "=== FF-PREMIUM 30 DIAS ===\n\nChave: FF30D-DNZ-XYZ123\nDNS: 1.1.1.1 / 1.0.0.1\nAPN: timbrasil.br\n\nValidade: 30 dias",
    "PROXY-1D": "=== PROXY IOS 1 DIA ===\n\nIP: 123.45.67.89\nPorta: 8080\nUsuário: dnzx\nSenha: 1234\n\nValidade: 24h",
    "PROXY-7D": "=== PROXY IOS 7 DIAS ===\n\nIP: 123.45.67.89\nPorta: 8080\nUsuário: dnzx\nSenha: 1234\n\nValidade: 7 dias",
    "PROXY-30D": "=== PROXY IOS 30 DIAS ===\n\nIP: 123.45.67.89\nPorta: 8080\nUsuário: dnzx\nSenha: 1234\n\nValidade: 30 dias",
    "HOLOGRAMA-250": "=== PACK HOLOGRAMA ===\n\nLink HUD: https://drive.google.com/seu_link\nSensi: 100 100 100 100 50\nTutorial: https://youtu.be/seu_video",
    "CONTA-LVL15": "=== CONTA NÍVEL 15 ===\n\nEmail: conta15@dnzx.com\nSenha: Dnzx@2026\nFacebook: Não vinculado\n\nTROCA TUDO AO RECEBER!",
    "CONTA-LVL20": "=== CONTA NÍVEL 20 ===\n\nEmail: conta20@dnzx.com\nSenha: Dnzx@2026\nFacebook: Não vinculado\n\nTROCA TUDO AO RECEBER!",
    "HUD-3D": "=== HUD 3 DEDOS ===\n\nLink: https://drive.google.com/seu_link\nReferência PNG + Tutorial incluso",
    "HUD-4D": "=== HUD 4 DEDOS ===\n\nLink: https://drive.google.com/seu_link\nReferência PNG + Tutorial incluso",
    "SENSI-HUD": "=== SENSI + HUD ===\n\nLink: https://drive.google.com/seu_link\nSensi + HUD + Tutorial",
    "PACK-COMPLETO": "=== PACK COMPLETO ===\n\nLink: https://drive.google.com/seu_link\nTudo incluso + Bônus"
}

class CupomModal(discord.ui.Modal, title="Aplicar Cupom de Desconto"):
    cupom = discord.ui.TextInput(
        label="Digite o cupom",
        placeholder="Ex: 2026",
        required=True,
        max_length=20
    )

    async def on_submit(self, interaction: discord.Interaction):
        produto_info = ultimo_produto.get(interaction.user.id)
        if not produto_info:
            await interaction.response.send_message("**❌ Erro:** Carrinho vazio.", ephemeral=True)
            return

        cupom_digitado = self.cupom.value.upper()
        
        CUPONS = {
            "2026": 10,
            "DNZX10": 10,
            "PRIMEIRA": 5
        }

        if cupom_digitado in CUPONS:
            valor_original = float(produto_info['valor'].replace(',', '.'))
            
            if cupom_digitado == "PRIMEIRA":
                desconto = CUPONS[cupom_digitado]
            else:
                desconto = valor_original * (CUPONS[cupom_digitado] / 100)
            
            ultimo_produto[interaction.user.id]['cupom'] = cupom_digitado
            ultimo_produto[interaction.user.id]['desconto'] = desconto
            
            valor_final = valor_original - desconto
            
            embed = discord.Embed(
                title="✅ Cupom Aplicado!",
                description=f"Cupom `{cupom_digitado}` aplicado com sucesso!",
                color=discord.Color.green()
            )
            embed.add_field(name="Valor Original", value=f"R$ {valor_original:.2f}".replace('.', ','), inline=True)
            embed.add_field(name="Desconto", value=f"R$ {desconto:.2f}".replace('.', ','), inline=True)
            embed.add_field(name="Valor Final", value=f"**R$ {valor_final:.2f}**".replace('.', ','), inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("**❌ Cupom inválido ou expirado.**", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} tá online!')
    try:
        synced = await bot.tree.sync()
        print(f'Sincronizei {len(synced)} comandos')
    except Exception as e:
        print(e)

# COMANDO PRA MANDAR A LOJA
@bot.command()
@commands.has_permissions(administrator=True)
async def loja(ctx):
    embed = discord.Embed(
        title="🔥 DNZX STORE - LOJA OFICIAL",
        description="**Escolha uma categoria abaixo:**",
        color=discord.Color.blurple()
    )
    
    view = View()
    view.add_item(Button(label="HS Peito OFC", style=discord.ButtonStyle.blurple, emoji="🎯", custom_id="categoria_hs_peito"))
    view.add_item(Button(label="HS Pescoço OFC", style=discord.ButtonStyle.blurple, emoji="🎯", custom_id="categoria_hs_pescoco"))
    view.add_item(Button(label="FF Premium", style=discord.ButtonStyle.green, emoji="💎", custom_id="categoria_ff_premium"))
    view.add_item(Button(label="Proxy iOS", style=discord.ButtonStyle.grey, emoji="📱", custom_id="categoria_proxy"))
    view.add_item(Button(label="Contas", style=discord.ButtonStyle.red, emoji="👤", custom_id="categoria_contas"))
    
    await ctx.send(embed=embed, view=view)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        
        # CATEGORIAS
        if interaction.data["custom_id"] == "categoria_hs_peito":
            embed = discord.Embed(title="🎯 HS PEITO OFC", description="**Escolha o produto:**", color=discord.Color.red())
            view = View()
            view.add_item(Button(label="HS Peito - R$ 2,00", style=discord.ButtonStyle.red, custom_id="hs_peito_200"))
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        elif interaction.data["custom_id"] == "categoria_hs_pescoco":
            embed = discord.Embed(title="🎯 HS PESCOÇO OFC", description="**Escolha o produto:**", color=discord.Color.red())
            view = View()
            view.add_item(Button(label="HS Pescoço - R$ 1,00", style=discord.ButtonStyle.red, custom_id="hs_pescoco_100"))
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        # HS PEITO - R$ 2,00
        elif interaction.data["custom_id"] == "hs_peito_200":
            ultimo_produto[interaction.user.id] = {"nome": "HS Peito OFC", "valor": "2,00", "id": "HS-PEITO-200"}
            embed = discord.Embed(description="✅ Seu carrinho foi criado com êxito.", color=discord.Color.green())
            view = View()
            view.add_item(Button(label="Ver Carrinho", style=discord.ButtonStyle.grey, emoji="🔗", custom_id="ver_carrinho"))
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        # HS PESCOÇO - R$ 1,00
        elif interaction.data["custom_id"] == "hs_pescoco_100":
            ultimo_produto[interaction.user.id] = {"nome": "HS Pescoço OFC", "valor": "1,00", "id": "HS-PESCOCO-100"}
            embed = discord.Embed(description="✅ Seu carrinho foi criado com êxito.", color=discord.Color.green())
            view = View()
            view.add_item(Button(label="Ver Carrinho", style=discord.ButtonStyle.grey, emoji="🔗", custom_id="ver_carrinho"))
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)        # BOTÃO VER CARRINHO
        elif interaction.data["custom_id"] == "ver_carrinho":
            produto_info = ultimo_produto.get(interaction.user.id)
            
            if not produto_info:
                await interaction.response.send_message("**❌ Carrinho vazio.** Clica em algum produto primeiro.", ephemeral=True)
                return
            
            valor_original = float(produto_info['valor'].replace(',', '.'))
            cupom_aplicado = produto_info.get('cupom', None)
            desconto = produto_info.get('desconto', 0)
            valor_final = valor_original - desconto
                
            embed = discord.Embed(
                title="Detalhes da sua compra",
                description="Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real. Você pode **alterar quantidades, aplicar cupons** ou **concluir sua compra** usando os botões abaixo.",
                color=discord.Color.blurple()
            )
            embed.add_field(name="Produtos no Carrinho (1x)", value=f"```1x {produto_info['nome']} | R$ {produto_info['valor']}```", inline=False)
            
            if cupom_aplicado:
                embed.add_field(name="Cupom Aplicado", value=f"```{cupom_aplicado} - R$ {desconto:.2f}```".replace('.', ','), inline=False)
                embed.add_field(name="Valor à vista", value=f"```R$ {valor_final:.2f}```".replace('.', ','), inline=False)
            else:
                embed.add_field(name="Valor à vista", value=f"```R$ {produto_info['valor']}```", inline=False)
                
            embed.set_footer(text=f"DnzX Store | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            view = View()
            view.add_item(Button(label="Ir para pagamento", style=discord.ButtonStyle.green, emoji="✔️", custom_id="ir_pagamento"))
            view.add_item(Button(label="Editar quantidade", style=discord.ButtonStyle.blurple, emoji="✏️", custom_id="editar_qtd"))
            view.add_item(Button(label="Usar cupom de desconto", style=discord.ButtonStyle.grey, emoji="🎟️", custom_id="usar_cupom"))
            
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        # IR PARA PAGAMENTO - EPHEMERAL PRO CLIENTE + CÓPIA PRA STAFF
        elif interaction.data["custom_id"] == "ir_pagamento":
            produto_info = ultimo_produto.get(interaction.user.id)
            if not produto_info:
                await interaction.response.send_message("**❌ Carrinho vazio.**", ephemeral=True)
                return
                
            valor_original = float(produto_info['valor'].replace(',', '.'))
            desconto = produto_info.get('desconto', 0)
            valor_final = valor_original - desconto
            
            embed = discord.Embed(
                title="Escolha a sua forma de pagamento",
                description="Dê uma última olhada na sua compra e escolha como deseja pagar para concluir de forma prática e rápida.",
                color=discord.Color.blurple()
            )
            embed.add_field(name="Produtos no Carrinho (1x)", value=f"```1x {produto_info['nome']} | R$ {valor_final:.2f}```".replace('.', ','), inline=False)
            embed.add_field(name="Valor à vista", value=f"```R$ {valor_final:.2f}```".replace('.', ','), inline=False)
            embed.set_footer(text=f"Cliente: {interaction.user.name} | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            view = View()
            view.add_item(Button(label="Pagar com Pix", style=discord.ButtonStyle.grey, emoji="💠", custom_id="pagar_pix"))
            view.add_item(Button(label="Pagar com Cartão", style=discord.ButtonStyle.grey, emoji="💳", custom_id="pagar_cartao", disabled=True))
            view.add_item(Button(label="Pagar com Saldo", style=discord.ButtonStyle.grey, emoji="💰", custom_id="pagar_saldo", disabled=True))
            view.add_item(Button(label="Voltar", style=discord.ButtonStyle.grey, emoji="↩️", custom_id="voltar_carrinho"))
            
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            
            canal_logs = bot.get_channel(ID_CANAL_LOGS)
            embed_logs = embed.copy()
            embed_logs.title = f"👀 {interaction.user.name} está na tela de pagamento"
            await canal_logs.send(embed=embed_logs)

        # PAGAR COM PIX - EPHEMERAL PRO CLIENTE + CÓPIA PRA STAFF
        elif interaction.data["custom_id"] == "pagar_pix":
            produto_info = ultimo_produto.get(interaction.user.id)
            if not produto_info:
                await interaction.response.send_message("**❌ Carrinho vazio.**", ephemeral=True)
                return
                
            valor_final = float(produto_info['valor'].replace(',', '.')) - produto_info.get('desconto', 0)
            pix_copia_cola = PIX
            
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(pix_copia_cola)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            arquivo_qr = discord.File(buffer, filename="qrcode_pix.png")
            
            embed = discord.Embed(
                title="Pagamento via PIX criado",
                color=discord.Color.blurple()
            )
            embed.add_field(name="Código copia e cola", value=f"```{pix_copia_cola}```", inline=False)
            embed.set_image(url="attachment://qrcode_pix.png")
            embed.set_footer(text=f"Cliente: {interaction.user.name} | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            view = View()
            view.add_item(Button(label="Código copia e cola", style=discord.ButtonStyle.grey, emoji="📋", custom_id="copiar_pix"))
            view.add_item(Button(label="Cancelar Compra", style=discord.ButtonStyle.red, emoji="❌", custom_id="cancelar_compra"))
            
            ultimo_produto[interaction.user.id]['pix_code'] = pix_copia_cola
            
            await interaction.response.send_message(embed=embed, file=arquivo_qr, view=view, ephemeral=True)
            
            buffer.seek(0)
            arquivo_qr_logs = discord.File(buffer, filename="qrcode_pix.png")
            canal_logs = bot.get_channel(ID_CANAL_LOGS)
            embed_logs = discord.Embed(title=f"💠 {interaction.user.name} gerou PIX", description=f"**Produto:** {produto_info['nome']}\n**Valor:** R$ {valor_final:.2f}".replace('.', ','), color=discord.Color.blue())
            embed_logs.set_image(url="attachment://qrcode_pix.png")
            await canal_logs.send(embed=embed_logs, file=arquivo_qr_logs)

        # COPIAR PIX
        elif interaction.data["custom_id"] == "copiar_pix":
            produto_info = ultimo_produto.get(interaction.user.id)
            pix_code = produto_info.get('pix_code', PIX)
            await interaction.response.send_message(f"**📋 PIX Copia e Cola:**\n```\n{pix_code}\n```", ephemeral=True)

        # CANCELAR COMPRA
        elif interaction.data["custom_id"] == "cancelar_compra":
            if interaction.user.id in ultimo_produto:
                del ultimo_produto[interaction.user.id]
            await interaction.response.edit_message(content="**❌ Compra cancelada.**\n\nSeu carrinho foi esvaziado.", embed=None, view=None, attachments=[])

        # PAGAR COM CARTÃO
        elif interaction.data["custom_id"] == "pagar_cartao":
            await interaction.response.send_message("**⚠️ Pagamento com cartão indisponível no momento.**\n\nUse PIX para liberação imediata.", ephemeral=True)

        # PAGAR COM SALDO
        elif interaction.data["custom_id"] == "pagar_saldo":
            await interaction.response.send_message("**⚠️ Sistema de saldo indisponível.**\n\nUse PIX para liberação imediata.", ephemeral=True)

        # VOLTAR PRO CARRINHO
        elif interaction.data["custom_id"] == "voltar_carrinho":
            produto_info = ultimo_produto.get(interaction.user.id)
            
            valor_original = float(produto_info['valor'].replace(',', '.'))
            cupom_aplicado = produto_info.get('cupom', None)
            desconto = produto_info.get('desconto', 0)
            valor_final = valor_original - desconto
                
            embed = discord.Embed(
                title="Detalhes da sua compra",
                description="Aqui estão os produtos que você escolheu, com valores atualizados e estoque em tempo real. Você pode **alterar quantidades, aplicar cupons** ou **concluir sua compra** usando os botões abaixo.",
                color=discord.Color.blurple()
            )
            embed.add_field(name="Produtos no Carrinho (1x)", value=f"```1x {produto_info['nome']} | R$ {produto_info['valor']}```", inline=False)
            
            if cupom_aplicado:
                embed.add_field(name="Cupom Aplicado", value=f"```{cupom_aplicado} - R$ {desconto:.2f}```".replace('.', ','), inline=False)
                embed.add_field(name="Valor à vista", value=f"```R$ {valor_final:.2f}```".replace('.', ','), inline=False)
            else:
                embed.add_field(name="Valor à vista", value=f"```R$ {produto_info['valor']}```", inline=False)
                
            embed.set_footer(text=f"DnzX Store | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            view = View()
            view.add_item(Button(label="Ir para pagamento", style=discord.ButtonStyle.green, emoji="✔️", custom_id="ir_pagamento"))
            view.add_item(Button(label="Editar quantidade", style=discord.ButtonStyle.blurple, emoji="✏️", custom_id="editar_qtd"))
            view.add_item(Button(label="Usar cupom de desconto", style=discord.ButtonStyle.grey, emoji="🎟️", custom_id="usar_cupom"))
            
            await interaction.response.edit_message(embed=embed, view=view)

        # EDITAR QUANTIDADE
        elif interaction.data["custom_id"] == "editar_qtd":
            await interaction.response.send_message("**⚠️ Por enquanto só vendemos 1 unidade por vez.**\n\nQuer mais de 1? Faz compras separadas ou abre um ticket.", ephemeral=True)

        # USAR CUPOM
        elif interaction.data["custom_id"] == "usar_cupom":
            await interaction.response.send_modal(CupomModal())

        # APROVAR COMPROVANTE
        elif interaction.data["custom_id"].startswith("aprovar_"):
            cliente_id = int(interaction.data["custom_id"].split("_")[1])
            produto_info = ultimo_produto.get(cliente_id)
            
            if not produto_info:
                await interaction.response.send_message("**❌ Erro:** Produto não encontrado.", ephemeral=True)
                return
            
            produto_id = produto_info['id']
            texto_entrega = PRODUTOS_ENTREGA.get(produto_id, "**❌ Produto não cadastrado. Adicione no código!**")
            
            cliente = await bot.fetch_user(cliente_id)
            try:
                embed_entrega = discord.Embed(
                    title="✅ PAGAMENTO APROVADO",
                    description=f"**{produto_info['nome']}**\n\n{texto_entrega}",
                    color=discord.Color.green()
                )
                embed_entrega.set_footer(text=f"DnzX Store | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                
                await cliente.send(embed=embed_entrega)
                await interaction.response.send_message(f"**✅ Entregue pra {cliente.mention}!**", ephemeral=True)
                
                if ID_CANAL_LOGS:
                    canal_logs = bot.get_channel(ID_CANAL_LOGS)
                    await canal_logs.send(f"✅ {interaction.user.mention} aprovou `{produto_info['nome']}` pra {cliente.mention}")
                
                del ultimo_produto[cliente_id]
                
            except:
                await interaction.response.send_message("**❌ Não consegui mandar DM pro cliente.** DM fechada.", ephemeral=True)

        # REPROVAR COMPROVANTE
        elif interaction.data["custom_id"].startswith("reprovar_"):
            cliente_id = int(interaction.data["custom_id"].split("_")[1])
            cliente = await bot.fetch_user(cliente_id)
            
            try:
                await cliente.send("**❌ PAGAMENTO REPROVADO**\n\nSeu comprovante foi reprovado. Verifique o pagamento ou abra um ticket.")
                await interaction.response.send_message(f"**❌ Reprovado pra {cliente.mention}**", ephemeral=True)
                
                if ID_CANAL_LOGS:
                    canal_logs = bot.get_channel(ID_CANAL_LOGS)
                    await canal_logs.send(f"❌ {interaction.user.mention} reprovou comprovante de {cliente.mention}")
                    
            except:
                await interaction.response.send_message("**❌ Não consegui avisar o cliente.**", ephemeral=True)

# SISTEMA DE COMPROVANTE NA DM
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        canal_comprovantes = bot.get_channel(ID_CANAL_COMPROVANTES)
        produto_info = ultimo_produto.get(message.author.id)

        if not produto_info:
            produto_nome = "⚠️ Produto não identificado"
            produto_valor = "Verificar com cliente"
            produto_id = "SEM-ID"
            cor = discord.Color.orange()
        else:
            produto_nome = produto_info['nome']
            produto_valor = f"R$ {float(produto_info['valor'].replace(',', '.')) - produto_info.get('desconto', 0):.2f}".replace('.', ',')
            produto_id = produto_info['id']
            cor = discord.Color.yellow()

        embed_staff = discord.Embed(
            title="📸 Novo Comprovante Recebido",
            description=f"**Cliente:** {message.author.mention}\n**ID:** {message.author.id}\n**Produto:** {produto_nome}\n**Valor:** {produto_valor}\n**ID:** {produto_id}",
            color=cor
        )
        embed_staff.set_image(url=message.attachments[0].url)
        embed_staff.set_footer(text=f"Recebido em {datetime.now().strftime('%d/%m/%Y %H:%M')}")

        view_staff = View()
        view_staff.add_item(Button(label="✅ Aprovar", style=discord.ButtonStyle.green, custom_id=f"aprovar_{message.author.id}"))
        view_staff.add_item(Button(label="❌ Reprovar", style=discord.ButtonStyle.red, custom_id=f"reprovar_{message.author.id}"))

        await canal_comprovantes.send(embed=embed_staff, view=view_staff)

        if produto_info:
            embed_cliente = discord.Embed(color=discord.Color.blue())
            embed_cliente.add_field(name="Detalhes", value=f"1x {produto_nome} | {produto_valor}", inline=False)
            embed_cliente.set_footer(text=f"DnzX Store | {datetime.now().strftime('%d/%m/%Y %H:%M')}")

            await message.reply("**✅ Comprovante recebido!** Aguarde a confirmação da equipe.", embed=embed_cliente)
        else:
            await message.reply("**⚠️ ATENÇÃO!**\n\nVocê enviou o comprovante mas não clicou no botão do produto antes.\n\n**Informe aqui na DM qual produto você comprou** ou abra um ticket.")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
