import time
from threading import Thread


class Compute(Thread):
    def __init__(self, task):
        Thread.__init__(self)
        self.task = task

    # todo - replace with Logging
    def run(self):
        self.task()
        print("Data persisted in Database.")
