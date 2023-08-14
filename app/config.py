# Config file
from pydantic import BaseSettings


class Config(BaseSettings):
    host_url: str = 'localhost'
    host_port: int = 8010
    access_log: bool = False
    open_api_token: str = ""
    model: str ="gpt-3.5-turbo-16k-0613"