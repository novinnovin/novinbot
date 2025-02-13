import os, re, sys, time, datetime, jdatetime, telethon, telethon.sync, utility as utl


for index, arg in enumerate(sys.argv):
    if index == 1:
        mbots_uniq_id = arg
    elif index == 2:
        from_id = arg
    elif index == 3:
        message_id = int(arg)

directory = os.path.dirname(os.path.abspath(__file__))
timestamp = int(time.time())

info_msg = utl.bot.edit_message_text(chat_id=from_id, text="در حال بررسی ...", message_id=message_id)

cs = utl.Database()
cs = cs.data()

cs.execute(f"SELECT * FROM {utl.mbots} WHERE uniq_id='{mbots_uniq_id}'")
row_mbots = cs.fetchone()
cs.execute(f"SELECT * FROM {utl.cats} WHERE id={row_mbots['cat_id']}")
row_cats = cs.fetchone()

utl.get_params_pids_by_full_script_name(param1=row_mbots['uniq_id'], is_kill_proccess=True)

try:
    client = telethon.sync.TelegramClient(session=f"{directory}/sessions/{row_mbots['uniq_id']}", api_id=row_mbots['api_id'], api_hash=row_mbots['api_hash'])
    client.connect()
    if client.is_user_authorized():
        cs.execute(f"UPDATE {utl.mbots} SET status=1 WHERE id={row_mbots['id']}")
        get_input_entity = client.get_input_entity(peer=777000)
        code = None
        for message in client.iter_messages(get_input_entity):
            try:
                code_date = jdatetime.datetime.fromtimestamp(message.date.timestamp()).astimezone(datetime.timezone(datetime.timedelta(hours=3, minutes=30)))
                regex = re.findall('Login code: [\d]*. Do not give this code', message.message)[0]
                code = regex.replace("Login code: ","").replace(". Do not give this code","")
                break
            except:
                pass
        password = f"<code>{row_mbots['password']}</code>" if row_mbots['password'] is not None else "ندارد"
        code = f"<code>{code}</code>\n‏   📅 {code_date.strftime('%Y-%m-%d %H:%M:%S')}" if code is not None else "ندارد"
        me = client.get_me()
        photo = "ندارد" if me.photo is None else "دارد"
        current_sessions = ""
        for session in client(telethon.functions.account.GetAuthorizationsRequest()).authorizations:
            if session.current:
                current_sessions += f"   🔻 IP: {session.ip}\n"
                current_sessions += f"   🔻 Country: {session.country}\n"
                current_sessions += f"   🔻 Device Model: {session.device_model}\n"
                current_sessions += f"   🔻 Platform: {session.platform}\n"
                current_sessions += f"   🔻 System Version: {session.system_version}\n"
                current_sessions += f"   🔻 Api Id: {session.api_id}\n"
                current_sessions += f"   🔻 App Name: {session.app_name}\n"
                current_sessions += f"   🔻 App Version: {session.app_version}\n"
                current_sessions += f"   🔻 Date Created: {jdatetime.datetime.fromtimestamp(session.date_created.timestamp()).strftime('%Y-%m-%d %H:%M:%S')}\n"
                current_sessions += f"   🔻 Date Active: {jdatetime.datetime.fromtimestamp(session.date_active.timestamp()).strftime('%Y-%m-%d %H:%M:%S')}\n"
        info_msg.edit_text(
            text=f"✅ اکانت فعال است\n\n"
                "سشن فعلی:\n"
                f"{current_sessions}\n"
                f"اطلاعات کلی:\n"
                f"   🔻 شماره: <code>{me.phone}</code>\n"
                f"   🔻 نام: {me.first_name}\n"
                f"   🔻 نام خانوادگی: "+(me.last_name if me.last_name is not None else "ثبت نشده")+"\n"
                f"   🔻 یوزرنیم: "+(me.username if me.username is not None else "ثبت نشده")+"\n"
                f"   🔻 تصویر: {photo}\n"
                f"\nرمز عبور: {password}\n"
                f"آخرین کد لاگین: {code}\n\n"
                f"📂 دسته بندی: ‏/category_{row_mbots['id']} ‏({row_cats['name']})\n"
                f"❌ حذف اکانت: /delete_{row_mbots['id']}",
            parse_mode='HTML'
        )
    else:
        cs.execute(f"UPDATE {utl.mbots} SET status=0 WHERE id={row_mbots['id']}")
        info_msg.edit_text(
            text="❌ اکانت در دسترس نیست\n\n"
                f"📞 شماره: <code>{row_mbots['phone']}</code>\n\n"
                f"📂 دسته بندی: ‏/category_{row_mbots['id']} ‏({row_cats['name']})\n"
                f"❌ حذف اکانت: /delete_{row_mbots['id']}",
            parse_mode='html'
        )
except telethon.errors.FloodWaitError as e:
    info_msg.edit_text(text=f"❌ اکانت به مدت {utl.convert_time(e.seconds, 2)} محدود شده است")
except Exception as e:
    error = str(e)
    if "database is locked" in error:
        info_msg.edit_text(text="❌ پروسس ها را کیل و مجدد امتحان کنید")
    elif "You have tried logging in too many times" in error:
        info_msg.edit_text(text="❌ اکانت محدود شده است، 24 ساعت بعد تلاش کنید")
    elif "The used phone number has been banned" in error:
        info_msg.edit_text(text="❌ شماره مسدود شده است")
    else:
        print(f"Error2: {error}")
        info_msg.edit_text(text=f"❌ خطای ناشناخته\n\n{error}")
    
