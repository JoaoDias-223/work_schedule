from math import ceil
from typing import List
from Machine import Machine
from Worker import Worker
import pandas as pd
import openpyxl



class Scheduler:
    def __init__(self,
                 number_of_machines: int = 4,
                 number_of_workers: int = 8,
                 harvesting_days: int = 90,
                 working_days: int = 6,
                 works_on_last_sunday: bool = True):

        self.number_of_machines = number_of_machines
        self.number_of_workers = number_of_workers
        self.harvesting_days = harvesting_days

        self.workers = [Worker(working_days, works_on_last_sunday, identifier=idx) for idx in range(self.number_of_workers)]
        self.machines = [Machine(id=idx) for idx in range(self.number_of_machines)]

        self.current_day = 0
        self.last_day = -1

    def run(self):
        if self.current_day == self.harvesting_days:
            return self.workers

        self.__increase__day__()
        print(f"Dia {self.current_day}")

        workers = self.__get_available_workers__()
        print()

        self.__make_workers_work__(workers)
        print()

        self.__bring_back_resting_workers__()
        self.__finish_working_day__()
        print()

        print("-"*15)

        self.run()

    def __increase__day__(self):
        self.last_day = self.current_day
        self.current_day += 1

    def __get_optimal_days_of_contract__(self):
        return ceil(self.harvesting_days / (self.number_of_workers / self.number_of_machines))

    def __get_available_workers__(self) -> List[Worker]:
        workers = []

        for idx, worker in enumerate(self.workers):
            if worker.can_work() \
                    and len(workers) < self.number_of_machines \
                    and len(worker.days_worked) < self.__get_optimal_days_of_contract__():
                workers.append(worker)
                print(f"\tO trabalhador {worker} está livre")
            else:
                print(f"\tO trabalhador {worker} tem que descansar")
                worker.rest()

        return workers

    def __make_workers_work__(self, workers: List[Worker]):
        for idx, worker in enumerate(workers):
            self.machines[idx].set_worker(worker)
            worker.work(self.current_day)
            print(f"{worker} trabalhou na máquina {self.machines[idx].id}")

        return workers

    def __bring_back_resting_workers__(self):
        for idx, worker in enumerate(self.workers):
            if worker.is_resting():
                worker.stop()

    def __finish_working_day__(self):
        for idx, worker in enumerate(self.workers):
            if worker.is_working():
                worker.stop()

    def __print_workers__(self, workers: List[Worker] = None):
        if workers is None:
            workers = self.workers

        for w in workers:
            print(w)

        print()

    def __print_machines__(self):
        for m in self.machines:
            print(m)
        print()

    def export_worker_schedule(self):
        worker_schedule = []

        for day in range(1, self.harvesting_days+1):
            print(f"day {day}")
            day_list = []
            for worker in self.workers:
                print(f"\tworker: {worker}", end=" ")
                for day_worked in worker.days_worked:
                    print(f"\t{day_worked}", end=" ")
                    if day == day_worked:
                        day_list.append(worker.id)

                print()

            worker_schedule.append(day_list)
            print("\n"*2)

        machines_column = [f"Máquina {machine.id}" for machine in self.machines]
        days_line = [f"Dia {day}" for day in range(1, self.harvesting_days+1)]

        print(worker_schedule)
        print(machines_column)

        df = pd.DataFrame(worker_schedule, index=days_line, columns=machines_column)

        df.to_excel(f"schedule.xlsx")
