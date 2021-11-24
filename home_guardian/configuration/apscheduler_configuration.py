import pytz
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger

from home_guardian.function_collection import get_cpu_count

_job_store = {"default": MemoryJobStore()}
_executors = {
    "default": ThreadPoolExecutor(
        max_workers=get_cpu_count(),
        pool_kwargs={"thread_name_prefix": "APSchedulerExecutor"},
    )
}
_job_defaults = {"coalesce": False, "max_instances": 3}
scheduler: BackgroundScheduler = BackgroundScheduler(
    jobstore=_job_store,
    executors=_executors,
    job_defaults=_job_defaults,
    timezone=pytz.timezone("Asia/Hong_Kong"),
)
scheduler.start()


def configure() -> None:
    """
    Configure APScheduler.
    """
    logger.warning(f"APScheduler configured. {scheduler}")


def cleanup() -> None:
    """
    Clean up APScheduler.
    """
    scheduler.shutdown()
    logger.warning(f"The scheduler was shut down completely, {scheduler}")


@scheduler.scheduled_job("interval", minutes=1)
def timed_job() -> None:
    logger.info("This job is run every 1 minute.")
