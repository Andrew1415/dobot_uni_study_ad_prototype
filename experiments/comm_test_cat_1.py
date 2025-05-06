import sys
from pathlib import Path
import csv
import logging
import time
from datetime import datetime
import threading

script_dir   = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root / "src"))

from communication_tcp import (
    setup_communication,
    request_candy,
    close_communication,
    RESPONSE_SUCCESS
)

CSV_FILENAME = "candy_robot_communication_test.csv"
ITERATIONS   = 10
ROW_MAX, COLUMN_MAX = 3, 5


def request_cat_1_sync(cmd: str) -> bool:

    done = threading.Event()
    result = {"ok": False}

    def _callback(response_code: int):
        result["ok"] = (response_code == RESPONSE_SUCCESS)
        done.set()

    request_candy(cmd, _callback)

    done.wait()
    return result["ok"]


def test_cat_1_communication():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

    setup_communication()

    with open(CSV_FILENAME, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "iteration",
            "row",
            "column",
            "send_timestamp",
            "response_timestamp",
            "duration",
            "success"
        ])

        for iteration in range(1, ITERATIONS + 1):
            for row in range(0, ROW_MAX + 1):
                for column in range(0, COLUMN_MAX + 1):
                    cmd = f"{row},{column}"

                    dt_send = datetime.now()
                    success = request_cat_1_sync(cmd)   
                    dt_resp = datetime.now()

                    duration_td = dt_resp - dt_send

                    t_send     = dt_send.isoformat(timespec="milliseconds")
                    t_resp     = dt_resp.isoformat(timespec="milliseconds")
                    duration_s = duration_td.total_seconds()  
                    writer.writerow([
                        iteration,
                        row,
                        column,
                        t_send,
                        t_resp,
                        duration_s,
                        success
                    ])

                    time.sleep(0.01)

    close_communication()
    logging.info(f"Test complete — results written to {CSV_FILENAME}")


if __name__ == "__main__":
    test_cat_1_communication()