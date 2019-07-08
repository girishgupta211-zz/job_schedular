from scheduler.apis import api, ns
from scheduler.apis.v1.schema import (
    SCHEDULE_JOB_MODEL,
)
from scheduler.app_settings import (
    SCHEDULE_TASK_REQUIRED_KEYS)
from scheduler.utils.custom_exceptions import (
    MissingKeysError, PayloadParseError, JobNotFoundError,
    InvalidCronExpressionError,
    InvalidFunctionError
)
from scheduler.utils.payload_processing import (
    parse_payload, check_required_keys
)
from scheduler.utils.response import response
from scheduler.utils.scheduler_utils import (
    get_all_scheduled_jobs, modify_job, schedule_job, serialize_job_details
)
from flask import current_app, request
from flask_restplus import Resource


@ns.route('/schedule-job')
class ScheduleTask(Resource):
    """
    Job scheduler
    """

    @api.expect(SCHEDULE_JOB_MODEL)
    def post(self):
        """
        Schedule job
        Method: POST
        Sample Payload:
            {
                "function_path": Absolute path of function,
                "args": Positional arguments to function,
                "cron_tab_expr": cron tab expression to schedule job.
                                please refer https://en.wikipedia.org/wiki/Cron
            }
        """
        try:
            payload = parse_payload(request)
            check_required_keys(payload, SCHEDULE_TASK_REQUIRED_KEYS)
            job = schedule_job(
                payload['function_path'],
                payload.get('args'),
                payload['cron_tab_expr']
            )
        except (InvalidCronExpressionError, InvalidFunctionError,
                MissingKeysError, PayloadParseError) as err:
            current_app.logger.error('error: %s' % err.to_dict())
            return response(error_dict=err.to_dict())

        return response(data=serialize_job_details([job]))


@ns.route('/jobs')
class ListTasks(Resource):
    """
    List all jobs
    """

    def get(self):
        """
        List all scheduled jobs
        Method: GET
        """
        jobs = get_all_scheduled_jobs()
        return response(data=jobs)


@ns.route('/job/<regex("pause|resume|remove"):action>/<string:job_id>')
class ModifyTask(Resource):
    """
    Pause/Resume/Remove job
    """

    def put(self, action, job_id):
        """
        Pause/Resume job
        Method: PUT
        """
        try:
            modify_job(job_id, action)
        except JobNotFoundError as err:
            current_app.logger.error('error: %s' % err.to_dict())
            return response(error_dict=err.to_dict())
        return response(data={'job_id': job_id})
