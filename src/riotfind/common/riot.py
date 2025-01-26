import os
import pathlib
import json
import logging
import requests
import urllib.parse
from typing import Dict, Optional

# Configurando o logger
logger = logging.getLogger(__name__)

class RiotCaller:
    def __init__(self, server: str = "br1", region: str = "americas"):
        """Inicializa a classe RiotCaller com servidor, região e configurações de endpoints."""
        
        self.server = server
        self.region = region
        
        self.server_url = f"https://{self.server}.api.riotgames.com"
        self.region_url = f"https://{self.region}.api.riotgames.com"

        # Caminho para o arquivo JSON de configuração
        self.config_file = pathlib.Path(__file__).parent / "utils/endpoints/lol_endpoints.json"

        # Carrega o arquivo de configuração
        self.endpoints_data = self._load_config()

        # Obtém a chave da API
        self.api_key = os.environ.get("RIOT_API_KEY")
        if not self.api_key:
            logger.warning("API Key is not set. Ensure that 'RIOT_API_KEY' is in your environment variables.")

    def _load_config(self) -> Dict:
        """Carrega os dados de configuração do arquivo JSON."""
        try:
            with open(self.config_file, "r") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            logger.error(f"Config file '{self.config_file}' not found.")
            raise
        except json.JSONDecodeError:
            logger.error(f"Error decoding the JSON file '{self.config_file}'.")
            raise

    def _get_base_url(self, scope: str) -> str:
        """Retorna a URL base correta de acordo com o escopo."""
        if scope == "server":
            return self.server_url
        elif scope == "region":
            return self.region_url
        else:
            raise ValueError(f"Unknown scope '{scope}'.")

    def _validate_params(self, required_params: list, provided_params: Dict):
        """Valida os parâmetros fornecidos contra os obrigatórios."""
        missing_params = [param for param in required_params if param not in provided_params]
        if missing_params:
            raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")

    def call_service(self, service_name: str, params: Optional[Dict] = None) -> Dict:
        """
        Interface única para o usuário. Ele apenas fornece o nome do serviço e os parâmetros.
        
        Parâmetros:
            - service_name (str): Nome do serviço que deseja chamar.
            - params (dict): Parâmetros necessários para o serviço.
        
        Retorna:
            - dict: Resposta JSON da API.
        """
        try:
            # Busca o serviço no JSON de configuração
            for scope, scope_data in self.endpoints_data.items():
                service_data = scope_data["services"].get(service_name)
                if service_data:
                    break
            else:
                raise ValueError(f"Service '{service_name}' not found in configuration.")

            # Valida os parâmetros fornecidos
            required_params = service_data["required_params"]
            params = params or {}
            self._validate_params(required_params, params)

            # Monta a URL base e completa com os parâmetros fornecidos
            base_url = self._get_base_url(scope_data["scope"])
            endpoint_url = service_data["url"].format(**params)
            full_url = urllib.parse.urljoin(base_url, endpoint_url)

            # Faz a requisição
            return self._make_request(full_url)

        except Exception as e:
            logger.error(f"Error calling service '{service_name}': {e}")
            raise

    def _make_request(self, url: str) -> Dict:
        """Realiza a requisição HTTP à API Riot e retorna a resposta JSON."""
        try:
            logger.info(f"Making request to {url}")
            response = requests.get(url, params={"api_key": self.api_key})
            response.raise_for_status()
            logger.info(f"Request to {url} succeeded.")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request failed: {url} - {e}")
            raise ValueError(f"Request failed: {url}") from e