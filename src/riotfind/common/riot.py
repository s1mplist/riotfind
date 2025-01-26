import os
import logging
import requests
import urllib.parse

from typing import Dict, Optional
from .utils.riot_types import (
    Scope,
    RiotServer,
    RiotRegion,
    PARAMS,
    ENDPOINTS,
    ServiceData,
)

# Configurando o logger
logger = logging.getLogger(__name__)


class RiotCaller:
    def __init__(self, server: RiotServer = RiotServer.AMERICAS, region: RiotRegion = RiotRegion.BR1):
        """Inicializa a classe RiotCaller com servidor, região e configurações de endpoints."""

        if not isinstance(server, RiotServer):
            raise ValueError(f"Invalid server: {server}")
        if not isinstance(region, RiotRegion):
            raise ValueError(f"Invalid region: {region}")

        self.server = server.value
        self.region = region.value

        self.server_url: str = f"https://{self.server}.api.riotgames.com"
        self.region_url: str = f"https://{self.region}.api.riotgames.com"

        # Obtém a chave da API
        self.api_key = os.environ.get("RIOT_API_KEY")
        if not self.api_key:
            logger.warning(
                "API Key is not set. Ensure that 'RIOT_API_KEY' is in your environment variables."
            )
    
    def _get_base_url(self, scope: Scope) -> str:
        """Retorna a URL base correta de acordo com o escopo."""
        if scope == "server":
            return self.server_url
        elif scope == "region":
            return self.region_url
        else:
            raise ValueError(f"Unknown scope '{scope}'.")
        
    def _validate_service_params(self, service_data: ServiceData, params: Dict):
        """Valida os parâmetros fornecidos contra os obrigatórios e os valores válidos."""
        
        if service_data["is_params_required"]:
            required_params = service_data["required_params"]
            missing_params = [param for param in required_params if param not in params]
            if missing_params:
                raise ValueError(
                    f"Missing required parameters: {', '.join(missing_params)}"
                )

        for param, value in params.items():
            if param in PARAMS:
                param_info = PARAMS[param]
                if param_info["options"] and value not in param_info["options"]:
                    raise ValueError(f"Invalid value for parameter '{param}': {value}")
    
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
            # Busca o serviço no ENDPOINTS
            for endpoint_group, endpoint_data in ENDPOINTS.items():
                service_data = endpoint_data["services"].get(service_name)
                if service_data:
                    break
            else:
                raise ValueError(
                    f"Service '{service_name}' not found in configuration."
                )

            # Valida os parâmetros fornecidos usando a nova função
            params = params or {}
            self._validate_service_params(service_data, params)

            # Monta a URL base e completa com os parâmetros fornecidos
            base_url = self._get_base_url(endpoint_data["scope"])
            endpoint_url = service_data["url"].format(**params)
            full_url = urllib.parse.urljoin(base_url, endpoint_url)

            # Faz a requisição
            return self._make_request(full_url)

        except Exception as e:
            logger.error(f"Error calling service '{service_name}': {e}")
            raise