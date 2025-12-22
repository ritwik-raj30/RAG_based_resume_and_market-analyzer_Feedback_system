"""
ThreadPool executor for handling heavy ML operations
Prevents blocking FastAPI event loop
"""
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio

logger = logging.getLogger(__name__)

# Create a thread pool for ML operations
# Adjust max_workers based on your server capacity (typically CPU cores)
ML_EXECUTOR = ThreadPoolExecutor(
    max_workers=4,  # Adjust based on CPU cores and memory
    thread_name_prefix="ml_worker"
)

def execute_ml_work(func, *args, **kwargs):
    """
    Execute ML work in thread pool
    Returns a coroutine that can be awaited
    
    Usage:
        result = await execute_ml_work(heavy_ml_function, arg1, arg2, kwarg1=value1)
    """
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(ML_EXECUTOR, lambda: func(*args, **kwargs))

def shutdown_executor():
    """Gracefully shutdown thread pool executor"""
    logger.info("Shutting down ML ThreadPoolExecutor...")
    ML_EXECUTOR.shutdown(wait=True)
    logger.info("ML ThreadPoolExecutor shutdown complete")


