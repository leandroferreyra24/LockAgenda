import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "clave-temporal-solo-para-desarrollo"
    )

    DATABASE = os.path.join(
        BASE_DIR,
        "instance",
        "lockagenda.db"
    )

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads",
        "logos"
    )

    MAX_CONTENT_LENGTH = 2 * 1024 * 1024