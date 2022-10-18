-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema sapc
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema sapc
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sapc` DEFAULT CHARACTER SET utf8 ;
USE `sapc` ;

-- -----------------------------------------------------
-- Table `sapc`.`ROLES`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc`.`ROLES` (
  `rol_id` INT NOT NULL,
  `descripcion` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`rol_id`),
  UNIQUE INDEX `descripcion_UNIQUE` (`descripcion` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc`.`USUARIOS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc`.`USUARIOS` (
  `usuario_id` INT NOT NULL AUTO_INCREMENT,
  `usuario` VARCHAR(16) NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `contrasenia` VARCHAR(128) NOT NULL,
  `rol_id` INT NOT NULL,
  `habilitada` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`usuario_id`),
  INDEX `rol_id_idx` (`rol_id` ASC) ,
  UNIQUE INDEX `usuario_UNIQUE` (`usuario` ASC) ,
  CONSTRAINT `USUARIOS_ROLES_FK`
    FOREIGN KEY (`rol_id`)
    REFERENCES `sapc`.`ROLES` (`rol_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc`.`TAREAS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc`.`TAREAS` (
  `tarea_id` INT NOT NULL,
  `tarea` VARCHAR(45) NULL,
  PRIMARY KEY (`tarea_id`),
  UNIQUE INDEX `tarea_UNIQUE` (`tarea` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc`.`ROLES_TAREAS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc`.`ROLES_TAREAS` (
  `rol_id` INT NOT NULL,
  `tarea_id` INT NOT NULL,
  PRIMARY KEY (`rol_id`, `tarea_id`),
  INDEX `ROLESTAREAS_TAREAS_FK_idx` (`tarea_id` ASC) ,
  CONSTRAINT `ROLESTAREAS_ROLES_FK`
    FOREIGN KEY (`rol_id`)
    REFERENCES `sapc`.`ROLES` (`rol_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ROLESTAREAS_TAREAS_FK`
    FOREIGN KEY (`tarea_id`)
    REFERENCES `sapc`.`TAREAS` (`tarea_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc`.`ASIENTOS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc`.`ASIENTOS` (
  `asiento_id` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATETIME NOT NULL,
  `descripcion` VARCHAR(45) NOT NULL,
  `usuario_id` INT NOT NULL,
  PRIMARY KEY (`asiento_id`),
  INDEX `usuario_id_idx` (`usuario_id` ASC) ,
  CONSTRAINT `ASIENTOS_USUARIOS_FK`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `sapc`.`USUARIOS` (`usuario_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc`.`TIPOS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc`.`TIPOS` (
  `tipo_id` INT NOT NULL,
  `tipo` VARCHAR(3) NOT NULL,
  `descripcion` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`tipo_id`),
  UNIQUE INDEX `TIPOScol_UNIQUE` (`tipo` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc`.`CUENTAS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc`.`CUENTAS` (
  `cuenta_id` INT NOT NULL AUTO_INCREMENT,
  `cuenta` VARCHAR(45) NOT NULL,
  `cuenta_padre_id` INT NULL,
  `codigo` INT NOT NULL,
  `tipo_id` INT NOT NULL,
  `recibe_saldo` TINYINT NOT NULL DEFAULT 0,
  `saldo_actual` DOUBLE NOT NULL DEFAULT 0,
  `habilitada` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`cuenta_id`),
  INDEX `tipo_id_idx` (`tipo_id` ASC) ,
  UNIQUE INDEX `cuenta_UNIQUE` (`cuenta` ASC) ,
  UNIQUE INDEX `codigo_UNIQUE` (`codigo` ASC) ,
  INDEX `CUENTAS_PADRE_FK_idx` (`cuenta_padre_id` ASC) ,
  CONSTRAINT `CUENTAS_TIPOS_FK`
    FOREIGN KEY (`tipo_id`)
    REFERENCES `sapc`.`TIPOS` (`tipo_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `CUENTAS_PADRE_FK`
    FOREIGN KEY (`cuenta_padre_id`)
    REFERENCES `sapc`.`CUENTAS` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc`.`ASIENTOS_CUENTAS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc`.`ASIENTOS_CUENTAS` (
  `asiento_id` INT NOT NULL,
  `cuenta_id` INT NOT NULL,
  `valor` DOUBLE NULL,
  `orden` INT NOT NULL,
  `saldo` DOUBLE NOT NULL,
  `haber` TINYINT NOT NULL,
  PRIMARY KEY (`asiento_id`, `cuenta_id`, `orden`),
  INDEX `AC_CUENTAS_FK_idx` (`cuenta_id` ASC) ,
  CONSTRAINT `AC_ASIENTOS_FK`
    FOREIGN KEY (`asiento_id`)
    REFERENCES `sapc`.`ASIENTOS` (`asiento_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `AC_CUENTAS_FK`
    FOREIGN KEY (`cuenta_id`)
    REFERENCES `sapc`.`CUENTAS` (`cuenta_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
