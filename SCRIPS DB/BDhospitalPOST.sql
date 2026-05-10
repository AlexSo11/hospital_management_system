-- SCRIPT PARA POSTGRESQL
-- BASE DE DATOS: NÚCLEO DE DIAGNÓSTICO

-- Ejecutar en psql:
-- CREATE DATABASE nucleo_diagnostico;
-- \c nucleo_diagnostico

DROP TABLE IF EXISTS consulta_medicamentos CASCADE;
DROP TABLE IF EXISTS consultas CASCADE;
DROP TABLE IF EXISTS citas CASCADE;
DROP TABLE IF EXISTS medicamentos CASCADE;
DROP TABLE IF EXISTS pacientes CASCADE;
DROP TABLE IF EXISTS doctores CASCADE;
DROP TABLE IF EXISTS empleados CASCADE;
DROP TABLE IF EXISTS administrador CASCADE;

-- TABLA: ADMINISTRADOR
CREATE TABLE IF NOT EXISTS administrador (
    id_admin SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: EMPLEADOS
CREATE TABLE IF NOT EXISTS empleados (
    id_empleado SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(15),
    fecha_nacimiento DATE,
    sexo VARCHAR(10) NOT NULL CHECK (sexo IN ('M', 'F', 'Otro')),
    sueldo NUMERIC(10, 2),
    turno VARCHAR(20) NOT NULL CHECK (turno IN ('Matutino', 'Vespertino', 'Nocturno')),
    contrasena VARCHAR(255) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- TABLA: DOCTORES
CREATE TABLE IF NOT EXISTS doctores (
    id_doctor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(15),
    fecha_nacimiento DATE,
    sexo VARCHAR(10) NOT NULL CHECK (sexo IN ('M', 'F', 'Otro')),
    especialidad VARCHAR(100) NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- TABLA: PACIENTES
CREATE TABLE IF NOT EXISTS pacientes (
    id_paciente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(15),
    fecha_nacimiento DATE NOT NULL,
    sexo VARCHAR(10) NOT NULL CHECK (sexo IN ('M', 'F', 'Otro')),
    edad INTEGER,
    estatura NUMERIC(5, 2),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- TABLA: MEDICAMENTOS
CREATE TABLE IF NOT EXISTS medicamentos (
    id_medicamento SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    via_administracion VARCHAR(50),
    presentacion VARCHAR(100),
    fecha_caducidad DATE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- TABLA: CITAS
CREATE TABLE IF NOT EXISTS citas (
    id_cita SERIAL PRIMARY KEY,
    id_paciente INTEGER NOT NULL,
    id_doctor INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado VARCHAR(20) DEFAULT 'Programada' CHECK (estado IN ('Programada', 'Completada', 'Cancelada')),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE CASCADE,
    FOREIGN KEY (id_doctor) REFERENCES doctores(id_doctor) ON DELETE CASCADE,
    CONSTRAINT chk_hora CHECK (hora >= '09:00:00' AND hora <= '20:00:00')
);

-- TABLA: CONSULTAS
CREATE TABLE IF NOT EXISTS consultas (
    id_consulta SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL,
    diagnostico TEXT NOT NULL,
    observaciones TEXT,
    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita) ON DELETE CASCADE
);

-- TABLA: CONSULTA_MEDICAMENTOS
CREATE TABLE IF NOT EXISTS consulta_medicamentos (
    id_consulta_medicamento SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_medicamento INTEGER NOT NULL,
    dosis VARCHAR(100),
    frecuencia VARCHAR(100),
    duracion VARCHAR(100),
    indicaciones TEXT,
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE CASCADE,
    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento) ON DELETE CASCADE
);

-- ÍNDICES
CREATE INDEX IF NOT EXISTS idx_citas_fecha ON citas(fecha);
CREATE INDEX IF NOT EXISTS idx_citas_doctor ON citas(id_doctor);
CREATE INDEX IF NOT EXISTS idx_citas_paciente ON citas(id_paciente);
CREATE INDEX IF NOT EXISTS idx_consultas_cita ON consultas(id_cita);
CREATE INDEX IF NOT EXISTS idx_pacientes_nombre ON pacientes(nombre);
CREATE INDEX IF NOT EXISTS idx_doctores_especialidad ON doctores(especialidad);

-- DATOS DE PRUEBA
INSERT INTO administrador (usuario, contrasena, nombre) 
VALUES ('admin', 'admin123', 'Administrador Sistema')
ON CONFLICT (usuario) DO NOTHING;
