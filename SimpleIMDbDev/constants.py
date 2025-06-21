from importlib.metadata import version

BASE_MODULE_NAME = __name__.split(".")[0]
BASE_HEADERS = {
    "User-Agent": f"{BASE_MODULE_NAME} ({version(BASE_MODULE_NAME)})",
    "Accept": "application/json",
}
