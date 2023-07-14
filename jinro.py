import discord
from discord.ext import commands
import re
import csv
import os
import asyncio
import random
import func
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.dm_messages = True
intents.message_content = True
intents.members = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()

#### LOAD ENV ####
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("SERVER_ID"))
VOICE_CH_ID = int(os.getenv("VOICE_CHANNEL_ID"))
TXT_CH_ID = int(os.getenv("TEXT_CHANNEL_ID"))
LOG_CH_ID = int(os.getenv("LOG_CHANNEL_ID"))
WLF_CH_ID = int(os.getenv("WEREWOLF_CHANNEL_ID"))
RIP_CH_ID = int(os.getenv("RIP_CHANNEL_ID"))
RIP_RL_ID = int(os.getenv("RIP_ROLE_ID"))
MAX_VOTE_REPEAT = int(os.getenv("MAX_VOTE"))
GRD_FLG = int(os.getenv("CONSECUTIVE_GRD_FLG"))


#### OTHER VALUE ####
REACTION_EMOJIS_A = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟','⏺️','🔼','⏹️','0️⃣']
REACTION_EMOJIS_B = ['⭕', '❌']

main_emb_message_id = None
global_task = None
exit_flg = False
m_exit_flg = False
user_exit_flg = False
remain_vote_repeat = MAX_VOTE_REPEAT
day = 0

#### VOICE CONTROL ####
async def mute_alives():
    with open('status.csv', 'r') as status_file:
        status_reader = csv.DictReader(status_file)
        for row in status_reader:
            if row['vital'] == '0':
                alive_id = row['id']
                member = bot.get_channel(VOICE_CH_ID).guild.get_member(int(alive_id))
                if member:
                    if not member.voice.mute:
                        await member.edit(mute=True)
                        await asyncio.sleep(0.3)

async def unmute_alives():
    with open('status.csv', 'r') as status_file:
        status_reader = csv.DictReader(status_file)
        for row in status_reader:
            if row['vital'] == '0':
                alive_id = row['id']
                member = bot.get_channel(VOICE_CH_ID).guild.get_member(int(alive_id))
                if member:
                    if member.voice.mute:
                        await member.edit(mute=False)
                        await asyncio.sleep(0.3)

async def unmute_select(user_id):
    member = bot.get_channel(VOICE_CH_ID).guild.get_member(int(user_id))
    if member:
        if member.voice.mute:
            await member.edit(mute=False)
            await asyncio.sleep(0.3)

async def mute_select(user_id):
    member = bot.get_channel(VOICE_CH_ID).guild.get_member(int(user_id))
    if member:
        if not member.voice.mute:
            await member.edit(mute=True)
            await asyncio.sleep(0.3)

async def unmute_all():
    vc = bot.get_channel(VOICE_CH_ID)
    if vc:
        async def unmute_and_undeafen(member):
            await member.edit(mute=False)
        tasks = [unmute_and_undeafen(member) for member in vc.members]
        await asyncio.gather(*tasks)

#### SKIPABLE TASKS ####
async def discussion_operates(message):
    global m_exit_flg
    m_exit_flg = False
    embed = message.embeds[0]
    embed.title = "会議の時間です"
    await message.edit(embed=embed)
    await asyncio.sleep(2)
    if m_exit_flg: return
    embed.set_footer(text="◇"*5 +"\n残り時間は5分です")
    await message.edit(embed=embed)
    await asyncio.sleep(30)
    if m_exit_flg: return
    await asyncio.sleep(30)
    if m_exit_flg: return
    embed.set_footer(text="◆" +"◇"*4 +"\n残り時間は4分です")
    await message.edit(embed=embed)
    await asyncio.sleep(30)
    if m_exit_flg: return
    await asyncio.sleep(30)
    if m_exit_flg: return
    embed.set_footer(text="◆"*2 +"◇"*3 +"\n残り時間は3分です")
    await message.edit(embed=embed)
    await asyncio.sleep(30)
    if m_exit_flg: return
    await asyncio.sleep(30)
    if m_exit_flg: return
    embed.set_footer(text="◆"*3 +"◇"*2 +"\n残り時間は2分です")
    await message.edit(embed=embed)
    await asyncio.sleep(30)
    if m_exit_flg: return
    await asyncio.sleep(30)
    if m_exit_flg: return
    embed.set_footer(text="◆"*4 +"◇"*1 +"\n残り時間は60秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if m_exit_flg: return
    embed.set_footer(text="■" +"□"*5 +"\n残り時間は50秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if m_exit_flg: return
    embed.set_footer(text="■"*2 +"□"*4 +"\n残り時間は40秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if m_exit_flg: return
    embed.set_footer(text="■"*3 +"□"*3 +"\n残り時間は30秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if m_exit_flg: return
    embed.set_footer(text="■"*4 +"□"*2 +"\n残り時間は20秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if m_exit_flg: return
    embed.set_footer(text="■"*5 +"□" +"\n残り時間は10秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if m_exit_flg: return
    embed.set_footer(text="■"*6 +"\n残り時間は0秒です")
    await message.edit(embed=embed)
    await mute_alives()
    embed.description = ""
    embed.set_footer(text="会議時間は終了しました")
    await message.edit(embed=embed)
    await asyncio.sleep(2)
    embed.set_footer(text="会議時間は終了しました\n✅を押して進行してください")
    await message.edit(embed=embed)
    await message.add_reaction('✅')

async def discussion_tasks(message):
    global global_task
    global_task = asyncio.create_task(discussion_operates(message))
    await global_task

async def interview_operates(message):
    global exit_flg
    exit_flg = False
    global user_exit_flg
    class A_error(Exception):
        pass
    embed = message.embeds[0]
    embed.title = "質疑応答の時間です"
    embed.color = 0x8B4513
    embed.set_footer(text="しばらくお待ちください")
    await message.edit(embed=embed)
    func.reset_temp()
    await asyncio.sleep(3)
    if exit_flg: return
    shuffled_order_ids = func.shuffle_discussion_order()
    for index, user_id in enumerate(shuffled_order_ids):
        if user_exit_flg:
            user_exit_flg = False
        func.update_from(user_id)
        user_name = func.get_name_by_id(user_id)
        embed.description = f"{index+1}人目の質問者は「{user_name}」です"
        embed.set_footer(text=f"{user_name}の応答を待機しています")
        await message.edit(embed=embed)
        if exit_flg: return
        if user_exit_flg:
            user_exit_flg = False
            await asyncio.sleep(3)
            continue
        user = await bot.fetch_user(user_id)
        smsg = await user.send("質問をスキップする場合は⏭️を押してください")
        await smsg.add_reaction('⏭️')
        await send_select_to(user_id)
        def check(payload):
            return payload.user_id == int(user_id)
        try:
            if exit_flg: return
            if user_exit_flg:
                user_exit_flg = False
                await asyncio.sleep(3)
                raise A_error()
            while True:
                if exit_flg: return
                if user_exit_flg:
                    user_exit_flg = False
                    await asyncio.sleep(3)
                    raise A_error()
                payload = await bot.wait_for("raw_reaction_add", check=check, timeout=30)
                dm_channel = await bot.fetch_channel(payload.channel_id)
                dm_message = await dm_channel.fetch_message(payload.message_id)
                if payload.emoji.name == "⭕" and dm_message.content.startswith("以下のユーザーに質問します"):
                    await asyncio.sleep(3)
                    if exit_flg: return
                    if user_exit_flg:
                        user_exit_flg = False
                        await asyncio.sleep(3)
                        raise A_error()
                    to_id = func.get_to_id(payload.user_id)
                    if to_id:
                        to_name = func.get_name_by_id(to_id)
                        to_user = await bot.fetch_user(to_id)
                        embed.description = f"「{user_name}」から「{to_name}」に質問です"
                        embed.set_footer(text= "質問時間は1分です\nまもなく始まります")
                        await message.edit(embed=embed)
                        fmsg = await user.send(f"まもなく「{to_name}」への質問が開始されます\n※まもなくミュートが外れます")
                        tmsg = await to_user.send(f"まもなく「{user_name}」からの質問が開始されます\n※まもなくミュートが外れます")
                        await asyncio.sleep(3)
                        if exit_flg: return
                        if user_exit_flg:
                            user_exit_flg = False
                            await asyncio.sleep(3)
                            raise A_error()
                        await unmute_select(user_id)
                        await unmute_select(to_id)
                        embed.set_footer(text="□"*6 +"\n残り時間は60秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        if exit_flg: return
                        if user_exit_flg:
                            user_exit_flg = False
                            await asyncio.sleep(3)
                            raise A_error()
                        embed.set_footer(text="■" +"□"*5 +"\n残り時間は50秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        if exit_flg: return
                        if user_exit_flg:
                            user_exit_flg = False
                            await asyncio.sleep(3)
                            raise A_error()
                        embed.set_footer(text="■"*2 +"□"*4 +"\n残り時間は40秒です")
                        await message.edit(embed=embed)
                        await fmsg.delete()
                        await tmsg.delete()
                        await asyncio.sleep(10)
                        if exit_flg: return
                        if user_exit_flg:
                            user_exit_flg = False
                            await asyncio.sleep(3)
                            raise A_error()
                        embed.set_footer(text="■"*3 +"□"*3 +"\n残り時間は30秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        if exit_flg: return
                        if user_exit_flg:
                            user_exit_flg = False
                            await asyncio.sleep(3)
                            raise A_error()
                        embed.set_footer(text="■"*4 +"□"*2 +"\n残り時間は20秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        if exit_flg: return
                        if user_exit_flg:
                            user_exit_flg = False
                            await asyncio.sleep(3)
                            raise A_error()
                        embed.set_footer(text="■"*5 +"□"*1 +"\n残り時間は10秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        await smsg.delete()
                        if exit_flg: return
                        if user_exit_flg:
                            user_exit_flg = False
                            await asyncio.sleep(3)
                            raise A_error()
                        embed.set_footer(text="■"*6 +"\n残り時間は0秒です")
                        await message.edit(embed=embed)
                        await mute_select(user_id)
                        await mute_select(to_id)
                        embed.description = f"「{user_name}」から「{to_name}」への質問が終わりました"
                        embed.set_footer(text="次の質問者へ移ります")
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        raise A_error()
                elif payload.emoji.name == "⏭️" and dm_message.content.startswith("質問をスキップする場合は"):
                    await asyncio.sleep(3)
                    user_exit_flg = False
                    break
            if exit_flg: return
            if user_exit_flg:
                user_exit_flg = False
                await asyncio.sleep(3)
                raise A_error()
        except A_error:
            pass
        except asyncio.TimeoutError:
            if exit_flg: return
            if user_exit_flg:
                user_exit_flg = False
                await asyncio.sleep(3)
                continue
            await clean_select_to_dm(user_id)
            await send_rand_to(user_id)
            func.random_select_to(user_id)
            to_id = func.get_to_id(user_id)
            to_name = func.get_name_by_id(to_id)
            to_user = await bot.fetch_user(to_id)
            fmsg = await user.send(f"まもなく「{to_name}」への質問が開始されます\n※まもなくミュートが外れます")
            tmsg = await to_user.send(f"まもなく「{user_name}」からの質問が開始されます\n※まもなくミュートが外れます")
            embed.description = f"「{user_name}」から「{to_name}」に質問です"
            embed.set_footer(text="■"*3 +"□"*3 +"\n質問時間は30秒です")
            await message.edit(embed=embed)
            if exit_flg: return
            if user_exit_flg:
                user_exit_flg = False
                await asyncio.sleep(3)
                continue
            await asyncio.sleep(3)
            await unmute_select(user_id)
            await unmute_select(to_id)
            await asyncio.sleep(10)
            if exit_flg: return
            if user_exit_flg:
                user_exit_flg = False
                await asyncio.sleep(3)
                continue            
            embed.set_footer(text="■"*4 +"□"*2 +"\n残り時間は20秒です")
            await message.edit(embed=embed)
            await asyncio.sleep(10)
            await fmsg.delete()
            await tmsg.delete()
            if exit_flg: return
            if user_exit_flg:
                user_exit_flg = False
                await asyncio.sleep(3)
                continue
            await clean_rand_to_dm(user_id)
            embed.set_footer(text="■"*5 +"□"*1 +"\n残り時間は10秒です")
            await message.edit(embed=embed)
            await asyncio.sleep(10)
            await smsg.delete()
            if exit_flg: return
            if user_exit_flg:
                user_exit_flg = False
                await asyncio.sleep(3)
                continue
            embed.set_footer(text="■"*6 +"\n残り時間は0秒です")
            await message.edit(embed=embed)
            await mute_select(user_id)
            await mute_select(to_id)
            embed.description = f"「{user_name}」から「{to_name}」への質問が終わりました"
            embed.set_footer(text="次の質問者へ移ります")
            await message.edit(embed=embed)
            await asyncio.sleep(3)
            if exit_flg: return
    embed.title = "質疑応答が終了しました"
    embed.color = 0x8B4513
    embed.description = ""
    embed.set_footer(text="✅を押して進行してください")
    await message.edit(embed=embed)
    await message.add_reaction('✅')

async def interview_tasks(message):
    global global_task
    global_task = asyncio.create_task(interview_operates(message))
    await global_task

async def will_operates(message):
    global exit_flg
    exit_flg = False
    embed = message.embeds[0]
    executed_id = func.get_exeid_by_sham()
    user = await bot.fetch_user(executed_id)
    embed.title = "遺言の時間です"
    embed.color = 0x8B4513
    embed.set_footer(text="□"*6+"\n遺言時間は1分です\nまもなく始まります")
    await message.edit(embed=embed)
    if exit_flg: return
    emsg = await user.send("※まもなくミュートが外れます")
    await asyncio.sleep(1)
    smsg = await user.send("遺言をスキップする場合は⏭️を押してください")
    await smsg.add_reaction('⏭️')
    await asyncio.sleep(1)
    await unmute_select(executed_id)
    if exit_flg: return
    embed.set_footer(text="□"*6 +"\n残り時間は60秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if exit_flg: return
    embed.set_footer(text="■"+"□"*5 +"\n残り時間は50秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if exit_flg: return
    embed.set_footer(text="■"*2 +"□"*4 +"\n残り時間は40秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if exit_flg: return
    await emsg.delete()
    embed.set_footer(text="■"*3 +"□"*3 +"\n残り時間は30秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if exit_flg: return
    embed.set_footer(text="■"*4 +"□"*2 +"\n残り時間は20秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if exit_flg: return
    embed.set_footer(text="■"*5 +"□"*1 +"\n残り時間は10秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if exit_flg: return
    embed.set_footer(text="■"*6 +"\n残り時間は0秒です")
    await message.edit(embed=embed)
    await mute_select(executed_id)
    await smsg.delete()
    await clean_will_dm(executed_id)
    await asyncio.sleep(3)
    if exit_flg: return
    embed.title = "処刑が執行されました"
    embed.color = 0x8B4513
    embed.description = ""
    embed.set_footer(text="✅を押して進行してください")
    await message.edit(embed=embed)
    await send_log(id=executed_id, flg=1)
    await user.send("あなたは処刑されました")
    await add_death_prefix(executed_id)
    await message.add_reaction('✅')

async def will_tasks(message):
    global global_task
    global_task = asyncio.create_task(will_operates(message))
    await global_task

async def persuasion_operates(message):
    global exit_flg
    exit_flg = False
    global user_exit_flg
    embed = message.embeds[0]
    embed.title = "弁明の時間です"
    embed.description = ""
    embed.set_footer(text="しばらくお待ちください")
    await message.edit(embed=embed)
    pre_executed_ids = func.get_vote_max_ids()
    random.shuffle(pre_executed_ids)
    for pre_executed_id in pre_executed_ids:
        user_exit_flg = False
        persuader = await bot.fetch_user(pre_executed_id)
        persuader_name = func.get_name_by_id(pre_executed_id)
        msg = await persuader.send("あなたの弁明の時間が始まります\n※まもなくミュートが外れます")
        await asyncio.sleep(1)
        smsg = await persuader.send("弁明をスキップする場合は⏭️を押してください")
        await smsg.add_reaction('⏭️')
        await asyncio.sleep(1)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message, msg)
            await asyncio.sleep(3)
            continue
        await unmute_select(pre_executed_id)
        embed.description = f"{persuader_name}による弁明です"
        embed.set_footer(text= "□"*6+"残り時間は1分です")
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message, msg)
            await asyncio.sleep(3)
            continue
        await asyncio.sleep(5)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message, msg)
            await asyncio.sleep(3)
            continue
        embed.set_footer(text= "■"+"□"*5+"残り時間は50秒です")
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message, msg)
            await asyncio.sleep(3)
            continue
        await asyncio.sleep(5)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message, msg)
            await asyncio.sleep(3)
            continue
        embed.set_footer(text= "■"*2+"□"*4+"残り時間は40秒です")
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message, msg)
            await asyncio.sleep(3)
            continue
        await asyncio.sleep(5)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message, msg)
            await asyncio.sleep(3)
            continue
        await msg.delete()
        embed.set_footer(text= "■"*3+"□"*3+"残り時間は30秒です")
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message)
            await asyncio.sleep(3)
            continue
        await asyncio.sleep(5)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message)
            await asyncio.sleep(3)
            continue
        embed.set_footer(text= "■"*4+"□"*2+"残り時間は20秒です")
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message)
            await asyncio.sleep(3)
            continue
        await asyncio.sleep(5)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message)
            await asyncio.sleep(3)
            continue
        embed.set_footer(text= "■"*5+"□"*1+"残り時間は10秒です")
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message)
            await asyncio.sleep(3)
            continue
        await asyncio.sleep(5)
        if exit_flg:
            return
        if user_exit_flg:
            await persuasion_skip(persuader_name, message)
            await asyncio.sleep(3)
            continue
        embed.set_footer(text= "■"*6+"残り時間は0秒です")
        await message.edit(embed=embed)
        await smsg.delete()
        await mute_select(pre_executed_id)
        embed.description = f"{persuader_name}による弁明が終わりました"
        embed.set_footer(text= "次に移行します\nしばらくお待ちください")
        await message.edit(embed=embed)
    embed.description = "全ての弁明が終わりました"
    embed.set_footer(text= "決選投票を始めます\n✅を押して進行してください")
    await message.edit(embed=embed)
    await message.add_reaction('✅')
    await clean_persuasion_dm(pre_executed_ids)

async def persuasion_tasks(message):
    global global_task
    global_task = asyncio.create_task(persuasion_operates(message))
    await global_task

async def persuasion_skip(persuader_name, message, msg = None):
    embed = message.embeds[0]
    if msg:
        await msg.delete()
    embed.description = f"{persuader_name}による弁明がスキップされました"
    embed.set_footer(text= "次に移行します\nしばらくお待ちください")
    await message.edit(embed=embed)

#### SYSTEM1 ####
async def add_wolf_room():
    wlf_ids = func.get_alivewolfs_ids()
    if len(wlf_ids) >= 2:
        guild = bot.get_guild(GUILD_ID)
        channel = discord.utils.get(guild.text_channels, id=WLF_CH_ID)
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages=True
        overwrite.send_messages=True
        overwrite.add_reactions=True
        for wlf_id in wlf_ids:
            member = guild.get_member(int(wlf_id))
            if not member.guild_permissions.administrator:
                try:
                    await channel.set_permissions(member, overwrite=overwrite)
                except:
                    pass

async def remove_all_werewolf_room():
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(WLF_CH_ID)
    members = []
    overwrite = discord.PermissionOverwrite()
    overwrite.read_messages=False
    overwrite.send_messages=False
    overwrite.add_reactions=False
    members = channel.members
    for member in members:
        if not member.guild_permissions.administrator:
            try:
                await channel.set_permissions(member, overwrite=overwrite)
            except:
                pass

async def send_log(id=None, name=None, vtx=None, flg=0):
    global day
    guild = bot.get_guild(GUILD_ID)
    channel = discord.utils.get(guild.text_channels, id=LOG_CH_ID)
    if vtx:
        log = f"投票結果\n```{vtx}```"
        await channel.send(log)
    elif flg == 0:
        if day == 0:
            log = "ゲーム開始\n...\n村民名簿\n>>> "
            with open('data.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
            for row in rows:
                log += (row['name'] + "\n")
            await channel.send(log.rstrip("\n"))
            day += 1
        else:
            await channel.send(f"□ {day}日目の朝を迎えた")
            day += 1
    elif flg == 1:
        if id:
            name = func.get_name_by_id(str(id))
            await channel.send(f"`「{name}」を処刑した`")
    elif flg == 2:
        if name:
            await channel.send(f"`「{name}」が殺された`")
        else:
            await channel.send("`昨夜は誰も殺されなかった`")
    elif flg == 3:
        await channel.send("人狼はいなくなった\n...\nゲーム終了")
    elif flg == 4:
        await channel.send("村人はいなくなった\n...\nゲーム終了")


#### DM ####
async def send_select_executed(user_id): # 処刑対象に投票してください
    exe_ids = func.select_ids_other_alives(user_id)
    name_list = func.get_name_list(exe_ids)
    user = await bot.fetch_user(user_id)
    list_message = "処刑対象に投票してください\n"
    for index, item in enumerate(name_list):
        if index < 14:
            list_message += f"{REACTION_EMOJIS_A[index]}: {item}\n"
    list_message += "リアクションで選択してください"
    sent_message = await user.send(list_message)
    for index in range(len(name_list)):
        await sent_message.add_reaction(REACTION_EMOJIS_A[index])

async def send_werewolf_operates():
    wolf_ids = func.get_alivewolfs_ids()
    if len(wolf_ids) == 1:
        user_id = wolf_ids[0]
        await send_werewolf_bite(user_id)
    elif len(wolf_ids) >= 2:
        await add_wolf_room()
        await send_werewolf_bite()

async def send_werewolf_bite(user_id=None): # 襲撃する対象を選んでください
    vil_ids = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['job'] != '人狼' and row['vital'] == '0':
                vil_ids.append(row['id'])
    vil_names = func.get_name_list(vil_ids)
    list_message = "襲撃する対象を選んでください\n"
    for index, item in enumerate(vil_names):
        if index < 14:
            list_message += f"{REACTION_EMOJIS_A[index]}: {item}\n"
    list_message += "リアクションで選択してください"
    if user_id:
        user = await bot.fetch_user(user_id)
        if user:
            sent_message = await user.send(list_message)
    else:
        guild = bot.get_guild(GUILD_ID)
        channel = discord.utils.get(guild.text_channels, id=WLF_CH_ID)
        sent_message = await channel.send(list_message)
    for index in range(len(vil_names)):
        await sent_message.add_reaction(REACTION_EMOJIS_A[index])

async def clean_werewolf_dm():
    wolf_ids = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['job'] == '人狼' and row['vital'] == '0':
                wolf_ids.append(row['id'])
    for user_id in wolf_ids:
        bot_messages = []
        user = await bot.fetch_user(user_id)
        dm_channel = user.dm_channel
        async for msg in dm_channel.history(limit=10):
            if msg.author.bot:
                bot_messages.append(msg)
        for msg in bot_messages:
            if msg.content.startswith("襲撃する対象を選んでください"):
                await msg.delete()

async def clean_select_to_dm(user_id):
    user = await bot.fetch_user(user_id)
    dm_channel = user.dm_channel
    async for msg in dm_channel.history(limit=10):
        if msg.author != bot.user:
            continue
        if msg.content.startswith("質問する相手") or msg.content.startswith("以下のユーザーに質問します") or msg.content.startswith("まもなく"):
            await msg.delete()

async def clean_persuasion_dm(ids):
    for pre_executed_id in ids:
        user = await bot.fetch_user(pre_executed_id)
        if user and user.dm_channel:
            dm_channel = user.dm_channel
            async for msg in dm_channel.history(limit=10):
                if msg.author != bot.user:
                    continue
                if msg.content.startswith("あなたの弁明") or msg.content.startswith("弁明をスキップ") or msg.content.startswith("処刑対象の候補に"):
                    await msg.delete()

async def clean_will_dm(user_id):
    user = await bot.fetch_user(user_id)
    if user and user.dm_channel:
        dm_channel = user.dm_channel
        async for msg in dm_channel.history(limit=10):
            if msg.author != bot.user:
                continue
            if msg.content.startswith("※まもなくミュートが") or msg.content.startswith("遺言をスキップ") or msg.content.startswith("あなたは処刑される事と"):
                await msg.delete()

async def send_select_to(user_id): # 質問する相手を選んでください
    to_ids = func.select_ids_other_alives(user_id)
    name_list = func.get_name_list(to_ids)
    user = await bot.fetch_user(user_id)
    list_message = "質問する相手を選んでください\n"
    for index, item in enumerate(name_list):
        if index < 14:
            list_message += f"{REACTION_EMOJIS_A[index]}: {item}\n"
    list_message += "リアクションで選択してください"
    sent_message = await user.send(list_message)
    for index in range(len(name_list)):
        await sent_message.add_reaction(REACTION_EMOJIS_A[index])

async def send_rand_to(user_id):
    user = await bot.fetch_user(user_id)
    dm_channel = user.dm_channel
    async for target_message in dm_channel.history(limit=10):
        if target_message.author != bot.user:
            continue
        if target_message.content.startswith("質問する相手を選んでください") or target_message.content.startswith("以下のユーザーに質問します"):
            await target_message.delete()
    await user.send("選択がなされなかったため対象がランダムに選択されます")

async def clean_rand_to_dm(user_id):
    user = await bot.fetch_user(user_id)
    dm_channel = user.dm_channel
    async for target_message in dm_channel.history(limit=10):
        if target_message.author != bot.user:
            continue
        if target_message.content.startswith("選択がなされなかったため"):
            await target_message.delete()
            break

async def clean_skip_inter_dm(user_id):
    user = await bot.fetch_user(user_id)
    dm_channel = user.dm_channel
    async for msg in dm_channel.history(limit=10):
        if msg.author != bot.user:
            continue
        if msg.content.startswith("質問をスキップする場合は"):
            await msg.delete()
            break

async def send_shaman_operates():
    user_id = None
    sham_id = None
    sham_color = None
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row['job'] == '霊媒師' and row['vital'] == '0':
                user_id = row['id']
                break
        for row in rows:
            if row['vital'] == '1' and row['sham'] == '1':
                sham_id = row['id']
                sham_color = row['col']
                row['sham'] = '0'
                break
    with open('status.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    if user_id:
        user = await bot.fetch_user(user_id)
        if sham_id:
            sham_name = func.get_name_by_id(sham_id)
            if sham_color == "1":
                await user.send(f"処刑された「{sham_name}」は「黒」でした")
            else:
                await user.send(f"処刑された「{sham_name}」は「白」でした")

async def send_fortune_operates(): # 占う対象を選んでください
    user_id = None
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row['job'] == '占い師' and row['vital'] == '0':
                user_id = row['id']
                break
        if user_id:
            fortune_ids = []
            for row in rows:
                if row['vital'] == '0' and row['ftnd'] != '1':
                    fortune_ids.append(row['id'])
    if user_id:
        user = await bot.fetch_user(user_id)
        if fortune_ids:
            fortune_names = func.get_name_list(fortune_ids)
            list_message = "占う対象を選んでください\n"
            for index, item in enumerate(fortune_names):
                if index < 14:
                    list_message += f"{REACTION_EMOJIS_A[index]}: {item}\n"
            list_message += "リアクションで選択してください"
            sent_message = await user.send(list_message)
            for index in range(len(fortune_names)):
                await sent_message.add_reaction(REACTION_EMOJIS_A[index])
        else:
            dm_channel = user.dm_channel
            has_target_message = False
            async for target_message in dm_channel.history(limit=20):
                if target_message.author != bot.user:
                    continue
                if target_message.content.startswith("もう占える対象がいません"):
                    has_target_message = True
                    break
            if not has_target_message:
                await user.send("もう占える対象がいません")

async def send_guard_operates(): # 保護する対象を選んでください
    user_id = None
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row['job'] == '騎士' and row['vital'] == '0':
                user_id = row['id']
                break
    if user_id:
        grd_ids = func.select_grd_ids(user_id)
        if grd_ids:
            grd_alives_names = func.get_name_list(grd_ids)
            user = await bot.fetch_user(user_id)
            list_message = "保護する対象を選んでください\n"
            for index, item in enumerate(grd_alives_names):
                if index < 14:
                    list_message += f"{REACTION_EMOJIS_A[index]}: {item}\n"
            list_message += "リアクションで選択してください"
            sent_message = await user.send(list_message)
            for index in range(len(grd_alives_names)):
                await sent_message.add_reaction(REACTION_EMOJIS_A[index])

async def send_fortune_result(id_number, user_id): # 占いの結果
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row['id'] == id_number:
                fortune_color = row['col']
                row['ftnd'] = '1'
                break
    with open('status.csv', 'w', newline='') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    fortune_name = func.get_name_by_id(id_number)
    user = await bot.fetch_user(user_id)
    if user:
        if fortune_color == "1":
            await user.send(f"占いの結果、「{fortune_name}」は「黒」でした")
        else:
            await user.send(f"占いの結果、「{fortune_name}」は「白」でした")

async def send_guardian_result():
    user_id = None
    grd_flg = False
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (row['grd'] == '1' and row['kil'] == '1') or (row['grd'] == '2' and row['kil'] == '1'):
                grd_flg = True
                break
        for row in reader:
            if row['job'] == '騎士':
                user_id = row['id']
                break
    if grd_flg and user_id:
        user = await bot.fetch_user(user_id)
        if user:
            await user.send("あなたの功績により村人が1人救われました")

async def send_werewolf_messages():
    werewolf_ids = func.get_alivewolfs_ids()
    if len(werewolf_ids) >= 2:
        await add_wolf_room()
        guild = bot.get_guild(GUILD_ID)
        channel = discord.utils.get(guild.text_channels, id=WLF_CH_ID)
        async for message in channel.history(limit=50):
            await message.delete()
            await asyncio.sleep(0.5)
        await channel.send(">>> 人狼部屋にようこそ\n人狼が複数いる夜はこの部屋が開放され、\nこちらに襲撃先の案内が送られます\n"
                            +"襲撃先は人狼全員で選択してください\nここから下が今回の人狼チャットです")
    werewolf_names = func.get_name_list(werewolf_ids)
    if werewolf_names:
        wolfnames_text = ", ".join(werewolf_names)
        for user_id in werewolf_ids:
            user = await bot.fetch_user(user_id)
            if user:
                message = "あなたは人狼です"
                file_name = "image/werewolf.jpg"
                file = discord.File(file_name, filename=file_name)
                await user.send(message, file=file)                
                await user.send(f"人狼は{wolfnames_text}です\n<#{WLF_CH_ID}>")
                await asyncio.sleep(1)
                sent_msg = await user.send("準備ができたら🆗をおしてください")
                await sent_msg.add_reaction("🆗")
                await asyncio.sleep(1)

async def send_citizen_messages():
    user_ids = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['job'] == '市民':
                user_ids.append(row['id'])
    if user_ids:
        for user_id in user_ids:
            user = await bot.fetch_user(user_id)
            if user:
                message = "あなたは市民です"
                file_name = "image/citizen.jpg"
                file = discord.File(file_name, filename=file_name)
                await user.send(message, file=file)
                sent_message = await user.send("確認ができたら🆗をおしてください")
                await sent_message.add_reaction("🆗")
                await asyncio.sleep(1)

async def send_mad_messages():
    user_id = None
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['job'] == '狂人':
                user_id = int(row['id'])
                break
    if user_id:
        user = await bot.fetch_user(user_id)
        if user:
            message = "あなたは狂人です"
            file_name = "image/mad.jpg"
            file = discord.File(file_name, filename=file_name)
            await user.send(message, file=file)
            sent_message = await user.send("確認ができたら🆗をおしてください")
            await sent_message.add_reaction("🆗")

async def send_guardian_messages():
    user_id = None
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['job'] == '騎士':
                user_id = row['id']
                break
    if user_id:
        user = await bot.fetch_user(user_id)
        if user:
            message = "あなたは騎士です"
            file_name = "image/guardian.jpg"
            file = discord.File(file_name, filename=file_name)
            await user.send(message, file=file)
            sent_message = await user.send("確認ができたら🆗をおしてください")
            await sent_message.add_reaction("🆗")

async def send_fortune_messages():
    user_id = None
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['job'] == '占い師':
                user_id = int(row['id'])
                break
    if user_id:
        user = await bot.fetch_user(user_id)
        if user:
            message = "あなたは占い師です"
            file_name = "image/fortune.jpg"
            file = discord.File(file_name, filename=file_name)
            await user.send(message, file=file)
            selected_name = func.select_random_white()
            await user.send(f"神のお告げにより「{selected_name}」が「白」であると分かりました")
            await asyncio.sleep(1)
            sent_message = await user.send("確認ができたら🆗をおしてください")
            await sent_message.add_reaction("🆗")

async def send_shaman_messages():
    user_id = None
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['job'] == '霊媒師':
                user_id = int(row['id'])
                break
    if user_id:
        user = await bot.fetch_user(user_id)
        if user:
            message = "あなたは霊媒師です"
            file_name = "image/shaman.jpg"
            file = discord.File(file_name, filename=file_name)
            await user.send(message, file=file)
            sent_message = await user.send("確認ができたら🆗をおしてください")
            await sent_message.add_reaction("🆗")

async def check_killed_victim():
    rows = []
    alive_wolf_ids = []
    killed_id = None
    grd_flg = False
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row['vital'] == '0' :
                if row['kil'] == '1' and row['grd'] == '0':
                    killed_id = row['id']
                    row['vital'] = '1'
                elif (row['kil'] == '1' and row['grd'] == '1') or (row['kil'] == '1' and row['grd'] == '2'):
                    grd_flg = True
                elif row['job'] == '人狼':
                    alive_wolf_ids.append(row['id'])
    with open('status.csv', 'w', newline='') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    if killed_id:
        user = await bot.fetch_user(killed_id)
        await user.send("あなたは襲撃され殺されました")
        await add_death_prefix(killed_id)
        await add_rip_role(killed_id)
        killed_name = func.get_name_by_id(killed_id)
        for alive_wolf_id in alive_wolf_ids:
            live_wolf = await bot.fetch_user(alive_wolf_id)
            await live_wolf.send(f"「{killed_name}」の襲撃に成功しました")
        return killed_name
    elif grd_flg:
        if len(alive_wolf_ids) >= 2:
            guild = bot.get_guild(GUILD_ID)
            channel = discord.utils.get(guild.text_channels, id=WLF_CH_ID)
            await channel.send("襲撃に失敗しました")
        else:
            alive_wolf_id = alive_wolf_ids[0]
            live_wolf = await bot.fetch_user(alive_wolf_id)
            await live_wolf.send("襲撃に失敗しました")
        return None
    return None

async def fin_vote_operates():
    alives_ids = func.get_alives_ids()
    prexe_ids = func.get_vote_max_ids()
    prexename_list = func.get_name_list(prexe_ids)
    vote_ids = [x for x in alives_ids if x not in prexe_ids]
    for user_id in vote_ids:
        user = await bot.fetch_user(user_id)
        list_message = "処刑対象に投票してください\n"
        for index, item in enumerate(prexename_list):
            if index < 14:
                list_message += f"{REACTION_EMOJIS_A[index]}: {item}\n"
        list_message += "リアクションで選択してください"
        sent_message = await user.send(list_message)
        for index in range(len(prexename_list)):
            await sent_message.add_reaction(REACTION_EMOJIS_A[index])

async def add_rip_role(user_id):
    guild = bot.get_guild(GUILD_ID)
    member = guild.get_member(int(user_id))
    if member:
        role = guild.get_role(RIP_RL_ID)
        await member.add_roles(role)
        await member.send(f"<#{RIP_CH_ID}>")

#### SYSTEM2 ####
async def add_death_prefix(user_id):
    guild = bot.get_guild(GUILD_ID)
    member = guild.get_member(int(user_id))
    if member:
        display_name = f"💀{member.display_name}"
        try:
            await member.edit(nick=display_name)
        except:
            pass

async def remove_death_prefix():
    voice_channel = bot.get_channel(VOICE_CH_ID)
    members = voice_channel.members
    for member in members:
        if member.display_name.startswith("💀"):
            new_display_name = member.display_name[1:]
            try:
                await member.edit(nick=new_display_name)
            except discord.Forbidden:
                continue
            except:
                pass

async def send_rip_st():
    guild = bot.get_guild(GUILD_ID)
    channel = discord.utils.get(guild.text_channels, id=RIP_CH_ID)
    await channel.send(">>> 墓場にようこそ\nここから下が今回の墓場チャットです")

async def remove_all_rip_role():
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(RIP_CH_ID)
    role = guild.get_role(RIP_RL_ID)
    members_with_role = [m for m in channel.members if role in m.roles]
    for member in members_with_role:
        await member.remove_roles(role)

async def task_kill():
    global global_task
    global exit_flg
    exit_flg = True
    if global_task:
        global_task.cancel()
        global_task = None

def reset_global():
    global global_task, exit_flg, m_exit_flg, user_exit_flg, remain_vote_repeat, day
    global_task = None
    exit_flg = False
    m_exit_flg = False
    user_exit_flg = False
    remain_vote_repeat = MAX_VOTE_REPEAT
    day = 0

#### MAIN ####
@bot.event
async def on_raw_reaction_add(payload):
    global main_emb_message_id
    global remain_vote_repeat
    if payload.user_id == bot.user.id:
        return
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if message.author != bot.user:
        return
    elif isinstance(channel, discord.TextChannel):
        member = channel.guild.get_member(payload.user_id)
        if message.embeds:
            embed = message.embeds[0]
        if payload.emoji.name == '❌':
            await message.remove_reaction(payload.emoji, member)
            await message.delete()
        elif message.content.startswith("襲撃する対象を選んでください"): # 以下のユーザーを襲撃します
            wolf_count = len(func.get_alivewolfs_ids())
            messages = message.content.split("\n")
            for i in range(len(REACTION_EMOJIS_A)):
                if payload.emoji.name == REACTION_EMOJIS_A[i]:
                    count = 0
                    for reaction in message.reactions:
                        if str(reaction.emoji) == REACTION_EMOJIS_A[i]:
                            count = reaction.count
                    if count == wolf_count + 1:
                        selected_line = messages[i+1]
                        if selected_line:
                            result = selected_line.split(": ")[-1]
                            sent_message = await channel.send(f"以下のユーザーを襲撃します\n{result}")
                            await sent_message.add_reaction(REACTION_EMOJIS_B[0])
                            await sent_message.add_reaction(REACTION_EMOJIS_B[1])
                            break
        elif message.content.startswith("以下のユーザーを襲撃します"):
            if payload.emoji.name == '⭕':
                target_name = message.content.split('\n')[1]
                await message.delete()
                dm_channel = await bot.fetch_channel(payload.channel_id)
                async for msg in dm_channel.history(limit=30):
                    if msg.author != bot.user:
                        continue
                    if msg.content.startswith("襲撃する対象を選んでください"):
                        await msg.delete()
                        break
                target_id = func.get_id_by_name(target_name)
                await dm_channel.send(f"「{target_name}」を襲撃しました")
                func.update_status(target_id, 1)
                alives_count = func.count_alives()
                channel = await bot.fetch_channel(TXT_CH_ID)
                target_message = await channel.fetch_message(main_emb_message_id)
                target_embed = target_message.embeds[0]
                if target_embed:
                    check_count = func.update_check_count_wolf()
                    if check_count == alives_count:
                        new_embed = target_embed.copy()
                        new_embed.set_footer(text="✅を押して進行してください")
                        await target_message.edit(embed=new_embed)
                        await target_message.add_reaction('✅')
            elif payload.emoji.name == '❌':
                await message.delete()
        elif payload.emoji.name == '✋' and embed:
            await message.remove_reaction(payload.emoji, member)
            if payload.message_id != main_emb_message_id:
                embed.set_footer(text="この埋め込みは現在ACTIVEではありません\n`!act`を使ってACTIVATEするか\n新しい埋め込みを作成してください")
                await message.edit(embed=embed)
                await message.add_reaction('❌')
                return
            user_mention = f'<@{payload.user_id}>'
            new_description = embed.description
            if user_mention not in new_description:
                dsc_lines = new_description.rsplit("\n", 1)
                new_description = f'{dsc_lines[0]}\n{user_mention}\n{dsc_lines[1]}' 
            else:
                new_description = embed.description.replace(f'\n{user_mention}', '')
            updated_embed = embed.copy()
            updated_embed.description = new_description
            await message.edit(embed=updated_embed)
        elif payload.emoji.name == '🗣️' and embed:
            await message.remove_reaction(payload.emoji, member)
            if payload.message_id != main_emb_message_id:
                embed.set_footer(text="この埋め込みは現在ACTIVEではありません\n`!act`を使ってACTIVATEするか\n新しい埋め込みを作成してください")
                await message.edit(embed=embed)
                await message.add_reaction('❌')
                return
            vc = await bot.fetch_channel(VOICE_CH_ID)
            if vc:
                member_ids = [member.id for member in vc.members]
                if member_ids:
                    new_description = embed.description
                    dsc_lines = new_description.rsplit("\n", 1)
                    for member_id in member_ids:
                        user_mention = f'<@{member_id}>'
                        if user_mention not in dsc_lines[0]:
                            dsc_lines[0] += f'\n{user_mention}'
                    updated_embed = embed.copy()
                    updated_embed.description = "\n".join(dsc_lines)
                    await message.edit(embed=updated_embed)
        elif payload.emoji.name == '🆗' and embed:
            await message.remove_reaction(payload.emoji, member)
            if payload.message_id != main_emb_message_id:
                embed.set_footer(text="この埋め込みは現在ACTIVEではありません\n`!act`を使ってACTIVATEするか\n新しい埋め込みを作成してください")
                await message.edit(embed=embed)
                await message.add_reaction('❌')
                return
            if embed.title == "人狼メンバー設定":
                await message.clear_reactions()
                embed.title = "ゲームを開始します"
                embed.color = 0x660000
                embed.set_footer(text='VCにメンバーが集まったら🆗を押してください')
                await message.edit(embed=embed)
                await message.add_reaction('🆗')
            elif embed.title == "ゲームを開始します":
                vc = bot.get_channel(VOICE_CH_ID)
                if vc:
                    member_ids = {member.id for member in vc.members}
                    with open('data.csv', 'r', newline='') as file:
                        reader = csv.DictReader(file)
                        csv_ids = {int(row['id']) for row in reader}
                    if csv_ids.issubset(member_ids):
                        await message.clear_reactions()
                        embed.description = ""
                        embed.set_footer(text="✅を押すと役職が配られます")
                        await message.edit(embed=embed)
                        await message.add_reaction('✅')
                    else:
                        embed.set_footer(text="VCにメンバーが集まっていません")
                        await message.edit(embed=embed)
        elif payload.emoji.name == '✅' and embed:
            await message.remove_reaction(payload.emoji, member)
            if payload.message_id != main_emb_message_id:
                embed.set_footer(text="この埋め込みは現在ACTIVEではありません\n`!act`を使ってACTIVATEするか\n新しい埋め込みを作成してください")
                await message.edit(embed=embed)
                await message.add_reaction('❌')
                return
            elif embed.title == "人狼メンバー設定":
                await remove_all_werewolf_room()
                await remove_all_rip_role()
                await remove_death_prefix()
                user_ids = re.findall(r'@[0-9]{18,20}', embed.description)
                user_ids = list(map(lambda x: int(x.replace('@', '')), user_ids))
                if len(user_ids) <= 3:
                    embed.set_footer(text="人数が不足しています\nメンバーを追加してください")
                    await message.edit(embed=embed)
                else:
                    embed.set_footer(text="読み込み中です")
                    await message.edit(embed=embed)
                    existing_names = []
                    with open("data_temp.csv", "w", newline="") as temp_file:
                        writer = csv.writer(temp_file)
                        writer.writerow(["name", "id"])
                    os.replace("data_temp.csv", "data.csv")
                    guild = bot.get_guild(GUILD_ID)
                    new_embed = embed.copy()
                    dsc_lines = new_embed.description.split("\n")
                    for index, user_id in enumerate(user_ids, start=1):
                        member = guild.get_member(int(user_id))
                        if member:
                            user = await bot.fetch_user(user_id)
                            display_name = member.display_name if member.display_name else user.display_name
                            if display_name:
                                if display_name in existing_names:
                                    embed.set_footer(text="ERROR\n名前が重複するメンバーが含まれています")
                                    await message.edit(embed=embed)
                                    return
                                else:
                                    existing_names.append(display_name)
                                    with open("data.csv", "a", newline="") as file:
                                        writer = csv.writer(file)
                                        writer.writerow([display_name,user_id])
                                    dsc_lines[index] += f" -> {display_name}"
                            else:
                                embed.set_footer(text="ERROR\n名前が取得できないメンバーが含まれています")
                                await message.edit(embed=embed)
                                return
                    new_embed.description = "\n".join(dsc_lines)
                    new_embed.set_footer(text="表示名を確認して🆗を押してください")
                    await message.edit(embed=new_embed)
                    await message.add_reaction('🆗')
            elif embed.title == "ゲームを開始します":
                await message.clear_reactions()
                reset_global()
                name_count = func.get_row_count('data.csv')
                embed.title = "おそろしい夜がやってきました"
                embed.color = 0xFF0000
                embed.description = "**LOADING** "+"□"*name_count
                embed.set_footer(text="配役確認中です\nLOADINGが完了するまでお待ちください")
                await message.edit(embed=embed)
                await remove_all_werewolf_room()
                await remove_all_rip_role()
                await remove_death_prefix()
                func.ini_settings()
                await mute_alives()
                func.assign_roles()
                await send_werewolf_messages()
                await asyncio.sleep(0.5)
                await send_mad_messages()
                await asyncio.sleep(0.5)
                await send_guardian_messages()
                await asyncio.sleep(0.5)
                await send_fortune_messages()
                await asyncio.sleep(0.5)
                await send_shaman_messages()
                await asyncio.sleep(0.5)
                await send_citizen_messages()
                await asyncio.sleep(0.5)
                await send_log()
                await send_rip_st()
            elif embed.title == "おそろしい夜がやってきました":
                await message.clear_reactions()
                embed.title = "朝を迎えました"
                embed.color = 0x87CEEB
                embed.description = ""
                embed.set_footer(text="ステータスの確認中です")
                await message.edit(embed=embed)
                await send_log()
                await asyncio.sleep(2)
                killed_name = await check_killed_victim()
                await remove_all_werewolf_room()
                flg_game = func.check_game_status()
                if flg_game == 2:
                    names, jobs = func.get_name_and_job_lists()
                    embed.title = "人狼はいなくなりました"
                    embed.description = "村人陣営の勝利です\n"+"-"*23
                    for name, job in zip(names, jobs):
                        embed.description += f"\n{name} {job}"
                    await send_log(flg=3)
                    embed.set_footer(text="同じメンバーで次のゲームを始める場合は✅を押してください")
                    await message.edit(embed=embed)
                    await unmute_all()
                    await remove_all_rip_role()
                    await remove_death_prefix()
                    await message.add_reaction('✅')
                elif flg_game == 1:
                    names, jobs = func.get_name_and_job_lists()
                    embed.title = "村人は全員人狼に食べられました"
                    embed.description = "人外陣営の勝利です\n"+"-"*23
                    for name, job in zip(names, jobs):
                        embed.description += f"\n{name} {job}"
                    embed.color = 0x660000
                    await send_log(flg=4)
                    embed.set_footer(text="同じメンバーで次のゲームを始める場合は✅を押してください")
                    await message.edit(embed=embed)
                    await unmute_all()
                    await remove_all_werewolf_room()
                    await remove_all_rip_role()
                    await remove_death_prefix()
                    await message.add_reaction('✅')
                elif flg_game == 0:
                    alives_count = func.count_alives()
                    if killed_name:
                        embed.description = f"「{killed_name}」が無残な姿で発見されました\n\n生存者は{alives_count}人です"
                        await send_log(name=killed_name, flg=2)
                    else:
                        await send_guardian_result()
                        await send_log(flg=2)
                        embed.description = f"昨夜の犠牲者はいませんでした\n\n生存者は{alives_count}人です"
                    embed.set_footer(text="会議を始めてください\nまもなくミュートが外れます")
                    await message.edit(embed=embed)
                    await asyncio.sleep(1)
                    await unmute_alives()
                    await discussion_tasks(message)
            elif embed.title == "会議の時間です" or embed.title == "朝の会議をスキップしました":
                await message.clear_reactions()
                await interview_tasks(message)
            elif embed.title == "人狼はいなくなりました" or embed.title == "村人は全員人狼に食べられました":
                await message.clear_reactions()
                embed.title = "ゲームを開始します"
                embed.color = 0x660000
                embed.description = ""
                embed.set_footer(text='VCにメンバーが集まったら🆗を押してください')
                await message.edit(embed=embed)
                await message.clear_reactions()
                await message.add_reaction('🆗')
            elif embed.title == "質疑応答が終了しました" or embed.title == "質疑応答をスキップしました":
                await message.clear_reactions()
                func.set_vote_data()
                func.reset_check_column()
                alives_count = func.count_alives()
                embed.title = "1名を選んで処刑します"
                embed.color = 0x8B4513
                embed.description = "**LOADING** "+"□"*alives_count
                embed.set_footer(text="投票先をきめてください")
                await message.edit(embed=embed)
                vote_ids = func.get_alives_ids()
                for user_id in vote_ids:
                    await send_select_executed(user_id)
                    await asyncio.sleep(0.3)
                embed.set_footer(text="投票先の集計中です\nLOADINGが完了するまでお待ちください")
                await message.edit(embed=embed)
            elif embed.title == "投票が完了しました":
                await message.clear_reactions()
                embed.description = "集計中です"
                embed.set_footer(text="しばらくお待ちください")
                pre_executed_ids = func.get_vote_max_ids()
                vote_dsc = func.mk_vote_dsc()
                alives_count = func.count_alives()
                if len(pre_executed_ids) == alives_count:
                    embed.title = "全員同率の投票となりました"
                    embed.description = f"投票結果\n{vote_dsc}\n \n投票をやり直してください"
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                    await send_log(vtx=vote_dsc)
                    await message.add_reaction('✅')
                elif len(pre_executed_ids) > 1 and remain_vote_repeat != 0:
                    for pre_executed_id in pre_executed_ids:
                        pre_exer = await bot.fetch_user(pre_executed_id)
                        await pre_exer.send("処刑対象の候補になりました\n弁明の準備をしてください")
                        await asyncio.sleep(0.3)
                    remain_vote_repeat -= 1
                    embed.title = "最多得票者が複数となりました"
                    embed.description = f"投票結果\n{vote_dsc}\n \n弁明の時間に移ります"
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                    await send_log(vtx=vote_dsc)
                    await message.add_reaction('✅')
                else:
                    if len(pre_executed_ids) >= 2 and remain_vote_repeat == 0:
                        embed.title = "最多得票者が同率でした"
                        embed.description = "1人がランダムで選ばれ処刑されます"
                        embed.set_footer(text="しばらくお待ちください")
                        await message.edit(embed=embed)
                        random.shuffle(pre_executed_ids)
                        await asyncio.sleep(3)
                    executed_id = pre_executed_ids[0]
                    func.update_status(executed_id, 5)
                    exer = await bot.fetch_user(executed_id)
                    await exer.send("あなたは処刑される事となりました\n遺言を残してください")
                    remain_vote_repeat = MAX_VOTE_REPEAT
                    exer_name = func.get_name_by_id(executed_id)
                    embed.title = "処刑対象が決定しました"
                    embed.color = 0x8B4513
                    embed.description = f"投票結果\n{vote_dsc}\n \n{exer_name}が処刑されることになりました\n遺言の時間に移ります"
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                    await send_log(vtx=vote_dsc)
                    await message.add_reaction('✅')
            elif embed.title == "処刑対象が決定しました":
                await message.clear_reactions()
                func.reset_fortune()
                await will_tasks(message)
            elif embed.title == "処刑が執行されました" or embed.title == "遺言がスキップされ処刑が執行されました":
                await message.clear_reactions()
                embed.title = "おそろしい夜がやってきました"
                embed.color = 0xFF0000
                embed.description = "夜の行動を選択中です"
                embed.set_footer(text="朝を迎えるまでしばらくお待ちください")
                await message.edit(embed=embed)
                await add_wolf_room()
                func.reset_check_column()
                func.reset_flg_status()
                await asyncio.sleep(1)
                await send_shaman_operates()
                await asyncio.sleep(1)
                check_count = func.update_check_count_other()
                alives_count = func.count_alives()
                if check_count == alives_count:
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                else:
                    await send_werewolf_operates()
                    await asyncio.sleep(1)
                    await send_fortune_operates()
                    await asyncio.sleep(1)
                    await send_guard_operates()
            elif embed.title.startswith("弁明"):
                await message.clear_reactions()
                alives_count = func.count_alives()
                func.set_vote_data(2)
                func.reset_check_column()
                row_count = func.get_row_count('vote.csv')
                vote_count = alives_count - row_count
                embed.title = "決選投票を始めます"
                embed.description = "**LOADING** " + "□"*vote_count
                embed.set_footer(text="しばらくお待ちください")
                await message.edit(embed=embed)
                await fin_vote_operates()
            elif embed.title == "最多得票者が複数となりました":
                await message.clear_reactions()
                await persuasion_tasks(message)
            elif embed.title == "全員同率の投票となりました":
                await message.clear_reactions()
                func.set_vote_data()
                func.reset_check_column()
                alives_count = func.count_alives()
                embed.title = "1名を選んで処刑します"
                embed.color = 0x8B4513
                embed.description = "**LOADING** "+"□"*alives_count
                embed.set_footer(text="投票先をきめてください")
                await message.edit(embed=embed)
                vote_ids = func.get_alives_ids()
                for user_id in vote_ids:
                    await send_select_executed(user_id)
                    await asyncio.sleep(0.3)
                embed.set_footer(text="投票先の集計中です\nLOADINGが完了するまでお待ちください")
                await message.edit(embed=embed)

    elif isinstance(channel, discord.DMChannel):
        global user_exit_flg
        user = await bot.fetch_user(payload.user_id)
        if payload.emoji.name == '🆗':
            if message.content.startswith("確認ができたら") or message.content.startswith("準備ができたら"):
                await message.delete()
                channel = await bot.fetch_channel(TXT_CH_ID)
                target_message = await channel.fetch_message(main_emb_message_id)
                target_embed = target_message.embeds[0]
                if target_embed:
                    check_count = func.update_check_count(payload)
                    name_count = func.get_row_count('data.csv')
                    new_embed = target_embed.copy()
                    if check_count == name_count:
                        new_embed.description = "**LOADING** "+"■"*check_count
                        new_embed.set_footer(text="配役の確認が完了しました\n✅を押して進行してください")
                        await target_message.edit(embed=new_embed)
                        await target_message.add_reaction('✅')
                    else:
                        new_embed.description = "**LOADING** "+"■"*check_count + "□"*(name_count - check_count)
                        await target_message.edit(embed=new_embed)
        elif payload.emoji.name == '⏭️' and message.content.startswith("質問をスキップする場合は"):
            await message.delete()
            user_exit_flg = True
            channel = await bot.fetch_channel(TXT_CH_ID)
            target_message = await channel.fetch_message(main_emb_message_id)
            target_embed = target_message.embeds[0]
            user_name = func.get_name_by_id(payload.user_id)
            target_embed.description = f"「{user_name}」が質問をスキップしました"
            target_embed.set_footer(text="次の質問者へ移ります")
            await target_message.edit(embed=target_embed)
            await mute_select(payload.user_id)
            to_id = func.get_to_id(payload.user_id)
            if to_id:
                await mute_select(to_id)
            await clean_select_to_dm(payload.user_id)
            await clean_rand_to_dm(payload.user_id)
            if to_id:
                await clean_select_to_dm(to_id)
            msg = await user.send("あなたの質問の時間がスキップされました")
            await asyncio.sleep(5)
            if msg:
                await msg.delete()
        elif payload.emoji.name == '⏭️' and message.content.startswith("弁明をスキップする場合は"):
            await message.delete()
            user_exit_flg = True
            msg = await user.send("あなたの弁明がスキップされます")
            await mute_select(payload.user_id)
            await clean_persuasion_dm([payload.user_id])
            await asyncio.sleep(5)
            if msg:
                await msg.delete()
        elif payload.emoji.name == '⏭️' and message.content.startswith("遺言をスキップする場合は"):
            await message.delete()
            await task_kill()
            await mute_select(payload.user_id)
            channel = await bot.fetch_channel(TXT_CH_ID)
            target_message = await channel.fetch_message(main_emb_message_id)
            target_embed = target_message.embeds[0]
            await clean_will_dm(payload.user_id)
            msg = await user.send("遺言がスキップされ処刑が執行されました")
            await add_death_prefix(payload.user_id)
            await add_rip_role(payload.user_id)
            await send_log(id=payload.user_id, flg=1)
            target_embed.title = "処刑が執行されました"
            target_embed.color = 0x8B4513
            target_embed.description = ""
            target_embed.set_footer(text="✅を押して進行してください")
            await target_message.edit(embed=target_embed)
            await target_message.add_reaction('✅')
            await asyncio.sleep(5)
            if msg:
                await msg.delete()
        
        elif message.content.startswith("処刑対象に投票してください"): # 以下のユーザーに投票します
            user = await bot.fetch_user(payload.user_id)
            messages = message.content.split("\n")
            for i in range(len(REACTION_EMOJIS_A)):
                if payload.emoji.name == REACTION_EMOJIS_A[i]:
                    selected_line = messages[i+1]
                    if selected_line:
                        result = selected_line.split(": ")[-1]
                        sent_message = await user.send(f"以下のユーザーに投票します\n{result}")
                        await sent_message.add_reaction(REACTION_EMOJIS_B[0])
                        await sent_message.add_reaction(REACTION_EMOJIS_B[1])
                        break
        elif message.content.startswith("襲撃する対象を選んでください"): # 以下のユーザーを襲撃します
            messages = message.content.split("\n")
            for i in range(len(REACTION_EMOJIS_A)):
                if payload.emoji.name == REACTION_EMOJIS_A[i]:
                    selected_line = messages[i+1]
                    if selected_line:
                        result = selected_line.split(": ")[-1]
                        sent_message = await user.send(f"以下のユーザーを襲撃します\n{result}")
                        await sent_message.add_reaction(REACTION_EMOJIS_B[0])
                        await sent_message.add_reaction(REACTION_EMOJIS_B[1])
                        break
        elif message.content.startswith("占う対象を選んでください"): # 以下のユーザーを占います
            messages = message.content.split("\n")
            for i in range(len(REACTION_EMOJIS_A)):
                if payload.emoji.name == REACTION_EMOJIS_A[i]:
                    selected_line = messages[i+1]
                    if selected_line:
                        result = selected_line.split(": ")[-1]
                        sent_message = await user.send(f"以下のユーザーを占います\n{result}")
                        await sent_message.add_reaction(REACTION_EMOJIS_B[0])
                        await sent_message.add_reaction(REACTION_EMOJIS_B[1])
                        break
        elif message.content.startswith("保護する対象を選んでください"): # 以下のユーザーを守ります
            messages = message.content.split("\n")
            for i in range(len(REACTION_EMOJIS_A)):
                if payload.emoji.name == REACTION_EMOJIS_A[i]:
                    selected_line = messages[i+1]
                    if selected_line:
                        result = selected_line.split(": ")[-1]
                        sent_message = await user.send(f"以下のユーザーを守ります\n{result}")
                        await sent_message.add_reaction(REACTION_EMOJIS_B[0])
                        await sent_message.add_reaction(REACTION_EMOJIS_B[1])
                        break
        elif message.content.startswith("質問する相手を選んでください"): # 以下のユーザーに質問します
            messages = message.content.split("\n")
            for i in range(len(REACTION_EMOJIS_A)):
                if payload.emoji.name == REACTION_EMOJIS_A[i]:
                    selected_line = messages[i+1]
                    if selected_line:
                        result = selected_line.split(": ")[-1]
                        sent_message = await user.send(f"以下のユーザーに質問します\n{result}")
                        await sent_message.add_reaction(REACTION_EMOJIS_B[0])
                        await sent_message.add_reaction(REACTION_EMOJIS_B[1])
                        break

        elif message.content.startswith("以下のユーザーに投票します"):
            if payload.emoji.name == '⭕':
                target_name = message.content.split('\n')[1]
                await message.delete()
                dm_channel = await bot.fetch_channel(payload.channel_id)
                async for msg in dm_channel.history(limit=10):
                    if msg.author != bot.user:
                        continue
                    if msg.content.startswith("処刑対象に投票してください"):
                        await msg.delete()
                        break
                check_count = func.update_check_count(payload)
                if check_count == -1:
                    async for msg in dm_channel.history(limit=10):
                        if msg.author != bot.user:
                            continue
                        if msg.content.startswith("以下のユーザーに投票します"):
                            await msg.delete()
                else:
                    target_id = func.get_id_by_name(target_name)
                    func.update_vote_list(target_id, payload.user_id)
                    alives_count = func.count_alives()
                    channel = await bot.fetch_channel(TXT_CH_ID)
                    target_message = await channel.fetch_message(main_emb_message_id)
                    target_embed = target_message.embeds[0]
                    if target_embed:
                        row_count = func.get_row_count('vote.csv')
                        if row_count != alives_count:
                            vote_count = alives_count - row_count
                        else:
                            vote_count = alives_count
                        new_embed = target_embed.copy()
                        if check_count == vote_count:
                            new_embed.title = "投票が完了しました"
                            new_embed.description = "**LOADING** "+"■"*check_count
                            new_embed.set_footer(text="✅を押して進行してください")
                            await target_message.edit(embed=new_embed)
                            await target_message.add_reaction('✅')
                        else:
                            new_embed.description = "**LOADING** "+"■"*check_count + "□"*(vote_count - check_count)
                            await target_message.edit(embed=new_embed)
            elif payload.emoji.name == '❌':
                await message.delete()
        elif message.content.startswith("以下のユーザーを襲撃します"):
            if payload.emoji.name == '⭕':
                target_name = message.content.split('\n')[1]
                await message.delete()
                dm_channel = await bot.fetch_channel(payload.channel_id)
                async for msg in dm_channel.history(limit=10):
                    if msg.author != bot.user:
                        continue
                    if msg.content.startswith("襲撃する対象を選んでください"):
                        await msg.delete()
                        break
                kil_check = func.check_status(1)
                if kil_check == 1:
                    async for msg in dm_channel.history(limit=10):
                        if msg.author != bot.user:
                            continue
                        if msg.content.startswith("以下のユーザーを襲撃します"):
                            await msg.delete()
                else:
                    target_id = func.get_id_by_name(target_name)
                    await dm_channel.send(f"「{target_name}」を襲撃しました")
                    func.update_status(target_id, 1)
                    alives_count = func.count_alives()
                    channel = await bot.fetch_channel(TXT_CH_ID)
                    target_message = await channel.fetch_message(main_emb_message_id)
                    target_embed = target_message.embeds[0]
                    if target_embed:
                        check_count = func.update_check_count_wolf()
                        if check_count == alives_count:
                            new_embed = target_embed.copy()
                            new_embed.set_footer(text="✅を押して進行してください")
                            await target_message.edit(embed=new_embed)
                            await target_message.add_reaction('✅')
            elif payload.emoji.name == '❌':
                await message.delete()
        elif message.content.startswith("以下のユーザーを占います"):
            if payload.emoji.name == '⭕':
                target_name = message.content.split('\n')[1]
                await message.delete()
                dm_channel = await bot.fetch_channel(payload.channel_id)
                async for msg in dm_channel.history(limit=10):
                    if msg.author != bot.user:
                        continue
                    if  msg.content.startswith("占う対象を選んでください"):
                        await msg.delete()
                        break
                ftn_check = func.check_status(2)
                if ftn_check == 1:
                    async for msg in dm_channel.history(limit=10):
                        if msg.author != bot.user:
                            continue
                        if  msg.content.startswith("以下のユーザーを占います"):
                            await msg.delete()
                else:
                    target_id = func.get_id_by_name(target_name)
                    func.update_status(target_id, 2)
                    await send_fortune_result(target_id, payload.user_id)
                    alives_count = func.count_alives()
                    channel = await bot.fetch_channel(TXT_CH_ID)
                    target_message = await channel.fetch_message(main_emb_message_id)
                    target_embed = target_message.embeds[0]
                    if target_embed:
                        check_count = func.update_check_count(payload)
                        if check_count == alives_count:
                            new_embed = target_embed.copy()
                            new_embed.set_footer(text="✅を押して進行してください")
                            await target_message.edit(embed=new_embed)
                            await target_message.add_reaction('✅')
            elif payload.emoji.name == '❌':
                await message.delete()
        elif message.content.startswith("以下のユーザーを守ります"):
            if payload.emoji.name == '⭕':
                target_name = message.content.split('\n')[1]
                await message.delete()
                dm_channel = await bot.fetch_channel(payload.channel_id)
                async for msg in dm_channel.history(limit=20):
                    if msg.author != bot.user:
                        continue
                    if msg.content.startswith("保護する対象を選んでください"):
                        await msg.delete()
                        break
                grd_check = func.check_status(3)
                if grd_check == 1:
                    async for msg in dm_channel.history(limit=10):
                        if msg.author != bot.user:
                            continue
                        if  msg.content.startswith("以下のユーザーを守ります"):
                            await msg.delete()
                else:
                    if GRD_FLG == 1:
                        func.reset_grd_flg()
                    target_id = func.get_id_by_name(target_name)
                    func.update_status(target_id, 3+GRD_FLG)
                    alives_count = func.count_alives()
                    channel = await bot.fetch_channel(TXT_CH_ID)
                    target_message = await channel.fetch_message(main_emb_message_id)
                    target_embed = target_message.embeds[0]
                    if target_embed:
                        check_count = func.update_check_count(payload)
                        if check_count == alives_count:
                            new_embed = target_embed.copy()
                            new_embed.set_footer(text="✅を押して進行してください")
                            await target_message.edit(embed=new_embed)
                            await target_message.add_reaction('✅')
            elif payload.emoji.name == '❌':
                await message.delete()
        elif message.content.startswith("以下のユーザーに質問します"):
            if payload.emoji.name == '⭕':
                target_name = message.content.split('\n')[1]
                await message.delete()
                dm_channel = await bot.fetch_channel(payload.channel_id)
                async for msg in dm_channel.history(limit=20):
                    if msg.author != bot.user:
                        continue
                    if msg.content.startswith("質問する相手を選んでください"):
                        await msg.delete()
                        break
                target_id = func.get_id_by_name(target_name)
                func.update_interview(str(payload.user_id) , target_id)
            elif payload.emoji.name == '❌':
                await message.delete()

#### !CMMAND ####
@bot.command(name='jinro')
async def create_embed_with_reaction(ctx: commands.Context):
    await ctx.message.delete()
    embed = discord.Embed(title='人狼メンバー設定', color=0x660000, description='-'*23+'\n'+'-'*23)
    embed.set_footer(text="メンバーを設定して✅を押してください")
    message = await ctx.send(embed=embed)
    await message.add_reaction('✋')
    await message.add_reaction('🗣️')
    await message.add_reaction('✅')
    global main_emb_message_id
    main_emb_message_id = message.id

@bot.command(name='adj')
async def ad_username(ctx: commands.Context, *names):
    await ctx.message.delete()
    global main_emb_message_id
    if main_emb_message_id:
        channel = await bot.fetch_channel(TXT_CH_ID)
        message = await channel.fetch_message(main_emb_message_id)
        embed = message.embeds[0]
        if embed:
            new_embed = embed.copy()
            dsc_lines = new_embed.description.rstlip("\n", 1)
            names_text = "\n".join(names)
            new_embed.description = f'{dsc_lines[0]}\n{names_text}\n{dsc_lines[1]}'
            await message.edit(embed=new_embed)

@bot.command(name='rmj')
async def rm_username(ctx: commands.Context, usermention: str):
    await ctx.message.delete()
    global main_emb_message_id
    if main_emb_message_id:
        channel = await bot.fetch_channel(TXT_CH_ID)
        message = await channel.fetch_message(main_emb_message_id)
        embed = message.embeds[0]
        if embed:
            new_embed = embed.copy()
            description_lines = new_embed.description.split('\n')
            updated_description = ''
            deleted = False
            for line in description_lines:
                if line.strip() != usermention:
                    updated_description += line + '\n'
                elif not deleted:
                    deleted = True
                else:
                    updated_description += line + '\n'
            new_embed.description = updated_description.rstrip('\n')
            await message.edit(embed=new_embed)

@bot.command(name='reset_aj')
async def reset_username(ctx: commands.Context):
    await ctx.message.delete()
    global main_emb_message_id
    if main_emb_message_id:
        channel = await bot.fetch_channel(TXT_CH_ID)
        message = await channel.fetch_message(main_emb_message_id)
        embed = message.embeds[0]
        if embed:
            new_embed = embed.copy()
            new_embed.description = '-'*23+'\n'+'-'*23
            await message.edit(embed=new_embed)

@bot.command(name='delete_j')
async def delete_embed(ctx: commands.Context):
    await ctx.message.delete()
    async for message in ctx.channel.history(limit=30):
        if message.author != bot.user:
            continue
        if message.embeds:
            for embedded in message.embeds:
                if embedded.type == 'rich':
                    await message.delete()
                return

@bot.command(name='prest')
async def create_embed_prestart(ctx: commands.Context):
    await ctx.message.delete()
    embed = discord.Embed(title='ゲームを開始します', color=0x660000)
    embed.set_footer(text='VCにメンバーが集まったら🆗を押してください')
    message = await ctx.send(embed=embed)
    await message.add_reaction('🆗')
    global main_emb_message_id
    main_emb_message_id = message.id

@bot.command(name='premo')
async def create_embed_premorning(ctx: commands.Context):
    await ctx.message.delete()
    embed = discord.Embed(title='おそろしい夜がやってきました', color=0xFF0000)
    embed.description = "朝の会議から始まります"
    embed.set_footer(text="✅を押して進行してください")
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')
    global main_emb_message_id
    main_emb_message_id = message.id

@bot.command(name='prein')
async def create_embed_preinterview(ctx: commands.Context):
    await ctx.message.delete()
    embed = discord.Embed(title='会議の時間です', color=0x8B4513)
    embed.description = "質疑応答から始まります"
    embed.set_footer(text="✅を押して進行してください")
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')
    global main_emb_message_id
    main_emb_message_id = message.id

@bot.command(name='prexe')
async def create_embed_preexecution(ctx: commands.Context):
    await ctx.message.delete()
    embed = discord.Embed(title='質疑応答が終了しました', color=0x8B4513)
    embed.description = "処刑から始まります"
    embed.set_footer(text="✅を押して進行してください")
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')
    global main_emb_message_id
    main_emb_message_id = message.id

@bot.command(name='preni')
async def create_embed_prenight(ctx: commands.Context, flg: int = 0):
    await ctx.message.delete()
    if flg == 1:
        func.reset_fortune()
    embed = discord.Embed(title='処刑が執行されました', color=0x8B4513)
    embed.description = "夜時間から始まります"
    embed.set_footer(text="✅を押して進行してください")
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')
    global main_emb_message_id
    main_emb_message_id = message.id

@bot.command(name='skip')
async def skip_to_next(ctx: commands.Context):
    await ctx.message.delete()
    await task_kill()
    global main_emb_message_id
    if main_emb_message_id:
        channel = await bot.fetch_channel(TXT_CH_ID)
        message = await channel.fetch_message(main_emb_message_id)
        embed = message.embeds[0]
        if embed.title.startswith("会議の時間です"):
            global m_exit_flg
            m_exit_flg = True
            embed.title = "朝の会議をスキップしました"
            embed.description = ""
            embed.set_footer(text="✅を押して進行してください")
            await message.edit(embed=embed)
            await mute_alives()
            await message.add_reaction('✅')
        elif embed.title.startswith("質疑応答の時間です"):          
            if "人目の質問者は" in embed.description:
                user_name = embed.description.split("人目の質問者は「")[-1].rstrip("」です")
                user_id = func.get_id_by_name(user_name)
                if user_id:
                    await clean_select_to_dm(user_id)
                    await clean_skip_inter_dm(user_id)
                    await clean_rand_to_dm(user_id)
            elif "に質問です" in embed.description:
                user_name = embed.description.split("」から「")[0].lstrip("「")
                user_id = func.get_id_by_name(user_name)
                if user_id:
                    await clean_select_to_dm(user_id)
                    await clean_skip_inter_dm(user_id)
                    await clean_rand_to_dm(user_id)
                to_name = embed.description.split("」から「")[-1].rstrip("」に質問です")
                to_id = func.get_id_by_name(to_name)
                if to_id:
                    await clean_select_to_dm(to_id)
            embed.title = "質疑応答をスキップしました"
            embed.description = ""
            embed.set_footer(text="✅を押して進行してください")
            await message.edit(embed=embed)
            await mute_alives()
            await message.add_reaction('✅')
        elif embed.title.startswith("遺言の時間"):
            await message.clear_reactions()
            executed_name = embed.description.split("が処刑される")[0].split("\n")[-1]
            executed_id = func.get_id_by_name(executed_name)
            user = await bot.fetch_user(executed_id)
            await clean_will_dm(executed_id)
            await user.send("あなたは処刑されました")
            await add_death_prefix(executed_id)
            await add_rip_role(executed_id)
            await send_log(id=executed_id, flg=1)
            embed.title = "遺言がスキップされ処刑が執行されました"
            embed.color = 0x8B4513
            embed.description = ""
            embed.set_footer(text="✅を押して進行してください")
            await message.edit(embed=embed)
            await mute_select(executed_id)
            await message.add_reaction('✅')
        elif embed.title.startswith("弁明の時間です"):
            await message.clear_reactions()
            prexer_ids = func.get_vote_max_ids()
            func.set_vote_data(2)
            func.reset_check_column()
            for perexer_id in prexer_ids:
                await mute_select(perexer_id)
            await clean_persuasion_dm(prexer_ids)
            row_count = func.get_row_count('vote.csv')
            alives_count = func.count_alives()
            vote_count = alives_count - row_count
            embed.title = "弁明の時間がスキップされました"
            embed.description = "**LOADING** " + "□"*vote_count
            embed.set_footer(text="決選投票を始めます\nしばらくお待ちください")
            await message.edit(embed=embed)
            await fin_vote_operates()
        else:
            embed.set_footer(text="現在スキップ不可能です")
            await message.edit(embed=embed)

@bot.command(name='dbmj')
async def delete_bot_messages(ctx: commands.Context, num: int = 1):
    channel = ctx.channel
    if isinstance(channel, discord.TextChannel):
        await ctx.message.delete()
    bot_messages = []
    async for message in channel.history(limit=50):
        if message.author.bot:
            bot_messages.append(message)
    num = min(num, len(bot_messages))
    for message in bot_messages[:num]:
        await message.delete()
        await asyncio.sleep(0.5)

@bot.command(name='act')
async def activate_emb(ctx: commands.Context):
    await ctx.message.delete()
    async for message in ctx.channel.history(limit=30):
        if message.embeds:
            for embedded in message.embeds:
                if embedded.type == 'rich':
                    target_embed = embedded
                    break
                if target_embed:
                    break
    if target_embed:
        global main_emb_message_id
        main_emb_message_id = message.id
        target_embed.set_footer(text="ACTIVATEに成功しました")
        await message.edit(embed=target_embed)

@bot.command(name='rip')
async def ad_rip_role_send_ch(ctx: commands.Context, usermention: str):
    await ctx.message.delete()
    user_id = usermention.lstrip('<@').rstrip('>')
    if user_id.isdigit():
        await add_death_prefix(user_id)
        await add_rip_role(user_id)

@bot.command(name='rmrip')
async def rm_rip_role(ctx: commands.Context, usermention=None):
    await ctx.message.delete()
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(RIP_RL_ID)
    if role:
        if usermention:
            user_id = usermention.lstrip('<@').rstrip('>')
            if user_id.isdigit():
                await remove_death_prefix(user_id)
                member = guild.get_member(int(user_id))
                if member:
                    await member.remove_roles(role)
        else:
            members_with_role = [m for m in guild.members if role in m.roles]
            await remove_death_prefix()
            for member in members_with_role:
                await member.remove_roles(role)

async def on_ready():
    print('Bot is ready.')

bot.run(TOKEN)
