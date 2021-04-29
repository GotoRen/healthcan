CREATE DATABASE IF NOT EXISTS `healthcan_db`;

CREATE TABLE IF NOT EXISTS `healthcan_db`.`healthcan` (
  `id`          int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id`     int(11) unsigned NOT NULL,
  `name`        varchar(256)     DEFAULT NULL,
  `date`        date             NOT NULL,
  `time`        time             NOT NULL,
  `height`      decimal(4,1)     NOT NULL DEFAULT '0',
  `weight`      decimal(4,1)     NOT NULL DEFAULT '0',
  `bmi`         decimal(3,1)     NOT NULL DEFAULT '0',
  `pro_weight`  decimal(5,2)     NOT NULL DEFAULT '0',
  `diff_weight` decimal(4,2)     NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
