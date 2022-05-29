import json
import argparse
import subprocess
from typing import Any, Dict

BLUE = "\033[1;34;48m"
END = "\033[1;37;0m"


def info(line: str):
    print(f"{BLUE}{line}{END}")


def read_devtool_json(filepath: str) -> Dict[str, Any]:
    with open(filepath, "r") as fd:
        devtool_json = json.load(fd)
    return devtool_json


def read_reverse_file_sync_spec(devtool_json: Dict[str, Any]) -> Dict[str, str]:
    spec = {}
    skaffold_config = devtool_json["skaffold"]
    for item in skaffold_config["reverseFileSync"]:
        spec[item["src"]] = item["dst"]

    return spec


def get_pod_name(devtool_json: Dict[str, Any]) -> str:
    pod_pattern: str = devtool_json["podPattern"]
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


def reverse_file_sync(pod_name: str, spec: Dict[str, str], base_dir: str) -> None:
    processes = {}
    for src, dst in spec.items():
        cp_src = f"{pod_name}:{src}"
        cp_dst = f"{base_dir}/{dst}"

        info(f"Copying {cp_src} to {cp_dst}")

        processes[cp_src, cp_dst] = subprocess.Popen(
            ["kubectl", "cp", cp_src, cp_dst], stdout=subprocess.PIPE
        )

    for (src, dst), process in processes.items():
        process.communicate()
        if process.returncode:
            raise RuntimeError(f"Failed when copying from {src} to {dst}")


def main():
    parser = argparse.ArgumentParser(description="Reverse file sync")
    parser.add_argument("--devtool-json", help="Where the devtool.json is located")
    parser.add_argument("--base-dir", help="Repo root absolute path")
    args = parser.parse_args()

    devtool_json = read_devtool_json(args.devtool_json)

    pod_name = get_pod_name(devtool_json)
    reverse_file_sync_spec = read_reverse_file_sync_spec(devtool_json)

    reverse_file_sync(pod_name, reverse_file_sync_spec, args.base_dir)


if __name__ == "__main__":
    main()
