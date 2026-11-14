"""Leest de instellingen uit het .env-bestand."""

from environs import Env

env = Env()
env.read_env()

DB_PATH = env.str("DB_PATH")
RAPPORT_MAP = env.str("RAPPORT_MAP", "rapporten")
