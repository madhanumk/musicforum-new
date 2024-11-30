-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 10.123.0.222:3306
-- Generation Time: Apr 04, 2023 at 08:50 AM
-- Server version: 8.0.22
-- PHP Version: 7.0.33-0+deb9u12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `madhanumk_cmf`
--

-- --------------------------------------------------------

--
-- Table structure for table `account_blocked_user`
--

CREATE TABLE `account_blocked_user` (
  `id` int NOT NULL,
  `blocked_by_id` int NOT NULL,
  `blocked_user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `account_chat`
--

CREATE TABLE `account_chat` (
  `id` int NOT NULL,
  `date` datetime(6) NOT NULL,
  `message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `unread` tinyint(1) NOT NULL,
  `m_file` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `conversation_id` int DEFAULT NULL,
  `sender_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_chat`
--

INSERT INTO `account_chat` (`id`, `date`, `message`, `unread`, `m_file`, `conversation_id`, `sender_id`) VALUES
(1, '2023-02-11 09:58:16.118380', 'Hai stu, How are you?', 1, '', 1, 2),
(2, '2023-02-13 17:13:08.917850', 'Welcome! You will now be kept up to date with all things at [business name]! Reply \'stop\' at any time to opt out\r\n\r\n', 0, '', 2, 2),
(3, '2023-02-13 17:13:08.959537', 'Welcome! You will now be kept up to date with all things at [business name]! Reply \'stop\' at any time to opt out\r\n\r\n', 0, '', 2, 2),
(4, '2023-02-13 17:14:05.605456', 'Hello there! You will now be amongst the first to hear the details of our special events hosted at [business name]. Reply STOP to unsubscribe\r\n\r\n', 1, '', 1, 2),
(5, '2023-02-13 17:14:38.536161', 'Any questions I can help clear up for you as you’re testing out your free trial? :)\r\n\r\n', 1, '', 3, 2);

-- --------------------------------------------------------

--
-- Table structure for table `account_conversation`
--

CREATE TABLE `account_conversation` (
  `id` int NOT NULL,
  `date` datetime(6) NOT NULL,
  `receiver_id` int NOT NULL,
  `sender_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_conversation`
--

INSERT INTO `account_conversation` (`id`, `date`, `receiver_id`, `sender_id`) VALUES
(1, '2023-02-13 17:14:05.603868', 3, 2),
(2, '2023-02-13 17:13:08.958053', 5, 2),
(3, '2023-02-13 17:14:38.534766', 4, 2);

-- --------------------------------------------------------

--
-- Table structure for table `account_course`
--

CREATE TABLE `account_course` (
  `id` int NOT NULL,
  `topic` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `age_limit` int UNSIGNED NOT NULL,
  `overview` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `prerequisite` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `learning_outcome` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `others` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `gurukulam_id` int NOT NULL
) ;

--
-- Dumping data for table `account_course`
--

INSERT INTO `account_course` (`id`, `topic`, `age_limit`, `overview`, `prerequisite`, `learning_outcome`, `others`, `gurukulam_id`) VALUES
(2, 'Flute', 35, 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', 'sample goes here', 'sample goes here', 'sample goes here', 1),
(3, 'Veena Course', 45, 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', 'sample goes here', 'sample goes here', 'sample goes here', 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_event_organizer`
--

CREATE TABLE `account_event_organizer` (
  `id` int NOT NULL,
  `about_us` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_event_organizer`
--

INSERT INTO `account_event_organizer` (`id`, `about_us`, `user_id`) VALUES
(1, 'Melky Celebrations, a leading event company to discover an progressive Event Planners and Wedding decorators in Coimbatore. We do Custom enabled equipments and skilled team people to elevate the whole Event management systems. We painstaking to moderate the every event decors and gave prodigy entertainment shows to every delegates and guests. We hold on every clients through our creative works and create a huge space on every delegates, meanwhile get hearty wishes from all celebration activities.', 5);

-- --------------------------------------------------------

--
-- Table structure for table `account_event_organizer_highlight`
--

CREATE TABLE `account_event_organizer_highlight` (
  `id` int NOT NULL,
  `title` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `video_link` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `event_organizer_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `account_event_organizer_highlight_highlight_category`
--

CREATE TABLE `account_event_organizer_highlight_highlight_category` (
  `id` int NOT NULL,
  `event_organizer_highlight_id` int NOT NULL,
  `highlight_category_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `account_event_performer`
--

CREATE TABLE `account_event_performer` (
  `id` int NOT NULL,
  `status` varchar(1) COLLATE utf8mb4_general_ci NOT NULL,
  `event_organizer_id` int NOT NULL,
  `musician_id` int DEFAULT NULL,
  `troupe_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_event_performer`
--

INSERT INTO `account_event_performer` (`id`, `status`, `event_organizer_id`, `musician_id`, `troupe_id`) VALUES
(2, 'A', 1, 1, NULL),
(3, 'A', 1, NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_gurukulam`
--

CREATE TABLE `account_gurukulam` (
  `id` int NOT NULL,
  `phone_no` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `about_us` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_gurukulam`
--

INSERT INTO `account_gurukulam` (`id`, `phone_no`, `about_us`, `user_id`) VALUES
(1, '7895666666', 'Best music class in chromepet and Iyyapanthangal\r\nABS School of music is a dream come true for B Arjun Venkatesh, who is a recognized music teacher in chennai.Founded in 2012,The music school was started to help people learn western music and guide them to enter the world of music which can communicate and touch others emotionally.\r\n\r\n​\r\n\r\nMain motto for starting the music class is to teach music with international quality. We are in the progress of fine tuning musical capabilities of young minds who are going to tomorrows musician. Our students have secured distinction in Music examinations by Trinity College of London Conducted every year', 7);

-- --------------------------------------------------------

--
-- Table structure for table `account_gurukulam_award`
--

CREATE TABLE `account_gurukulam_award` (
  `id` int NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `photo` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `gurukulam_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_gurukulam_award`
--

INSERT INTO `account_gurukulam_award` (`id`, `title`, `photo`, `gurukulam_id`) VALUES
(4, 'Best Music School', 'gurukulam/award/b_ms_2_rUlPeKz.jpg', 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_gurukulam_skill`
--

CREATE TABLE `account_gurukulam_skill` (
  `id` int NOT NULL,
  `gurukulam_id` int NOT NULL,
  `skill_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_gurukulam_skill`
--

INSERT INTO `account_gurukulam_skill` (`id`, `gurukulam_id`, `skill_id`) VALUES
(1, 1, 2),
(2, 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `account_gurukulam_teacher`
--

CREATE TABLE `account_gurukulam_teacher` (
  `id` int NOT NULL,
  `status` varchar(1) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `gurukulam_id` int NOT NULL,
  `musician_id` int NOT NULL,
  `sender_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_gurukulam_teacher`
--

INSERT INTO `account_gurukulam_teacher` (`id`, `status`, `gurukulam_id`, `musician_id`, `sender_id`) VALUES
(1, 'S', 1, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `account_gurukulam_testimonial`
--

CREATE TABLE `account_gurukulam_testimonial` (
  `id` int NOT NULL,
  `testimonial` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `gurukulam_id` int NOT NULL,
  `musician_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_gurukulam_testimonial`
--

INSERT INTO `account_gurukulam_testimonial` (`id`, `testimonial`, `gurukulam_id`, `musician_id`) VALUES
(2, 'Raja is a wonderful performer and kept our guests entertained all evening. He had us all on our feet and singing along by the end of the night. We would not hesitate to book him again.', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_highlight`
--

CREATE TABLE `account_highlight` (
  `id` int NOT NULL,
  `title` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `video_link` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int NOT NULL,
  `description` longtext COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_highlight`
--

INSERT INTO `account_highlight` (`id`, `title`, `video_link`, `user_id`, `description`) VALUES
(1, 'Best Singer', 'https://www.youtube.com/watch?v=AwfYTc7-dac', 2, 'Indian singers,Today episode we are comparing the best indian Singers of all time in india ,For this comparison we have taken the creteria of number of national award they have won in there career.This best indian singers comes from all corners of the country,Surprisingly more award winners are not from Bollywood but from South india.'),
(2, 'Artist Award', 'https://www.youtube.com/watch?v=AwfYTc7-dac', 6, 'There’s so much to talk, every time we converse with Ameeth Thomas, the singer, songwriter, producer, recording and mixing engineer and frontman of Junkyard Groove. Currently riding the wave of his hit Bumblebee, which got nominated for the best rock artist award on a popular radio channel, Ameeth says the timing of the song’s release was odd. “My bandmates didn’t want that song to be released, but I decided to release it anyway under my name. They all left... but who knew this would be nominated! Over the years, I’ve learnt that the only constant in the Junkyard Groove has been me and me alone. And this is why I decided to go solo. We do have musicians in the band, but they keep changing,” says Ameeth.'),
(3, 'Sample highlight goes here', 'https://www.youtube.com/watch?v=65QbACEtRyg', 5, 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.');

-- --------------------------------------------------------

--
-- Table structure for table `account_highlight_category`
--

CREATE TABLE `account_highlight_category` (
  `id` int NOT NULL,
  `category_name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `account_key_performer`
--

CREATE TABLE `account_key_performer` (
  `id` int NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `profile_photo` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `status` varchar(1) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `musician_id` int DEFAULT NULL,
  `troupe_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_key_performer`
--

INSERT INTO `account_key_performer` (`id`, `name`, `profile_photo`, `status`, `musician_id`, `troupe_id`) VALUES
(2, NULL, '', 'A', 2, 1),
(3, NULL, '', 'A', 3, 1),
(5, NULL, '', NULL, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_lecture_video`
--

CREATE TABLE `account_lecture_video` (
  `id` int NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `video` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `gurukulam_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_lecture_video`
--

INSERT INTO `account_lecture_video` (`id`, `title`, `video`, `gurukulam_id`) VALUES
(1, 'Flute', 'https://www.youtube.com/watch?v=uxEFy5HTxnw', 1),
(2, 'Veena', 'https://www.youtube.com/watch?v=cj9gXaxNOR8', 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_location`
--

CREATE TABLE `account_location` (
  `id` int NOT NULL,
  `name` varchar(256) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_location`
--

INSERT INTO `account_location` (`id`, `name`) VALUES
(1, 'Coimbatore'),
(2, 'Erode');

-- --------------------------------------------------------

--
-- Table structure for table `account_musician`
--

CREATE TABLE `account_musician` (
  `id` int NOT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(1) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `profession` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `about_me` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_musician`
--

INSERT INTO `account_musician` (`id`, `dob`, `gender`, `profession`, `about_me`, `user_id`) VALUES
(1, '2023-02-11', 'M', 'Singer', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 2),
(2, '2023-02-11', 'M', 'SINGER', 'SINGER', 3),
(3, '2023-02-11', 'M', 'SINGER', 'SINGER', 4),
(4, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 8),
(5, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 9),
(6, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 10),
(7, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 11),
(8, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 12),
(9, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 13),
(10, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 14),
(11, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 15),
(12, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 16),
(13, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 17),
(14, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 18),
(15, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 19),
(16, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 20),
(17, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 21),
(18, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 22),
(19, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 23),
(20, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 24),
(21, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 25),
(22, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 26),
(23, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 27),
(24, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 28),
(25, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 29),
(26, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 30),
(27, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 31),
(28, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 32),
(29, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 33),
(30, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 34),
(31, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 35),
(32, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 36),
(33, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 37),
(34, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 38),
(35, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 39),
(36, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 40),
(37, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 41),
(38, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 42),
(39, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 43),
(40, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 44),
(41, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 45),
(42, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 46),
(43, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 47),
(44, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 48),
(45, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 49),
(46, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 50),
(47, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 51),
(48, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 52),
(49, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 53),
(50, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 54),
(51, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 55),
(52, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 56),
(53, '2023-02-11', NULL, 'Musician', 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).', 57);

-- --------------------------------------------------------

--
-- Table structure for table `account_musician_award`
--

CREATE TABLE `account_musician_award` (
  `id` int NOT NULL,
  `title` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `musician_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_musician_award`
--

INSERT INTO `account_musician_award` (`id`, `title`, `image`, `musician_id`) VALUES
(1, 'Best Music Artist', 'musician_award/flute.jpg', 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_musician_gurukulam`
--

CREATE TABLE `account_musician_gurukulam` (
  `id` int NOT NULL,
  `status` varchar(1) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `gurukulam_id` int NOT NULL,
  `musician_id` int NOT NULL,
  `sender_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_musician_gurukulam`
--

INSERT INTO `account_musician_gurukulam` (`id`, `status`, `gurukulam_id`, `musician_id`, `sender_id`) VALUES
(1, 'S', 1, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `account_musician_highlight`
--

CREATE TABLE `account_musician_highlight` (
  `id` int NOT NULL,
  `title` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `video_link` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `musician_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `account_musician_highlight_highlight_category`
--

CREATE TABLE `account_musician_highlight_highlight_category` (
  `id` int NOT NULL,
  `musician_highlight_id` int NOT NULL,
  `highlight_category_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `account_musician_skill`
--

CREATE TABLE `account_musician_skill` (
  `id` int NOT NULL,
  `teach` tinyint(1) NOT NULL,
  `musician_id` int NOT NULL,
  `skill_id` int NOT NULL,
  `skill_level_id` int NOT NULL,
  `perform` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_musician_skill`
--

INSERT INTO `account_musician_skill` (`id`, `teach`, `musician_id`, `skill_id`, `skill_level_id`, `perform`) VALUES
(1, 1, 1, 1, 2, 1),
(2, 1, 1, 2, 2, 1),
(3, 1, 1, 3, 2, 1),
(4, 1, 4, 2, 2, 1),
(5, 1, 5, 1, 2, 1),
(6, 1, 6, 3, 1, 1),
(7, 1, 7, 2, 1, 1),
(8, 1, 8, 2, 2, 1),
(9, 1, 9, 3, 1, 1),
(10, 1, 10, 3, 1, 1),
(11, 1, 11, 2, 1, 1),
(12, 1, 12, 1, 2, 1),
(13, 1, 13, 2, 1, 1),
(14, 1, 14, 1, 3, 1),
(15, 1, 15, 3, 2, 1),
(16, 1, 16, 2, 2, 1),
(17, 1, 17, 2, 3, 1),
(18, 1, 18, 3, 1, 1),
(19, 1, 19, 2, 2, 1),
(20, 1, 20, 3, 3, 1),
(21, 1, 21, 1, 3, 1),
(22, 1, 22, 1, 3, 1),
(23, 1, 23, 2, 3, 1),
(24, 1, 24, 1, 1, 1),
(25, 1, 25, 2, 1, 1),
(26, 1, 26, 1, 3, 1),
(27, 1, 27, 2, 1, 1),
(28, 1, 28, 3, 1, 1),
(29, 1, 29, 3, 1, 1),
(30, 1, 30, 3, 1, 1),
(31, 1, 31, 1, 1, 1),
(32, 1, 32, 1, 3, 1),
(33, 1, 33, 2, 3, 1),
(34, 1, 34, 1, 3, 1),
(35, 1, 35, 2, 2, 1),
(36, 1, 36, 1, 2, 1),
(37, 1, 37, 3, 2, 1),
(38, 1, 38, 1, 3, 1),
(39, 1, 39, 1, 2, 1),
(40, 1, 40, 2, 3, 1),
(41, 1, 41, 3, 3, 1),
(42, 1, 42, 2, 3, 1),
(43, 1, 43, 3, 3, 1),
(44, 1, 44, 1, 3, 1),
(45, 1, 45, 1, 3, 1),
(46, 1, 46, 3, 1, 1),
(47, 1, 47, 3, 3, 1),
(48, 1, 48, 1, 1, 1),
(49, 1, 49, 1, 3, 1),
(50, 1, 50, 3, 3, 1),
(51, 1, 51, 1, 1, 1),
(52, 1, 52, 2, 1, 1),
(53, 1, 53, 2, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_post`
--

CREATE TABLE `account_post` (
  `id` int NOT NULL,
  `content` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `posted_on` datetime(6) NOT NULL,
  `likes` int UNSIGNED NOT NULL,
  `interest_id` int DEFAULT NULL,
  `invitation_id` int DEFAULT NULL,
  `location_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `highlight_id` int DEFAULT NULL
) ;

--
-- Dumping data for table `account_post`
--

INSERT INTO `account_post` (`id`, `content`, `posted_on`, `likes`, `interest_id`, `invitation_id`, `location_id`, `user_id`, `highlight_id`) VALUES
(1, 'Indian singers,Today episode we are comparing the best indian Singers of all time in india ,For this comparison we have taken the creteria of number of national award they have won in there career.This best indian singers comes from all corners of the country,Surprisingly more award winners are not from Bollywood but from South india.<br>Video Link: <a href=https://www.youtube.com/watch?v=AwfYTc7-dac\">Watch Video </a>', '2023-02-11 09:29:19.739782', 0, NULL, NULL, NULL, 2, 1),
(2, 'There’s so much to talk, every time we converse with Ameeth Thomas, the singer, songwriter, producer, recording and mixing engineer and frontman of Junkyard Groove. Currently riding the wave of his hit Bumblebee, which got nominated for the best rock artist award on a popular radio channel, Ameeth says the timing of the song’s release was odd. “My bandmates didn’t want that song to be released, but I decided to release it anyway under my name. They all left... but who knew this would be nominated! Over the years, I’ve learnt that the only constant in the Junkyard Groove has been me and me alone. And this is why I decided to go solo. We do have musicians in the band, but they keep changing,” says Ameeth.<br>Video Link: <a href=https://www.youtube.com/watch?v=AwfYTc7-dac\">Watch Video </a>', '2023-02-11 09:38:41.319726', 0, NULL, NULL, NULL, 6, 2),
(3, 'I am going to participate <a  href=\"/event_details/5/\">Bilbao BBK Live</a> <br> <img class=\"img-fluid\" src=\"/media/event_poster/Top50MusicFestivalsintheWorld_LetItRoll_rI63Tyl.jpg\">', '2023-02-11 09:44:49.166677', 0, NULL, NULL, 1, 6, NULL),
(4, 'I am going to participate <a  href=\"/event_details/4/\">Montreux Jazz Festival</a> <br> <img class=\"img-fluid\" src=\"/media/event_poster/Top50MusicFestivalsintheWorld_Coachella_zjOF9Su.jpg\">', '2023-02-11 09:46:08.026541', 0, NULL, NULL, 1, 6, NULL),
(5, 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.<br>Video Link: <a href=https://www.youtube.com/watch?v=65QbACEtRyg\">Watch Video </a>', '2023-02-13 11:59:08.026683', 0, NULL, NULL, NULL, 5, 3);

-- --------------------------------------------------------

--
-- Table structure for table `account_post_comment`
--

CREATE TABLE `account_post_comment` (
  `id` int NOT NULL,
  `comment` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `commented_on` datetime(6) NOT NULL,
  `post_id` int NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_post_comment`
--

INSERT INTO `account_post_comment` (`id`, `comment`, `commented_on`, `post_id`, `user_id`) VALUES
(1, 'hey wow, congrats dood', '2023-02-11 09:45:11.457318', 3, 5);

-- --------------------------------------------------------

--
-- Table structure for table `account_post_user_likes`
--

CREATE TABLE `account_post_user_likes` (
  `id` int NOT NULL,
  `post_id` int NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_post_user_likes`
--

INSERT INTO `account_post_user_likes` (`id`, `post_id`, `user_id`) VALUES
(6, 1, 6),
(2, 2, 2),
(5, 3, 6),
(4, 4, 6),
(3, 5, 6);

-- --------------------------------------------------------

--
-- Table structure for table `account_reply`
--

CREATE TABLE `account_reply` (
  `id` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `reply` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `comment_id` int NOT NULL,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `account_report_people`
--

CREATE TABLE `account_report_people` (
  `id` int NOT NULL,
  `reported_on` date NOT NULL,
  `complaint` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `report_file` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `reported_by_id` int NOT NULL,
  `reported_user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `account_skill`
--

CREATE TABLE `account_skill` (
  `id` int NOT NULL,
  `skill_name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `skill_category_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_skill`
--

INSERT INTO `account_skill` (`id`, `skill_name`, `skill_category_id`) VALUES
(1, 'Carnatic', 1),
(2, 'Veena', 2),
(3, 'Flute', 2);

-- --------------------------------------------------------

--
-- Table structure for table `account_skill_category`
--

CREATE TABLE `account_skill_category` (
  `id` int NOT NULL,
  `category_name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_skill_category`
--

INSERT INTO `account_skill_category` (`id`, `category_name`) VALUES
(1, 'Vocal'),
(2, 'Instrument');

-- --------------------------------------------------------

--
-- Table structure for table `account_skill_level`
--

CREATE TABLE `account_skill_level` (
  `id` int NOT NULL,
  `level` varchar(50) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_skill_level`
--

INSERT INTO `account_skill_level` (`id`, `level`) VALUES
(1, 'Pro'),
(2, 'Performer'),
(3, 'Amateur');

-- --------------------------------------------------------

--
-- Table structure for table `account_troupe`
--

CREATE TABLE `account_troupe` (
  `id` int NOT NULL,
  `president` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `about_us` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_troupe`
--

INSERT INTO `account_troupe` (`id`, `president`, `about_us`, `user_id`) VALUES
(1, 'Hari', 'Home page of Junkyard Groove. Covers, Rock, Country, Blues, Funk, Soul we do it all. ... Junkyard Groove. Jason Sturmon , Lead Vocals, Acoustic Guitar', 6);

-- --------------------------------------------------------

--
-- Table structure for table `account_troupe_highlight`
--

CREATE TABLE `account_troupe_highlight` (
  `id` int NOT NULL,
  `title` varchar(400) COLLATE utf8mb4_general_ci NOT NULL,
  `video_link` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `troupe_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `account_troupe_highlight_highlight_category`
--

CREATE TABLE `account_troupe_highlight_highlight_category` (
  `id` int NOT NULL,
  `troupe_highlight_id` int NOT NULL,
  `highlight_category_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `account_troupe_skill`
--

CREATE TABLE `account_troupe_skill` (
  `id` int NOT NULL,
  `skill_id` int NOT NULL,
  `troupe_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_troupe_skill`
--

INSERT INTO `account_troupe_skill` (`id`, `skill_id`, `troupe_id`) VALUES
(1, 1, 1),
(2, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_user`
--

CREATE TABLE `account_user` (
  `id` int NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(60) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(400) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `verified_email` tinyint(1) NOT NULL,
  `address` longtext COLLATE utf8mb4_general_ci,
  `mobile_no` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `profile_picture` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cover_picture` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `registered_on` date NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `location_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_user`
--

INSERT INTO `account_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `name`, `email`, `verified_email`, `address`, `mobile_no`, `profile_picture`, `cover_picture`, `registered_on`, `is_active`, `is_staff`, `location_id`) VALUES
(1, 'pbkdf2_sha256$150000$e0hnLiwGIvpi$6W8V2VWQap3HN3cr273UzV3Xh7gnQA9bbARzv/4kE10=', '2023-02-13 17:42:52.545757', 1, 'admin', '', '', '', NULL, 0, NULL, NULL, '', '', '2023-02-10', 1, 1, NULL),
(2, 'pbkdf2_sha256$150000$fAN81MlZ7K5R$c1l/e+RBpeANeUKA8za8xyd7lnACE9hJHNsv3LZLuMY=', '2023-04-04 14:07:34.111376', 0, 'musician@gmail.com', 'Raja Gunasekaran', '', '', 'musician@gmail.com', 1, 'Vellakovil', '9095375754', 'm1_yfzIJ1E.jpg', '', '2023-02-11', 1, 0, 1),
(3, 'pbkdf2_sha256$150000$TszMTJxycFCE$NlCJmccfkT3dlajLKrT+77Yyw+zWVWGGSHgnVd+YEtA=', '2023-04-04 10:54:14.567420', 0, 'musician1@gmail.com', 'Karthick Stu', '', '', 'musician1@gmail.com', 1, 'Udumalpet', '9098655555', 'stu.jpg', '', '2023-02-11', 1, 0, 1),
(4, 'pbkdf2_sha256$390000$MbiokLzUIKqT8ufwhY5Vzz$yNHCvpQtuVHjzM2+03QZx49l2oZsiVmQlTWENjyBnlo=', NULL, 0, 'musician2@gmail.com', 'Sachin', '', '', 'musician2@gmail.com', 1, 'Udumalpet', '9098655555', 'sachin.jfif', '', '2023-02-11', 1, 0, 1),
(5, 'pbkdf2_sha256$150000$FgnxxaWkpIAY$62MG7QT7oiUel7KzxZlpqGHrQwkxEVij1v5Yvz/t0BY=', '2023-04-04 14:07:50.661399', 0, 'organizer@gmail.com', 'GPK Eventer', '', '', 'organizer@gmail.com', 1, 'Coimbatore', '7333333333', 'eventer_TiqN8EA.jpg', '', '2023-02-11', 1, 0, 1),
(6, 'pbkdf2_sha256$150000$hOOdIqM8B5KR$aA2vqOQ8RLPl4jmI9jIudw3JUdC4eVpF1lgibSuI5MA=', '2023-04-04 14:07:19.419700', 0, 'band@gmail.com', 'Junkyard Groove', '', '', 'band@gmail.com', 1, 'Coimbatore', '7865467004', 'Junkyard-Groove.jpg', '', '2023-02-11', 1, 0, 1),
(7, 'pbkdf2_sha256$150000$gp4nmdY5aoKr$iCP44tHfMfrj45DvEL6t29/EkyYOqQ3cZAjTqU714fw=', '2023-04-04 14:06:09.765936', 0, 'musicschool@gmail.com', 'PMA School of Music P Ltd', '', '', 'musicschool@gmail.com', 1, 'Coimbatore', '8906342222', 'download.png', '', '2023-02-11', 1, 0, 1),
(8, '', NULL, 0, 'ChristopherTownsend@gmail.com', 'Christopher', 'Townsend', '', 'ChristopherTownsend@gmail.com', 1, 'Sample address goes here..!', '6745628793', '', '', '2023-03-16', 1, 0, 1),
(9, '', NULL, 0, 'JessicaMitchell@gmail.com', 'Jessica', 'Mitchell', '', 'JessicaMitchell@gmail.com', 1, 'Sample address goes here..!', '6745628794', '', '', '2023-03-16', 1, 0, 1),
(10, '', NULL, 0, 'KyleJohnson@gmail.com', 'Kyle', 'Johnson', '', 'KyleJohnson@gmail.com', 1, 'Sample address goes here..!', '6745628795', '', '', '2023-03-16', 1, 0, 1),
(11, '', NULL, 0, 'RicardoEvans@gmail.com', 'Ricardo', 'Evans', '', 'RicardoEvans@gmail.com', 1, 'Sample address goes here..!', '6745628796', '', '', '2023-03-16', 1, 0, 1),
(12, '', NULL, 0, 'DawnTurner@gmail.com', 'Dawn', 'Turner', '', 'DawnTurner@gmail.com', 1, 'Sample address goes here..!', '6745628797', '', '', '2023-03-16', 1, 0, 1),
(13, '', NULL, 0, 'JohnMcmahon@gmail.com', 'John', 'Mcmahon', '', 'JohnMcmahon@gmail.com', 1, 'Sample address goes here..!', '6745628798', '', '', '2023-03-16', 1, 0, 1),
(14, '', NULL, 0, 'KimberlyKirk@gmail.com', 'Kimberly', 'Kirk', '', 'KimberlyKirk@gmail.com', 1, 'Sample address goes here..!', '6745628799', '', '', '2023-03-16', 1, 0, 1),
(15, '', NULL, 0, 'JenniferRios@gmail.com', 'Jennifer', 'Rios', '', 'JenniferRios@gmail.com', 1, 'Sample address goes here..!', '6745628800', '', '', '2023-03-16', 1, 0, 1),
(16, '', NULL, 0, 'DebraMontgomery@gmail.com', 'Debra', 'Montgomery', '', 'DebraMontgomery@gmail.com', 1, 'Sample address goes here..!', '6745628801', '', '', '2023-03-16', 1, 0, 1),
(17, '', NULL, 0, 'MarcusHarmon@gmail.com', 'Marcus', 'Harmon', '', 'MarcusHarmon@gmail.com', 1, 'Sample address goes here..!', '6745628802', '', '', '2023-03-16', 1, 0, 1),
(18, '', NULL, 0, 'TimothyQuinn@gmail.com', 'Timothy', 'Quinn', '', 'TimothyQuinn@gmail.com', 1, 'Sample address goes here..!', '6745628803', '', '', '2023-03-16', 1, 0, 1),
(19, '', NULL, 0, 'JamesWall@gmail.com', 'James', 'Wall', '', 'JamesWall@gmail.com', 1, 'Sample address goes here..!', '6745628804', '', '', '2023-03-16', 1, 0, 1),
(20, '', NULL, 0, 'Ms.Regina@gmail.com', 'Ms.', 'Regina', '', 'Ms.Regina@gmail.com', 1, 'Sample address goes here..!', '6745628805', '', '', '2023-03-16', 1, 0, 1),
(21, '', NULL, 0, 'BrettReese@gmail.com', 'Brett', 'Reese', '', 'BrettReese@gmail.com', 1, 'Sample address goes here..!', '6745628806', '', '', '2023-03-16', 1, 0, 1),
(22, '', NULL, 0, 'AmandaHowell@gmail.com', 'Amanda', 'Howell', '', 'AmandaHowell@gmail.com', 1, 'Sample address goes here..!', '6745628807', '', '', '2023-03-16', 1, 0, 1),
(23, '', NULL, 0, 'GregoryCruz@gmail.com', 'Gregory', 'Cruz', '', 'GregoryCruz@gmail.com', 1, 'Sample address goes here..!', '6745628808', '', '', '2023-03-16', 1, 0, 1),
(24, '', NULL, 0, 'TerryCarney@gmail.com', 'Terry', 'Carney', '', 'TerryCarney@gmail.com', 1, 'Sample address goes here..!', '6745628809', '', '', '2023-03-16', 1, 0, 1),
(25, '', NULL, 0, 'JeremyBenitez@gmail.com', 'Jeremy', 'Benitez', '', 'JeremyBenitez@gmail.com', 1, 'Sample address goes here..!', '6745628810', '', '', '2023-03-16', 1, 0, 1),
(26, '', NULL, 0, 'LukeMayo@gmail.com', 'Luke', 'Mayo', '', 'LukeMayo@gmail.com', 1, 'Sample address goes here..!', '6745628811', '', '', '2023-03-16', 1, 0, 1),
(27, '', NULL, 0, 'JoshuaDonovan@gmail.com', 'Joshua', 'Donovan', '', 'JoshuaDonovan@gmail.com', 1, 'Sample address goes here..!', '6745628812', '', '', '2023-03-16', 1, 0, 1),
(28, '', NULL, 0, 'SamanthaHenry@gmail.com', 'Samantha', 'Henry', '', 'SamanthaHenry@gmail.com', 1, 'Sample address goes here..!', '6745628813', '', '', '2023-03-16', 1, 0, 1),
(29, '', NULL, 0, 'JeffreyBaker@gmail.com', 'Jeffrey', 'Baker', '', 'JeffreyBaker@gmail.com', 1, 'Sample address goes here..!', '6745628814', '', '', '2023-03-16', 1, 0, 1),
(30, '', NULL, 0, 'JuliaStark@gmail.com', 'Julia', 'Stark', '', 'JuliaStark@gmail.com', 1, 'Sample address goes here..!', '6745628815', '', '', '2023-03-16', 1, 0, 1),
(31, '', NULL, 0, 'MeganGarcia@gmail.com', 'Megan', 'Garcia', '', 'MeganGarcia@gmail.com', 1, 'Sample address goes here..!', '6745628816', '', '', '2023-03-16', 1, 0, 1),
(32, '', NULL, 0, 'MonicaHurley@gmail.com', 'Monica', 'Hurley', '', 'MonicaHurley@gmail.com', 1, 'Sample address goes here..!', '6745628817', '', '', '2023-03-16', 1, 0, 1),
(33, '', NULL, 0, 'BradleyRiley@gmail.com', 'Bradley', 'Riley', '', 'BradleyRiley@gmail.com', 1, 'Sample address goes here..!', '6745628818', '', '', '2023-03-16', 1, 0, 1),
(34, '', NULL, 0, 'AnthonyJuarez@gmail.com', 'Anthony', 'Juarez', '', 'AnthonyJuarez@gmail.com', 1, 'Sample address goes here..!', '6745628819', '', '', '2023-03-16', 1, 0, 1),
(35, '', NULL, 0, 'MatthewRice@gmail.com', 'Matthew', 'Rice', '', 'MatthewRice@gmail.com', 1, 'Sample address goes here..!', '6745628820', '', '', '2023-03-16', 1, 0, 1),
(36, '', NULL, 0, 'EmilyGordon@gmail.com', 'Emily', 'Gordon', '', 'EmilyGordon@gmail.com', 1, 'Sample address goes here..!', '6745628821', '', '', '2023-03-16', 1, 0, 1),
(37, '', NULL, 0, 'AndrewReynolds@gmail.com', 'Andrew', 'Reynolds', '', 'AndrewReynolds@gmail.com', 1, 'Sample address goes here..!', '6745628822', '', '', '2023-03-16', 1, 0, 1),
(38, '', NULL, 0, 'MariahStephens@gmail.com', 'Mariah', 'Stephens', '', 'MariahStephens@gmail.com', 1, 'Sample address goes here..!', '6745628823', '', '', '2023-03-16', 1, 0, 1),
(39, '', NULL, 0, 'BrookeHoffman@gmail.com', 'Brooke', 'Hoffman', '', 'BrookeHoffman@gmail.com', 1, 'Sample address goes here..!', '6745628824', '', '', '2023-03-16', 1, 0, 1),
(40, '', NULL, 0, 'ChadSmith@gmail.com', 'Chad', 'Smith', '', 'ChadSmith@gmail.com', 1, 'Sample address goes here..!', '6745628825', '', '', '2023-03-16', 1, 0, 1),
(41, '', NULL, 0, 'KendraEstes@gmail.com', 'Kendra', 'Estes', '', 'KendraEstes@gmail.com', 1, 'Sample address goes here..!', '6745628826', '', '', '2023-03-16', 1, 0, 1),
(42, '', NULL, 0, 'DavidYoung@gmail.com', 'David', 'Young', '', 'DavidYoung@gmail.com', 1, 'Sample address goes here..!', '6745628827', '', '', '2023-03-16', 1, 0, 1),
(43, '', NULL, 0, 'JoshuaLiu@gmail.com', 'Joshua', 'Liu', '', 'JoshuaLiu@gmail.com', 1, 'Sample address goes here..!', '6745628828', '', '', '2023-03-16', 1, 0, 1),
(44, '', NULL, 0, 'JenniferCox@gmail.com', 'Jennifer', 'Cox', '', 'JenniferCox@gmail.com', 1, 'Sample address goes here..!', '6745628829', '', '', '2023-03-16', 1, 0, 1),
(45, '', NULL, 0, 'BrittanyPeterson@gmail.com', 'Brittany', 'Peterson', '', 'BrittanyPeterson@gmail.com', 1, 'Sample address goes here..!', '6745628830', '', '', '2023-03-16', 1, 0, 1),
(46, '', NULL, 0, 'KrystalDavis@gmail.com', 'Krystal', 'Davis', '', 'KrystalDavis@gmail.com', 1, 'Sample address goes here..!', '6745628831', '', '', '2023-03-16', 1, 0, 1),
(47, '', NULL, 0, 'GlenGarcia@gmail.com', 'Glen', 'Garcia', '', 'GlenGarcia@gmail.com', 1, 'Sample address goes here..!', '6745628832', '', '', '2023-03-16', 1, 0, 1),
(48, '', NULL, 0, 'GeorgeVargas@gmail.com', 'George', 'Vargas', '', 'GeorgeVargas@gmail.com', 1, 'Sample address goes here..!', '6745628833', '', '', '2023-03-16', 1, 0, 1),
(49, '', NULL, 0, 'SaraSaunders@gmail.com', 'Sara', 'Saunders', '', 'SaraSaunders@gmail.com', 1, 'Sample address goes here..!', '6745628834', '', '', '2023-03-16', 1, 0, 1),
(50, '', NULL, 0, 'DestinyTorres@gmail.com', 'Destiny', 'Torres', '', 'DestinyTorres@gmail.com', 1, 'Sample address goes here..!', '6745628835', '', '', '2023-03-16', 1, 0, 1),
(51, '', NULL, 0, 'JamesMiller@gmail.com', 'James', 'Miller', '', 'JamesMiller@gmail.com', 1, 'Sample address goes here..!', '6745628836', '', '', '2023-03-16', 1, 0, 1),
(52, '', NULL, 0, 'VictoriaJones@gmail.com', 'Victoria', 'Jones', '', 'VictoriaJones@gmail.com', 1, 'Sample address goes here..!', '6745628837', '', '', '2023-03-16', 1, 0, 1),
(53, '', NULL, 0, 'EmilyMiller@gmail.com', 'Emily', 'Miller', '', 'EmilyMiller@gmail.com', 1, 'Sample address goes here..!', '6745628838', '', '', '2023-03-16', 1, 0, 1),
(54, '', NULL, 0, 'KarenThompson@gmail.com', 'Karen', 'Thompson', '', 'KarenThompson@gmail.com', 1, 'Sample address goes here..!', '6745628839', '', '', '2023-03-16', 1, 0, 1),
(55, '', NULL, 0, 'MarkRobinson@gmail.com', 'Mark', 'Robinson', '', 'MarkRobinson@gmail.com', 1, 'Sample address goes here..!', '6745628840', '', '', '2023-03-16', 1, 0, 1),
(56, '', NULL, 0, 'KellyCarpenter@gmail.com', 'Kelly', 'Carpenter', '', 'KellyCarpenter@gmail.com', 1, 'Sample address goes here..!', '6745628841', '', '', '2023-03-16', 1, 0, 1),
(57, '', NULL, 0, 'MichaelHebert@gmail.com', 'Michael', 'Hebert', '', 'MichaelHebert@gmail.com', 1, 'Sample address goes here..!', '6745628842', '', '', '2023-03-16', 1, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_userfollowing`
--

CREATE TABLE `account_userfollowing` (
  `id` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `following_user_id_id` int NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_userfollowing`
--

INSERT INTO `account_userfollowing` (`id`, `created`, `following_user_id_id`, `user_id`) VALUES
(4, '2023-02-11 09:44:11.018342', 3, 6),
(9, '2023-02-13 18:14:20.203174', 7, 5),
(10, '2023-02-13 18:14:29.249935', 2, 7),
(11, '2023-03-13 15:49:15.633040', 3, 2),
(12, '2023-03-15 14:40:16.740595', 7, 6),
(13, '2023-03-15 14:40:27.625492', 2, 6),
(14, '2023-03-15 14:40:28.953257', 4, 6),
(15, '2023-03-15 15:11:06.648318', 5, 6),
(16, '2023-03-16 16:45:52.900071', 11, 2),
(17, '2023-03-16 16:45:55.484604', 9, 2),
(18, '2023-03-16 16:48:12.177526', 57, 2),
(19, '2023-03-16 16:48:13.647452', 55, 2),
(20, '2023-03-16 16:48:14.970339', 53, 2),
(21, '2023-03-17 11:16:29.335218', 30, 2),
(22, '2023-03-17 11:16:31.527671', 29, 2),
(23, '2023-03-17 11:16:33.825147', 31, 2);

-- --------------------------------------------------------

--
-- Table structure for table `account_user_groups`
--

CREATE TABLE `account_user_groups` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `account_user_groups`
--

INSERT INTO `account_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 2, 1),
(2, 3, 1),
(3, 4, 1),
(4, 5, 3),
(5, 6, 4),
(6, 7, 2),
(7, 8, 1),
(8, 9, 1),
(9, 10, 1),
(10, 11, 1),
(11, 12, 1),
(12, 13, 1),
(13, 14, 1),
(14, 15, 1),
(15, 16, 1),
(16, 17, 1),
(17, 18, 1),
(18, 19, 1),
(19, 20, 1),
(20, 21, 1),
(21, 22, 1),
(22, 23, 1),
(23, 24, 1),
(24, 25, 1),
(25, 26, 1),
(26, 27, 1),
(27, 28, 1),
(28, 29, 1),
(29, 30, 1),
(30, 31, 1),
(31, 32, 1),
(32, 33, 1),
(33, 34, 1),
(34, 35, 1),
(35, 36, 1),
(36, 37, 1),
(37, 38, 1),
(38, 39, 1),
(39, 40, 1),
(40, 41, 1),
(41, 42, 1),
(42, 43, 1),
(43, 44, 1),
(44, 45, 1),
(45, 46, 1),
(46, 47, 1),
(47, 48, 1),
(48, 49, 1),
(49, 50, 1),
(50, 51, 1),
(51, 52, 1),
(52, 53, 1),
(53, 54, 1),
(54, 55, 1),
(55, 56, 1),
(56, 57, 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_user_user_permissions`
--

CREATE TABLE `account_user_user_permissions` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(4, 'Band'),
(3, 'Event Organizer'),
(2, 'Music School'),
(1, 'Musician');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `auth_permission`
--

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
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_user'),
(22, 'Can change user', 6, 'change_user'),
(23, 'Can delete user', 6, 'delete_user'),
(24, 'Can view user', 6, 'view_user'),
(25, 'Can add blocked_ user', 7, 'add_blocked_user'),
(26, 'Can change blocked_ user', 7, 'change_blocked_user'),
(27, 'Can delete blocked_ user', 7, 'delete_blocked_user'),
(28, 'Can view blocked_ user', 7, 'view_blocked_user'),
(29, 'Can add chat', 8, 'add_chat'),
(30, 'Can change chat', 8, 'change_chat'),
(31, 'Can delete chat', 8, 'delete_chat'),
(32, 'Can view chat', 8, 'view_chat'),
(33, 'Can add conversation', 9, 'add_conversation'),
(34, 'Can change conversation', 9, 'change_conversation'),
(35, 'Can delete conversation', 9, 'delete_conversation'),
(36, 'Can view conversation', 9, 'view_conversation'),
(37, 'Can add course', 10, 'add_course'),
(38, 'Can change course', 10, 'change_course'),
(39, 'Can delete course', 10, 'delete_course'),
(40, 'Can view course', 10, 'view_course'),
(41, 'Can add event_ organizer', 11, 'add_event_organizer'),
(42, 'Can change event_ organizer', 11, 'change_event_organizer'),
(43, 'Can delete event_ organizer', 11, 'delete_event_organizer'),
(44, 'Can view event_ organizer', 11, 'view_event_organizer'),
(45, 'Can add event_ organizer_ highlight', 12, 'add_event_organizer_highlight'),
(46, 'Can change event_ organizer_ highlight', 12, 'change_event_organizer_highlight'),
(47, 'Can delete event_ organizer_ highlight', 12, 'delete_event_organizer_highlight'),
(48, 'Can view event_ organizer_ highlight', 12, 'view_event_organizer_highlight'),
(49, 'Can add event_ performer', 13, 'add_event_performer'),
(50, 'Can change event_ performer', 13, 'change_event_performer'),
(51, 'Can delete event_ performer', 13, 'delete_event_performer'),
(52, 'Can view event_ performer', 13, 'view_event_performer'),
(53, 'Can add gurukulam', 14, 'add_gurukulam'),
(54, 'Can change gurukulam', 14, 'change_gurukulam'),
(55, 'Can delete gurukulam', 14, 'delete_gurukulam'),
(56, 'Can view gurukulam', 14, 'view_gurukulam'),
(57, 'Can add gurukulam_ award', 15, 'add_gurukulam_award'),
(58, 'Can change gurukulam_ award', 15, 'change_gurukulam_award'),
(59, 'Can delete gurukulam_ award', 15, 'delete_gurukulam_award'),
(60, 'Can view gurukulam_ award', 15, 'view_gurukulam_award'),
(61, 'Can add gurukulam_ skill', 16, 'add_gurukulam_skill'),
(62, 'Can change gurukulam_ skill', 16, 'change_gurukulam_skill'),
(63, 'Can delete gurukulam_ skill', 16, 'delete_gurukulam_skill'),
(64, 'Can view gurukulam_ skill', 16, 'view_gurukulam_skill'),
(65, 'Can add gurukulam_ teacher', 17, 'add_gurukulam_teacher'),
(66, 'Can change gurukulam_ teacher', 17, 'change_gurukulam_teacher'),
(67, 'Can delete gurukulam_ teacher', 17, 'delete_gurukulam_teacher'),
(68, 'Can view gurukulam_ teacher', 17, 'view_gurukulam_teacher'),
(69, 'Can add gurukulam_ testimonial', 18, 'add_gurukulam_testimonial'),
(70, 'Can change gurukulam_ testimonial', 18, 'change_gurukulam_testimonial'),
(71, 'Can delete gurukulam_ testimonial', 18, 'delete_gurukulam_testimonial'),
(72, 'Can view gurukulam_ testimonial', 18, 'view_gurukulam_testimonial'),
(73, 'Can add highlight', 19, 'add_highlight'),
(74, 'Can change highlight', 19, 'change_highlight'),
(75, 'Can delete highlight', 19, 'delete_highlight'),
(76, 'Can view highlight', 19, 'view_highlight'),
(77, 'Can add highlight_ category', 20, 'add_highlight_category'),
(78, 'Can change highlight_ category', 20, 'change_highlight_category'),
(79, 'Can delete highlight_ category', 20, 'delete_highlight_category'),
(80, 'Can view highlight_ category', 20, 'view_highlight_category'),
(81, 'Can add key_ performer', 21, 'add_key_performer'),
(82, 'Can change key_ performer', 21, 'change_key_performer'),
(83, 'Can delete key_ performer', 21, 'delete_key_performer'),
(84, 'Can view key_ performer', 21, 'view_key_performer'),
(85, 'Can add lecture_ video', 22, 'add_lecture_video'),
(86, 'Can change lecture_ video', 22, 'change_lecture_video'),
(87, 'Can delete lecture_ video', 22, 'delete_lecture_video'),
(88, 'Can view lecture_ video', 22, 'view_lecture_video'),
(89, 'Can add musician', 23, 'add_musician'),
(90, 'Can change musician', 23, 'change_musician'),
(91, 'Can delete musician', 23, 'delete_musician'),
(92, 'Can view musician', 23, 'view_musician'),
(93, 'Can add musician_ award', 24, 'add_musician_award'),
(94, 'Can change musician_ award', 24, 'change_musician_award'),
(95, 'Can delete musician_ award', 24, 'delete_musician_award'),
(96, 'Can view musician_ award', 24, 'view_musician_award'),
(97, 'Can add musician_ gurukulam', 25, 'add_musician_gurukulam'),
(98, 'Can change musician_ gurukulam', 25, 'change_musician_gurukulam'),
(99, 'Can delete musician_ gurukulam', 25, 'delete_musician_gurukulam'),
(100, 'Can view musician_ gurukulam', 25, 'view_musician_gurukulam'),
(101, 'Can add musician_ highlight', 26, 'add_musician_highlight'),
(102, 'Can change musician_ highlight', 26, 'change_musician_highlight'),
(103, 'Can delete musician_ highlight', 26, 'delete_musician_highlight'),
(104, 'Can view musician_ highlight', 26, 'view_musician_highlight'),
(105, 'Can add musician_ skill', 27, 'add_musician_skill'),
(106, 'Can change musician_ skill', 27, 'change_musician_skill'),
(107, 'Can delete musician_ skill', 27, 'delete_musician_skill'),
(108, 'Can view musician_ skill', 27, 'view_musician_skill'),
(109, 'Can add post', 28, 'add_post'),
(110, 'Can change post', 28, 'change_post'),
(111, 'Can delete post', 28, 'delete_post'),
(112, 'Can view post', 28, 'view_post'),
(113, 'Can add post_ comment', 29, 'add_post_comment'),
(114, 'Can change post_ comment', 29, 'change_post_comment'),
(115, 'Can delete post_ comment', 29, 'delete_post_comment'),
(116, 'Can view post_ comment', 29, 'view_post_comment'),
(117, 'Can add skill', 30, 'add_skill'),
(118, 'Can change skill', 30, 'change_skill'),
(119, 'Can delete skill', 30, 'delete_skill'),
(120, 'Can view skill', 30, 'view_skill'),
(121, 'Can add skill_ category', 31, 'add_skill_category'),
(122, 'Can change skill_ category', 31, 'change_skill_category'),
(123, 'Can delete skill_ category', 31, 'delete_skill_category'),
(124, 'Can view skill_ category', 31, 'view_skill_category'),
(125, 'Can add skill_ level', 32, 'add_skill_level'),
(126, 'Can change skill_ level', 32, 'change_skill_level'),
(127, 'Can delete skill_ level', 32, 'delete_skill_level'),
(128, 'Can view skill_ level', 32, 'view_skill_level'),
(129, 'Can add troupe', 33, 'add_troupe'),
(130, 'Can change troupe', 33, 'change_troupe'),
(131, 'Can delete troupe', 33, 'delete_troupe'),
(132, 'Can view troupe', 33, 'view_troupe'),
(133, 'Can add user following', 34, 'add_userfollowing'),
(134, 'Can change user following', 34, 'change_userfollowing'),
(135, 'Can delete user following', 34, 'delete_userfollowing'),
(136, 'Can view user following', 34, 'view_userfollowing'),
(137, 'Can add troupe_ skill', 35, 'add_troupe_skill'),
(138, 'Can change troupe_ skill', 35, 'change_troupe_skill'),
(139, 'Can delete troupe_ skill', 35, 'delete_troupe_skill'),
(140, 'Can view troupe_ skill', 35, 'view_troupe_skill'),
(141, 'Can add troupe_ highlight', 36, 'add_troupe_highlight'),
(142, 'Can change troupe_ highlight', 36, 'change_troupe_highlight'),
(143, 'Can delete troupe_ highlight', 36, 'delete_troupe_highlight'),
(144, 'Can view troupe_ highlight', 36, 'view_troupe_highlight'),
(145, 'Can add report_ people', 37, 'add_report_people'),
(146, 'Can change report_ people', 37, 'change_report_people'),
(147, 'Can delete report_ people', 37, 'delete_report_people'),
(148, 'Can view report_ people', 37, 'view_report_people'),
(149, 'Can add reply', 38, 'add_reply'),
(150, 'Can change reply', 38, 'change_reply'),
(151, 'Can delete reply', 38, 'delete_reply'),
(152, 'Can view reply', 38, 'view_reply'),
(153, 'Can add location', 39, 'add_location'),
(154, 'Can change location', 39, 'change_location'),
(155, 'Can delete location', 39, 'delete_location'),
(156, 'Can view location', 39, 'view_location'),
(157, 'Can add event', 40, 'add_event'),
(158, 'Can change event', 40, 'change_event'),
(159, 'Can delete event', 40, 'delete_event'),
(160, 'Can view event', 40, 'view_event'),
(161, 'Can add event_ category', 41, 'add_event_category'),
(162, 'Can change event_ category', 41, 'change_event_category'),
(163, 'Can delete event_ category', 41, 'delete_event_category'),
(164, 'Can view event_ category', 41, 'view_event_category'),
(165, 'Can add event_ type', 42, 'add_event_type'),
(166, 'Can change event_ type', 42, 'change_event_type'),
(167, 'Can delete event_ type', 42, 'delete_event_type'),
(168, 'Can view event_ type', 42, 'view_event_type'),
(169, 'Can add interest', 43, 'add_interest'),
(170, 'Can change interest', 43, 'change_interest'),
(171, 'Can delete interest', 43, 'delete_interest'),
(172, 'Can view interest', 43, 'view_interest'),
(173, 'Can add invitation', 44, 'add_invitation'),
(174, 'Can change invitation', 44, 'change_invitation'),
(175, 'Can delete invitation', 44, 'delete_invitation'),
(176, 'Can view invitation', 44, 'view_invitation'),
(177, 'Can add subscription_ type', 45, 'add_subscription_type'),
(178, 'Can change subscription_ type', 45, 'change_subscription_type'),
(179, 'Can delete subscription_ type', 45, 'delete_subscription_type'),
(180, 'Can view subscription_ type', 45, 'view_subscription_type'),
(181, 'Can add subscription', 46, 'add_subscription'),
(182, 'Can change subscription', 46, 'change_subscription'),
(183, 'Can delete subscription', 46, 'delete_subscription'),
(184, 'Can view subscription', 46, 'view_subscription'),
(185, 'Can add message', 47, 'add_message'),
(186, 'Can change message', 47, 'change_message'),
(187, 'Can delete message', 47, 'delete_message'),
(188, 'Can view message', 47, 'view_message'),
(189, 'Can add event_ skill', 48, 'add_event_skill'),
(190, 'Can change event_ skill', 48, 'change_event_skill'),
(191, 'Can delete event_ skill', 48, 'delete_event_skill'),
(192, 'Can view event_ skill', 48, 'view_event_skill');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL
) ;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2023-02-11 08:50:49.649668', '1', 'Musician', 1, '[{\"added\": {}}]', 3, 1),
(2, '2023-02-11 08:51:08.423776', '2', 'Music School', 1, '[{\"added\": {}}]', 3, 1),
(3, '2023-02-11 08:51:58.230940', '3', 'Event Organizer', 1, '[{\"added\": {}}]', 3, 1),
(4, '2023-02-11 08:52:20.045380', '4', 'Band', 1, '[{\"added\": {}}]', 3, 1),
(5, '2023-02-11 08:53:12.057152', '1', 'Coimbatore', 1, '[{\"added\": {}}]', 39, 1),
(6, '2023-02-11 08:53:27.244623', '2', 'Erode', 1, '[{\"added\": {}}]', 39, 1),
(7, '2023-02-11 08:54:12.664703', '1', 'Vocal', 1, '[{\"added\": {}}]', 31, 1),
(8, '2023-02-11 08:54:15.277459', '1', 'Carnatic', 1, '[{\"added\": {}}]', 30, 1),
(9, '2023-02-11 08:55:03.918726', '2', 'Instrument', 1, '[{\"added\": {}}]', 31, 1),
(10, '2023-02-11 08:55:05.585975', '2', 'Veena', 1, '[{\"added\": {}}]', 30, 1),
(11, '2023-02-11 08:55:33.853351', '3', 'Flute', 1, '[{\"added\": {}}]', 30, 1),
(12, '2023-02-11 08:55:33.931307', '4', 'Flute', 1, '[{\"added\": {}}]', 30, 1),
(13, '2023-02-11 08:56:35.921780', '2', 'Raja Gunasekaran', 1, '[{\"added\": {}}]', 6, 1),
(14, '2023-02-11 08:56:53.371954', '1', 'Raja Gunasekaran', 1, '[{\"added\": {}}]', 23, 1),
(15, '2023-02-11 08:59:30.201858', '2', 'Raja Gunasekaran', 2, '[{\"changed\": {\"fields\": [\"Profile picture\"]}}]', 6, 1),
(16, '2023-02-11 08:59:32.695990', '1', 'Raja Gunasekaran', 2, '[]', 23, 1),
(17, '2023-02-11 09:01:16.701361', '3', 'Karthick Stu', 1, '[{\"added\": {}}]', 6, 1),
(18, '2023-02-11 09:02:45.639841', '4', 'Sachin', 1, '[{\"added\": {}}]', 6, 1),
(19, '2023-02-11 09:02:59.536254', '2', 'Karthick Stu', 1, '[{\"added\": {}}]', 23, 1),
(20, '2023-02-11 09:03:04.482606', '3', 'Sachin', 1, '[{\"added\": {}}]', 23, 1),
(21, '2023-02-11 09:08:56.622470', '5', 'GPK Eventer', 1, '[{\"added\": {}}]', 6, 1),
(22, '2023-02-11 09:09:17.182275', '1', 'GPK Eventer', 1, '[{\"added\": {}}]', 11, 1),
(23, '2023-02-11 09:11:42.557679', '1', 'Contest', 1, '[{\"added\": {}}]', 41, 1),
(24, '2023-02-11 09:12:13.235084', '2', 'Orchestra', 1, '[{\"added\": {}}]', 41, 1),
(25, '2023-02-11 09:12:49.877365', '3', 'Bhajan', 1, '[{\"added\": {}}]', 41, 1),
(26, '2023-02-11 09:13:46.846074', '1', 'Online', 1, '[{\"added\": {}}]', 42, 1),
(27, '2023-02-11 09:13:52.318356', '2', 'Offline', 1, '[{\"added\": {}}]', 42, 1),
(28, '2023-02-11 09:26:04.118508', '1', 'Pro', 1, '[{\"added\": {}}]', 32, 1),
(29, '2023-02-11 09:26:45.402295', '2', 'Performer', 1, '[{\"added\": {}}]', 32, 1),
(30, '2023-02-11 09:26:55.336419', '3', 'Amateur', 1, '[{\"added\": {}}]', 32, 1),
(31, '2023-02-11 09:27:20.587698', '4', 'Flute', 3, '', 30, 1),
(32, '2023-02-11 09:35:42.250730', '6', 'Junkyard Groove', 1, '[{\"added\": {}}]', 6, 1),
(33, '2023-02-11 09:36:20.609695', '1', 'Junkyard Groove', 1, '[{\"added\": {}}]', 33, 1),
(34, '2023-02-11 09:47:22.788507', '7', 'PMA School of Music P Ltd', 1, '[{\"added\": {}}]', 6, 1),
(35, '2023-02-11 09:47:39.109696', '1', 'PMA School of Music P Ltd', 1, '[{\"added\": {}}]', 14, 1),
(36, '2023-02-13 11:54:41.984078', '1', 'Event_Performer object (1)', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 13, 1),
(37, '2023-02-13 11:55:17.440080', '1', 'Event_Performer object (1)', 2, '[]', 13, 1),
(38, '2023-02-13 17:43:22.929713', '3', 'Sachin', 2, '[{\"changed\": {\"fields\": [\"status\"]}}]', 21, 1),
(39, '2023-02-13 17:43:35.756101', '2', 'Karthick Stu', 2, '[{\"changed\": {\"fields\": [\"status\"]}}]', 21, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(7, 'account', 'blocked_user'),
(8, 'account', 'chat'),
(9, 'account', 'conversation'),
(10, 'account', 'course'),
(11, 'account', 'event_organizer'),
(12, 'account', 'event_organizer_highlight'),
(13, 'account', 'event_performer'),
(14, 'account', 'gurukulam'),
(15, 'account', 'gurukulam_award'),
(16, 'account', 'gurukulam_skill'),
(17, 'account', 'gurukulam_teacher'),
(18, 'account', 'gurukulam_testimonial'),
(19, 'account', 'highlight'),
(20, 'account', 'highlight_category'),
(21, 'account', 'key_performer'),
(22, 'account', 'lecture_video'),
(39, 'account', 'location'),
(23, 'account', 'musician'),
(24, 'account', 'musician_award'),
(25, 'account', 'musician_gurukulam'),
(26, 'account', 'musician_highlight'),
(27, 'account', 'musician_skill'),
(28, 'account', 'post'),
(29, 'account', 'post_comment'),
(38, 'account', 'reply'),
(37, 'account', 'report_people'),
(30, 'account', 'skill'),
(31, 'account', 'skill_category'),
(32, 'account', 'skill_level'),
(33, 'account', 'troupe'),
(36, 'account', 'troupe_highlight'),
(35, 'account', 'troupe_skill'),
(6, 'account', 'user'),
(34, 'account', 'userfollowing'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(40, 'event', 'event'),
(41, 'event', 'event_category'),
(48, 'event', 'event_skill'),
(42, 'event', 'event_type'),
(43, 'event', 'interest'),
(44, 'event', 'invitation'),
(47, 'event', 'message'),
(46, 'event', 'subscription'),
(45, 'event', 'subscription_type'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int NOT NULL,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'account', '0001_initial', '2023-02-10 16:49:14.884417'),
(2, 'event', '0001_initial', '2023-02-10 16:49:37.147295'),
(3, 'contenttypes', '0001_initial', '2023-02-10 16:49:37.506392'),
(4, 'contenttypes', '0002_remove_content_type_name', '2023-02-10 16:49:38.242400'),
(5, 'auth', '0001_initial', '2023-02-10 16:49:42.318329'),
(6, 'auth', '0002_alter_permission_name_max_length', '2023-02-10 16:49:43.288203'),
(7, 'auth', '0003_alter_user_email_max_length', '2023-02-10 16:49:43.339972'),
(8, 'auth', '0004_alter_user_username_opts', '2023-02-10 16:49:43.374004'),
(9, 'auth', '0005_alter_user_last_login_null', '2023-02-10 16:49:43.434244'),
(10, 'auth', '0006_require_contenttypes_0002', '2023-02-10 16:49:43.502016'),
(11, 'auth', '0007_alter_validators_add_error_messages', '2023-02-10 16:49:43.556830'),
(12, 'auth', '0008_alter_user_username_max_length', '2023-02-10 16:49:43.594459'),
(13, 'auth', '0009_alter_user_last_name_max_length', '2023-02-10 16:49:43.628455'),
(14, 'auth', '0010_alter_group_name_max_length', '2023-02-10 16:49:43.818939'),
(15, 'auth', '0011_update_proxy_permissions', '2023-02-10 16:49:44.100182'),
(16, 'auth', '0012_alter_user_first_name_max_length', '2023-02-10 16:49:44.153283'),
(17, 'account', '0002_initial', '2023-02-10 16:50:34.719906'),
(18, 'account', '0003_musician_skill_performing', '2023-02-10 16:50:34.954806'),
(19, 'account', '0004_location_remove_user_city_remove_user_district', '2023-02-10 16:50:37.103587'),
(20, 'event', '0002_remove_event_city_remove_event_district_and_more', '2023-02-10 16:50:39.530374'),
(21, 'account', '0005_delete_city_user_location_alter_post_location_and_more', '2023-02-10 16:50:42.794627'),
(22, 'account', '0006_remove_highlight_highlight_category_and_more', '2023-02-10 16:50:43.968089'),
(23, 'account', '0007_remove_post_musician_highlight_post_highlight', '2023-02-10 16:50:46.568348'),
(24, 'account', '0008_rename_performing_musician_skill_perform', '2023-02-10 16:50:47.005627'),
(25, 'account', '0009_alter_troupe_user_alter_troupe_skill_troupe', '2023-02-10 16:50:47.134604'),
(26, 'admin', '0001_initial', '2023-02-10 16:50:49.916528'),
(27, 'admin', '0002_logentry_remove_auto_add', '2023-02-10 16:50:49.993069'),
(28, 'admin', '0003_logentry_add_action_flag_choices', '2023-02-10 16:50:50.033989'),
(29, 'event', '0003_event_auto_accept', '2023-02-10 16:50:50.186780'),
(30, 'sessions', '0001_initial', '2023-02-10 16:50:50.677800');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0keu37nb77i4n5nzlhrpk4m0jrgazke6', 'NmIwODFmNmE4ZWJhNTEwZDgzMTAzZjI0NTczOGRjMWIwMGIxNzQ3NDp7Il9hdXRoX3VzZXJfaGFzaCI6IjVkYTczNjQwMjg1YzU0ZDZiMDZiY2JjNDNhMDM4ZjlhYzI1YjA4ZDgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI1In0=', '2023-04-18 09:22:29.050473'),
('13azwwhvfzlihu19gvwbjzfu1h0w54rc', 'NmIwODFmNmE4ZWJhNTEwZDgzMTAzZjI0NTczOGRjMWIwMGIxNzQ3NDp7Il9hdXRoX3VzZXJfaGFzaCI6IjVkYTczNjQwMjg1YzU0ZDZiMDZiY2JjNDNhMDM4ZjlhYzI1YjA4ZDgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI1In0=', '2023-02-27 18:10:38.374690'),
('3npfeyyjkhcdl7bjxvu8e9a646thny89', 'Y2QwMmZlZjNjYmQwYjU2ZjRjMWNmZGVhZDhkZmIyZWNmNTZkMTFlNTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiODc0NDdiYjMxZTI4OTFhY2VjY2I4YjdmMjAyMDdlMTIzODk3ODBhNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2023-04-05 09:06:55.163020'),
('6ithsqu0dqdex154jasim4s1e3mddbx1', '.eJxVjDsOwyAQBe9CHSHW5psyvc-AFhaCkwgkY1dR7h5bcpG0b2bem3nc1uK3nhY_E7sywy6_W8D4TPUA9MB6bzy2ui5z4IfCT9r51Ci9bqf7d1Cwl70WKBTk0SpSAYlolC4HEzVQhjA4q6UzzqDUADrbbEkMEXZROQNRjY59vukXN7c:1pQjn8:JI8KrXBxV0fippaSNzJXLD1qfmBhbpCRNHMBRDHTrbI', '2023-02-25 12:25:22.439972'),
('6ql2j2l3gi3b7kmbmat9bcbu0bnl83fl', 'NDg4ZGJkYWExYjVkYzdlOGZjNTViYWRlODJlZTYzNmY3ZjlhYmM2MDp7Il9hdXRoX3VzZXJfaGFzaCI6IjVkYTczNjQwMjg1YzU0ZDZiMDZiY2JjNDNhMDM4ZjlhYzI1YjA4ZDgiLCJfYXV0aF91c2VyX2lkIjoiNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2023-04-05 09:21:17.259854'),
('78799aj6qpgdcksy3wdgsxudbxpk1s71', '.eJxVjDsOwjAQBe_iGln-ZW0o6XMGa3dt4wBypDipEHeHSCmgfTPzXiLitta49bzEKYmL0OL0uxHyI7cdpDu22yx5busykdwVedAuxznl5_Vw_w4q9vqtFRdAGwJ4QAYDjm0oarDOeaUzYg7aF8cGDFsiJPBeDZBUAX2mBEm8P9A2N54:1pQgP2:7UmnCffzuN5kIAb21HqX4bHZp1Lp5yhYpxznfrLyzDc', '2023-02-25 08:48:16.392832'),
('852tu0dzlgc807ywqmg9rbii54cpsec5', '.eJxVjDsOwyAQBe9CHSHW5psyvc-AFhaCkwgkY1dR7h5bcpG0b2bem3nc1uK3nhY_E7sywy6_W8D4TPUA9MB6bzy2ui5z4IfCT9r51Ci9bqf7d1Cwl70WKBTk0SpSAYlolC4HEzVQhjA4q6UzzqDUADrbbEkMEXZROQNRjY59vukXN7c:1pQhKf:cEnWt2azYueVvO5P-MBnTHSQFWujcrVesu-LmisNfWk', '2023-02-25 09:47:49.982999'),
('8af8s8dxv7m2kipg0cu8rlyiq9ynwj5v', '.eJxVjDsOwjAQBe_iGln-ZW0o6XMGa3dt4wBypDipEHeHSCmgfTPzXiLitta49bzEKYmL0OL0uxHyI7cdpDu22yx5busykdwVedAuxznl5_Vw_w4q9vqtFRdAGwJ4QAYDjm0oarDOeaUzYg7aF8cGDFsiJPBeDZBUAX2mBEm8P9A2N54:1pRSGO:3k-zQf6MTb5iXmzdv1n865JkFgG3tuBRTbmkSWqQzDM', '2023-02-27 11:54:32.752621'),
('aj9u0sjia5dy17j8n99o58s9in1s3fmk', 'NzJhZmU0Nzc0NmFhMTgyNzc3M2JkN2NhOTIxNTg1MzE2MjhhMjI2ODp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZmI4ODU2MDMzNGM0MGNkYjZlZDk1NDY0NDY3NjkwYmE2NjYxOWQ4ZCIsIl9hdXRoX3VzZXJfaWQiOiI3In0=', '2023-02-27 17:46:10.582490'),
('isusp72m1aoz9ohpyltyi0knt2nwmk75', 'MGU4ZDFjY2QxMDQ2ZTJlNGVhNzQ1MjMyYzRjNmQ0ZDExZWI1NzBlMzp7Il9hdXRoX3VzZXJfaGFzaCI6IjdkY2JkZGRlMzFjZmFlNjlkODZhZDM0N2VhNGY4NWRjYjkzNTdjM2YiLCJfYXV0aF91c2VyX2lkIjoiMyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2023-04-18 10:54:14.570956'),
('l67jm3dsuvzivcdhbyioolepfy6d61m7', '.eJxVjDsOwjAQBe_iGln-ZW0o6XMGa3dt4wBypDipEHeHSCmgfTPzXiLitta49bzEKYmL0OL0uxHyI7cdpDu22yx5busykdwVedAuxznl5_Vw_w4q9vqtFRdAGwJ4QAYDjm0oarDOeaUzYg7aF8cGDFsiJPBeDZBUAX2mBEm8P9A2N54:1pQhaQ:R6df4OgAkxBCkTAgK9sITHHE-ras2BSzNBy93XO3VvY', '2023-02-25 10:04:06.949040'),
('ludlg1p732anqm9j5qmpb0b6hoywoera', 'MGM5ZTI2NDg3Y2UzZWZkZDg4OWFiNzhhYmMzNmFkMWQxNGNjNWU0ZTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiY2QyNGE1MzZjZjY4MTlhYjA3OGI4NWNjYmQwYjJhMWY5ZjkyZTRkNSIsIl9hdXRoX3VzZXJfaWQiOiIxIiwidGVtcF9sb2NhdGlvbiI6IjEifQ==', '2023-02-27 18:25:01.491132'),
('mpfsavq9bqossd2l5mqk60slssqeue73', '.eJxVjDsOwjAQBe_iGln476WkzxmsXXuDA8iR4qRC3B0ipYD2zcx7iYTbWtPWeUlTERfhxOl3I8wPbjsod2y3Wea5rctEclfkQbsc5sLP6-H-HVTs9VsHNqCd0WEctSWLXM6QPRNpp1RhH5QNlsBbB8WjyZmyNTGoqKMBQBDvD9t7N1w:1pQjj2:Q76jF9xLCHlmvTt2VsiZlW6KhPTpwhOAP582J4P1Kig', '2023-02-25 12:21:08.539460'),
('nw2afi4fzg6hnhevg1iap3iyaw91j9x3', '.eJxVjMEOwiAQRP-FsyFIhQWP3vsNhN0FqRpISnsy_rtt0oMeZ96beYsQ16WEtac5TCyuQovTb4eRnqnugB-x3pukVpd5Qrkr8qBdjo3T63a4fwcl9rKtXUStMIMjx8YqT9rkCASoiNC7LV0GZTIajZ69Y7aQ7ZABzhopJRCfL_agOHs:1pQilc:8eN26dcG-IFat2slgHvteNkNATMUY0hBC4z_TeNYtlg', '2023-02-25 11:19:44.479627'),
('pfn21ehmnk24v5776te3d3gl6w2lk5ct', 'Y2QwMmZlZjNjYmQwYjU2ZjRjMWNmZGVhZDhkZmIyZWNmNTZkMTFlNTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiODc0NDdiYjMxZTI4OTFhY2VjY2I4YjdmMjAyMDdlMTIzODk3ODBhNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2023-04-11 10:47:43.173031'),
('pn8tf84wa1jfb58qsrpk9g04uh664nig', 'Y2QwMmZlZjNjYmQwYjU2ZjRjMWNmZGVhZDhkZmIyZWNmNTZkMTFlNTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiODc0NDdiYjMxZTI4OTFhY2VjY2I4YjdmMjAyMDdlMTIzODk3ODBhNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2023-04-12 11:48:43.722332'),
('s5a68yilsybcnzmge8q6r0dv41ro9cli', 'YTU1ZDBlZTMxMjhmOWU4NGMxNDMyYzRiNjljYjQzNGIzZDg3ZmZhMDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjUiLCJfYXV0aF91c2VyX2hhc2giOiI1ZGE3MzY0MDI4NWM1NGQ2YjA2YmNiYzQzYTAzOGY5YWMyNWIwOGQ4In0=', '2023-04-18 14:07:30.637055'),
('slhsvlk3pzh76ph35jnkl9bjijgzvy5r', 'Y2QwMmZlZjNjYmQwYjU2ZjRjMWNmZGVhZDhkZmIyZWNmNTZkMTFlNTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9oYXNoIjoiODc0NDdiYjMxZTI4OTFhY2VjY2I4YjdmMjAyMDdlMTIzODk3ODBhNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2023-04-08 17:12:54.370767'),
('sotu6jgjsjmyuj8zf76oslb85o0kmte3', '.eJxVjMEOwiAQRP-FsyFIhQWP3vsNhN0FqRpISnsy_rtt0oMeZ96beYsQ16WEtac5TCyuQovTb4eRnqnugB-x3pukVpd5Qrkr8qBdjo3T63a4fwcl9rKtXUStMIMjx8YqT9rkCASoiNC7LV0GZTIajZ69Y7aQ7ZABzhopJRCfL_agOHs:1pQmUF:KXd-fp9vqX0uOZ85dsPPOhXNR7NpoqSbK1F0083wuho', '2023-02-25 15:18:03.617579'),
('utl7gcz3egqbhbvnl1labyua8m7a9hxd', 'MzliZWNkOTQ3OTlkMTgwNjgxNTMxZmM5Y2MwYTBhYjIzNzU4OGY3Nzp7Il9hdXRoX3VzZXJfaGFzaCI6Ijg3NDQ3YmIzMWUyODkxYWNlY2NiOGI3ZjIwMjA3ZTEyMzg5NzgwYTUiLCJ0ZW1wX2xvY2F0aW9uIjoiMSIsIl9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQifQ==', '2023-04-13 13:51:33.850708'),
('xb8v1f2w2obu60sg3kogj0wkjcwwalk8', 'YTU1ZDBlZTMxMjhmOWU4NGMxNDMyYzRiNjljYjQzNGIzZDg3ZmZhMDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjUiLCJfYXV0aF91c2VyX2hhc2giOiI1ZGE3MzY0MDI4NWM1NGQ2YjA2YmNiYzQzYTAzOGY5YWMyNWIwOGQ4In0=', '2023-04-18 12:28:46.734095'),
('y34k9e6ix30jlval5y8c7cy0i5hpfzkt', '.eJxVjMEOwiAQRP-FsyFIhQWP3vsNhN0FqRpISnsy_rtt0oMeZ96beYsQ16WEtac5TCyuQovTb4eRnqnugB-x3pukVpd5Qrkr8qBdjo3T63a4fwcl9rKtXUStMIMjx8YqT9rkCASoiNC7LV0GZTIajZ69Y7aQ7ZABzhopJRCfL_agOHs:1pQhN0:lJ1LdkrHeBEKBtfQ-gil2BIgE62sofKwAuQUSpfIPqo', '2023-02-25 09:50:14.734349');

-- --------------------------------------------------------

--
-- Table structure for table `event_event`
--

CREATE TABLE `event_event` (
  `id` int NOT NULL,
  `name` varchar(300) COLLATE utf8mb4_general_ci NOT NULL,
  `event_details` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `from_date` datetime(6) DEFAULT NULL,
  `to_date` datetime(6) DEFAULT NULL,
  `created_on` datetime(6) NOT NULL,
  `poster_image` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `registration_close_date` date DEFAULT NULL,
  `venue` varchar(300) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `self_reference` tinyint(1) NOT NULL,
  `highlight` longtext COLLATE utf8mb4_general_ci,
  `event_category_id` int NOT NULL,
  `event_organizer_id` int DEFAULT NULL,
  `event_type_id` int NOT NULL,
  `gurukulam_id` int DEFAULT NULL,
  `location_id` int DEFAULT NULL,
  `auto_accept` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `event_event`
--

INSERT INTO `event_event` (`id`, `name`, `event_details`, `from_date`, `to_date`, `created_on`, `poster_image`, `registration_close_date`, `venue`, `self_reference`, `highlight`, `event_category_id`, `event_organizer_id`, `event_type_id`, `gurukulam_id`, `location_id`, `auto_accept`) VALUES
(1, 'Blackbox Music Festival', 'It should come as no surprise to see the jewel in Barcelona\'s crown on this list. Year after year the festival pulls together an incredible lineup unencumbered by genre boundaries, uniting alternative favourites and discerning music fans from across the globe in the beachside Parc del Fòrum.', '2023-03-31 09:20:00.000000', '2023-04-20 20:30:00.000000', '2023-04-04 09:23:27.784060', 'event_poster/e713d0_7d3ed96fefba4d7692566f63f3e21afc_mv2_DQrOo8A.webp', '2023-04-21', 'Coimbatore', 0, 'It should come as no surprise to see the jewel in Barcelona\'s crown on this list. Year after year the festival pulls together an incredible lineup unencumbered by genre boundaries, uniting alternative favourites and discerning music fans from across the globe in the beachside Parc del Fòrum.', 1, 1, 1, NULL, 1, 1),
(2, 'Primavera Sound', 'It should come as no surprise to see the jewel in Barcelona\'s crown on this list. Year after year the festival pulls together an incredible lineup unencumbered by genre boundaries, uniting alternative favourites and discerning music fans from across the globe in the beachside Parc del Fòrum.', '2023-04-12 12:19:00.000000', '2023-04-21 09:24:00.000000', '2023-04-04 09:23:40.367096', 'event_poster/e713d0_37be41bd18d240d3b212488f9f6c99e8_mv2_1_UeJ88Us.webp', '2023-04-30', 'Coimbatore', 0, 'It should come as no surprise to see the jewel in Barcelona\'s crown on this list. Year after year the festival pulls together an incredible lineup unencumbered by genre boundaries, uniting alternative favourites and discerning music fans from across the globe in the beachside Parc del Fòrum.', 1, 1, 1, NULL, 1, 0),
(3, 'Coachella Music & Arts Festival', 'Is there really anything we could tell you about Coachella that you don\'t already know? It\'s a great big melting pot (California in April is more than hot enough) of fashion, A-list music, giant art structures and super grammable moments wherever you look. If this list were numbered, Coachella would definitely be circling the top spot. When & where: 15-17 & 22-24 April 2022; Indio', '2023-04-29 11:25:00.000000', '2023-04-30 11:25:00.000000', '2023-03-22 09:15:36.340430', 'event_poster/event_2_USSDGO4_HtogQ7c.png', '2023-04-28', 'Kinathukadavu', 0, 'Is there really anything we could tell you about Coachella that you don\'t already know? It\'s a great big melting pot (California in April is more than hot enough) of fashion, A-list music, giant art structures and super grammable moments wherever you look. If this list were numbered, Coachella would definitely be circling the top spot. When & where: 15-17 & 22-24 April 2022; Indio', 2, 1, 1, NULL, 1, 0),
(4, 'Montreux Jazz Festival', 'Held every year since 1967, there is no older festival on this list. What\'s more, few others anywhere in the world can boast such an impressive alumnus of previous performers, from Miles Davis, B.B. King and Nina Simone through to David Bowie, Bob Dylan and Queen. To this day the Lake Geneva shoreline is a hub for creative talent from across the globe, performing in venues throughout the Swiss city.', '2023-04-13 12:30:00.000000', '2023-04-20 14:30:00.000000', '2023-03-22 09:18:15.756229', 'event_poster/Top50MusicFestivalsintheWorld_Coachella_zjOF9Su.jpg', '2023-04-12', 'Pollachi', 0, 'Held every year since 1967, there is no older festival on this list. What\'s more, few others anywhere in the world can boast such an impressive alumnus of previous performers, from Miles Davis, B.B. King and Nina Simone through to David Bowie, Bob Dylan and Queen. To this day the Lake Geneva shoreline is a hub for creative talent from across the globe, performing in venues throughout the Swiss city.', 1, 1, 1, NULL, 1, 0),
(5, 'Bilbao BBK Live', 'Up in in the enchanting woodlands and lush greenery of Mount Cobetas – aka Kobetamendi – you\'ll find Bilbao BBK Live. Merging the intimacy of the verdant setting with lineups that boast generation-defining musical talent from several genres, it\'s no surprise that the festival has fans flocking back to the mountain each summer.', '2023-04-01 13:35:00.000000', '2023-04-02 12:35:00.000000', '2023-03-22 09:10:59.237641', 'event_poster/Top50MusicFestivalsintheWorld_LetItRoll_rI63Tyl.jpg', '2023-03-31', 'Metupalayam', 0, 'Up in in the enchanting woodlands and lush greenery of Mount Cobetas – aka Kobetamendi – you\'ll find Bilbao BBK Live. Merging the intimacy of the verdant setting with lineups that boast generation-defining musical talent from several genres, it\'s no surprise that the festival has fans flocking back to the mountain each summer.', 1, 1, 1, NULL, 1, 0),
(6, 'Mahindra Blues Festival', 'The Mahindra Blues Festival is not just another music festival.\r\nIt’s a cultural movement.\r\n\r\nIn the last 11 years of its existence, the Mahindra Blues Festival has put the blues genre on the global map and is one of the largest blues festivals in Asia. The Mahindra Blues community is one of the largest online communities, with over 2,00,000 plus followers. An iconic 70-year Bollywood Studio is the home of The Mahindra Blues Festival and is held annually in the second weekend of February.\r\n\r\nNot just Indian audiences but folks from all over the world have been regulars at the Mahindra Blues Festival for the last decade. The festival vibe across the multiple music stages, courtyard, and garden is accompanied by world-class food courts and malts, which completes the beautiful ambience.\r\n\r\nThis 2-day celebration is a feast for the mind, body, and soul with world-renowned musical legends setting the stage with soulful tunes that will keep your grooving and swaying throughout the night.\r\n\r\nGrab your tickets now and stay tuned for more updates very soon.', '2023-03-04 12:10:00.000000', '2023-03-05 12:10:00.000000', '2023-02-11 10:08:48.343116', 'event_poster/Rampage_YTrz5rx.jpeg', '2023-03-01', 'Coimbatore', 1, 'The Mahindra Blues Festival is not just another music festival.\r\nIt’s a cultural movement.\r\n\r\nIn the last 11 years of its existence, the Mahindra Blues Festival has put the blues genre on the global map and is one of the largest blues festivals in Asia. The Mahindra Blues community is one of the largest online communities, with over 2,00,000 plus followers. An iconic 70-year Bollywood Studio is the home of The Mahindra Blues Festival and is held annually in the second weekend of February.\r\n\r\nNot just Indian audiences but folks from all over the world have been regulars at the Mahindra Blues Festival for the last decade. The festival vibe across the multiple music stages, courtyard, and garden is accompanied by world-class food courts and malts, which completes the beautiful ambience.\r\n\r\nThis 2-day celebration is a feast for the mind, body, and soul with world-renowned musical legends setting the stage with soulful tunes that will keep your grooving and swaying throughout the night.\r\n\r\nGrab your tickets now and stay tuned for more updates very soon.', 1, NULL, 1, 1, 1, 0),
(7, 'YOURWAYS YOUTH FESTIVAL', 'Yourways India is going to organize YOURWAYS YOUTH FESTIVAL and it will be the biggest event in Delhi after COVID. In this event, we are introducing multiple categories like; Fashion Show, Dance Battles, Band Performances, DJ Nights with DJ RAVATOR, DJ KHUSHI, DJ DNA, Nukkad Natak, Exhibitions, Food Stalls, Fun Section for Kids, Marathon & a live Concert with SAAHEL, RCR RAPSTAR & GURNAZAR. It\'s a charity event where we are sharing a free platform with talents. We are going to reestablish our Free Education center in South Delhi again through this fund and we need your love & support to finish this event with huge success!', '2023-03-10 13:20:00.000000', '2023-03-12 15:30:00.000000', '2023-02-11 10:19:39.783602', '', '2023-03-09', 'Coimbatore', 1, 'Yourways India is going to organize YOURWAYS YOUTH FESTIVAL and it will be the biggest event in Delhi after COVID. In this event, we are introducing multiple categories like; Fashion Show, Dance Battles, Band Performances, DJ Nights with DJ RAVATOR, DJ KHUSHI, DJ DNA, Nukkad Natak, Exhibitions, Food Stalls, Fun Section for Kids, Marathon & a live Concert with SAAHEL, RCR RAPSTAR & GURNAZAR. It\'s a charity event where we are sharing a free platform with talents. We are going to reestablish our Free Education center in South Delhi again through this fund and we need your love & support to finish this event with huge success!', 1, NULL, 1, NULL, 1, 0),
(8, 'YOURWAYS YOUTH FESTIVAL', 'Yourways India is going to organize YOURWAYS YOUTH FESTIVAL and it will be the biggest event in Delhi after COVID. In this event, we are introducing multiple categories like; Fashion Show, Dance Battles, Band Performances, DJ Nights with DJ RAVATOR, DJ KHUSHI, DJ DNA, Nukkad Natak, Exhibitions, Food Stalls, Fun Section for Kids, Marathon & a live Concert with SAAHEL, RCR RAPSTAR & GURNAZAR. It\'s a charity event where we are sharing a free platform with talents. We are going to reestablish our Free Education center in South Delhi again through this fund and we need your love & support to finish this event with huge success!', '2023-03-10 13:20:00.000000', '2023-03-12 15:30:00.000000', '2023-02-11 10:19:39.837334', '', '2023-03-09', 'Coimbatore', 1, 'Yourways India is going to organize YOURWAYS YOUTH FESTIVAL and it will be the biggest event in Delhi after COVID. In this event, we are introducing multiple categories like; Fashion Show, Dance Battles, Band Performances, DJ Nights with DJ RAVATOR, DJ KHUSHI, DJ DNA, Nukkad Natak, Exhibitions, Food Stalls, Fun Section for Kids, Marathon & a live Concert with SAAHEL, RCR RAPSTAR & GURNAZAR. It\'s a charity event where we are sharing a free platform with talents. We are going to reestablish our Free Education center in South Delhi again through this fund and we need your love & support to finish this event with huge success!', 1, NULL, 1, NULL, 1, 0),
(9, 'YOURWAYS YOUTH FESTIVAL', 'Yourways India is going to organize YOURWAYS YOUTH FESTIVAL and it will be the biggest event in Delhi after COVID. In this event, we are introducing multiple categories like; Fashion Show, Dance Battles, Band Performances, DJ Nights with DJ RAVATOR, DJ KHUSHI, DJ DNA, Nukkad Natak, Exhibitions, Food Stalls, Fun Section for Kids, Marathon & a live Concert with SAAHEL, RCR RAPSTAR & GURNAZAR. It\'s a charity event where we are sharing a free platform with talents. We are going to reestablish our Free Education center in South Delhi again through this fund and we need your love & support to finish this event with huge success!', '2023-03-10 13:20:00.000000', '2023-03-12 15:30:00.000000', '2023-02-11 10:24:46.175802', 'event_poster/Top50MusicFestivalsintheWorld_MadCool_QxXWHnD.jpg', '2023-03-09', 'Coimbatore', 0, 'Yourways India is going to organize YOURWAYS YOUTH FESTIVAL and it will be the biggest event in Delhi after COVID. In this event, we are introducing multiple categories like; Fashion Show, Dance Battles, Band Performances, DJ Nights with DJ RAVATOR, DJ KHUSHI, DJ DNA, Nukkad Natak, Exhibitions, Food Stalls, Fun Section for Kids, Marathon & a live Concert with SAAHEL, RCR RAPSTAR & GURNAZAR. It\'s a charity event where we are sharing a free platform with talents. We are going to reestablish our Free Education center in South Delhi again through this fund and we need your love & support to finish this event with huge success!', 1, NULL, 1, 1, 1, 0),
(10, 'India Tour 2023 with Kenn Day', 'We will be visiting sites of spiritual and historical significance, natural beauty and cultural interest in Northern India. Our two-week trip will include first class accommodations, guided tours and opportunities to connect with the people and spirits of this ancient and amazing land.', '2023-04-20 20:30:00.000000', '2023-04-28 20:30:00.000000', '2023-03-22 09:14:26.634270', 'event_poster/Top50MusicFestivalsintheWorld_Coachella_zjOF9Su_nxcfohW.jpg', '2023-04-19', 'Erode', 0, 'We will be visiting sites of spiritual and historical significance, natural beauty and cultural interest in Northern India. Our two-week trip will include first class accommodations, guided tours and opportunities to connect with the people and spirits of this ancient and amazing land.', 1, 1, 1, NULL, 2, 1),
(11, 'Indian Music Experience Museum', 'Immerse yourself in India`s rich musical heritage at Bengaluru`s newest and most exciting cultural hub – the Indian Music Experience Museum (IME)!', '2023-02-15 20:50:00.000000', '2023-02-16 22:50:00.000000', '2023-02-13 17:47:56.394426', 'event_poster/Top50MusicFestivalsintheWorld_LetItRoll_5BJB9Rn.jpg', '2023-02-14', 'Erode', 0, 'Immerse yourself in India`s rich musical heritage at Bengaluru`s newest and most exciting cultural hub – the Indian Music Experience Museum (IME)!', 1, NULL, 1, 1, 2, 1),
(12, 'Indian Music Experience Museum', 'Immerse yourself in India`s rich musical heritage at Bengaluru`s newest and most exciting cultural hub – the Indian Music Experience Museum (IME)!', '2023-02-15 20:50:00.000000', '2023-02-16 22:50:00.000000', '2023-02-13 17:47:56.508761', 'event_poster/Top50MusicFestivalsintheWorld_LetItRoll_6CTOLuf.jpg', '2023-02-14', 'Erode', 0, 'Immerse yourself in India`s rich musical heritage at Bengaluru`s newest and most exciting cultural hub – the Indian Music Experience Museum (IME)!', 1, NULL, 1, 1, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `event_event_category`
--

CREATE TABLE `event_event_category` (
  `id` int NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `event_event_category`
--

INSERT INTO `event_event_category` (`id`, `name`) VALUES
(1, 'Contest'),
(2, 'Orchestra'),
(3, 'Bhajan');

-- --------------------------------------------------------

--
-- Table structure for table `event_event_skill`
--

CREATE TABLE `event_event_skill` (
  `id` int NOT NULL,
  `event_id` int NOT NULL,
  `skill_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `event_event_skill`
--

INSERT INTO `event_event_skill` (`id`, `event_id`, `skill_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 2, 2),
(5, 2, 3),
(6, 3, 2),
(7, 4, 2),
(8, 4, 1),
(9, 5, 1),
(10, 5, 3),
(11, 6, 1),
(12, 9, 1),
(13, 9, 2),
(14, 9, 3);

-- --------------------------------------------------------

--
-- Table structure for table `event_event_type`
--

CREATE TABLE `event_event_type` (
  `id` int NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `event_event_type`
--

INSERT INTO `event_event_type` (`id`, `name`) VALUES
(1, 'Online'),
(2, 'Offline');

-- --------------------------------------------------------

--
-- Table structure for table `event_interest`
--

CREATE TABLE `event_interest` (
  `id` int NOT NULL,
  `status` varchar(1) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `timestamp` datetime(6) DEFAULT NULL,
  `event_id` int DEFAULT NULL,
  `musician_id` int DEFAULT NULL,
  `troupe_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `event_interest`
--

INSERT INTO `event_interest` (`id`, `status`, `timestamp`, `event_id`, `musician_id`, `troupe_id`) VALUES
(1, 'A', '2023-02-11 09:42:59.836959', 5, NULL, 1),
(2, 'A', '2023-02-11 09:42:59.954746', 4, NULL, 1),
(4, 'R', '2023-02-13 17:45:12.050330', 3, NULL, 1),
(6, 'S', '2023-03-29 12:46:40.769565', 4, 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `event_invitation`
--

CREATE TABLE `event_invitation` (
  `id` int NOT NULL,
  `status` varchar(1) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `event_id` int DEFAULT NULL,
  `gurukulam_id` int DEFAULT NULL,
  `musician_id` int DEFAULT NULL,
  `troupe_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `event_invitation`
--

INSERT INTO `event_invitation` (`id`, `status`, `timestamp`, `event_id`, `gurukulam_id`, `musician_id`, `troupe_id`) VALUES
(1, 'A', '2023-02-11 09:17:43.210351', 1, NULL, 1, NULL),
(2, 'A', '2023-02-11 09:17:43.303020', 1, NULL, 2, NULL),
(3, 'A', '2023-02-11 09:17:43.424963', 1, NULL, 3, NULL),
(4, 'A', '2023-02-13 17:25:29.824029', 10, NULL, 1, NULL),
(5, 'A', '2023-02-13 17:25:29.830699', 10, NULL, 2, NULL),
(6, 'A', '2023-02-13 17:25:29.833630', 10, NULL, 3, NULL),
(7, 'A', '2023-02-13 17:25:29.837686', 10, NULL, NULL, 1),
(8, 'A', '2023-02-13 17:47:56.398523', 11, NULL, 2, NULL),
(9, 'A', '2023-02-13 17:47:56.402576', 11, NULL, 3, NULL),
(10, 'A', '2023-02-13 17:47:56.519258', 12, NULL, 2, NULL),
(11, 'A', '2023-02-13 17:47:56.528401', 12, NULL, 3, NULL),
(12, 'S', '2023-04-04 14:08:33.162109', 3, NULL, 4, NULL),
(13, 'S', '2023-04-04 14:08:33.199595', 3, NULL, 7, NULL),
(14, 'S', '2023-04-04 14:08:55.390396', 3, NULL, 8, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `event_message`
--

CREATE TABLE `event_message` (
  `id` int NOT NULL,
  `text` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `sent_on` datetime(6) NOT NULL,
  `unread` tinyint(1) NOT NULL,
  `interest_id` int DEFAULT NULL,
  `invitation_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

--
-- Dumping data for table `event_message`
--

INSERT INTO `event_message` (`id`, `text`, `sent_on`, `unread`, `interest_id`, `invitation_id`, `user_id`) VALUES
(1, '', '2023-02-11 09:17:43.267269', 0, NULL, 1, 5),
(2, '', '2023-02-11 09:17:43.325517', 1, NULL, 2, 5),
(3, '', '2023-02-11 09:17:43.441291', 1, NULL, 3, 5),
(4, 'Hai Hello this is ', '2023-02-11 09:33:42.158245', 1, NULL, 1, 2),
(5, 'Hai Hello this is ', '2023-02-11 09:33:42.315716', 1, NULL, 1, 2),
(6, 'I like to ', '2023-02-11 09:42:59.887603', 0, 1, NULL, 6),
(7, 'I like to ', '2023-02-11 09:42:59.989214', 0, 2, NULL, 6),
(8, 'Join us dood', '2023-02-11 09:44:49.023400', 0, 1, NULL, 5),
(9, 'Join us dood', '2023-02-11 09:46:07.891111', 1, 2, NULL, 5),
(10, 'Any questions I can help clear up for you as you’re testing out your free trial? :)\n\n', '2023-02-13 17:15:00.401671', 1, NULL, 1, 2),
(11, 'Any questions I can help clear up for you as you’re testing out your free trial? :)\n\n', '2023-02-13 17:15:01.112800', 1, NULL, 1, 2),
(13, '', '2023-02-13 17:25:29.827652', 0, NULL, 4, 5),
(14, '', '2023-02-13 17:25:29.831672', 1, NULL, 5, 5),
(15, '', '2023-02-13 17:25:29.834537', 1, NULL, 6, 5),
(16, '', '2023-02-13 17:25:29.838681', 0, NULL, 7, 5),
(17, 'Hello team, I am interesting', '2023-02-13 17:45:12.051646', 0, 4, NULL, 6),
(18, 'Hi hello this is sample message', '2023-02-13 17:45:41.884527', 1, NULL, 7, 6),
(19, 'Hi hello this is sample message', '2023-02-13 17:45:42.282785', 1, NULL, 7, 6),
(20, '', '2023-02-13 17:47:56.399821', 1, NULL, 8, 7),
(21, '', '2023-02-13 17:47:56.403603', 1, NULL, 9, 7),
(22, '', '2023-02-13 17:47:56.520682', 1, NULL, 10, 7),
(23, '', '2023-02-13 17:47:56.530993', 1, NULL, 11, 7),
(25, 'Interested', '2023-03-29 12:46:40.770939', 1, 6, NULL, 2),
(26, 'hi', '2023-04-04 14:08:33.163568', 1, NULL, 12, 5),
(27, 'hi', '2023-04-04 14:08:33.200747', 1, NULL, 13, 5),
(28, 'hi', '2023-04-04 14:08:55.391608', 1, NULL, 14, 5),
(29, 'hi', '2023-04-04 14:10:46.653090', 1, 4, NULL, 5);

-- --------------------------------------------------------

--
-- Table structure for table `event_subscription`
--

CREATE TABLE `event_subscription` (
  `id` int NOT NULL,
  `subscription_date` date NOT NULL,
  `active` tinyint(1) NOT NULL,
  `event_organizer_id` int DEFAULT NULL,
  `gurukulam_id` int DEFAULT NULL,
  `musician_id` int DEFAULT NULL,
  `subscription_type_id` int NOT NULL,
  `troupe_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci TABLESPACE `madhanumk_cmf`;

-- --------------------------------------------------------

--
-- Table structure for table `event_subscription_type`
--

CREATE TABLE `event_subscription_type` (
  `id` int NOT NULL,
  `name` varchar(60) COLLATE utf8mb4_general_ci NOT NULL,
  `price` double NOT NULL,
  `days` int UNSIGNED DEFAULT NULL
) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account_blocked_user`
--
ALTER TABLE `account_blocked_user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_blocked_user_blocked_by_id_fb2b209b_fk_account_user_id` (`blocked_by_id`),
  ADD KEY `account_blocked_user_blocked_user_id_784b3531_fk_account_user_id` (`blocked_user_id`);

--
-- Indexes for table `account_chat`
--
ALTER TABLE `account_chat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_chat_conversation_id_1c0aeeb5_fk_account_conversation_id` (`conversation_id`),
  ADD KEY `account_chat_sender_id_fa6c8461_fk_account_user_id` (`sender_id`);

--
-- Indexes for table `account_conversation`
--
ALTER TABLE `account_conversation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_conversation_receiver_id_02551a23_fk_account_user_id` (`receiver_id`),
  ADD KEY `account_conversation_sender_id_dc7e4fe3_fk_account_user_id` (`sender_id`);

--
-- Indexes for table `account_course`
--
ALTER TABLE `account_course`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_course_gurukulam_id_c30e76c1_fk_account_gurukulam_id` (`gurukulam_id`);

--
-- Indexes for table `account_event_organizer`
--
ALTER TABLE `account_event_organizer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `account_event_organizer_highlight`
--
ALTER TABLE `account_event_organizer_highlight`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_event_organi_event_organizer_id_ee7da733_fk_account_e` (`event_organizer_id`);

--
-- Indexes for table `account_event_organizer_highlight_highlight_category`
--
ALTER TABLE `account_event_organizer_highlight_highlight_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_event_organizer__event_organizer_highligh_eea97578_uniq` (`event_organizer_highlight_id`,`highlight_category_id`),
  ADD KEY `account_event_organi_highlight_category_i_a89da2b9_fk_account_h` (`highlight_category_id`);

--
-- Indexes for table `account_event_performer`
--
ALTER TABLE `account_event_performer`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_event_perfor_event_organizer_id_4ba3d1a9_fk_account_e` (`event_organizer_id`),
  ADD KEY `account_event_perfor_musician_id_94b5956b_fk_account_m` (`musician_id`),
  ADD KEY `account_event_performer_troupe_id_b7197768_fk_account_troupe_id` (`troupe_id`);

--
-- Indexes for table `account_gurukulam`
--
ALTER TABLE `account_gurukulam`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `account_gurukulam_award`
--
ALTER TABLE `account_gurukulam_award`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_gurukulam_aw_gurukulam_id_850a7a3f_fk_account_g` (`gurukulam_id`);

--
-- Indexes for table `account_gurukulam_skill`
--
ALTER TABLE `account_gurukulam_skill`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_gurukulam_sk_gurukulam_id_0ba6e386_fk_account_g` (`gurukulam_id`),
  ADD KEY `account_gurukulam_skill_skill_id_24272661_fk_account_skill_id` (`skill_id`);

--
-- Indexes for table `account_gurukulam_teacher`
--
ALTER TABLE `account_gurukulam_teacher`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_gurukulam_te_gurukulam_id_497566fc_fk_account_g` (`gurukulam_id`),
  ADD KEY `account_gurukulam_te_musician_id_9e009bec_fk_account_m` (`musician_id`),
  ADD KEY `account_gurukulam_teacher_sender_id_e043092d_fk_account_user_id` (`sender_id`);

--
-- Indexes for table `account_gurukulam_testimonial`
--
ALTER TABLE `account_gurukulam_testimonial`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_gurukulam_te_gurukulam_id_79482f84_fk_account_g` (`gurukulam_id`),
  ADD KEY `account_gurukulam_te_musician_id_9f02f948_fk_account_m` (`musician_id`);

--
-- Indexes for table `account_highlight`
--
ALTER TABLE `account_highlight`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_highlight_user_id_c3727fef_fk_account_user_id` (`user_id`);

--
-- Indexes for table `account_highlight_category`
--
ALTER TABLE `account_highlight_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `account_key_performer`
--
ALTER TABLE `account_key_performer`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_key_performe_musician_id_4f3ce56e_fk_account_m` (`musician_id`),
  ADD KEY `account_key_performer_troupe_id_22357981_fk_account_troupe_id` (`troupe_id`);

--
-- Indexes for table `account_lecture_video`
--
ALTER TABLE `account_lecture_video`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_lecture_vide_gurukulam_id_f04557b5_fk_account_g` (`gurukulam_id`);

--
-- Indexes for table `account_location`
--
ALTER TABLE `account_location`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `account_musician`
--
ALTER TABLE `account_musician`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `account_musician_award`
--
ALTER TABLE `account_musician_award`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_musician_awa_musician_id_e0ef4a28_fk_account_m` (`musician_id`);

--
-- Indexes for table `account_musician_gurukulam`
--
ALTER TABLE `account_musician_gurukulam`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_musician_gur_gurukulam_id_b795cd52_fk_account_g` (`gurukulam_id`),
  ADD KEY `account_musician_gur_musician_id_09828a77_fk_account_m` (`musician_id`),
  ADD KEY `account_musician_gurukulam_sender_id_825102b9_fk_account_user_id` (`sender_id`);

--
-- Indexes for table `account_musician_highlight`
--
ALTER TABLE `account_musician_highlight`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_musician_hig_musician_id_ded0d393_fk_account_m` (`musician_id`);

--
-- Indexes for table `account_musician_highlight_highlight_category`
--
ALTER TABLE `account_musician_highlight_highlight_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_musician_highlig_musician_highlight_id_hi_1d664573_uniq` (`musician_highlight_id`,`highlight_category_id`),
  ADD KEY `account_musician_hig_highlight_category_i_559c80d0_fk_account_h` (`highlight_category_id`);

--
-- Indexes for table `account_musician_skill`
--
ALTER TABLE `account_musician_skill`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_musician_ski_musician_id_3e2592f4_fk_account_m` (`musician_id`),
  ADD KEY `account_musician_skill_skill_id_bf54c683_fk_account_skill_id` (`skill_id`),
  ADD KEY `account_musician_ski_skill_level_id_4b3054c7_fk_account_s` (`skill_level_id`);

--
-- Indexes for table `account_post`
--
ALTER TABLE `account_post`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_post_interest_id_c518eff1_fk_event_interest_id` (`interest_id`),
  ADD KEY `account_post_invitation_id_b2033104_fk_event_invitation_id` (`invitation_id`),
  ADD KEY `account_post_user_id_7502b583_fk_account_user_id` (`user_id`),
  ADD KEY `account_post_location_id_d3c33d49_fk_account_location_id` (`location_id`),
  ADD KEY `account_post_highlight_id_f8829399_fk_account_highlight_id` (`highlight_id`);

--
-- Indexes for table `account_post_comment`
--
ALTER TABLE `account_post_comment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_post_comment_post_id_5ad1b7ee_fk_account_post_id` (`post_id`),
  ADD KEY `account_post_comment_user_id_75ed6427_fk_account_user_id` (`user_id`);

--
-- Indexes for table `account_post_user_likes`
--
ALTER TABLE `account_post_user_likes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_post_user_likes_post_id_user_id_75588e89_uniq` (`post_id`,`user_id`),
  ADD KEY `account_post_user_likes_user_id_9aeb685d_fk_account_user_id` (`user_id`);

--
-- Indexes for table `account_reply`
--
ALTER TABLE `account_reply`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_reply_comment_id_c8d4a568_fk_account_post_comment_id` (`comment_id`),
  ADD KEY `account_reply_user_id_794cc73d_fk_account_user_id` (`user_id`);

--
-- Indexes for table `account_report_people`
--
ALTER TABLE `account_report_people`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_report_people_reported_by_id_dd7f8473_fk_account_user_id` (`reported_by_id`),
  ADD KEY `account_report_peopl_reported_user_id_7826eddf_fk_account_u` (`reported_user_id`);

--
-- Indexes for table `account_skill`
--
ALTER TABLE `account_skill`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_skill_skill_category_id_bf8ebca3_fk_account_s` (`skill_category_id`);

--
-- Indexes for table `account_skill_category`
--
ALTER TABLE `account_skill_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `account_skill_level`
--
ALTER TABLE `account_skill_level`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `account_troupe`
--
ALTER TABLE `account_troupe`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `account_troupe_highlight`
--
ALTER TABLE `account_troupe_highlight`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_troupe_highlight_troupe_id_96aca7af_fk_account_troupe_id` (`troupe_id`);

--
-- Indexes for table `account_troupe_highlight_highlight_category`
--
ALTER TABLE `account_troupe_highlight_highlight_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_troupe_highlight_troupe_highlight_id_high_6fdb8af7_uniq` (`troupe_highlight_id`,`highlight_category_id`),
  ADD KEY `account_troupe_highl_highlight_category_i_3a241ccd_fk_account_h` (`highlight_category_id`);

--
-- Indexes for table `account_troupe_skill`
--
ALTER TABLE `account_troupe_skill`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_troupe_skill_skill_id_b99b4507_fk_account_skill_id` (`skill_id`),
  ADD KEY `account_troupe_skill_troupe_id_33de635d_fk_account_troupe_id` (`troupe_id`);

--
-- Indexes for table `account_user`
--
ALTER TABLE `account_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `account_user_location_id_621ee626_fk_account_location_id` (`location_id`);

--
-- Indexes for table `account_userfollowing`
--
ALTER TABLE `account_userfollowing`
  ADD PRIMARY KEY (`id`),
  ADD KEY `account_userfollowin_following_user_id_id_68485b1f_fk_account_u` (`following_user_id_id`),
  ADD KEY `account_userfollowing_user_id_3df84ba0_fk_account_user_id` (`user_id`);

--
-- Indexes for table `account_user_groups`
--
ALTER TABLE `account_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_user_groups_user_id_group_id_4d09af3e_uniq` (`user_id`,`group_id`),
  ADD KEY `account_user_groups_group_id_6c71f749_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `account_user_user_permissions`
--
ALTER TABLE `account_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account_user_user_permis_user_id_permission_id_48bdd28b_uniq` (`user_id`,`permission_id`),
  ADD KEY `account_user_user_pe_permission_id_66c44191_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_account_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `event_event`
--
ALTER TABLE `event_event`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_event_event_category_id_b55beb35_fk_event_eve` (`event_category_id`),
  ADD KEY `event_event_event_organizer_id_c15859a4_fk_account_e` (`event_organizer_id`),
  ADD KEY `event_event_event_type_id_6785b75f_fk_event_event_type_id` (`event_type_id`),
  ADD KEY `event_event_gurukulam_id_21da1427_fk_account_gurukulam_id` (`gurukulam_id`),
  ADD KEY `event_event_location_id_2e2c812f_fk_account_location_id` (`location_id`);

--
-- Indexes for table `event_event_category`
--
ALTER TABLE `event_event_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event_event_skill`
--
ALTER TABLE `event_event_skill`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_event_skill_event_id_0cf9dcd3_fk_event_event_id` (`event_id`),
  ADD KEY `event_event_skill_skill_id_15c4484a_fk_account_skill_id` (`skill_id`);

--
-- Indexes for table `event_event_type`
--
ALTER TABLE `event_event_type`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event_interest`
--
ALTER TABLE `event_interest`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_interest_event_id_5074cdfb_fk_event_event_id` (`event_id`),
  ADD KEY `event_interest_musician_id_36d45549_fk_account_musician_id` (`musician_id`),
  ADD KEY `event_interest_troupe_id_750ea202_fk_account_troupe_id` (`troupe_id`);

--
-- Indexes for table `event_invitation`
--
ALTER TABLE `event_invitation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_invitation_event_id_a24ec405_fk_event_event_id` (`event_id`),
  ADD KEY `event_invitation_gurukulam_id_8f1b096f_fk_account_gurukulam_id` (`gurukulam_id`),
  ADD KEY `event_invitation_musician_id_e42ae4fc_fk_account_musician_id` (`musician_id`),
  ADD KEY `event_invitation_troupe_id_aa0dfce1_fk_account_troupe_id` (`troupe_id`);

--
-- Indexes for table `event_message`
--
ALTER TABLE `event_message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_message_interest_id_a9db718a_fk_event_interest_id` (`interest_id`),
  ADD KEY `event_message_invitation_id_54885e43_fk_event_invitation_id` (`invitation_id`),
  ADD KEY `event_message_user_id_22eb54aa_fk_account_user_id` (`user_id`);

--
-- Indexes for table `event_subscription`
--
ALTER TABLE `event_subscription`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_subscription_event_organizer_id_3000e0a5_fk_account_e` (`event_organizer_id`),
  ADD KEY `event_subscription_gurukulam_id_5bdbe9e0_fk_account_gurukulam_id` (`gurukulam_id`),
  ADD KEY `event_subscription_musician_id_56a7eeae_fk_account_musician_id` (`musician_id`),
  ADD KEY `event_subscription_subscription_type_id_f5fd6fe2_fk_event_sub` (`subscription_type_id`),
  ADD KEY `event_subscription_troupe_id_528c2c8d_fk_account_troupe_id` (`troupe_id`);

--
-- Indexes for table `event_subscription_type`
--
ALTER TABLE `event_subscription_type`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account_blocked_user`
--
ALTER TABLE `account_blocked_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_chat`
--
ALTER TABLE `account_chat`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `account_conversation`
--
ALTER TABLE `account_conversation`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `account_course`
--
ALTER TABLE `account_course`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_event_organizer`
--
ALTER TABLE `account_event_organizer`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `account_event_organizer_highlight`
--
ALTER TABLE `account_event_organizer_highlight`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_event_organizer_highlight_highlight_category`
--
ALTER TABLE `account_event_organizer_highlight_highlight_category`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_event_performer`
--
ALTER TABLE `account_event_performer`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `account_gurukulam`
--
ALTER TABLE `account_gurukulam`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `account_gurukulam_award`
--
ALTER TABLE `account_gurukulam_award`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `account_gurukulam_skill`
--
ALTER TABLE `account_gurukulam_skill`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `account_gurukulam_teacher`
--
ALTER TABLE `account_gurukulam_teacher`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `account_gurukulam_testimonial`
--
ALTER TABLE `account_gurukulam_testimonial`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `account_highlight`
--
ALTER TABLE `account_highlight`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `account_highlight_category`
--
ALTER TABLE `account_highlight_category`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_key_performer`
--
ALTER TABLE `account_key_performer`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `account_lecture_video`
--
ALTER TABLE `account_lecture_video`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `account_location`
--
ALTER TABLE `account_location`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `account_musician`
--
ALTER TABLE `account_musician`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT for table `account_musician_award`
--
ALTER TABLE `account_musician_award`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `account_musician_gurukulam`
--
ALTER TABLE `account_musician_gurukulam`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `account_musician_highlight`
--
ALTER TABLE `account_musician_highlight`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_musician_highlight_highlight_category`
--
ALTER TABLE `account_musician_highlight_highlight_category`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_musician_skill`
--
ALTER TABLE `account_musician_skill`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT for table `account_post`
--
ALTER TABLE `account_post`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_post_comment`
--
ALTER TABLE `account_post_comment`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `account_post_user_likes`
--
ALTER TABLE `account_post_user_likes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `account_reply`
--
ALTER TABLE `account_reply`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_report_people`
--
ALTER TABLE `account_report_people`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_skill`
--
ALTER TABLE `account_skill`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `account_skill_category`
--
ALTER TABLE `account_skill_category`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `account_skill_level`
--
ALTER TABLE `account_skill_level`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `account_troupe`
--
ALTER TABLE `account_troupe`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `account_troupe_highlight`
--
ALTER TABLE `account_troupe_highlight`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_troupe_highlight_highlight_category`
--
ALTER TABLE `account_troupe_highlight_highlight_category`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `account_troupe_skill`
--
ALTER TABLE `account_troupe_skill`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `account_user`
--
ALTER TABLE `account_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `account_userfollowing`
--
ALTER TABLE `account_userfollowing`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `account_user_groups`
--
ALTER TABLE `account_user_groups`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `account_user_user_permissions`
--
ALTER TABLE `account_user_user_permissions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=193;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `event_event`
--
ALTER TABLE `event_event`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `event_event_category`
--
ALTER TABLE `event_event_category`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `event_event_skill`
--
ALTER TABLE `event_event_skill`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `event_event_type`
--
ALTER TABLE `event_event_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `event_interest`
--
ALTER TABLE `event_interest`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `event_invitation`
--
ALTER TABLE `event_invitation`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `event_message`
--
ALTER TABLE `event_message`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `event_subscription`
--
ALTER TABLE `event_subscription`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `event_subscription_type`
--
ALTER TABLE `event_subscription_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account_blocked_user`
--
ALTER TABLE `account_blocked_user`
  ADD CONSTRAINT `account_blocked_user_blocked_by_id_fb2b209b_fk_account_user_id` FOREIGN KEY (`blocked_by_id`) REFERENCES `account_user` (`id`),
  ADD CONSTRAINT `account_blocked_user_blocked_user_id_784b3531_fk_account_user_id` FOREIGN KEY (`blocked_user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_chat`
--
ALTER TABLE `account_chat`
  ADD CONSTRAINT `account_chat_conversation_id_1c0aeeb5_fk_account_conversation_id` FOREIGN KEY (`conversation_id`) REFERENCES `account_conversation` (`id`),
  ADD CONSTRAINT `account_chat_sender_id_fa6c8461_fk_account_user_id` FOREIGN KEY (`sender_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_conversation`
--
ALTER TABLE `account_conversation`
  ADD CONSTRAINT `account_conversation_receiver_id_02551a23_fk_account_user_id` FOREIGN KEY (`receiver_id`) REFERENCES `account_user` (`id`),
  ADD CONSTRAINT `account_conversation_sender_id_dc7e4fe3_fk_account_user_id` FOREIGN KEY (`sender_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_course`
--
ALTER TABLE `account_course`
  ADD CONSTRAINT `account_course_gurukulam_id_c30e76c1_fk_account_gurukulam_id` FOREIGN KEY (`gurukulam_id`) REFERENCES `account_gurukulam` (`id`);

--
-- Constraints for table `account_event_organizer`
--
ALTER TABLE `account_event_organizer`
  ADD CONSTRAINT `account_event_organizer_user_id_e6b2f5f9_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_event_organizer_highlight`
--
ALTER TABLE `account_event_organizer_highlight`
  ADD CONSTRAINT `account_event_organi_event_organizer_id_ee7da733_fk_account_e` FOREIGN KEY (`event_organizer_id`) REFERENCES `account_event_organizer` (`id`);

--
-- Constraints for table `account_event_organizer_highlight_highlight_category`
--
ALTER TABLE `account_event_organizer_highlight_highlight_category`
  ADD CONSTRAINT `account_event_organi_event_organizer_high_4748bb98_fk_account_e` FOREIGN KEY (`event_organizer_highlight_id`) REFERENCES `account_event_organizer_highlight` (`id`),
  ADD CONSTRAINT `account_event_organi_highlight_category_i_a89da2b9_fk_account_h` FOREIGN KEY (`highlight_category_id`) REFERENCES `account_highlight_category` (`id`);

--
-- Constraints for table `account_event_performer`
--
ALTER TABLE `account_event_performer`
  ADD CONSTRAINT `account_event_perfor_event_organizer_id_4ba3d1a9_fk_account_e` FOREIGN KEY (`event_organizer_id`) REFERENCES `account_event_organizer` (`id`),
  ADD CONSTRAINT `account_event_perfor_musician_id_94b5956b_fk_account_m` FOREIGN KEY (`musician_id`) REFERENCES `account_musician` (`id`),
  ADD CONSTRAINT `account_event_performer_troupe_id_b7197768_fk_account_troupe_id` FOREIGN KEY (`troupe_id`) REFERENCES `account_troupe` (`id`);

--
-- Constraints for table `account_gurukulam`
--
ALTER TABLE `account_gurukulam`
  ADD CONSTRAINT `account_gurukulam_user_id_e1f89a54_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_gurukulam_award`
--
ALTER TABLE `account_gurukulam_award`
  ADD CONSTRAINT `account_gurukulam_aw_gurukulam_id_850a7a3f_fk_account_g` FOREIGN KEY (`gurukulam_id`) REFERENCES `account_gurukulam` (`id`);

--
-- Constraints for table `account_gurukulam_skill`
--
ALTER TABLE `account_gurukulam_skill`
  ADD CONSTRAINT `account_gurukulam_sk_gurukulam_id_0ba6e386_fk_account_g` FOREIGN KEY (`gurukulam_id`) REFERENCES `account_gurukulam` (`id`),
  ADD CONSTRAINT `account_gurukulam_skill_skill_id_24272661_fk_account_skill_id` FOREIGN KEY (`skill_id`) REFERENCES `account_skill` (`id`);

--
-- Constraints for table `account_gurukulam_teacher`
--
ALTER TABLE `account_gurukulam_teacher`
  ADD CONSTRAINT `account_gurukulam_te_gurukulam_id_497566fc_fk_account_g` FOREIGN KEY (`gurukulam_id`) REFERENCES `account_gurukulam` (`id`),
  ADD CONSTRAINT `account_gurukulam_te_musician_id_9e009bec_fk_account_m` FOREIGN KEY (`musician_id`) REFERENCES `account_musician` (`id`),
  ADD CONSTRAINT `account_gurukulam_teacher_sender_id_e043092d_fk_account_user_id` FOREIGN KEY (`sender_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_gurukulam_testimonial`
--
ALTER TABLE `account_gurukulam_testimonial`
  ADD CONSTRAINT `account_gurukulam_te_gurukulam_id_79482f84_fk_account_g` FOREIGN KEY (`gurukulam_id`) REFERENCES `account_gurukulam` (`id`),
  ADD CONSTRAINT `account_gurukulam_te_musician_id_9f02f948_fk_account_m` FOREIGN KEY (`musician_id`) REFERENCES `account_musician` (`id`);

--
-- Constraints for table `account_highlight`
--
ALTER TABLE `account_highlight`
  ADD CONSTRAINT `account_highlight_user_id_c3727fef_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_key_performer`
--
ALTER TABLE `account_key_performer`
  ADD CONSTRAINT `account_key_performe_musician_id_4f3ce56e_fk_account_m` FOREIGN KEY (`musician_id`) REFERENCES `account_musician` (`id`),
  ADD CONSTRAINT `account_key_performer_troupe_id_22357981_fk_account_troupe_id` FOREIGN KEY (`troupe_id`) REFERENCES `account_troupe` (`id`);

--
-- Constraints for table `account_lecture_video`
--
ALTER TABLE `account_lecture_video`
  ADD CONSTRAINT `account_lecture_vide_gurukulam_id_f04557b5_fk_account_g` FOREIGN KEY (`gurukulam_id`) REFERENCES `account_gurukulam` (`id`);

--
-- Constraints for table `account_musician`
--
ALTER TABLE `account_musician`
  ADD CONSTRAINT `account_musician_user_id_7c662056_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_musician_award`
--
ALTER TABLE `account_musician_award`
  ADD CONSTRAINT `account_musician_awa_musician_id_e0ef4a28_fk_account_m` FOREIGN KEY (`musician_id`) REFERENCES `account_musician` (`id`);

--
-- Constraints for table `account_musician_gurukulam`
--
ALTER TABLE `account_musician_gurukulam`
  ADD CONSTRAINT `account_musician_gur_gurukulam_id_b795cd52_fk_account_g` FOREIGN KEY (`gurukulam_id`) REFERENCES `account_gurukulam` (`id`),
  ADD CONSTRAINT `account_musician_gur_musician_id_09828a77_fk_account_m` FOREIGN KEY (`musician_id`) REFERENCES `account_musician` (`id`),
  ADD CONSTRAINT `account_musician_gurukulam_sender_id_825102b9_fk_account_user_id` FOREIGN KEY (`sender_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_musician_highlight`
--
ALTER TABLE `account_musician_highlight`
  ADD CONSTRAINT `account_musician_hig_musician_id_ded0d393_fk_account_m` FOREIGN KEY (`musician_id`) REFERENCES `account_musician` (`id`);

--
-- Constraints for table `account_musician_highlight_highlight_category`
--
ALTER TABLE `account_musician_highlight_highlight_category`
  ADD CONSTRAINT `account_musician_hig_highlight_category_i_559c80d0_fk_account_h` FOREIGN KEY (`highlight_category_id`) REFERENCES `account_highlight_category` (`id`),
  ADD CONSTRAINT `account_musician_hig_musician_highlight_i_f95e60db_fk_account_m` FOREIGN KEY (`musician_highlight_id`) REFERENCES `account_musician_highlight` (`id`);

--
-- Constraints for table `account_musician_skill`
--
ALTER TABLE `account_musician_skill`
  ADD CONSTRAINT `account_musician_ski_musician_id_3e2592f4_fk_account_m` FOREIGN KEY (`musician_id`) REFERENCES `account_musician` (`id`),
  ADD CONSTRAINT `account_musician_ski_skill_level_id_4b3054c7_fk_account_s` FOREIGN KEY (`skill_level_id`) REFERENCES `account_skill_level` (`id`),
  ADD CONSTRAINT `account_musician_skill_skill_id_bf54c683_fk_account_skill_id` FOREIGN KEY (`skill_id`) REFERENCES `account_skill` (`id`);

--
-- Constraints for table `account_post`
--
ALTER TABLE `account_post`
  ADD CONSTRAINT `account_post_highlight_id_f8829399_fk_account_highlight_id` FOREIGN KEY (`highlight_id`) REFERENCES `account_highlight` (`id`),
  ADD CONSTRAINT `account_post_interest_id_c518eff1_fk_event_interest_id` FOREIGN KEY (`interest_id`) REFERENCES `event_interest` (`id`),
  ADD CONSTRAINT `account_post_invitation_id_b2033104_fk_event_invitation_id` FOREIGN KEY (`invitation_id`) REFERENCES `event_invitation` (`id`),
  ADD CONSTRAINT `account_post_location_id_d3c33d49_fk_account_location_id` FOREIGN KEY (`location_id`) REFERENCES `account_location` (`id`),
  ADD CONSTRAINT `account_post_user_id_7502b583_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_post_comment`
--
ALTER TABLE `account_post_comment`
  ADD CONSTRAINT `account_post_comment_post_id_5ad1b7ee_fk_account_post_id` FOREIGN KEY (`post_id`) REFERENCES `account_post` (`id`),
  ADD CONSTRAINT `account_post_comment_user_id_75ed6427_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_post_user_likes`
--
ALTER TABLE `account_post_user_likes`
  ADD CONSTRAINT `account_post_user_likes_post_id_c7a7fa9f_fk_account_post_id` FOREIGN KEY (`post_id`) REFERENCES `account_post` (`id`),
  ADD CONSTRAINT `account_post_user_likes_user_id_9aeb685d_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_reply`
--
ALTER TABLE `account_reply`
  ADD CONSTRAINT `account_reply_comment_id_c8d4a568_fk_account_post_comment_id` FOREIGN KEY (`comment_id`) REFERENCES `account_post_comment` (`id`),
  ADD CONSTRAINT `account_reply_user_id_794cc73d_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_report_people`
--
ALTER TABLE `account_report_people`
  ADD CONSTRAINT `account_report_peopl_reported_user_id_7826eddf_fk_account_u` FOREIGN KEY (`reported_user_id`) REFERENCES `account_user` (`id`),
  ADD CONSTRAINT `account_report_people_reported_by_id_dd7f8473_fk_account_user_id` FOREIGN KEY (`reported_by_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_skill`
--
ALTER TABLE `account_skill`
  ADD CONSTRAINT `account_skill_skill_category_id_bf8ebca3_fk_account_s` FOREIGN KEY (`skill_category_id`) REFERENCES `account_skill_category` (`id`);

--
-- Constraints for table `account_troupe`
--
ALTER TABLE `account_troupe`
  ADD CONSTRAINT `account_troupe_user_id_3741ee0f_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_troupe_highlight`
--
ALTER TABLE `account_troupe_highlight`
  ADD CONSTRAINT `account_troupe_highlight_troupe_id_96aca7af_fk_account_troupe_id` FOREIGN KEY (`troupe_id`) REFERENCES `account_troupe` (`id`);

--
-- Constraints for table `account_troupe_highlight_highlight_category`
--
ALTER TABLE `account_troupe_highlight_highlight_category`
  ADD CONSTRAINT `account_troupe_highl_highlight_category_i_3a241ccd_fk_account_h` FOREIGN KEY (`highlight_category_id`) REFERENCES `account_highlight_category` (`id`),
  ADD CONSTRAINT `account_troupe_highl_troupe_highlight_id_1d4a4ced_fk_account_t` FOREIGN KEY (`troupe_highlight_id`) REFERENCES `account_troupe_highlight` (`id`);

--
-- Constraints for table `account_troupe_skill`
--
ALTER TABLE `account_troupe_skill`
  ADD CONSTRAINT `account_troupe_skill_skill_id_b99b4507_fk_account_skill_id` FOREIGN KEY (`skill_id`) REFERENCES `account_skill` (`id`),
  ADD CONSTRAINT `account_troupe_skill_troupe_id_33de635d_fk_account_troupe_id` FOREIGN KEY (`troupe_id`) REFERENCES `account_troupe` (`id`);

--
-- Constraints for table `account_user`
--
ALTER TABLE `account_user`
  ADD CONSTRAINT `account_user_location_id_621ee626_fk_account_location_id` FOREIGN KEY (`location_id`) REFERENCES `account_location` (`id`);

--
-- Constraints for table `account_userfollowing`
--
ALTER TABLE `account_userfollowing`
  ADD CONSTRAINT `account_userfollowin_following_user_id_id_68485b1f_fk_account_u` FOREIGN KEY (`following_user_id_id`) REFERENCES `account_user` (`id`),
  ADD CONSTRAINT `account_userfollowing_user_id_3df84ba0_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_user_groups`
--
ALTER TABLE `account_user_groups`
  ADD CONSTRAINT `account_user_groups_group_id_6c71f749_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `account_user_groups_user_id_14345e7b_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `account_user_user_permissions`
--
ALTER TABLE `account_user_user_permissions`
  ADD CONSTRAINT `account_user_user_pe_permission_id_66c44191_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `account_user_user_pe_user_id_cc42d270_fk_account_u` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `event_event`
--
ALTER TABLE `event_event`
  ADD CONSTRAINT `event_event_event_category_id_b55beb35_fk_event_eve` FOREIGN KEY (`event_category_id`) REFERENCES `event_event_category` (`id`),
  ADD CONSTRAINT `event_event_event_organizer_id_c15859a4_fk_account_e` FOREIGN KEY (`event_organizer_id`) REFERENCES `account_event_organizer` (`id`),
  ADD CONSTRAINT `event_event_event_type_id_6785b75f_fk_event_event_type_id` FOREIGN KEY (`event_type_id`) REFERENCES `event_event_type` (`id`),
  ADD CONSTRAINT `event_event_gurukulam_id_21da1427_fk_account_gurukulam_id` FOREIGN KEY (`gurukulam_id`) REFERENCES `account_gurukulam` (`id`),
  ADD CONSTRAINT `event_event_location_id_2e2c812f_fk_account_location_id` FOREIGN KEY (`location_id`) REFERENCES `account_location` (`id`);

--
-- Constraints for table `event_event_skill`
--
ALTER TABLE `event_event_skill`
  ADD CONSTRAINT `event_event_skill_event_id_0cf9dcd3_fk_event_event_id` FOREIGN KEY (`event_id`) REFERENCES `event_event` (`id`),
  ADD CONSTRAINT `event_event_skill_skill_id_15c4484a_fk_account_skill_id` FOREIGN KEY (`skill_id`) REFERENCES `account_skill` (`id`);

--
-- Constraints for table `event_interest`
--
ALTER TABLE `event_interest`
  ADD CONSTRAINT `event_interest_event_id_5074cdfb_fk_event_event_id` FOREIGN KEY (`event_id`) REFERENCES `event_event` (`id`),
  ADD CONSTRAINT `event_interest_musician_id_36d45549_fk_account_musician_id` FOREIGN KEY (`musician_id`) REFERENCES `account_musician` (`id`),
  ADD CONSTRAINT `event_interest_troupe_id_750ea202_fk_account_troupe_id` FOREIGN KEY (`troupe_id`) REFERENCES `account_troupe` (`id`);

--
-- Constraints for table `event_invitation`
--
ALTER TABLE `event_invitation`
  ADD CONSTRAINT `event_invitation_event_id_a24ec405_fk_event_event_id` FOREIGN KEY (`event_id`) REFERENCES `event_event` (`id`),
  ADD CONSTRAINT `event_invitation_gurukulam_id_8f1b096f_fk_account_gurukulam_id` FOREIGN KEY (`gurukulam_id`) REFERENCES `account_gurukulam` (`id`),
  ADD CONSTRAINT `event_invitation_musician_id_e42ae4fc_fk_account_musician_id` FOREIGN KEY (`musician_id`) REFERENCES `account_musician` (`id`),
  ADD CONSTRAINT `event_invitation_troupe_id_aa0dfce1_fk_account_troupe_id` FOREIGN KEY (`troupe_id`) REFERENCES `account_troupe` (`id`);

--
-- Constraints for table `event_message`
--
ALTER TABLE `event_message`
  ADD CONSTRAINT `event_message_interest_id_a9db718a_fk_event_interest_id` FOREIGN KEY (`interest_id`) REFERENCES `event_interest` (`id`),
  ADD CONSTRAINT `event_message_invitation_id_54885e43_fk_event_invitation_id` FOREIGN KEY (`invitation_id`) REFERENCES `event_invitation` (`id`),
  ADD CONSTRAINT `event_message_user_id_22eb54aa_fk_account_user_id` FOREIGN KEY (`user_id`) REFERENCES `account_user` (`id`);

--
-- Constraints for table `event_subscription`
--
ALTER TABLE `event_subscription`
  ADD CONSTRAINT `event_subscription_event_organizer_id_3000e0a5_fk_account_e` FOREIGN KEY (`event_organizer_id`) REFERENCES `account_event_organizer` (`id`),
  ADD CONSTRAINT `event_subscription_gurukulam_id_5bdbe9e0_fk_account_gurukulam_id` FOREIGN KEY (`gurukulam_id`) REFERENCES `account_gurukulam` (`id`),
  ADD CONSTRAINT `event_subscription_musician_id_56a7eeae_fk_account_musician_id` FOREIGN KEY (`musician_id`) REFERENCES `account_musician` (`id`),
  ADD CONSTRAINT `event_subscription_subscription_type_id_f5fd6fe2_fk_event_sub` FOREIGN KEY (`subscription_type_id`) REFERENCES `event_subscription_type` (`id`),
  ADD CONSTRAINT `event_subscription_troupe_id_528c2c8d_fk_account_troupe_id` FOREIGN KEY (`troupe_id`) REFERENCES `account_troupe` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
