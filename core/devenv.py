from decouple import Config, RepositoryEnv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
config = Config(RepositoryEnv(BASE_DIR / ".env.dev"))