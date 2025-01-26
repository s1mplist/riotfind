RIOT_SERVERS = [
    "americas",
    "asia",
    "europe",
    "esports"
]

RIOT_REGIONS = [
    "BR1",
    "EUN1",
    "EUW1",
    "JP1",
    "KR",
    "LA1",
    "LA2",
    "ME1",
    "NA1",
    "OC1",
    "PBE1",
    "PH2",
    "RU",
    "SG2",
    "TH2",
    "TR1",
    "VN2"
]

PARAMS = {
    "puuid": {
        "description": "Identificador único do jogador no jogo.",

    },
    "gameName": {
        "description": "Nome do jogador no jogo.",

    },
    "tagLine": {
        "description": "Tag do jogador no jogo.",

    },
    "game": {
        "description": "Nome do jogo (ex: 'val', 'lor').",

        "options": ["val", "lor"]  # Valores possíveis para o jogo
    },
    "queue": {
        "description": "Tipo de fila no jogo (ex: 'competitive', 'normal').",

        "options": ["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT"]  # Valores possíveis para fila
    },
    "tier": {
        "description": "Tier do jogador (ex: 'bronze', 'silver', 'gold').",

        "options": ["BRONZE", "IRON", "SILVER", "GOLD", "PLATINUM", "EMERALD", "DIAMOND"]  # Valores possíveis para o tier
    },
    "division": {
        "description": "Divisão do jogador dentro do tier (ex: 'I', 'II', 'III').",

        "options": ["I", "II", "III", "IV", "V"]  # Valores possíveis para divisão
    },
    "leagueId": {
        "description": "ID da liga no jogo."

    },
    "encryptedSummonerId": {
        "description": "ID criptografado do invocador."

    }
}
