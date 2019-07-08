"""
v1 version app settings
"""
APP_SECRET_KEY = "l\x9b\x0cb\x86\x96Z/-\x88Ry\x03y\xea\x9c"
URL_PREFIX = '/scheduler/api/v1'

DEFAULT_USER = 'tech.admin'

SCHEDULE_TASK_REQUIRED_KEYS = (
    'function_path',
    'cron_tab_expr',
)
