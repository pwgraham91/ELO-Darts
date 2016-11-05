import schedule
import time

from app.libs.game_lib import decay_users

print 'starting scheduler'

schedule.every().day.at("10:30").do(decay_users)

while True:
    schedule.run_pending()
    time.sleep(1)
    'end run pending'

print 'ending scheduler'
