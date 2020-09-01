from h1st_saas.workbench_controller import WorkbenchController

import time

if __name__ == "__main__":
    print("Synching all active deployments ...")
    wc = WorkbenchController()
    while True:
        l = len(wc.sync())
        print(f"Sync {l} items")
        time.sleep(5)
