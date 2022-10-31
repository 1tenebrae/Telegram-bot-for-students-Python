-- MySQL dump 10.13  Distrib 5.7.39, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: db_bot
-- ------------------------------------------------------
-- Server version	5.7.39

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
-- Table structure for table `SubjectTable`
--

DROP TABLE IF EXISTS `SubjectTable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SubjectTable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_group` int(11) DEFAULT NULL,
  `type_week` int(11) DEFAULT NULL,
  `day_week` int(11) DEFAULT NULL,
  `id_time` int(11) DEFAULT NULL,
  `id_lesson` int(11) DEFAULT NULL,
  `id_subject` int(11) DEFAULT NULL,
  `id_teacher` int(11) DEFAULT NULL,
  `id_auditorium` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_group_idx` (`id_group`),
  KEY `id_auditorium_idx` (`id_auditorium`),
  KEY `id_time_idx` (`id_time`),
  KEY `id_subject_idx` (`id_subject`),
  KEY `id_teacher_idx` (`id_teacher`),
  KEY `fk_SubjectTable_1_idx` (`id_lesson`),
  CONSTRAINT `id_auditorium` FOREIGN KEY (`id_auditorium`) REFERENCES `auditorium` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_group` FOREIGN KEY (`id_group`) REFERENCES `group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_lesson` FOREIGN KEY (`id_lesson`) REFERENCES `type_lesson` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_subject` FOREIGN KEY (`id_subject`) REFERENCES `subject` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_teacher` FOREIGN KEY (`id_teacher`) REFERENCES `teacher` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_time` FOREIGN KEY (`id_time`) REFERENCES `lesson_time` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SubjectTable`
--

LOCK TABLES `SubjectTable` WRITE;
/*!40000 ALTER TABLE `SubjectTable` DISABLE KEYS */;
INSERT INTO `SubjectTable` VALUES (1,1,0,0,1,3,12,7,4),(2,1,0,1,1,3,12,7,4),(3,1,0,2,1,3,12,7,4),(4,1,0,3,1,3,12,7,4),(5,1,0,4,1,3,12,7,4),(6,1,0,5,1,3,12,7,4),(7,1,0,5,2,3,12,7,4),(11,1,1,0,2,3,12,7,4),(12,4,1,0,1,3,12,7,4),(13,4,0,0,1,3,12,7,4),(14,3,1,0,1,3,12,7,4),(15,3,0,0,1,3,12,7,4),(16,3,0,0,2,6,15,9,14);
/*!40000 ALTER TABLE `SubjectTable` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-25 17:47:36
