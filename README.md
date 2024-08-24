# Web_world
celery -A app_parking worker -l info -P eventlet
celery -A app_parking beat -l info
celery -A app_parking flower --broker=redis://localhost:6379/0 --address='127.0.0.1' -l info --pool=eventlet