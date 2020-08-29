from h1st_saas.workbench_controller import WorkbenchController


if __name__ == "__main__":
    print("Synching all active deployments ...")
    wc = WorkbenchController()
    l = len(wc.sync())
    print(f"Sync {l} items")
