-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 12, 2025 at 02:55 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `system2`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(10) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `phone` int(10) NOT NULL,
  `username` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `Email`, `password`, `phone`, `username`) VALUES
(1012667234, 'admin01@gmail.com', '0000', 567331016, 'admin01');

-- --------------------------------------------------------

--
-- Table structure for table `companion`
--

CREATE TABLE `companion` (
  `companion_id` int(10) NOT NULL,
  `Firstname` varchar(50) NOT NULL,
  `lastName` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `phone` int(10) NOT NULL,
  `password` varchar(50) NOT NULL,
  `Gender` varchar(11) NOT NULL,
  `birthdate` date NOT NULL,
  `AccountStatus` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `Experience` varchar(50) NOT NULL,
  `companion_Status` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `complaints & lnquiries`
--

CREATE TABLE `complaints & lnquiries` (
  `Complaint_id` int(10) NOT NULL,
  `Complaint_Text` text NOT NULL,
  `Complaint_Date` date NOT NULL,
  `Response` text NOT NULL,
  `Requests_Type` varchar(7) NOT NULL,
  `customer_id` int(10) NOT NULL,
  `admin_id` int(10) NOT NULL,
  `Driver_id` int(10) NOT NULL,
  `companion_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `customer_Id` int(10) NOT NULL,
  `Firstname` varchar(50) NOT NULL,
  `lastName` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `phone` int(10) NOT NULL,
  `Gender` varchar(11) NOT NULL,
  `birthdate` date DEFAULT NULL,
  `disabilty_type` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`customer_Id`, `Firstname`, `lastName`, `Email`, `password`, `phone`, `Gender`, `birthdate`, `disabilty_type`, `username`) VALUES
(1122050097, 'امل', 'الحربي', 'LAMA55@gmil.com', '11', 0, 'أنثى', '2025-03-27', 'حركية', '0'),
(1122334455, 'ريناد', 'الاحمدي', 'rrrrr55@gmail.com', '3322', 445552278, 'أنثى', '2025-03-07', 'بصرية', 'dd.33'),
(1122334466, 'ثريا', 'حربي', 'rrrrr55@gmail.com', '2211', 445552278, 'أنثى', '2025-03-07', 'بصرية', 'dd.33'),
(1133050097, 'ثريا', 'الكعبي', 'THURAYA.123@gmail.com', '112233', 504270485, 'أنثى', '2025-03-28', 'حركية', '0'),
(2147483647, 'لمى', 'الحربي', 'LAMA55@gmil.com', '5544', 0, 'أنثى', '2025-03-26', 'حركية', '0');

-- --------------------------------------------------------

--
-- Table structure for table `driver`
--

CREATE TABLE `driver` (
  `Driver_id` int(10) NOT NULL,
  `FirstName` varchar(50) NOT NULL,
  `lastName` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `phone` int(10) NOT NULL,
  `Gender` varchar(11) NOT NULL,
  `birthdate` date NOT NULL,
  `AccountStatus` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `license_number` varchar(10) NOT NULL,
  `companion_id` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `rating`
--

CREATE TABLE `rating` (
  `rating_id` int(10) NOT NULL,
  `ratings_value` int(5) NOT NULL,
  `rating_Notes` text DEFAULT NULL,
  `customer_id` int(10) NOT NULL,
  `Trip_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `trips`
--

CREATE TABLE `trips` (
  `Trip_id` int(10) NOT NULL,
  `Meeting_Location` varchar(255) NOT NULL,
  `Destination_Location` varchar(255) NOT NULL,
  `Payment_Method` varchar(50) NOT NULL,
  `Trip_Status` varchar(255) NOT NULL,
  `Vehicle_Type` varchar(50) NOT NULL,
  `companion_Service` tinyint(1) NOT NULL,
  `companion_Gender` varchar(4) NOT NULL,
  `Trip_Date` date NOT NULL,
  `customer_id` int(10) NOT NULL,
  `Driver_id` int(10) NOT NULL,
  `companion_id` int(10) NOT NULL,
  `Vehicle_number` varchar(20) NOT NULL,
  `rating_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `Vehicle_number` varchar(20) NOT NULL,
  `Vehicle_Model` varchar(50) NOT NULL,
  `Vehicle_Type` varchar(50) NOT NULL,
  `license_number` varchar(10) NOT NULL,
  `Vehicle_status` varchar(50) NOT NULL,
  `Trip_id` int(10) NOT NULL,
  `Driver_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--




--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `companion`
--
ALTER TABLE `companion`
  ADD PRIMARY KEY (`companion_id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `complaints & lnquiries`
--
ALTER TABLE `complaints & lnquiries`
  ADD PRIMARY KEY (`Complaint_id`),
  ADD KEY `admin_id` (`admin_id`),
  ADD KEY `Driver_id` (`Driver_id`),
  ADD KEY `rider_id` (`customer_id`),
  ADD KEY `companion_id` (`companion_id`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`customer_Id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `driver`
--
ALTER TABLE `driver`
  ADD PRIMARY KEY (`Driver_id`),
  ADD KEY `companion_id` (`companion_id`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `rating`
--
ALTER TABLE `rating`
  ADD PRIMARY KEY (`rating_id`),
  ADD KEY `rider_id` (`customer_id`),
  ADD KEY `Trip_id` (`Trip_id`);

--
-- Indexes for table `trips`
--
ALTER TABLE `trips`
  ADD PRIMARY KEY (`Trip_id`),
  ADD KEY `Driver_id` (`Driver_id`),
  ADD KEY `rider_id` (`customer_id`),
  ADD KEY `Vehicle_number` (`Vehicle_number`),
  ADD KEY `rating_id` (`rating_id`),
  ADD KEY `companion_id` (`companion_id`);

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`Vehicle_number`),
  ADD KEY `Driver_id` (`Driver_id`),
  ADD KEY `Trip_id` (`Trip_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `rating`
--
ALTER TABLE `rating`
  MODIFY `rating_id` int(10) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `complaints & lnquiries`
--
ALTER TABLE `complaints & lnquiries`
  ADD CONSTRAINT `complaints & lnquiries_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`),
  ADD CONSTRAINT `complaints & lnquiries_ibfk_2` FOREIGN KEY (`Driver_id`) REFERENCES `driver` (`Driver_id`),
  ADD CONSTRAINT `complaints & lnquiries_ibfk_3` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_Id`),
  ADD CONSTRAINT `complaints & lnquiries_ibfk_4` FOREIGN KEY (`companion_id`) REFERENCES `companion` (`companion_id`);

--
-- Constraints for table `driver`
--
ALTER TABLE `driver`
  ADD CONSTRAINT `driver_ibfk_1` FOREIGN KEY (`companion_id`) REFERENCES `companion` (`companion_id`);

--
-- Constraints for table `rating`
--
ALTER TABLE `rating`
  ADD CONSTRAINT `rating_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_Id`),
  ADD CONSTRAINT `rating_ibfk_2` FOREIGN KEY (`Trip_id`) REFERENCES `trips` (`Trip_id`);

--
-- Constraints for table `trips`
--
ALTER TABLE `trips`
  ADD CONSTRAINT `trips_ibfk_1` FOREIGN KEY (`Driver_id`) REFERENCES `driver` (`Driver_id`),
  ADD CONSTRAINT `trips_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_Id`),
  ADD CONSTRAINT `trips_ibfk_3` FOREIGN KEY (`Vehicle_number`) REFERENCES `vehicles` (`Vehicle_number`),
  ADD CONSTRAINT `trips_ibfk_4` FOREIGN KEY (`rating_id`) REFERENCES `rating` (`rating_id`),
  ADD CONSTRAINT `trips_ibfk_5` FOREIGN KEY (`companion_id`) REFERENCES `companion` (`companion_id`);

--
-- Constraints for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD CONSTRAINT `vehicles_ibfk_1` FOREIGN KEY (`Driver_id`) REFERENCES `driver` (`Driver_id`),
  ADD CONSTRAINT `vehicles_ibfk_2` FOREIGN KEY (`Trip_id`) REFERENCES `trips` (`Trip_id`);

-- تعديلات على قاعدة البيانات لتحسين العلاقات
ALTER TABLE `trips` MODIFY `companion_id` int(10) DEFAULT NULL;
ALTER TABLE `trips` MODIFY `rating_id` int(10) DEFAULT NULL;
ALTER TABLE `trips` MODIFY `Vehicle_number` varchar(20) DEFAULT NULL;
ALTER TABLE `trips` MODIFY `Driver_id` int(10) DEFAULT NULL;

ALTER TABLE `rating` MODIFY `Trip_id` int(10) DEFAULT NULL;

ALTER TABLE `vehicles` MODIFY `Trip_id` int(10) DEFAULT NULL;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
