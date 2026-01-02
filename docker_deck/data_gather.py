import json
import re
from subprocess import run

from docker_deck.models import Service, ServiceState


def get_running_containers():
    # COMMAND = ["docker", "ps", "--format", "{{.Image}}-{{.Names}}-{{.Status}}-{{.Ports}}"]
    COMMAND = ["docker", "ps", "-a", "--format", "json"]

    output = run(COMMAND, capture_output=True, text=True, check=False)

    if output.returncode != 0:
        pass

    running = parse_docker_ps_output(output.stdout)
    return running


def parse_docker_ps_output(output: str) -> list[Service]:
    lines = output.strip().split("\n")
    containers = [json.loads(line) for line in lines if line]
    services = [build_service_from_container(container) for container in containers]

    return services


def build_service_from_container(container: dict) -> Service:
    return Service(
        container_name=container["Names"],
        state=ServiceState.RUNNING if container["State"] == "running" else ServiceState.STOPPED,
        port=parse_ports(container["Ports"]),
        image=container["Image"],
    )


def parse_ports(ports_str: str) -> int:
    pattern = r"(\d+)->"
    result = re.search(pattern, ports_str)

    match result:
        case re.Match():
            port = int(result.group(1))
            return port
        case None:
            return -1
