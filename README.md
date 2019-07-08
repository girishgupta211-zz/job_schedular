# Job Scheduler

This is a REST Interface for scheduling jobs
# Setup pipenv
```bash
pipenv shell
pipenv install
````

## Run the Project
to run scheduling server

```python
export FLASK_APP=wsgi.py
export FLASK_RUN_PORT=8002 #only if you want to run it on different port
flask run
```

## Check APIs documentation here

http://127.0.0.1:8002/v1/app/scheduler/doc/

#Run DB migration on EC2 instance if there is any database change
```
cd /home/ubuntu/scheduler
cp /etc/sysconfig/scheduler/.env  .
venv --venv
#this will give you pipenv path like /home/ubuntu/.local/share/virtualenvs/scheduler-o0SoDClB
source /home/ubuntu/.local/share/virtualenvs/scheduler-o0SoDClB/bin/activate
flask db init
flask db migrate
flask db upgrade
```
