# hallo world

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await bot.fetch_user(payload.user_id)
    if isinstance(channel, discord.TextChannel):
        guild = await bot.fetch_guild(GUILD_ID)
        member = guild.get_member(payload.user_id)
        if message.embeds[0]:
			embed = message.embeds[0]
            if payload.emoji.name == '✅' and embed.title.startswith("投票先が決定しました"):
                await message.remove_reaction(payload.emoji, member)
                pre_executed_ids = check_vote_max()
				vote_dsc = get_vote_from_ids()
                if len(pre_executed_ids) >= 2:
					for pre_executed_id in pre_executed_ids:
						pre_exer = await bot.fetch_user(pre_executed_id)
						await pre_exer.send("処刑対象の候補になりました\n弁明の準備をしてください")
                    embed.title = "決戦投票へ移ります"
                    embed.description = f"投票結果\n{vote_dsc}\n \n弁明の時間に移ります"
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
                else:
                    executed_id = pre_executed_ids[0]
                    update_status(executed_id)
                    exer = await bot.fetch_user(executed_id)
                    await exer.send("あなたは処刑される事となりました\n遺言を残してください")
                    exer_name = get_name_by_id(executed_id)
                    embed.title = "処刑対象が決定しました"
                    embed.description = f"投票結果\n{vote_dsc}\n \n{exer_name}が処刑されることになりました\n遺言の時間に移ります"
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
            elif payload.emoji.name == '✅' and embed.title.startswith("決戦投票へ移ります"):
                await message.remove_reaction(payload.emoji, member)
				await persuasion_tasks(message)
			elif payload.emoji.name == '✅' and embed.title.startswith("処刑対象が決定しました"):
                await message.remove_reaction(payload.emoji, member)
                await will_tasks(message)
            elif payload.emoji.name == '✅' and embed.title.startswith("遺言"):
				await message.remove_reaction(payload.emoji, member)
				embed.title = "おそろしい夜がやってきました"
				embed.description = "夜の行動を選択中です"
                embed.set_footer(text="しばらくお待ちください")
                await message.edit(embed=embed)
			elif payload.emoji.name == '✅' and embed.title.startswith("弁明"):
	            await message.remove_reaction(payload.emoji, member)
				embed.title = "決戦投票を始めます"
				embed.description = "LOADING" + "□"*count
                embed.set_footer(text="しばらくお待ちください")
				await message.edit(embed=embed)

			
			...
    
    elif isinstance(channel, discord.DMChannel):
		global exit_flg
		if payload.emoji.name == '➡️' and message.content.startswith("弁明をスキップする場合は"):
			await message.delete()
			exit_flg = True
			await user.send("あなたの弁明がスキップされます")
        ...

async def persuasion_operates(message):
	global exit_flg
	embed = message.embeds[0]
	embed.title = "弁明の時間です"
	embed.description = ""
	embed.set_footer(text="しばらくお待ちください")
	await message.edit(embed=embed)
	pre_executed_ids = check_vote_max()
	random.shuffle(pre_executed_ids)
	for pre_executed_id in pre_executed_ids:
		exit_flg = Flase
		persuader = await bot.fetch_user(pre_executed_id)
		persuader_name = get_name_by_id(pre_executed_id)
		msg = await persuader.send("あなたの弁明の時間が始まります\nまもなくミュートが外れます")
		await asyncio.sleep(1)
		smsg = await persuader.send("弁明をスキップする場合は➡️を押してください")
		await smsg.add_reaction('➡️')
		await asyncio.sleep(1)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		await unmute_select(pre_executed_id)
		embed.description = f"{persuader_name}による弁明です"
		embed.set_footer(text= "□"*6+"残り時間は1分です")
		await message.edit(embed=embed)
		await asyncio.sleep(5)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		await asyncio.sleep(5)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		embed.set_footer(text= "■"+"□"*5+"残り時間は50秒です")
		await message.edit(embed=embed)
		await asyncio.sleep(5)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		await asyncio.sleep(5)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		embed.set_footer(text= "■"*2+"□"*4+"残り時間は40秒です")
		await message.edit(embed=embed)
		await asyncio.sleep(5)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		await asyncio.sleep(5)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		await meg.delete()
		embed.set_footer(text= "■"*3+"□"*3+"残り時間は30秒です")
		await message.edit(embed=embed)
		await asyncio.sleep(5)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		await asyncio.sleep(5)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		embed.set_footer(text= "■"*4+"□"*2+"残り時間は20秒です")
		await message.edit(embed=embed)
		await asyncio.sleep(5)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		await asyncio.sleep(5)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		embed.set_footer(text= "■"*5+"□"*1+"残り時間は10秒です")
		await message.edit(embed=embed)
		await asyncio.sleep(5)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		await asyncio.sleep(5)
		if exit_flg:
			await persuasion_skip(pre_executed_id, persuader_name, message, meg)
			break
		embed.set_footer(text= "■"*6+"残り時間は0秒です")
		await message.edit(embed=embed)
		await smeg.delete()
		await mute_select(pre_executed_id)
		embed.description = f"{persuader_name}による弁明が終わりました"
		embed.set_footer(text= "次に移行します\nしばらくお待ちください")
		await message.edit(embed=embed)
	embed.description = "全ての弁明が終わりました"
	embed.set_footer(text= "決戦投票を始めます\n✅を押して進行してください")
	await message.edit(embed=embed)
	await message.add_reaction('✅')
	await clean_persuasion_dm(pre_executed_ids)
	
	### if skiped
	await clean_persuasion_dm()
	...

async def persuasion_skip(pre_executed_id, persuader_name, message, meg):
	await mute_select(pre_executed_id)
	if msg:
		await meg.delete()
	embed.description = f"{persuader_name}による弁明がスキップされました"
	embed.set_footer(text= "次に移行します\nしばらくお待ちください")
	await message.edit(embed=embed)

async def clean_persuasion_dm(ids=None):
	if ids:
		pre_executed_ids = ids
	else:
		pre_executed_ids = check_vote_max()
	for pre_executed_id in pre_executed_ids:
		user = await bot.fetch_user(pre_executed_id)
	    if user and user.dm_channel:
	        dm_channel = user.dm_channel
	        dm_messages = await dm_channel.history(limit=10).flatten()
	        for message in dm_messages:
	            if message.content.startswith("あなたの弁明") or message.content.startswith("弁明をスキップ") or message.content.startswith("処刑対象の候補に"):
	                await message.delete()

async def will_operates():
	will_name = embed.description.split("が処刑され")[0]
	embed.title = "遺言の時間です"
	embed.description = f"{will_name}の遺言です"
	embed.set_footer(text="遺言時間は1分です\nまもなく始まります")
	await message.edit(embed=embed)

	...
	
	executed_id = get_exe_id_sham()

    ...

await asyncio.sleep(2)
