import os, sys, time, telethon, telethon.sync, utility as utl


for index, arg in enumerate(sys.argv):
    if index == 1:
        mbots_uniq_id = arg
    elif index == 2:
        from_id = int(arg)
    elif index == 3:
        message_id = int(arg)

directory = os.path.dirname(os.path.abspath(__file__))
timestamp = int(time.time())

cs = utl.Database()
cs = cs.data()

cs.execute(f"SELECT * FROM {utl.mbots} WHERE uniq_id='{mbots_uniq_id}'")
row_mbots = cs.fetchone()

info_msg = utl.bot.edit_message_text(chat_id=from_id, text="در حال بررسی ...", message_id=message_id)
try:
    client = telethon.sync.TelegramClient(session=f"{directory}/sessions/{row_mbots['uniq_id']}", api_id=row_mbots['api_id'], api_hash=row_mbots['api_hash'])
    client.connect()
    
    me = client.send_code_request(phone=row_mbots['phone'])
    phone_code_hash = me.phone_code_hash
    cs.execute(f"UPDATE {utl.mbots} SET code=null,password=null WHERE id={row_mbots['id']}")
    cs.execute(f"UPDATE {utl.users} SET step='add_acc;{row_mbots['id']};number;code' WHERE user_id={from_id}")
    info_msg.reply_html(text="کد ارسال شده به اکانت را وارد کنید:")
    step_login = 'code'
    i = 0
    while i < 180:
        cs.execute(f"SELECT * FROM {utl.mbots} WHERE id={row_mbots['id']}")
        row_mbots = cs.fetchone()
        if row_mbots is None:
            exit()
        elif step_login == 'code':
            if row_mbots['code'] is not None:
                try:
                    me = client.sign_in(phone=row_mbots['phone'], phone_code_hash=phone_code_hash, code=row_mbots['code'])
                    step_login = 'success'
                except telethon.errors.PhoneNumberInvalidError as e:
                    info_msg.reply_html(text="❌ شماره اشتباه است")
                    break
                except telethon.errors.PhoneCodeInvalidError as e:
                    cs.execute(f"UPDATE {utl.mbots} SET code=null WHERE id={row_mbots['id']}")
                    info_msg.reply_html(text="❌ کد اشتباه است، مجدد ارسال کنید")
                except telethon.errors.PhoneCodeExpiredError as e:
                    cs.execute(f"UPDATE {utl.mbots} SET code=null WHERE id={row_mbots['id']}")
                    info_msg.reply_html(
                        text="❌ کد منقضی شده است، به نکته زیر توجه کنید 👇🏻\n\n"
                            "فرض کنید دو تا اکانت x و y دارید\n"
                            "اگر میخواهید اکانت x رو در ربات لاگین کنید باید اینکار رو با اکانت y انجام بدید"
                    )
                    exit()
                except telethon.errors.SessionPasswordNeededError as e:
                    cs.execute(f"UPDATE {utl.users} SET step='add_acc;{row_mbots['id']};number;password' WHERE user_id={from_id}")
                    step_login = 'password'
                    info_msg.reply_html(text="رمز عبور را وارد کنید:")
        elif step_login == 'password':
            if row_mbots['password'] is not None:
                try:
                    me = client.sign_in(password=row_mbots['password'])
                    step_login = 'success'
                except telethon.errors.PasswordHashInvalidError as e:
                    cs.execute(f"UPDATE {utl.mbots} SET password=null WHERE id={row_mbots['id']}")
                    info_msg.reply_html(text="❌ رمز عبور اشتباه است، مجدد وارد کنید")
        if step_login == 'success':
            cs.execute(f"UPDATE {utl.mbots} SET user_id={me.id},status=1 WHERE id={row_mbots['id']}")
            cs.execute(f"UPDATE {utl.users} SET step='panel' WHERE user_id={from_id}")
            info_msg.reply_html(
                text="✅ با موفقیت لاگین شد\n\n"+
                    f"شماره: <code>{row_mbots['phone']}</code>",
            )
            break
        i += 1
        time.sleep(1)
except telethon.errors.FloodWaitError as e:
    info_msg.reply_html(text=f"❌ شماره به مدت {utl.convert_time(e.seconds, 2)} محدود شده است")
except telethon.errors.PhoneNumberBannedError as e:
    info_msg.reply_html(text="❌ شماره مسدود شده است")
except telethon.errors.PhonePasswordFloodError as e:
    info_msg.reply_html(text="❌ اکانت موقتا محدود شده است، بعدا تلاش کنید")
except Exception as e:
    error = str(e)
    if "database is locked" in error:
        info_msg.reply_html(text="❌ پروسس ها را کیل و مجدد امتحان کنید")
    else:
        print(f"Error2: {error}")
        info_msg.reply_html(text=f"❌ خطای رخ داد\n\n{error}")
