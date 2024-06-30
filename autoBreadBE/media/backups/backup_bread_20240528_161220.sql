-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: bread
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add 用户信息',6,'add_user'),(22,'Can change 用户信息',6,'change_user'),(23,'Can delete 用户信息',6,'delete_user'),(24,'Can view 用户信息',6,'view_user'),(25,'Can add goods',7,'add_goods'),(26,'Can change goods',7,'change_goods'),(27,'Can delete goods',7,'delete_goods'),(28,'Can view goods',7,'view_goods'),(29,'Can add inventory',8,'add_inventory'),(30,'Can change inventory',8,'change_inventory'),(31,'Can delete inventory',8,'delete_inventory'),(32,'Can view inventory',8,'view_inventory'),(33,'Can add role',9,'add_role'),(34,'Can change role',9,'change_role'),(35,'Can delete role',9,'delete_role'),(36,'Can view role',9,'view_role'),(37,'Can add sale receipt',10,'add_salereceipt'),(38,'Can change sale receipt',10,'change_salereceipt'),(39,'Can delete sale receipt',10,'delete_salereceipt'),(40,'Can view sale receipt',10,'view_salereceipt'),(41,'Can add stock order',11,'add_stockorder'),(42,'Can change stock order',11,'change_stockorder'),(43,'Can delete stock order',11,'delete_stockorder'),(44,'Can view stock order',11,'view_stockorder'),(45,'Can add user role',12,'add_userrole'),(46,'Can change user role',12,'change_userrole'),(47,'Can delete user role',12,'delete_userrole'),(48,'Can view user role',12,'view_userrole'),(49,'Can add receipt item',13,'add_receiptitem'),(50,'Can change receipt item',13,'change_receiptitem'),(51,'Can delete receipt item',13,'delete_receiptitem'),(52,'Can view receipt item',13,'view_receiptitem'),(53,'Can add permission',14,'add_permission'),(54,'Can change permission',14,'change_permission'),(55,'Can delete permission',14,'delete_permission'),(56,'Can view permission',14,'view_permission'),(57,'Can add customer',15,'add_customer'),(58,'Can change customer',15,'change_customer'),(59,'Can delete customer',15,'delete_customer'),(60,'Can view customer',15,'view_customer'),(61,'Can add discount',16,'add_discount'),(62,'Can change discount',16,'change_discount'),(63,'Can delete discount',16,'delete_discount'),(64,'Can view discount',16,'view_discount'),(65,'Can add database backup',17,'add_databasebackup'),(66,'Can change database backup',17,'change_databasebackup'),(67,'Can delete database backup',17,'delete_databasebackup'),(68,'Can view database backup',17,'view_databasebackup');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `system_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session'),(15,'system','customer'),(17,'system','databasebackup'),(16,'system','discount'),(7,'system','goods'),(8,'system','inventory'),(14,'system','permission'),(13,'system','receiptitem'),(9,'system','role'),(10,'system','salereceipt'),(11,'system','stockorder'),(6,'system','user'),(12,'system','userrole');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'system','0001_initial','2024-03-02 18:29:03.398509'),(2,'contenttypes','0001_initial','2024-03-02 18:29:03.433827'),(3,'admin','0001_initial','2024-03-02 18:29:03.512604'),(4,'admin','0002_logentry_remove_auto_add','2024-03-02 18:29:03.518795'),(5,'admin','0003_logentry_add_action_flag_choices','2024-03-02 18:29:03.524998'),(6,'contenttypes','0002_remove_content_type_name','2024-03-02 18:29:03.569773'),(7,'auth','0001_initial','2024-03-02 18:29:03.708142'),(8,'auth','0002_alter_permission_name_max_length','2024-03-02 18:29:03.739489'),(9,'auth','0003_alter_user_email_max_length','2024-03-02 18:29:03.747035'),(10,'auth','0004_alter_user_username_opts','2024-03-02 18:29:03.753219'),(11,'auth','0005_alter_user_last_login_null','2024-03-02 18:29:03.759446'),(12,'auth','0006_require_contenttypes_0002','2024-03-02 18:29:03.762681'),(13,'auth','0007_alter_validators_add_error_messages','2024-03-02 18:29:03.769853'),(14,'auth','0008_alter_user_username_max_length','2024-03-02 18:29:03.777191'),(15,'auth','0009_alter_user_last_name_max_length','2024-03-02 18:29:03.784539'),(16,'auth','0010_alter_group_name_max_length','2024-03-02 18:29:03.815518'),(17,'auth','0011_update_proxy_permissions','2024-03-02 18:29:03.823780'),(18,'auth','0012_alter_user_first_name_max_length','2024-03-02 18:29:03.830220'),(19,'sessions','0001_initial','2024-03-02 18:29:03.854496'),(20,'system','0002_goods_inventory_role_salereceipt_stockorder_and_more','2024-03-02 18:29:04.135439'),(21,'system','0003_rename_user_pwd_user_password_remove_user_true_name','2024-03-02 18:29:04.170094'),(22,'system','0004_alter_user_id','2024-03-02 18:29:04.343220'),(23,'system','0005_user_last_login','2024-03-02 18:29:04.362005'),(24,'system','0006_alter_user_id','2024-03-02 18:29:04.525416'),(25,'system','0007_alter_user_managers_user_date_joined_user_first_name_and_more','2024-03-02 18:29:04.837210'),(26,'system','0008_alter_user_password','2024-03-02 18:29:04.886767'),(27,'system','0009_alter_user_password','2024-03-02 18:29:04.927698'),(28,'system','0010_alter_user_password','2024-03-02 18:29:04.970310'),(29,'system','0011_rename_bread_name_goods_breadname','2024-03-02 18:29:04.991267'),(30,'system','0012_rename_shelf_life_goods_sheld_life','2024-03-04 17:10:05.926625'),(31,'system','0013_user_name_alter_user_username','2024-03-10 19:02:45.514825'),(32,'system','0014_user_role_alter_user_avatar_alter_user_birthday','2024-03-12 16:15:05.830791'),(33,'system','0015_delete_userrole','2024-03-12 16:26:10.404386'),(34,'system','0016_alter_user_role','2024-03-12 17:24:19.739129'),(35,'system','0017_permission_role_permission','2024-03-15 13:16:47.679123'),(36,'system','0018_remove_permission_parent_permission_pid_and_more','2024-03-15 13:43:30.604682'),(37,'system','0019_remove_permission_select','2024-03-15 16:35:31.237758'),(38,'system','0020_permission_code','2024-03-17 18:03:38.520088'),(39,'system','0021_alter_permission_code','2024-03-17 18:12:58.353116'),(40,'system','0022_permission_is_button','2024-03-20 14:46:02.073738'),(41,'system','0023_alter_permission_is_button','2024-03-20 14:51:13.603852'),(42,'system','0024_remove_inventory_bread_name_inventory_breadname_and_more','2024-03-27 14:28:13.438851'),(43,'system','0025_rename_shelf_life_inventory_shield_life','2024-03-28 15:25:29.203161'),(44,'system','0026_rename_sheld_life_goods_shield_life','2024-03-28 22:07:36.509365'),(45,'system','0027_rename_sale_count_inventory_out_count_and_more','2024-03-29 10:44:07.265254'),(46,'system','0028_alter_receiptitem_receipt','2024-03-29 23:04:26.136960'),(47,'system','0029_alter_receiptitem_receipt','2024-03-29 23:17:54.814382'),(48,'system','0030_alter_user_email_alter_user_username','2024-05-09 20:17:35.104583'),(49,'system','0031_alter_permission_code_alter_permission_name','2024-05-09 20:46:45.499264'),(50,'system','0032_user_favatar','2024-05-11 10:45:06.567078'),(51,'system','0033_remove_user_favatar_alter_user_avatar','2024-05-11 13:00:45.163391'),(52,'system','0034_alter_user_avatar','2024-05-11 13:05:25.447112'),(53,'system','0035_customer_salereceipt_customer','2024-05-11 17:24:32.396955'),(54,'system','0036_discount','2024-05-11 20:20:13.494396'),(55,'system','0036_customerlevel_delete_stockorder_inventory_goods_and_more','2024-05-13 20:48:48.147006'),(56,'system','0037_customerlevel_delete_stockorder_and_more','2024-05-13 21:19:53.731773'),(57,'system','0038_customerlevel_delete_stockorder_and_more','2024-05-21 15:48:35.159585'),(58,'system','0039_customerlevel_delete_stockorder_and_more','2024-05-21 16:02:32.241489'),(59,'system','0040_customerlevel_delete_stockorder_and_more','2024-05-21 16:04:11.531144'),(60,'system','0041_customerlevel_databasebackup_delete_stockorder','2024-05-23 17:16:48.701575');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_customer`
--

DROP TABLE IF EXISTS `system_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_customer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `level` int NOT NULL,
  `score` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `system_customer_user_id_426659b4_fk_system_user_id` FOREIGN KEY (`user_id`) REFERENCES `system_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_customer`
--

LOCK TABLES `system_customer` WRITE;
/*!40000 ALTER TABLE `system_customer` DISABLE KEYS */;
INSERT INTO `system_customer` VALUES (1,0,11,2),(2,0,30,47),(7,0,0,48);
/*!40000 ALTER TABLE `system_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_customerlevel`
--

DROP TABLE IF EXISTS `system_customerlevel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_customerlevel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `level` int NOT NULL,
  `discount` decimal(10,2) NOT NULL,
  `required_score` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `level` (`level`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_customerlevel`
--

LOCK TABLES `system_customerlevel` WRITE;
/*!40000 ALTER TABLE `system_customerlevel` DISABLE KEYS */;
INSERT INTO `system_customerlevel` VALUES (1,0,10.00,0),(2,1,9.00,500),(3,2,8.00,1000),(4,3,7.00,2000);
/*!40000 ALTER TABLE `system_customerlevel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_databasebackup`
--

DROP TABLE IF EXISTS `system_databasebackup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_databasebackup` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `backup_name` varchar(255) NOT NULL,
  `backup_date` datetime(6) NOT NULL,
  `backup_description` longtext NOT NULL,
  `backup_file` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `backup_name` (`backup_name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_databasebackup`
--

LOCK TABLES `system_databasebackup` WRITE;
/*!40000 ALTER TABLE `system_databasebackup` DISABLE KEYS */;
INSERT INTO `system_databasebackup` VALUES (11,'测试','2024-05-28 16:11:51.847284','test','backups/backup_bread_20240528_161151.sql'),(12,'停电','2024-05-28 16:12:03.155625','停电','backups/backup_bread_20240528_161202.sql'),(13,'111','2024-05-28 16:12:09.309526','1111','backups/backup_bread_20240528_161209.sql');
/*!40000 ALTER TABLE `system_databasebackup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_goods`
--

DROP TABLE IF EXISTS `system_goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_goods` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `breadname` varchar(64) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `MFG_date` date NOT NULL,
  `shield_life` int NOT NULL,
  `count` int NOT NULL,
  `sale_count` int NOT NULL,
  `is_expired` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_goods`
--

LOCK TABLES `system_goods` WRITE;
/*!40000 ALTER TABLE `system_goods` DISABLE KEYS */;
INSERT INTO `system_goods` VALUES (32,'千层蛋糕',20.00,'2024-05-13',30,11,0,0),(33,'甜甜圈',8.00,'2024-05-13',10,10,0,1),(34,'法棍',8.00,'2024-05-13',10,2,0,1),(35,'三明治',7.00,'2024-05-13',10,5,0,1),(36,'牛角包',6.00,'2024-05-21',30,10,0,0);
/*!40000 ALTER TABLE `system_goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_inventory`
--

DROP TABLE IF EXISTS `system_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_inventory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `price` decimal(10,2) NOT NULL,
  `MFG_date` date NOT NULL,
  `shield_life` int NOT NULL,
  `count` int NOT NULL,
  `out_count` int NOT NULL,
  `is_expired` tinyint(1) NOT NULL,
  `breadname` varchar(64) NOT NULL,
  `goods_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `goods_id` (`goods_id`),
  CONSTRAINT `system_inventory_goods_id_bb465d2c_fk_system_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `system_goods` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_inventory`
--

LOCK TABLES `system_inventory` WRITE;
/*!40000 ALTER TABLE `system_inventory` DISABLE KEYS */;
INSERT INTO `system_inventory` VALUES (1,8.00,'2024-05-13',30,12,11,0,'千层蛋糕',32),(2,3.00,'2024-05-13',10,21,10,1,'甜甜圈',33),(3,4.00,'2024-05-13',10,4,2,1,'法棍',34),(5,2.00,'2024-05-13',10,10,5,1,'三明治',35),(12,1.00,'2024-05-21',30,30,10,0,'牛角包',36);
/*!40000 ALTER TABLE `system_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_permission`
--

DROP TABLE IF EXISTS `system_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_permission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `level` int DEFAULT NULL,
  `pid_id` bigint DEFAULT NULL,
  `code` varchar(30) DEFAULT NULL,
  `is_button` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `system_permission_code_38743541_uniq` (`code`),
  KEY `system_permission_pid_id_37849224_fk_system_permission_id` (`pid_id`),
  CONSTRAINT `system_permission_pid_id_37849224_fk_system_permission_id` FOREIGN KEY (`pid_id`) REFERENCES `system_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_permission`
--

LOCK TABLES `system_permission` WRITE;
/*!40000 ALTER TABLE `system_permission` DISABLE KEYS */;
INSERT INTO `system_permission` VALUES (1,'全部数据',1,NULL,NULL,0),(2,'商品管理',2,1,'Goods',0),(3,'权限管理',2,1,'Acl',0),(4,'库存管理',2,1,'Inventory',0),(6,'会员管理',2,1,'Customer',0),(8,'添加商品',3,2,'btn.Goods.add',1),(9,'删除商品',3,2,'btn.Goods.remove',1),(10,'修改商品',3,2,'btn.Goods.update',1),(11,'用户管理',3,3,'User',0),(12,'角色管理',3,3,'Role',0),(13,'菜单管理',3,3,'Permission',0),(14,'添加用户',4,11,'btn.User.add',1),(15,'删除用户',4,11,'btn.User.remove',1),(16,'修改用户',4,11,'btn.User.update',1),(17,'分配角色',4,11,'btn.User.assign',1),(18,'添加角色',4,12,'btn.Role.add',1),(19,'删除角色',4,12,'btn.Role.remove',1),(20,'修改角色',4,12,'btn.Role.update',1),(21,'分配权限',4,12,'btn.Role.assign',1),(22,'添加菜单',4,13,'btn.Permission.add',1),(23,'删除菜单',4,13,'btn.Permission.remove',1),(24,'修改菜单',4,13,'btn.Permission.update',1),(28,'测试',2,1,'test',0),(31,'会员信息管理',3,6,'CustomerManage',0),(32,'会员等级管理',3,6,'CustomerLevelManage',0),(33,'销售管理',2,1,'Sell',0),(34,'销售记录',3,33,'Receipt',0),(35,'销售统计',3,33,'Detail',0),(36,'库存统计',3,4,'InventoryStatistics',0);
/*!40000 ALTER TABLE `system_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_receiptitem`
--

DROP TABLE IF EXISTS `system_receiptitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_receiptitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `sub_total` decimal(10,2) NOT NULL,
  `receipt_id` bigint NOT NULL,
  `breadname` varchar(64) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_receiptitem_receipt_id_4c983459_fk_system_salereceipt_id` (`receipt_id`),
  CONSTRAINT `system_receiptitem_receipt_id_4c983459_fk_system_salereceipt_id` FOREIGN KEY (`receipt_id`) REFERENCES `system_salereceipt` (`id`),
  CONSTRAINT `system_receiptitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_receiptitem`
--

LOCK TABLES `system_receiptitem` WRITE;
/*!40000 ALTER TABLE `system_receiptitem` DISABLE KEYS */;
INSERT INTO `system_receiptitem` VALUES (1,2,36.00,1,'千层蛋糕',18.00),(2,1,5.00,2,'牛角包',5.00),(3,1,6.00,2,'甜甜圈',6.00),(4,2,16.00,3,'三明治',8.00),(5,1,7.00,3,'法棍',7.00),(6,2,14.00,4,'法棍',7.00),(7,1,7.00,4,'法棍',7.00),(8,1,7.00,4,'法棍',7.00),(9,1,18.00,5,'千层蛋糕',18.00),(10,1,7.00,6,'法棍',7.00),(11,1,18.00,7,'千层蛋糕',18.00),(12,1,6.00,9,'甜甜圈',6.00),(13,2,12.00,9,'甜甜圈',6.00),(14,2,12.00,10,'甜甜圈',6.00),(15,1,6.00,11,'甜甜圈',6.00),(16,2,12.00,12,'甜甜圈',6.00),(17,1,5.40,15,'甜甜圈',6.00),(18,1,6.00,16,'甜甜圈',6.00),(19,2,10.00,18,'千层蛋糕',5.00),(20,1,5.00,19,'千层蛋糕',5.00),(34,1,5.00,26,'千层蛋糕',5.00),(35,1,5.00,26,'千层蛋糕',5.00),(37,1,3.00,28,'甜甜圈',3.00),(43,1,5.00,34,'千层蛋糕',5.00);
/*!40000 ALTER TABLE `system_receiptitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_role`
--

DROP TABLE IF EXISTS `system_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_role`
--

LOCK TABLES `system_role` WRITE;
/*!40000 ALTER TABLE `system_role` DISABLE KEYS */;
INSERT INTO `system_role` VALUES (2,'员工'),(1,'管理员'),(3,'顾客');
/*!40000 ALTER TABLE `system_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_role_permission`
--

DROP TABLE IF EXISTS `system_role_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_role_permission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_id` bigint NOT NULL,
  `permission_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_role_permission_role_id_permission_id_19e707bf_uniq` (`role_id`,`permission_id`),
  KEY `system_role_permissi_permission_id_f36f6499_fk_system_pe` (`permission_id`),
  CONSTRAINT `system_role_permissi_permission_id_f36f6499_fk_system_pe` FOREIGN KEY (`permission_id`) REFERENCES `system_permission` (`id`),
  CONSTRAINT `system_role_permission_role_id_ca5e9412_fk_system_role_id` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_role_permission`
--

LOCK TABLES `system_role_permission` WRITE;
/*!40000 ALTER TABLE `system_role_permission` DISABLE KEYS */;
INSERT INTO `system_role_permission` VALUES (1,1,1),(46,1,2),(47,1,3),(48,1,4),(50,1,6),(52,1,8),(53,1,9),(54,1,10),(55,1,11),(56,1,12),(57,1,13),(58,1,14),(59,1,15),(60,1,16),(61,1,17),(62,1,18),(63,1,19),(64,1,20),(65,1,21),(66,1,22),(67,1,23),(68,1,24),(70,1,28),(116,1,31),(112,1,32),(113,1,33),(114,1,34),(115,1,35),(118,1,36),(91,2,1),(2,2,2),(117,2,4),(71,2,8),(72,2,9),(73,2,10);
/*!40000 ALTER TABLE `system_role_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_salereceipt`
--

DROP TABLE IF EXISTS `system_salereceipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_salereceipt` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` datetime(6) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `customer_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `system_salereceipt_customer_id_7dcaf9e2_fk_system_customer_id` (`customer_id`),
  CONSTRAINT `system_salereceipt_customer_id_7dcaf9e2_fk_system_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `system_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_salereceipt`
--

LOCK TABLES `system_salereceipt` WRITE;
/*!40000 ALTER TABLE `system_salereceipt` DISABLE KEYS */;
INSERT INTO `system_salereceipt` VALUES (1,'2022-04-01 14:30:00.000000',36.00,NULL),(2,'2023-04-01 14:30:00.000000',11.00,NULL),(3,'2023-04-01 14:30:00.000000',23.00,NULL),(4,'2024-04-04 14:29:24.797430',28.00,NULL),(5,'2024-04-07 13:29:50.344660',18.00,NULL),(6,'2024-04-07 14:02:06.286232',7.00,NULL),(7,'2024-05-12 14:16:15.993608',18.00,NULL),(8,'2024-05-16 16:47:00.073513',0.00,NULL),(9,'2024-05-16 17:02:58.793274',18.00,1),(10,'2024-05-16 17:22:56.660843',12.00,2),(11,'2024-05-16 17:33:22.993461',6.00,1),(12,'2024-05-16 17:34:43.321034',12.00,2),(15,'2024-05-16 18:15:09.224570',5.40,1),(16,'2024-05-16 18:23:01.524562',6.00,NULL),(18,'2024-05-20 20:43:13.691164',10.00,NULL),(19,'2024-05-20 20:43:58.110626',5.00,NULL),(26,'2024-05-20 21:17:37.655112',10.00,2),(28,'2024-05-20 21:20:31.936393',3.00,2),(34,'2024-05-21 16:42:27.826395',5.00,2);
/*!40000 ALTER TABLE `system_salereceipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_user`
--

DROP TABLE IF EXISTS `system_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `password` varchar(128) NOT NULL,
  `gender` int DEFAULT NULL,
  `mobile` varchar(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `date_joined` datetime(6) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_user`
--

LOCK TABLES `system_user` WRITE;
/*!40000 ALTER TABLE `system_user` DISABLE KEYS */;
INSERT INTO `system_user` VALUES (1,'admin','pbkdf2_sha256$600000$3FqXvkmWCDLbNbzXLq4CLF$WO9Iy2Ggfyri4Cx9HFQ2l8TOEGHXhym7E4z9cHgcONE=',1,'13888888880','12345@qq.com','2024-05-23','avatar/屏幕截图_2023-12-18_102802.png','2024-05-28 15:34:04.562663','2024-02-28 16:03:24.988820','null',1,0,0,'null','admin'),(2,'zhangsan','123456',2,'15888888888','456@qq.com','2000-01-01','','2024-03-02 17:32:18.304579','2024-02-28 16:03:24.988820','null',1,0,0,'nul','张三'),(3,'zhangfei','123456',0,NULL,NULL,NULL,NULL,NULL,'2024-03-11 15:11:06.539191','',1,0,0,'','张飞qaq'),(4,'diaochan','11111111',0,NULL,NULL,NULL,NULL,NULL,'2024-03-11 15:11:42.051846','',1,0,0,'','貂蝉'),(7,'gaoyulu','pbkdf2_sha256$600000$RYK7WCEOkRYBup2eaGm1UM$YgjS+U5q4KvQ7NJF0fz77KrBS2JnwLo0liwbmLd3O8s=',0,NULL,NULL,NULL,'avatar/my_cat.jpg','2024-05-11 16:14:41.524907','2024-03-11 15:31:01.943065','',1,0,0,'','高瑜潞'),(8,'lisishen','pbkdf2_sha256$600000$OP5JQHyXc5C6iiHTcUDQeJ$X0jsrRleL1vzsKnIgkusDy+ZX5OzKIqnZOPg79VWty4=',0,NULL,NULL,NULL,NULL,'2024-04-27 21:42:23.592114','2024-03-11 15:33:49.569099','',1,0,0,'','lisishen'),(9,'gaoyi','e10adc3949ba59abbe56e057f20f883e',0,NULL,NULL,NULL,NULL,'2024-03-11 15:37:48.924053','2024-03-11 15:36:48.484619','',1,0,0,'','gaoyi'),(19,'123456','pbkdf2_sha256$600000$8KU4c7dNN2dIRJcgXIpj1B$Y3JBNOIKZbJovtxKppxhMo46pxHxHrl2VvnVjgCt1nA=',0,NULL,NULL,NULL,NULL,NULL,'2024-03-12 21:35:39.711643','',1,0,0,'','123456'),(28,'dfdfds','pbkdf2_sha256$600000$aiw7Oa0Z99oJQUPawPLCKh$o7JSGbJXLWdpmpzr3GHYPwBvRxfaiMzW8UtyY+B6CDY=',0,NULL,NULL,NULL,NULL,NULL,'2024-03-12 22:09:54.551157','',1,0,0,'','fsdfasf'),(29,'fsdfdsffdsffsdff','pbkdf2_sha256$600000$CbT0GDyzWIDuYVdsfuTAnt$53eJSWm5/sgeY2jqqmC+xBYy7Nys3qGwvNA+hHe0hQ4=',0,NULL,NULL,NULL,NULL,NULL,'2024-03-12 22:10:14.085606','',1,0,0,'','fdsfdsf'),(30,'fdsfdsf','pbkdf2_sha256$600000$2p6lvIXAtfn4APtSXtR80K$k5bkHqOffDHIyEoMB6jGHY2O4ccAbCOQcW9PjznvZj8=',0,NULL,NULL,NULL,NULL,NULL,'2024-03-12 22:16:38.694107','',1,0,0,'','fdfdf'),(31,'ffdsfds','pbkdf2_sha256$600000$XFDV7EqbCOlDdughyKNih6$sr/MhhJ/eUbacVoNQzdmyluXHiuF/v/dyLUB7QC15d8=',0,NULL,NULL,NULL,NULL,NULL,'2024-03-12 22:16:48.314918','',1,0,0,'','fasdafa'),(32,'撒大苏打的撒','pbkdf2_sha256$600000$31U2FCsk73TE5wgWIc0xRo$VJxfylzaC35NCEVY+zpPSkJ2b2/etXBGa4n2YkTeajY=',0,NULL,NULL,NULL,NULL,NULL,'2024-03-12 22:21:25.793276','',1,0,0,'','曹张新村深度'),(33,'fdsfsd','pbkdf2_sha256$600000$mDy7v5Aypp4Ppi30B56Arx$OUY0HJH3ITX7q0FREkq7coPQmkm49zU5qq0M50YvHi4=',0,NULL,NULL,NULL,NULL,NULL,'2024-03-12 22:28:49.027033','',1,0,0,'','dfdfds'),(34,'dsadsa','pbkdf2_sha256$600000$b28nz0lPrRsBjroeaBFgKq$M8koGpozlWyZ8E+xjdWDBYnE6pwGoBsrNe+jhwHMzi0=',0,NULL,NULL,NULL,NULL,NULL,'2024-03-12 22:32:56.070819','',1,0,0,'','dsadsd'),(35,'fdfdfd','pbkdf2_sha256$600000$rFnp6uEpuawr8FHfYfrGAa$5yRq3mpH/GBQwG7+j/liEZCZE+m9NlGu6ID0TbfC7E0=',0,NULL,NULL,NULL,NULL,NULL,'2024-03-12 22:33:07.362918','',1,0,0,'','dsadasd'),(36,'dsadasd','pbkdf2_sha256$600000$hKOgLbPEl5im25N9IMDE1B$+Y2cdhr7rSaptHmrJRXd2GpUUaRuGMgxK/FLHFmLFmc=',0,NULL,NULL,NULL,NULL,NULL,'2024-03-12 22:33:28.308520','',1,0,0,'','dsadas'),(37,'dasdas','pbkdf2_sha256$600000$Fecq34n6K8vBlPvKbgNJKi$9jp72QERFwznNjGby89u2d00bWTAOMcPPDqPsCCusnM=',0,NULL,NULL,NULL,NULL,NULL,'2024-03-12 22:33:35.410294','',1,0,0,'','dasda'),(38,'asdasd','pbkdf2_sha256$600000$4dHjtm8kEjqaKc1kuT6PNA$XKvMqES7Ed3g47kmQ2idc5r8hi540n5PvMr5BhgTo4A=',0,NULL,NULL,NULL,NULL,NULL,'2024-03-12 22:33:45.486330','',1,0,0,'','asdsad'),(46,'monkeyman','pbkdf2_sha256$600000$85HIfhL6oeI014FIKIMqiZ$0DMmGz36I4dKLGx8G41WC1uKvLavOLhiX/od3UWcVZY=',0,NULL,NULL,NULL,NULL,NULL,'2024-05-10 16:47:19.061180','',1,0,0,'',NULL),(47,'nihao','pbkdf2_sha256$600000$Z6HnMjSaF8vVO3UMBkUw0l$dv3dfJFiI0qi4GVkd3psjG4SyKPDE1N/VzhiY4Py+Hw=',0,NULL,NULL,NULL,'',NULL,'2024-05-11 17:34:10.779883','',1,0,0,'',NULL),(48,'qaqaq','pbkdf2_sha256$600000$WbcxoA9tD8iEGrZvT6dr2d$Hh459r6uV5bFhQ6BGZ1o/LzDA33Ix1DVF+tftZf2sFk=',0,NULL,NULL,NULL,'','2024-05-13 21:26:47.104462','2024-05-11 18:43:53.712918','',1,0,0,'',NULL),(49,'worker','pbkdf2_sha256$600000$aKMNMQIXJAFQfVSJXznxir$xDwb65x1mddh8MIstDb2Fn3n1GZ7Aa45mNmyuaIljBc=',0,'13688888888','1359058611@qq.com','2003-01-10','avatar/IMG_20240514_172119.jpg','2024-05-23 15:07:39.210902','2024-05-14 17:16:49.574600','',1,0,0,'','高瑜潞');
/*!40000 ALTER TABLE `system_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_user_groups`
--

DROP TABLE IF EXISTS `system_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_user_groups_user_id_group_id_33e2ef7b_uniq` (`user_id`,`group_id`),
  KEY `system_user_groups_group_id_925e6bcb_fk_auth_group_id` (`group_id`),
  CONSTRAINT `system_user_groups_group_id_925e6bcb_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `system_user_groups_user_id_8e766c0f_fk_system_user_id` FOREIGN KEY (`user_id`) REFERENCES `system_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_user_groups`
--

LOCK TABLES `system_user_groups` WRITE;
/*!40000 ALTER TABLE `system_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_user_role`
--

DROP TABLE IF EXISTS `system_user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_user_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_user_role_user_id_role_id_7f547efb_uniq` (`user_id`,`role_id`),
  KEY `system_user_role_role_id_d4d57704_fk_system_role_id` (`role_id`),
  CONSTRAINT `system_user_role_role_id_d4d57704_fk_system_role_id` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`),
  CONSTRAINT `system_user_role_user_id_51214d60_fk_system_user_id` FOREIGN KEY (`user_id`) REFERENCES `system_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_user_role`
--

LOCK TABLES `system_user_role` WRITE;
/*!40000 ALTER TABLE `system_user_role` DISABLE KEYS */;
INSERT INTO `system_user_role` VALUES (1,1,1),(2,2,2),(3,2,3),(8,8,2),(14,38,2),(16,47,3),(21,48,3),(23,49,2);
/*!40000 ALTER TABLE `system_user_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_user_user_permissions`
--

DROP TABLE IF EXISTS `system_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_user_user_permissions_user_id_permission_id_2c3e5fa1_uniq` (`user_id`,`permission_id`),
  KEY `system_user_user_per_permission_id_9339fa91_fk_auth_perm` (`permission_id`),
  CONSTRAINT `system_user_user_per_permission_id_9339fa91_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `system_user_user_permissions_user_id_0c39fdf8_fk_system_user_id` FOREIGN KEY (`user_id`) REFERENCES `system_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_user_user_permissions`
--

LOCK TABLES `system_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `system_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-28 16:12:20
