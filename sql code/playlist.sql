-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2023-04-30 06:15:26
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
-- 表的结构 `playlist`
--

CREATE TABLE `playlist` (
  `list_id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `photo_link` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 转存表中的数据 `playlist`
--

INSERT INTO `playlist` (`list_id`, `name`, `photo_link`) VALUES
(50, '[Lofi学习小组] 让音乐做你的同桌密友', 'http://p2.music.126.net/0TRWKG6SAwQVsTo0bBiM2g==/109951168300058148.jpg?param=140y140'),
(51, '[伴你入眠] 音乐代替爱人拥抱你', 'http://p2.music.126.net/D6-boayfBROgXYs27ocDJQ==/109951168540178923.jpg?param=140y140'),
(52, '[自习打卡] 开启心无杂念学习模式', 'http://p2.music.126.net/VOKhgqm8RE12yZHGDXL2VQ==/109951168539672779.jpg?param=140y140'),
(53, '[氛围梦乡] 带你去看霓虹色的梦', 'http://p2.music.126.net/MPk3ueg5xmdqpwACttjOAA==/109951168290378177.jpg?param=140y140'),
(54, '[沉浸式阅读] 在琴声中阅见自己', 'http://p2.music.126.net/SE8cHSmQa64k-d0fPztdLw==/109951168456600591.jpg?param=140y140'),
(55, '[孤独心事] 一个人听的寂寞独白', 'http://p2.music.126.net/SU_Q1SfPi7QYsy1HkpIUsQ==/109951168537698980.jpg?param=140y140'),
(56, '[梦游仙境] 在柔和氛围中沉睡', 'http://p2.music.126.net/ptVZ_E9jQqTe0s7BTMKwaA==/109951168566943551.jpg?param=140y140'),
(57, '[沉浸式刷题] 用笔尖给未来画上翅膀', 'http://p2.music.126.net/vIraK-I9OsJIDWEbUtC4AA==/109951168378406638.jpg?param=140y140'),
(58, '[宁静阅览室] 漫步静谧慵懒空间 ', 'http://p2.music.126.net/tD_bJa-EwI7s6rCb7q31_A==/109951168476025055.jpg?param=140y140'),
(59, '[睡个回笼觉] 关掉闹钟 重新入梦吧 ', 'http://p2.music.126.net/g_b_iIR6Duuo_Cj87-_9lw==/109951168573749921.jpg?param=140y140'),
(510, '[祝你好梦] 伴着温柔的旋律入眠', 'http://p2.music.126.net/_wkApRkHWgwglrg0-dVRrg==/109951168502986682.jpg?param=140y140'),
(511, '[Lofi梦境] 熟睡后的云端漫游体验', 'http://p2.music.126.net/6i2s1aiMjMrnOaAkm4qnNA==/109951168314047134.jpg?param=140y140'),
(512, '[古典早安时光] 一日之计在于晨', 'http://p2.music.126.net/Ac3M387C8logbNk-vSZLOQ==/109951168518827154.jpg?param=140y140'),
(513, '[舒缓减压舱] 收拾好心情 重新出发吧', 'http://p2.music.126.net/IcDlEgXtmFMkCkCIPpLMyw==/109951168476050433.jpg?param=140y140'),
(514, '[雨天随想] 心事随雨 缓缓落下', 'http://p2.music.126.net/iFfiKltDXcTHjnAFp9FTbg==/109951168296863731.jpg?param=140y140'),
(515, '[东方禅意] 碧涧流泉的袅袅余音', 'http://p2.music.126.net/9evWp_5h8AOhlHm2hX_mhg==/109951166195575714.jpg?param=140y140'),
(516, '[24小时自习室] 保持专注 考前冲刺好伴侣', 'http://p2.music.126.net/uTRKjOpjDR8lqg2w9fVDvw==/109951168571978328.jpg?param=140y140'),
(517, '[舒缓轻音] 停泊心灵的治愈所', 'http://p2.music.126.net/Nc-kZC-4S00IZ_DYswTbEg==/109951168529295233.jpg?param=140y140'),
(518, '[晚安小夜曲] 就让今天在轻柔的音乐里结束吧', 'http://p2.music.126.net/ZIs4vATKqZfSwprg6D8zKg==/109951168529260868.jpg?param=140y140'),
(519, '[沉浸式备考] 考前必备减压攻略', 'http://p2.music.126.net/JtM_ZMp0toMxIQfXKxyPZA==/109951168407517609.jpg?param=140y140'),
(520, '[古典放松一下] 疗愈身心的天籁之音', 'http://p2.music.126.net/awZm95pYrfyFglPK6t6cnA==/109951168518832016.jpg?param=140y140'),
(521, '[专注好时光] 清新韩系助你捕捉灵感信号', 'http://p2.music.126.net/BFhKki8EXQ7ddh5ve4O90w==/109951168470786669.jpg?param=140y140'),
(522, '[入梦氛围] 伴你度过宁静的夜晚', 'http://p2.music.126.net/OQPcO6HWSEwGCZh7QOyThQ==/109951168566918811.jpg?param=140y140'),
(523, '[助眠颂钵] 抚慰心灵的悠远天籁', 'http://p2.music.126.net/uo1rfA7afNSx41Owz3w0ow==/109951168189587984.jpg?param=140y140'),
(524, '[古典专注氛围] 用音符让大脑保持专注', 'http://p2.music.126.net/4Pt6FBRU1U7wiV09EFSDUQ==/109951168518815626.jpg?param=140y140'),
(525, '[沉浸式学习] 埋头刷题中 欢迎打卡同行', 'http://p2.music.126.net/JdFWZTHpJh0YyAqAKKVfMw==/109951168299914898.jpg?param=140y140'),
(526, '[轻松阅读时光] 品味与文字的美妙际遇', 'http://p2.music.126.net/GEJCqwRHcMDhI14fpy5g1Q==/109951168537811701.jpg?param=140y140'),
(527, '[愉快工作时光] 保持专注 让大脑活跃起来', 'http://p2.music.126.net/aCmsMUHChew6Fq5gaiRNZw==/109951168537814540.jpg?param=140y140'),
(528, '[林间梦境] 在梦中与森林共呼吸', 'http://p2.music.126.net/n5nnlAoW8b7VXcZOS8-HoA==/109951168565289374.jpg?param=140y140'),
(529, '[温柔灵魂乐] 静静地为你舒展心灵', 'http://p2.music.126.net/T0pnUp5lT1HVnSYc-mZJsg==/109951168537661987.jpg?param=140y140'),
(530, '[古典西餐厅] 在音乐中度过慵懒时光', 'http://p2.music.126.net/m9ohFfl3axr1sB-omfgpTg==/109951168503622074.jpg?param=140y140'),
(531, '[一起发呆] 放空思绪 享受片刻抽离', 'http://p2.music.126.net/Y5ESgb2OAkTQwEoBueBIaA==/109951168571312633.jpg?param=140y140'),
(532, '[学习听民谣] 埋头学习时听的温柔旋律', 'http://p2.music.126.net/_hgEhT8v_jisgrssMT6NoQ==/109951168439992143.jpg?param=140y140'),
(533, '[深度学习时间] 为高效时刻营造完美氛围', 'http://p2.music.126.net/wD5c0tABoz9kywJIqbK7Ow==/109951168307306918.jpg?param=140y140'),
(534, '[古典快乐时光] 懂你好心情的古典音乐', 'http://p2.music.126.net/I6soEUc0c1K-pm1FXhQvaQ==/109951168518794875.jpg?param=140y140');

--
-- 转储表的索引
--

--
-- 表的索引 `playlist`
--
ALTER TABLE `playlist`
  ADD PRIMARY KEY (`list_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
