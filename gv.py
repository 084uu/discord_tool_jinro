import discord
import asyncio
import re
import func


REACTION_EMOJIS = ('1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟','⏺️','🔼','⏹️','0️⃣')

#### SYSTEM ####

async def add_wolf_room(channel):
    wolf_ids = func.get_alive_wolfs()
    if len(wolf_ids) >= 2:
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

async def remove_all_werewolf_room(SERVER, WLF_CH_ID):
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

async def vote_ops(user_id, target_name, MAIN_CH, MAIN_EMB_ID):
    target_id = func.get_id_by_name(target_name)
    func.update_vote(target_id, user_id)
    message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
    embed = message.embeds[0]
    if embed:
        alives_count = func.get_count_alives()
        vote_count = func.get_vote_count()
        prexe_ids = func.get_prexe()
        prexe_count = len(prexe_ids)
        left_count = alives_count - vote_count - prexe_count
        if left_count:
            embed.description = "**LOADING** "+"■"*vote_count + "□"*left_count
            await message.edit(embed=embed)
        else:
            embed.title = "投票が完了しました"
            embed.description = "**LOADING** "+"■"*vote_count
            embed.set_footer(text="✅を押して進行してください")
            await message.edit(embed=embed)
            await message.add_reaction('✅')

async def night_ops(user_id, channel, message_id):
    message = await channel.fetch_message(message_id)
    embed = message.embeds[0]
    if embed:
        alives_count = func.get_count_alives()
        check_count = func.update_check_count(user_id)
        if check_count == alives_count:
            new_embed = embed.copy()
            new_embed.set_footer(text="✅を押して進行してください")
            await message.edit(embed=new_embed)
            await message.add_reaction('✅')

async def send_werewolf_ops(channel):
    wolf_ids = func.get_alive_wolfs()
    if len(wolf_ids) == 1:
        user_id = wolf_ids.pop()
        await send_werewolf_bite(channel, user_id)
    elif len(wolf_ids) >= 2:
        await add_wolf_room(channel)
        await send_werewolf_bite(channel)

async def send_werewolf_bite(channel, user_id=None): # 襲撃する対象を選んでください
    names = func.get_alive_vil_names()
    list_message = "`襲撃する対象を選んでください`\n"
    for index, item in enumerate(names):
        list_message += f"{REACTION_EMOJIS[index]}: {item}\n"
    list_message += "`リアクションで選択してください`"
    if user_id:
        user = func.get_member(user_id)
        sent_message = await user.send(list_message)
    else:
        sent_message = await channel.send(list_message)
    for index in range(len(names)):
        await sent_message.add_reaction(REACTION_EMOJIS[index])

async def send_werewolf_messages(channel, WLF_CH_ID):
    wolf_ids = func.get_alive_wolfs()
    wlfs_text = None
    if len(wolf_ids) >= 2:
        await add_wolf_room(channel)
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
            sent_msg = await user.send("`準備ができたら🆗をおしてください`")
            await sent_msg.add_reaction("🆗")
            await asyncio.sleep(0.5)

async def check_killed_victim(SERVER, WLF_CH_ID, RIP_RL_ID, RIP_CH_ID):
    killed_id = func.update_kill()
    alive_wolf_ids = func.get_alive_wolfs()
    if killed_id:
        user = func.get_member(killed_id)
        await user.send("あなたは襲撃され殺されました")
        await add_rip_role_and_prefix(killed_id, SERVER, RIP_RL_ID, RIP_CH_ID)
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

async def add_rip_role_and_prefix(user_id, SERVER, RIP_RL_ID, RIP_CH_ID):
    member = await SERVER.fetch_member(int(user_id))
    role = SERVER.get_role(RIP_RL_ID)
    if member:
        await member.add_roles(role)
        await member.send(f"<#{RIP_CH_ID}>")
        display_name = f"💀{member.display_name}"
        try:
            await member.edit(nick=display_name)
        except:
            pass

async def member_setting_ops(message, embed, SERVER):
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
        existing_names = set()
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
                    existing_names.add(display_name)
                    dsc_lines[index] = f"<@{user_id}> -> {display_name}"
                func.set_member(user_id, member, display_name)
        embed.description = "\n".join(dsc_lines)
        embed.set_footer(text="表示名を確認して🆗を押してください")
        await message.edit(embed=embed)
        await message.add_reaction('🆗')

async def remove_death_prefix(SERVER, RIP_RL_ID):
    role = SERVER.get_role(RIP_RL_ID)
    for member in role.members:
        if member.display_name.startswith("💀"):
            new_display_name = member.display_name[1:]
            try:
                await member.edit(nick=new_display_name)
            except discord.Forbidden:
                continue
            except:
                pass

async def remove_all_rip_role(SERVER, RIP_RL_ID):
    role = SERVER.get_role(RIP_RL_ID)
    for member in role.members:
        await member.remove_roles(role)
        if member.display_name.startswith("💀"):
            new_display_name = member.display_name[1:]
            try:
                await member.edit(nick=new_display_name)
            except discord.Forbidden:
                continue
            except:
                pass

#### PROCESS ####

async def coming_vote(message, embed):
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

async def next_game(message, embed, SERVER, WLF_CH_ID, RIP_RL_ID):
    func.restart_data()
    names_txt = func.get_alives_txt()
    await remove_all_werewolf_room(SERVER, WLF_CH_ID)
    await remove_all_rip_role(SERVER, RIP_RL_ID)
    embed.title = "ゲームを開始します"
    embed.description = f"以下のメンバーで開始します\n`{names_txt}`"
    embed.color = 0x660000
    embed.set_footer(text='VCにメンバーが集まったら🆗を押してください')
    await message.edit(embed=embed)
    await message.add_reaction('🆗')
    await message.add_reaction('🛠️')

async def coming_fin_vote(message, embed):
    alives_count = func.get_count_alives()
    prexe_ids = func.get_prexe()
    vote_count = alives_count - len(prexe_ids)
    func.reset_vote(flg=1)
    embed.title = "決選投票を始めます"
    embed.description = "**LOADING** " + "□"*vote_count
    embed.set_footer(text="しばらくお待ちください")
    await message.edit(embed=embed)
    await func.vote_again_ops(prexe_ids)

async def info_field_set(message, embed, MAX_VOTE_REPEAT, GRD_FLG):
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

async def hand_up(user_mention, message, embed):
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
    embed.description = new_description.rstrip("\n")
    await message.edit(embed=embed)

async def vc_members_set(message, embed, SERVER, VOICE_CH_ID):
    voice_ch = SERVER.get_channel(VOICE_CH_ID)
    if voice_ch:
        member_ids = {member.id for member in voice_ch.members}
        if member_ids:
            new_description = embed.description
            dsc_lines = new_description.rsplit("\n", 1)
            for member_id in member_ids:
                user_mention = f"<@{member_id}>"
                if user_mention not in dsc_lines[0]:
                    dsc_lines[0] += f"\n{user_mention}"
            embed.description = "\n".join(dsc_lines)
            await message.edit(embed=embed)

async def ok_ops(message, embed, SERVER, VOICE_CH_ID):
    if embed.title == "人狼メンバー設定":
        await message.clear_reactions()
        names_txt = func.get_alives_txt()
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

async def edit_member_set(message, embed):
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

async def select_victim(message, payload, channel, RC_FLG, MAIN_CH, MAIN_EMB_ID):
    wolf_count = len(func.get_alive_wolfs())
    messages = message.content.split("\n")
    for i in range(len(REACTION_EMOJIS)):
        if payload.emoji.name == REACTION_EMOJIS[i]:
            break
    count = 0
    for reaction in message.reactions:
        if str(reaction.emoji) == REACTION_EMOJIS[i]:
            count = reaction.count
            break
    if count == wolf_count + 1: # wlfs + bot
        selected_line = messages[i+1]
        target_name = selected_line.split(": ")[-1]
        if RC_FLG == 1:
            sent_message = await channel.send(f"`以下のユーザーを襲撃します`\n{target_name}")
            await sent_message.add_reaction('⭕')
            await sent_message.add_reaction('❌')
        elif RC_FLG == 0:
            await message.delete()
            target_id = func.get_id_by_name(target_name)
            await channel.send(f"「{target_name}」を襲撃しました")
            func.update_status(target_id, 1)
            print("[襲撃]", ">>", target_name)
            target_message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
            target_embed = target_message.embeds[0]
            alives_count = func.get_count_alives()
            check_count = func.update_check_wolf()
            if check_count == alives_count:
                new_embed = target_embed.copy()
                new_embed.set_footer(text="✅を押して進行してください")
                await target_message.edit(embed=new_embed)
                await target_message.add_reaction('✅')

async def select_vic_check(message, payload, channel, MAIN_CH, MAIN_EMB_ID):
    if payload.emoji.name == '❌':
        await message.delete()
    elif payload.emoji.name == '⭕':
        target_name = message.content.split('\n')[1]
        kil_check = func.check_status(1)
        if kil_check == 0:
            async for msg in channel.history(limit=15):
                if msg.content.startswith("`"):
                    await msg.delete()
            target_id = func.get_id_by_name(target_name)
            await channel.send(f"「{target_name}」を襲撃しました")
            func.update_status(target_id, 1)
            print("[襲撃]", ">>", target_name)
            target_message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
            target_embed = target_message.embeds[0]
            alives_count = func.get_count_alives()
            check_count = func.update_check_wolf()
            if check_count == alives_count:
                new_embed = target_embed.copy()
                new_embed.set_footer(text="✅を押して進行してください")
                await target_message.edit(embed=new_embed)
                await target_message.add_reaction('✅')

async def night_check_ops(user_id, message, MAIN_CH, MAIN_EMB_ID):
    if message.content.startswith("`確認ができたら") or message.content.startswith("`準備ができたら"):
        await message.delete()
        target_message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
        embed = target_message.embeds[0]
        alives_count = func.get_count_alives()
        check_count = func.update_check_count(user_id)
        func.fin_night_output(user_id)
        if check_count == alives_count:
            embed.description = "**LOADING** "+"■"*check_count
            embed.set_footer(text="配役の確認が完了しました\n✅を押して進行してください")
            await target_message.edit(embed=embed)
            await target_message.add_reaction('✅')
        else:
            embed.description = "**LOADING** "+"■"*check_count + "□"*(alives_count - check_count)
            await target_message.edit(embed=embed)
    elif message.content.startswith("`あなたは深い眠り"):
        await message.delete()
        target_message = await MAIN_CH.fetch_message(MAIN_EMB_ID)
        embed = target_message.embeds[0]
        alives_count = func.get_count_alives()
        check_count = func.update_check_count(user_id)
        func.fin_night_output(user_id)
        if check_count == alives_count:
            embed.set_footer(text="✅を押して進行してください")
            await target_message.edit(embed=embed)
            await target_message.add_reaction('✅')

async def dm_select_target(message, payload, channel, RC_FLG, MAIN_CH, MAIN_EMB_ID, DAY):
    if message.content.startswith("`処刑対象に投票してください`"): # 以下のユーザーに投票します
        messages = message.content.split("\n")
        for i in range(len(REACTION_EMOJIS)):
            if payload.emoji.name == REACTION_EMOJIS[i]:
                break
        selected_line = messages[i+1]
        target_name = selected_line.split(": ")[-1]
        if RC_FLG == 1:
            sent_message = await channel.send(f"`以下のユーザーに投票します`\n{target_name}")
            await sent_message.add_reaction('⭕')
            await sent_message.add_reaction('❌')
        else:
            await message.delete()
            check_count = func.update_check_count(payload.user_id)
            if check_count != -1:
                await vote_ops(payload.user_id, target_name, MAIN_CH, MAIN_EMB_ID)
    elif message.content.startswith("`襲撃する対象を選んでください`"): # 以下のユーザーを襲撃します
        messages = message.content.split("\n")
        for i in range(len(REACTION_EMOJIS)):
            if payload.emoji.name == REACTION_EMOJIS[i]:
                break
        selected_line = messages[i+1]
        target_name = selected_line.split(": ")[-1]
        if RC_FLG == 1:
            sent_message = await channel.send(f"`以下のユーザーを襲撃します`\n{target_name}")
            await sent_message.add_reaction('⭕')
            await sent_message.add_reaction('❌')
        else:
            await message.delete()
            kil_check = func.check_status(1)
            if kil_check == 0:
                target_id = func.get_id_by_name(target_name)
                await channel.send(f"「{target_name}」を襲撃しました")
                func.update_status(target_id, 1)
                print("[襲撃]", ">>", target_name)
                func.fin_night_output(payload.user_id)
                await night_ops(payload.user_id, MAIN_CH, MAIN_EMB_ID)
    elif message.content.startswith("`占う対象を選んでください"): # 以下のユーザーを占います
        messages = message.content.split("\n")
        for i in range(len(REACTION_EMOJIS)):
            if payload.emoji.name == REACTION_EMOJIS[i]:
                break
        selected_line = messages[i+1]
        target_name = selected_line.split(": ")[-1]
        if RC_FLG == 1:
            sent_message = await channel.send(f"`以下のユーザーを占います`\n{target_name}")
            await sent_message.add_reaction('⭕')
            await sent_message.add_reaction('❌')
        else:
            await message.delete()
            ftn_check = func.check_status(2)
            if ftn_check == 0:
                target_id = func.get_id_by_name(target_name)
                await func.send_fortune_result(target_id, payload.user_id)
                func.fin_night_output(payload.user_id)
                await night_ops(payload.user_id, MAIN_CH, MAIN_EMB_ID)
    elif message.content.startswith("`保護する対象を選んでください"): # 以下のユーザーを守ります
        messages = message.content.split("\n")
        for i in range(len(REACTION_EMOJIS)):
            if payload.emoji.name == REACTION_EMOJIS[i]:
                break
        selected_line = messages[i+1]
        target_name = selected_line.split(": ")[-1]
        if RC_FLG == 1:
            sent_message = await channel.send(f"`以下のユーザーを守ります`\n{target_name}")
            await sent_message.add_reaction('⭕')
            await sent_message.add_reaction('❌')
        else:
            await message.delete()
            grd_check = func.check_status(3)
            if grd_check == 0:
                await channel.send(f"「{target_name}」を守りました")
                target_id = func.get_id_by_name(target_name)
                func.update_status(target_id, 3)
                print("[保護]", ">>", target_name)
                func.fin_night_output(payload.user_id)
                await night_ops(payload.user_id, MAIN_CH, MAIN_EMB_ID)
    elif message.content.startswith("`質問する相手を選んでください"): # 以下のユーザーに質問します
        messages = message.content.split("\n")
        for i in range(len(REACTION_EMOJIS)):
            if payload.emoji.name == REACTION_EMOJIS[i]:
                break
        selected_line = messages[i+1]
        target_name = selected_line.split(": ")[-1]
        if RC_FLG == 1:
            sent_message = await channel.send(f"`以下のユーザーに質問します`\n{target_name}")
            await sent_message.add_reaction('⭕')
            await sent_message.add_reaction('❌')
        else:
            await message.delete()
            target_id = func.get_id_by_name(target_name)
            func.update_qa(DAY, payload.user_id, target_id)

async def dm_select_check(message, channel, user_id, MAIN_CH, MAIN_EMB_ID, DAY):
    if message.content.startswith("`以下のユーザーに投票します"):
        target_name = message.content.split('\n')[1]
        check_count = func.update_check_count(user_id)
        if check_count != -1:
            async for msg in channel.history(limit=10):
                if msg.content.startswith("`"):
                    await msg.delete()
            await vote_ops(user_id, target_name, MAIN_CH, MAIN_EMB_ID)
    elif message.content.startswith("`以下のユーザーを襲撃します"):
        target_name = message.content.split('\n')[1]
        kil_check = func.check_status(1)
        if kil_check == 0:
            async for msg in channel.history(limit=10):
                if msg.content.startswith("`"):
                    await msg.delete()
            target_id = func.get_id_by_name(target_name)
            func.update_status(target_id, 1)
            await channel.send(f"「{target_name}」を襲撃しました")
            print("[襲撃]", ">>", target_name)
            func.fin_night_output(user_id)
            await night_ops(user_id, MAIN_CH, MAIN_EMB_ID)
    elif message.content.startswith("`以下のユーザーを占います"):
        target_name = message.content.split('\n')[1]
        ftn_check = func.check_status(2)
        if ftn_check == 0:
            async for msg in channel.history(limit=10):
                if msg.content.startswith("`"):
                    await msg.delete()
            target_id = func.get_id_by_name(target_name)
            await func.send_fortune_result(target_id, user_id)
            func.fin_night_output(user_id)
            await night_ops(user_id, MAIN_CH, MAIN_EMB_ID)
    elif message.content.startswith("`以下のユーザーを守ります"):
        target_name = message.content.split('\n')[1]
        grd_check = func.check_status(3)
        if grd_check == 0:
            async for msg in channel.history(limit=10):
                if msg.content.startswith("`"):
                    await msg.delete()
            await channel.send(f"「{target_name}」を守りました")
            target_id = func.get_id_by_name(target_name)
            func.update_status(target_id, 3)
            print("[保護]", ">>", target_name)
            func.fin_night_output(user_id)
            await night_ops(user_id, MAIN_CH, MAIN_EMB_ID)
    elif message.content.startswith("`以下のユーザーに質問します"):
        target_name = message.content.split('\n')[1]
        async for msg in channel.history(limit=10):
            if msg.content.startswith("`"):
                await msg.delete()
        target_id = func.get_id_by_name(target_name)
        func.update_qa(DAY, user_id, target_id)

