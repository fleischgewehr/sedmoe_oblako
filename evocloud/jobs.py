from datetime import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler

from evocloud import db
from evocloud.models import File
from evocloud.utils import next_hour, get_extension
from evocloud.config import Config

sched = BackgroundScheduler()


# runs once on startup
@sched.scheduled_job('date', run_date=datetime.now())
# regular check every hour
@sched.scheduled_job('interval', hours=1, start_date=next_hour())
def cleanup():
    pool = [f for f in File.query.all() if f.exp_date <= datetime.now()]
    if pool:
        for file in pool:
            f = File.query.filter_by(file=file.file, hash=file.hash).first()
            # delete file from storage
            os.remove(os.path.join(Config.UPLOAD_FOLDER,
                                   (file.hash + get_extension(file.file))))
            # delete database record
            db.session.delete(f)
    db.session.commit()


sched.start()
