import schedule, time


import getlog

def job():
    getlog.main()


def main():
    schedule.every(1).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()