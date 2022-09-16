-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema sapc_test
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema sapc_test
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sapc_test` DEFAULT CHARACTER SET utf8 ;
USE `sapc_test` ;

-- -----------------------------------------------------
-- Table `sapc_test`.`ROLES`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc_test`.`ROLES` (
  `rol_id` INT NOT NULL,
  `descripcion` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`rol_id`),
  UNIQUE INDEX `descripcion_UNIQUE` (`descripcion` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc_test`.`USUARIOS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc_test`.`USUARIOS` (
  `usuario_id` INT NOT NULL AUTO_INCREMENT,
  `usuario` VARCHAR(16) NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `contrasenia` VARCHAR(128) NOT NULL,
  `rol_id` INT NOT NULL,
  `habilitada` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`usuario_id`),
  INDEX `rol_id_idx` (`rol_id` ASC) VISIBLE,
  UNIQUE INDEX `usuario_UNIQUE` (`usuario` ASC) VISIBLE,
  CONSTRAINT `USUARIOS_ROLES_FK`
    FOREIGN KEY (`rol_id`)
    REFERENCES `sapc_test`.`ROLES` (`rol_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc_test`.`TAREAS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc_test`.`TAREAS` (
  `tarea_id` INT NOT NULL,
  `tarea` VARCHAR(45) NULL,
  PRIMARY KEY (`tarea_id`),
  UNIQUE INDEX `tarea_UNIQUE` (`tarea` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc_test`.`ROLES_TAREAS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc_test`.`ROLES_TAREAS` (
  `rol_id` INT NOT NULL,
  `tarea_id` INT NOT NULL,
  PRIMARY KEY (`rol_id`, `tarea_id`),
  INDEX `ROLESTAREAS_TAREAS_FK_idx` (`tarea_id` ASC) VISIBLE,
  CONSTRAINT `ROLESTAREAS_ROLES_FK`
    FOREIGN KEY (`rol_id`)
    REFERENCES `sapc_test`.`ROLES` (`rol_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ROLESTAREAS_TAREAS_FK`
    FOREIGN KEY (`tarea_id`)
    REFERENCES `sapc_test`.`TAREAS` (`tarea_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc_test`.`ASIENTOS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc_test`.`ASIENTOS` (
  `asiento_id` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `desc` VARCHAR(45) NOT NULL,
  `usuario_id` INT NOT NULL,
  PRIMARY KEY (`asiento_id`),
  INDEX `usuario_id_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `ASIENTOS_USUARIOS_FK`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `sapc_test`.`USUARIOS` (`usuario_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc_test`.`TIPOS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc_test`.`TIPOS` (
  `tipo_id` INT NOT NULL,
  `tipo` VARCHAR(3) NOT NULL,
  `descripcion` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`tipo_id`),
  UNIQUE INDEX `TIPOScol_UNIQUE` (`tipo` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc_test`.`CUENTAS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc_test`.`CUENTAS` (
  `cuenta_id` INT NOT NULL AUTO_INCREMENT,
  `cuenta` VARCHAR(45) NOT NULL,
  `codigo` INT NOT NULL,
  `tipo_id` INT NOT NULL,
  `recibe_saldo` TINYINT NOT NULL DEFAULT 0,
  `saldo_actual` DOUBLE NOT NULL DEFAULT 0,
  PRIMARY KEY (`cuenta_id`),
  INDEX `tipo_id_idx` (`tipo_id` ASC) VISIBLE,
  UNIQUE INDEX `cuenta_UNIQUE` (`cuenta` ASC) VISIBLE,
  UNIQUE INDEX `codigo_UNIQUE` (`codigo` ASC) VISIBLE,
  CONSTRAINT `CUENTAS_TIPOS_FK`
    FOREIGN KEY (`tipo_id`)
    REFERENCES `sapc_test`.`TIPOS` (`tipo_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sapc_test`.`ASIENTOS_CUENTAS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sapc_test`.`ASIENTOS_CUENTAS` (
  `asiento_id` INT NOT NULL,
  `cuenta_id` INT NOT NULL,
  `valor` DOUBLE NULL,
  `orden` INT NOT NULL,
  `saldo` DOUBLE NOT NULL,
  `debe_haber` TINYINT NOT NULL,
  PRIMARY KEY (`asiento_id`, `cuenta_id`),
  INDEX `AC_CUENTAS_FK_idx` (`cuenta_id` ASC) VISIBLE,
  CONSTRAINT `AC_ASIENTOS_FK`
    FOREIGN KEY (`asiento_id`)
    REFERENCES `sapc_test`.`ASIENTOS` (`asiento_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `AC_CUENTAS_FK`
    FOREIGN KEY (`cuenta_id`)
    REFERENCES `sapc_test`.`CUENTAS` (`cuenta_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
