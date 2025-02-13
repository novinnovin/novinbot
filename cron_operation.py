import os, time, utility as utl


directory = os.path.dirname(os.path.abspath(__file__))
filename = str(os.path.basename(__file__))

utl.get_params_pids_by_full_script_name(script_names=[f"{directory}/{filename}"], is_kill_proccess=True)
print(f"ok: {filename}")


while True:
    try:
        cs = utl.Database()
        cs = cs.data()

        cs.execute(f"SELECT * FROM {utl.admin}")
        row_admin = cs.fetchone()

        cs.execute(f"SELECT * FROM {utl.reports} GROUP BY order_id ORDER BY id DESC LIMIT 10")
        result = cs.fetchall()
        for row_reports in result:
            cs.execute(f"SELECT * FROM {utl.orders} WHERE id={row_reports['order_id']}")
            row_orders = cs.fetchone()
            if row_orders is None:
                cs.execute(f"DELETE FROM {utl.reports} WHERE order_id={row_reports['order_id']}")

        cs.execute(f"SELECT * FROM {utl.orders} WHERE status=2 AND is_finalanalyzed=0")
        result = cs.fetchall()
        for row_orders in result:
            cs.execute(f"DELETE FROM {utl.usedaccs} WHERE order_id={row_orders['id']}")
            list_users = ""
            cs.execute(f"SELECT * FROM {utl.reports} WHERE order_id={row_orders['id']} AND status=0")
            result_reports = cs.fetchall()
            if result_reports:
                for row_reports in result_reports:
                    list_users += f"{row_reports['username']}\n"
                with open(f"{directory}/files/exo_{row_orders['id']}_r.txt", 'w') as file:
                    file.write(list_users)
            
            list_users = ""
            cs.execute(f"SELECT * FROM {utl.reports} WHERE order_id={row_orders['id']} AND status=1")
            result_reports = cs.fetchall()
            if result_reports:
                for row_reports in result_reports:
                    list_users += f"{row_reports['username']}\n"
                with open(f"{directory}/files/exo_{row_orders['id']}_m.txt", 'w') as file:
                    file.write(list_users)
            
            list_users = ""
            cs.execute(f"SELECT * FROM {utl.reports} WHERE order_id={row_orders['id']} AND status=2")
            result_reports = cs.fetchall()
            if result_reports:
                for row_reports in result_reports:
                    list_users += f"{row_reports['username']}\n"
                with open(f"{directory}/files/exo_{row_orders['id']}_e.txt", 'w') as file:
                    file.write(list_users)

            cs.execute(f"DELETE FROM {utl.reports} WHERE order_id={row_orders['id']} AND status NOT IN (1)")
            cs.execute(f"UPDATE {utl.orders} SET is_finalanalyzed=1 WHERE id={row_orders['id']}")
            
            
        cs.execute(f"SELECT * FROM {utl.orders} WHERE status=1")
        row_orders = cs.fetchone()
        if row_orders is not None:
            where = ""
            cats = row_orders['cats'].split(",")
            for category in cats:
                where += f"cat_id={int(category)} OR "
            where = where[0:-4]
            
            cs.execute(f"SELECT * FROM {utl.mbots} WHERE status=1 AND ({where}) ORDER BY last_order_at ASC")
            result_mbots = cs.fetchall()
            cs.execute(f"SELECT * FROM {utl.reports} WHERE order_id={row_orders['id']} AND status=0 LIMIT 1")
            result_reports = cs.fetchall()
            if result_mbots and result_reports:
                for row_mbots in result_mbots:
                    result_pids = utl.get_params_pids_by_full_script_name(param1=row_mbots['uniq_id'])
                    if not result_pids:
                        cs.execute(f"SELECT * FROM {utl.usedaccs} WHERE order_id={row_orders['id']} AND bot_id={row_mbots['id']}")
                        if cs.fetchone() is None:
                            os.system(f"{utl.python_version} \"{directory}/tl_run_account.py\" {row_mbots['uniq_id']} {row_orders['id']}")
                    
                    cs.execute(f"SELECT * FROM {utl.orders} WHERE id={row_orders['id']}")
                    row_orders = cs.fetchone()
                    if row_orders['status'] != 2 and row_orders['count_moved'] > 0 and row_orders['count_moved'] >= row_orders['count']:
                        cs.execute(f"UPDATE {utl.orders} SET status=2,updated_at={int(time.time())} WHERE id={row_orders['id']}")
                        break
            
            cs.execute(f"SELECT * FROM {utl.orders} WHERE id={row_orders['id']}")
            row_orders = cs.fetchone()
            if row_orders['status'] != 2:
                cs.execute(f"UPDATE {utl.orders} SET status=2,updated_at={int(time.time())} WHERE id={row_orders['id']}")
    except Exception as e:
        print(f"Error in main: {e}")
    time.sleep(10)

