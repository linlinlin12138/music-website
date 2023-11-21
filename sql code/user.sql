-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2023-04-30 06:15:42
-- 服务器版本： 10.4.27-MariaDB
-- PHP 版本： 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `music`
--

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `name` varchar(40) DEFAULT NULL,
  `e_mail` varchar(80) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `phone_number` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`user_id`, `name`, `e_mail`, `password`, `phone_number`) VALUES
(1, 'user1', '1234@qq.com', '1234', 12345678910),
(2, 'user2', '1235@qq.com', '1234', 12345678911),
(3, 'user3', '1236@qq.com', '1234', 12345678912),
(4, 'user4', '1237@qq.com', '1234', 12345678913),
(5, 'user5', '1238@qq.com', '1234', 12345678914),
(6, 'user6', '1239@qq.com', '1234', 12345678915),
(7, 'user7', '1240@qq.com', '1234', 12345678916),
(8, 'user8', '1241@qq.com', '1234', 12345678917),
(9, 'user9', '1242@qq.com', '1234', 12345678918),
(10, 'user10', '1243@qq.com', '1234', 12345678919);

--
-- 转储表的索引
--

--
-- 表的索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
