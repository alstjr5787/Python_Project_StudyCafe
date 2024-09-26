-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- 생성 시간: 24-09-27 00:10
-- 서버 버전: 8.0.36
-- PHP 버전: 8.2.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 데이터베이스: `jukson`
--

-- --------------------------------------------------------

--
-- 테이블 구조 `cafe_seat`
--

CREATE TABLE `cafe_seat` (
  `id` int NOT NULL,
  `start_time` datetime NOT NULL,
  `status` enum('true','false') NOT NULL,
  `scheduled_end_time` datetime DEFAULT NULL,
  `user_id` varchar(50) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 테이블의 덤프 데이터 `cafe_seat`
--

INSERT INTO `cafe_seat` (`id`, `start_time`, `status`, `scheduled_end_time`, `user_id`) VALUES
(1, '2024-09-26 23:14:26', 'true', '2024-09-27 01:14:26', 'jukson'),
(2, '2024-09-26 22:44:06', 'false', NULL, ''),
(3, '2024-09-26 20:20:54', 'false', NULL, ''),
(4, '2024-09-27 00:00:02', 'true', '2024-09-27 02:00:02', 'jukson'),
(5, '2024-09-26 22:18:16', 'false', NULL, ''),
(6, '2024-09-26 20:19:57', 'false', NULL, ''),
(7, '2024-09-26 18:38:29', 'false', NULL, NULL),
(8, '2024-09-26 12:30:00', 'false', NULL, NULL),
(9, '2024-09-26 13:00:00', 'false', NULL, NULL),
(10, '2024-09-26 13:30:00', 'false', NULL, NULL);

-- --------------------------------------------------------

--
-- 테이블 구조 `cafe_user`
--

CREATE TABLE `cafe_user` (
  `id` int NOT NULL,
  `member_id` varchar(255) NOT NULL,
  `member_password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `account_status` varchar(20) DEFAULT 'active',
  `suspension_end_date` datetime DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 테이블의 덤프 데이터 `cafe_user`
--

INSERT INTO `cafe_user` (`id`, `member_id`, `member_password`, `name`, `phone_number`, `account_status`, `suspension_end_date`) VALUES
(38, 'jukson', '$2y$10$KNMb6UyR8kCj4MNI96ObFe3T38.DbLO2/RZaaOynf3Stks0DK7cbK', '김민석', '01012341234', 'active', NULL),
(37, 'test6', '$2y$10$Dkg2MBHt6dw0XWqIjqL98ObW88GEmT.26ea9Fv6X1OfejtJFcLtVm', '김수미', '010-0001-0006', 'active', NULL),
(35, 'test4', '$2y$10$Dkg2MBHt6dw0XWqIjqL98ObW88GEmT.26ea9Fv6X1OfejtJFcLtVm', '이수', '010-0001-0004', 'active', NULL),
(36, 'test5', '$2y$10$Dkg2MBHt6dw0XWqIjqL98ObW88GEmT.26ea9Fv6X1OfejtJFcLtVm', '강진혁', '010-0001-0005', 'active', NULL),
(34, 'test3', '$2y$10$Dkg2MBHt6dw0XWqIjqL98ObW88GEmT.26ea9Fv6X1OfejtJFcLtVm', '김미나', '010-0001-0003', 'active', NULL),
(33, 'test2', '$2y$10$Dkg2MBHt6dw0XWqIjqL98ObW88GEmT.26ea9Fv6X1OfejtJFcLtVm', '홍길동', '010-0001-0002', 'active', NULL),
(32, 'test1', '$2y$10$Dkg2MBHt6dw0XWqIjqL98ObW88GEmT.26ea9Fv6X1OfejtJFcLtVm', '개나리', '010-0001-0001', 'active', NULL);

--
-- 덤프된 테이블의 인덱스
--

--
-- 테이블의 인덱스 `cafe_seat`
--
ALTER TABLE `cafe_seat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- 테이블의 인덱스 `cafe_user`
--
ALTER TABLE `cafe_user`
  ADD PRIMARY KEY (`id`);

--
-- 덤프된 테이블의 AUTO_INCREMENT
--

--
-- 테이블의 AUTO_INCREMENT `cafe_user`
--
ALTER TABLE `cafe_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
