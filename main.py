# =========================================
# DISCORD BOT SIMPLES - RENDER READY
# =========================================

# Biblioteca padrão para acessar variáveis de ambiente
import os

# Biblioteca principal do Discord
import discord
from discord.ext import commands

# =========================================
# INTENTS (PERMISSÕES DO BOT)
# =========================================
# Intents dizem ao Discord o que o bot pode acessar
# message_content é OBRIGATÓRIO para comandos com prefixo

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# =========================================
# CRIAÇÃO DO BOT
# =========================================

bot = commands.Bot(
    command_prefix="!",   # Prefixo dos comandos (!ping, !clear, etc)
    intents=intents,
    help_command=None     # Remove o help padrão
)

# =========================================
# EVENTO: BOT CONECTADO
# =========================================

@bot.event
async def on_ready():
    print("===================================")
    print("🤖 Bot iniciado com sucesso!")
    print(f"Usuário: {bot.user}")
    print(f"ID: {bot.user.id}")
    print("Rodando no Render 🚀")
    print("===================================")

    await bot.change_presence(
        activity=discord.Game(name="Online | Render")
    )

# =========================================
# COMANDO: PING
# =========================================

@bot.command()
async def ping(ctx):
    """Mostra a latência do bot"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong 🏓 | `{latency}ms`")

# =========================================
# COMANDO: USERINFO
# =========================================

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    """Mostra informações de um usuário"""
    member = member or ctx.author

    embed = discord.Embed(
        title="👤 Informações do Usuário",
        color=discord.Color.blue()
    )

    embed.add_field(name="Nome", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(
        name="Conta criada em",
        value=member.created_at.strftime("%d/%m/%Y"),
        inline=False
    )

    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)

    await ctx.send(embed=embed)

# =========================================
# COMANDO: CLEAR (ADMIN)
# =========================================

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, quantidade: int):
    """Apaga mensagens do canal"""
    await ctx.channel.purge(limit=quantidade + 1)
    msg = await ctx.send(f"🧹 {quantidade} mensagens apagadas")
    await msg.delete(delay=3)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Use: !clear <quantidade>")

# =========================================
# INICIALIZAÇÃO DO BOT
# =========================================

# 🔐 O TOKEN NÃO FICA NO CÓDIGO
# Ele vem do Render (Environment Variable)

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN NÃO DEFINIDO! Configure no Render.")

bot.run(TOKEN)
