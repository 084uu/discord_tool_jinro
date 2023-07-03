# hallo world

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await bot.fetch_user(payload.user_id)
    if isinstance(channel, discord.TextChannel):
        if message.embeds[0]:
            embed = message.embeds[0]
            if embed.title.startswith("あいうえお"):
                target_ids = check_vote_max()
                if len(target_ids) >= 2:
                    vote_dsc = get_vote_from_ids(target_ids)
                    embed.title = "決戦投票へ移ります"
                    embed.description = f"投票結果\n{vote_dsc}\n"
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
                else:
                    embed.title = "処刑対象が決定しました"
                    embed.description = f"{user_name}が処刑されることになりました\n遺言の時間に移ります"
                    embed.set_footer(text="✅を押して進行してください")
                    await message.edit(embed=embed)
                    await message.add_reaction('✅')
    elif isinstance(channel, discord.DMChannel):


