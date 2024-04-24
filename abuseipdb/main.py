import configparser
import ipaddress
import logging
import random
import time
import json
import os
from celery import Celery
from celery.schedules import crontab
from datetime import datetime
from abuseipdb.clickhouse_client import ClickHouseClient
from abuseipdb.abuseipdb_wrapper import AbuseIPDB


redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = os.environ.get("REDIS_PORT", 6379)

app = Celery(
	"abuseipdb",
	backend=f"redis://{redis_host}:{redis_port}/1",
	broker=f"redis://{redis_host}:{redis_port}/0",
)


def get_tokens(config: configparser.ConfigParser) -> tuple:
    return len(config["abuseipdb"]), [value for value in config["abuseipdb"].values()]


def get_interval(token_count) -> int:
    return int(round(86400 / (token_count * 5), 0))


def prepare_data(raw_data: list) -> list:
    data = []
    for item in raw_data:
        if item["ipAddress"] is None:
            print(item)
        try:
            data.append(
                [
                    int(ipaddress.IPv4Address(item["ipAddress"])),
                    item["countryCode"],
                    item["abuseConfidenceScore"],
                    datetime.strptime(item["lastReportedAt"], "%Y-%m-%dT%H:%M:%S%z"),
                ]
            )

        except Exception:
            continue
    return data


def get_black_list(tokens: list, host: str, username: str) -> None:
    try:
        for i in range(50):
            token = random.choice(tokens)

            abuse_ip_db_client = AbuseIPDB(token)

            response = abuse_ip_db_client.get_black_list()

            if response.status_code == 200:
                logging.debug(f"Success response received. Token: {token}")

                rows = prepare_data(json.loads(response.text)["data"])

                client = ClickHouseClient(host=host, username=username)

                client.insert(rows)

                del client

            else:
                logging.debug(f"Request limit exceeded. Token: {token}")
    except Exception as ex:
        logging.error(ex)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, main.s())

@app.task
def main():
    config = configparser.ConfigParser()
    config.read(os.environ.get("ABUSE_CONFIG_FILE", "config.ini"))

    token_count, tokens = get_tokens(config)

    logging.basicConfig(
        format="%(name)s %(asctime)s %(levelname)s %(message)s",
        level=logging.getLevelName(config["logging"]["level"]),
    )

    logging.info("Serivce started...")

    get_black_list(
        tokens=tokens,
        host=config["clickhouse"]["host"],
        username=config["clickhouse"]["username"],
    )
