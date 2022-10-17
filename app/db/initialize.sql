INSERT INTO tareas VALUES
(01,'Administrar Usuarios'),
(02,'Ver Usuarios'),
(11,'Ver Cuentas'),
(12,'Actualizar Cuentas'),
(13,'Administrar Cuentas'),
(21,'Ver Asientos'),
(22,'Crear Asientos'),
(23,'Administrar Asientos');

INSERT INTO roles VALUES (0,'Admin'),(1,'Usuario');

INSERT INTO roles_tareas VALUES
(0,01),(0,02),
(0,11),(0,12),(0,13),
(0,21),(0,22),(0,23);

INSERT INTO usuarios(usuario,nombre,contrasenia,rol_id,habilitada) VALUE ('Admin',
'Marcos Suckerberg',
'pbkdf2:sha256:260000$UE3VkQ302ZWXCaBk$d932b47f7ec2856b81aa381514df39defd34b603b1e5acf70ec4dc9a01bb8d42',
0,1);

INSERT INTO tipos VALUES
(1,'Ac','Cuenta de Activos'),
(2,'Pa','Cuenta de Pasivos'),
(3,'Pm','Cuenta de Patrimonio'),
(4,'R+','Resultados Positivos'),
(5,'R-','Resultados Negativos');

INSERT INTO cuentas (cuenta, cuenta_padre_id, codigo, tipo_id, recibe_saldo, saldo_actual) VALUES
('Activo',NULL,10000,1,0,0),
	('Caja y Bancos',10000,10100,1,0,0),
		('Caja',10100,10101,1,1,0),
		('Banco Plazo Fijo',10100,10102,1,1,0),
		('Banco c/c',10100,10103,1,1,0),
	('Creditos',10000,10200,1,0,0),
		('Deudores por Ventas',10200,10201,1,1,0),
		('Documentos a Cobrar',10200,10202,1,1,0),
		('Valores a Depositar',10200,10203,1,1,0),
	('Bienes de Cambio',10000,10300,1,0,0),
		('Mercaderias',10300,10301,1,1,0),
	('Bienes de Uso',10000,10400,1,0,0),
		('Inmuebles',10400,10401,1,1,0),
		('Rodados',10400,10402,1,1,0),
		('Instalaciones',10400,10403,1,1,0),
('Pasivo',NULL,20000,2,0,0),
	('Deudas Comerciales',20000,20100,2,0,0),
		('Proveedores',20100,20101,2,1,0),
		('Sueldos a Pagar',20100,20102,2,1,0),
	('Deudas Fiscales',20000,20200,2,0,0),
		('Impuestos a Pagar',20200,20201,2,1,0),
		('Moratorias',20200,20202,2,1,0),
	('Prestamos Bancarios',20000,20300,2,1,0),
('Patrimonio',NULL,30000,3,0,0),
	('Capital',30000,30100,3,1,0),
	('Resultados',30000,30200,3,1,0),
('Ingresos',NULL,40000,4,0,0),
	('Ventas',40000,40100,4,0,0),
		('Venta de Mercaderia',40100,40101,4,1,0),
	('Otros Ingresos',40000,40200,4,0,0),
	('Intereses Ganados',40000,40300,4,1,0),
('Egresos',NULL,50000,5,0,0),
	('Costo de Mercaderia Vendida',50000,50100,5,1,0),
	('Impuestos',50000,50200,5,1,0),
	('Sueldos',50000,50300,5,1,0),
	('Intereses',50000,50400,5,1,0),
	('Alquileres',50000,50500,5,1,0);