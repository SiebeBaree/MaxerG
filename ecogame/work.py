import discord
from discord.ext import commands
import json
import random
from random import randint
import time
import datetime
import mysql.connector

with open('./db_settings.json', 'r', encoding='utf-8') as read_settings:
    settings = json.load(read_settings)

host = settings['host']
user = settings['user']
password = settings['password']
database = settings['database']

read_settings.close()


class EcoWork(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        minigame_channels = ["💰│economy-game", "🔒│bots"]
        if str(ctx.channel) in minigame_channels:
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
            embed_footer = maxergdb_cursor.fetchone()

            maxergdb_cursor.execute("SELECT currency FROM maxerg_config")
            currency_tuple = maxergdb_cursor.fetchone()
            currency = currency_tuple[0]

            loon = randint(6, 25)
            loon_cast = int(loon)

            ecogame_sql_cash = f"UPDATE maxerg_ecogame SET cash = cash + {loon_cast} WHERE user_id = {ctx.author.id}"
            maxergdb_cursor.execute(ecogame_sql_cash)
            db_maxerg.commit()

            mogelijke_antwoorden = [f'Je kreeg {currency}{loon_cast} om hamburgers te maken in de McDonalds.',
                                    f'Je baas betaalde je {currency}{loon_cast} om zijn kantoor te renoveren.',
                                    f'Je hebt geholpen bij een hand car wash en kreeg {currency}{loon_cast}.',
                                    f'Je hielp iemand verhuizen. Aan het einde van de dag kreeg je {currency}{loon_cast}.',
                                    f'Je hebt de router gefixt bij je buren en als beloning gaven ze je {currency}{loon_cast}.',
                                    f'Je speelde mee in een Minecraft skywars potje en je won {currency}{loon_cast}.',
                                    f'Door al je items op Hypixel Skyblock te verkopen verdiende je {currency}{loon_cast}.',
                                    f'Je werkte als een schoonmaker en je kreeg {currency}{loon_cast}.',
                                    f'Je behaalde goede punten en kreeg {currency}{loon_cast} van je ouders.']
            antwoord = random.choice(mogelijke_antwoorden)

            em = discord.Embed(
                description=f"{antwoord}",
                color=0x1bd115,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=embed_footer[0])
            await ctx.send(embed=em)

            db_maxerg.close()
        else:
            await ctx.channel.purge(limit=1)
            del_msg = await ctx.send(f"Je moet in <#708055327958106164> zitten om deze command uit te voeren.")
            time.sleep(3)
            await del_msg.delete()

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            db_maxerg = mysql.connector.connect(host=host, database=database, user=user, passwd=password)
            maxergdb_cursor = db_maxerg.cursor()

            maxergdb_cursor.execute("SELECT footer FROM maxerg_config")
            embed_footer = maxergdb_cursor.fetchone()

            maxergdb_cursor.execute("SELECT embedcolor FROM maxerg_config")
            embed_color_tuple = maxergdb_cursor.fetchone()
            embed_color = int(embed_color_tuple[0], 16)

            cooldown_limit = error.retry_after
            if cooldown_limit >= 86400:
                conversion = time.strftime("%#dd %#Hu %#Mm %#Ss", time.gmtime(error.retry_after))
            elif 3600 <= cooldown_limit < 86400:
                conversion = time.strftime("%#Hu %#Mm %#Ss", time.gmtime(error.retry_after))
            else:
                conversion = time.strftime("%#Mm %#Ss", time.gmtime(error.retry_after))

            em = discord.Embed(
                description=f"<:error:725030739531268187> Je moet {conversion} wachten om deze command opnieuw te gebruiken.",
                color=embed_color,
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            em.set_footer(text=embed_footer[0])
            await ctx.send(embed=em)

            db_maxerg.close()
        else:
            raise error


def setup(client):
    client.add_cog(EcoWork(client))
