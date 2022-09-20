class Worker:
    NOT_ALLOCATED = 0
    WORKING = 1
    RESTING = 2

    def __init__(self, working_days: int = 6, works_on_last_sunday: bool = True, identifier: int = 0):
        self.working_days: int = working_days
        self.works_on_last_sunday: bool = works_on_last_sunday
        self.current_working_days: int = 0
        self.id = identifier
        self.days_worked = []
        self.current_state = Worker.NOT_ALLOCATED
        self.current_resting_days = 0

    def reset(self):
        self.current_working_days = 0

    def is_not_allocated(self):
        return self.current_state == Worker.NOT_ALLOCATED

    def is_working(self):
        return self.current_state == Worker.WORKING

    def is_resting(self):
        return self.current_state == Worker.RESTING

    def work(self, day: int):
        self.current_state = Worker.WORKING
        self.current_working_days += 1
        self.days_worked.append(day)

    def rest(self):
        self.current_state = Worker.RESTING
        self.current_working_days = 0

    def stop(self):
        self.current_state = Worker.NOT_ALLOCATED

    def __get_current_state__(self):
        if self.current_state == Worker.NOT_ALLOCATED:
            return "Not Allocated"
        elif self.current_state == Worker.WORKING:
            return "Working"
        elif self.current_state == Worker.RESTING:
            return "Resting"

    def has_worked_enough_days(self):
        return self.current_working_days >= self.working_days

    def can_work(self):
        return self.is_not_allocated() and not self.has_worked_enough_days()

    def __str__(self):
        return f"[id: {self.id}, " \
               f"current_working_days: {self.current_working_days}, " \
               f"current_state: {self.__get_current_state__()}, " \
               f"days_worked: {len(self.days_worked)}]"
