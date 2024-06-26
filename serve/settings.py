import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    postgres_user = os.environ.get("POSTGRES_USER")
    postgres_password = os.environ.get("POSTGRES_PASSWORD")
    postgres_hostname = os.environ.get("POSTGRES_HOSTNAME")
    postgres_db = os.environ.get("POSTGRES_DB")
    postgres_port = os.environ.get("POSTGRES_PORT")

    db_url = (
            "postgresql://"
            + postgres_user
            + ":"
            + postgres_password
            + "@"
            + postgres_hostname
            + ":"
            + postgres_port
            + "/"
            + postgres_db
    )

    mep_list_source: str = "https://www.europarl.europa.eu/meps/en/full-list/xml"
    outgoing_mep_list_source: str = "https://www.europarl.europa.eu/meps/en/incoming-outgoing/outgoing/xml"


settings = Settings()
