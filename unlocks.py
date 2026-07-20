# unlocks.py


from commands.jobs import JOBS


def get_unlocked_jobs(level):

    unlocked = []

    for job, data in JOBS.items():

        if level >= data["level"]:

            unlocked.append(job)

    return unlocked