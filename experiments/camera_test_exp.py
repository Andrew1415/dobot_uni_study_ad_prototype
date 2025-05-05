import sys
from pathlib import Path
import csv
import logging
from datetime import datetime

script_dir   = Path(__file__).resolve().parent    # experiments/
project_root = script_dir.parent                  # parent of experiments/ and src/
sys.path.insert(0, str(project_root / "src"))

from camera_capture import find_candy

CSV_FILENAME = "candy_location_finding_test.csv"
ITERATIONS   = 100
X_MAX = 1


def test_candy_location():
    # 1) configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

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

        # 4) loops: each (x) for ITERATIONS times
        for iteration in range(1, ITERATIONS + 1):
            for x in range(0, X_MAX + 1):
                cmd = x

                dt_send = datetime.now()
                success = find_candy(cmd)   # blocks until done
                dt_resp = datetime.now()

                duration_td = dt_resp - dt_send

                t_send     = dt_send.isoformat(timespec="milliseconds")
                t_resp     = dt_resp.isoformat(timespec="milliseconds")

                if success != None :
                    best_place = success
                    success = True
                elif success == None:
                    best_place = None
                    success = False

                if x == 0:
                    x = "Yellow"
                elif x == 1:
                    x = "Red"

                duration_s = duration_td.total_seconds()  # duration in seconds (float)
                writer.writerow([
                    iteration,
                    x,
                    t_send,
                    t_resp,
                    duration_s,
                    best_place,
                    success
                ])

                    # small pause to avoid overwhelming the robot
                    #time.sleep(0.01)

    logging.info(f"Test complete — results written to {CSV_FILENAME}")


if __name__ == "__main__":
    test_candy_location()