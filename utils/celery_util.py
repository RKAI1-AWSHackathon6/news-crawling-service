from celery.result import AsyncResult
from core.celery_app import celery_app

def get_task_result(async_result, try_cnt = 3):
    if isinstance(async_result, str):
        res = AsyncResult(async_result ,app=celery_app)
    else:
        res = async_result
    while try_cnt > 0:
        try_cnt = try_cnt - 1
        try:
            result = res.get(timeout=10)
            return True,result

        except Exception as e:
            continue
    return False, None