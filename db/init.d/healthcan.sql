CREATE DATABASE IF NOT EXISTS `db_healthcan`;

CREATE TABLE IF NOT EXISTS `db_healthcan`.`healthcan` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned NOT NULL,
  `name` varchar(256) DEFAULT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `height` decimal(4, 1) NOT NULL,
  `weight` decimal(4, 1) NOT NULL,
  `bmi` decimal(3, 1) NOT NULL,
  `pro_weight` decimal(5, 2) NOT NULL,
  `diff_weight` decimal(4, 2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `name` (`name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;