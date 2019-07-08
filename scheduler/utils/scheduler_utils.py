import atexit
import importlib
import logging
import os

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from scheduler.utils.custom_exceptions import (
    InvalidCronExpressionError, InvalidFunctionError, JobNotFoundError
)

postgres = {
    'user': os.getenv("POSTGRES_USER"),
    'pw': os.getenv("POSTGRES_PASSWORD"),
    'db': os.getenv("POSTGRES_DB"),
    'host': os.getenv("POSTGRES_HOST"),
    'port': os.getenv("POSTGRES_PORT"),
}
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % postgres

jobstore = {
    'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
}


def task_status(event):
    if event.exception:
        logging.error('Task crashed')
    else:
        logging.info('Task completed')


bg_scheduler = BackgroundScheduler(jobstores=jobstore)
bg_scheduler.add_listener(task_status, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
bg_scheduler.start()
atexit.register(lambda: bg_scheduler.shutdown())


def schedule_job(func_path, args, cron_tab_expr):
    """
    Schedule job
    :param func_path:
    :param args:
    :param cron_tab_expr: See https://en.wikipedia.org/wiki/Cron for more
     information on the format accepted here.
    :return:
    """
    path, name = None, None
    try:
        path, name = func_path.rsplit('.', 1)
        module = importlib.import_module(path)
        return bg_scheduler.add_job(
            getattr(module, name),
            CronTrigger.from_crontab(cron_tab_expr),
            args=args
        )
    except (ImportError, AttributeError):
        raise InvalidFunctionError(
            'function: %s at path: %s not present' % (name, path)
        )
    except ValueError:
        # from_crontab raises value error if crontab expression is not correct
        raise InvalidCronExpressionError(
            'cron expression %s is not valid' % cron_tab_expr
        )


def get_all_scheduled_jobs():
    """
    Return all scheduled jobs
    """
    jobs = bg_scheduler.get_jobs()
    return serialize_job_details(jobs)


def modify_job(job_id, action):
    """
    Pause/Resume Scheduled Job
    :param job_id:
    :param action:
    :return:
    """
    try:
        if action == 'pause':
            bg_scheduler.pause_job(job_id=job_id)
        elif action == 'resume':
            bg_scheduler.resume_job(job_id=job_id)
        elif action == 'remove':
            bg_scheduler.remove_job(job_id=job_id)

    except JobLookupError:
        raise JobNotFoundError('job with id %s not found' % job_id)


def serialize_job_details(jobs):
    """
    Serialize job objects
    :param jobs:
    :return:
    """
    data = [{'id': job.id, 'name': job.name, 'args': job.args,
             'next_run_time': str(job.next_run_time)} for job in jobs]
    return data
