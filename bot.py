import discord
import responses
from discord.ext import commands, tasks
import datetime
import config

# async def send_message(message, user_message, is_private):
#     try:
#         response = responses.get_response(user_message)
#         print(f"The extracted response was {response}")
#         await message.author.send(response) if is_private else await message.channel.send(response)
#     except Exception as e:
#         print(e)

# async def send_message(message):
#     try:
#         userid = message.author.id
#         await message.channel.send(userid)
#     except Exception as e:
#         print(e)

def run_discord_bot():
    TOKEN = config.TOKEN
    
    intents = discord.Intents.all()
    # intents.members = True
    
    bot = commands.Bot(command_prefix=commands.when_mentioned_or("$"), intents=intents)    
    general_text_channel_id = 696847976819064887
    
    forbidden_words = ["χαμπο", "mpeite", "καρδαμη", "exoume", "εχουμε", "+1"]
    lovely_words = ["among", "αμονγκ"]
    
    @bot.event
    async def on_ready():
        # bot.wait_until_ready()
        print(f"{bot.user.name} is now running!")
        if not scheduled_message.is_running():
            scheduled_message.start()
            print("scheduled messaged started normally")
    
    
    @bot.event
    async def on_connect():
        print("Ok Amen")
    
    
    @bot.slash_command()
    async def ping(ctx, name):
        await ctx.respond(f"Bot ping is {bot.latency} seconds, your name is {name}")
    
    
    @bot.command()
    async def calculate(ctx, num1, operator, num2):
        def add(num1, num2):
            return float(num1) + float(num2)
        def multiply(num1, num2):
            return float(num1) * float(num2)
        def divide(num1, num2):
            return float(num1) / float(num2)
        def subtract(num1, num2):
            return float(num1) - float(num2)
        
        if operator == "+":
            result = add(num1, num2)
            await ctx.respond(f"Done! The answer is {result}")
        elif operator == "-":
            result = subtract(num1, num2)
        elif operator == "*":
            result = multiply(num1, num2)
        elif operator == "/":
            result = divide(num1, num2)
        else:
            result = "Not valid operator symbol. You need to try one of the following ` + - / * `"
        
        await ctx.respond(f"Done! The answer is {result}")
        return
    

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        # detected_author = str(message.author)  
        
        if any(fword in message.content for fword in forbidden_words):
            await message.add_reaction("\U0001F921")
        elif any(fword in message.content for fword in lovely_words):
            await message.add_reaction("\U0001F497")
        elif len(message.content) > 20:
            await message.add_reaction("\U0001F642")

        await bot.process_commands(message)
        
    @bot.event
    async def on_message_edit(initial_msg, edited_msg):
        if edited_msg.author == bot.user:
            return
        
        detected_author = str(initial_msg.author)
        await edited_msg.channel.send(f"WARNING! You cannot escape your mistakes in this world. \n {detected_author} initially said {str(initial_msg.content)}")
        
    
    @bot.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(f'Hi {member.name}, welcome to the most toxic Discord server!')
    
    
    @bot.event
    async def on_user_update(initial_profile, edited_profile):
        if initial_profile.name != edited_profile.name:
            await edited_profile.channel.send(f"{initial_profile.name} was changed into {edited_profile.name}")
        elif initial_profile.avatar != edited_profile.avatar:
            await edited_profile.avatar.channel.send(f"{initial_profile.avatar} was changed into {edited_profile.avatar}")
        
    
    def fancy_printing(txt):
        return "`" + txt + "`"
    
    
    @bot.event
    async def on_message_delete(message):
        if message.author.id == bot.user.id:
            return
        response = message.content
        to_be_printed = fancy_printing(response)
        await message.channel.send("Sadly once something is said you can't unsay it.\n")
        await message.channel.send(f"User {message.author} said:\n")
        await message.channel.send(to_be_printed)
    
    
    @bot.command()
    async def bitcoin(ctx, currency):
        await ctx.send(responses.get_bitcoin_price(currency))
        
        
    goodMorningTime = datetime.time(hour=19) #Athens - utc+2
    @tasks.loop(time=goodMorningTime)
    async def scheduled_message(ctx):
        channel = bot.get_channel(general_text_channel_id)
        await channel.send("`Scheduled message:\n`")
        await channel.send("`Current prices of bitcoin`")
        await channel.send(responses.get_coin_report())
     
    # scheduled_message.start()
    bot.run(TOKEN)
    
        
     
        
        
        
        
        