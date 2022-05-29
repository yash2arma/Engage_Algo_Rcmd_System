-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.3:4306
-- Generation Time: May 29, 2022 at 06:03 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `user_detail`
--

-- --------------------------------------------------------

--
-- Table structure for table `movie_ratings`
--

CREATE TABLE `movie_ratings` (
  `movie_no` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `rating` double NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `movie_ratings`
--

INSERT INTO `movie_ratings` (`movie_no`, `user_id`, `movie_id`, `rating`, `timestamp`) VALUES
(1, 1, 211672, 8.2, '2022-05-28 15:59:05'),
(2, 1, 211672, 8.2, '2022-05-28 16:00:05'),
(3, 1, 211672, 7.7, '2022-05-28 16:00:14'),
(4, 1, 211672, 5, '2022-05-28 16:00:23'),
(5, 1, 211672, 5, '2022-05-28 16:09:06'),
(6, 1, 211672, 5, '2022-05-28 16:09:14'),
(7, 1, 211672, 5, '2022-05-28 16:12:16'),
(8, 1, 211672, 5, '2022-05-28 16:14:13'),
(9, 1, 211672, 5, '2022-05-28 16:18:22'),
(10, 1, 211672, 5, '2022-05-28 16:20:16'),
(11, 1, 211672, 5, '2022-05-28 16:26:03'),
(12, 5, 297222, 9.4, '2022-05-29 01:06:58'),
(13, 5, 7508, 5, '2022-05-29 01:11:47'),
(14, 5, 7508, 10, '2022-05-29 01:14:01'),
(15, 5, 7508, 10, '2022-05-29 01:15:40'),
(16, 5, 7508, 10, '2022-05-29 01:16:11'),
(17, 4, 191714, 9.1, '2022-05-29 02:12:17'),
(18, 4, 414276, 8.8, '2022-05-29 02:32:43'),
(19, 4, 1422, 5.2, '2022-05-29 02:37:43'),
(20, 6, 297222, 10, '2022-05-29 03:31:40'),
(21, 6, 297222, 10, '2022-05-29 03:39:38'),
(22, 6, 7508, 7.1, '2022-05-29 03:40:12'),
(23, 6, 9100, 9.3, '2022-05-29 03:53:06'),
(24, 6, 907, 8.3, '2022-05-29 03:53:37'),
(25, 6, 4599, 6.2, '2022-05-29 03:54:46'),
(26, 6, 204435, 8.3, '2022-05-29 03:56:08');

-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE `user_details` (
  `id` int(11) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_details`
--

INSERT INTO `user_details` (`id`, `user_name`, `user_email`, `user_password`) VALUES
(1, 'yash', 'yash@gmail.com', 'yash'),
(2, 'yash', 'yash@gmail.com', 'yash'),
(3, 'yash', 'yash@gmail.com', 'yash'),
(4, 'rohit', 'rohit@gmail.com', 'rohit'),
(5, 'ayush', 'ayush@gmail.com', 'ayush'),
(6, 'sachin', 'sachin@gmail.com', 'sachin');

-- --------------------------------------------------------

--
-- Table structure for table `user_wishlist`
--

CREATE TABLE `user_wishlist` (
  `movie_no` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_wishlist`
--

INSERT INTO `user_wishlist` (`movie_no`, `user_id`, `movie_id`) VALUES
(1, 1, 211672),
(2, 1, 157336),
(3, 1, 102899),
(4, 1, 102899),
(5, 1, 119450),
(6, 1, 135397),
(7, 1, 135397),
(8, 1, 293660),
(9, 1, 109445),
(10, 4, 297222),
(11, 4, 297222),
(12, 4, 191714),
(13, 4, 414276),
(14, 4, 1422),
(15, 6, 7508),
(16, 6, 7508),
(17, 6, 7508),
(18, 6, 7508),
(19, 6, 329909),
(20, 6, 907),
(21, 6, 4599),
(22, 6, 204435);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `movie_ratings`
--
ALTER TABLE `movie_ratings`
  ADD PRIMARY KEY (`movie_no`);

--
-- Indexes for table `user_details`
--
ALTER TABLE `user_details`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_wishlist`
--
ALTER TABLE `user_wishlist`
  ADD PRIMARY KEY (`movie_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `movie_ratings`
--
ALTER TABLE `movie_ratings`
  MODIFY `movie_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `user_details`
--
ALTER TABLE `user_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user_wishlist`
--
ALTER TABLE `user_wishlist`
  MODIFY `movie_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
