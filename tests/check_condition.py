"""Exercise the actual role condition with Ansible's strict evaluator."""
import pathlib
import subprocess
import tempfile

import yaml

root = pathlib.Path(__file__).resolve().parents[1]
condition = yaml.safe_load((root / "tasks/configure.yml").read_text())[0]["when"]
plays = []
for managed, host, expected in [
    (True, "logs.example.com", True),
    (True, "", False),
    (False, "logs.example.com", False),
    (False, "", False),
]:
    plays.append({
        "name": f"managed={managed}, host={host!r}",
        "hosts": "localhost",
        "gather_facts": False,
        "vars": {
            "papertrail_managed_conf_file": managed,
            "papertrail_destination_host": host,
        },
        "tasks": [
            {"ansible.builtin.debug": {"msg": "configure"},
             "when": condition, "register": "result"},
            {"ansible.builtin.assert": {
                "that": ["result is not skipped" if expected else "result is skipped"]}},
        ],
    })
with tempfile.TemporaryDirectory() as directory:
    playbook = pathlib.Path(directory) / "condition.yml"
    playbook.write_text(yaml.safe_dump(plays))
    subprocess.run(["ansible-playbook", "-i", "localhost,", "-c", "local", str(playbook)], check=True)
