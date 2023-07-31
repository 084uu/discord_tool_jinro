import discord
from discord.ext import commands
import re
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
RC_FLG = int(os.getenv("RECHECK_FLG"))
VOTE_RANDOM = int(os.getenv("VOTE_RANDOM_SELECT"))
MAX_VOTE_REPEAT = int(os.getenv("MAX_VOTE"))
GRD_FLG = int(os.getenv("CONSECUTIVE_GRD_FLG"))
QA_FLG = int(os.getenv("QA_SESSION_FLG"))
NIGHT_AUTO_FLG = int(os.getenv("NIGHT_AUTO_CHECK_FLG"))

###########################################################################################

#### OTHER VALUE ####
REACTION_EMOJIS_A = ('1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟','⏺️','🔼','⏹️','0️⃣')
REACTION_EMOJIS_B = ('⭕', '❌')

#### GLOBAL VARIABLES ####
GLOBAL_TASK = None
EXIT_FLG = False
M_EXIT_FLG = False
USER_EXIT_FLG = False
VOTE_REPEAT = MAX_VOTE_REPEAT
DAY = 0

SERVER = None
MAIN_CH =None
MAIN_EMB_ID = None

#### SYSTEM0 ####
async def get_payload_member(payload):
    flg = func.check(payload.user_id)
    if flg:
        member = func.get_member(payload.user_id)
    else:
        member = await SERVER.fetch_member(payload.user_id)
    return member

#### VOICE CONTROL ####
async def mute_alives(user_ids=[]):
    async def mute(member):
        await member.edit(mute=True)
        await asyncio.sleep(0.3)
    if user_ids:
        members = func.get_members(user_ids)
        tasks = [mute(member) for member in members]
        await asyncio.gather(*tasks)
    else:
        members = func.get_alive_members()
        tasks = [mute(member) for member in members]
        await asyncio.gather(*tasks)

async def unmute_alives(user_ids=[]):
    async def unmute(member):
        await member.edit(mute=False)
        await asyncio.sleep(0.3)
    if user_ids:
        members = func.get_members(user_ids)
        tasks = [unmute(member) for member in members]
        await asyncio.gather(*tasks)
    else:
        members = func.get_alive_members()
        tasks = [unmute(member) for member in members]
        await asyncio.gather(*tasks)

async def unmute_all():
    voice_ch = SERVER.get_channel(VOICE_CH_ID)
    async def unmute(member):
        await member.edit(mute=False)
        await asyncio.sleep(0.3)
    tasks = [unmute(member) for member in voice_ch.members]
    await asyncio.gather(*tasks)

#### SKIPABLE TASKS ####
async def discussion_ops(message):
    global M_EXIT_FLG
    M_EXIT_FLG = False
    embed = message.embeds[0]
    await message.add_reaction('⏭️')
    await unmute_alives()
    await asyncio.sleep(2)
    if M_EXIT_FLG: return
    embed.set_footer(text="◇"*5 +"\n残り時間は5分です")
    await message.edit(embed=embed)
    await asyncio.sleep(30)
    if M_EXIT_FLG: return
    await asyncio.sleep(30)
    if M_EXIT_FLG: return
    embed.set_footer(text="◆" +"◇"*4 +"\n残り時間は4分です")
    await message.edit(embed=embed)
    await asyncio.sleep(30)
    if M_EXIT_FLG: return
    await asyncio.sleep(30)
    if M_EXIT_FLG: return
    embed.set_footer(text="◆"*2 +"◇"*3 +"\n残り時間は3分です")
    await message.edit(embed=embed)
    await asyncio.sleep(30)
    if M_EXIT_FLG: return
    await asyncio.sleep(30)
    if M_EXIT_FLG: return
    embed.set_footer(text="◆"*3 +"◇"*2 +"\n残り時間は2分です")
    await message.edit(embed=embed)
    await asyncio.sleep(30)
    if M_EXIT_FLG: return
    await asyncio.sleep(30)
    if M_EXIT_FLG: return
    embed.set_footer(text="◆"*4 +"◇"*1 +"\n残り時間は60秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if M_EXIT_FLG: return
    embed.set_footer(text="■" +"□"*5 +"\n残り時間は50秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if M_EXIT_FLG: return
    embed.set_footer(text="■"*2 +"□"*4 +"\n残り時間は40秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if M_EXIT_FLG: return
    embed.set_footer(text="■"*3 +"□"*3 +"\n残り時間は30秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if M_EXIT_FLG: return
    embed.set_footer(text="■"*4 +"□"*2 +"\n残り時間は20秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if M_EXIT_FLG: return
    embed.set_footer(text="■"*5 +"□" +"\n残り時間は10秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if M_EXIT_FLG: return
    embed.set_footer(text="■"*6 +"\n残り時間は0秒です")
    await message.edit(embed=embed)
    await mute_alives()
    await message.clear_reactions()
    embed.description = ""
    embed.set_footer(text="会議時間は終了しました")
    await message.edit(embed=embed)
    await asyncio.sleep(2)
    embed.set_footer(text="会議時間は終了しました\n✅を押して進行してください")
    await message.edit(embed=embed)
    await message.add_reaction('✅')

async def discussion_tasks(message):
    global GLOBAL_TASK
    GLOBAL_TASK = asyncio.create_task(discussion_ops(message))
    await GLOBAL_TASK

async def qa_ops(message):
    global EXIT_FLG
    EXIT_FLG = False
    global USER_EXIT_FLG
    class A_error(Exception):
        pass
    embed = message.embeds[0]
    embed.title = "質疑応答の時間です"
    embed.color = 0x8B4513
    embed.set_footer(text="しばらくお待ちください")
    await message.edit(embed=embed)
    func.reset_qa()
    await asyncio.sleep(3)
    if EXIT_FLG: return
    alive_ids = func.get_alives()
    for index, user_id in enumerate(alive_ids):
        if USER_EXIT_FLG:
            USER_EXIT_FLG = False
        func.update_qa(DAY, user_id)
        user_name = func.get_name_by_id(user_id)
        embed.description = f"{index+1}人目の質問者は「{user_name}」です"
        embed.set_footer(text=f"{user_name}の応答を待機しています")
        await message.edit(embed=embed)
        if index == 0:
            await message.add_reaction('⏭️')
        if EXIT_FLG: return
        if USER_EXIT_FLG:
            USER_EXIT_FLG = False
            await asyncio.sleep(3)
            continue
        user = func.get_member(user_id)
        smsg = await user.send("質問をスキップする場合は⏭️を押してください")
        await smsg.add_reaction('⏭️')
        await func.send_select_to(user_id)
        def check(payload):
            return payload.user_id == user_id
        try:
            if EXIT_FLG: return
            if USER_EXIT_FLG:
                USER_EXIT_FLG = False
                await asyncio.sleep(3)
                raise A_error()
            while True:
                if EXIT_FLG: return
                if USER_EXIT_FLG:
                    USER_EXIT_FLG = False
                    await asyncio.sleep(3)
                    raise A_error()
                payload = await bot.wait_for("raw_reaction_add", check=check, timeout=30)
                dm_channel = await bot.fetch_channel(payload.channel_id)
                dm_message = await dm_channel.fetch_message(payload.message_id)
                if (payload.emoji.name == "⭕" and dm_message.content.startswith("以下のユーザーに質問します")) or (RC_FLG == 0 and message.content.startswith("質問する相手を")):
                    await asyncio.sleep(5)
                    if EXIT_FLG: return
                    if USER_EXIT_FLG:
                        USER_EXIT_FLG = False
                        await asyncio.sleep(3)
                        raise A_error()
                    to_id = func.get_qa_to_id(DAY, payload.user_id)
                    if to_id:
                        to_name = func.get_name_by_id(to_id)
                        to_user = func.get_member(to_id)
                        embed.description = f"「{user_name}」から「{to_name}」に質問です"
                        embed.set_footer(text= "質問時間は1分です\nまもなく始まります")
                        await message.edit(embed=embed)
                        fmsg = await user.send(f"まもなく「{to_name}」への質問が開始されます\n※まもなくミュートが外れます")
                        tmsg = await to_user.send(f"まもなく「{user_name}」からの質問が開始されます\n※まもなくミュートが外れます")
                        await asyncio.sleep(3)
                        if EXIT_FLG: return
                        if USER_EXIT_FLG:
                            USER_EXIT_FLG = False
                            await asyncio.sleep(3)
                            raise A_error()
                        await unmute_alives([user_id, to_id])
                        embed.set_footer(text="□"*6 +"\n残り時間は60秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        if EXIT_FLG: return
                        if USER_EXIT_FLG:
                            USER_EXIT_FLG = False
                            await asyncio.sleep(3)
                            raise A_error()
                        embed.set_footer(text="■" +"□"*5 +"\n残り時間は50秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        if EXIT_FLG: return
                        if USER_EXIT_FLG:
                            USER_EXIT_FLG = False
                            await asyncio.sleep(3)
                            raise A_error()
                        embed.set_footer(text="■"*2 +"□"*4 +"\n残り時間は40秒です")
                        await message.edit(embed=embed)
                        await fmsg.delete()
                        await tmsg.delete()
                        await asyncio.sleep(10)
                        if EXIT_FLG: return
                        if USER_EXIT_FLG:
                            USER_EXIT_FLG = False
                            await asyncio.sleep(3)
                            raise A_error()
                        embed.set_footer(text="■"*3 +"□"*3 +"\n残り時間は30秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        if EXIT_FLG: return
                        if USER_EXIT_FLG:
                            USER_EXIT_FLG = False
                            await asyncio.sleep(3)
                            raise A_error()
                        embed.set_footer(text="■"*4 +"□"*2 +"\n残り時間は20秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        if EXIT_FLG: return
                        if USER_EXIT_FLG:
                            USER_EXIT_FLG = False
                            await asyncio.sleep(3)
                            raise A_error()
                        embed.set_footer(text="■"*5 +"□"*1 +"\n残り時間は10秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        await smsg.delete()
                        if EXIT_FLG: return
                        if USER_EXIT_FLG:
                            USER_EXIT_FLG = False
                            await asyncio.sleep(3)
                            raise A_error()
                        embed.set_footer(text="■"*6 +"\n残り時間は0秒です")
                        await message.edit(embed=embed)
                        await mute_alives([user_id, to_id])
                        embed.description = f"「{user_name}」から「{to_name}」への質問が終わりました"
                        embed.set_footer(text="次の質問者へ移ります")
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        raise A_error()
                elif payload.emoji.name == "⏭️" and dm_message.content.startswith("質問をスキップする場合は"):
                    await asyncio.sleep(3)
                    USER_EXIT_FLG = False
                    break
            if EXIT_FLG: return
            if USER_EXIT_FLG:
                USER_EXIT_FLG = False
                await asyncio.sleep(3)
                raise A_error()
        except A_error:
            pass
        except asyncio.TimeoutError:
            if EXIT_FLG: return
            if USER_EXIT_FLG:
                USER_EXIT_FLG = False
                await asyncio.sleep(3)
                continue
            await func.clean_select_to_dm(user_id)
            await func.send_rand_to(user_id)
            to_id, to_name, to_user = func.random_select_to(DAY, user_id)
            fmsg = await user.send(f"まもなく「{to_name}」への質問が開始されます\n※まもなくミュートが外れます")
            tmsg = await to_user.send(f"まもなく「{user_name}」からの質問が開始されます\n※まもなくミュートが外れます")
            embed.description = f"「{user_name}」から「{to_name}」に質問です"
            embed.set_footer(text="■"*3 +"□"*3 +"\n質問時間は30秒です")
            await message.edit(embed=embed)
            if EXIT_FLG: return
            if USER_EXIT_FLG:
                USER_EXIT_FLG = False
                await asyncio.sleep(3)
                continue
            await asyncio.sleep(3)
            await unmute_alives([user_id, to_id])
            await asyncio.sleep(10)
            if EXIT_FLG: return
            if USER_EXIT_FLG:
                USER_EXIT_FLG = False
                await asyncio.sleep(3)
                continue            
            embed.set_footer(text="■"*4 +"□"*2 +"\n残り時間は20秒です")
            await message.edit(embed=embed)
            await asyncio.sleep(10)
            await fmsg.delete()
            await tmsg.delete()
            if EXIT_FLG: return
            if USER_EXIT_FLG:
                USER_EXIT_FLG = False
                await asyncio.sleep(3)
                continue
            await func.clean_rand_to_dm(user_id)
            embed.set_footer(text="■"*5 +"□"*1 +"\n残り時間は10秒です")
            await message.edit(embed=embed)
            await asyncio.sleep(10)
            await smsg.delete()
            if EXIT_FLG: return
            if USER_EXIT_FLG:
                USER_EXIT_FLG = False
                await asyncio.sleep(3)
                continue
            embed.set_footer(text="■"*6 +"\n残り時間は0秒です")
            await message.edit(embed=embed)
            await mute_alives([user_id, to_id])
            embed.description = f"「{user_name}」から「{to_name}」への質問が終わりました"
            embed.set_footer(text="次の質問者へ移ります")
            await message.edit(embed=embed)
            await asyncio.sleep(3)
            if EXIT_FLG: return
    await message.clear_reactions()
    embed.title = "質疑応答が終了しました"
    embed.color = 0x8B4513
    embed.description = ""
    embed.set_footer(text="✅を押して進行してください")
    await message.edit(embed=embed)
    await message.add_reaction('✅')

async def qa_tasks(message):
    global GLOBAL_TASK
    GLOBAL_TASK = asyncio.create_task(qa_ops(message))
    await GLOBAL_TASK

async def will_ops(message):
    global EXIT_FLG
    EXIT_FLG = False
    embed = message.embeds[0]
    exed_id = func.get_executed()
    user = func.get_member(exed_id)
    embed.title = "遺言の時間です"
    embed.color = 0x8B4513
    embed.set_footer(text="□"*6+"\n遺言時間は1分です\nまもなく始まります")
    await message.edit(embed=embed)
    if EXIT_FLG: return
    emsg = await user.send("※まもなくミュートが外れます")
    smsg = await user.send("遺言をスキップする場合は⏭️を押してください")
    await smsg.add_reaction('⏭️')
    await asyncio.sleep(1)
    await unmute_alives([exed_id])
    if EXIT_FLG: return
    embed.set_footer(text="□"*6 +"\n残り時間は60秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if EXIT_FLG: return
    embed.set_footer(text="■"+"□"*5 +"\n残り時間は50秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if EXIT_FLG: return
    embed.set_footer(text="■"*2 +"□"*4 +"\n残り時間は40秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if EXIT_FLG: return
    await emsg.delete()
    embed.set_footer(text="■"*3 +"□"*3 +"\n残り時間は30秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if EXIT_FLG: return
    embed.set_footer(text="■"*4 +"□"*2 +"\n残り時間は20秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if EXIT_FLG: return
    embed.set_footer(text="■"*5 +"□"*1 +"\n残り時間は10秒です")
    await message.edit(embed=embed)
    await asyncio.sleep(10)
    if EXIT_FLG: return
    embed.set_footer(text="■"*6 +"\n残り時間は0秒です")
    await message.edit(embed=embed)
    await mute_alives([exed_id])
    await smsg.delete()
    await func.clean_will_dm(exed_id)
    await asyncio.sleep(3)
    if EXIT_FLG: return
    embed.title = "処刑が執行されました"
    embed.color = 0x8B4513
    embed.description = ""
    embed.set_footer(text="✅を押して進行してください")
    await message.edit(embed=embed)
    await user.send("あなたは処刑されました")
    await add_rip_role_and_prefix(exed_id)
    await send_log(id=exed_id, flg=1)
    await message.add_reaction('✅')

async def will_tasks(message):
    global GLOBAL_TASK
    GLOBAL_TASK = asyncio.create_task(will_ops(message))
    await GLOBAL_TASK

async def persuasion_ops(message):
    global EXIT_FLG
    EXIT_FLG = False
    global USER_EXIT_FLG
    embed = message.embeds[0]
    embed.title = "弁明の時間です"
    embed.description = ""
    embed.set_footer(text="しばらくお待ちください")
    await message.edit(embed=embed)
    prexed_ids = func.get_prexe()
    for prexed_id in prexed_ids:
        USER_EXIT_FLG = False
        prexer = func.get_member(prexed_id)
        prexer_name = func.get_name_by_id(prexed_id)
        msg = await prexer.send("あなたの弁明の時間が始まります\n※まもなくミュートが外れます")
        await asyncio.sleep(1)
        smsg = await prexer.send("弁明をスキップする場合は⏭️を押してください")
        await smsg.add_reaction('⏭️')
        await asyncio.sleep(1)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message, msg)
            await asyncio.sleep(3)
            continue
        await unmute_alives([prexed_id])
        embed.description = f"「{prexer_name}」による弁明です"
        embed.set_footer(text= "□"*6+"残り時間は1分です")
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message, msg)
            await asyncio.sleep(3)
            continue
        await asyncio.sleep(5)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message, msg)
            await asyncio.sleep(3)
            continue
        embed.set_footer(text= "■"+"□"*5+"残り時間は50秒です")
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message, msg)
            await asyncio.sleep(3)
            continue
        await asyncio.sleep(5)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message, msg)
            await asyncio.sleep(3)
            continue
        embed.set_footer(text= "■"*2+"□"*4+"残り時間は40秒です")
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message, msg)
            await asyncio.sleep(3)
            continue
        await asyncio.sleep(5)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message, msg)
            await asyncio.sleep(3)
            continue
        await msg.delete()
        embed.set_footer(text= "■"*3+"□"*3+"残り時間は30秒です")
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message)
            await asyncio.sleep(3)
            continue
        await asyncio.sleep(5)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message)
            await asyncio.sleep(3)
            continue
        embed.set_footer(text= "■"*4+"□"*2+"残り時間は20秒です")
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message)
            await asyncio.sleep(3)
            continue
        await asyncio.sleep(5)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message)
            await asyncio.sleep(3)
            continue
        embed.set_footer(text= "■"*5+"□"*1+"残り時間は10秒です")
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message)
            await asyncio.sleep(3)
            continue
        await asyncio.sleep(5)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message)
            await asyncio.sleep(3)
            continue
        embed.set_footer(text= "■"*6+"残り時間は0秒です")
        await message.edit(embed=embed)
        await smsg.delete()
        await mute_alives([prexed_id])
        embed.description = f"「{prexer_name}」による弁明が終わりました"
        embed.set_footer(text= "次に移行します\nしばらくお待ちください")
        await message.edit(embed=embed)
    embed.description = "全ての弁明が終わりました"
    embed.set_footer(text= "決選投票を始めます\n✅を押して進行してください")
    await message.edit(embed=embed)
    await message.add_reaction('✅')
    await func.clean_persuasion_dm(prexed_ids)

async def persuasion_tasks(message):
    global GLOBAL_TASK
    GLOBAL_TASK = asyncio.create_task(persuasion_ops(message))
    await GLOBAL_TASK

async def persuasion_skip(persuader_name, message, msg = None):
    if msg:
        try:
            await msg.delete()
        except:
            pass
    if message.embeds:
        embed = message.embeds[0]
        embed.description = f"「{persuader_name}」による弁明がスキップされました"
        embed.set_footer(text= "次に移行します\nしばらくお待ちください")
        await message.edit(embed=embed)

#### SYSTEM1 ####
async def add_wolf_room():
    wolf_ids = func.get_alive_wolfs()
    if len(wolf_ids) >= 2:
        channel = SERVER.get_channel(WLF_CH_ID)
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages=True
        overwrite.send_messages=True
        overwrite.add_reactions=True
        for wlf_id in wolf_ids:
            member = func.get_member(wlf_id)
            if not member.guild_permissions.administrator:
                try:
                    await channel.set_permissions(member, overwrite=overwrite)
                except:
                    pass

async def remove_all_werewolf_room():
    channel = SERVER.get_channel(WLF_CH_ID)
    overwrite = discord.PermissionOverwrite()
    overwrite.read_messages=False
    overwrite.send_messages=False
    overwrite.add_reactions=False
    for member in channel.members:
        if not member.guild_permissions.administrator:
            try:
                await channel.set_permissions(member, overwrite=overwrite)
            except:
                pass

async def send_log(id=None, name=None, vtx=None, flg=0):
    global DAY
    channel = SERVER.get_channel(LOG_CH_ID)
    if vtx:
        log = f"□ 投票結果\n{vtx}"
        await channel.send(log)
    elif flg == 0:
        if DAY == 0:
            log = "## === ゲーム開始 ===\n>>> "
            names_txt = func.get_names_txt()
            log += names_txt
            await channel.send(log)
            DAY += 1
        else:
            await channel.send(f"## {DAY}日目")
            DAY += 1
    elif flg == 1:
        if id:
            name = func.get_name_by_id(id)
            await channel.send(f"■ 処刑\n`「{name}」を処刑した`")
        else:
            await channel.send("...処刑できなかった")
    elif flg == 2:
        if name:
            await channel.send(f"■ 犠牲\n`「{name}」が殺された`")
        else:
            await channel.send("...昨夜は誰も殺されなかった")
        if DAY > 2:
            alives_txt = func.get_alives_txt()
            await channel.send(f"□ 生存者\n>>> {alives_txt}")
    elif flg == 3:
        await channel.send(f"...人狼はいなくなった\n## === ゲーム終了 ===")
        result = func.get_result()
        await channel.send(f"```{result}```")
    elif flg == 4:
        await channel.send(f"...全員人狼に食べられた\n## === ゲーム終了 ===")
        result = func.get_result()
        await channel.send(f"```{result}```")

async def vote_ops(user_id, target_name):
    target_id = func.get_id_by_name(target_name)
    func.update_vote(target_id, user_id)
    message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
    embed = message.embeds[0]
    if embed:
        alives_count = func.get_count_alives()
        vote_count = func.get_vote_count()
        left_count = alives_count - vote_count
        if not left_count:
            new_embed = embed.copy()
            new_embed.title = "投票が完了しました"
            new_embed.description = "**LOADING** "+"■"*vote_count
            new_embed.set_footer(text="✅を押して進行してください")
            await message.edit(embed=new_embed)
            await message.add_reaction('✅')
        else:
            new_embed = embed.copy()
            new_embed.description = "**LOADING** "+"■"*vote_count + "□"*left_count
            await message.edit(embed=new_embed)

async def night_ops(user_id):
    message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
    embed = message.embeds[0]
    if embed:
        alives_count = func.get_count_alives()
        check_count = func.update_check_count(user_id)
        if check_count == alives_count:
            new_embed = embed.copy()
            new_embed.set_footer(text="✅を押して進行してください")
            await message.edit(embed=new_embed)
            await message.add_reaction('✅')

#### DM ####
async def send_werewolf_ops():
    wolf_ids = func.get_alive_wolfs()
    if len(wolf_ids) == 1:
        user_id = wolf_ids.pop()
        await send_werewolf_bite(user_id)
    elif len(wolf_ids) >= 2:
        await add_wolf_room()
        await send_werewolf_bite()

async def send_werewolf_bite(user_id=None): # 襲撃する対象を選んでください
    names = func.get_alive_vil_names()
    list_message = "襲撃する対象を選んでください\n"
    for index, item in enumerate(names):
        list_message += f"{REACTION_EMOJIS_A[index]}: {item}\n"
    list_message += "リアクションで選択してください"
    if user_id:
        user = func.get_member(user_id)
        sent_message = await user.send(list_message)
    else:
        channel = SERVER.get_channel(WLF_CH_ID)
        sent_message = await channel.send(list_message)
    for index in range(len(names)):
        await sent_message.add_reaction(REACTION_EMOJIS_A[index])

async def send_werewolf_messages():
    wolf_ids = func.get_alive_wolfs()
    wlfs_text = None
    if len(wolf_ids) >= 2:
        await add_wolf_room()
        channel = SERVER.get_channel(WLF_CH_ID)
        await channel.send(">>> 人狼部屋にようこそ\n人狼が複数いる夜はこの部屋が開放され、\nこちらに襲撃先の案内が送られます\n"
                            +"襲撃先は人狼全員で選択してください\nここから下が今回の人狼チャットです")
        wlf_names = func.get_names_by_ids(wolf_ids)
        wlfs_text = ", ".join(x for x in wlf_names)
    for user_id in wolf_ids:
        user = func.get_member(user_id)
        if user:
            message = "あなたは人狼です"
            file_name = "image/werewolf.jpg"
            file = discord.File(file_name, filename=file_name)
            await user.send(message, file=file)
            if wlfs_text:
                await user.send(f"人狼は{wlfs_text}です\n<#{WLF_CH_ID}>")
            sent_msg = await user.send("準備ができたら🆗をおしてください")
            await sent_msg.add_reaction("🆗")
            await asyncio.sleep(0.5)

async def check_killed_victim():
    killed_id = func.update_kill()
    alive_wolf_ids = func.get_alive_wolfs()
    if killed_id:
        user = func.get_member(killed_id)
        await user.send("あなたは襲撃され殺されました")
        await add_rip_role_and_prefix(killed_id)
        killed_name = func.get_name_by_id(killed_id)
        if len(alive_wolf_ids) >= 2:
            channel = SERVER.get_channel(WLF_CH_ID)
            await channel.send(f"「{killed_name}」の襲撃に成功しました")
        else:
            alive_wolf_id = next(iter(alive_wolf_ids), None)
            alive_wlf = func.get_member(alive_wolf_id)
            await alive_wlf.send(f"「{killed_name}」の襲撃に成功しました")
        return killed_name
    elif killed_id == 0:
        return None
    else:
        await func.send_guard_result()
        if len(alive_wolf_ids) >= 2:
            channel = SERVER.get_channel(WLF_CH_ID)
            await channel.send("襲撃に失敗しました")
        else:
            alive_wolf_id = next(iter(alive_wolf_ids), None)
            alive_wlf = func.get_member(alive_wolf_id)
            await alive_wlf.send("襲撃に失敗しました")
        return None

async def add_rip_role_and_prefix(user_id):
    member = await SERVER.fetch_member(int(user_id))
    if member:
        role = SERVER.get_role(RIP_RL_ID)
        await member.add_roles(role)
        await member.send(f"<#{RIP_CH_ID}>")
        display_name = f"💀{member.display_name}"
        try:
            await member.edit(nick=display_name)
        except:
            pass

#### SYSTEM2 ####
async def member_setting_ops(message, embed):
    user_ids = re.findall(r'@[0-9]{18,20}', embed.description)
    user_ids = list(map(lambda x: int(x.replace('@', '')), user_ids))
    if len(user_ids) < 4:
        embed.set_footer(text="人数が不足しています\nメンバーを追加してください")
        await message.edit(embed=embed)
    elif len(user_ids) > 15:
        embed.set_footer(text="人数が多すぎます\nメンバーを減らしてください")
        await message.edit(embed=embed)
    else:
        embed.set_footer(text="読み込み中です")
        await message.edit(embed=embed)
        dsc_lines = embed.description.split("\n")
        existing_names = []
        for index, user_id in enumerate(user_ids, start=1):
            member = await SERVER.fetch_member(user_id)
            if member:
                display_name = member.display_name
                display_name = display_name.encode('cp932', 'ignore').decode('cp932')
                if not display_name:
                    embed.set_footer(text="ERROR\n名前が取得できないメンバーが含まれています")
                    await message.edit(embed=embed)
                    return
                elif display_name in existing_names:
                    embed.set_footer(text="ERROR\n名前が重複するメンバーが含まれています")
                    await message.edit(embed=embed)
                    return
                else:
                    existing_names.append(display_name)
                    dsc_lines[index] = f"<@{user_id}> -> {display_name}"
                func.set_member(user_id, member, display_name)
        embed.description = "\n".join(dsc_lines)
        embed.set_footer(text="表示名を確認して🆗を押してください")
        await message.edit(embed=embed)
        await message.add_reaction('🆗')

async def remove_death_prefix():
    voice_ch = SERVER.get_channel(VOICE_CH_ID)
    for member in voice_ch.members:
        if member.display_name.startswith("💀"):
            new_display_name = member.display_name[1:]
            try:
                await member.edit(nick=new_display_name)
            except discord.Forbidden:
                continue
            except:
                pass

async def remove_all_rip_role():
    role = SERVER.get_role(RIP_RL_ID)
    for member in role.members:
        await member.remove_roles(role)

async def task_kill():
    global GLOBAL_TASK
    global EXIT_FLG
    EXIT_FLG = True
    if GLOBAL_TASK:
        GLOBAL_TASK.cancel()
        GLOBAL_TASK = None

def reset_global():
    global GLOBAL_TASK, EXIT_FLG, M_EXIT_FLG, USER_EXIT_FLG, VOTE_REPEAT, DAY
    GLOBAL_TASK = None
    EXIT_FLG = False
    M_EXIT_FLG = False
    USER_EXIT_FLG = False
    VOTE_REPEAT = MAX_VOTE_REPEAT
    DAY = 0

#### MAIN ####
@bot.event
async def on_raw_reaction_add(payload):
    global MAIN_EMB_ID, VOTE_REPEAT
    if payload.user_id == bot.user.id:
        return
    if payload.channel_id == TXT_CH_ID and payload.message_id == MAIN_EMB_ID:
        message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
        embed = message.embeds[0]
        member = await get_payload_member(payload)
        if payload.emoji.name == '✅':
            await message.remove_reaction(payload.emoji, member)
            if embed.title == "人狼メンバー設定":
                await remove_all_werewolf_room()
                await remove_all_rip_role()
                await remove_death_prefix()
                func.reset_data()
                await member_setting_ops(message, embed)
            elif embed.title == "ゲームを開始します":
                await message.clear_reactions()
                reset_global()
                name_count = func.get_count_alives()
                embed.title = "おそろしい夜がやってきました"
                embed.color = 0xFF0000
                embed.description = "**LOADING** "+"□"*name_count
                embed.set_footer(text="配役確認中です\nLOADINGが完了するまでお待ちください")
                await message.edit(embed=embed)
                await mute_alives()
                func.ini_settings()
                await send_werewolf_messages()
                await func.send_mad_messages()
                await func.send_guardian_messages()
                await func.send_fortune_messages()
                await func.send_shaman_messages()
                await func.send_citizen_messages()
                await send_log()
                rip_channel = SERVER.get_channel(RIP_CH_ID)
                await rip_channel.send(">>> 墓場にようこそ\nここから下が今回の墓場チャットです")
            elif embed.title == "おそろしい夜がやってきました":
                await message.clear_reactions()
                embed.title = "朝を迎えました"
                embed.color = 0x87CEEB
                embed.description = ""
                embed.set_footer(text="ステータスの確認中です")
                await message.edit(embed=embed)
                await send_log()
                await asyncio.sleep(3)
                killed_name = await check_killed_victim()
                await remove_all_werewolf_room()
                flg_game = func.check_game_status()
                if flg_game == 2:
                    await send_log(flg=2)
                    result = func.get_result()
                    dsc_txt = "村人陣営の勝利です\n"+"-"*23+f"\n{result}\n"+"-"*23
                    embed.title = "人狼はいなくなりました"
                    embed.description = dsc_txt
                    embed.set_footer(text="同じメンバーで次のゲームを始める場合は✅を押してください")
                    await message.edit(embed=embed)
                    await unmute_all()
                    await remove_death_prefix()
                    await send_log(flg=3)
                    await message.add_reaction('✅')
                    await message.add_reaction('🛠️')
                elif flg_game == 1:
                    if killed_name:
                        await send_log(name=killed_name, flg=2)
                    result = func.get_result()
                    dsc_txt = "人外陣営の勝利です\n"+"-"*23+f"\n{result}\n"+"-"*23
                    embed.title = "村人は全員人狼に食べられました"
                    embed.description = dsc_txt
                    embed.color = 0x660000
                    embed.set_footer(text="同じメンバーで次のゲームを始める場合は✅を押してください")
                    await message.edit(embed=embed)
                    await unmute_all()
                    await remove_death_prefix()
                    await send_log(flg=4)
                    await message.add_reaction('✅')
                    await message.add_reaction('🛠️')
                elif flg_game == 0:
                    alives_count = func.get_count_alives()
                    if killed_name:
                        await send_log(name=killed_name, flg=2)
                        embed.description = f"「{killed_name}」が無残な姿で発見されました\n\n生存者は{alives_count}人です"
                    else:
                        await send_log(flg=2)
                        embed.description = f"昨夜の犠牲者はいませんでした\n\n生存者は{alives_count}人です\n会議を始めてください"
                    embed.set_footer(text="会議時間は5分です")
                    await message.edit(embed=embed)
                    await discussion_tasks(message)
            elif embed.title == "朝を迎えました" or embed.title == "朝の会議をスキップしました":
                await message.clear_reactions()
                if QA_FLG == 0:
                    await qa_tasks(message)
                elif QA_FLG == 1:
                    func.reset_vote()
                    alives = func.get_alives()
                    alives_count = len(alives)
                    embed.title = "1名を選んで処刑します"
                    embed.color = 0x8B4513
                    embed.description = "**LOADING** "+"□"*alives_count
                    embed.set_footer(text="投票先をきめてください")
                    await message.edit(embed=embed)
                    for user_id in alives:
                        await func.send_select_executed(user_id)
                        await asyncio.sleep(0.3)
                    embed.set_footer(text="投票先の集計中です\nLOADINGが完了するまでお待ちください")
                    await message.edit(embed=embed)
            elif embed.title == "人狼はいなくなりました" or embed.title == "村人は全員人狼に食べられました":
                await message.clear_reactions()
                func.restart_data()
                names_txt = func.get_names_txt()
                await remove_all_werewolf_room()
                await remove_all_rip_role()
                await remove_death_prefix()
                embed.title = "ゲームを開始します"
                embed.description = f"以下のメンバーで開始します\n`{names_txt}`"
                embed.color = 0x660000
                embed.set_footer(text='VCにメンバーが集まったら🆗を押してください')
                await message.edit(embed=embed)
                await message.clear_reactions()
                await message.add_reaction('🆗')
                await message.add_reaction('🛠️')
            elif embed.title == "質疑応答が終了しました" or embed.title == "質疑応答をスキップしました":
                await message.clear_reactions()
                func.reset_vote()
                alives = func.get_alives()
                alives_count = len(alives)
                embed.title = "1名を選んで処刑します"
                embed.color = 0x8B4513
                embed.description = "**LOADING** "+"□"*alives_count
                embed.set_footer(text="投票先をきめてください")
                await message.edit(embed=embed)
                for user_id in alives:
                    await func.send_select_executed(user_id)
                    await asyncio.sleep(0.3)
                embed.set_footer(text="投票先の集計中です\nLOADINGが完了するまでお待ちください")
                await message.edit(embed=embed)
            elif embed.title == "投票が完了しました":
                await message.clear_reactions()
                embed.description = "集計中です"
                embed.set_footer(text="しばらくお待ちください")
                await message.edit(embed=embed)
                await asyncio.sleep(2)
                pre_exed_ids = func.get_vote_max_ids()
                vote_dsc = func.mk_vote_dsc()
                alives_count = func.get_count_alives()
                if len(pre_exed_ids) == alives_count:
                    embed.title = "全員同率の投票となりました"
                    embed.description = f"投票結果\n{vote_dsc}\n投票をやり直してください"
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                    await send_log(vtx=vote_dsc)
                    await message.add_reaction('✅')
                elif len(pre_exed_ids) > 1 and VOTE_REPEAT != 0:
                    for pre_exed_id in pre_exed_ids:
                        pre_exer = func.get_member(pre_exed_id)
                        await pre_exer.send("処刑対象の候補になりました\n弁明の準備をしてください")
                        await asyncio.sleep(0.3)
                    VOTE_REPEAT -= 1
                    embed.title = "最多得票者が複数となりました"
                    embed.description = f"投票結果\n{vote_dsc}\n弁明の時間に移ります"
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                    await send_log(vtx=vote_dsc)
                    await message.add_reaction('✅')
                elif len(pre_exed_ids) > 1 and VOTE_REPEAT == 0:
                    if VOTE_RANDOM == 1:
                        embed.title = "最多得票者が同率でした"
                        embed.description = f"投票結果\n{vote_dsc}"
                        embed.set_footer(text="1人がランダムで選ばれ処刑されます\nしばらくお待ちください")
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        executed_id = random.choics(list(pre_exed_ids))
                        func.update_status(executed_id, 5)
                        VOTE_REPEAT = MAX_VOTE_REPEAT
                        exer = func.get_member(executed_id)
                        await exer.send("あなたは処刑される事となりました\n遺言を残してください")
                        exer_name = func.get_name_by_id(executed_id)
                        embed.title = "処刑対象が決定しました"
                        embed.color = 0x8B4513
                        embed.description = f"投票結果\n{vote_dsc}\n「{exer_name}」が処刑されることになりました\n遺言の時間に移ります"
                        embed.set_footer(text="✅を押して進行してください")
                        await message.edit(embed=embed)
                        await send_log(vtx=vote_dsc)
                        await message.add_reaction('✅')
                    else:
                        embed.title = "最多得票者が同率でした"
                        embed.description = f"投票結果\n{vote_dsc}"
                        embed.set_footer(text="処刑がスキップされます\n✅を押して進行してください")
                        await message.edit(embed=embed)
                        VOTE_REPEAT = MAX_VOTE_REPEAT
                        await send_log(vtx=vote_dsc)
                        await send_log(flg=1)
                        await message.add_reaction('✅')
                else:
                    executed_id = next(iter(pre_exed_ids), None)
                    func.update_status(executed_id, 5)
                    VOTE_REPEAT = MAX_VOTE_REPEAT
                    exer = func.get_member(executed_id)
                    await exer.send("あなたは処刑される事となりました\n遺言を残してください")
                    exer_name = func.get_name_by_id(executed_id)
                    embed.title = "処刑対象が決定しました"
                    embed.color = 0x8B4513
                    embed.description = f"投票結果\n{vote_dsc}\n「{exer_name}」が処刑されることになりました"
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                    await send_log(vtx=vote_dsc)
                    await message.add_reaction('✅')
            elif embed.title == "処刑対象が決定しました":
                await message.clear_reactions()
                await will_tasks(message)
            elif embed.title == "処刑が執行されました" or embed.title == "遺言がスキップされ処刑が執行されました" or embed.title == "最多得票者が同率でした":
                await message.clear_reactions()
                embed.set_footer(text="読み込み中です\nしばらくお待ちください")
                await message.edit(embed=embed)
                await asyncio.sleep(2)
                flg_game = func.check_game_status()
                if flg_game == 2:
                    result = func.get_result()
                    dsc_txt = "村人陣営の勝利です\n"+"-"*23+f"\n{result}\n"+"-"*23
                    embed.title = "人狼はいなくなりました"
                    embed.description = dsc_txt
                    embed.set_footer(text="同じメンバーで次のゲームを始める場合は✅を押してください")
                    await message.edit(embed=embed)
                    await unmute_all()
                    await remove_death_prefix()
                    await send_log(flg=3)
                    await message.add_reaction('✅')
                    await message.add_reaction('🛠️')
                elif flg_game == 1:
                    result = func.get_result()
                    dsc_txt = "人外陣営の勝利です\n"+"-"*23+f"\n{result}\n"+"-"*23
                    embed.title = "村人は全員人狼に食べられました"
                    embed.description = dsc_txt
                    embed.color = 0x660000
                    embed.set_footer(text="同じメンバーで次のゲームを始める場合は✅を押してください")
                    await message.edit(embed=embed)
                    await unmute_all()
                    await remove_death_prefix()
                    await send_log(flg=4)
                    await message.add_reaction('✅')
                    await message.add_reaction('🛠️')
                elif flg_game == 0:
                    embed.title = "おそろしい夜がやってきました"
                    embed.color = 0xFF0000
                    embed.description = "夜の行動を選択中です"
                    embed.set_footer(text="朝を迎えるまでしばらくお待ちください")
                    await message.edit(embed=embed)
                    await add_wolf_room()
                    func.reset_flg_status()
                    await send_werewolf_ops()
                    await asyncio.sleep(0.5)
                    await func.send_fortune_ops(NIGHT_AUTO_FLG)
                    await asyncio.sleep(0.5)
                    await func.send_guard_ops(GRD_FLG)
                    await asyncio.sleep(0.5)
                    await func.send_shaman_ops(NIGHT_AUTO_FLG)
                    await asyncio.sleep(0.5)
                    await func.send_others_ops(NIGHT_AUTO_FLG)                    
            elif embed.title.startswith("弁明"):
                await message.clear_reactions()
                func.reset_vote()
                alives_count = func.get_count_alives()
                prexe_count = func.get_prexe()
                vote_count = alives_count - prexe_count
                embed.title = "決選投票を始めます"
                embed.description = "**LOADING** " + "□"*vote_count
                embed.set_footer(text="しばらくお待ちください")
                await message.edit(embed=embed)
                await func.vote_again_ops()
            elif embed.title == "最多得票者が複数となりました":
                await message.clear_reactions()
                await persuasion_tasks(message)
            elif embed.title == "全員同率の投票となりました":
                await message.clear_reactions()
                func.reset_vote()
                alives = func.get_alives()
                alives_count = len(alives)
                embed.title = "1名を選んで処刑します"
                embed.color = 0x8B4513
                embed.description = "**LOADING** "+"□"*alives_count
                embed.set_footer(text="投票先をきめてください")
                await message.edit(embed=embed)
                for user_id in alives:
                    await func.send_select_executed(user_id)
                    await asyncio.sleep(0.3)
                embed.set_footer(text="投票先の集計中です\nLOADINGが完了するまでお待ちください")
                await message.edit(embed=embed)

        elif payload.emoji.name == 'ℹ️' and embed.title == "人狼メンバー設定":
            await message.remove_reaction(payload.emoji, member)
            user_ids = re.findall(r'@[0-9]{18,20}', embed.description)
            if embed.fields:
                num = embed.fields[0].name.split("(")[-1]
                num = num.strip("人)")
                try:
                    num = int(num)
                except:
                    embed.clear_fields()
                    await message.edit(embed=embed)
                    return
                if num == len(user_ids):
                    embed.clear_fields()
                    await message.edit(embed=embed)
                else:
                    embed.clear_fields()
                    ftx = func.mk_info(len(user_ids))
                    stx = f"□ その他\n再投票: 最大{MAX_VOTE_REPEAT}回まで"
                    if GRD_FLG == 1:
                        stx += "\n連続ガード: なし"
                    else:
                        stx += "\n連続ガード: あり"
                    embed.add_field(name=f'# 設定一覧 ({str(len(user_ids))}人)',
                                    value=f'```{ftx}\n{stx}```',
                                    inline=False)
                    await message.edit(embed=embed)
            else:
                ftx = func.mk_info(len(user_ids))
                stx = f"□ その他\n再投票: 最大{MAX_VOTE_REPEAT}回まで"
                if GRD_FLG == 1:
                    stx += "\n連続ガード: なし"
                else:
                    stx += "\n連続ガード: あり"
                embed.add_field(name=f'# 設定一覧 ({str(len(user_ids))}人)',
                                value=f'```{ftx}\n{stx}```',
                                inline=False)
                await message.edit(embed=embed)
        elif payload.emoji.name == '✋' and embed.title == "人狼メンバー設定":
            await message.remove_reaction(payload.emoji, member)
            user_mention = f'<@{payload.user_id}>'
            emb_description = embed.description
            if user_mention not in emb_description:
                dsc_lines = emb_description.rsplit("\n", 1)
                new_description = f'{dsc_lines[0]}\n{user_mention}\n{dsc_lines[1]}' 
            else:
                lines = emb_description.split("\n")
                new_description = ""
                for line in lines:
                    if user_mention not in line:
                        new_description += line + "\n"
            updated_embed = embed.copy()
            updated_embed.description = new_description.rstrip("\n")
            await message.edit(embed=updated_embed)
        elif payload.emoji.name == '🆗':
            await message.remove_reaction(payload.emoji, member)
            if embed.title == "人狼メンバー設定":
                await message.clear_reactions()
                names_txt = func.get_names_txt()
                if embed.fields:
                    embed.clear_fields()
                embed.title = "ゲームを開始します"
                embed.description = f"以下のメンバーで開始します\n`{names_txt}`"
                embed.color = 0x660000
                embed.set_footer(text='VCにメンバーが集まったら🆗を押してください')
                await message.edit(embed=embed)
                await message.add_reaction('🆗')
                await message.add_reaction('🛠️')
            elif embed.title == "ゲームを開始します":
                voice_ch = SERVER.get_channel(VOICE_CH_ID)
                if voice_ch:
                    member_ids = {member.id for member in voice_ch.members}
                    alives = func.get_alives()
                    if alives <= member_ids:
                        await message.clear_reactions()
                        embed.description = ""
                        embed.set_footer(text="✅を押すと役職が配られます")
                        await message.edit(embed=embed)
                        await message.add_reaction('✅')
                    else:
                        embed.set_footer(text="VCにメンバーが集まっていません")
                        await message.edit(embed=embed)
        elif payload.emoji.name == '⏭️':
            await message.clear_reactions()
            await task_kill()
            if embed.title.startswith("朝を迎えました"):
                global M_EXIT_FLG
                M_EXIT_FLG = True
                embed.title = "朝の会議をスキップしました"
                embed.description = ""
                embed.set_footer(text="しばらくお待ちください")
                await message.edit(embed=embed)
                await mute_alives()
                embed.set_footer(text="✅を押して進行してください")
                await message.edit(embed=embed)
                await message.add_reaction('✅')
            elif embed.title.startswith("質疑応答の時間です"):          
                if "人目の質問者は" in embed.description:
                    user_name = embed.description.split("人目の質問者は「")[-1].rstrip("」です")
                    user_id = func.get_id_by_name(user_name)
                    if user_id:
                        await func.clean_select_to_dm(user_id)
                        await func.clean_skip_qa_dm(user_id)
                        await func.clean_rand_to_dm(user_id)
                elif "に質問です" in embed.description:
                    user_name = embed.description.split("」から「")[0].lstrip("「")
                    user_id = func.get_id_by_name(user_name)
                    if user_id:
                        await func.clean_select_to_dm(user_id)
                        await func.clean_skip_qa_dm(user_id)
                        await func.clean_rand_to_dm(user_id)
                    to_name = embed.description.split("」から「")[-1].rstrip("」に質問です")
                    to_id = func.get_id_by_name(to_name)
                    if to_id:
                        await func.clean_select_to_dm(to_id)
                embed.title = "質疑応答をスキップしました"
                embed.description = ""
                embed.set_footer(text="✅を押して進行してください")
                await message.edit(embed=embed)
                await mute_alives()
                await message.add_reaction('✅')
        elif payload.emoji.name == '🛠️' and embed.title == "ゲームを開始します":
            await message.clear_reactions()
            ids = func.get_ids()
            mentions = ""
            for user_id in ids:
                mentions += f"<@{user_id}>\n"
            embed.title='人狼メンバー設定'
            embed.description='-'*23+'\n'+ mentions + '-'*23
            embed.set_footer(text="メンバーを設定して✅を押してください")
            await message.edit(embed=embed)
            await message.add_reaction('✋')
            await message.add_reaction('🗣️')
            await message.add_reaction('ℹ️')
            await message.add_reaction('✅')
        elif payload.emoji.name == '🛠️' and (embed.title == "人狼はいなくなりました" or embed.title == "村人は全員人狼に食べられました"):
            await message.clear_reactions()
            ids = func.get_ids()
            mentions = ""
            for user_id in ids:
                mentions += f"<@{user_id}>\n"
            embed.title='人狼メンバー設定'
            embed.description='-'*23+'\n'+ mentions + '-'*23
            embed.set_footer(text="メンバーを設定して✅を押してください")
            await message.edit(embed=embed)
            await message.add_reaction('✋')
            await message.add_reaction('🗣️')
            await message.add_reaction('ℹ️')
            await message.add_reaction('✅')
        elif payload.emoji.name == '🗣️' and embed.title == "人狼メンバー設定":
            await message.remove_reaction(payload.emoji, member)
            voice_ch = SERVER.get_channel(VOICE_CH_ID)
            if voice_ch:
                member_ids = {member.id for member in voice_ch.members}
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

    elif payload.channel_id == TXT_CH_ID and payload.message_id != MAIN_EMB_ID:
        message = await MAIN_CH.fetch_message(payload.message_id)
        if message.author != bot.user:
            return
        if payload.emoji.name == '❌':
            await message.delete()
        elif message.embeds:
            embed = message.embeds[0]
            await message.clear_reactions()
            embed.set_footer(text="この埋め込みは現在ACTIVEではありません\n新しい埋め込みを作成してください")
            await message.edit(embed=embed)
            await message.add_reaction('❌')
        
    elif payload.channel_id == WLF_CH_ID:
        channel = SERVER.get_channel(WLF_CH_ID)
        message = await channel.fetch_message(payload.message_id)
        if message.author != bot.user:
            return
        if message.content.startswith("襲撃する対象を選んでください"): # 以下のユーザーを襲撃します
            wolf_count = len(func.get_alive_wolfs())
            messages = message.content.split("\n")
            for i in range(len(REACTION_EMOJIS_A)):
                if payload.emoji.name == REACTION_EMOJIS_A[i]:
                    count = 0
                    for reaction in message.reactions:
                        if str(reaction.emoji) == REACTION_EMOJIS_A[i]:
                            count = reaction.count
                            break
                    if count == wolf_count + 1: # wlfs + bot
                        selected_line = messages[i+1]
                        target_name = selected_line.split(": ")[-1]
                        if RC_FLG == 1:
                            sent_message = await channel.send(f"以下のユーザーを襲撃します\n{target_name}")
                            await sent_message.add_reaction(REACTION_EMOJIS_B[0])
                            await sent_message.add_reaction(REACTION_EMOJIS_B[1])
                            break
                        elif RC_FLG == 0:
                            await message.delete()
                            target_id = func.get_id_by_name(target_name)
                            await channel.send(f"「{target_name}」を襲撃しました")
                            func.update_status(target_id, 1)
                            target_message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
                            target_embed = target_message.embeds[0]
                            alives_count = func.get_count_alives()
                            check_count = func.update_check_wolf()
                            if check_count == alives_count:
                                new_embed = target_embed.copy()
                                new_embed.set_footer(text="✅を押して進行してください")
                                await target_message.edit(embed=new_embed)
                                await target_message.add_reaction('✅')
                            break
        elif message.content.startswith("以下のユーザーを襲撃します"): # at wlfs_room
            if payload.emoji.name == '⭕':
                target_name = message.content.split('\n')[1]
                await message.delete()
                async for msg in channel.history(limit=30):
                    if msg.author != bot.user:
                        continue
                    if msg.content.startswith("襲撃する対象を選んでください"):
                        await msg.delete()
                        break
                kil_check = func.check_status(1)
                if kil_check == 1:
                    async for msg in channel.history(limit=10):
                        if msg.author != bot.user:
                            continue
                        if msg.content.startswith("以下のユーザーを襲撃します"):
                            await msg.delete()
                else:
                    target_id = func.get_id_by_name(target_name)
                    await channel.send(f"「{target_name}」を襲撃しました")
                    func.update_status(target_id, 1)
                    target_message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
                    target_embed = target_message.embeds[0]
                    alives_count = func.get_count_alives()
                    check_count = func.update_check_wolf()
                    if check_count == alives_count:
                        new_embed = target_embed.copy()
                        new_embed.set_footer(text="✅を押して進行してください")
                        await target_message.edit(embed=new_embed)
                        await target_message.add_reaction('✅')
            elif payload.emoji.name == '❌':
                await message.delete()

    else:
        channel = await bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if isinstance(channel, discord.DMChannel):
            global USER_EXIT_FLG
            if payload.emoji.name == '🆗':
                if message.content.startswith("確認ができたら") or message.content.startswith("準備ができたら"):
                    await message.delete()
                    target_message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
                    target_embed = target_message.embeds[0]
                    check_count = func.update_check_count(payload.user_id)
                    alives_count = func.get_count_alives()
                    new_embed = target_embed.copy()
                    if check_count == alives_count:
                        new_embed.description = "**LOADING** "+"■"*check_count
                        new_embed.set_footer(text="配役の確認が完了しました\n✅を押して進行してください")
                        await target_message.edit(embed=new_embed)
                        await target_message.add_reaction('✅')
                    else:
                        new_embed.description = "**LOADING** "+"■"*check_count + "□"*(alives_count - check_count)
                        await target_message.edit(embed=new_embed)
                elif message.content.startswith("あなたは深い眠り"):
                    await message.delete()
                    target_message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
                    target_embed = target_message.embeds[0]
                    check_count = func.update_check_count(payload.user_id)
                    alives_count = func.get_count_alives()
                    if check_count == alives_count:
                        new_embed = target_embed.copy()
                        new_embed.set_footer(text="✅を押して進行してください")
                        await target_message.edit(embed=new_embed)
                        await target_message.add_reaction('✅')

            elif payload.emoji.name == '⏭️':
                if message.content.startswith("質問をスキップする場合は"):
                    await message.delete()
                    USER_EXIT_FLG = True
                    target_message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
                    target_embed = target_message.embeds[0]
                    user_name = func.get_name_by_id(payload.user_id)
                    target_embed.description = f"「{user_name}」が質問をスキップしました"
                    target_embed.set_footer(text="次の質問者へ移ります")
                    await target_message.edit(embed=target_embed)
                    to_id = func.get_qa_to_id(DAY, payload.user_id)
                    user_ids = [payload.user_id]
                    if to_id:
                        user_ids.append(to_id)
                    await mute_alives(user_ids)
                    await func.clean_select_to_dm(payload.user_id)
                    await func.clean_rand_to_dm(payload.user_id)
                    if to_id:
                        await func.clean_select_to_dm(to_id)
                    msg = await channel.send("あなたの質問の時間がスキップされました")
                    await asyncio.sleep(5)
                    try:
                        await msg.delete()
                    except:
                        pass
                elif message.content.startswith("弁明をスキップする場合は"):
                    await message.delete()
                    USER_EXIT_FLG = True
                    await mute_alives([payload.user_id])
                    await func.clean_persuasion_dm([payload.user_id])
                    msg = await channel.send("あなたの弁明がスキップされました")
                    await asyncio.sleep(5)
                    try:
                        await msg.delete()
                    except:
                        pass
                elif message.content.startswith("遺言をスキップする場合は"):
                    await message.delete()
                    await task_kill()
                    await mute_alives([payload.user_id])
                    target_message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
                    target_embed = target_message.embeds[0]
                    await func.clean_will_dm(payload.user_id)
                    await channel.send("遺言がスキップされ処刑が執行されました")
                    await add_rip_role_and_prefix(payload.user_id)
                    await send_log(id=payload.user_id, flg=1)
                    target_embed.title = "処刑が執行されました"
                    target_embed.color = 0x8B4513
                    target_embed.description = ""
                    target_embed.set_footer(text="✅を押して進行してください")
                    await target_message.edit(embed=target_embed)
                    await target_message.add_reaction('✅')

            elif payload.emoji.name in REACTION_EMOJIS_A:
                if message.content.startswith("処刑対象に投票してください"): # 以下のユーザーに投票します
                    messages = message.content.split("\n")
                    for i in range(len(REACTION_EMOJIS_A)):
                        if payload.emoji.name == REACTION_EMOJIS_A[i]:
                            selected_line = messages[i+1]
                            target_name = selected_line.split(": ")[-1]
                            if RC_FLG == 1:
                                sent_message = await channel.send(f"以下のユーザーに投票します\n{target_name}")
                                await sent_message.add_reaction(REACTION_EMOJIS_B[0])
                                await sent_message.add_reaction(REACTION_EMOJIS_B[1])
                                break
                            else:
                                await message.delete()
                                check_count = func.update_check_count(payload.user_id)
                                if check_count != -1:
                                    await vote_ops(payload.user_id, target_name)
                                break
                elif message.content.startswith("襲撃する対象を選んでください"): # 以下のユーザーを襲撃します
                    messages = message.content.split("\n")
                    for i in range(len(REACTION_EMOJIS_A)):
                        if payload.emoji.name == REACTION_EMOJIS_A[i]:
                            selected_line = messages[i+1]
                            target_name = selected_line.split(": ")[-1]
                            if RC_FLG == 1:
                                sent_message = await channel.send(f"以下のユーザーを襲撃します\n{target_name}")
                                await sent_message.add_reaction(REACTION_EMOJIS_B[0])
                                await sent_message.add_reaction(REACTION_EMOJIS_B[1])
                                break
                            else:
                                await message.delete()
                                kil_check = func.check_status(1)
                                if kil_check == 0:
                                    target_id = func.get_id_by_name(target_name)
                                    await channel.send(f"「{target_name}」を襲撃しました")
                                    func.update_status(target_id, 1)
                                    await night_ops(payload.user_id)
                                break
                elif message.content.startswith("占う対象を選んでください"): # 以下のユーザーを占います
                    messages = message.content.split("\n")
                    for i in range(len(REACTION_EMOJIS_A)):
                        if payload.emoji.name == REACTION_EMOJIS_A[i]:
                            selected_line = messages[i+1]
                            target_name = selected_line.split(": ")[-1]
                            if RC_FLG == 1:
                                sent_message = await channel.send(f"以下のユーザーを占います\n{target_name}")
                                await sent_message.add_reaction(REACTION_EMOJIS_B[0])
                                await sent_message.add_reaction(REACTION_EMOJIS_B[1])
                                break
                            else:
                                await message.delete()
                                ftn_check = func.check_status(2)
                                if ftn_check == 0:
                                    target_id = func.get_id_by_name(target_name)
                                    await func.send_fortune_result(target_id, payload.user_id)
                                    await night_ops(payload.user_id)
                                break
                elif message.content.startswith("保護する対象を選んでください"): # 以下のユーザーを守ります
                    messages = message.content.split("\n")
                    for i in range(len(REACTION_EMOJIS_A)):
                        if payload.emoji.name == REACTION_EMOJIS_A[i]:
                            selected_line = messages[i+1]
                            target_name = selected_line.split(": ")[-1]
                            if RC_FLG == 1:
                                sent_message = await channel.send(f"以下のユーザーを守ります\n{target_name}")
                                await sent_message.add_reaction(REACTION_EMOJIS_B[0])
                                await sent_message.add_reaction(REACTION_EMOJIS_B[1])
                                break
                            else:
                                await message.delete()
                                grd_check = func.check_status(3)
                                if grd_check == 0:
                                    await channel.send(f"「{target_name}」を守りました")
                                    target_id = func.get_id_by_name(target_name)
                                    func.update_status(target_id, 3)
                                    await night_ops(payload.user_id)
                                break
                elif message.content.startswith("質問する相手を選んでください"): # 以下のユーザーに質問します
                    messages = message.content.split("\n")
                    for i in range(len(REACTION_EMOJIS_A)):
                        if payload.emoji.name == REACTION_EMOJIS_A[i]:
                            selected_line = messages[i+1]
                            target_name = selected_line.split(": ")[-1]
                            if RC_FLG == 1:
                                sent_message = await channel.send(f"以下のユーザーに質問します\n{target_name}")
                                await sent_message.add_reaction(REACTION_EMOJIS_B[0])
                                await sent_message.add_reaction(REACTION_EMOJIS_B[1])
                                break
                            else:
                                await message.delete()
                                target_id = func.get_id_by_name(target_name)
                                func.update_qa(DAY, payload.user_id, target_id)

            elif payload.emoji.name == '❌':
                for reaction in message.reactions:
                    if reaction.emoji == '❌':
                        if reaction.count == 2:
                            await message.delete()
                        break
            elif payload.emoji.name == '⭕':
                if message.content.startswith("以下のユーザーに投票します"):
                    target_name = message.content.split('\n')[1]
                    await message.delete()
                    async for msg in channel.history(limit=10):
                        if msg.author == bot.user:
                            if msg.content.startswith("処刑対象に投票してください"):
                                await msg.delete()
                                break
                    check_count = func.update_check_count(payload.user_id)
                    if check_count == -1:
                        async for msg in channel.history(limit=10):
                            if msg.author != bot.user:
                                continue
                            if msg.content.startswith("以下のユーザーに投票します"):
                                await msg.delete()
                    else:
                        await vote_ops(payload.user_id, target_name)
                elif message.content.startswith("以下のユーザーを襲撃します"):
                    target_name = message.content.split('\n')[1]
                    await message.delete()
                    async for msg in channel.history(limit=10):
                        if msg.author != bot.user:
                            continue
                        if msg.content.startswith("襲撃する対象を選んでください"):
                            await msg.delete()
                            break
                    kil_check = func.check_status(1)
                    if kil_check == 1:
                        async for msg in channel.history(limit=10):
                            if msg.author != bot.user:
                                continue
                            if msg.content.startswith("以下のユーザーを襲撃します"):
                                await msg.delete()
                    else:
                        target_id = func.get_id_by_name(target_name)
                        await channel.send(f"「{target_name}」を襲撃しました")
                        func.update_status(target_id, 1)
                        await night_ops(payload.user_id)
                elif message.content.startswith("以下のユーザーを占います"):
                    target_name = message.content.split('\n')[1]
                    await message.delete()
                    async for msg in channel.history(limit=10):
                        if msg.author != bot.user:
                            continue
                        if  msg.content.startswith("占う対象を選んでください"):
                            await msg.delete()
                            break
                    ftn_check = func.check_status(2)
                    if ftn_check == 1:
                        async for msg in channel.history(limit=10):
                            if msg.author != bot.user:
                                continue
                            if  msg.content.startswith("以下のユーザーを占います"):
                                await msg.delete()
                    else:
                        target_id = func.get_id_by_name(target_name)
                        await func.send_fortune_result(target_id, payload.user_id)
                        await night_ops(payload.user_id)
                elif message.content.startswith("以下のユーザーを守ります"):
                    target_name = message.content.split('\n')[1]
                    await message.delete()
                    async for msg in channel.history(limit=20):
                        if msg.author != bot.user:
                            continue
                        if msg.content.startswith("保護する対象を選んでください"):
                            await msg.delete()
                            break
                    grd_check = func.check_status(3)
                    if grd_check == 1:
                        async for msg in channel.history(limit=10):
                            if msg.author != bot.user:
                                continue
                            if  msg.content.startswith("以下のユーザーを守ります"):
                                await msg.delete()
                    else:
                        await channel.send(f"「{target_name}」を守りました")
                        target_id = func.get_id_by_name(target_name)
                        func.update_status(target_id, 3)
                        await night_ops(payload.user_id)
                elif message.content.startswith("以下のユーザーに質問します"):
                    target_name = message.content.split('\n')[1]
                    await message.delete()
                    async for msg in channel.history(limit=20):
                        if msg.author != bot.user:
                            continue
                        if msg.content.startswith("質問する相手を選んでください"):
                            await msg.delete()
                            break
                    target_id = func.get_id_by_name(target_name)
                    func.update_qa(DAY, payload.user_id, target_id)

#### !CMMAND ####
@bot.command(name='jinro')
async def create_embed_with_reaction(ctx: commands.Context):
    global MAIN_EMB_ID
    await ctx.message.delete()
    if not MAIN_EMB_ID:
        embed = discord.Embed(title='人狼メンバー設定', color=0x660000, description='-'*23+'\n'+'-'*23)
        embed.set_footer(text="メンバーを設定して✅を押してください")
        message = await ctx.send(embed=embed)
        await message.add_reaction('✋')
        await message.add_reaction('🗣️')
        await message.add_reaction('ℹ️')
        await message.add_reaction('✅')
        MAIN_EMB_ID = message.id

@bot.command(name='jinro_new')
async def create_new_embed(ctx: commands.Context):
    global MAIN_EMB_ID
    await ctx.message.delete()
    embed = discord.Embed(title='人狼メンバー設定', color=0x660000, description='-'*23+'\n'+'-'*23)
    embed.set_footer(text="メンバーを設定して✅を押してください")
    message = await ctx.send(embed=embed)
    await message.add_reaction('✋')
    await message.add_reaction('🗣️')
    await message.add_reaction('ℹ️')
    await message.add_reaction('✅')
    MAIN_EMB_ID = message.id

@bot.command(name='jinro_re')
async def create_new_embed_copy(ctx: commands.Context):
    global MAIN_EMB_ID
    await ctx.message.delete()
    async for message in ctx.channel.history(limit=30):
        if message.embeds:
            for embed in message.embeds:
                if embed.type == 'rich':
                    break
    if embed:
        mentions = re.findall(r'<@[0-9]{18,20}>', embed.description)
        dsc = ("\n").join(mentions)
        await message.delete()
        new_embed = discord.Embed(title='人狼メンバー設定', color=0x660000, description='-'*23+'\n'+ dsc +'\n'+'-'*23)
        new_embed.set_footer(text="メンバーを設定して✅を押してください")
        new_message = await ctx.send(embed=new_embed)
        await new_message.add_reaction('✋')
        await new_message.add_reaction('🗣️')
        await new_message.add_reaction('ℹ️')
        await new_message.add_reaction('✅')
        MAIN_EMB_ID = new_message.id

@bot.command(name='adj')
async def ad_username(ctx: commands.Context, *names):
    global MAIN_EMB_ID
    await ctx.message.delete()
    if MAIN_EMB_ID:
        message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
        embed = message.embeds[0]
        new_embed = embed.copy()
        dsc_lines = new_embed.description.rsplit("\n", 1)
        names_text = "\n".join(names)
        new_embed.description = f'{dsc_lines[0]}\n{names_text}\n{dsc_lines[1]}'
        await message.edit(embed=new_embed)

@bot.command(name='rmj')
async def rm_username(ctx: commands.Context, usermention: str):
    global MAIN_EMB_ID
    await ctx.message.delete()
    if MAIN_EMB_ID:
        message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
        embed = message.embeds[0]
        new_embed = embed.copy()
        description_lines = new_embed.description.split('\n')
        updated_description = ''
        deleted = False
        for line in description_lines:
            if usermention not in line:
                updated_description += line + '\n'
            elif not deleted:
                deleted = True
            else:
                updated_description += line + '\n'
        new_embed.description = updated_description.rstrip('\n')
        await message.edit(embed=new_embed)

@bot.command(name='reset_aj')
async def reset_username(ctx: commands.Context):
    global MAIN_EMB_ID
    await ctx.message.delete()
    if MAIN_EMB_ID:
        message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
        embed = message.embeds[0]
        new_embed = embed.copy()
        new_embed.description = '-'*23+'\n'+'-'*23
        await message.edit(embed=new_embed)

@bot.command(name='delete_j')
async def delete_embed(ctx: commands.Context):
    global MAIN_EMB_ID
    await ctx.message.delete()
    async for message in ctx.channel.history(limit=30):
        if message.author != bot.user:
            continue
        if message.embeds:
            for embed in message.embeds:
                if embed.type == 'rich':
                    if message.id == MAIN_EMB_ID:
                        MAIN_EMB_ID = None
                    await message.delete()
                return

@bot.command(name='prest')
async def create_embed_prestart(ctx: commands.Context):
    global MAIN_EMB_ID
    await ctx.message.delete()
    embed = discord.Embed(title='ゲームを開始します', color=0x660000)
    embed.set_footer(text='VCにメンバーが集まったら🆗を押してください')
    message = await ctx.send(embed=embed)
    await message.add_reaction('🆗')
    MAIN_EMB_ID = message.id

@bot.command(name='premo')
async def create_embed_premorning(ctx: commands.Context):
    global MAIN_EMB_ID
    await ctx.message.delete()
    embed = discord.Embed(title='おそろしい夜がやってきました', color=0xFF0000)
    embed.description = "朝の会議から始まります"
    embed.set_footer(text="✅を押して進行してください")
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')
    MAIN_EMB_ID = message.id

@bot.command(name='preq')
async def create_embed_preinterview(ctx: commands.Context):
    global MAIN_EMB_ID
    await ctx.message.delete()
    embed = discord.Embed(title='会議の時間です', color=0x8B4513)
    embed.description = "質疑応答から始まります"
    embed.set_footer(text="✅を押して進行してください")
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')
    MAIN_EMB_ID = message.id

@bot.command(name='prexe')
async def create_embed_preexecution(ctx: commands.Context):
    global MAIN_EMB_ID
    await ctx.message.delete()
    embed = discord.Embed(title='質疑応答が終了しました', color=0x8B4513)
    embed.description = "処刑から始まります"
    embed.set_footer(text="✅を押して進行してください")
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')
    MAIN_EMB_ID = message.id

@bot.command(name='preni')
async def create_embed_prenight(ctx: commands.Context):
    global MAIN_EMB_ID
    await ctx.message.delete()
    embed = discord.Embed(title='処刑が執行されました', color=0x8B4513)
    embed.description = "夜時間から始まります"
    embed.set_footer(text="✅を押して進行してください")
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')
    MAIN_EMB_ID = message.id

@bot.command(name='skip')
async def skip_to_next(ctx: commands.Context):
    await ctx.message.delete()
    await task_kill()
    if MAIN_EMB_ID:
        message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
        await message.clear_reactions()
        embed = message.embeds[0]
        if embed.title.startswith("朝を迎えました"):
            global M_EXIT_FLG
            M_EXIT_FLG = True
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
                    await func.clean_select_to_dm(user_id)
                    await func.clean_skip_qa_dm(user_id)
                    await func.clean_rand_to_dm(user_id)
            elif "に質問です" in embed.description:
                user_name = embed.description.split("」から「")[0].lstrip("「")
                user_id = func.get_id_by_name(user_name)
                if user_id:
                    await func.clean_select_to_dm(user_id)
                    await func.clean_skip_qa_dm(user_id)
                    await func.clean_rand_to_dm(user_id)
                to_name = embed.description.split("」から「")[-1].rstrip("」に質問です")
                to_id = func.get_id_by_name(to_name)
                if to_id:
                    await func.clean_select_to_dm(to_id)
            embed.title = "質疑応答をスキップしました"
            embed.description = ""
            embed.set_footer(text="✅を押して進行してください")
            await message.edit(embed=embed)
            await mute_alives()
            await message.add_reaction('✅')
        elif embed.title.startswith("遺言の時間"):
            executed_name = embed.description.split("」が処刑される")[0].split("\n「")[-1]
            executed_id = func.get_id_by_name(executed_name)
            await mute_alives([executed_id])
            await func.clean_will_dm(executed_id)
            user = func.get_member(executed_id)
            await user.send("あなたは処刑されました")
            await add_rip_role_and_prefix(executed_id)
            await send_log(id=executed_id, flg=1)
            embed.title = "遺言がスキップされ処刑が執行されました"
            embed.color = 0x8B4513
            embed.description = ""
            embed.set_footer(text="✅を押して進行してください")
            await message.edit(embed=embed)
            await message.add_reaction('✅')
        elif embed.title.startswith("弁明の時間です"):
            prexed_ids = func.get_prexe()
            func.reset_vote()
            await mute_alives(prexed_ids)
            await func.clean_persuasion_dm(prexed_ids)
            alives_count = func.get_count_alives()
            left_count = alives_count - len(prexed_ids)
            embed.title = "弁明の時間がスキップされました"
            embed.description = "**LOADING** " + "□"*left_count
            embed.set_footer(text="決選投票を始めます\nしばらくお待ちください")
            await message.edit(embed=embed)
            await func.vote_again_ops()
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

@bot.command(name='env')
async def reload_env(ctx: commands.Context, v: int = -1, g: int = -1, n: int = -1):
    await ctx.message.delete()
    global MAX_VOTE_REPEAT, GRD_FLG, NIGHT_AUTO_FLG
    if v >= 0:
        MAX_VOTE_REPEAT = int(v)
    if g == 0 or g == 1:
        GRD_FLG = g
    if n == 0 or n == 1:
        NIGHT_AUTO_FLG = n

@bot.command(name='check')
async def en_checked(ctx: commands.Context):
    await ctx.message.delete()
    if MAIN_EMB_ID:
        message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
        await message.add_reaction('✅')

@bot.command(name='rip')
async def ad_rip_role_send_ch(ctx: commands.Context, usermention: str = None):
    await ctx.message.delete()
    if usermention:
        user_id = usermention.lstrip('<@').rstrip('>')
        if user_id.isdigit():
            await add_rip_role_and_prefix(user_id)

@bot.command(name='rmrip')
async def rm_rip_role(ctx: commands.Context, usermention: str = None):
    await ctx.message.delete()
    role = SERVER.get_role(RIP_RL_ID)
    if role:
        if usermention:
            user_id = usermention.lstrip('<@').rstrip('>')
            if user_id.isdigit():
                await remove_death_prefix(user_id)
                for member in role.members:
                    if member.id == int(user_id):
                        await member.remove_roles(role)
                        break
        else:
            await remove_death_prefix()
            for member in role.members:
                await member.remove_roles(role)

@bot.command(name='adwlf')
async def ad_wlf_role(ctx: commands.Context, usermention: str = None):
    await ctx.message.delete()
    if usermention:
        user_id = usermention.lstrip('<@').rstrip('>')
        if user_id.isdigit():
            channel = SERVER.get_channel(WLF_CH_ID)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages=True
            overwrite.send_messages=True
            overwrite.add_reactions=True
            member = await SERVER.fetch_member(int(user_id))
            if not member.guild_permissions.administrator:
                try:
                    await channel.set_permissions(member, overwrite=overwrite)
                except:
                    pass

@bot.command(name='rmwlf')
async def rm_wlf_role(ctx: commands.Context, usermention: str = None):
    await ctx.message.delete()
    channel = SERVER.get_channel(WLF_CH_ID)
    overwrite = discord.PermissionOverwrite()
    overwrite.read_messages=False
    overwrite.send_messages=False
    overwrite.add_reactions=False
    if usermention:
        user_id = usermention.lstrip('<@').rstrip('>')
        if user_id.isdigit():
            for member in channel.members:
                if member.id == int(user_id):
                    if not member.guild_permissions.administrator:
                        try:
                            await channel.set_permissions(member, overwrite=overwrite)
                        except:
                            pass
                    break
    else:
        for member in channel.members:
            if not member.guild_permissions.administrator:
                try:
                    await channel.set_permissions(member, overwrite=overwrite)
                except:
                    pass

@bot.event
async def on_ready():
    global SERVER, MAIN_CH
    SERVER = bot.get_guild(GUILD_ID)
    MAIN_CH = await SERVER.fetch_channel(TXT_CH_ID)
    await SERVER.fetch_channel(VOICE_CH_ID)
    await SERVER.fetch_channel(RIP_CH_ID)
    await SERVER.fetch_channel(WLF_CH_ID)
    await SERVER.fetch_channel(LOG_CH_ID)
    print("Log in to", SERVER.name)
    print('Bot is ready.')

bot.run(TOKEN)