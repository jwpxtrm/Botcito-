import os
import discord
from discord import app_commands
from discord.ext import commands

# Lee el Token de Discord configurado en el servidor (Koyeb/Discloud)
TOKEN = os.getenv("DISCORD_TOKEN")

class TikTokBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sincroniza los comandos slash con Discord
        await self.tree.sync()

bot = TikTokBot()

@bot.event
async def on_ready():
    print(f"Bot conectado y listo como: {bot.user}")

@bot.tree.command(name="directo", description="Anuncia el directo de LEO_VXLS en TikTok")
@app_commands.describe(
    enlace="Pega aquí el enlace completo de la transmisión de TikTok"
)
async def directo(interaction: discord.Interaction, enlace: str):
    # 1. Crear la tarjeta (Embed) con enlace en texto
    embed = discord.Embed(
        title="🔴 ¡LEO_VXLS ESTÁ EN DIRECTO! 🔴",
        description=(
            "¡El stream acaba de comenzar! 🚀\n\n"
            f"[Click aquí]({enlace})\n\n"
            "👉 ¡Entra a saludar, deja tu me gusta 💖 y comparte con tus amigos! 🍿✨"
        ),
        color=0xFF0050  # Color de TikTok
    )
    embed.set_footer(
        text=f"Anunciado por {interaction.user.display_name}",
        icon_url=interaction.user.display_avatar.url
    )

    # 2. Crear el botón interactivo que redirige a TikTok
    view = discord.ui.View()
    boton_tiktok = discord.ui.Button(
        label="Ir a TikTok Live",
        url=enlace,
        style=discord.ButtonStyle.link,
        emoji="🎥"
    )
    view.add_item(boton_tiktok)

    # 3. Enviar el mensaje mencionando a @everyone
    await interaction.response.send_message(
        content="@everyone", 
        embed=embed, 
        view=view
    )

if __name__ == "__main__":
    if not TOKEN:
        print("Error: No se ha detectado la variable de entorno DISCORD_TOKEN.")
    else:
        bot.run(TOKEN)
