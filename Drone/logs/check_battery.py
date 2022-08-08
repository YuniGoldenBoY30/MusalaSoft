import os

from crontab import CronTab

empty_cron = CronTab()
my_user_cron = CronTab(user=True)
# users_cron = CronTab(user=f'{os.getlogin()}')

file_cron = CronTab(tabfile='filename.tab')
mem_cron = CronTab(tab="""
  * * * * * command
""")