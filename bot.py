import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

class TikTokBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = TikTokBot()

@bot.event
async def on_ready():
    print(f"Bot conectado y listo como: {bot.user}")

@bot.tree.command(name="directo", description="Anuncia el directo de LEO_VXLS en TikTok")
@app_commands.describe(enlace="Pega aquí el enlace del live de TikTok")
@app_commands.checks.has_permissions(administrator=True)  # Solo Administradores pueden usarlo
async def directo(interaction: discord.Interaction, enlace: str):
    embed = discord.Embed(
        title="🔴 ¡LEO_VXLS ESTÁ EN DIRECTO! 🔴",
        description=(
            "¡El stream acaba de comenzar! 🚀\n\n"
            f"[Click aquí]({enlace})\n\n"
            "👉 ¡Entra a saludar, deja tu me gusta 💖 y comparte con tus amigos! 🍿✨"
        ),
        color=0xFF0050
    )
    embed.set_footer(
        text=f"Anunciado por {interaction.user.display_name}",
        icon_url=interaction.user.display_avatar.url
    )

    view = discord.ui.View()
    boton_tiktok = discord.ui.Button(
        label="Ir a TikTok Live",
        url=enlace,
        style=discord.ButtonStyle.link,
        emoji="🎥"
    )
    view.add_item(boton_tiktok)

    await interaction.response.send_message(content="@everyone", embed=embed, view=view)

# Si alguien sin permiso de Administrador intenta usar el comando
@directo.error
async def directo_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "❌ Solo los **Administradores** pueden usar este comando.", 
            ephemeral=True  # Mensaje privado solo visible para quien ejecutó el comando
        )

if __name__ == "__main__":
    bot.run(TOKEN)
    
