import os
from pathlib import Path
from git import Repo
from datetime import datetime, date
from collections import OrderedDict



def get_creation_time(path : Path) -> str:
    return datetime.fromtimestamp(path.stat().st_ctime).strftime("%Y-%m-%d")

def get_modification_time(path : Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")


def generate_date_to_files_change_dictionary(repo, base_path) -> OrderedDict:
    changesDict = OrderedDict()
    untracked = repo.untracked_files
    untracked_changes = list()
    for file in untracked:
        path = Path(file)
        creation_time = get_creation_time(base_path / path)
        print(f"{path} created at {creation_time}")
        untracked_changes.append({"date": creation_time, "path": file})


    tracked_changes = list()
    deleted = list()
    changed = [item for item in repo.index.diff(None)]
    for change in changed:
        a_path = change.a_path
        if not change.deleted_file:
            path = Path(a_path)
            modification_time = get_modification_time(base_path / path)
            print(f"{path} modified at {modification_time}")
            tracked_changes.append({"date": modification_time, "path": a_path})
        else:
            deleted.append(a_path)

    to_stage_changes = tracked_changes + untracked_changes
    to_stage_changes.sort(key=lambda x: x["date"])

    if len(to_stage_changes) == 0:
        print("There are no changes to anchor deletions, using current time")
    else:
        first_element = to_stage_changes[0]
        date = first_element["date"]
        for delete in deleted:
            to_stage_changes = [{"date": date, "path": delete}] + to_stage_changes
        

    for change in to_stage_changes:
        if changesDict.get(change["date"]) is None:
            changesDict[change["date"]] = set()

        changesDict[change["date"]].add(change["path"])
        
                
    print(f"{len(tracked_changes)} files changed")
    print(f"{len(untracked_changes)} files untracked")
    print(f"{len(deleted)} files deleted")
    return changesDict

def commit_changes(repo, changesDict: OrderedDict):
    for date, changed_files in changesDict.items():
        repo.index.add(list(changed_files))
        os.environ["GIT_AUTHOR_DATE"] = datetime.fromisoformat(date).isoformat()
        os.environ["GIT_COMMITTER_DATE"] = datetime.fromisoformat(date).isoformat()
        print(f"Committing {len(changed_files)} files at {datetime.fromisoformat(date).isoformat()} ")
        repo.index.commit("Update")


base_path = Path(os.getcwd())
repo = Repo(os.getcwd())
changesDict = generate_date_to_files_change_dictionary(repo, base_path)
commit_changes(repo, changesDict)
