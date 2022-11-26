import random
import shlex
import string
import subprocess


def run_cmd(cmd: str) -> str:
    return subprocess.check_output(
        shlex.split(cmd), encoding="utf-8", stderr=subprocess.STDOUT
    )


def make_random_string(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def test_cli_integration_basic():
    username_1 = make_random_string()
    username_2 = make_random_string()

    storage_path = make_random_string()
    assert "not found" in run_cmd(
        f"user-manager get {username_1} --storage-path {storage_path}"
    )

    run_cmd(f"user-manager set {username_1} --storage-path {storage_path} --address city1")
    assert "city1" in run_cmd(
        f"user-manager get {username_1} --storage-path {storage_path}"
    )

    run_cmd(f"user-manager set {username_1} work --storage-path {storage_path} --address city2")
    assert "city2" in run_cmd(
        f"user-manager get {username_1} work --storage-path {storage_path}"
    )

    run_cmd(f"user-manager set {username_2} --storage-path {storage_path} --phone-number +123")
    assert "+123" in run_cmd(
        f"user-manager get {username_2} --storage-path {storage_path}"
    )
