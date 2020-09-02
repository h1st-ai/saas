from h1st_saas.workbench_controller import WorkbenchController

import sys
import logging
import time

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger('worker')

if __name__ == "__main__":
    wc = WorkbenchController()
    while True:
        l = len(wc.sync())
        # logger.info(f"Sync {l} items")
        time.sleep(5)
