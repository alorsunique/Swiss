from pathlib import Path
import time


def get_next_run_time(minute_root, interval_minute):

    current_time = time.time()

    # hour_mark = int(time.strftime("%H", time.localtime(current_time)))
    minute_mark = int(time.strftime("%M", time.localtime(current_time)))
    second_mark = int(time.strftime("%S", time.localtime(current_time)))

    minute_root = minute_root
    interval_minute = interval_minute

    next_minute = minute_root + ((((minute_mark-minute_root) // interval_minute) + 1) * interval_minute)

    if next_minute >= 60:
        # This resets it back to the hour
        next_run_time = current_time + ((60 - minute_mark) * 60 - second_mark)
    else:
        next_run_time = current_time + ((next_minute - minute_mark) * 60 - second_mark)

    return next_run_time

if __name__ == "__main__":
    next_run_time = get_next_run_time(0,2)
    print(next_run_time)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(next_run_time)))