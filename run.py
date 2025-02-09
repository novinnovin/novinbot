import os
import subprocess

import utility as utl

directory = os.path.dirname(os.path.abspath(__file__))
filename = str(os.path.basename(__file__))

utl.get_params_pids_by_full_script_name(
    script_names=[f"{directory}/{filename}"], is_kill_proccess=True
)


subprocess.Popen([utl.python_version, f"{directory}/bot.py"])
subprocess.Popen([utl.python_version, f"{directory}/cron_settings.py"])
subprocess.Popen([utl.python_version, f"{directory}/cron_operation.py"])
