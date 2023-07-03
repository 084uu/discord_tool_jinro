# hallo world

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await bot.fetch_user(payload.user_id)
    if isinstance(channel, discord.TextChannel):
        if message.embeds[0]:
            embed = message.embeds[0]
            if payload.emoji.name == '✅' and embed.title.startswith("投票先が決定しました"):
                executed_ids = check_vote_max()
                if len(executed_ids) >= 2:
                    vote_dsc = get_vote_from_ids(target_ids)
                    embed.title = "決戦投票へ移ります"
                    embed.description = f"投票結果\n{vote_dsc}\n \n弁明の時間に移ります"
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
                else:
                    executed_id = executed_ids[0]
                    update_status(executed_id)
                    exer = await bot.fetch_user(executed_id)
                    await exer.send("あなたは処刑される事となりました\n遺言を残してください")
                    exer_name = get_name_by_id(executed_id)
                    embed.title = "処刑対象が決定しました"
                    embed.description = f"{exer_name}が処刑されることになりました\n遺言の時間に移ります"
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
            elif payload.emoji.name == '✅' and embed.title.startswith("決戦投票へ移ります"):
            elif payload.emoji.name == '✅' and embed.title.startswith("処刑対象が決定しました"):
                embed.description = f"{exer_name}が処刑されることになりました\n遺言の時間に移ります"
                embed.set_footer(text="遺言時間は1分です\nまもなく始まります")
                await message.edit(embed=embed)
                await asyncio.sleep(2)
                await will_task()
                
    
    elif isinstance(channel, discord.DMChannel):

        
        

async def will_operates()
    executed_id = get_exe_id_sham()


