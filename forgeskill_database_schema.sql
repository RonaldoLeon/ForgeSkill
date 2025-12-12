-- ====================================================================
-- FORGESKILL DATABASE SCHEMA
-- ====================================================================
-- Generado automáticamente desde Django ORM
-- Fecha: 2025-12-12 12:20:05
-- Base de datos: MySQL
-- Django Version: 6.0
-- 
-- Este archivo contiene el esquema completo de la base de datos
-- ForgeSkill incluyendo todas las tablas, campos, relaciones y
-- constraints generados por las migraciones de Django.
--
-- IMPORTANTE: Este archivo es independiente y puede usarse para
-- recrear la estructura de la base de datos en un servidor MySQL limpio.
-- ====================================================================

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS forgeskill CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE forgeskill;

-- ====================================================================
-- INICIO DEL ESQUEMA DE TABLAS
-- ====================================================================

--
-- Create model Conocimiento
--
CREATE TABLE `ForgeSkill_conocimiento` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre` varchar(100) NOT NULL);
--
-- Create model Examen
--
CREATE TABLE `ForgeSkill_examen` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `titulo` varchar(200) NOT NULL, `descripcion` longtext NOT NULL);
--
-- Create model Insignia
--
CREATE TABLE `ForgeSkill_insignia` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre` varchar(100) NOT NULL, `fecha` date NOT NULL, `usuario_id` integer NOT NULL);
--
-- Create model InsigniaOtorgada
--
CREATE TABLE `ForgeSkill_insigniaotorgada` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `fecha` datetime(6) NOT NULL, `motivo` longtext NULL, `insignia_id` bigint NOT NULL, `usuario_id` integer NOT NULL);
--
-- Create model Mensaje
--
CREATE TABLE `ForgeSkill_mensaje` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `contenido` longtext NOT NULL, `fecha` datetime(6) NOT NULL, `receptor_id` integer NOT NULL, `remitente_id` integer NOT NULL);
--
-- Create model Perfil
--
CREATE TABLE `ForgeSkill_perfil` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `foto` varchar(100) NULL, `bio` longtext NULL, `area_trabajo` varchar(200) NULL, `telefono` varchar(20) NULL, `ciudad` varchar(100) NULL, `user_id` integer NOT NULL UNIQUE);
CREATE TABLE `ForgeSkill_perfil_conocimientos` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `perfil_id` bigint NOT NULL, `conocimiento_id` bigint NOT NULL);
--
-- Create model Experiencia
--
CREATE TABLE `ForgeSkill_experiencia` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `proyecto` varchar(200) NOT NULL, `rol` varchar(150) NOT NULL, `descripcion` longtext NOT NULL, `fecha` date NOT NULL, `perfil_id` bigint NOT NULL);
--
-- Create model Pregunta
--
CREATE TABLE `ForgeSkill_pregunta` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `texto_pregunta` longtext NOT NULL, `tipo` varchar(20) NOT NULL, `opcion_correcta` varchar(200) NOT NULL, `otras_opciones` longtext NOT NULL, `examen_id` bigint NOT NULL);
--
-- Create model Proyecto
--
CREATE TABLE `ForgeSkill_proyecto` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre` varchar(100) NOT NULL, `estado` varchar(20) NOT NULL, `lider_id` integer NOT NULL);
--
-- Add field proyecto to examen
--
ALTER TABLE `ForgeSkill_examen` ADD COLUMN `proyecto_id` bigint NOT NULL , ADD CONSTRAINT `ForgeSkill_examen_proyecto_id_c54a593e_fk_ForgeSkill_proyecto_id` FOREIGN KEY (`proyecto_id`) REFERENCES `ForgeSkill_proyecto`(`id`);
--
-- Create model ComentarioProyecto
--
CREATE TABLE `ForgeSkill_comentarioproyecto` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `contenido` longtext NOT NULL, `fecha` datetime(6) NOT NULL, `usuario_id` integer NOT NULL, `proyecto_id` bigint NOT NULL);
--
-- Create model ResultadoExamen
--
CREATE TABLE `ForgeSkill_resultadoexamen` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `puntaje` double precision NOT NULL, `fecha` datetime(6) NOT NULL, `examen_id` bigint NOT NULL, `usuario_id` integer NOT NULL);
--
-- Create model Solicitud
--
CREATE TABLE `ForgeSkill_solicitud` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `estado` varchar(20) NOT NULL, `proyecto_id` bigint NOT NULL, `usuario_id` integer NOT NULL);
--
-- Create model Tarea
--
CREATE TABLE `ForgeSkill_tarea` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `titulo` varchar(200) NOT NULL, `estado` varchar(20) NOT NULL, `asignado_a_id` integer NULL, `proyecto_id` bigint NOT NULL);
ALTER TABLE `ForgeSkill_insignia` ADD CONSTRAINT `ForgeSkill_insignia_usuario_id_c668cdd8_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `ForgeSkill_insigniaotorgada` ADD CONSTRAINT `ForgeSkill_insigniao_insignia_id_c1804cf1_fk_ForgeSkil` FOREIGN KEY (`insignia_id`) REFERENCES `ForgeSkill_insignia` (`id`);
ALTER TABLE `ForgeSkill_insigniaotorgada` ADD CONSTRAINT `ForgeSkill_insigniaotorgada_usuario_id_07c6c7d7_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `ForgeSkill_mensaje` ADD CONSTRAINT `ForgeSkill_mensaje_receptor_id_f71eb9b0_fk_auth_user_id` FOREIGN KEY (`receptor_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `ForgeSkill_mensaje` ADD CONSTRAINT `ForgeSkill_mensaje_remitente_id_2e30a458_fk_auth_user_id` FOREIGN KEY (`remitente_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `ForgeSkill_perfil` ADD CONSTRAINT `ForgeSkill_perfil_user_id_88cf70a7_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `ForgeSkill_perfil_conocimientos` ADD CONSTRAINT `ForgeSkill_perfil_conoci_perfil_id_conocimiento_i_b62850b2_uniq` UNIQUE (`perfil_id`, `conocimiento_id`);
ALTER TABLE `ForgeSkill_perfil_conocimientos` ADD CONSTRAINT `ForgeSkill_perfil_co_perfil_id_cfc298b9_fk_ForgeSkil` FOREIGN KEY (`perfil_id`) REFERENCES `ForgeSkill_perfil` (`id`);
ALTER TABLE `ForgeSkill_perfil_conocimientos` ADD CONSTRAINT `ForgeSkill_perfil_co_conocimiento_id_a60afebe_fk_ForgeSkil` FOREIGN KEY (`conocimiento_id`) REFERENCES `ForgeSkill_conocimiento` (`id`);
ALTER TABLE `ForgeSkill_experiencia` ADD CONSTRAINT `ForgeSkill_experienc_perfil_id_458fa225_fk_ForgeSkil` FOREIGN KEY (`perfil_id`) REFERENCES `ForgeSkill_perfil` (`id`);
ALTER TABLE `ForgeSkill_pregunta` ADD CONSTRAINT `ForgeSkill_pregunta_examen_id_9c95764e_fk_ForgeSkill_examen_id` FOREIGN KEY (`examen_id`) REFERENCES `ForgeSkill_examen` (`id`);
ALTER TABLE `ForgeSkill_proyecto` ADD CONSTRAINT `ForgeSkill_proyecto_lider_id_4a16e56c_fk_auth_user_id` FOREIGN KEY (`lider_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `ForgeSkill_comentarioproyecto` ADD CONSTRAINT `ForgeSkill_comentari_usuario_id_f2133121_fk_auth_user` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `ForgeSkill_comentarioproyecto` ADD CONSTRAINT `ForgeSkill_comentari_proyecto_id_a918198c_fk_ForgeSkil` FOREIGN KEY (`proyecto_id`) REFERENCES `ForgeSkill_proyecto` (`id`);
ALTER TABLE `ForgeSkill_resultadoexamen` ADD CONSTRAINT `ForgeSkill_resultado_examen_id_07d6cb68_fk_ForgeSkil` FOREIGN KEY (`examen_id`) REFERENCES `ForgeSkill_examen` (`id`);
ALTER TABLE `ForgeSkill_resultadoexamen` ADD CONSTRAINT `ForgeSkill_resultadoexamen_usuario_id_85885dd1_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `ForgeSkill_solicitud` ADD CONSTRAINT `ForgeSkill_solicitud_proyecto_id_0a9806fb_fk_ForgeSkil` FOREIGN KEY (`proyecto_id`) REFERENCES `ForgeSkill_proyecto` (`id`);
ALTER TABLE `ForgeSkill_solicitud` ADD CONSTRAINT `ForgeSkill_solicitud_usuario_id_aa8a35ef_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `ForgeSkill_tarea` ADD CONSTRAINT `ForgeSkill_tarea_asignado_a_id_b3241ea3_fk_auth_user_id` FOREIGN KEY (`asignado_a_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `ForgeSkill_tarea` ADD CONSTRAINT `ForgeSkill_tarea_proyecto_id_83fbff6c_fk_ForgeSkill_proyecto_id` FOREIGN KEY (`proyecto_id`) REFERENCES `ForgeSkill_proyecto` (`id`);
--
-- Add field descripcion to proyecto
--
ALTER TABLE `ForgeSkill_proyecto` ADD COLUMN `descripcion` longtext NULL;
--
-- Add field dificultad to proyecto
--
ALTER TABLE `ForgeSkill_proyecto` ADD COLUMN `dificultad` varchar(50) NULL;
--
-- Add field participantes to proyecto
--
CREATE TABLE `ForgeSkill_proyecto_participantes` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `proyecto_id` bigint NOT NULL, `user_id` integer NOT NULL);
ALTER TABLE `ForgeSkill_proyecto_participantes` ADD CONSTRAINT `ForgeSkill_proyecto_part_proyecto_id_user_id_52ec998d_uniq` UNIQUE (`proyecto_id`, `user_id`);
ALTER TABLE `ForgeSkill_proyecto_participantes` ADD CONSTRAINT `ForgeSkill_proyecto__proyecto_id_2e4e9945_fk_ForgeSkil` FOREIGN KEY (`proyecto_id`) REFERENCES `ForgeSkill_proyecto` (`id`);
ALTER TABLE `ForgeSkill_proyecto_participantes` ADD CONSTRAINT `ForgeSkill_proyecto__user_id_4029b6ff_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
--
-- Add field imagen to proyecto
--
ALTER TABLE `ForgeSkill_proyecto` ADD COLUMN `imagen` varchar(100) NULL;
--
-- Add field idiomas to perfil
--
ALTER TABLE `ForgeSkill_perfil` ADD COLUMN `idiomas` longtext NULL;
--
-- Add field nivel_estudio to perfil
--
ALTER TABLE `ForgeSkill_perfil` ADD COLUMN `nivel_estudio` longtext NULL;
--
-- Add field limite_miembros to proyecto
--
ALTER TABLE `ForgeSkill_proyecto` ADD COLUMN `limite_miembros` integer UNSIGNED DEFAULT 0 NOT NULL CHECK (`limite_miembros` >= 0);
ALTER TABLE `ForgeSkill_proyecto` ALTER COLUMN `limite_miembros` DROP DEFAULT;
--
-- Add field progreso to proyecto
--
ALTER TABLE `ForgeSkill_proyecto` ADD COLUMN `progreso` integer UNSIGNED DEFAULT 0 NOT NULL CHECK (`progreso` >= 0);
ALTER TABLE `ForgeSkill_proyecto` ALTER COLUMN `progreso` DROP DEFAULT;
--
-- Add field descripcion to insignia
--
ALTER TABLE `ForgeSkill_insignia` ADD COLUMN `descripcion` longtext NULL;
--
-- Add field imagen to insignia
--
ALTER TABLE `ForgeSkill_insignia` ADD COLUMN `imagen` varchar(100) NULL;
--
-- Add field puntos to insignia
--
ALTER TABLE `ForgeSkill_insignia` ADD COLUMN `puntos` integer UNSIGNED DEFAULT 0 NOT NULL CHECK (`puntos` >= 0);
ALTER TABLE `ForgeSkill_insignia` ALTER COLUMN `puntos` DROP DEFAULT;
--
-- Alter field usuario on insignia
--
ALTER TABLE `ForgeSkill_insignia` DROP FOREIGN KEY `ForgeSkill_insignia_usuario_id_c668cdd8_fk_auth_user_id`;
ALTER TABLE `ForgeSkill_insignia` MODIFY `usuario_id` integer NULL;
ALTER TABLE `ForgeSkill_insignia` ADD CONSTRAINT `ForgeSkill_insignia_usuario_id_c668cdd8_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);
--
-- Create model ProyectoActividad
--
CREATE TABLE `ForgeSkill_proyectoactividad` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `accion` varchar(100) NOT NULL, `detalle` longtext NULL, `fecha` datetime(6) NOT NULL, `proyecto_id` bigint NOT NULL, `usuario_id` integer NULL);
ALTER TABLE `ForgeSkill_proyectoactividad` ADD CONSTRAINT `ForgeSkill_proyectoa_proyecto_id_438357c1_fk_ForgeSkil` FOREIGN KEY (`proyecto_id`) REFERENCES `ForgeSkill_proyecto` (`id`);
ALTER TABLE `ForgeSkill_proyectoactividad` ADD CONSTRAINT `ForgeSkill_proyectoactividad_usuario_id_c538fce1_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);
--
-- Add field habilidades_requeridas to proyecto
--
ALTER TABLE `ForgeSkill_proyecto` ADD COLUMN `habilidades_requeridas` longtext NULL;
--
-- Add field lenguajes_programacion to proyecto
--
ALTER TABLE `ForgeSkill_proyecto` ADD COLUMN `lenguajes_programacion` longtext NULL;
--
-- Add field archivo_evidencia to tarea
--
ALTER TABLE `ForgeSkill_tarea` ADD COLUMN `archivo_evidencia` varchar(100) NULL;
--
-- Add field completado_por to tarea
--
ALTER TABLE `ForgeSkill_tarea` ADD COLUMN `completado_por_id` integer NULL , ADD CONSTRAINT `ForgeSkill_tarea_completado_por_id_9b685a33_fk_auth_user_id` FOREIGN KEY (`completado_por_id`) REFERENCES `auth_user`(`id`);
--
-- Add field descripcion to tarea
--
ALTER TABLE `ForgeSkill_tarea` ADD COLUMN `descripcion` longtext NULL;
--
-- Add field fecha_completado to tarea
--
ALTER TABLE `ForgeSkill_tarea` ADD COLUMN `fecha_completado` datetime(6) NULL;
--
-- Remove field conocimientos from perfil
--
DROP TABLE `ForgeSkill_perfil_conocimientos` CASCADE;
--
-- Add field conocimientos to perfil
--
ALTER TABLE `ForgeSkill_perfil` ADD COLUMN `conocimientos` longtext NULL;
--
-- Add field estado_retraso to tarea
--
ALTER TABLE `ForgeSkill_tarea` ADD COLUMN `estado_retraso` varchar(20) DEFAULT 'a_tiempo' NOT NULL;
ALTER TABLE `ForgeSkill_tarea` ALTER COLUMN `estado_retraso` DROP DEFAULT;
--
-- Add field fecha_asignacion to tarea
--
ALTER TABLE `ForgeSkill_tarea` ADD COLUMN `fecha_asignacion` datetime(6) DEFAULT '2025-12-12 18:19:30.059123' NULL;
ALTER TABLE `ForgeSkill_tarea` ALTER COLUMN `fecha_asignacion` SET DEFAULT NULL;
--
-- Add field fecha_entrega to tarea
--
ALTER TABLE `ForgeSkill_tarea` ADD COLUMN `fecha_entrega` datetime(6) NULL;
