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
'Marcos Suckerber',
'pbkdf2:sha256:260000$UE3VkQ302ZWXCaBk$d932b47f7ec2856b81aa381514df39defd34b603b1e5acf70ec4dc9a01bb8d42',
0,1);

INSERT INTO tipos VALUES
(1,'Ac','Cuenta de Activos'),
(2,'Pa','Cuenta de Pasivos'),
(3,'Pm','Cuenta de Patrimonio'),
(4,'R+','Resultados Positivos'),
(5,'R-','Resultados Negativos');

INSERT INTO cuentas (cuenta,codigo,tipo_id,recibe_saldo,saldo_actual) VALUES
('Activo',100,1,0,0),
('Pasivo',200,2,0,0),
('Patrimonio',300,3,0,0),
('Ingresos',400,4,0,0),
('Egresos',500,5,0,0);