CREATE DATABASE IF NOT EXISTS `db_healthcan`;

CREATE TABLE IF NOT EXISTS `db_healthcan`.`user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(256) NOT NULL DEFAULT '',
  `name` varchar(256) DEFAULT NULL,
  `password` varchar(256) DEFAULT NULL,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `OUTER_KEY` (`email`),
  KEY `KEY_INDEX` (`email`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;