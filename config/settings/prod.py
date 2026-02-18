from os import getenv, path

from dotenv import load_dotenv

from .base import *  # noqa

# load local environment variables
local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(dotenv_path=local_env_file)

SECRET_KEY = getenv("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = []

ADMINS = [
    ("Shadaab Karim", "karimshadaab510@gmail.com"),
]
