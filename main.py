from Scheduler import Scheduler


def main():
    scheduler = Scheduler()

    result = scheduler.run()

    scheduler.__print_workers__()

    scheduler.export_worker_schedule()


if __name__ == "__main__":
    main()
