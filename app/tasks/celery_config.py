from celery import Celery

celery = Celery(
    main='tasks',
    broker='redis://localhost:6379',
    include=['app.tasks.tasks']
)
