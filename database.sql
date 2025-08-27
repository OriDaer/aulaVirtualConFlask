-- Crear base de datos
CREATE DATABASE IF NOT EXISTS aula_virtual;
USE aula_virtual;

-- Borrar tablas viejas si existen
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS cursos;

-- Crear tabla usuarios con rol
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'estudiante'
);

-- Crear tabla cursos
CREATE TABLE cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500),
    profesor VARCHAR(100) NOT NULL
);

-- Insertar usuarios de prueba
INSERT INTO usuarios (nombre, email, password, rol)
VALUES 
('Profesor Juan Pérez', 'juan@uni.com', SHA2('1234',256), 'profesor'),
('Profesora Carolina', 'c@utn.com', SHA2('5678',256), 'profesor'),
('Estudiante Ana', 'ana@uni.com', SHA2('abcd',256), 'estudiante');

-- Insertar cursos de ejemplo
INSERT INTO cursos (nombre, descripcion, profesor)
VALUES
('Matemática', 'Curso de matemáticas básicas', 'Profesor Juan Pérez'),
('Ciencias naturales', 'Introducción a las ciencias naturales', 'Profesora Carolina'),
('Física', 'Introducción a la física', 'Profesor Juan Pérez');
