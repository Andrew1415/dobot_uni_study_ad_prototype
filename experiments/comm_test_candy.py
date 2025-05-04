import sys
from pathlib import Path
import csv
import logging
import time
from datetime import datetime
import threading

script_dir   = Path(__file__).resolve().parent    # experiments/
project_root = script_dir.parent                  # parent of experiments/ and src/
sys.path.insert(0, str(project_root / "src"))

from communication_tcp import (
    setup_communication,
    request_candy,
    close_communication,
    RESPONSE_SUCCESS
)

CSV_FILENAME = "candy_robot_communication_test.csv"
ITERATIONS   = 1
X_MAX, Y_MAX = 3, 5


def request_candy_sync(cmd: str) -> bool:
    """
    Wraps the async request_candy(cmd, callback) into a blocking call.
    Returns True if the robot responded with RESPONSE_SUCCESS, else False.
    """
    done = threading.Event()
    result = {"ok": False}

    def _callback(response_code: int):
        result["ok"] = (response_code == RESPONSE_SUCCESS)
        done.set()

    # fire off the async request
    request_candy(cmd, _callback)
    # wait until the callback signals completion
    done.wait()
    return result["ok"]


def test_candy_communication():
    # 1) configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

    # 2) connect once, before any send
    setup_communication()

    # 3) open CSV for writing
    with open(CSV_FILENAME, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "iteration",
            "x",
            "y",
            "send_timestamp",
            "response_timestamp",
            "duration",
            "success"
        ])

        # 4) loops: each (x,y) for ITERATIONS times
        for iteration in range(1, ITERATIONS + 1):
            for x in range(0, X_MAX + 1):
                for y in range(0, Y_MAX + 1):
                    cmd = f"{x},{y}"

                    dt_send = datetime.now()
                    success = request_candy_sync(cmd)   # blocks until done
                    dt_resp = datetime.now()

                    duration_td = dt_resp - dt_send

                    t_send     = dt_send.isoformat(timespec="milliseconds")
                    t_resp     = dt_resp.isoformat(timespec="milliseconds")
                    duration_s = duration_td.total_seconds()  # duration in seconds (float)
                    writer.writerow([
                        iteration,
                        x,
                        y,
                        t_send,
                        t_resp,
                        duration_s,
                        success
                    ])

                    # small pause to avoid overwhelming the robot
                    time.sleep(0.01)

    # 5) close the socket once, after all sends
    close_communication()
    logging.info(f"Test complete — results written to {CSV_FILENAME}")


if __name__ == "__main__":
    test_candy_communication()