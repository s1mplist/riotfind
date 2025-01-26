from typing import List, Dict, TypedDict
from enum import Enum


class Scope(str, Enum):
    REGION = "region"
    SERVER = "server"


class RiotServer(str, Enum):
    AMERICAS = "americas"
    ASIA = "asia"
    EUROPE = "europe"
    ESPORTS = "esports"


class RiotRegion(str, Enum):
    BR1 = "BR1"
    EUN1 = "EUN1"
    EUW1 = "EUW1"
    JP1 = "JP1"
    KR = "KR"
    LA1 = "LA1"
    LA2 = "LA2"
    ME1 = "ME1"
    NA1 = "NA1"
    OC1 = "OC1"
    PBE1 = "PBE1"
    PH2 = "PH2"
    RU = "RU"
    SG2 = "SG2"
    TH2 = "TH2"
    TR1 = "TR1"
    VN2 = "VN2"


class RiotGame(str, Enum):
    VALORANT = "val"
    LEGENDS_OF_RUNETERRA = "lor"


class LolQueue(str, Enum):
    RANKED_SOLO_5x5 = "RANKED_SOLO_5x5"
    RANKED_FLEX_SR = "RANKED_FLEX_SR"
    RANKED_FLEX_TT = "RANKED_FLEX_TT"


class LolTier(str, Enum):
    BRONZE = "BRONZE"
    IRON = "IRON"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"
    EMERALD = "EMERALD"
    DIAMOND = "DIAMOND"


class LolDivision(str, Enum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"
    V = "V"


class ParamInfo(TypedDict):
    description: str
    options: List[str]


class ServiceData(TypedDict):
    url: str
    description: str
    is_params_required: bool
    required_params: List[str]


class EndpointGroup(TypedDict):
    scope: Scope
    services: Dict[str, ServiceData]


PARAMS: Dict[str, ParamInfo] = {
    "puuid": {
        "description": "Identificador único do jogador no jogo.",
        "options": [],
    },
    "gameName": {
        "description": "Nome do jogador no jogo.",
        "options": [],
    },
    "tagLine": {
        "description": "Tag do jogador no jogo.",
        "options": [],
    },
    "game": {
        "description": "Nome do jogo (ex: 'val', 'lor').",
        "options": ["val", "lor"],
    },
    "queue": {
        "description": "Tipo de fila no jogo.",
        "options": ["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT"],
    },
    "tier": {
        "description": "Tier do jogador.",
        "options": [
            "BRONZE",
            "IRON",
            "SILVER",
            "GOLD",
            "PLATINUM",
            "EMERALD",
            "DIAMOND",
        ],
    },
    "division": {
        "description": "Divisão do jogador dentro do tier.",
        "options": ["I", "II", "III", "IV", "V"],
    },
    "leagueId": {
        "description": "ID da liga no jogo.",
        "options": [],
    },
    "encryptedSummonerId": {
        "description": "ID criptografado do invocador.",
        "options": [],
    },
}

ENDPOINTS: Dict[str, EndpointGroup] = {
    "ACCOUNT_V1": {
        "scope": Scope.SERVER,
        "services": {
            "get_account_by_riot_id": ServiceData(
                url="/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}",
                description="Busca uma conta usando gameName e tagLine.",
                is_params_required=True,
                required_params=["gameName", "tagLine"],
            ),
            "get_active_shards_by_game_and_puuid": ServiceData(
                url="/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}",
                description="Obtém shards ativos para um jogo usando game e PUUID.",
                is_params_required=True,
                required_params=["game", "puuid"],
            ),
        },
    },
    "LEAGUE_V4": {
        "scope": Scope.REGION,
        "services": {
            "get_challenger_league_by_queue": ServiceData(
                url="/lol/league/v4/challengerleagues/by-queue/{queue}",
                description="Obtém a liga challenger para uma fila específica.",
                is_params_required=True,
                required_params=["queue"],
            ),
            "get_league_entries_by_summoner_id": ServiceData(
                url="/lol/league/v4/entries/by-summoner/{encryptedSummonerId}",
                description="Obtém as entradas de liga para todas as filas para um dado summoner ID.",
                is_params_required=True,
                required_params=["encryptedSummonerId"],
            ),
            "get_league_entries_by_queue_tier_and_division": ServiceData(
                url="/lol/league/v4/entries/{queue}/{tier}/{division}",
                description="Obtém todas as entradas de liga com base na fila, tier e divisão.",
                is_params_required=True,
                required_params=["queue", "tier", "division"],
            ),
            "get_grandmaster_league_by_queue": ServiceData(
                url="/lol/league/v4/grandmasterleagues/by-queue/{queue}",
                description="Obtém a liga grandmaster para uma fila específica.",
                is_params_required=True,
                required_params=["queue"],
            ),
            "get_league_by_id": ServiceData(
                url="/lol/league/v4/leagues/{leagueId}",
                description="Obtém os dados de uma liga com um ID específico, incluindo entradas inativas.",
                is_params_required=True,
                required_params=["leagueId"],
            ),
            "get_master_league_by_queue": ServiceData(
                url="/lol/league/v4/masterleagues/by-queue/{queue}",
                description="Obtém a liga master para uma fila específica.",
                is_params_required=True,
                required_params=["queue"],
            ),
        },
    },
    "STATUS_V4": {
        "scope": Scope.REGION,
        "services": {
            "get_league_of_legends_platform_data": ServiceData(
                url="/lol/status/v4/platform-data",
                description="Obtém o status da plataforma de League of Legends para a plataforma especificada.",
                is_params_required=False,
                required_params=[],
            )
        },
    },
}
