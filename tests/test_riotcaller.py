import pytest
import logging

from riotfind.common import RiotCaller

# Set up logging for tests
logging.basicConfig(level=logging.INFO)

def test_riotcaller_init():
    # Test that the class initializes correctly
    riotcaller = RiotCaller()
    assert riotcaller.server == "br1"
    assert riotcaller.region == "americas"
    assert riotcaller.server_url == "https://br1.api.riotgames.com"
    assert riotcaller.region_url == "https://americas.api.riotgames.com"

def test_riotcaller_init_custom_server_region():
    # Test that the class initializes correctly with custom server and region
    riotcaller = RiotCaller(server="eu1", region="europe")
    assert riotcaller.server == "eu1"
    assert riotcaller.region == "europe"
    assert riotcaller.server_url == "https://eu1.api.riotgames.com"
    assert riotcaller.region_url == "https://europe.api.riotgames.com"

def test_riotcaller_load_config():
    # Test that the class loads the config file correctly
    riotcaller = RiotCaller()
    config_data = riotcaller._load_config()
    assert isinstance(config_data, dict)

def test_riotcaller_get_base_url():
    # Test that the class gets the base URL correctly
    riotcaller = RiotCaller()
    base_url = riotcaller._get_base_url("server")
    assert base_url == "https://br1.api.riotgames.com"

def test_riotcaller_get_base_url_region():
    # Test that the class gets the base URL correctly for region scope
    riotcaller = RiotCaller()
    base_url = riotcaller._get_base_url("region")
    assert base_url == "https://americas.api.riotgames.com"

def test_riotcaller_validate_params():
    # Test that the class validates params correctly
    riotcaller = RiotCaller()
    required_params = ["param1", "param2"]
    provided_params = {"param1": "value1", "param2": "value2"}
    riotcaller._validate_params(required_params, provided_params)

def test_riotcaller_validate_params_missing_param():
    # Test that the class raises an error when a param is missing
    riotcaller = RiotCaller()
    required_params = ["param1", "param2"]
    provided_params = {"param1": "value1"}
    with pytest.raises(ValueError):
        riotcaller._validate_params(required_params, provided_params)

def test_riotcaller_call_service():
    # Test that the class calls a service correctly
    riotcaller = RiotCaller()
    service_name = "get_master_league_by_queue"
    params = {"queue": "RANKED_SOLO_5x5"}
    response = riotcaller.call_service(service_name, params)
    assert isinstance(response, dict)