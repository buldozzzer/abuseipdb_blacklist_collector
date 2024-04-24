import clickhouse_connect
import logging


class ClickHouseClient:
    __table: str = "blacklist"

    def __init__(
        self,
        host: str,
        username: str,
        password: str = "",
        port: int = 8123,
        db: str = "default",
    ) -> None:
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__db = db

        self.__client = clickhouse_connect.get_client(
            host=self.__host,
            port=self.__port,
            username=self.__username,
            password=self.__password,
        )

        self.init_table()

    def __del__(self):
        self.__client.close()

    def init_table(self):
        self.__client.command(
            """CREATE TABLE IF NOT EXISTS {}.{} 
            (
                ipAddress UInt64 NOT NULL, 
                countryCode String, 
                abuseConfidenceScore UInt8, 
                lastReportedAt DateTime('Europe/London')
            )
            ENGINE = ReplacingMergeTree ORDER BY ipAddress
            """.format(
                self.__db, self.__table
            )
        )

    def drop_table(self):
        self.__client.command(
            "DROP TABLE IF EXISTS {}.{}".format(self.__db, self.__table)
        )

    def insert(self, rows: list):
        written_rows = self.__client.insert(
            table=self.__table,
            data=rows,
            column_names=[
                "ipAddress",
                "countryCode",
                "abuseConfidenceScore",
                "lastReportedAt",
            ],
        ).written_rows
        logging.debug(f"Inserted {len(rows)} row(s)")
