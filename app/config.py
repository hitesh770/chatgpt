# Config file
from pydantic import BaseSettings


class Config(BaseSettings):
    host_url: str = 'localhost'
    host_port: int = 8010
    access_log: bool = False
    open_api_token: str = "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"
    url_to_scan :str ="https://jeremyhuss.com/"
    model: str ="gpt-3.5-turbo-16k-0613"