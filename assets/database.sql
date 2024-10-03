SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- ----------------------------------------------------

CREATE DATABASE term2project;
USE term2project;

-- ----------------------------------------------------

CREATE TABLE `credentials` (
  `password` varchar(32) NOT NULL
);

CREATE TABLE `data` (
  `date` varchar(11) NOT NULL,
  `time` varchar(11) NOT NULL,
  `bill_id` varchar(11) NOT NULL,
  `costumer_name` varchar(40) NOT NULL,
  `phone` varchar(11) NOT NULL,
  `invoice` mediumblob NOT NULL
);

CREATE TABLE `products` (
  `id` varchar(5) NOT NULL,
  `name` varchar(40) NOT NULL,
  `price` varchar(5) NOT NULL,
  `stock` varchar(5) NOT NULL,
  `indexing` int(11) NOT NULL
);

-- ----------------------------------------------------

ALTER TABLE `data`
  ADD PRIMARY KEY (`bill_id`);

ALTER TABLE `products`
  ADD PRIMARY KEY (`indexing`);

ALTER TABLE `products`
  MODIFY `indexing` int(11) NOT NULL AUTO_INCREMENT;

-- ----------------------------------------------------

INSERT INTO `credentials` (`password`) VALUES
('2d93dc59f6eaf52c92e1a08b57e9282d');

-- term2project

INSERT INTO `products` (`id`, `name`, `price`, `stock`) VALUES
('p1', 'item1', '10', '50'),
('p2', 'item2', '20', '50'),
('p3', 'item3', '30', '50');

INSERT INTO `data` (`date`, `time`, `bill_id`, `costumer_name`, `phone`, `invoice`) VALUES
('11-Jan-1111', '00:00 AM', '1000000', 'Demo', '1111111111', 0x2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d0d0a202020202020202020202020202020202020202047656e6572616c2053746f72652020200d0a2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d0d0a2020202020202020202020202020436f6e74616374204e6f2e202d20383938393839383938390d0a0d0a2020202020202020202020202020202020202020202020494e564f4943450d0a0d0a44617465203a2031312d4a616e2d3131313120202020202020202020202020202020202020202054696d65203a2030303a303020414d0d0a0d0a496e766f696365204944203a20313030303030300d0a436f7374756d6572204e616d65203a2044656d6f0d0a0d0a2b2d2d2d2d2d2d2d2d2b2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2b2d2d2d2d2d2d2d2d2d2d2b2d2d2d2d2d2d2d2d2b0d0a7c20204974656d20207c20506572204974656d20436f7374207c205175616e74697479207c20416d6f756e74207c0d0a2b2d2d2d2d2d2d2d2d2b2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2b2d2d2d2d2d2d2d2d2d2d2b2d2d2d2d2d2d2d2d2b0d0a7c204974656d2031207c2020202020203530202020202020207c202020203130202020207c20203530302020207c0d0a7c204974656d2032207c2020202020203530202020202020207c202020203130202020207c20203530302020207c0d0a7c204974656d2033207c2020202020203530202020202020207c202020203130202020207c20203530302020207c0d0a7c204974656d2034207c2020202020203530202020202020207c202020203130202020207c20203530302020207c0d0a7c204974656d2035207c2020202020203530202020202020207c202020203130202020207c20203530302020207c0d0a2b2d2d2d2d2d2d2d2d2b2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2b2d2d2d2d2d2d2d2d2d2d2b2d2d2d2d2d2d2d2d2b0d0a0d0a416d6f756e74203a2052732e323530300d0a0d0a2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d);

COMMIT;