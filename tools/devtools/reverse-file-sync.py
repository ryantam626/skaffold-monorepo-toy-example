import dataclasses
import json
import argparse
import shutil
import subprocess
from typing import Any, Dict, List

BLUE = "\033[1;34;48m"
GREEN = "\033[1;32;48m"
YELLOW = "\033[1;33;48m"
END = "\033[1;37;0m"


def success(line: str):
    print(f"{GREEN}{line}{END}")


def info(line: str):
    print(f"{BLUE}{line}{END}")


def warning(line: str):
    print(f"{YELLOW}{line}{END}")


def read_devtools_json(filepath: str) -> Dict[str, Any]:
    with open(filepath, "r") as fd:
        devtools_json = json.load(fd)
    return devtools_json


@dataclasses.dataclass
class ReverseFileSyncSpec:
    src: str
    dst: str
    when_changed: bool

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReverseFileSyncSpec":
        return ReverseFileSyncSpec(
            src=d["src"],
            dst=d["dst"],
            when_changed=d.get("whenChanged", False),
        )


def read_reverse_file_sync_spec(
    devtools_json: Dict[str, Any]
) -> List[ReverseFileSyncSpec]:
    return [
        ReverseFileSyncSpec.from_dict(item)
        for item in devtools_json["skaffold"]["reverseFileSync"]
    ]


def get_pod_name(devtools_json: Dict[str, Any]) -> str:
    pod_pattern: str = devtools_json["podPattern"]
    kubectl_get_pod_proc = subprocess.Popen(
        ["kubectl", "get", "pod"], stdout=subprocess.PIPE
    )
    egrep_proc = subprocess.check_output(
        ["egrep", f"{pod_pattern}.*Running"], stdin=kubectl_get_pod_proc.stdout
    )
    pods = egrep_proc.splitlines()
    if len(pods) != 1:
        raise RuntimeError("Can't find exactly one pod to reverse file mount...")

    [pod] = pods
    pod_name, *_ = pod.decode().split(" ")
    return pod_name


def reverse_file_sync_always(
    pod_name: str, spec: ReverseFileSyncSpec, base_dir: str
) -> None:
    cp_src = f"{pod_name}:{spec.src}"
    cp_dst = f"{base_dir}/{spec.dst}"

    info(f"Copying {cp_src} to {cp_dst}")

    proc = subprocess.Popen(["kubectl", "cp", cp_src, cp_dst], stdout=subprocess.PIPE)
    proc.communicate()
    if proc.returncode:
        raise RuntimeError(f"Failed when copying {cp_src} to {cp_dst}")


def revese_file_sync_if_required(
    pod_name: str, spec: ReverseFileSyncSpec, base_dir: str
) -> None:
    cp_src = f"{pod_name}:{spec.src}"
    tmp_cp_dst = f"/tmp/{base_dir}/{spec.dst}"
    repo_cp_dst = f"/tmp/{base_dir}/{spec.dst}"

    info(f"Copying {cp_src} to {tmp_cp_dst} to check for changes")

    proc = subprocess.Popen(
        ["kubectl", "cp", cp_src, tmp_cp_dst], stdout=subprocess.PIPE
    )
    proc.communicate()
    if proc.returncode:
        raise RuntimeError(f"Failed when copying {cp_src} to {tmp_cp_dst}")

    require_sync = False
    try:
        # TODO: Implement something for comparing dirs, I have no use case for this so skipping for now.
        with open(tmp_cp_dst, "r") as tmp, open(repo_cp_dst, "r") as repo:
            if tmp.read() != repo.read():
                require_sync = True
    except Exception:
        info(
            f"Could not check for difference between {tmp_cp_dst} and {repo_cp_dst}, syncing regardless."
        )
        require_sync = True

    if require_sync:
        success(f"Copying from {tmp_cp_dst} to {repo_cp_dst}")
        shutil.copyfile(tmp_cp_dst, repo_cp_dst)
    else:
        success(f"Skipping copy from {tmp_cp_dst} to {repo_cp_dst}")


def reverse_file_sync(
    pod_name: str, specs: List[ReverseFileSyncSpec], base_dir: str
) -> None:
    for spec in specs:
        if not spec.when_changed:
            reverse_file_sync_always(pod_name, spec, base_dir)
        else:
            revese_file_sync_if_required(pod_name, spec, base_dir)


def main():
    parser = argparse.ArgumentParser(description="Reverse file sync")
    parser.add_argument("--devtools-json", help="Where the devtools.json is located")
    parser.add_argument("--base-dir", help="Repo root absolute path")
    args = parser.parse_args()

    devtools_json = read_devtools_json(args.devtools_json)

    pod_name = get_pod_name(devtools_json)
    reverse_file_sync_spec = read_reverse_file_sync_spec(devtools_json)

    reverse_file_sync(pod_name, reverse_file_sync_spec, args.base_dir)


if __name__ == "__main__":
    main()
