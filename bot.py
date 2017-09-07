# Name: meido chan (meido-bot)
# Description: a simple discord chat bot built on discord.py
# Author: Alice Archer

import discord
from discord.ext import commands

import random # eightball
import re     # sed
import pyowm  # weather

# load config information from ./.bot.conf (this will be static for now)

keyList = {}
lines = []

with open('./.bot.conf') as conf:
    lines = conf.readlines()

for l in lines:
    prefix = l.split(" :: ")[0]
    postfix = l.split(" :: ")[1]
    temp = {prefix: postfix}
    keyList.update(temp)

# loading complete
# keys are now in keyList

weatherFetch = pyowm.OWM(keyList['weatherAppKey'])

description = '''meido chan is here to help you, master.'''
history = []

class MeidoBot(commands.Bot):
    async def on_message(self, message):
        pattern = re.compile(r'\.s\/(?P<find>.+)\/(?P<replace>.+)\/((?P<tags>\w+))?')
        match = pattern.fullmatch(message.content)
        pattern_no_case = re.compile(r'\.s\/(?P<find>.+)\/(?P<replace>.+)\/((?P<tags>\w+))?', re.IGNORECASE)
        match_no_case = pattern_no_case.fullmatch(message.content)
        if match:
            async for m in self.logs_from(message.channel):
                if m.author == self.user or m.id == message.id:
                    continue
                original = m.content
                if (match.group('tags') is not None):
                    if 'g' in match.group('tags'):
                        new = re.sub(match.group('find'), match.group('replace'), original)
                else:
                    new = re.sub(match.group('find'), match.group('replace'), original, 1)

                if new != original:
                    usr = m.author.nick
                    await self.send_message(message.channel, f'{message.author.mention()} meant: {new}')
                    break
        else:
            await super().on_message(message)

bot = MeidoBot(command_prefix='.', description="meidobot, a discord bot for helping with your daily tasks")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('Yes, {0.subcommand_passed} is cool'.format(ctx))

@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')

@bot.command()
async def eightball(question : str):
    """gives a response from the eightball to a question"""
    answers = [ "It is certain","It is decidedly so","Without a doubt","Yes definitely","You may rely on it","As I see it, yes","Most likely","Outlook good","Yes","Signs point to yes","Reply hazy try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","My sources say no","Outlook not so good","Very doubtful" ]
    await bot.say(random.choice(answers))

@bot.command()
async def rude(question : str):
    answers = [ "You Wish","Get a clue","You've got to be kidding","Ask me if i care","whatever","Doubt it","No","You'd like that wouldn't you","Really?","Who Cares","Not in a million years","Nope Nope Nope","It seems you're in denial","Cannot predict now","That's Ridiculous","Huh?","All signs point to yes, or maybe no","If you say so","I really hope not","Oh, Please" ]
    await bot.say(random.choice(answers))

@bot.command()
async def weather(city : str, state : str):
    """gives weather"""
    observation = weatherFetch.weather_at_place(city + ',' + state)
    w = observation.get_weather()
    wind = w.get_wind()
    hum = w.get_humidity()
    temp = w.get_temperature('fahrenheit')

    rWind = wind['speed']
    rHum = hum
    rTemp = temp['temp']

    reply = "It is currently: " + str(rTemp) + "F degrees in " + city + ", " + state + " with wind speed of " + str(rWind) + "mph with a humidity of " + str(rHum) + "%."
    await bot.say(reply)

@bot.command()
async def headpat(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say(":headpat: {0.subcommand_passed}".format(ctx))

# run the bot
bot.run(keyList['discordAppKey'])