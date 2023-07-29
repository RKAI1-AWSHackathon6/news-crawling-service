from celery import Celery
from core.config import settings

celery_app = Celery("worker",
                    broker=settings.REDIS_BROKER_URL,
                    backend=settings.REDIS_BACKEND_URL)

# How many messages to prefetch at a time multiplied by the number of concurrent processes.
# disable prefetching, set worker_prefetch_multiplier to 1
celery_app.conf.update(worker_prefetch_multiplier=1)
celery_app.conf.broker_transport_options = {
    'queue_order_strategy': 'priority',
}

celery_app.conf.task_routes = {"worker.keyword_extraction": {"queue":"keyword-extraction-queue"},
                               "app.worker.processing": {"queue":"main-queue"}}

