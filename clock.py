# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import time

sched = BlockingScheduler()

# @sched.scheduled_job('interval', minutes=1)
@sched.scheduled_job('cron', minute='0,5,10,15,20,25,30,35,40,45,50,55', second=5 )
def timed_job_awake_your_app():
    url = 'https://ayni-booking.herokuapp.com/booking/api/cron/exec/'
    requests.post(url)

sched.start()
