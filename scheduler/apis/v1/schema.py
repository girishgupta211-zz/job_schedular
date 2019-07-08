from flask_restplus import fields

from scheduler.apis import api

SCHEDULE_JOB_MODEL = api.model(
    'Schedule Job Model',
    {
        'function_path': fields.String(
            description='absolute path of function',
            example='scheduler.utils.tasks.visit_urls'),
        'args': fields.List(fields.List(
            fields.String(),
            description='args array',
            example=[
                "https://apscheduler.readthedocs.io",
                "https://github.com/agronholm/apscheduler"]
        )),
        'cron_tab_expr': fields.String(
            description='cron tab expression',
            example="41 18 * * *"),
    }
)
