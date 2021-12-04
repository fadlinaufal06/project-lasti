-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 20, 2020 at 12:40 PM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.3.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nodemcu_rfid_iot_projects`
--

-- --------------------------------------------------------

--
-- Table structure for table `table_the_iot_projects`
--

CREATE TABLE `item_data_matahari` (
  `id_tag` varchar(100) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `add_info` varchar(100) NOT NULL,
  `harga` integer NOT NULL,
  `stok` integer NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `table_the_iot_projects`
--

INSERT INTO `item_data_matahari` (`id_tag`, `nama`, `add_info`, `harga`, `stok`) VALUES
('A368F596','Nike_AirForce1', 'Shoes-Black-36', '1500000', '24'),
('2B55EDCG', 'Zoya_Scarf101', 'Scarf-Maroon-LR', '230000', '56'),
('03E7A308', 'Nike_AirForce1', 'Shoes-Black-40', '1500000', '10'),
('2BAA43CG', 'Zoya_Scarf302', 'Scarf-Maroon-LR', '230000', '34');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `table_the_iot_projects`
--
ALTER TABLE `item_data_matahari`
  ADD PRIMARY KEY (`id_tag`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
