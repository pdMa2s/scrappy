from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler


class JobScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = {}
        self.scheduler.start()

    def add_job(self, func, hour: int, *args, **kwargs):
        job_id = f"{hour:02d}"
        if job_id in self.jobs:
            raise ValueError(f"A job with id {job_id} already exists")
        self.jobs[job_id] = self.scheduler.add_job(func, 'interval', minutes=1, *args, **kwargs)
        return job_id

    def remove_job(self, job_id: str):
        try:
            job = self.jobs.pop(job_id)
            job.remove()
            return True
        except (KeyError, JobLookupError):
            return False

    def list_jobs(self) -> set[str]:
        return set(self.jobs.keys())

    def shutdown(self):
        self.scheduler.shutdown()
