import datetime
import math
import os
import sys
import time

import jdatetime
import telethon
import telethon.sync

import utility as utl

for index, arg in enumerate(sys.argv):
    if index == 1:
        mbots_uniq_id = arg
    elif index == 2:
        from_id = int(arg)
    elif index == 3:
        table_id = int(arg)
    elif index == 4:
        status = arg
    elif index == 5:
        message_id = int(arg)

directory = os.path.dirname(os.path.abspath(__file__))
timestamp = int(time.time())

info_msg = utl.bot.edit_message_text(
    chat_id=from_id, text="در حال بررسی ...", message_id=message_id
)

cs = utl.Database()
cs = cs.data()

cs.execute(f"SELECT * FROM {utl.egroup} WHERE id={table_id}")
row_egroup = cs.fetchone()
cs.execute(f"SELECT * FROM {utl.mbots} WHERE uniq_id='{mbots_uniq_id}'")
row_mbots = cs.fetchone()

utl.get_params_pids_by_full_script_name(
    param1=row_mbots["uniq_id"], is_kill_proccess=True
)

try:
    client = telethon.sync.TelegramClient(
        session=f"{directory}/sessions/{row_mbots['uniq_id']}",
        api_id=row_mbots["api_id"],
        api_hash=row_mbots["api_hash"],
    )
    client.connect()
    if not client.is_user_authorized():
        cs.execute(f"UPDATE {utl.mbots} SET status=0 WHERE id={row_mbots['id']}")
        info_msg.edit_text(
            text=f"⛔️ اکانت /status_{row_mbots['id']} از دسترسی خارج شد (<code>{row_mbots['phone']}</code>)",
            parse_mode="HTML",
        )
    else:
        try:
            if status == "users":
                info_msg.edit_text(text="در حال بررسی چت ...")
                link = row_egroup["link"]
                try:
                    if row_egroup["chat_id"] != "0":
                        link = int(row_egroup["chat_id"])
                    client(
                        telethon.functions.channels.GetParticipantRequest(
                            channel=link, participant="me"
                        )
                    )
                except:
                    try:
                        if "/joinchat/" in link:
                            client(
                                telethon.functions.messages.ImportChatInviteRequest(
                                    link.split("/joinchat/")[1]
                                )
                            )
                        else:
                            client(
                                telethon.functions.channels.JoinChannelRequest(
                                    channel=link
                                )
                            )
                    except telethon.errors.UserAlreadyParticipantError as e:
                        pass
                result = client(
                    telethon.functions.channels.GetFullChannelRequest(channel=link)
                )
                chat = result.full_chat.id
                chat_id = int(f"-100{chat}")
                participants_count = result.full_chat.participants_count
                online_count = result.full_chat.online_count
                cs.execute(
                    f"UPDATE {utl.egroup} SET chat_id='{chat_id}' WHERE id={row_egroup['id']}"
                )

                info_msg.edit_text(text="در حال آنالیز  ...")
                queryKey = [
                    "",
                    "a",
                    "b",
                    "c",
                    "d",
                    "e",
                    "f",
                    "g",
                    "h",
                    "i",
                    "j",
                    "k",
                    "l",
                    "m",
                    "n",
                    "o",
                    "p",
                    "q",
                    "r",
                    "s",
                    "t",
                    "u",
                    "v",
                    "w",
                    "x",
                    "y",
                    "z",
                ]
                participants_all_id = []
                participants_all_username = []
                participants_real = []
                participants_fake = []
                participants_has_phone = []
                participants_online = []
                participants_bots = []
                percent = timestamp_start = i = 0
                for key in queryKey:
                    offset = 0
                    while True:
                        participants = client(
                            telethon.functions.channels.GetParticipantsRequest(
                                chat,
                                telethon.types.ChannelParticipantsSearch(key),
                                offset,
                                200,
                                hash=0,
                            )
                        )
                        if participants.users:
                            for user in participants.users:
                                try:
                                    if (
                                        not user.id in participants_all_id
                                        and row_mbots["user_id"] != user.id
                                    ):
                                        participants_all_id.append(user.id)
                                        if user.username:
                                            username = f"@{user.username}"
                                            if user.bot:
                                                participants_bots.append(username)
                                            else:
                                                participants_all_username.append(
                                                    username
                                                )
                                                if (
                                                    isinstance(
                                                        user.status,
                                                        telethon.types.UserStatusRecently,
                                                    )
                                                    or isinstance(
                                                        user.status,
                                                        telethon.types.UserStatusOnline,
                                                    )
                                                    or (
                                                        isinstance(
                                                            user.status,
                                                            telethon.types.UserStatusOffline,
                                                        )
                                                        and (
                                                            timestamp
                                                            - user.status.was_online.timestamp()
                                                        )
                                                        < 259200
                                                    )
                                                ):
                                                    if (
                                                        not username
                                                        in participants_real
                                                    ):
                                                        participants_real.append(
                                                            username
                                                        )
                                                elif not username in participants_fake:
                                                    participants_fake.append(username)
                                                if isinstance(
                                                    user.status,
                                                    telethon.types.UserStatusOnline,
                                                ) or (
                                                    isinstance(
                                                        user.status,
                                                        telethon.types.UserStatusOffline,
                                                    )
                                                    and (
                                                        timestamp
                                                        - user.status.was_online.timestamp()
                                                    )
                                                    < 1800
                                                ):
                                                    if (
                                                        not username
                                                        in participants_online
                                                    ):
                                                        participants_online.append(
                                                            username
                                                        )
                                                if (
                                                    user.phone
                                                    and not user.phone
                                                    in participants_has_phone
                                                ):
                                                    participants_has_phone.append(
                                                        user.phone
                                                    )
                                except:
                                    pass
                            try:
                                offset += len(participants.users)
                                if (int(time.time()) - timestamp_start) > 4:
                                    cs.execute(
                                        f"SELECT * FROM {utl.egroup} WHERE id={row_egroup['id']}"
                                    )
                                    row_egroup = cs.fetchone()
                                    if row_egroup["status"] == 2:
                                        break
                                    timestamp_start = int(time.time())
                                    count = len(participants_all_id)
                                    percent = float(
                                        "{:.2f}".format(
                                            count / participants_count * 100
                                        )
                                    )
                                    if percent >= 100:
                                        break
                                    percent_key = math.ceil((i / 26) * 100)
                                    if percent_key > percent:
                                        percent = percent_key
                                    info_msg.edit_text(
                                        text="⏳ در حال آنالیز ...\n\n"
                                        + f"🔗 لینک: {link}\n"
                                        + f"♻️ در حال پیشرفت: {percent}%\n"
                                        + f"👥 کاربران: [{count:,}/{participants_count:,}]\n"
                                        + "➖➖➖➖➖➖\n"
                                        + f"📅 مدت زمان: {utl.convert_time((int(time.time()) - timestamp), 2)}\n"
                                        f"📅 زمان حال: {jdatetime.datetime.now().astimezone(datetime.timezone(datetime.timedelta(hours=3, minutes=30))).strftime('%H:%M:%S')}",
                                        disable_web_page_preview=True,
                                        reply_markup={
                                            "inline_keyboard": [
                                                [
                                                    {
                                                        "text": "توقف",
                                                        "callback_data": f"analyze;{row_egroup['id']}",
                                                    }
                                                ]
                                            ]
                                        },
                                    )
                            except:
                                pass
                        else:
                            break
                    cs.execute(
                        f"SELECT * FROM {utl.egroup} WHERE id={row_egroup['id']}"
                    )
                    row_egroup = cs.fetchone()
                    if row_egroup["status"] == 2:
                        break
                    elif percent >= 100:
                        break
                    i += 1

                try:
                    os.mkdir(f"{directory}/export/{row_egroup['id']}")
                except:
                    pass
                users_real = users_fake = users_has_phone = users_online = ""
                for value_ in participants_real:
                    users_real += f"{value_}\n"
                for value_ in participants_fake:
                    users_fake += f"{value_}\n"
                for value_ in participants_has_phone:
                    users_has_phone += f"{value_}\n"
                for value_ in participants_online:
                    users_online += f"{value_}\n"

                with open(
                    f"{directory}/export/{row_egroup['id']}/users_all.txt", "w"
                ) as file:
                    file.write(users_real + users_fake)
                with open(
                    f"{directory}/export/{row_egroup['id']}/users_real.txt", "w"
                ) as file:
                    file.write(users_real)
                with open(
                    f"{directory}/export/{row_egroup['id']}/users_fake.txt", "w"
                ) as file:
                    file.write(users_fake)
                with open(
                    f"{directory}/export/{row_egroup['id']}/users_has_phone.txt", "w"
                ) as file:
                    file.write(users_has_phone)
                with open(
                    f"{directory}/export/{row_egroup['id']}/users_online.txt", "w"
                ) as file:
                    file.write(users_online)
                users_all_id = len(participants_all_id)
                users_real_count = len(participants_real)
                users_fake_count = len(participants_fake)
                users_has_phone_count = len(participants_has_phone)
                users_online_count = len(participants_online)
                bots_count = len(participants_bots)

                cs.execute(
                    f"UPDATE {utl.egroup} SET status=2,users_real='{users_real_count}',users_fake='{users_fake_count}',users_has_phone='{users_has_phone_count}',users_online='{users_online_count}',participants_count='{participants_count}',participants_online_count='{online_count}',participants_bot_count='{bots_count}' WHERE id={row_egroup['id']}"
                )
                info_msg.reply_html(
                    text=f"🔻 آیدی گروه: <code>{chat_id}</code>\n"
                    f"🔻 لینک: {row_egroup['link']}\n"
                    f"🔻 کل کاربران: {participants_count:,}\n"
                    f"🔻 کاربران آنلاین: {online_count:,}\n"
                    f"🔻 ربات ها: {bots_count}\n"
                    "————————————————————\n"
                    "♻️ کاربران شناسایی شده (دارای یوزرنیم):\n"
                    f"🔻 همه کاربران: {(users_real_count + users_fake_count):,} (/ex_{row_egroup['id']}_a)\n"
                    f"🔻 کاربران واقعی: {users_real_count:,} (/ex_{row_egroup['id']}_u)\n"
                    f"🔻 کاربران فیک: {users_fake_count:,} (/ex_{row_egroup['id']}_f)\n"
                    f"🔻 کاربران با شماره: {users_has_phone_count:,} (/ex_{row_egroup['id']}_n)\n"
                    f"🔻 کاربران آنلاین: {users_online_count:,} (/ex_{row_egroup['id']}_o)\n\n"
                    f"⏰ مدت زمان: {utl.convert_time((int(time.time()) - timestamp), 2)}",
                    disable_web_page_preview=True,
                )
            elif status == "messages":
                info_msg.edit_text(text="در حال بررسی چت ...")
                link = row_egroup["link"]
                try:
                    if row_egroup["chat_id"] != "0":
                        link = int(row_egroup["chat_id"])
                    client(
                        telethon.functions.channels.GetParticipantRequest(
                            channel=link, participant="me"
                        )
                    )
                except:
                    try:
                        if "/joinchat/" in link:
                            client(
                                telethon.functions.messages.ImportChatInviteRequest(
                                    link.split("/joinchat/")[1]
                                )
                            )
                        else:
                            client(
                                telethon.functions.channels.JoinChannelRequest(
                                    channel=link
                                )
                            )
                    except telethon.errors.UserAlreadyParticipantError as e:
                        pass
                result = client(
                    telethon.functions.channels.GetFullChannelRequest(channel=link)
                )
                chat = result.full_chat.id
                chat_id = int(f"-100{chat}")
                participants_count = result.full_chat.participants_count
                online_count = result.full_chat.online_count
                cs.execute(
                    f"UPDATE {utl.egroup} SET chat_id='{chat_id}' WHERE id={row_egroup['id']}"
                )

                info_msg.edit_text(text="در حال آنالیز  ...")
                first_message_id = 0
                last_message_id = 0
                participants_all_id = []
                participants_all = []
                participants_bots = []
                timestamp_start = i = 0
                for message in client.iter_messages(chat_id):
                    last_message_id = message.id
                    if not first_message_id:
                        first_message_id = message.id
                    if isinstance(message, telethon.types.Message):
                        try:
                            if message.from_id is not None and isinstance(
                                message.from_id, telethon.types.PeerUser
                            ):
                                user_id = message.from_id.user_id
                                if (
                                    not user_id in participants_all_id
                                    and row_mbots["user_id"] != user_id
                                ):
                                    participants_all_id.append(user_id)
                                    result = client.get_entity(user_id)
                                    if result.bot:
                                        participants_bots.append(f"@{result.username}")
                                    elif result.username is not None:
                                        participants_all.append(f"@{result.username}")

                        except Exception as e:
                            print(e)
                    if (int(time.time()) - timestamp_start) > 5:
                        timestamp_start = int(time.time())
                        info_msg.edit_text(
                            text="⏳ در حال آنالیز ...\n\n"
                            f"🔗 لینک: {link}\n"
                            f"♻️ پیام های آنالیز شده: {(first_message_id-last_message_id):,}\n"
                            f"👥 کل کاربران: {len(participants_all_id):,}\n"
                            f"👥 کاربران دارای یوزرنیم: {len(participants_all):,}\n"
                            "➖➖➖➖➖➖\n"
                            + f"📅 مدت زمان: {utl.convert_time((int(time.time()) - timestamp), 2)}\n"
                            f"📅 زمان حال: {jdatetime.datetime.now().astimezone(datetime.timezone(datetime.timedelta(hours=3, minutes=30))).strftime('%H:%M:%S')}",
                            disable_web_page_preview=True,
                            reply_markup={
                                "inline_keyboard": [
                                    [
                                        {
                                            "text": "توقف",
                                            "callback_data": f"analyze;{row_egroup['id']}",
                                        }
                                    ]
                                ]
                            },
                        )
                        cs.execute(
                            f"SELECT * FROM {utl.egroup} WHERE id={row_egroup['id']}"
                        )
                        row_egroup = cs.fetchone()
                        if row_egroup["status"] == 2:
                            break

                try:
                    os.mkdir(f"{directory}/export/{row_egroup['id']}")
                except:
                    pass
                users_all = users_username = users_bots = ""
                for value_ in participants_all_id:
                    users_all += f"{value_}\n"
                for value_ in participants_all:
                    users_username += f"{value_}\n"
                for value_ in participants_bots:
                    users_bots += f"{value_}\n"

                with open(
                    f"{directory}/export/{row_egroup['id']}/users_all.txt", "w"
                ) as file:
                    file.write(users_all)
                with open(
                    f"{directory}/export/{row_egroup['id']}/users_username.txt", "w"
                ) as file:
                    file.write(users_username)
                with open(
                    f"{directory}/export/{row_egroup['id']}/users_bots.txt", "w"
                ) as file:
                    file.write(users_bots)
                row_egroup["chat_id"] = str(chat_id)
                row_egroup["participants_count"] = participants_count
                row_egroup["participants_online_count"] = online_count
                row_egroup["users_all"] = len(participants_all_id)
                row_egroup["users_real"] = len(participants_all)
                row_egroup["participants_bot_count"] = len(participants_bots)

                cs.execute(
                    f"UPDATE {utl.egroup} SET status=2,users_all={row_egroup['users_all']},users_real={row_egroup['users_real']},participants_count={row_egroup['participants_count']},participants_online_count={row_egroup['participants_online_count']},participants_bot_count={row_egroup['participants_bot_count']} WHERE id={row_egroup['id']}"
                )
                info_msg.reply_html(
                    text=f"🔻 آیدی گروه: <code>{row_egroup['chat_id']}</code>\n"
                    f"🔻 لینک: {row_egroup['link']}\n"
                    f"🔻 کل کاربران: {row_egroup['participants_count']:,}\n"
                    f"🔻 کاربران آنلاین: {row_egroup['participants_online_count']:,}\n"
                    "————————————————————\n"
                    "♻️ کاربران شناسایی شده:\n"
                    f"🔻 همه کاربران: {row_egroup['users_all']:,} (/ex_{row_egroup['id']}_a)\n"
                    f"🔻 کاربران دارای یوزرنیم: {row_egroup['users_real']:,} (/ex_{row_egroup['id']}_u)\n"
                    f"🔻 ربات ها: {row_egroup['participants_bot_count']:,} (/ex_{row_egroup['id']}_b)\n\n"
                    f"⏰ مدت زمان: {utl.convert_time((int(time.time()) - timestamp), 2)}",
                    disable_web_page_preview=True,
                )
            elif status == "order_link":
                cs.execute(f"SELECT * FROM {utl.orders} WHERE id={table_id}")
                row_orders = cs.fetchone()
                links = row_orders["origin"].split(",")  # جدا کردن لینک‌های مبدا

                for link in links:  # پردازش هر لینک مبدا به‌صورت جداگانه
                    link = link.strip()
                    try:
                        client(
                            telethon.functions.channels.GetParticipantRequest(
                                channel=link, participant="me"
                            )
                        )
                    except:
                        try:
                            if "/joinchat/" in link:
                                client(
                                    telethon.functions.messages.ImportChatInviteRequest(
                                        link.split("/joinchat/")[1]
                                    )
                                )
                            else:
                                client(
                                    telethon.functions.channels.JoinChannelRequest(
                                        channel=link
                                    )
                                )
                        except telethon.errors.UserAlreadyParticipantError:
                            pass
                    
                    result = client(
                        telethon.functions.channels.GetFullChannelRequest(channel=link)
                    )
                    chat_origin = result.full_chat.id
                    origin_id = int(f"-100{result.full_chat.id}")
                    cs.execute(
                        f"UPDATE {utl.orders} SET origin_id='{origin_id}' WHERE id={row_orders['id']}'"
                    )


                link = row_orders["destination"]
                try:
                    client(
                        telethon.functions.channels.GetParticipantRequest(
                            channel=link, participant="me"
                        )
                    )
                except:
                    try:
                        if "/joinchat/" in link:
                            client(
                                telethon.functions.messages.ImportChatInviteRequest(
                                    link.split("/joinchat/")[1]
                                )
                            )
                        else:
                            client(
                                telethon.functions.channels.JoinChannelRequest(
                                    channel=link
                                )
                            )
                    except telethon.errors.UserAlreadyParticipantError as e:
                        pass
                result = client(
                    telethon.functions.channels.GetFullChannelRequest(channel=link)
                )
                chat_destination = result.full_chat.id
                destination_id = int(f"-100{result.full_chat.id}")

                cs.execute(
                    f"UPDATE {utl.orders} SET destination_id='{destination_id}' WHERE id={row_orders['id']}"
                )
                cs.execute(f"SELECT * FROM {utl.orders} WHERE id={row_orders['id']}")
                row_orders = cs.fetchone()

                info_msg.edit_text(text="در حال آنالیز ...")

                queryKey = [
                    "",
                    "a",
                    "b",
                    "c",
                    "d",
                    "e",
                    "f",
                    "g",
                    "h",
                    "i",
                    "j",
                    "k",
                    "l",
                    "m",
                    "n",
                    "o",
                    "p",
                    "q",
                    "r",
                    "s",
                    "t",
                    "u",
                    "v",
                    "w",
                    "x",
                    "y",
                    "z",
                ]
                participants_all_id = []
                participants_all = []
                percent = timestamp_start = i = 0
                for key in queryKey:
                    offset = 0
                    while True:
                        participants = client(
                            telethon.functions.channels.GetParticipantsRequest(
                                chat_origin,
                                telethon.types.ChannelParticipantsSearch(key),
                                offset,
                                200,
                                hash=0,
                            )
                        )
                        if participants.users:
                            if row_orders["type_analyze"] == 1:
                                for user in participants.users:
                                    if not user.id in participants_all_id:
                                        participants_all_id.append(user.id)
                                        if user.username:
                                            username = f"@{user.username}"
                                            if not username in participants_all:
                                                try:
                                                    client(
                                                        telethon.functions.channels.GetParticipantRequest(
                                                            channel=chat_destination,
                                                            participant=user,
                                                        )
                                                    )
                                                except (
                                                    telethon.errors.UserNotParticipantError
                                                ) as e:
                                                    try:
                                                        is_real = 0
                                                        is_online = 0
                                                        is_withphone = 0
                                                        participants_all.append(
                                                            username
                                                        )
                                                        if (
                                                            isinstance(
                                                                user.status,
                                                                telethon.types.UserStatusRecently,
                                                            )
                                                            or isinstance(
                                                                user.status,
                                                                telethon.types.UserStatusOnline,
                                                            )
                                                            or (
                                                                isinstance(
                                                                    user.status,
                                                                    telethon.types.UserStatusOffline,
                                                                )
                                                                and (
                                                                    timestamp
                                                                    - user.status.was_online.timestamp()
                                                                )
                                                                < 259200
                                                            )
                                                        ):
                                                            is_real = 1
                                                        if isinstance(
                                                            user.status,
                                                            telethon.types.UserStatusOnline,
                                                        ) or (
                                                            isinstance(
                                                                user.status,
                                                                telethon.types.UserStatusOffline,
                                                            )
                                                            and (
                                                                timestamp
                                                                - user.status.was_online.timestamp()
                                                            )
                                                            < 1800
                                                        ):
                                                            is_online = 1
                                                        if user.phone:
                                                            is_withphone = 1
                                                        utl.insert(
                                                            cs,
                                                            f"INSERT INTO {utl.reports} (order_id,username,is_real,is_online,is_withphone,status,created_at) VALUES ({row_orders['id']},'{username}',{is_real},{is_online},{is_withphone},0,{timestamp})",
                                                        )
                                                    except Exception as e:
                                                        print(f"dd: {e}")
                                                        pass
                                                except (
                                                    telethon.errors.FloodWaitError
                                                ) as e:
                                                    break
                                                except:
                                                    pass
                            else:
                                for user in participants.users:
                                    try:
                                        if not user.id in participants_all_id:
                                            participants_all_id.append(user.id)
                                            if user.username:
                                                username = "@" + user.username
                                                if not username in participants_all:
                                                    is_real = 0
                                                    is_online = 0
                                                    is_withphone = 0
                                                    participants_all.append(username)
                                                    if (
                                                        isinstance(
                                                            user.status,
                                                            telethon.types.UserStatusRecently,
                                                        )
                                                        or isinstance(
                                                            user.status,
                                                            telethon.types.UserStatusOnline,
                                                        )
                                                        or (
                                                            isinstance(
                                                                user.status,
                                                                telethon.types.UserStatusOffline,
                                                            )
                                                            and (
                                                                timestamp
                                                                - user.status.was_online.timestamp()
                                                            )
                                                            < 259200
                                                        )
                                                    ):
                                                        is_real = 1
                                                    if isinstance(
                                                        user.status,
                                                        telethon.types.UserStatusOnline,
                                                    ) or (
                                                        isinstance(
                                                            user.status,
                                                            telethon.types.UserStatusOffline,
                                                        )
                                                        and (
                                                            timestamp
                                                            - user.status.was_online.timestamp()
                                                        )
                                                        < 1800
                                                    ):
                                                        is_online = 1
                                                    if user.phone:
                                                        is_withphone = 1
                                                    utl.insert(
                                                        cs,
                                                        f"INSERT INTO {utl.reports} (order_id,username,is_real,is_online,is_withphone,status,created_at) VALUES ({row_orders['id']},'{username}',{is_real},{is_online},{is_withphone},0,{timestamp})",
                                                    )
                                    except:
                                        pass
                            try:
                                offset += len(participants.users)
                                if (int(time.time()) - timestamp_start) > 4:
                                    cs.execute(
                                        f"SELECT * FROM {utl.orders} WHERE id={row_orders['id']}"
                                    )
                                    row_orders = cs.fetchone()
                                    if not row_orders:
                                        exit()
                                    elif not row_orders["is_analyzing"]:
                                        break
                                    timestamp_start = int(time.time())
                                    count = len(participants_all_id)
                                    percent = float(
                                        "{:.2f}".format(
                                            count / participants_count * 100
                                        )
                                    )
                                    if percent >= 100:
                                        break
                                    percent_key = math.ceil((i / 26) * 100)
                                    if percent_key > percent:
                                        percent = percent_key
                                    now = jdatetime.datetime.now().strftime("%H:%M:%S")
                                    participants_all_length = len(participants_all)
                                    info_msg.edit_text(
                                        text="⏳ در حال آنالیز ...\n\n"
                                        f"🔗 لینک: {row_orders['origin']}\n"
                                        f"♻️ در حال پیشرفت: {percent}%\n"
                                        f"👥 کاربران: [{count:,}/{participants_count:,}]\n"
                                        "➖➖➖➖➖➖\n"
                                        + f"📅 مدت زمان: {utl.convert_time((timestamp_start - timestamp), 2)}\n"
                                        f"📅 زمان حال: {now}",
                                        disable_web_page_preview=True,
                                        reply_markup={
                                            "inline_keyboard": [
                                                [
                                                    {
                                                        "text": "توقف",
                                                        "callback_data": f"is_analyzing;{row_orders['id']}",
                                                    }
                                                ]
                                            ]
                                        },
                                    )
                            except:
                                pass
                        else:
                            break
                    cs.execute(
                        f"SELECT * FROM {utl.orders} WHERE id={row_orders['id']}"
                    )
                    row_orders = cs.fetchone()
                    if not row_orders:
                        exit()
                    elif not row_orders["is_analyzing"]:
                        break
                    if percent >= 100:
                        break
                    i += 1

                participants = client(
                    telethon.functions.channels.GetParticipantsRequest(
                        chat_origin,
                        telethon.types.ChannelParticipantsAdmins(),
                        0,
                        200,
                        0,
                    )
                )
                if participants.users:
                    for user in participants.users:
                        try:
                            if user.username:
                                username = f"@{user.username}"
                                cs.execute(
                                    f"DELETE FROM {utl.reports} WHERE username='{username}'"
                                )
                        except:
                            pass

                cs.execute(f"SELECT COUNT(*) as count FROM {utl.reports}")
                users_all = cs.fetchone()["count"]
                cs.execute(
                    f"SELECT COUNT(*) as count FROM {utl.reports} WHERE order_id={row_orders['id']} AND is_real=1"
                )
                users_real = cs.fetchone()["count"]
                cs.execute(
                    f"SELECT COUNT(*) as count FROM {utl.reports} WHERE order_id={row_orders['id']} AND is_real=0"
                )
                users_fake = cs.fetchone()["count"]
                cs.execute(
                    f"SELECT COUNT(*) as count FROM {utl.reports} WHERE order_id={row_orders['id']} AND is_online=1"
                )
                users_has_phone = cs.fetchone()["count"]
                cs.execute(
                    f"SELECT COUNT(*) as count FROM {utl.reports} WHERE order_id={row_orders['id']} AND is_withphone=1"
                )
                users_online = cs.fetchone()["count"]

                cs.execute(f"SELECT * FROM {utl.orders} WHERE id={row_orders['id']}")
                row_orders = cs.fetchone()
                if row_orders:
                    cs.execute(
                        f"UPDATE {utl.users} SET step='create_order;type_users;{row_orders['id']}' WHERE user_id={from_id}"
                    )
                    info_msg.reply_html(
                        text="نوع کاربران را انتخاب کنید:\n\n"
                        f"🔻 همه کاربران: {(users_real + users_fake):,}\n"
                        f"🔻 کاربران واقعی: {users_real:,}\n"
                        f"🔻 کاربران فیک: {users_fake:,}\n"
                        f"🔻 کاربران آنلاین: {users_online:,}\n"
                        f"🔻 کاربران با شماره: {users_has_phone:,}\n"
                        f"⏰ مدت زمان: {utl.convert_time((int(time.time()) - timestamp), 2)}",
                        reply_markup={
                            "resize_keyboard": True,
                            "keyboard": [
                                [{"text": "همه کاربران"}],
                                [{"text": "کاربران فیک"}, {"text": "کاربران واقعی"}],
                                [
                                    {"text": "کاربران با شماره"},
                                    {"text": "کاربران آنلاین"},
                                ],
                                [{"text": utl.menu_var}],
                            ],
                        },
                    )
            elif status == "order_file":
                cs.execute(f"SELECT * FROM {utl.orders} WHERE id={table_id}")
                row_orders = cs.fetchone()
                link = row_orders["destination"]
                try:
                    client(
                        telethon.functions.channels.GetParticipantRequest(
                            channel=link, participant="me"
                        )
                    )
                except:
                    try:
                        if "/joinchat/" in link:
                            client(
                                telethon.functions.messages.ImportChatInviteRequest(
                                    link.split("/joinchat/")[1]
                                )
                            )
                        else:
                            client(
                                telethon.functions.channels.JoinChannelRequest(
                                    channel=link
                                )
                            )
                    except telethon.errors.UserAlreadyParticipantError as e:
                        pass
                result = client(
                    telethon.functions.channels.GetFullChannelRequest(channel=link)
                )
                destination_id = int(f"-100{result.full_chat.id}")

                cs.execute(
                    f"UPDATE {utl.orders} SET destination_id='{destination_id}' WHERE id={row_orders['id']}"
                )
                cs.execute(
                    f"UPDATE {utl.users} SET step='create_order_file;file;{row_orders['id']}' WHERE user_id={from_id}"
                )
                info_msg.reply_html(
                    text="هر کدام از یوزرنیم ها را در یک خط داخل یک فایل txt وارد کنید و فایل را ارسال کنید:",
                    reply_markup={
                        "resize_keyboard": True,
                        "keyboard": [[{"text": utl.menu_var}]],
                    },
                )
        except telethon.errors.FloodWaitError as e:
            print(f"{row_mbots['phone']}" + str(e))
            end_restrict = int(e.seconds) + int(time.time())
            cs.execute(
                f"UPDATE {utl.mbots} SET status=2,end_restrict={end_restrict} WHERE id={row_mbots['id']}"
            )
            info_msg.reply_html(text="❌ اکانت محدود شده، مجدد تلاش کنید")
        except Exception as e:
            print(f"{row_mbots['phone']}: {e}")
            info_msg.reply_html(text=f"❌ خطای ناشناخته\n\n{e}")
except Exception as e:
    info_msg.reply_html(text=f"❌ خطای ناشناخته\n\n{e}")
