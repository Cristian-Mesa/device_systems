import logging
import time
import uuid

from fastapi import Request


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('device_systems')


async def add_request_information(request: Request, call_next):
    start_time = time.perf_counter()
    request_id = request.headers.get('X-Request-ID', uuid.uuid4().hex)

    response = await call_next(request)

    process_time = time.perf_counter() - start_time
    response.headers['X-Process-Time'] = f'{process_time:.4f}'
    response.headers['X-App-Name'] = 'device_systems'
    response.headers['X-Request-ID'] = request_id

    logger.info('%s %s - %s', request.method, request.url.path, response.status_code)
    return response