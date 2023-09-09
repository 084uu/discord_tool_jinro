import discord
from discord.ext import commands
import re
import asyncio
import random
import func
import gv

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
intents.messages = True
intents.reactions = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

#### LOAD ENV ####
TOKEN = ****
GUILD_ID = 
VOICE_CH_ID = 
TXT_CH_ID = 
LOG_CH_ID = 
WLF_CH_ID = 
RIP_CH_ID = 
RIP_RL_ID = 

# 選択再確認（0:なし、1:あり）
RC_FLG = 0
# ランダム処刑（0:なし、1:あり）
VOTE_RANDOM = 0
# 決選投票の最大回数 (0:得票同率時ランダム選択)
MAX_VOTE_REPEAT = 0
# 連続ガード可否（0:可、1:不可）
GRD_FLG = 1
# 夜時間簡易チェック (0:不使用、1:使用)
NIGHT_AUTO_FLG = 1
# 質疑応答時間（0:あり、1:省略）
QA_FLG = 0

###########################################################################################

#### OTHER VALUE ####
REACTION_EMOJIS = ('1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟','⏺️','🔼','⏹️','0️⃣')

#### GLOBAL VARIABLES ####
GLOBAL_TASK = None
EXIT_FLG = False
M_EXIT_FLG = False
USER_EXIT_FLG = False
VOTE_REPEAT = MAX_VOTE_REPEAT
DAY = 1

SERVER = None
MAIN_CH =None
MAIN_EMB_ID = None

#### VOICE CONTROL ####
async def mute_alives(user_ids=set()):
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

async def unmute_alives(user_ids=set()):
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

#### PROCESS ####
async def coming_first_night(message, embed):
    reset_global()
    print("### Game Start ###")
    name_count = func.get_count_alives()
    embed.title = "おそろしい夜がやってきました"
    embed.color = 0xFF0000
    embed.description = "**LOADING** "+"□"*name_count
    embed.set_footer(text="配役確認中です\nLOADINGが完了するまでお待ちください")
    await message.edit(embed=embed)
    await mute_alives()
    func.ini_settings()
    wlf_channel = SERVER.get_channel(WLF_CH_ID)
    await gv.send_werewolf_messages(wlf_channel, WLF_CH_ID)
    await func.send_first_messages()
    await send_log(flg=0)
    rip_channel = SERVER.get_channel(RIP_CH_ID)
    await rip_channel.send(">>> 墓場にようこそ\nここから下が今回の墓場チャットです")

async def coming_morning(message, embed):
    embed.title = "朝を迎えました"
    embed.color = 0x87CEEB
    embed.description = ""
    embed.set_footer(text="ステータスの確認中です")
    await message.edit(embed=embed)
    await asyncio.sleep(3)
    killed_name = await gv.check_killed_victim(SERVER, WLF_CH_ID, RIP_RL_ID, RIP_CH_ID)
    await gv.remove_all_werewolf_room(SERVER, WLF_CH_ID)
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
        await gv.remove_death_prefix(SERVER, RIP_RL_ID)
        print("___ Game End ___")
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
        await gv.remove_death_prefix(SERVER, RIP_RL_ID)
        print("___ Game End ___")
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
        await send_log(flg=5)
        await ops_tasks(message, flg=0)

async def exe_result(message, embed):
    global VOTE_REPEAT
    embed.description = "集計中です"
    embed.set_footer(text="しばらくお待ちください")
    await message.edit(embed=embed)
    await asyncio.sleep(2)
    prexed_ids = func.get_vote_max_ids()
    vote_dsc = func.mk_vote_dsc()
    alives_count = func.get_count_alives()
    if len(prexed_ids) == alives_count:
        embed.title = "全員同率の投票となりました"
        embed.description = "投票結果\n"+"-"*23+f"\n{vote_dsc}\n"+"-"*23+"\n投票をやり直してください"
        embed.set_footer(text="✅を押して進行してください")
        await message.edit(embed=embed)
        await send_log(vtx=vote_dsc)
        await message.add_reaction('✅')
    elif len(prexed_ids) > 1 and VOTE_REPEAT != 0:
        for pre_exed_id in prexed_ids:
            pre_exer = func.get_member(pre_exed_id)
            await pre_exer.send("`処刑対象の候補になりました\n弁明の準備をしてください`")
            await asyncio.sleep(0.3)
        VOTE_REPEAT -= 1
        embed.title = "最多得票者が複数となりました"
        embed.description = "投票結果\n"+"-"*23+f"\n{vote_dsc}\n"+"-"*23+"\n弁明の時間に移ります"
        embed.set_footer(text="✅を押して進行してください")
        await message.edit(embed=embed)
        await send_log(vtx=vote_dsc)
        await message.add_reaction('✅')
    elif len(prexed_ids) > 1 and VOTE_REPEAT == 0:
        if VOTE_RANDOM == 1:
            embed.title = "最多得票者が同率でした"
            embed.description = "投票結果\n"+"-"*23+f"\n{vote_dsc}\n"+"-"*23
            embed.set_footer(text="1人がランダムで選ばれ処刑されます\nしばらくお待ちください")
            await message.edit(embed=embed)
            await asyncio.sleep(3)
            executed_id = random.choice(list(prexed_ids))
            func.update_status(executed_id, 5)
            VOTE_REPEAT = MAX_VOTE_REPEAT
            exer = func.get_member(executed_id)
            await exer.send("`あなたは処刑される事となりました\n遺言を残してください`")
            exer_name = func.get_name_by_id(executed_id)
            embed.title = "処刑対象が決定しました"
            embed.color = 0x8B4513
            embed.description = "投票結果\n"+"-"*23+f"\n{vote_dsc}\n"+"-"*23+f"\n「{exer_name}」が処刑されることになりました\n遺言の時間に移ります"
            embed.set_footer(text="✅を押して進行してください")
            await message.edit(embed=embed)
            await send_log(vtx=vote_dsc)
            await message.add_reaction('✅')
        else:
            embed.title = "最多得票者が同率でした"
            embed.description = "投票結果\n"+"-"*23+f"\n{vote_dsc}\n"+"-"*23
            embed.set_footer(text="処刑がスキップされます\n✅を押して進行してください")
            await message.edit(embed=embed)
            VOTE_REPEAT = MAX_VOTE_REPEAT
            await send_log(vtx=vote_dsc)
            await send_log(flg=1)
            await message.add_reaction('✅')
    else:
        executed_id = next(iter(prexed_ids), None)
        func.update_status(executed_id, 5)
        VOTE_REPEAT = MAX_VOTE_REPEAT
        exer = func.get_member(executed_id)
        await exer.send("`あなたは処刑される事となりました\n遺言を残してください`")
        exer_name = func.get_name_by_id(executed_id)
        embed.title = "処刑対象が決定しました"
        embed.color = 0x8B4513
        embed.description = "投票結果\n"+"-"*23+f"\n{vote_dsc}\n"+"-"*23+f"\n「{exer_name}」が処刑されることになりました"
        embed.set_footer(text="✅を押して進行してください")
        await message.edit(embed=embed)
        await send_log(vtx=vote_dsc)
        await message.add_reaction('✅')

async def coming_night_or_end(message, embed):
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
        await gv.remove_death_prefix(SERVER, RIP_RL_ID)
        print("___ Game End ___")
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
        await gv.remove_death_prefix(SERVER, RIP_RL_ID)
        print("___ Game End ___")
        await send_log(flg=4)
        await message.add_reaction('✅')
        await message.add_reaction('🛠️')
    elif flg_game == 0:
        embed.title = "おそろしい夜がやってきました"
        embed.color = 0xFF0000
        embed.description = "夜の行動を選択中です"
        embed.set_footer(text="朝を迎えるまでしばらくお待ちください")
        await message.edit(embed=embed)
        wlf_channel = SERVER.get_channel(WLF_CH_ID)
        await gv.add_wolf_room(wlf_channel)
        func.reset_flg_status()
        await gv.send_werewolf_ops(wlf_channel)
        await asyncio.sleep(0.5)
        await func.send_fortune_ops(NIGHT_AUTO_FLG)
        await asyncio.sleep(0.5)
        await func.send_guard_ops(GRD_FLG)
        await asyncio.sleep(0.5)
        await func.send_shaman_ops(NIGHT_AUTO_FLG)
        await asyncio.sleep(0.5)
        await func.send_others_ops(NIGHT_AUTO_FLG)

async def skip_ops(message, embed):
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
                await func.clean_dm({user_id})
        elif "に質問です" in embed.description:
            user_name = embed.description.split("」から「")[0].lstrip("「")
            user_id = func.get_id_by_name(user_name)
            if user_id:
                await func.clean_dm({user_id})
            to_name = embed.description.split("」から「")[-1].rstrip("」に質問です")
            to_id = func.get_id_by_name(to_name)
            if to_id:
                await func.clean_dm({to_id})
        embed.title = "質疑応答をスキップしました"
        embed.description = ""
        embed.set_footer(text="✅を押して進行してください")
        await message.edit(embed=embed)
        await mute_alives()
        await message.add_reaction('✅')

async def user_skip_ops(user_id, message, channel):
    global USER_EXIT_FLG
    if message.content.startswith("`質問をスキップする場合は"):
        await message.delete()
        USER_EXIT_FLG = True
        target_message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
        target_embed = target_message.embeds[0]
        target_embed.description = "スキップ処理中です"
        target_embed.set_footer(text="しばらくお待ちください")
        await target_message.edit(embed=target_embed)
        to_id = func.get_qa_to_id(DAY, user_id)
        user_ids = {user_id}
        if to_id:
            user_ids.add(to_id)
        await mute_alives(user_ids)
        await func.clean_dm({user_id})
        if to_id:
            await func.clean_dm({to_id})
        msg = await channel.send("`あなたの質問の時間がスキップされました`")
        await asyncio.sleep(5)
        try:
            await msg.delete()
        except:
            pass
    elif message.content.startswith("`弁明をスキップする場合は"):
        await message.delete()
        USER_EXIT_FLG = True
        await mute_alives({user_id})
        await func.clean_dm({user_id})
        msg = await channel.send("`あなたの弁明がスキップされました`")
        await asyncio.sleep(5)
        try:
            await msg.delete()
        except:
            pass
    elif message.content.startswith("`遺言をスキップする場合は"):
        await message.delete()
        await task_kill()
        await mute_alives({user_id})
        target_message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
        target_embed = target_message.embeds[0]
        await func.clean_dm({user_id})
        await channel.send("遺言がスキップされ処刑が執行されました")
        await gv.add_rip_role_and_prefix(user_id, SERVER, RIP_RL_ID, RIP_CH_ID)
        await send_log(id=user_id, flg=1)
        target_embed.title = "処刑が執行されました"
        target_embed.color = 0x8B4513
        target_embed.description = ""
        target_embed.set_footer(text="✅を押して進行してください")
        await target_message.edit(embed=target_embed)
        await target_message.add_reaction('✅')

async def reaction_check_ops(message, embed):
    if embed.title == "人狼メンバー設定":
        await gv.remove_all_werewolf_room(SERVER, WLF_CH_ID)
        await gv.remove_all_rip_role(SERVER, RIP_RL_ID)
        func.reset_data()
        await gv.member_setting_ops(message, embed, SERVER)
    else:
        await message.clear_reactions()
        if embed.title == "ゲームを開始します":
            await coming_first_night(message, embed)
        elif embed.title == "おそろしい夜がやってきました":
            await coming_morning(message, embed)
        elif embed.title == "朝を迎えました" or embed.title == "朝の会議をスキップしました":
            if QA_FLG == 0:
                await ops_tasks(message, flg=1)
            elif QA_FLG == 1:
                await gv.coming_vote(message, embed)
        elif embed.title == "人狼はいなくなりました" or embed.title == "村人は全員人狼に食べられました":
            await gv.next_game(message, embed, SERVER, WLF_CH_ID, RIP_RL_ID)
        elif embed.title == "質疑応答が終了しました" or embed.title == "質疑応答をスキップしました":
            await gv.coming_vote(message, embed)
        elif embed.title == "投票が完了しました":
            await exe_result(message, embed)
        elif embed.title == "処刑対象が決定しました":
            await ops_tasks(message, flg=2)
        elif embed.title == "処刑が執行されました" or embed.title == "遺言がスキップされ処刑が執行されました" or embed.title == "最多得票者が同率でした":
            await coming_night_or_end(message, embed)
        elif embed.title.startswith("弁明"):
            await gv.coming_fin_vote(message, embed)
        elif embed.title == "最多得票者が複数となりました":
            await ops_tasks(message, flg=3)
        elif embed.title == "全員同率の投票となりました":
            await gv.coming_vote(message, embed)

#### SKIPABLE TASKS ####
async def ops_tasks(message, flg=0):
    global GLOBAL_TASK
    if flg == 0:
        GLOBAL_TASK = asyncio.create_task(discussion_ops(message))
    elif flg == 1:
        GLOBAL_TASK = asyncio.create_task(qa_ops(message))
    elif flg == 2:
        GLOBAL_TASK = asyncio.create_task(will_ops(message))
    elif flg == 3:
        GLOBAL_TASK = asyncio.create_task(persuasion_ops(message))
    await GLOBAL_TASK

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

async def qa_ops(message):
    global EXIT_FLG, USER_EXIT_FLG
    EXIT_FLG = False
    USER_EXIT_FLG = False
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
            await asyncio.sleep(3)
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
        user = func.get_member(user_id)
        smsg = await user.send("`質問をスキップする場合は⏭️を押してください`")
        await smsg.add_reaction('⏭️')
        await func.send_select_to(user_id)
        def check(payload):
            return payload.user_id == user_id
        try:
            while True:
                if EXIT_FLG or USER_EXIT_FLG: raise A_error()
                payload = await bot.wait_for("raw_reaction_add", check=check, timeout=10)
                dm_channel = await bot.fetch_channel(payload.channel_id)
                dm_message = await dm_channel.fetch_message(payload.message_id)
                if (payload.emoji.name == "⭕" and dm_message.content.startswith("`以下のユーザーに質問します")) or (RC_FLG == 0 and dm_message.content.startswith("`質問する相手を")):
                    if EXIT_FLG or USER_EXIT_FLG: raise A_error()
                    await asyncio.sleep(3)
                    to_id = func.get_qa_to_id(DAY, user_id)
                    if to_id:
                        to_name = func.get_name_by_id(to_id)
                        to_user = func.get_member(to_id)
                        embed.description = f"「{user_name}」から「{to_name}」に質問です"
                        embed.set_footer(text= "質問時間は1分です\nまもなく始まります")
                        await message.edit(embed=embed)
                        fmsg = await user.send(f"`まもなく「{to_name}」への質問が開始されます\n※まもなくミュートが外れます`")
                        tmsg = await to_user.send(f"`まもなく「{user_name}」からの質問が開始されます\n※まもなくミュートが外れます`")
                        await asyncio.sleep(3)
                        if EXIT_FLG or USER_EXIT_FLG: raise A_error()
                        await unmute_alives({user_id, to_id})
                        embed.set_footer(text="□"*6 +"\n残り時間は60秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        if EXIT_FLG or USER_EXIT_FLG: raise A_error()
                        embed.set_footer(text="■" +"□"*5 +"\n残り時間は50秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        if EXIT_FLG or USER_EXIT_FLG: raise A_error()
                        embed.set_footer(text="■"*2 +"□"*4 +"\n残り時間は40秒です")
                        await message.edit(embed=embed)
                        await fmsg.delete()
                        await tmsg.delete()
                        await asyncio.sleep(10)
                        if EXIT_FLG or USER_EXIT_FLG: raise A_error()
                        embed.set_footer(text="■"*3 +"□"*3 +"\n残り時間は30秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        if EXIT_FLG or USER_EXIT_FLG: raise A_error()
                        embed.set_footer(text="■"*4 +"□"*2 +"\n残り時間は20秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        if EXIT_FLG or USER_EXIT_FLG: raise A_error()
                        embed.set_footer(text="■"*5 +"□"*1 +"\n残り時間は10秒です")
                        await message.edit(embed=embed)
                        await asyncio.sleep(10)
                        await smsg.delete()
                        if EXIT_FLG or USER_EXIT_FLG: raise A_error()
                        embed.set_footer(text="■"*6 +"\n残り時間は0秒です")
                        await message.edit(embed=embed)
                        await mute_alives({user_id, to_id})
                        embed.description = f"「{user_name}」から「{to_name}」への質問が終わりました"
                        embed.set_footer(text="次の質問者へ移ります")
                        await message.edit(embed=embed)
                        await asyncio.sleep(3)
                        raise A_error()
                elif payload.emoji.name == "⏭️" and dm_message.content.startswith("質問をスキップする場合は"):
                    raise A_error()
        except A_error:
            if EXIT_FLG: return
            await asyncio.sleep(2)
        except asyncio.TimeoutError:
            if EXIT_FLG: return
            if USER_EXIT_FLG: continue
            await func.clean_dm({user_id})
            await func.send_rand_to(user_id)
            to_id, to_name, to_user = func.random_select_to(DAY, user_id)
            smsg = await user.send("`質問をスキップする場合は⏭️を押してください`")
            await smsg.add_reaction('⏭️')
            fmsg = await user.send(f"`まもなく「{to_name}」への質問が開始されます\n※まもなくミュートが外れます`")
            tmsg = await to_user.send(f"`まもなく「{user_name}」からの質問が開始されます\n※まもなくミュートが外れます`")
            embed.description = f"「{user_name}」から「{to_name}」に質問です"
            embed.set_footer(text="■"*3 +"□"*3 +"\n質問時間は30秒です")
            await message.edit(embed=embed)
            if EXIT_FLG: return
            if USER_EXIT_FLG: continue
            await asyncio.sleep(3)
            await unmute_alives({user_id, to_id})
            await asyncio.sleep(10)
            if EXIT_FLG: return
            if USER_EXIT_FLG: continue
            embed.set_footer(text="■"*4 +"□"*2 +"\n残り時間は20秒です")
            await message.edit(embed=embed)
            await asyncio.sleep(10)
            if EXIT_FLG: return
            if USER_EXIT_FLG: continue
            await func.clean_dm({user_id})
            embed.set_footer(text="■"*5 +"□"*1 +"\n残り時間は10秒です")
            await message.edit(embed=embed)
            await asyncio.sleep(10)
            try:
                await fmsg.delete()
                await tmsg.delete()
                await smsg.delete()
            except: pass
            if EXIT_FLG: return
            if USER_EXIT_FLG: continue
            embed.set_footer(text="■"*6 +"\n残り時間は0秒です")
            await message.edit(embed=embed)
            await mute_alives({user_id, to_id})
            embed.description = f"「{user_name}」から「{to_name}」への質問が終わりました"
            embed.set_footer(text="次の質問者へ移ります")
            await message.edit(embed=embed)
            await asyncio.sleep(3)
            if EXIT_FLG: return
            continue
    await message.clear_reactions()
    embed.title = "質疑応答が終了しました"
    embed.color = 0x8B4513
    embed.description = ""
    embed.set_footer(text="✅を押して進行してください")
    await message.edit(embed=embed)
    await message.add_reaction('✅')

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
    emsg = await user.send("`※まもなくミュートが外れます`")
    smsg = await user.send("`遺言をスキップする場合は⏭️を押してください`")
    await smsg.add_reaction('⏭️')
    await asyncio.sleep(1)
    await unmute_alives({exed_id})
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
    await mute_alives({exed_id})
    await smsg.delete()
    await func.clean_dm({exed_id})
    await asyncio.sleep(3)
    if EXIT_FLG: return
    embed.title = "処刑が執行されました"
    embed.color = 0x8B4513
    embed.description = ""
    embed.set_footer(text="✅を押して進行してください")
    await message.edit(embed=embed)
    await user.send("あなたは処刑されました")
    await gv.add_rip_role_and_prefix(exed_id, SERVER, RIP_RL_ID, RIP_CH_ID)
    await send_log(id=exed_id, flg=1)
    await message.add_reaction('✅')

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
        msg = await prexer.send("`あなたの弁明の時間が始まります\n※まもなくミュートが外れます`")
        await asyncio.sleep(1)
        smsg = await prexer.send("`弁明をスキップする場合は⏭️を押してください`")
        await smsg.add_reaction('⏭️')
        await asyncio.sleep(1)
        if EXIT_FLG:
            return
        if USER_EXIT_FLG:
            await persuasion_skip(prexer_name, message, msg)
            await asyncio.sleep(3)
            continue
        await unmute_alives({prexed_id})
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
        await mute_alives({prexed_id})
        embed.description = f"「{prexer_name}」による弁明が終わりました"
        embed.set_footer(text= "次に移行します\nしばらくお待ちください")
        await message.edit(embed=embed)
    embed.description = "全ての弁明が終わりました"
    embed.set_footer(text= "決選投票を始めます\n✅を押して進行してください")
    await message.edit(embed=embed)
    await message.add_reaction('✅')
    await func.clean_dm(prexed_ids)

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

#### SYSTEM ####
async def send_log(id=None, name=None, vtx=None, flg=0):
    global DAY
    channel = SERVER.get_channel(LOG_CH_ID)
    if vtx:
        await channel.send(f"```\n{vtx}\n```")
    elif flg == 0:
        log = "## === ゲーム開始 ===\n```\n"
        names_txt = func.get_status_txt()
        log += names_txt
        log += "\n```"
        await channel.send(log)
    elif flg == 1:
        if id:
            name = func.get_name_by_id(id)
            await channel.send(f"`「{name}」を処刑した`")
        else:
            await channel.send("`> 処刑しなかった`")
    elif flg == 2:
        if name:
            await channel.send(f"`「{name}」が殺された`")
        else:
            if DAY != 1:
                await channel.send("`> 誰も死ななかった`")
    elif flg == 3:
        await channel.send(f"`>> 村人の勝利`\n## === ゲーム終了 ===")
        result = func.get_result()
        await channel.send(f"```\n{result}\n```")
    elif flg == 4:
        await channel.send(f"`>> 人狼の勝利`\n## === ゲーム終了 ===")
        result = func.get_result()
        await channel.send(f"```\n{result}\n```")
    elif flg == 5:
        await channel.send(f"`{DAY}日目`")
        if DAY != 1:
            names_txt = func.get_status_txt()
            await channel.send(f"```\n{names_txt}\n```")
        DAY += 1

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
    DAY = 1

#### MAIN ####
@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
    if payload.channel_id == TXT_CH_ID and payload.message_id == MAIN_EMB_ID:
        message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
        embed = message.embeds[0]
        if payload.emoji.name == '✅':
            await message.remove_reaction(payload.emoji, payload.member)
            await reaction_check_ops(message, embed)
        elif payload.emoji.name == 'ℹ️' and embed.title == "人狼メンバー設定":
            await message.remove_reaction(payload.emoji, payload.member)
            await gv.info_field_set(message, embed, MAX_VOTE_REPEAT, GRD_FLG)
        elif payload.emoji.name == '✋' and embed.title == "人狼メンバー設定":
            await message.remove_reaction(payload.emoji, payload.member)
            user_mention = f"<@{payload.user_id}>"
            await gv.hand_up(user_mention, message, embed)
        elif payload.emoji.name == '🆗':
            await message.remove_reaction(payload.emoji, payload.member)
            await gv.ok_ops(message, embed, SERVER, VOICE_CH_ID)
        elif payload.emoji.name == '⏭️':
            await message.clear_reactions()
            await task_kill()
            await skip_ops(message, embed)
        elif payload.emoji.name == '🛠️':
            await message.clear_reactions()
            await gv.edit_member_set(message, embed)
        elif payload.emoji.name == '🗣️' and embed.title == "人狼メンバー設定":
            await message.remove_reaction(payload.emoji, payload.member)
            await gv.vc_members_set(message, embed, SERVER, VOICE_CH_ID)
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
            await gv.select_victim(message, payload, channel, RC_FLG, MAIN_CH, MAIN_EMB_ID)
        elif message.content.startswith("以下のユーザーを襲撃します"): # at wlfs_room
            await gv.select_vic_check(message, payload, channel, MAIN_CH, MAIN_EMB_ID)
    else:
        channel = await bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if isinstance(channel, discord.DMChannel):
            if payload.emoji.name == '🆗':
                await gv.night_check_ops(payload.user_id, message, MAIN_CH, MAIN_EMB_ID)
            elif payload.emoji.name == '⏭️':
                await user_skip_ops(payload.user_id, message, channel)
            elif payload.emoji.name in REACTION_EMOJIS:
                await gv.dm_select_target(message, payload, channel, RC_FLG, MAIN_CH, MAIN_EMB_ID, DAY)
            elif payload.emoji.name == '❌':
                for reaction in message.reactions:
                    if reaction.emoji == '❌':
                        if reaction.count == 2:
                            await message.delete()
                        break
            elif payload.emoji.name == '⭕':
                await gv.dm_select_check(message, channel, payload.user_id, MAIN_CH, MAIN_EMB_ID, DAY)

#### !CMMAND ####
@bot.command(name='jinro')
async def create_embed_with_reaction(ctx: commands.Context):
    global MAIN_EMB_ID
    await ctx.message.delete()
    if not MAIN_EMB_ID:
        embed = discord.Embed(title='人狼メンバー設定', color=0x660000, description='-'*23+'\n'+'-'*23)
        embed.set_footer(text="メンバーを設定して✅を押してください")
        message = await ctx.send(embed=embed)
        MAIN_EMB_ID = message.id
        await message.add_reaction('✋')
        await message.add_reaction('🗣️')
        await message.add_reaction('ℹ️')
        await message.add_reaction('✅')

@bot.command(name='jinro_new')
async def create_new_embed(ctx: commands.Context):
    global MAIN_EMB_ID
    await ctx.message.delete()
    embed = discord.Embed(title='人狼メンバー設定', color=0x660000, description='-'*23+'\n'+'-'*23)
    embed.set_footer(text="メンバーを設定して✅を押してください")
    message = await ctx.send(embed=embed)
    MAIN_EMB_ID = message.id
    await message.add_reaction('✋')
    await message.add_reaction('🗣️')
    await message.add_reaction('ℹ️')
    await message.add_reaction('✅')

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
                break
    if embed:
        await message.delete()
        mentions = re.findall(r'<@[0-9]{18,20}>', embed.description)
        if not mentions:
            new_embed = discord.Embed(title='人狼メンバー設定', color=0x660000, description='-'*23+'\n'+'-'*23)
        else:
            dsc = ("\n").join(mentions)
            new_embed = discord.Embed(title='人狼メンバー設定', color=0x660000, description='-'*23+'\n'+ dsc +'\n'+'-'*23)
        new_embed.set_footer(text="メンバーを設定して✅を押してください")
        new_message = await ctx.send(embed=new_embed)
        MAIN_EMB_ID = new_message.id
        await new_message.add_reaction('✋')
        await new_message.add_reaction('🗣️')
        await new_message.add_reaction('ℹ️')
        await new_message.add_reaction('✅')

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
                    await func.clean_dm({user_id})
            elif "に質問です" in embed.description:
                user_name = embed.description.split("」から「")[0].lstrip("「")
                user_id = func.get_id_by_name(user_name)
                if user_id:
                    await func.clean_dm({user_id})
                to_name = embed.description.split("」から「")[-1].rstrip("」に質問です")
                to_id = func.get_id_by_name(to_name)
                if to_id:
                    await func.clean_dm({to_id})
            embed.title = "質疑応答をスキップしました"
            embed.description = ""
            embed.set_footer(text="✅を押して進行してください")
            await message.edit(embed=embed)
            await mute_alives()
            await message.add_reaction('✅')
        elif embed.title.startswith("遺言の時間"):
            executed_name = embed.description.split("」が処刑される")[0].split("\n「")[-1]
            executed_id = func.get_id_by_name(executed_name)
            await mute_alives({executed_id})
            await func.clean_dm({executed_id})
            user = func.get_member(executed_id)
            await user.send("あなたは処刑されました")
            await gv.add_rip_role_and_prefix(executed_id, SERVER, RIP_RL_ID, RIP_CH_ID)
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
            await func.clean_dm(prexed_ids)
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
    async for message in channel.history(limit=200):
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
            await gv.add_rip_role_and_prefix(user_id, SERVER, RIP_RL_ID, RIP_CH_ID)

@bot.command(name='rmrip')
async def rm_rip_role_and_prefix(ctx: commands.Context):
    await ctx.message.delete()
    await gv.remove_all_rip_role(SERVER, RIP_RL_ID)

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

@bot.command(name='otpt')
async def output_data(ctx: commands.Context):
    await ctx.message.delete()
    func.output()

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