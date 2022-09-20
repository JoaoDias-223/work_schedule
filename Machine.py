from Worker import Worker


class Machine:
    def __init__(self, id: int = 0):
        self.current_worker: Worker = None
        self.is_being_used: bool = False
        self.id = id

    def set_worker(self, worker: Worker):
        self.current_worker = worker
        is_being_used = True

    def reset(self):
        self.current_worker = None
        self.is_being_used = False

    def __str__(self):
        return f"[id: {self.id}, " \
               f"current_worker: {self.current_worker}]"
