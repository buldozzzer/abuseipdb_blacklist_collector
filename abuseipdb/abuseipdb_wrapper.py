import requests


class AbuseIPDB:
    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key

    def get_black_list(self, **kwargs) -> requests.Response:
        r"""
        :Keyword-аргументы:
        * *limit* (``int``) --
          ограничение числа ip-адресов в ответе (по умолчанию 10000)
        * *confidence_minimum* (``int``) --
          минимальная оценка того, на сколько "грязными" являются ip-адреса,
          от 25 до 100 (по умолчанию 100)
        * *ip_version* (``int``) --
          версия IP (4 или 6)
        * *except_countries* (``str``) --
          список кодов стран ISO 3166 alpha-2 (например, "RU,MX,CA")
        * *only_countries* (``str``) --
          список кодов стран ISO 3166 alpha-2 (например, "RU,MX,CA")
        """

        url = "https://api.abuseipdb.com/api/v2/blacklist"

        querystring = {
            "limit": "{}".format(kwargs.get("limit", 10000)),
            "confidenceMinimum": "{}".format(kwargs.get("confidence_minimum", 100)),
            "ipVersion": kwargs.get("ip_version", None),
            "exceptCountries": kwargs.get("except_countries", None),
            "onlyCountries": kwargs.get("only_countries", None),
        }

        headers = {
            "Accept": "application/json",
            "Key": self.__api_key,
        }

        response = requests.get(url=url, headers=headers, params=querystring)

        return response

    def check_ip(self, **kwargs) -> requests.Response:
        r"""
        :Keyword-аргументы:
        * *ip* (``str``) --
          целевой ip-адрес
        * *max_age_in_days* (``int``) --
          число дней с момента запроса, за которое предоставятся отчет (по умолчанию 30, максимально 365)
        * *verbose* (``bool``) --
          запрос подробного отчета (по умолчанию False)
        """

        url = "https://api.abuseipdb.com/api/v2/check"

        querystring = {
            "ipAddress": kwargs.get("ip"),
            "maxAgeInDays": kwargs.get("max_age_in_days", 30),
        }

        verbose = kwargs.get("verbose", False)

        if verbose:
            querystring["verbose"] = verbose

        headers = {"Accept": "application/json", "Key": self.__api_key}

        response = requests.get(url=url, headers=headers, params=querystring)

        return response
