-- MySQL dump 10.13  Distrib 5.1.63, for apple-darwin10.3.0 (i386)
--
-- Host: localhost    Database: scloud
-- ------------------------------------------------------
-- Server version	5.1.63

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `credential_mapping`
--

DROP TABLE IF EXISTS `credential_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `credential_mapping` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `user_pass` varchar(255) NOT NULL,
  `base_storage_type` varchar(255) NOT NULL,
  `base_user_name` varchar(255) NOT NULL,
  `base_user_pass` varchar(255) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credential_mapping`
--

LOCK TABLES `credential_mapping` WRITE;
/*!40000 ALTER TABLE `credential_mapping` DISABLE KEYS */;
/*!40000 ALTER TABLE `credential_mapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_acl`
--

DROP TABLE IF EXISTS `data_acl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_acl` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `data_uri` varchar(255) NOT NULL,
  `data_type` varchar(255) NOT NULL,
  `owner_id` varchar(255) NOT NULL,
  `acl_type` varchar(255) NOT NULL,
  `acl_content` text NOT NULL,
  `data_pass` varchar(255) NOT NULL DEFAULT '',
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_acl`
--

LOCK TABLES `data_acl` WRITE;
/*!40000 ALTER TABLE `data_acl` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_acl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domain`
--

DROP TABLE IF EXISTS `domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `domain_type_id` int(11) NOT NULL,
  `space_id` int(11) NOT NULL,
  `size` float(11) NOT NULL DEFAULT '0',
  `left` float(11) NOT NULL DEFAULT '2',
  `is_active` int(11) NOT NULL DEFAULT '1',
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `space_id` (`space_id`),
  KEY `domain_type_id` (`domain_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domain`
--

LOCK TABLES `domain` WRITE;
/*!40000 ALTER TABLE `domain` DISABLE KEYS */;
INSERT INTO `domain` VALUES (1,'d1',1,1,2,2,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(2,'d2',2,1,1,2,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(3,'d3',3,1,1,2,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(4,'d4',3,2,3,2,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(5,'d5',3,2,1,2,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(6,'d6',3,2,5,2,1,'2013-10-08 20:39:01','2013-10-08 20:39:01');
/*!40000 ALTER TABLE `domain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domain_type`
--

DROP TABLE IF EXISTS `domain_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain_type` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domain_type`
--

LOCK TABLES `domain_type` WRITE;
/*!40000 ALTER TABLE `domain_type` DISABLE KEYS */;
INSERT INTO `domain_type` VALUES (1,'public'),(2,'protected'),(3,'private');
/*!40000 ALTER TABLE `domain_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permission` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES (1,'GET_OBJ','2013-10-08 20:39:01','2013-10-08 20:39:01'),(2,'GET_CON','2013-10-08 20:39:01','2013-10-08 20:39:01'),(3,'GET_DOM','2013-10-08 20:39:01','2013-10-08 20:39:01'),(4,'GET_CAP','2013-10-08 20:39:01','2013-10-08 20:39:01'),(5,'GET_QUE','2013-10-08 20:39:01','2013-10-08 20:39:01'),(6,'GET_USE','2013-10-08 20:39:01','2013-10-08 20:39:01'),(7,'PUT_OBJ','2013-10-08 20:39:01','2013-10-08 20:39:01'),(8,'PUT_CON','2013-10-08 20:39:01','2013-10-08 20:39:01'),(9,'PUT_DOM','2013-10-08 20:39:01','2013-10-08 20:39:01'),(10,'PUT_CAP','2013-10-08 20:39:01','2013-10-08 20:39:01'),(11,'PUT_QUE','2013-10-08 20:39:01','2013-10-08 20:39:01'),(12,'PUT_USE','2013-10-08 20:39:01','2013-10-08 20:39:01'),(13,'DELETE_OBJ','2013-10-08 20:39:01','2013-10-08 20:39:01'),(14,'DELETE_CON','2013-10-08 20:39:01','2013-10-08 20:39:01'),(15,'DELETE_DOM','2013-10-08 20:39:01','2013-10-08 20:39:01'),(16,'DELETE_CAP','2013-10-08 20:39:01','2013-10-08 20:39:01'),(17,'DELETE_QUE','2013-10-08 20:39:01','2013-10-08 20:39:01'),(18,'DELETE_USE','2013-10-08 20:39:01','2013-10-08 20:39:01'),(19,'UPDATE_OBJ','2013-10-08 20:39:01','2013-10-08 20:39:01'),(20,'UPDATE_CON','2013-10-08 20:39:01','2013-10-08 20:39:01'),(21,'UPDATE_DOM','2013-10-08 20:39:01','2013-10-08 20:39:01'),(22,'UPDATE_CAP','2013-10-08 20:39:01','2013-10-08 20:39:01'),(23,'UPDATE_QUE','2013-10-08 20:39:01','2013-10-08 20:39:01'),(24,'UPDATE_USE','2013-10-08 20:39:01','2013-10-08 20:39:01');
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission_group`
--

DROP TABLE IF EXISTS `permission_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permission_group` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `group_meta` varchar(1000) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission_group`
--

LOCK TABLES `permission_group` WRITE;
/*!40000 ALTER TABLE `permission_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `permission_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `role_name` varchar(255) NOT NULL,
  `role_type` varchar(255) NOT NULL DEFAULT '',
  `role_expires` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `metadata` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'super_admin','sys','2013-10-08 20:39:01',1,'all'),(2,'admin','sys','2013-10-08 20:39:01',1,'1,2,3,4'),(3,'operator','sys','2013-10-08 20:39:01',1,'1,2,3'),(4,'member','sys','2013-10-08 20:39:01',1,'1,2'),(5,'guest','sys','2013-10-08 20:39:01',1,'1');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_exclusive`
--

DROP TABLE IF EXISTS `role_exclusive`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role_exclusive` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `role1_id` int(11) NOT NULL,
  `role2_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_exclusive`
--

LOCK TABLES `role_exclusive` WRITE;
/*!40000 ALTER TABLE `role_exclusive` DISABLE KEYS */;
/*!40000 ALTER TABLE `role_exclusive` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles_in_domain`
--

DROP TABLE IF EXISTS `roles_in_domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles_in_domain` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `domain_type_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`),
  KEY `domain_type_id` (`domain_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_in_domain`
--

LOCK TABLES `roles_in_domain` WRITE;
/*!40000 ALTER TABLE `roles_in_domain` DISABLE KEYS */;
INSERT INTO `roles_in_domain` VALUES (1,1,2),(2,1,3),(3,1,4),(4,1,5),(5,2,2),(6,2,3),(7,3,2);
/*!40000 ALTER TABLE `roles_in_domain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_reg` tinyint(1) NOT NULL DEFAULT '1',
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','ADMIN','rob@scloud.com',1,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(2,'rob','scloud','rob@scloud.com',1,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(3,'hi','scloud','rob@scloud.com',1,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(4,'hello','scloud','rob@scloud.com',1,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(5,'haha','scloud','rob@scloud.com',1,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(6,'niu','scloud','rob@scloud.com',1,1,'2013-10-08 20:39:01','2013-10-08 20:39:01');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_domain_roles`
--

DROP TABLE IF EXISTS `user_domain_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_domain_roles` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `domain_id` (`domain_id`),
  KEY `role_id` (`role_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_domain_roles`
--

LOCK TABLES `user_domain_roles` WRITE;
/*!40000 ALTER TABLE `user_domain_roles` DISABLE KEYS */;
INSERT INTO `user_domain_roles` VALUES (1,1,1,1,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(2,1,1,2,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(3,1,2,3,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(4,2,2,2,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(5,3,1,3,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(6,4,2,4,1,'2013-10-08 20:39:01','2013-10-08 20:39:01'),(7,5,1,2,1,'2013-10-08 20:39:01','2013-10-08 20:39:01');
/*!40000 ALTER TABLE `user_domain_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_roles`
--

DROP TABLE IF EXISTS `user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_roles` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `role_id` (`role_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles`
--

LOCK TABLES `user_roles` WRITE;
/*!40000 ALTER TABLE `user_roles` DISABLE KEYS */;
INSERT INTO `user_roles` VALUES (1,1,1,'2013-10-04 14:44:19','2013-10-04 14:44:19'),(2,1,2,'2013-10-04 14:44:19','2013-10-04 14:44:19'),(3,1,3,'2013-10-04 14:44:19','2013-10-04 14:44:19'),(4,2,2,'2013-10-04 14:44:19','2013-10-04 14:44:19'),(5,3,3,'2013-10-04 14:44:19','2013-10-04 14:44:19'),(6,4,4,'2013-10-04 14:44:19','2013-10-04 14:44:19'),(7,1,4,'2013-10-04 20:30:42','2013-10-04 20:30:42'),(8,10,3,'2013-10-04 20:31:01','2013-10-04 20:31:01');
/*!40000 ALTER TABLE `user_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_space`
--

DROP TABLE IF EXISTS `user_space`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_space` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `size` int(11) NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created` datetime NOT NULL,
  `expires` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_space`
--

LOCK TABLES `user_space` WRITE;
/*!40000 ALTER TABLE `user_space` DISABLE KEYS */;
INSERT INTO `user_space` VALUES (1,'rob_space',2,10,1,'2013-10-08 20:39:01','2013-10-08 20:39:01','2013-10-08 20:39:01'),(2,'hi_space',3,10,1,'2013-10-08 20:39:01','2013-10-08 20:39:01','2013-10-08 20:39:01'),(3,'hello_space',4,15,1,'2013-10-08 20:39:01','2013-10-08 20:39:01','2013-10-08 20:39:01'),(4,'haha_space',5,8,1,'2013-10-08 20:39:01','2013-10-08 20:39:01','2013-10-08 20:39:01'),(5,'niu_space',6,15,1,'2013-10-08 20:39:01','2013-10-08 20:39:01','2013-10-08 20:39:01');
/*!40000 ALTER TABLE `user_space` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-10-10 14:26:29
