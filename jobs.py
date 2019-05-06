"""Heroku Scheduler process. Runs every hour at :00"""
from datetime import datetime
import os

from evocloud import db
from evocloud.models import File
from evocloud.utils import get_extension
from evocloud.config import Config


def cleanup():
    pool = [f for f in File.query.all() if f.exp_date <= datetime.now()]
    if pool:
        for file in pool:
            f = File.query.filter_by(file=file.file, hash=file.hash).first()
            # delete file from storage

            # heroku stores user files only for few minutes,
            # so there's no sense in os.remove() operation.
            # though i should've connected AWS S3 & used boto3 to interact
            # with its API via python, my payment credentials auth failed

            # os.remove(os.path.join(Config.UPLOAD_FOLDER,
            #                       (file.hash + get_extension(file.file))))

            # delete database record
            db.session.delete(f)
    db.session.commit()


if __name__ == '__main__':
    cleanup()
