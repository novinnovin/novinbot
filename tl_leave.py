import os, sys, time, jdatetime, telethon, telethon.sync, utility as utl


for index, arg in enumerate(sys.argv):
    if index == 1:
        mbots_uniq_id = arg
    elif index == 2:
        from_id = arg
    elif index == 3:
        status = arg
    elif index == 4:
        message_id = int(arg)
    # elif index == 5:
    #     ex_data = arg.split(",")

directory = os.path.dirname(os.path.abspath(__file__))
timestamp = int(time.time())

cs = utl.Database()
cs = cs.data()

cs.execute(f"SELECT * FROM {utl.mbots} WHERE uniq_id='{mbots_uniq_id}'")
row_mbots = cs.fetchone()

utl.get_params_pids_by_full_script_name(param1=row_mbots['uniq_id'], is_kill_proccess=True)

count_op = 0
# timestamp_start = int(time.time())
# count_analyze = int(ex_data[0])
# count_analyzable = int(ex_data[1])
try:
    client = telethon.sync.TelegramClient(session=f"{directory}/sessions/{row_mbots['uniq_id']}", api_id=row_mbots['api_id'], api_hash=row_mbots['api_hash'])
    client.connect()
    if not client.is_user_authorized():
        cs.execute(f"UPDATE {utl.mbots} SET status=0 WHERE id={row_mbots['id']}")
    else:
        if status == 'channel':
            cs.execute(f"UPDATE {utl.mbots} SET last_leave_at={timestamp} WHERE id={row_mbots['id']}")
            for dialog in client.iter_dialogs():
                chat_id = dialog.entity.id
                if isinstance(dialog.entity, telethon.types.Channel):
                    client(telethon.functions.channels.LeaveChannelRequest(channel=dialog.entity))
                    count_op += 1
            # if (int(time.time()) - timestamp_start) > 4 or count_analyze == count_analyzable:
            #     timestamp_start = int(time.time())
            #     utl.bot.edit_message_text(
            #         chat_id=from_id,
            #         text="⏳ در حال ترک چت ها...\n\n"
            #             f"👤 اکانت ها: <b>[{count_analyze:,} / {count_analyzable:,}]</b> <b>{int((count_analyze / count_analyzable) * 100)}%</b>\n"
            #             f"♻️ ترک کرده: <b>{count_op:,}</b>\n"
            #             "➖➖➖➖➖➖\n"
            #             f"📅 مدت زمان: <b>{utl.convert_time((int(time.time()) - int(ex_data[2])), 2)}</b>\n"
            #             f"📅 زمان حال: <b>{jdatetime.datetime.now().strftime('%H:%M:%S')}</b>",
            #         parse_mode='html',
            #         message_id=message_id
            #     )
except Exception as e:
    print(f"{row_mbots['phone']}: {e}")

