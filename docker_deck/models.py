from enum import Enum

from pydantic import BaseModel


class ServiceState(Enum):
    RUNNING = "running"
    STOPPED = "stopped"


class Service(BaseModel):
    container_name: str
    state: ServiceState
    port: int
    image: str
