import asyncio
import random
import discord

REACTION_EMOJIS_A = ('1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟','⏺️','🔼','⏹️','0️⃣')

#### USER DATA ####
DATA = {
    "alives": set(),
    "executed": [],
    "kill": set(),
    "killed": set(),
    "grd": set(),
    "grded": set(),
    "ftnd": set(),
    "prexe": set(),
    "ftflg": 0,
    "ftall": 0
}

JOB = {
    "wolfs": set(),
    "fotune": set(),
    "gurder": set(),
    "sham": set(),
    "mad": set(),
    "citizen": set()
}

USR = {

}

ID = {

}

CHK = set()
QA = set()

VOTE = {

}

#### get ####
def check(user_id):
    if user_id in USR.keys():
        return True
    else:
        False

def get_alives():
    return DATA["alives"]

def get_members(user_ids):
    members = []
    for user_id in user_ids:
        members.append(USR[user_id]["member"])
    return members

def get_member(user_id):
    return USR[user_id]["member"]

def get_check_count():
    return sum(len(values) for values in CHK.values())

def get_vote_count():
    return sum(len(values) for values in VOTE.values())

def get_alive_wolfs():
    alives = DATA["alives"]
    wolfs = JOB["wolfs"].copy()
    return wolfs.intersection(alives)

def get_alive_vil_names():
    alives = DATA["alives"]
    wolfs = JOB["wolfs"]
    vils = alives - wolfs
    names = set()
    for alive_id in vils:
        names.add(USR[alive_id]["name"])
    return names

def get_id_by_name(target_name):
    return ID[target_name]

def get_name_by_id(user_id):
    return USR[user_id]["name"]

def get_names_by_ids(user_ids):
    names = set()
    for user_id in user_ids:
        names.add(USR[user_id]["name"])
    return names

def get_alive_members():
    members = []
    alive_ids = DATA["alives"]
    for user_id in alive_ids:
        members.append(USR[user_id]["member"])
    return members

def get_count_alives():
    return len(DATA["alives"])

def get_vote_max_ids():
    max_len = max(len(value) for value in VOTE.values())
    prexe_ids = {key for key, value in VOTE.items() if len(value) == max_len}
    if len(prexe_ids) >= 2:
        global DATA
        DATA["prexe"] = prexe_ids
    return prexe_ids

def mk_vote_dsc():
    dsc = "-"*23 + "\n"
    for key, values in VOTE.items():
        name = USR[key]["name"]
        vote_count = len(values)
        votes = ", ".join(x for x in values)
        dsc += f"{name} {vote_count}票 <- {votes}\n"
    dsc += "-"*23
    return dsc

def check_status(flg=0):
    checked = 0
    if flg == 1:
        if DATA["kill"]:
            checked = 1
    elif flg == 2:
        if DATA["ftflg"]:
            checked = 1
    elif flg == 3:
        if DATA["grd"]:
            checked = 1
    return checked

def check_game_status():
    alives = DATA["alives"]
    wlfs = JOB["wolfs"].copy()
    mads = JOB["mad"].copy()
    wlfs = wlfs.intersection(alives)
    if len(wlfs) == 0:
        return 2
    mads = mads.intersection(alives)
    vils = alives - wlfs - mads
    wlfs_count = len(wlfs) + len(mads)
    vils_count = len(vils)
    if wlfs_count >= vils_count:
        return 1
    else:
        return 0

def get_executed():
    return DATA["executed"][-1]

def get_other_alives_names(user_id):
    alive_ids = DATA["alives"]
    names = set()
    for alive_id in alive_ids:
        if alive_id == user_id:
            continue
        else:
            names.add(USR[alive_id]["name"])
    return names

def get_qa_to_id(day, user_id):
    return QA[day][user_id]

def get_prexe():
    return DATA["prexe"]

def get_names_txt():
    txt = ""
    for name in ID.keys():
        txt += name + "\n"
    txt.rstrip("\n")
    return txt

def get_alives_txt():
    alives = DATA["alives"]
    names = get_names_by_ids(alives)
    txt = "\n".join(x for x in names)
    return txt

def get_result():
    result = ""
    for key in USR.keys():
        name = USR[key]["name"]
        job = USR[key]["job"]
        result += f"{name} {job}\n"
    result = result.rstrip("\n")
    return result

def get_ids():
    return USR.keys()

#### clean ####
async def clean_will_dm(user_id):
    user = USR[user_id]["member"]
    dm_channel = user.dm_channel
    async for msg in dm_channel.history(limit=10):
        if msg.content.startswith("※まもなくミュートが") or msg.content.startswith("遺言をスキップ") or msg.content.startswith("あなたは処刑される事と"):
            await msg.delete()

async def clean_rand_to_dm(user_id):
    user = USR[user_id]["member"]
    dm_channel = user.dm_channel
    async for target_message in dm_channel.history(limit=10):
        if target_message.content.startswith("選択がなされなかったため"):
            await target_message.delete()
            break

async def clean_werewolf_dm():
    wolf_ids = get_alive_wolfs()
    members = get_members(wolf_ids)
    for user in members:
        dm_channel = user.dm_channel
        async for msg in dm_channel.history(limit=10):
            if msg.content.startswith("襲撃する対象を選んでください"):
                await msg.delete()
                break

async def clean_select_to_dm(user_id):
    user = USR[user_id]["member"]
    dm_channel = user.dm_channel
    async for msg in dm_channel.history(limit=10):
        if msg.content.startswith("質問する相手") or msg.content.startswith("以下のユーザーに質問します") or msg.content.startswith("まもなく"):
            await msg.delete()

async def clean_persuasion_dm(ids):
    for user_id in ids:
        user = USR[user_id]["member"]
        dm_channel = user.dm_channel
        async for msg in dm_channel.history(limit=10):
            if msg.content.startswith("あなたの弁明の") or msg.content.startswith("弁明をスキップ") or msg.content.startswith("処刑対象の候補に"):
                await msg.delete()

async def clean_skip_qa_dm(user_id):
    user = USR[user_id]["member"]
    dm_channel = user.dm_channel
    async for msg in dm_channel.history(limit=10):
        if msg.content.startswith("質問をスキップする場合は"):
            await msg.delete()
            break

#### edit ####
def update_check_count(user_id):
    global CHK
    if user_id in CHK:
        return -1
    else:
        CHK.add(user_id)
        return len(CHK)

def update_qa(day, user_id, questioned_id=None):
    global QA
    if QA[day]:
        QA[day][user_id] = questioned_id
    else:
        QA[day] = {}
        QA[day][user_id] = questioned_id

def update_status(user_id, flg=0):
    global DATA
    if flg == 1:
        DATA["kill"]= {user_id}
    elif flg == 2:
        DATA["ftflg"] = 1
        DATA["ftnd"].add(user_id)
    elif flg == 3:
        DATA["grd"] = {user_id}
    elif flg == 5:
        DATA["executed"].append(user_id)
        DATA["alives"].remove(user_id)

def update_vote(target_id, user_id):
    global VOTE
    user_name = USR[user_id]["name"]
    if target_id in VOTE.keys():
        VOTE[target_id].add(user_name)
    else:
        VOTE[target_id] = {user_name}

def update_check_wolf():
    global CHK
    wlf_ids = get_alive_wolfs()
    CHK.update(wlf_ids)
    return len(CHK)

def update_kill():
    global DATA
    kill_id = DATA["kill"].copy()
    if not kill_id:
        return 0
    grd_id = DATA["grd"]
    if kill_id == grd_id:
        return None
    else:
        DATA["killed"].update(kill_id)
        DATA["alives"] = DATA["alives"] - kill_id
        kill_id = DATA["kill"].pop()
        return kill_id

def reset_flg_status():
    global DATA, CHK
    CHK = set()
    grded_id = DATA["grd"].copy()
    DATA["grd"] = set()
    DATA["grded"] = grded_id
    DATA["ftflg"] = 0

def reset_vote():
    global DATA, CHK, VOTE
    DATA["prexe"] = set()
    CHK = set()
    VOTE = {}

def reset_qa():
    global QA
    QA = set()

def random_select_to(day, user_id):
    global QA
    alive_ids = DATA["alives"].copy()
    alive_ids.remove(user_id)
    ran_to_id = random.choice(tuple(alive_ids))
    QA[day][user_id] = ran_to_id
    to_name = USR[ran_to_id]["name"]
    to_user = USR[ran_to_id]["member"]
    return ran_to_id, to_name, to_user

def reset_data():
    global DATA, ID, USR
    DATA = {"alives": set(),"executed": [],"kill": set(),"killed": set(),"grd": set(),"grded": set(),"ftnd": set(),"prexe": set(),"ftflg": 0,"ftall": 0}
    ID = {}
    USR = {}

def set_member(user_id, member, name):
    global DATA, ID, USR
    DATA["alives"].add(user_id)
    ID[name] = user_id
    USR[user_id] = {}
    USR[user_id]["name"] = name
    USR[user_id]["member"] = member
    USR[user_id]["job"] = ""

def restart_data():
    global DATA, USR
    DATA = {"alives": set(),"executed": [],"kill": set(),"killed": set(),"grd": set(),"grded": set(),"ftnd": set(),"prexe": set(),"ftflg": 0,"ftall": 0}
    for key in USR.keys():
        USR[key]["job"] = ""
        DATA["alives"].add(key)

def ini_settings():
    global DATA, JOB, USR, CHK, QA, VOTE
    JOB = {"wolfs": set(),"fortune": set(),"gurder": set(),"sham": set(),"mad": set(),"citizen": set()}
    CHK = set()
    QA = set()
    VOTE = {}
    name_count = len(DATA["alives"])
    if 9 <= name_count <= 11:
        roles = ['人狼', '人狼', '狂人', '騎士', '占い師', '霊媒師']
    elif 12 <= name_count <= 14:
        roles = ['人狼', '人狼', '人狼', '狂人', '騎士', '占い師', '霊媒師']
    elif name_count == 15:
        roles = ['人狼', '人狼', '人狼', '狂人', '狂人', '騎士', '占い師', '霊媒師']
    elif name_count == 8:
        roles = ['市民', '狂人', '騎士', '占い師', '霊媒師']
        random.shuffle(roles)
        roles.pop()
        roles += ['人狼']*2
    elif name_count == 7:
        roles = ['市民', '騎士', '占い師', '霊媒師']
        random.shuffle(roles)
        roles.pop()
        roles += ['人狼']*2
    elif 4 <= name_count <= 6:
        roles = ['市民', '狂人', '騎士', '占い師']
        random.shuffle(roles)
        roles.pop()
        roles += ['人狼']
    else:
        print("assign error")
        return
    num_citizens = name_count - len(roles)
    roles += ['市民'] * num_citizens
    random.shuffle(roles)
    for index, key in enumerate(USR.keys()):
        USR[key]["job"] = roles[index]
        if roles[index] == '人狼':
            JOB["wolfs"].add(key)
        elif roles[index] == '市民':
            JOB["citizen"].add(key)
        elif roles[index] == '狂人':
            JOB["mad"].add(key)
        elif roles[index] == '占い師':
            JOB["fortune"].add(key)
            DATA["ftnd"].add(key)
        elif roles[index] == '霊媒師':
            JOB["sham"].add(key)
        elif roles[index] == '騎士':
            JOB["gurder"].add(key)

#### DM ####
async def send_select_to(user_id): # 質問する相手を選んでください
    names = get_other_alives_names(user_id)
    user = USR[user_id]["member"]
    list_message = "質問する相手を選んでください\n"
    for index, item in enumerate(names):
        list_message += f"{REACTION_EMOJIS_A[index]}: {item}\n"
    list_message += "リアクションで選択してください"
    sent_message = await user.send(list_message)
    for index in range(len(names)):
        await sent_message.add_reaction(REACTION_EMOJIS_A[index])

async def send_select_executed(user_id): # 処刑対象に投票してください
    names = get_other_alives_names(user_id)
    user = USR[user_id]["member"]
    list_message = "処刑対象に投票してください\n"
    for index, item in enumerate(names):
        list_message += f"{REACTION_EMOJIS_A[index]}: {item}\n"
    list_message += "リアクションで選択してください"
    sent_message = await user.send(list_message)
    for index in range(len(names)):
        await sent_message.add_reaction(REACTION_EMOJIS_A[index])

async def vote_again_ops():
    alives_ids = DATA["alives"]
    prexe_ids = DATA["prexe"]
    prexe_names = get_names_by_ids(prexe_ids)
    vote_ids = alives_ids - prexe_ids
    for user_id in vote_ids:
        user = get_member(user_id)
        list_message = "処刑対象に投票してください\n"
        for index, item in enumerate(prexe_names):
            list_message += f"{REACTION_EMOJIS_A[index]}: {item}\n"
        list_message += "リアクションで選択してください"
        sent_message = await user.send(list_message)
        for index in range(len(prexe_names)):
            await sent_message.add_reaction(REACTION_EMOJIS_A[index])
        await asyncio.sleep(0.3)

async def send_shaman_ops(naflg=0):
    global CHK
    user_id = next(iter(JOB["sham"]), None)
    alive_ids = DATA["alives"]
    if user_id in alive_ids:
        result = 0
        exed_id = DATA["executed"][-1]
        exed_name = USR[exed_id]["name"]
        if exed_id in JOB["wolfs"]:
            result = 1
        user = DATA[user_id]["USER"]
        if result == 1:
            await user.send(f"処刑された「{exed_name}」は「黒」でした")
        else:
            await user.send(f"処刑された「{exed_name}」は「白」でした")
        if naflg == 0:
            sent_message = await user.send("あなたは深い眠りにつきます")
            await sent_message.add_reaction('🆗')
        elif naflg == 1:
            CHK.add(user_id)

async def send_fortune_ops(naflg=0): # 占う対象を選んでください
    global DATA, CHK
    user_id = next(iter(JOB["fortune"]), None)
    alive_ids = DATA["alives"]
    if user_id in alive_ids:
        ftnd_ids = DATA["ftnd"]
        fortune_ids = alive_ids - ftnd_ids
        user = USR[user_id]["member"]
        if fortune_ids:
            names = set()
            for fortune_id in fortune_ids:
                names.add(USR[fortune_id]["name"])
            list_message = "占う対象を選んでください\n"
            for index, item in enumerate(names):
                list_message += f"{REACTION_EMOJIS_A[index]}: {item}\n"
            list_message += "リアクションで選択してください"
            sent_message = await user.send(list_message)
            for index in range(len(names)):
                await sent_message.add_reaction(REACTION_EMOJIS_A[index])
        else:
            flg = DATA["ftall"]
            if flg == 0:
                await user.send("もう占える対象がいません")
                DATA["ftall"] = 1
            if naflg == 0:
                sent_message = await user.send("あなたは深い眠りにつきます")
                await sent_message.add_reaction('🆗')
            elif naflg == 1:
                CHK.add(user_id)

async def send_rand_to(user_id):
    user = USR[user_id]["member"]
    dm_channel = user.dm_channel
    async for target_message in dm_channel.history(limit=10):
        if target_message.content.startswith("質問する相手を選んでください") or target_message.content.startswith("以下のユーザーに質問します"):
            await target_message.delete()
    await user.send("選択がなされなかったため対象がランダムに選択されます")

async def send_others_ops(naflg=0):
    global CHK
    user_ids = JOB["citizen"].copy()
    mad_ids = JOB["mad"].copy()
    user_ids.update(mad_ids)
    alive_ids = DATA["alives"]
    alive_citis = user_ids.intersection(alive_ids)
    if naflg == 0:
        for user_id in alive_citis:
            user = get_member(user_id)
            sent_message = await user.send("あなたは深い眠りにつきます")
            await sent_message.add_reaction('🆗')
    elif naflg == 1:
        CHK.update(alive_citis)

async def send_fortune_result(target_id, user_id): # 占いの結果
    global DATA
    if DATA["ftflg"] == 0:
        DATA["ftflg"] = 1
        DATA["ftnd"].add(target_id)
        result = 0
        if target_id in JOB["wolfs"]:
            result = 1
        ftnd_name = USR[target_id]["name"]
        user = USR[user_id]["member"]
        if result == 1:
            await user.send(f"占いの結果、「{ftnd_name}」は「黒」でした")
        else:
            await user.send(f"占いの結果、「{ftnd_name}」は「白」でした")

async def send_guard_ops(grdflg): # 保護する対象を選んでください
    global DATA
    user_id = JOB["gurder"]
    if len(user_id) == 1:
        alive_ids = DATA["alives"]
        if user_id <= alive_ids:
            grd_ids = alive_ids - user_id
            if grdflg == 1:
                grded_id = DATA["grded"]
                if grded_id:
                    grd_ids = grd_ids - grded_id
            DATA["grded"] = set()
            names = set()
            for grd_id in grd_ids:
                names.add(USR[grd_id]["name"])
            user_id = next(iter(user_id), None)
            user = get_member(user_id)
            list_message = "保護する対象を選んでください\n"
            for index, item in enumerate(names):
                list_message += f"{REACTION_EMOJIS_A[index]}: {item}\n"
            list_message += "リアクションで選択してください"
            sent_message = await user.send(list_message)
            for index in range(len(names)):
                await sent_message.add_reaction(REACTION_EMOJIS_A[index])

async def send_guard_result():
    user_id = next(iter(JOB["gurder"]), None)
    user = get_member(user_id)
    await user.send("あなたの功績により村人が1人救われました")

async def send_fortune_messages():
    user_id = next(iter(JOB["fortune"]), None)
    if user_id:
        user = get_member(user_id)
        message = "あなたは占い師です"
        file_name = "image/fortune.jpg"
        file = discord.File(file_name, filename=file_name)
        await user.send(message, file=file)
        selected_name = select_random_white()
        await user.send(f"神のお告げにより「{selected_name}」が「白」であると分かりました")
        sent_message = await user.send("確認ができたら🆗をおしてください")
        await sent_message.add_reaction("🆗")
        await asyncio.sleep(0.5)

async def send_guardian_messages():
    user_id = next(iter(JOB["gurder"]), None)
    if user_id:
        user = get_member(user_id)
        message = "あなたは騎士です"
        file_name = "image/guardian.jpg"
        file = discord.File(file_name, filename=file_name)
        await user.send(message, file=file)
        sent_message = await user.send("確認ができたら🆗をおしてください")
        await sent_message.add_reaction("🆗")
        await asyncio.sleep(0.5)

async def send_shaman_messages():
    user_id = next(iter(JOB["sham"]), None)
    if user_id:
        user = get_member(user_id)
        message = "あなたは霊媒師です"
        file_name = "image/shaman.jpg"
        file = discord.File(file_name, filename=file_name)
        await user.send(message, file=file)
        sent_message = await user.send("確認ができたら🆗をおしてください")
        await sent_message.add_reaction("🆗")
        await asyncio.sleep(0.5)

async def send_mad_messages():
    user_ids = JOB["mad"]
    if user_ids:
        for user_id in user_ids:
            user = get_member(user_id)
            message = "あなたは狂人です"
            file_name = "image/mad.jpg"
            file = discord.File(file_name, filename=file_name)
            await user.send(message, file=file)
            sent_message = await user.send("確認ができたら🆗をおしてください")
            await sent_message.add_reaction("🆗")
            await asyncio.sleep(0.5)

async def send_citizen_messages():
    user_ids = JOB["citizen"]
    if user_ids:
        for user_id in user_ids:
            user = get_member(user_id)
            message = "あなたは市民です"
            file_name = "image/citizen.jpg"
            file = discord.File(file_name, filename=file_name)
            await user.send(message, file=file)
            sent_message = await user.send("確認ができたら🆗をおしてください")
            await sent_message.add_reaction("🆗")
            await asyncio.sleep(0.5)

def select_random_white():
    global DATA
    user_id = JOB["fortune"]
    alive_ids = DATA["alives"]
    wolf_ids = JOB["wolfs"]
    ftnd_ids = alive_ids - wolf_ids - user_id
    rand_wh_id = random.choice(tuple(ftnd_ids))
    DATA["ftnd"].add(rand_wh_id)
    return USR[rand_wh_id]["name"]

def mk_info(num):
    if 9 <= num <= 11:
        txt = "□ 配役\n人狼2 狂人1 占い師1 霊媒師1 騎士1 " + f"\n市民{num-6}"
    elif 12 <= num <= 14:
        txt = "□ 配役\n人狼3 狂人1 占い師1 霊媒師1 騎士1 " + f"\n市民{num-7}"
    elif num == 15:
        txt = "□ 配役\n人狼3 狂人2 占い師1 霊媒師1 騎士1 \n市民7"
    elif num == 8:
        txt = "□ 配役\n人狼2 狂人1* 占い師1* 霊媒師1* 騎士1* \n市民2~3 ※*欠けあり"
    elif num == 7:
        txt = "□ 配役\n人狼2 占い師1* 霊媒師1* 騎士1* \n市民2~3 ※*欠けあり"
    elif 4 <= num <= 6:
        txt = "□ 配役\n人狼1 狂人1* 占い師1* 騎士1* "+ f"\n市民{num-4}~{num-3} ※*欠けあり"
    else:
        txt = "□ 配役\n（4~15人まで設定可）"
    return txt


