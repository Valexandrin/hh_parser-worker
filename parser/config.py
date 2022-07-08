import os

from pydantic import BaseModel


class Source(BaseModel):
    url: str


class Endpoint(BaseModel):
    url: str


class AppConfig(BaseModel):
    source: Source
    endpoint: Endpoint


def load_from_env() -> AppConfig:
    source = os.environ['SOURCE']
    endpoint = os.environ['ENDPOINT']

    return AppConfig(
        source=Source(url=source),
        endpoint=Endpoint(url=endpoint),
    )


config = load_from_env()
