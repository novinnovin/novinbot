# encoding: utf-8

import utility as utl


cs = utl.Database()
cs = cs.data()

def alter_table(cs, sql):
    try:
        cs.execute(sql)
    except:
        pass
    try:
        sql_split = sql.split(" ")
        if sql[0:11] == 'ALTER TABLE':
            if 'UNIQUE' in sql:
                try:
                    cs.execute(f"ALTER TABLE {sql_split[2]} ADD CONSTRAINT {sql_split[4]} UNIQUE({sql_split[4]})")
                except:
                    pass
            sql = sql.replace("ADD", "CHANGE").replace(" UNIQUE", "")
            sql_split_2 = sql.split(f"{sql_split[2]} ")
            sql_split_2[1] = sql_split_2[1].replace(f"{sql_split[4]}", f"{sql_split[4]} {sql_split[4]}")
            sql = f"{sql_split[2]} ".join(sql_split_2)
            cs.execute(sql)
    except:
        pass

##########################
# UPDATE
##########################
# cs.execute(f"UPDATE {utl.mbots} SET uniq_id=phone WHERE status='first_level' OR status='submitted' OR status='restrict'")
# cs.execute(f"UPDATE {utl.mbots} SET status='0' WHERE status='first_level'")
# cs.execute(f"UPDATE {utl.mbots} SET status='1' WHERE status='submitted'")
# cs.execute(f"UPDATE {utl.mbots} SET status='2' WHERE status='restrict'")

# cs.execute(f"UPDATE {utl.egroup} SET status='0' WHERE status='start'")
# cs.execute(f"UPDATE {utl.egroup} SET status='2' WHERE status='end'")

# cs.execute(f"UPDATE {utl.orders} SET status='0' WHERE status='start'")
# cs.execute(f"UPDATE {utl.orders} SET status='1' WHERE status='doing'")
# cs.execute(f"UPDATE {utl.orders} SET status='2' WHERE status='end'")

# cs.execute(f"UPDATE {utl.users} SET status='0' WHERE status='user'")
# cs.execute(f"UPDATE {utl.users} SET status='1' WHERE status='admin'")
# cs.execute(f"UPDATE {utl.users} SET status='2' WHERE status='block'")

# cs.execute(f"RENAME TABLE {utl.orders.replace("gtg", "orders")} TO {utl.orders}")
# cs.execute(f"ALTER TABLE {utl.reports} CHANGE gtg_id order_id int(11) NOT NULL DEFAULT 0;")
##########################
# UPDATE
##########################

alter_table(cs, f"CREATE TABLE IF NOT EXISTS {utl.admin} (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
alter_table(cs, f"ALTER TABLE {utl.admin} ADD change_pass tinyint(1) NOT NULL DEFAULT 0 AFTER id")
alter_table(cs, f"ALTER TABLE {utl.admin} ADD exit_session tinyint(1) NOT NULL DEFAULT 0 AFTER change_pass")
alter_table(cs, f"ALTER TABLE {utl.admin} ADD is_change_profile tinyint(1) NOT NULL DEFAULT 0 AFTER exit_session")
alter_table(cs, f"ALTER TABLE {utl.admin} ADD is_set_username tinyint(1) NOT NULL DEFAULT 0 AFTER is_change_profile")
alter_table(cs, f"ALTER TABLE {utl.admin} ADD api_per_number int(11) NOT NULL DEFAULT 1 AFTER is_set_username")
alter_table(cs, f"ALTER TABLE {utl.admin} ADD limit_per_h int(11) NOT NULL DEFAULT 24 AFTER api_per_number")
alter_table(cs, f"ALTER TABLE {utl.admin} ADD add_per_h int(11) NOT NULL DEFAULT 19 AFTER limit_per_h")
alter_table(cs, f"ALTER TABLE {utl.admin} ADD account_password varchar(64) DEFAULT NULL AFTER add_per_h")


alter_table(cs, f"CREATE TABLE IF NOT EXISTS {utl.apis} (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
alter_table(cs, f"ALTER TABLE {utl.apis} ADD api_id varchar(20) DEFAULT NULL UNIQUE AFTER id")
alter_table(cs, f"ALTER TABLE {utl.apis} ADD api_hash varchar(200) DEFAULT NULL UNIQUE AFTER api_id")


alter_table(cs, f"CREATE TABLE IF NOT EXISTS {utl.egroup} (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD type TINYINT(1) NOT NULL DEFAULT 0 AFTER id")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD user_id BIGINT(20) DEFAULT NULL AFTER type")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD chat_id varchar(30) DEFAULT NULL AFTER user_id")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD link varchar(200) DEFAULT NULL AFTER chat_id")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD status tinyint(1) NOT NULL DEFAULT 0 AFTER link")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD users_all int(11) NOT NULL DEFAULT 0 AFTER status")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD users_real int(11) NOT NULL DEFAULT 0 AFTER users_all")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD users_fake int(11) NOT NULL DEFAULT 0 AFTER users_real")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD users_has_phone int(11) NOT NULL DEFAULT 0 AFTER users_fake")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD users_online int(11) NOT NULL DEFAULT 0 AFTER users_has_phone")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD participants_count int(11) NOT NULL DEFAULT 0 AFTER users_online")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD participants_online_count int(11) NOT NULL DEFAULT 0 AFTER participants_count")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD participants_bot_count int(11) NOT NULL DEFAULT 0 AFTER participants_online_count")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD created_at int(11) NOT NULL DEFAULT 0 AFTER participants_bot_count")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD updated_at int(11) NOT NULL DEFAULT 0 AFTER created_at")
alter_table(cs, f"ALTER TABLE {utl.egroup} ADD uniq_id varchar(50) DEFAULT NULL AFTER updated_at")


alter_table(cs, f"CREATE TABLE IF NOT EXISTS {utl.orders} (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD user_id BIGINT(20) DEFAULT NULL AFTER id")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD cats varchar(100) DEFAULT NULL AFTER user_id")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD origin varchar(200) NOT NULL DEFAULT 0 AFTER cats")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD origin_id varchar(20) NOT NULL DEFAULT 0 AFTER origin")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD destination varchar(200) NOT NULL DEFAULT 0 AFTER origin_id")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD destination_id varchar(20) NOT NULL DEFAULT 0 AFTER destination")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count int(11) NOT NULL DEFAULT 0 AFTER destination_id")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_moved int(11) NOT NULL DEFAULT 0 AFTER count")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD last_member_check int(11) NOT NULL DEFAULT 0 AFTER count_moved")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD max_users int(11) NOT NULL DEFAULT 0 AFTER last_member_check")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD type_users tinyint(1) NOT NULL DEFAULT 0 AFTER max_users")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD type_analyze tinyint(1) NOT NULL DEFAULT 0 AFTER type_users")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD status tinyint(1) NOT NULL DEFAULT 0 AFTER type_analyze")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD is_analyzing tinyint(1) NOT NULL DEFAULT 1 AFTER status")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_acc int(11) NOT NULL DEFAULT 0 AFTER is_analyzing")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_accban int(11) NOT NULL DEFAULT 0 AFTER count_acc")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_accout int(11) NOT NULL DEFAULT 0 AFTER count_accban")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_accreport int(11) NOT NULL DEFAULT 0 AFTER count_accout")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_accrestrict int(11) NOT NULL DEFAULT 0 AFTER count_accreport")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_accpermission int(11) NOT NULL DEFAULT 0 AFTER count_accrestrict")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_accotheerror int(11) NOT NULL DEFAULT 0 AFTER count_accpermission")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_usrrepeat int(11) NOT NULL DEFAULT 0 AFTER count_accotheerror")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_usrprivacy int(11) NOT NULL DEFAULT 0 AFTER count_usrrepeat")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_usrtoomuch int(11) NOT NULL DEFAULT 0 AFTER count_usrprivacy")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_usrban int(11) NOT NULL DEFAULT 0 AFTER count_usrtoomuch")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_usrspam int(11) NOT NULL DEFAULT 0 AFTER count_usrban")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD count_usrotheerror int(11) NOT NULL DEFAULT 0 AFTER count_usrspam")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD add_per_h int(11) NOT NULL DEFAULT 0 AFTER count_usrotheerror")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD is_finalanalyzed tinyint(1) NOT NULL DEFAULT 1 AFTER add_per_h")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD created_at int(11) NOT NULL DEFAULT 0 AFTER is_finalanalyzed")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD updated_at int(11) NOT NULL DEFAULT 0 AFTER created_at")
alter_table(cs, f"ALTER TABLE {utl.orders} ADD uniq_id varchar(50) DEFAULT NULL AFTER updated_at")


alter_table(cs, f"CREATE TABLE IF NOT EXISTS {utl.mbots} (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD creator_user_id BIGINT(20) DEFAULT NULL AFTER id")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD cat_id int(11) NOT NULL DEFAULT 0 AFTER creator_user_id")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD phone varchar(20) DEFAULT NULL AFTER cat_id")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD user_id BIGINT(20) DEFAULT NULL AFTER phone")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD status tinyint(1) NOT NULL DEFAULT 0 AFTER user_id")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD end_restrict int(11) NOT NULL DEFAULT 0 AFTER status")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD last_order_at int(11) NOT NULL DEFAULT 0 AFTER end_restrict")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD last_leave_at int(11) NOT NULL DEFAULT 0 AFTER last_order_at")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD last_delete_chats_at int(11) NOT NULL DEFAULT 0 AFTER last_leave_at")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD api_id varchar(20) DEFAULT NULL AFTER last_delete_chats_at")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD api_hash varchar(200) DEFAULT NULL AFTER api_id")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD phone_code_hash varchar(100) DEFAULT NULL AFTER api_hash")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD code int(11) DEFAULT NULL AFTER phone_code_hash")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD password varchar(100) DEFAULT NULL AFTER code")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD is_change_pass tinyint(1) NOT NULL DEFAULT 0 AFTER password")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD change_pass_at int(11) NOT NULL DEFAULT 0 AFTER is_change_pass")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD is_exit_session tinyint(1) NOT NULL DEFAULT 0 AFTER change_pass_at")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD exit_session_at int(11) NOT NULL DEFAULT 0 AFTER is_exit_session")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD is_change_profile tinyint(1) NOT NULL DEFAULT 0 AFTER exit_session_at")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD is_set_username tinyint(1) NOT NULL DEFAULT 0 AFTER is_change_profile")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD created_at int(11) NOT NULL DEFAULT 0 AFTER is_set_username")
alter_table(cs, f"ALTER TABLE {utl.mbots} ADD uniq_id varchar(50) DEFAULT NULL AFTER created_at")


alter_table(cs, f"CREATE TABLE IF NOT EXISTS {utl.usedaccs} (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
alter_table(cs, f"ALTER TABLE {utl.usedaccs} ADD order_id int(11) NOT NULL DEFAULT 0 AFTER id")
alter_table(cs, f"ALTER TABLE {utl.usedaccs} ADD bot_id int(11) NOT NULL DEFAULT 0 AFTER order_id")
alter_table(cs, f"ALTER TABLE {utl.usedaccs} ADD created_at int(11) NOT NULL DEFAULT 0 AFTER bot_id")


alter_table(cs, f"CREATE TABLE IF NOT EXISTS {utl.reports} (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
alter_table(cs, f"ALTER TABLE {utl.reports} ADD order_id int(11) NOT NULL DEFAULT 0 AFTER id")
alter_table(cs, f"ALTER TABLE {utl.reports} ADD bot_id int(11) NOT NULL DEFAULT 0 AFTER order_id")
alter_table(cs, f"ALTER TABLE {utl.reports} ADD username varchar(50) DEFAULT NULL AFTER bot_id")
alter_table(cs, f"ALTER TABLE {utl.reports} ADD is_real tinyint(1) NOT NULL DEFAULT 0 AFTER username")
alter_table(cs, f"ALTER TABLE {utl.reports} ADD is_online tinyint(1) NOT NULL DEFAULT 0 AFTER is_real")
alter_table(cs, f"ALTER TABLE {utl.reports} ADD is_withphone tinyint(1) NOT NULL DEFAULT 0 AFTER is_online")
alter_table(cs, f"ALTER TABLE {utl.reports} ADD status tinyint(1) NOT NULL DEFAULT 0 AFTER is_withphone")
alter_table(cs, f"ALTER TABLE {utl.reports} ADD created_at int(11) NOT NULL DEFAULT 0 AFTER status")


alter_table(cs, f"CREATE TABLE IF NOT EXISTS {utl.cats} (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
alter_table(cs, f"ALTER TABLE {utl.cats} ADD name varchar(50) DEFAULT NULL UNIQUE AFTER id")
alter_table(cs, f"UPDATE {utl.mbots} SET cat_id=1 WHERE cat_id=0")


alter_table(cs, f"CREATE TABLE IF NOT EXISTS {utl.users} (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
alter_table(cs, f"ALTER TABLE {utl.users} ADD user_id BIGINT(20) DEFAULT NULL UNIQUE AFTER id")
alter_table(cs, f"ALTER TABLE {utl.users} ADD status tinyint(1) NOT NULL DEFAULT 0 AFTER user_id")
alter_table(cs, f"ALTER TABLE {utl.users} ADD step varchar(50) DEFAULT NULL AFTER status")
alter_table(cs, f"ALTER TABLE {utl.users} ADD prev_step varchar(50) DEFAULT NULL AFTER step")
alter_table(cs, f"ALTER TABLE {utl.users} ADD created_at int(11) NOT NULL DEFAULT 0 AFTER prev_step")
alter_table(cs, f"ALTER TABLE {utl.users} ADD uniq_id varchar(50) DEFAULT NULL AFTER created_at")


cs.execute(f"SELECT * FROM {utl.admin}")
row_admin = cs.fetchone()
if row_admin is None:
    cs.execute(f"INSERT INTO {utl.admin} (id) VALUES (1)")

cs.execute(f"SELECT * FROM {utl.cats}")
row_cats = cs.fetchone()
if row_cats is None:
    cs.execute(f"INSERT INTO {utl.cats} (id,name) VALUES (1,'default')")
