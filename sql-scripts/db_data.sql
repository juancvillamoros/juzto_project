-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.32 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando datos para la tabla juztoaudiencias.auth_group: ~1 rows (aproximadamente)
INSERT INTO `auth_group` (`id`, `name`) VALUES
	(1, 'lawyer');

-- Volcando datos para la tabla juztoaudiencias.auth_group_permissions: ~2 rows (aproximadamente)
INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
	(1, 1, 17),
	(2, 1, 20);

-- Volcando datos para la tabla juztoaudiencias.auth_permission: ~40 rows (aproximadamente)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session'),
	(25, 'Can add video', 7, 'add_video'),
	(26, 'Can change video', 7, 'change_video'),
	(27, 'Can delete video', 7, 'delete_video'),
	(28, 'Can view video', 7, 'view_video'),
	(29, 'Can add video', 8, 'add_video'),
	(30, 'Can change video', 8, 'change_video'),
	(31, 'Can delete video', 8, 'delete_video'),
	(32, 'Can view video', 8, 'view_video'),
	(33, 'Can add playlist', 9, 'add_playlist'),
	(34, 'Can change playlist', 9, 'change_playlist'),
	(35, 'Can delete playlist', 9, 'delete_playlist'),
	(36, 'Can view playlist', 9, 'view_playlist'),
	(37, 'Can add reporte', 10, 'add_reporte'),
	(38, 'Can change reporte', 10, 'change_reporte'),
	(39, 'Can delete reporte', 10, 'delete_reporte'),
	(40, 'Can view reporte', 10, 'view_reporte');

-- Volcando datos para la tabla juztoaudiencias.auth_user: ~11 rows (aproximadamente)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, 'pbkdf2_sha256$390000$Q6NrLIUITItrdlZccAXPPz$8Aa1ayfWrxgtpTM2VVoj99TumbDWGSGO9JaIpLwSUj0=', '2023-04-10 03:33:41.686558', 1, 'juan.villamoros@juzto.co', 'Juan C', 'Villamoros', 'juan.villamoros@juzto.co', 1, 1, '2023-04-05 19:54:50.000000'),
	(2, 'pbkdf2_sha256$390000$P5HXznJaZwzscLbZ9oS3zW$ztBezn5Vn930cl5zA7JLwsT83ruyEkhH5SakQrii+6E=', '2023-04-10 12:32:29.823006', 0, 'ana.ortiz@juzto.co', 'Ana Daniela', 'Ortiz Jimenez', 'ana.ortiz@juzto.co', 0, 1, '2023-04-05 20:00:52.000000'),
	(3, 'pbkdf2_sha256$390000$WQP9Tt2qbDZnrCGVIz5O2R$eC7LpLuMntC5FIix0uQvrtIDwPpRqlOb9Q3RoPvPBTc=', '2023-04-08 03:52:08.401307', 0, 'carlos.tapia@juzto.co', 'Carlos', 'Tapia Bogallo', 'carlos.tapia@juzto.co', 0, 1, '2023-04-05 20:01:52.000000'),
	(4, 'pbkdf2_sha256$390000$omVnS46vrsyPu5d6JEJqVE$ICp5/4JSHTR6Z0Mp1LGDbAgnf405+j1T0bXMrGZOXek=', NULL, 0, 'diana.ceron@juzto.co', 'Diana', 'Ceron', 'diana.ceron@juzto.co', 0, 1, '2023-04-05 20:02:46.000000'),
	(5, 'pbkdf2_sha256$390000$Mqd0ZDXY3Vo0vYmXaReD6n$L7zPitBiMr8mQXVrjaa8rSEAmH81gS4B4KK3rcQYYdM=', NULL, 0, 'karla.mendez@juzto.co', 'Karla Andrea', 'Mendez Doria', 'karla.mendez@juzto.co', 0, 1, '2023-04-05 20:06:24.000000'),
	(6, 'pbkdf2_sha256$390000$8Uj9sBJvt1ko4jDP4HqdPB$9W5gHIIzhZZNeyI58ozYzbFT7J6lGKm5Y+CuDH/ND7Q=', NULL, 0, 'marla.tangarife@juzto.co', 'Marla Patricia', 'Tangarife España', 'marla.tangarife@juzto.co', 0, 1, '2023-04-05 20:07:22.000000'),
	(7, 'pbkdf2_sha256$390000$7FaiMTjRrakDHNWCYQswJb$IMF4nCAJlCRd8Teml6MAjdyEzTUk1LDbosJ8IaUotis=', NULL, 0, 'mariadelosangeles.arguello@juzto.co', 'María de los Ángeles', 'Arguello', 'mariadelosangeles.arguello@juzto.co', 0, 1, '2023-04-05 20:08:13.000000'),
	(8, 'pbkdf2_sha256$390000$Qhb7yQmxgvW7F4gELqqFTk$+BU8fysdQdHhMshfIc/wtRCxlRqdZv9sbu5p6M4PvKw=', NULL, 0, 'samuel.calao@juzto.co', 'Samuel Said', 'Calao Segura', 'samuel.calao@juzto.co', 0, 1, '2023-04-05 20:10:31.000000'),
	(9, 'pbkdf2_sha256$390000$2ptBbJaEoPmBJ1siJQuI2U$jafBKMVX0XZ2ZIdObGWRIlSUW0TaHWNWSCRvN9lQOGc=', NULL, 0, 'sandy.salcedo@juzto.co', 'Sandy', 'Salcedo Salgado', 'sandy.salcedo@juzto.co', 0, 1, '2023-04-05 20:11:35.000000'),
	(10, 'pbkdf2_sha256$390000$mQSztzf9n4CHrPZ71NAufi$Cq8GBppTnM4BI7WUCt4CvP65ngpV/chMBLJvM4QNPYA=', NULL, 0, 'santiago.duran@juzto.co', 'Santiago', 'Duran Solorzano', 'santiago.duran@juzto.co', 0, 1, '2023-04-05 20:28:43.000000'),
	(11, 'pbkdf2_sha256$390000$BJTIH0gFjhAC5vQEC32Yla$Y8qFzo+QOWwpYp/gXk0WMs2hgjJ2ICkqjJVZMOI3Cwo=', NULL, 0, 'vanessa.castro@juzto.co', 'Vanessa', 'Castro', 'vanessa.castro@juzto.co', 0, 1, '2023-04-05 20:30:01.000000');

-- Volcando datos para la tabla juztoaudiencias.auth_user_groups: ~0 rows (aproximadamente)

-- Volcando datos para la tabla juztoaudiencias.auth_user_user_permissions: ~0 rows (aproximadamente)

-- Volcando datos para la tabla juztoaudiencias.capacitaciones_playlist: ~0 rows (aproximadamente)

-- Volcando datos para la tabla juztoaudiencias.capacitaciones_video: ~0 rows (aproximadamente)

-- Volcando datos para la tabla juztoaudiencias.django_admin_log: ~22 rows (aproximadamente)
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2023-04-05 19:59:53.775894', '1', 'lawyer', 1, '[{"added": {}}]', 3, 1),
	(2, '2023-04-05 20:00:52.217174', '2', 'ana.ortiz@juzto.co', 1, '[{"added": {}}]', 4, 1),
	(3, '2023-04-05 20:01:27.490908', '2', 'ana.ortiz@juzto.co', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address"]}}]', 4, 1),
	(4, '2023-04-05 20:01:52.929311', '3', 'carlos.tapia@juzto.co', 1, '[{"added": {}}]', 4, 1),
	(5, '2023-04-05 20:02:13.519929', '3', 'carlos.tapia@juzto.co', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address"]}}]', 4, 1),
	(6, '2023-04-05 20:02:47.087686', '4', 'diana.ceron@juzto.co', 1, '[{"added": {}}]', 4, 1),
	(7, '2023-04-05 20:03:04.265698', '4', 'diana.ceron@juzto.co', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address"]}}]', 4, 1),
	(8, '2023-04-05 20:03:48.815793', '1', 'juan.villamoros@juzto.co', 2, '[{"changed": {"fields": ["Username", "First name", "Last name"]}}]', 4, 1),
	(9, '2023-04-05 20:06:24.585400', '5', 'karla.mendez@juzto.co', 1, '[{"added": {}}]', 4, 1),
	(10, '2023-04-05 20:06:47.112477', '5', 'karla.mendez@juzto.co', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address"]}}]', 4, 1),
	(11, '2023-04-05 20:07:22.651470', '6', 'marla.tangarife@juzto.co', 1, '[{"added": {}}]', 4, 1),
	(12, '2023-04-05 20:07:54.828712', '6', 'marla.tangarife@juzto.co', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address"]}}]', 4, 1),
	(13, '2023-04-05 20:08:13.159657', '7', 'mariadelosangeles.arguello@juzto.co', 1, '[{"added": {}}]', 4, 1),
	(14, '2023-04-05 20:08:39.502111', '7', 'mariadelosangeles.arguello@juzto.co', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address"]}}]', 4, 1),
	(15, '2023-04-05 20:10:31.416745', '8', 'samuel.calao@juzto.co', 1, '[{"added": {}}]', 4, 1),
	(16, '2023-04-05 20:10:56.591764', '8', 'samuel.calao@juzto.co', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address"]}}]', 4, 1),
	(17, '2023-04-05 20:11:35.203479', '9', 'sandy.salcedo@juzto.co', 1, '[{"added": {}}]', 4, 1),
	(18, '2023-04-05 20:11:59.492574', '9', 'sandy.salcedo@juzto.co', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address"]}}]', 4, 1),
	(19, '2023-04-05 20:28:43.989939', '10', 'santiago.duran@juzto.co', 1, '[{"added": {}}]', 4, 1),
	(20, '2023-04-05 20:29:08.449706', '10', 'santiago.duran@juzto.co', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address"]}}]', 4, 1),
	(21, '2023-04-05 20:30:02.011189', '11', 'vanessa.castro@juzto.co', 1, '[{"added": {}}]', 4, 1),
	(22, '2023-04-05 20:30:25.353447', '11', 'vanessa.castro@juzto.co', 2, '[{"changed": {"fields": ["First name", "Last name", "Email address"]}}]', 4, 1);

-- Volcando datos para la tabla juztoaudiencias.django_content_type: ~10 rows (aproximadamente)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(9, 'capacitaciones', 'playlist'),
	(8, 'capacitaciones', 'video'),
	(5, 'contenttypes', 'contenttype'),
	(10, 'reportarbugs', 'reporte'),
	(6, 'sessions', 'session'),
	(7, 'video_upload', 'video');

-- Volcando datos para la tabla juztoaudiencias.django_migrations: ~23 rows (aproximadamente)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2023-04-05 19:01:34.690430'),
	(2, 'auth', '0001_initial', '2023-04-05 19:01:35.155573'),
	(3, 'admin', '0001_initial', '2023-04-05 19:01:35.256137'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2023-04-05 19:01:35.276935'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2023-04-05 19:01:35.285367'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2023-04-05 19:01:35.347763'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2023-04-05 19:01:35.395676'),
	(8, 'auth', '0003_alter_user_email_max_length', '2023-04-05 19:01:35.418803'),
	(9, 'auth', '0004_alter_user_username_opts', '2023-04-05 19:01:35.426328'),
	(10, 'auth', '0005_alter_user_last_login_null', '2023-04-05 19:01:35.481631'),
	(11, 'auth', '0006_require_contenttypes_0002', '2023-04-05 19:01:35.485866'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2023-04-05 19:01:35.493843'),
	(13, 'auth', '0008_alter_user_username_max_length', '2023-04-05 19:01:35.543457'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2023-04-05 19:01:35.591876'),
	(15, 'auth', '0010_alter_group_name_max_length', '2023-04-05 19:01:35.608848'),
	(16, 'auth', '0011_update_proxy_permissions', '2023-04-05 19:01:35.616575'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2023-04-05 19:01:35.667547'),
	(18, 'sessions', '0001_initial', '2023-04-05 19:01:35.696796'),
	(19, 'capacitaciones', '0001_initial', '2023-04-07 21:30:03.317784'),
	(20, 'video_upload', '0001_initial', '2023-04-07 21:30:03.334553'),
	(21, 'reportarbugs', '0001_initial', '2023-04-08 21:56:10.974963'),
	(22, 'video_upload', '0002_video_user', '2023-04-09 20:37:27.207516'),
	(23, 'reportarbugs', '0002_reporte_user', '2023-04-10 01:56:27.839829');

-- Volcando datos para la tabla juztoaudiencias.django_session: ~1 rows (aproximadamente)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('henuqn9vkev68921137jsl58gp1276k6', '.eJxVjMsOwiAQRf-FtSEMFBlcuu83kOkw2KqBpI-V8d-1SRe6veec-1KJtnVM2yJzmrK6KKtOv9tA_JC6g3ynemuaW13nadC7og-66L5leV4P9-9gpGX81h4ZSuEOxYEjOxQ6Y-eMFxuMZ4GCMQBkH53BGB0bDmKRMBgEj11W7w_UZzb0:1plqhB:rdZSrgxcyVYP7Ajg_4Igivjo-DodwZ99ieVHNTbv5jE', '2023-04-24 12:32:29.827854');

-- Volcando datos para la tabla juztoaudiencias.reportarbugs_reporte: ~0 rows (aproximadamente)

-- Volcando datos para la tabla juztoaudiencias.video_upload_video: ~0 rows (aproximadamente)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
