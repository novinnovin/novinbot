import os
import time
import uuid

import psutil
import pymysql
import telegram

from config import *

# version: 2.9.1

admin = "agg_admin_wcxm3zshoatkpfrlutrshidcx84gon"
apis = "agg_apis_zyehay1fsqbd7npojvk0hlaku2goqu"
cats = "agg_cats_VbSRNhBUJfgTzdE6AGu2PW3FDsKH1l"
egroup = "agg_export_bamc48pk2381zndh38pajd739cn57plq"
orders = "agg_order_nchw0128zn389xpw429qpdj38427tspa"
mbots = "agg_mbots_a28cnsz83jcn38pqn849shg48wol4"
reports = "agg_reports_wierddxz8i2ltfus1cxm0uemoovqpr"
usedaccs = "agg_usedaccs_414c4106473a47f8a9907021e6ee1572"
users = "agg_users_hc137znsdyhy38qpsk47sj39palw379"


menu_var = "🏛 منو اصلی"
back_var = "بازگشت 🔙"
step_page = 10


bot = telegram.Bot(token=token)
get_me = await bot.get_me()
bot_id = get_me.id
bot_username = get_me.username


status_users = {0: "کاربر", 1: "ادمین ✅", 2: "بلاک ⛔️"}
status_mbots = {0: "لاگ اوت شده ⏳", 1: "فعال ✅", 2: "محدود شده ⛔️"}
status_order = {
    0: "در حال آماده سازی ❕️",
    1: "در حال انجام ♻️",
    2: "پایان یافته ✅",
}
type_users_order = {
    0: "Users all",
    1: "Users real",
    2: "Users fake",
    3: "Users online",
    4: "Users has phone",
}
type_analyze_order = {
    0: "Noting",
    1: "Delete users who are already members",
}
type_reports = {
    0: "Noting",
    1: "Real users",
    2: "Fake users",
    3: "Online users",
    4: "With phone users",
}
status_reports = {
    0: "Noting",
    1: "Join users",
    2: "Error when add users",
}
status_egroup = {
    0: "Start",
    2: "End",
}


name_list = [
    "Arghavan",
    "Yaran",
    "Parmida",
    "Tara",
    "Samin",
    "Janan",
    "Chakameh",
    "Hadis",
    "Dayan",
    "Zakereh",
    "Roya",
    "Zari",
    "Sara",
    "Shadi",
    "Atefeh",
    "Ghazal",
    "Gasedak",
    "Amal",
    "Aneseh",
    "Atiyeh",
    "Ala",
    "Ayeh",
    "Ayat",
    "Aynoor",
    "Abtesam",
    "Aklil",
    "Akram",
    "Asena",
    "Amira",
    "Amaneh",
    "Amineh",
    "Asila",
    "Aroon",
    "Ima",
    "Asra",
    "Alhan",
    "Alisa",
    "Talia",
    "Tabarak",
    "Tabasom",
    "Taranom",
    "Taktam",
    "Tasnim",
    "Tina",
    "Sana",
    "Smr",
    "Samreh",
    "Samina",
    "Samineh",
    "Samin",
    "Jenan",
    "Hanipha",
    "Hanipheh",
    "Hoora",
    "Hooraneh",
    "Hareh",
    "Hamedeh",
    "Hadis",
    "Hadiseh",
    "Hakimeh",
    "Hosna",
    "Hosniyeh",
    "Hosna",
    "Hasiba",
    "Hamra",
    "Hemaseh",
    "Hana",
    "Hanan",
    "Hananeh",
    "Hoor Afarin",
    "Hoor Rokh",
    "Hoordis",
    "Hoorcad",
    "Hoori Dokht",
    "Hoorosh",
    "Hooriya",
    "Halma",
    "Heliya",
    "Heliyeh",
    "Khazar",
    "Dina",
    "Dorsa",
    "Rada",
    "Rahel",
    "Rafe",
    "Rayehe",
    "Rakeehe",
    "Rahil",
    "Rahmeh",
    "Raziyeh",
    "Rezvaneh",
    "Roman",
    "Roman",
    "Reyhan",
    "Reyhaneh",
    "Raniya",
    "Romisa",
    "Zamzam",
    "Zoofa",
    "Zeytoon",
]
about_list = [
    "Do not let anyone step on your dreams",
    "If you are afraid of the heights of the sky, you cant own the moon",
    "Be deaf when your beautiful dreams are said to be impossible",
    "You only know a part of me; I am a world full of mystery",
    "Be your own hero",
    "Be happy, let them understand that you are stronger than yesterday",
    "In a world full of trends I want to remain a classic",
    "Be strong and firm :) But be kind",
    "Stay kind. It makes you beautiful.",
    "Blocking is for the weak youre gonna see me enjoying my life",
    "You can break me, but you will never destroy me",
    "Never be the same to people, who arent the same to you anymore",
    "always smile laughter embarrasses your enemies",
    "Some people want to see you fail Disappoint them",
    "know the difference between being patient and wasting your time",
    "Silent people have the loudest minds",
    "silence is the most powerful sceam",
    "Live for ourselves not for showing that to others",
    "I will win, not immediately but definitely",
    "Life is short… Smile while you still have teeth",
    "Forgiving someone is easy, trusting them again not",
    "The kites always rise with adverse winds",
    "When you catch in a calumny, you know your real friends",
    "When you realize Your worth youll stop giving people Discounts",
    "Always the huge blaze is from small spunkie",
    "I shine from within so no one can dim my light",
    "We are born to be real, not perfect",
    "I’m a woman with ambition and a heart of gold",
    "Everything started from a dream",
    "Believing in making the impossible possible",
    "We have nothing to fear but fear itself",
    "My mission in life is not merely to survive but thrive",
    "It wasn’t always easy but it’s worth it",
    "Time is precious, waste it wisely",
    "Live each day as if itٌs your last",
    "Life is short. Live passionately",
]
username_list = [
    "mary",
    "jennifer",
    "elizabeth",
    "linda",
    "barbara",
    "susan",
    "margaret",
    "jessica",
    "dorothy",
    "sarah",
    "nancy",
    "betty",
    "lisa",
    "sandra",
    "helen",
    "ashley",
    "donna",
    "kimberly",
    "carol",
    "michelle",
    "emily",
    "amanda",
    "melissa",
    "deborah",
    "laura",
    "stephanie",
    "rebecca",
    "sharon",
    "kathleen",
    "cynthia",
    "ruth",
    "anna",
    "shirley",
    "amy",
    "angela",
    "virginia",
    "brenda",
    "pamela",
    "catherine",
    "nicole",
    "samantha",
    "dennis",
    "diane",
]


def insert(cs, sql):
    try:
        cs.execute(sql)
    except:
        pass


def unique_id():
    return str(uuid.uuid1()).replace("-", "")


def select_api(cs, num):
    outout = ""
    cs.execute(
        f"SELECT api_id,count(*) FROM {mbots} GROUP BY api_id HAVING count(*)>={num}"
    )
    result = cs.fetchall()
    if not result:
        cs.execute(f"SELECT * FROM {apis} ORDER BY RAND()")
        return cs.fetchone()

    for row in result:
        outout += f"'{row['api_id']}',"

    cs.execute(
        f"SELECT * FROM {apis} WHERE api_id NOT IN ({outout[0:-1]}) ORDER BY RAND()"
    )
    return cs.fetchone()


def convert_time(time, level=4):
    time = int(time)
    day = int(time / 86400)
    hour = int((time % 86400) / 3600)
    minute = int((time % 3600) / 60)
    second = int(time % 60)
    level_check = 1
    if time >= 86400:
        if time == 86400:
            return "1 روز"
        output = f"{day} روز"
        if hour > 0 and level > level_check:
            output += f", {hour} ساعت"
            level_check += 1
        if minute > 0 and level > level_check:
            output += f", {minute} دقیقه"
            level_check += 1
        if second > 0 and level > level_check:
            output += f", {second} ثانیه"
        return output
    if time >= 3600:
        if time == 3600:
            return "1 ساعت"
        output = f"{hour} ساعت"
        if minute > 0 and level > level_check:
            output += f", {minute} دقیقه"
            level_check += 1
        if second > 0 and level > level_check:
            output += f", {second} ثانیه"
        return output
    if time >= 60:
        if time == 60:
            return "1 دقیقه"
        output = f"{minute} دقیقه"
        if second > 0 and level > level_check:
            output += f", {second} ثانیه"
        return output
    if second > 0:
        return f"{second} ثانیه"
    else:
        return f"1 ثانیه"


def get_params_pids_by_full_script_name(
    script_names=None, param1=None, param2=None, is_kill_proccess=False
):
    pids = []
    if script_names is not None:
        if isinstance(script_names, str):
            script_names = [script_names]
        for script_name in script_names:
            for proc in psutil.process_iter():
                try:
                    cmdline = proc.cmdline()
                    pid = proc.pid
                    if (
                        len(cmdline) >= 2
                        and "python" in cmdline[0]
                        and cmdline[1] == script_name
                    ):
                        if param1 is not None and cmdline[2] != param1:
                            continue
                        if param2 is not None and cmdline[3] != param2:
                            continue
                        if len(cmdline) >= 5:
                            pids.append(
                                {
                                    "pid": pid,
                                    "param1": cmdline[2],
                                    "param2": cmdline[3],
                                    "param3": cmdline[4],
                                }
                            )
                        elif len(cmdline) >= 4:
                            pids.append(
                                {"pid": pid, "param1": cmdline[2], "param2": cmdline[3]}
                            )
                        elif len(cmdline) >= 3:
                            pids.append({"pid": pid, "param1": cmdline[2]})
                        else:
                            pids.append({"pid": pid})
                except:
                    pass
    else:
        for proc in psutil.process_iter():
            try:
                cmdline = proc.cmdline()
                pid = proc.pid
                if len(cmdline) < 2 or "python" not in cmdline[0]:
                    continue
                if param1 is not None and cmdline[2] != param1:
                    continue
                if param2 is not None and cmdline[3] != param2:
                    continue
                if len(cmdline) >= 5:
                    pids.append(
                        {
                            "path": cmdline[1],
                            "pid": pid,
                            "param1": cmdline[2],
                            "param2": cmdline[3],
                            "param3": cmdline[4],
                        }
                    )
                elif len(cmdline) >= 4:
                    pids.append(
                        {
                            "path": cmdline[1],
                            "pid": pid,
                            "param1": cmdline[2],
                            "param2": cmdline[3],
                        }
                    )
                elif len(cmdline) >= 3:
                    pids.append({"path": cmdline[1], "pid": pid, "param1": cmdline[2]})
                else:
                    pids.append({"path": cmdline[1], "pid": pid})
            except:
                pass
    if is_kill_proccess and pids:
        pid_this_thread = int(os.getpid())
        for procc in pids:
            if pid_this_thread != procc["pid"]:
                try:
                    pid = psutil.Process(procc["pid"])
                    pid.terminate()
                except:
                    pass
        time.sleep(1)
    return pids


class Database:
    def __init__(self):
        cs = pymysql.connect(
            host=host_db,
            user=user_db,
            password=passwd_db,
            database=database,
            port=port,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        cs = cs.cursor()
        self.cs = cs

    def data(self):
        return self.cs


class Pagination:
    def __init__(
        self, update, type_btn, output, step_page, num_all_pages, extra_key=""
    ):
        self.update = update
        self.type_btn = type_btn
        self.text = output
        self.step_page = step_page
        self.num_all_pages = num_all_pages
        self.extra_key = extra_key

    def setStepPage(self, step_page):
        self.step_page = step_page

    def setText(self, text):
        self.text = text

    def setNumAllPages(self, num_all_pages):
        self.num_all_pages = num_all_pages

    def process(self):
        if self.update.callback_query:
            self.processCallback()
        else:
            self.processMessage()

    def processMessage(self):
        if self.num_all_pages > self.step_page:
            return self.update.message.reply_html(
                text=self.text,
                disable_web_page_preview=True,
                reply_markup={
                    "inline_keyboard": [
                        [
                            {
                                "text": "« صفحه 2",
                                "callback_data": f"pg;{self.type_btn};2;{self.extra_key}",
                            }
                        ]
                    ]
                },
            )
        else:
            return self.update.message.reply_html(
                text=self.text, disable_web_page_preview=True
            )

    def processCallback(self):
        query = self.update.callback_query
        ex_data = query.data.split(";")
        num_current_page = int(ex_data[2])
        num_prev_page = num_current_page - 1
        num_next_page = num_current_page + 1
        if num_current_page == 1:
            return query.edit_message_text(
                text=self.text,
                parse_mode="HTML",
                disable_web_page_preview=True,
                reply_markup={
                    "inline_keyboard": [
                        [
                            {
                                "text": f"« صفحه {num_next_page}",
                                "callback_data": f"pg;{self.type_btn};{num_next_page};{self.extra_key}",
                            }
                        ]
                    ]
                },
            )
        elif self.num_all_pages > (num_current_page * self.step_page):
            return query.edit_message_text(
                text=self.text,
                parse_mode="HTML",
                disable_web_page_preview=True,
                reply_markup={
                    "inline_keyboard": [
                        [
                            {
                                "text": f"صفحه {num_prev_page} »",
                                "callback_data": f"pg;{self.type_btn};{num_prev_page};{self.extra_key}",
                            },
                            {
                                "text": f"« صفحه {num_next_page}",
                                "callback_data": f"pg;{self.type_btn};{num_next_page};{self.extra_key}",
                            },
                        ]
                    ]
                },
            )
        else:
            return query.edit_message_text(
                text=self.text,
                parse_mode="HTML",
                disable_web_page_preview=True,
                reply_markup={
                    "inline_keyboard": [
                        [
                            {
                                "text": f"صفحه {num_prev_page} »",
                                "callback_data": f"pg;{self.type_btn};{num_prev_page};{self.extra_key}",
                            }
                        ]
                    ]
                },
            )
