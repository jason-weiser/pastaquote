from pathlib import Path
import logging
import yaml

log = logging.getLogger(__name__)
_config_path = None

def set_config_path(path):
    global _config_path
    _config_path = Path(path).expanduser().resolve()

def config_path():
    if _config_path is None:
        raise RuntimeError("No config path set. Call set_config_path() first")
    return _config_path

def data_dir():
    d = config_path().parent / "data"
    d.mkdir(parents=True, exist_ok=True)
    return d

def pull_config(section):
    with open(config_path()) as config_yml:
        config = yaml.safe_load(config_yml)
    return config[section]

def platform_config():
    try:
        platforms = pull_config('PLATFORMS')
    except KeyError:
        msg = "Attempting to use old config. Please update config to new format, as this will likely break with future updates."
        print(msg)
        log.info(msg)
        platforms = None
    return platforms

def get_platform_creds(platform):
    cred = platform_config().get(platform)
    if cred is None:
        log.info("%s not present in config. Skipping")
    return cred