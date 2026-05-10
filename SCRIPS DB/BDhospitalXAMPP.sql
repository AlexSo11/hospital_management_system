-- SCRIPT PARA MYSQL / XAMPP
-- BASE DE DATOS: NÚCLEO DE DIAGNÓSTICO

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS nucleo_diagnostico CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE nucleo_diagnostico;

-- Eliminar tablas en orden inverso a sus dependencias
DROP TABLE IF EXISTS consulta_medicamentos;
DROP TABLE IF EXISTS consultas;
DROP TABLE IF EXISTS citas;
DROP TABLE IF EXISTS medicamentos;
DROP TABLE IF EXISTS pacientes;
DROP TABLE IF EXISTS doctores;
DROP TABLE IF EXISTS empleados;
DROP TABLE IF EXISTS administrador;

-- TABLA: ADMINISTRADOR
CREATE TABLE IF NOT EXISTS administrador (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- TABLA: EMPLEADOS
CREATE TABLE IF NOT EXISTS empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(15),
    fecha_nacimiento DATE,
    sexo ENUM('M', 'F', 'Otro') NOT NULL,
    sueldo DECIMAL(10, 2),
    turno ENUM('Matutino', 'Vespertino', 'Nocturno') NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo TINYINT(1) DEFAULT 1
) ENGINE=InnoDB;

-- TABLA: DOCTORES
CREATE TABLE IF NOT EXISTS doctores (
    id_doctor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(15),
    fecha_nacimiento DATE,
    sexo ENUM('M', 'F', 'Otro') NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo TINYINT(1) DEFAULT 1
) ENGINE=InnoDB;

-- TABLA: PACIENTES
CREATE TABLE IF NOT EXISTS pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(15),
    fecha_nacimiento DATE NOT NULL,
    sexo ENUM('M', 'F', 'Otro') NOT NULL,
    edad INT,
    estatura DECIMAL(5, 2),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo TINYINT(1) DEFAULT 1
) ENGINE=InnoDB;

-- TABLA: MEDICAMENTOS
CREATE TABLE IF NOT EXISTS medicamentos (
    id_medicamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    via_administracion VARCHAR(50),
    presentacion VARCHAR(100),
    fecha_caducidad DATE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo TINYINT(1) DEFAULT 1
) ENGINE=InnoDB;

-- TABLA: CITAS
CREATE TABLE IF NOT EXISTS citas (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_doctor INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado ENUM('Programada', 'Completada', 'Cancelada') DEFAULT 'Programada',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_hora CHECK (hora >= '09:00:00' AND hora <= '20:00:00'),
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_doctor) REFERENCES doctores(id_doctor) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- TABLA: CONSULTAS
CREATE TABLE IF NOT EXISTS consultas (
    id_consulta INT AUTO_INCREMENT PRIMARY KEY,
    id_cita INT NOT NULL,
    diagnostico TEXT NOT NULL,
    observaciones TEXT,
    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- TABLA: CONSULTA_MEDICAMENTOS
CREATE TABLE IF NOT EXISTS consulta_medicamentos (
    id_consulta_medicamento INT AUTO_INCREMENT PRIMARY KEY,
    id_consulta INT NOT NULL,
    id_medicamento INT NOT NULL,
    dosis VARCHAR(100),
    frecuencia VARCHAR(100),
    duracion VARCHAR(100),
    indicaciones TEXT,
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ÍNDICES
CREATE INDEX idx_citas_fecha ON citas(fecha);
CREATE INDEX idx_citas_doctor ON citas(id_doctor);
CREATE INDEX idx_citas_paciente ON citas(id_paciente);
CREATE INDEX idx_consultas_cita ON consultas(id_cita);
CREATE INDEX idx_pacientes_nombre ON pacientes(nombre);
CREATE INDEX idx_doctores_especialidad ON doctores(especialidad);

-- DATOS DE PRUEBA
INSERT INTO administrador (usuario, contrasena, nombre)
VALUES ('admin', 'admin123', 'Administrador Sistema')
ON DUPLICATE KEY UPDATE usuario = usuario;

INSERT INTO empleados (nombre, direccion, telefono, fecha_nacimiento, sexo, sueldo, turno, contrasena, usuario)
VALUES ('JANET', 'Av. Test 123', '3312345678', '1992-08-15', 'F', 9000.00, 'Matutino', 'janet123', 'janet');

INSERT INTO empleados (nombre, direccion, telefono, fecha_nacimiento, sexo, sueldo, turno, contrasena, usuario)
VALUES ('BEATRIZ', 'Calle Principal 100', '3312345678', '1990-05-15', 'F', 8000.00, 'Matutino', 'beatriz123', 'beatriz');

INSERT INTO doctores (nombre, direccion, telefono, fecha_nacimiento, sexo, especialidad, contrasena, usuario)
VALUES ('Dr. JOSUE', 'Av. Médica 200', '3398765432', '1980-03-20', 'M', 'Medicina General', 'josue123', 'dr.josue');

INSERT INTO doctores (nombre, direccion, telefono, fecha_nacimiento, sexo, especialidad, contrasena, usuario)
VALUES ('Dr. CHRISTOPHER', 'Col. Doctores 300', '3387654321', '1975-08-10', 'M', 'Cardiología', 'christopher123', 'dr.christopher');
