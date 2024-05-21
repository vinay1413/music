-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: localhost    Database: music_streaming
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `albums`
--

DROP TABLE IF EXISTS `albums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `albums` (
  `album_id` int NOT NULL AUTO_INCREMENT,
  `album_name` varchar(255) NOT NULL,
  `release_year` date DEFAULT NULL,
  `created_by` varchar(255) NOT NULL,
  `album_pic` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`album_id`),
  UNIQUE KEY `album_name` (`album_name`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `albums_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `creater` (`creatername`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `albums`
--

LOCK TABLES `albums` WRITE;
/*!40000 ALTER TABLE `albums` DISABLE KEYS */;
INSERT INTO `albums` VALUES (48,'katara','2023-09-23','charan','KantaraR2wE2lN5h'),(49,'Adipurush','2023-06-16','charan','AdipurushH1lM5lW3o'),(50,'Guntur Karam','2024-01-12','charan','Guntur KaramB5uT4nN5s'),(51,'Dasara','2023-04-19','charan','DasaraA7kN6lR2q'),(52,'Sahoo','2019-08-28','charan','SahooG6mR4xW9m'),(53,'Hi Nanna','2023-12-13','charan','Hi NannaO9lQ1wC0s'),(54,'Pushpa','2021-10-13','charan','PushpaW7jF4qP9m'),(57,'Salaar','2023-12-22','charan','SalaarK3pN3pO7t'),(58,'Shyam Singha Roy','2021-12-24','charan','Shyam Singha RoyN8hK9eA0b'),(59,'Darling','2010-04-23','charan','DarlingT8xV0wT6y'),(60,'Radhe Shyam','2022-03-11','charan','Radhe ShyamR4fX8sF9v');
/*!40000 ALTER TABLE `albums` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `artists`
--

DROP TABLE IF EXISTS `artists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `artists` (
  `artist_id` int NOT NULL AUTO_INCREMENT,
  `artist_name` varchar(255) NOT NULL,
  `created_by` varchar(255) NOT NULL,
  `artist_pic` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`artist_id`),
  UNIQUE KEY `artist_name` (`artist_name`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `artists_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `creater` (`creatername`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artists`
--

LOCK TABLES `artists` WRITE;
/*!40000 ALTER TABLE `artists` DISABLE KEYS */;
INSERT INTO `artists` VALUES (51,'narayana','creater1','naga shauryaF2lQ0uT1v'),(54,'sruthi hassan','creater1','sruthi hassanW7xI2iZ4y'),(55,'Rishab','vinay','anirudhU6tS8oY2m'),(56,'asif','vinay','asifE0sW7rO5f'),(57,'sandeep','vinay','sandeepO6tI9dF9z'),(58,'NTR','charan','NTRB2gN0cP5c'),(59,'Prabhas','charan','PrabhasR4mB4tQ7r'),(60,'Mahesh babu','charan','Mahesh babuZ9qW7dC3h'),(61,'Nani','charan','NaniS6lH4yS5y'),(62,'Allu Arjun','charan','Allu ArjunH8zD7mO3k'),(63,'RISHAB SHETTY','charan','RISHAB SHETTYG2mY9oN0l');
/*!40000 ALTER TABLE `artists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `creater`
--

DROP TABLE IF EXISTS `creater`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `creater` (
  `creatername` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`creatername`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `creater`
--

LOCK TABLES `creater` WRITE;
/*!40000 ALTER TABLE `creater` DISABLE KEYS */;
INSERT INTO `creater` VALUES ('charan','charaneede9999@gmail.com','admin','2024-05-11 11:48:10'),('creater1','nagalakshmi@codegnan.com','password1','2024-03-05 09:45:13'),('vinay','vinaychintha92@gmail.com','admin','2024-05-10 09:37:17');
/*!40000 ALTER TABLE `creater` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `directors`
--

DROP TABLE IF EXISTS `directors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `directors` (
  `director_id` int NOT NULL AUTO_INCREMENT,
  `director_name` varchar(255) NOT NULL,
  `director_pic` varchar(255) DEFAULT NULL,
  `created_by` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`director_id`),
  UNIQUE KEY `director_name` (`director_name`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `directors_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `creater` (`creatername`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `directors`
--

LOCK TABLES `directors` WRITE;
/*!40000 ALTER TABLE `directors` DISABLE KEYS */;
INSERT INTO `directors` VALUES (49,'neel','neelA3kH5vA6x','vinay'),(52,'ss rajamouli','ss rajamouliF9dM8kF4m','charan'),(53,'                 df','rishab shettyV0oA0oR3o','charan'),(54,' Om Raut','Om RautQ8xP3fR6l','charan'),(55,' Trivikram','TrivikramF9rS4yD8f','charan'),(56,'Srikanth','SrikanthT3eN3yD7k','charan'),(57,'sujeeth','sujeethI0oD1fK4e','charan'),(58,'shouryuv','shouryuvV6rH3kH8m','charan'),(59,'shuryovv','shuryovvJ7sR1vE0h','charan'),(60,' Sukumar','SukumarU0mU9eW9k','charan'),(61,'Bobby','BobbyG0qU0cF2g','vinay'),(62,'vinay','vinayM9lA9yZ9r','charan'),(63,'Rahul Sankrityan','Rahul SankrityanC8aP4gM0u','charan'),(64,' Karunakaran','KarunakaranY9bB5oD8o','charan'),(65,'  Radha Krishna','Radha KrishnaB7yP8rK7k','charan');
/*!40000 ALTER TABLE `directors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `likes` (
  `creator_id` varchar(255) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `song_id` int NOT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`creator_id`,`user_id`,`song_id`),
  KEY `user_id` (`user_id`),
  KEY `song_id` (`song_id`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `creater` (`creatername`),
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`username`),
  CONSTRAINT `likes_ibfk_3` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES ('charan','charan',50,'2024-05-21 05:27:43'),('charan','charan',51,'2024-05-16 05:10:47'),('charan','charan',53,'2024-05-16 05:53:13'),('charan','charan',54,'2024-05-15 16:27:42');
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `singers`
--

DROP TABLE IF EXISTS `singers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `singers` (
  `singer_id` int NOT NULL AUTO_INCREMENT,
  `singer_name` varchar(255) NOT NULL,
  `singer_pic` varchar(255) DEFAULT NULL,
  `created_by` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`singer_id`),
  UNIQUE KEY `singer_name` (`singer_name`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `singers_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `creater` (`creatername`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `singers`
--

LOCK TABLES `singers` WRITE;
/*!40000 ALTER TABLE `singers` DISABLE KEYS */;
INSERT INTO `singers` VALUES (54,'dhan','dhanushZ2yK3fX1u','creater1'),(55,'sruthi hassan','sruthi hassanP5kT8eS0c','creater1'),(56,'anir','anirudhL7dC8wO6d','vinay'),(57,'sandeep','sandeepP0eL6wB8y','vinay'),(58,'hema chandra','hema chandraB5fU1cF3d','charan'),(59,'Ajay Atul','Ajay AtulM8mB1vV4u','charan'),(60,'Manoj ','Manoj A5bW1nB8y','charan'),(61,'sanjith','sanjithO7fT3nW3d','charan'),(62,'rahul','rahulV2eP5eT1w','charan'),(63,'Hari charan','Hari charanI2vF2fW9m','charan'),(64,'karthik','karthikR9cI4pR3l','charan'),(65,'Divya kumar','Divya kumarT5zZ0uE4t','vinay'),(66,'hema','hemaI7kI5mD7h','charan'),(67,'bhavana isvi','bhavana isviP3vX7wM3r','charan'),(68,'SruthiHassan','SruthiHassanF9lL0hD6n','charan'),(69,'Ravi Basrur','Ravi BasrurL4dE1hT0b','charan'),(70,'Thaman S','Thaman SB8jV4oA9r','charan'),(71,'ThamanS','ThamanSR6zS9kF8p','charan'),(72,'Thaman','ThamanC8gG7kR3k','charan'),(73,'Mickey J meyer','Mickey J meyerA7lU3hR4d','charan'),(74,'G.V.Prakash kumar','G.V.Prakash kumarP9nY7oG3e','charan'),(75,'Justin Prabhakaran','Justin PrabhakaranQ6oJ5nP1g','charan');
/*!40000 ALTER TABLE `singers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `songs`
--

DROP TABLE IF EXISTS `songs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `songs` (
  `song_id` int NOT NULL AUTO_INCREMENT,
  `song_name` varchar(255) NOT NULL,
  `release_date` date DEFAULT NULL,
  `audio_data` varchar(255) DEFAULT NULL,
  `song_picture` varchar(255) DEFAULT NULL,
  `mood` varchar(230) DEFAULT NULL,
  `album_id` int DEFAULT NULL,
  `created_by` varchar(255) NOT NULL,
  `uploaded_at` datetime DEFAULT NULL,
  `artist_id` int DEFAULT NULL,
  `likes` int DEFAULT '0',
  `director_id` int DEFAULT NULL,
  `singer_id` int DEFAULT NULL,
  `artist2` int DEFAULT NULL,
  `singer2` int DEFAULT NULL,
  PRIMARY KEY (`song_id`),
  UNIQUE KEY `audio_data` (`audio_data`),
  UNIQUE KEY `song_picture` (`song_picture`),
  KEY `created_by` (`created_by`),
  KEY `fk_album` (`album_id`),
  KEY `fk_artist_id` (`artist_id`),
  KEY `fk_director` (`director_id`),
  KEY `fk_singer` (`singer_id`),
  KEY `ar_2` (`artist2`),
  KEY `sr_2` (`singer2`),
  CONSTRAINT `ar_2` FOREIGN KEY (`artist2`) REFERENCES `artists` (`artist_id`),
  CONSTRAINT `fk_album` FOREIGN KEY (`album_id`) REFERENCES `albums` (`album_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_artist_id` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_director` FOREIGN KEY (`director_id`) REFERENCES `directors` (`director_id`),
  CONSTRAINT `fk_singer` FOREIGN KEY (`singer_id`) REFERENCES `singers` (`singer_id`),
  CONSTRAINT `songs_ibfk_1` FOREIGN KEY (`album_id`) REFERENCES `albums` (`album_id`),
  CONSTRAINT `songs_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `creater` (`creatername`),
  CONSTRAINT `sr_2` FOREIGN KEY (`singer2`) REFERENCES `singers` (`singer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `songs`
--

LOCK TABLES `songs` WRITE;
/*!40000 ALTER TABLE `songs` DISABLE KEYS */;
INSERT INTO `songs` VALUES (50,'Varaha Roopam','2023-09-23','Varaha RoopamM0eR7wP5b','Varaha RoopamT8bF2aO5o','',48,'charan','2024-05-12 00:00:00',55,0,53,56,51,54),(51,'Jai shree ram','2023-06-16','Jai shree ramT5mG8gR2w','Jai shree ramZ5bA5rA3q','Energetic',49,'charan','2024-05-15 00:00:00',59,0,54,59,NULL,60),(53,'Dum Masala','2024-01-12','Dum MasalaY3oB1jC2x','Dum MasalaH5sX0cZ8n','Happy',50,'charan','2024-05-15 00:00:00',60,0,55,61,NULL,NULL),(54,'Dhoom dam','2023-04-19','Dhoom damC2uC6sO6e','Dhoom damR9dK9oF4q','Excited',51,'charan','2024-05-15 00:00:00',61,0,56,62,NULL,NULL),(55,'ye chota nuvvunna','2019-08-28','ye chota nuvvunnaF3oC1vA3a','ye chota nuvvunnaI2dZ9kB1i','Peaceful',52,'charan','2024-05-15 00:00:00',59,0,57,63,NULL,NULL),(56,'Adigaa','2023-12-13','AdigaaA3yB6aM6l','AdigaaV7fC7wO9f','Happy',53,'charan','2024-05-15 00:00:00',61,0,59,64,NULL,NULL),(58,'Enno enno','2023-12-13','Enno ennoM0lD2tC3c','Enno ennoD4zN5iF3v','Romantic',53,'charan','2024-05-17 00:00:00',61,0,58,67,NULL,NULL),(61,'Odiyamma','2023-12-13','OdiyammaZ6kQ4xL8s','OdiyammaO6rR1rN7r','Energetic',53,'charan','2024-05-17 00:00:00',61,0,59,68,NULL,NULL),(62,'Samayama','2023-12-13','SamayamaO4vN1dU4t','SamayamaJ6gV2gC5o','Excited',53,'charan','2024-05-17 00:00:00',61,0,58,68,NULL,NULL),(63,'Psycho Saiyaan','2019-08-30','Psycho SaiyaanZ6sL3eG9r','Psycho SaiyaanC7hU5cW9h','Romantic',52,'charan','2024-05-17 00:00:00',59,0,57,56,NULL,NULL),(64,'Saaho Bang','2019-08-30','Saaho BangW6kT2xN2w','Saaho BangS2aK6yX3m','Upbeat',52,'charan','2024-05-17 00:00:00',59,0,57,56,NULL,NULL),(66,'Sooreede','2023-12-22','SooreedeS5jC7dM8e','SooreedeJ4pF6pD5o','Happy',57,'charan','2024-05-17 00:00:00',59,0,49,69,NULL,NULL),(67,'Aaru Sethulunnaa','2023-12-22','Aaru SethulunnaaC6xR2aE9e','Aaru SethulunnaaT3wT4lW5q','Upbeat',57,'charan','2024-05-17 00:00:00',59,0,49,69,NULL,NULL),(68,'Oh My Baby','2024-01-12','Oh My BabyO4nS0dP1t','Oh My BabyZ6oF9wV8s','Energetic',50,'charan','2024-05-17 00:00:00',60,0,55,70,NULL,NULL),(69,'Kurchi Madathapetti','2024-01-12','Kurchi MadathapettiD3qY8bQ9g','Kurchi MadathapettiE0iS7iC2q','Upbeat',50,'charan','2024-05-17 00:00:00',60,0,55,70,NULL,NULL),(70,'Amma','2024-01-12','AmmaT5kC2mK3w','AmmaF4fI1aB4d','Sad',50,'charan','2024-05-17 00:00:00',60,0,55,70,NULL,NULL),(71,'Andhaala Nadhive','2022-10-12','Andhaala NadhiveW8qN8cC1u','Andhaala NadhiveS7aY5eI1v','Peaceful',48,'charan','2024-05-17 00:00:00',63,0,53,69,NULL,NULL),(72,'Rise of Shyam','2021-12-24','Rise of ShyamP6rE6lY7o','Rise of ShyamF8hW7jY2t','Upbeat',58,'charan','2024-05-18 00:00:00',61,0,63,73,NULL,NULL),(73,'Edo Edo','2021-12-24','Edo EdoK2gA4pE8c','Edo EdoG7nB8tR0i','Romantic',58,'charan','2024-05-18 00:00:00',61,0,63,73,NULL,NULL),(74,'Sirrivennela','2021-12-24','SirrivennelaT6wC0oL1n','SirrivennelaH8lV3pV2o','Calm',58,'charan','2024-05-18 00:00:00',61,0,63,73,NULL,NULL),(75,'Tara','2021-12-24','TaraN2iE9sL6n','TaraR5mC2mX2r','Peaceful',58,'charan','2024-05-18 00:00:00',61,0,63,73,NULL,NULL),(76,'Inka Eedo','2010-04-23','Inka EedoV6bP4gG5o','Inka EedoH7pD9uT5q','Romantic',59,'charan','2024-05-18 00:00:00',59,0,64,74,NULL,NULL),(77,'Neeve','2010-04-23','NeeveX0nH9dP5r','NeeveR1jP7pO8k','Romantic',59,'charan','2024-05-18 00:00:00',59,0,64,74,NULL,NULL),(78,'Pranama','2010-04-23','PranamaM3yY6jV8s','PranamaT5iQ3iB2n','',59,'charan','2024-05-18 00:00:00',59,0,64,74,NULL,NULL),(79,'Yeyo','2010-04-23','YeyoO2cV5zX5l','YeyoJ7dV9zB9i','Energetic',58,'charan','2024-05-18 00:00:00',59,0,64,74,NULL,NULL),(80,'Ee Raathale','2022-03-11','Ee RaathaleG5oZ1eC7z','Ee RaathaleJ9uL9xI3l','Romantic',60,'charan','2024-05-18 00:00:00',59,0,65,75,NULL,NULL),(81,'Ninnele','2022-03-11','NinneleE8jP2qB6v','NinneleV4lS6pU4q','Peaceful',60,'charan','2024-05-18 00:00:00',59,0,65,75,NULL,NULL),(82,'Sanchari','2022-03-11','SanchariY7uR0qK1a','SanchariW5uR3vN3j','Energetic',60,'charan','2024-05-18 00:00:00',59,0,65,75,NULL,NULL),(83,'Sundhara Vadhana','2022-03-11','Sundhara VadhanaL8lY0lE2n','Sundhara VadhanaF5gD5lL0h','',60,'charan','2024-05-18 00:00:00',59,0,65,75,NULL,NULL);
/*!40000 ALTER TABLE `songs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('charan','charaneede9999@gmail.com','adminn','2024-05-10 09:33:05'),('nagu','nagulakshmi@codegnan.com','123','2024-03-11 07:46:24');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-21 12:29:54
