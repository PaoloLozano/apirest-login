-- ============================================
-- SCRIPT DE MIGRACION A POSTGRESQL
-- ============================================

-- Crear extension UUID (opcional, recomendado para IDs)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- TABLA: usuarios
-- ============================================
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL,
    edad INTEGER,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(50) DEFAULT 'user'
);

-- ============================================
-- INDICES
-- ============================================
CREATE INDEX IF NOT EXISTS idx_usuarios_id ON usuarios(id);

-- ============================================
-- COMENTARIOS (opcional, documentacion)
-- ============================================
COMMENT ON TABLE usuarios IS 'Tabla de usuarios del sistema';
COMMENT ON COLUMN usuarios.id IS 'Identificador unico del usuario';
COMMENT ON COLUMN usuarios.nombre IS 'Nombre de usuario (unico)';
COMMENT ON COLUMN usuarios.edad IS 'Edad del usuario';
COMMENT ON COLUMN usuarios.email IS 'Correo electronico (unico)';
COMMENT ON COLUMN usuarios.password IS 'Contrasena hasheada';
COMMENT ON COLUMN usuarios.rol IS 'Rol del usuario (default: user)';
