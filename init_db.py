import sqlite3
import os

from config import Config
from werkzeug.security import generate_password_hash


def init_db(database_path=None):

    db_path = database_path or Config.DATABASE

    os.makedirs(
        os.path.dirname(db_path),
        exist_ok=True
    )

    connection = sqlite3.connect(db_path)

    connection.execute("PRAGMA foreign_keys = ON")

    with open("schema.sql", "r", encoding="utf-8") as file:

        connection.executescript(file.read())

    connection.execute("""
        INSERT OR IGNORE INTO perfiles
        (nombre, descripcion)
        VALUES
        ('Administrador', 'Acceso administrativo'),
        ('Tecnico', 'Perfil de técnico'),
        ('Encargado', 'Perfil de encargado')
    """)

    password_hash = generate_password_hash("Admin123!")

    connection.execute("""
        INSERT OR IGNORE INTO usuarios
        (nombre, email, password_hash, perfil_id)
        VALUES (?, ?, ?, ?)
    """, (
        "Administrador",
        "admin@lockagenda.local",
        password_hash,
        1
    ))

    connection.commit()

    connection.close()

    print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    init_db()