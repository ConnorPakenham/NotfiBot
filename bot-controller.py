import discord
import asyncio
import time
from splatoonschedule import get_updates

TOKEN = 'XXXXXXX'

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!sub'):
        
        user = message.author.mention
        sublist = message.content.split(" ")[1]

        f = open("{0}/{1}".format(sublist, sublist), "r") 
        flag = False
        
        for line in f:
            subscriber = line.split("//")[0]
            if user == subscriber.strip():
                flag = True

        if flag == False:
            try:
                f = open("{0}/{1}".format(sublist, sublist), "a")
                

                f.write("{0}//{1}\n".format(user, sublist))

                msg = "Subbed"

            except OSError:
                msg = "No such mailing list!"
        else:
            msg = "Already on the mailing list"

        await client.send_message(message.channel, msg)
    elif message.content.startswith('!check'):
        channel = discord.Object(id='478905754510688279')
        f = open("splatoon2/lastmsg", "r")
        msg = "Salmon Run" 
        msg += "\n=================================\n"
        msg +=  f.read()
        msg += "\n=================================\n"

        await client.send_message(channel, msg)
        

async def check_for_updates():
    await client.wait_until_ready()
    channel = discord.Object(id='478905754510688279')
    while not client.is_closed:

        update = get_updates()
        f = open("splatoon2/lastmsg", "r")
        oldupdate = f.read()
        if(oldupdate != update):

            msg = "Salmon Run" 
            msg += "\n=================================\n"
            msg +=  update
            msg += "\n=================================\n"

            sub_file = open("splatoon2/splatoon2", "r")

            for line in sub_file:
                subscriber,topic = line.split("//")
                if 'splatoon2' == topic.strip():
                    msg += subscriber + " "

            await client.send_message(channel, msg)
            f = open("splatoon2/lastmsg", "w")
            f.write(update)

        await asyncio.sleep(7200) # task runs every 2 hours

async def remind_lauren():
    await client.wait_until_ready()
    channel = discord.Object(id='478905754510688279')
    while not client.is_closed:
        f = open("splatoon2/eta_time", "r")
        eta = f.read()
        eta_start, eta_end = eta.split("//")
        eta_time, eta_date  = eta_start.split(" ")
        if eta_date.strip()  == time.strftime("%d-%m-%Y"):
            if eta_time[:-2] == time.strftime("%H"):
                f = open("splatoon2/lastmsg", "r")
                msg = "***STARTING SOON Salmon Run STARTING SOON***" 
                msg += "\n=================================\n"
                msg +=  f.read()
                msg += "\n=================================\n"

                sub_file = open("splatoon2/splatoon2", "r")

                for line in sub_file:
                    subscriber,topic = line.split("//")
                    if 'splatoon2' == topic.strip():
                        msg += subscriber + " "

                await client.send_message(channel, msg)
        await asyncio.sleep(60)




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(check_for_updates())
client.loop.create_task(remind_lauren())
client.run(TOKEN)