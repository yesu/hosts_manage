
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for batch
-- ----------------------------
DROP TABLE IF EXISTS `batch`;
CREATE TABLE `batch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for batch_detail
-- ----------------------------
DROP TABLE IF EXISTS `batch_detail`;
CREATE TABLE `batch_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `batch_id` smallint(6) NOT NULL,
  `ip` char(15) DEFAULT NULL,
  `flag` smallint(6) DEFAULT NULL,
  `cmd` varchar(255) DEFAULT NULL,
  `result` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `batch_id` (`batch_id`) USING BTREE,
  KEY `ip` (`ip`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=396 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cpu_batch
-- ----------------------------
DROP TABLE IF EXISTS `cpu_batch`;
CREATE TABLE `cpu_batch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cpu_detail
-- ----------------------------
DROP TABLE IF EXISTS `cpu_detail`;
CREATE TABLE `cpu_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(15) DEFAULT NULL,
  `cpu_used` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=277 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for df_batch
-- ----------------------------
DROP TABLE IF EXISTS `df_batch`;
CREATE TABLE `df_batch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for df_detail
-- ----------------------------
DROP TABLE IF EXISTS `df_detail`;
CREATE TABLE `df_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(15) DEFAULT NULL,
  `df_used` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=293 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for last_batch
-- ----------------------------
DROP TABLE IF EXISTS `last_batch`;
CREATE TABLE `last_batch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for last_detail
-- ----------------------------
DROP TABLE IF EXISTS `last_detail`;
CREATE TABLE `last_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` char(15) DEFAULT NULL,
  `login_ip` char(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2836 DEFAULT CHARSET=utf8;
DROP TRIGGER IF EXISTS `create_time`;
DELIMITER ;;
CREATE TRIGGER `create_time` BEFORE INSERT ON `batch` FOR EACH ROW if new.create_time is null then
       set new.create_time = now();
     end if
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `cpu_create_time`;
DELIMITER ;;
CREATE TRIGGER `cpu_create_time` BEFORE INSERT ON `cpu_batch` FOR EACH ROW if new.create_time is null then
       set new.create_time = now();
     end if
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `df_create_time`;
DELIMITER ;;
CREATE TRIGGER `df_create_time` BEFORE INSERT ON `df_batch` FOR EACH ROW if new.create_time is null then
       set new.create_time = now();
     end if
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `last_create_time`;
DELIMITER ;;
CREATE TRIGGER `last_create_time` BEFORE INSERT ON `last_batch` FOR EACH ROW if new.create_time is null then
       set new.create_time = now();
     end if
;;
DELIMITER ;
