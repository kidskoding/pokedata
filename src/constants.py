STAT_COLS = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]

ALL_TYPES = [
    "normal", "fire", "water", "electric", "grass", "ice",
    "fighting", "poison", "ground", "flying", "psychic", "bug",
    "rock", "ghost", "dragon", "dark", "steel", "fairy"
]

TYPE_COLORS = {
    "normal":   "#A8A878", "fire":     "#F08030", "water":    "#6890F0",
    "electric": "#F8D030", "grass":    "#78C850", "ice":      "#98D8D8",
    "fighting": "#C03028", "poison":   "#A040A0", "ground":   "#E0C068",
    "flying":   "#A890F0", "psychic":  "#F85888", "bug":      "#A8B820",
    "rock":     "#B8A038", "ghost":    "#705898", "dragon":   "#7038F8",
    "dark":     "#705848", "steel":    "#B8B8D0", "fairy":    "#EE99AC",
}

VALID_MULTIPLIERS = {0.0, 0.25, 0.5, 1.0, 2.0, 4.0}

SPEED_TIERS = {
    "slow":  (0, 49),
    "mid":   (50, 79),
    "fast":  (80, 109),
    "ultra": (110, 999),
}

POKEAPI_BASE = "https://pokeapi.co/api/v2"

POKEAPI_ENDPOINTS = {
    "pokemon": {"url": f"{POKEAPI_BASE}/pokemon", "count": 1025},
    "pokemon-species": {"url": f"{POKEAPI_BASE}/pokemon-species", "count": 1025},
    "pokemon-form": {"url": f"{POKEAPI_BASE}/pokemon-form", "count": 1500},
    "move": {"url": f"{POKEAPI_BASE}/move", "count": 920},
    "ability": {"url": f"{POKEAPI_BASE}/ability", "count": 298},
    "type": {"url": f"{POKEAPI_BASE}/type", "count": 18},
    "evolution-chain": {"url": f"{POKEAPI_BASE}/evolution-chain", "count": 541},
    "item": {"url": f"{POKEAPI_BASE}/item", "count": 2050},
    "location": {"url": f"{POKEAPI_BASE}/location", "count": 850},
    "location-area": {"url": f"{POKEAPI_BASE}/location-area", "count": 1000},
    "berry": {"url": f"{POKEAPI_BASE}/berry", "count": 64},
    "nature": {"url": f"{POKEAPI_BASE}/nature", "count": 25},
    "egg-group": {"url": f"{POKEAPI_BASE}/egg-group", "count": 15},
    "growth-rate": {"url": f"{POKEAPI_BASE}/growth-rate", "count": 6},
    "generation": {"url": f"{POKEAPI_BASE}/generation", "count": 9},
    "stat": {"url": f"{POKEAPI_BASE}/stat", "count": 8},
    "pokedex": {"url": f"{POKEAPI_BASE}/pokedex", "count": 30},
}