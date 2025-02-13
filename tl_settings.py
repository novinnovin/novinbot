import os, sys, time, glob, random, telethon.sync, utility as utl


for index, arg in enumerate(sys.argv):
    if index == 1:
        mbots_uniq_id = arg

directory = os.path.dirname(os.path.abspath(__file__))
timestamp = int(time.time())

cs = utl.Database()
cs = cs.data()

cs.execute(f"SELECT * FROM {utl.admin}")
row_admin = cs.fetchone()

cs.execute(f"SELECT * FROM {utl.mbots} WHERE uniq_id='{mbots_uniq_id}'")
row_mbots = cs.fetchone()

try:
    client = telethon.sync.TelegramClient(session=f"{directory}/sessions/{row_mbots['uniq_id']}", api_id=row_mbots['api_id'], api_hash=row_mbots['api_hash'])
    client.connect()
    if client.is_user_authorized():
        if row_admin['change_pass'] and row_admin['account_password'] is not None and (timestamp - row_mbots["change_pass_at"]) > 43200 and not row_mbots["is_change_pass"]:
            cs.execute(f"UPDATE {utl.mbots} SET change_pass_at={timestamp} WHERE id={row_mbots['id']}")
            try:
                new_password = row_admin['account_password']
                if row_mbots['password'] is None or row_mbots['password'] == '':
                    client.edit_2fa(new_password=new_password)
                else:
                    client.edit_2fa(current_password=row_mbots['password'], new_password=new_password)
                cs.execute(f"UPDATE {utl.mbots} SET password='{new_password}',is_change_pass=1 WHERE id={row_mbots['id']}")
                print(f"{row_mbots['phone']} : Password OK")
            except Exception as e:
                if "you entered is invalid" in str(e):
                    print(f"{row_mbots['phone']}: Password Invalid")
                    cs.execute(f"UPDATE {utl.mbots} SET is_change_pass=1 WHERE id={row_mbots['id']}")
                else:
                    print(f"Error Password: {e}")
        if row_admin['is_change_profile'] and not row_mbots["is_change_profile"]:
            files = glob.glob(f"{directory}/images/*.jpg")
            files_length = len(files) - 1
            client(telethon.functions.account.UpdateProfileRequest(first_name=utl.name_list[random.randint(0, (len(utl.name_list) - 1))], last_name='', about=utl.about_list[random.randint(0, (len(utl.about_list) - 1))]))
            client(telethon.functions.photos.UploadProfilePhotoRequest(file=client.upload_file(files[random.randint(0, files_length)])))
            client(telethon.functions.photos.UploadProfilePhotoRequest(file=client.upload_file(files[random.randint(0, files_length)])))
            cs.execute(f"UPDATE {utl.mbots} SET is_change_profile=1 WHERE id={row_mbots['id']}")
            print(f"{row_mbots['phone']} : Profile OK")
        if row_admin['is_set_username'] and not row_mbots["is_set_username"]:
            client(telethon.functions.account.UpdateUsernameRequest(username=utl.username_list[random.randint(0, (len(utl.username_list) - 1))] + utl.random_generate(10)))
            cs.execute(f"UPDATE {utl.mbots} SET is_set_username=1 WHERE id={row_mbots['id']}")
            print(f"{row_mbots['phone']} : Username OK")
        if row_admin['exit_session'] and not row_mbots["is_exit_session"] and (timestamp - row_mbots["exit_session_at"]) > 43200:
            cs.execute(f"UPDATE {utl.mbots} SET exit_session_at={timestamp} WHERE id={row_mbots['id']}")
            is_ok = True
            for session in client(telethon.functions.account.GetAuthorizationsRequest()).authorizations:
                if not session.current:
                    if (timestamp - session.date_created.timestamp()) > 90000:
                        try:
                            client(telethon.functions.account.ResetAuthorizationRequest(hash=session.hash))
                            print(f"{row_mbots['phone']}: Exit Session")
                        except:
                            is_ok = False
                    else:
                        is_ok = False
            if is_ok:
                cs.execute(f"UPDATE {utl.mbots} SET is_exit_session=1 WHERE id={row_mbots['id']}")
    else:
        cs.execute(f"UPDATE {utl.mbots} SET status=0 WHERE id={row_mbots['id']}")
except Exception as e:
    print(e)
    