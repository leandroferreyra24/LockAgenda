CREATE TABLE IF NOT EXISTS perfiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    perfil_id INTEGER NOT NULL,
    activo INTEGER NOT NULL DEFAULT 1,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (perfil_id)
        REFERENCES perfiles(id)
);

CREATE TABLE IF NOT EXISTS empresa (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    razon_social TEXT NOT NULL,
    identificacion_fiscal TEXT,
    direccion TEXT,
    telefono TEXT,
    email TEXT,
    logo TEXT
);