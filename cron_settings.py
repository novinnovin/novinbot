import os, time, utility as utl


directory = os.path.dirname(os.path.abspath(__file__))
filename = str(os.path.basename(__file__))

utl.get_params_pids_by_full_script_name(script_names=[f"{directory}/{filename}"], is_kill_proccess=True)
print(f"ok: {filename}")


while True:
    try:
        timestamp = int(time.time())
        cs = utl.Database()
        cs = cs.data()

        cs.execute(f"UPDATE {utl.mbots} SET status=1 WHERE status=2 AND end_restrict<{timestamp}")
        cs.execute(f"SELECT * FROM {utl.orders} WHERE status=1")
        row_orders = cs.fetchone()
        if row_orders is None:
            cs.execute(f"SELECT * FROM {utl.mbots} WHERE status>0 AND ((is_exit_session=0 AND ({timestamp}-exit_session_at)>43200) OR (is_change_pass=0 AND ({timestamp}-change_pass_at)>43200) OR (is_change_profile=0) OR (is_set_username=0))")
            result = cs.fetchall()
            for row_mbots in result:
                result_pids = utl.get_params_pids_by_full_script_name(param1=row_mbots['uniq_id'])
                if not result_pids:
                    os.system(f"{utl.python_version} \"{directory}/tl_settings.py\" {row_mbots['uniq_id']}")
    except Exception as e:
        print(f"cron_settings.py: {e}")
    time.sleep(30)
