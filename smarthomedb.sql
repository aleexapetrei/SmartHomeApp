-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 26, 2019 at 01:03 PM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.1.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smarthomedb`
--

-- --------------------------------------------------------

--
-- Table structure for table `devicestate`
--

CREATE TABLE `devicestate` (
  `deviceId` int(10) NOT NULL,
  `deviceName` varchar(200) DEFAULT NULL,
  `deviceLoc` varchar(200) DEFAULT NULL,
  `deviceState` int(1) DEFAULT NULL,
  `Id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `devicestate`
--

INSERT INTO `devicestate` (`deviceId`, `deviceName`, `deviceLoc`, `deviceState`, `Id`) VALUES
(21, 'Radio', 'Kitchen', 0, 1),
(21, 'Radio', 'Kitchen', 1, 2),
(19, 'Kettle', 'Kitchen', 1, 3),
(19, 'Kettle', 'Kitchen', 0, 4);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(2) NOT NULL,
  `userName` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `userName`, `email`, `password`) VALUES
(28, 'Alex', 'aleex.apetrei@yahoo.com', 'apetrei77'),
(33, 'aa', 'aa@yahoo.com', 'ala'),
(34, '2', 'alabala@yahoo.com', 'ala'),
(45, 'AlexApetrei', 'CA871@yahoo.com', '00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `devicestate`
--
ALTER TABLE `devicestate`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `devicestate`
--
ALTER TABLE `devicestate`
  MODIFY `Id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=163;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
