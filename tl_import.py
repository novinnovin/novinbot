import os, sys, time, telethon.sync, utility as utl


for index, arg in enumerate(sys.argv):
    if index == 1:
        mbots_uniq_id = arg

directory = os.path.dirname(os.path.abspath(__file__))
timestamp = int(time.time())

cs = utl.Database()
cs = cs.data()


cs.execute(f"SELECT * FROM {utl.mbots} WHERE uniq_id='{mbots_uniq_id}'")
row_mbots = cs.fetchone()
try:
    client = telethon.sync.TelegramClient(session=f"{directory}/sessions/{row_mbots['uniq_id']}.session", api_id=row_mbots['api_id'], api_hash=row_mbots['api_hash'])
    client.connect()
    if client.is_user_authorized():
        me = client.get_me()
        phone = me.phone
        client.disconnect()

        cs.execute(f"SELECT * FROM {utl.mbots} WHERE phone='{phone}' AND status>0")
        row_mbots_select = cs.fetchone()
        if row_mbots_select is None:
            print("Success")
            phone = phone.replace("+","").replace(" ","")
            cs.execute(f"UPDATE {utl.mbots} SET user_id={me.id},phone='{phone}',status=1,created_at={timestamp} WHERE id={row_mbots['id']}")
        else:
            print("Existed")
    else:
        print("Failed")
        cs.execute(f"DELETE FROM {utl.mbots} WHERE id={row_mbots['id']}")
except Exception as e:
    print(f"tl_import.py: {e}")
