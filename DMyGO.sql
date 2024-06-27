-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        8.0.26 - MySQL Community Server - GPL
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  12.4.0.6659
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 导出 dmygo 的数据库结构
CREATE DATABASE IF NOT EXISTS `dmygo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dmygo`;

-- 导出  表 dmygo.account 结构
CREATE TABLE IF NOT EXISTS `account` (
  `user_id` int NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `user_name` varchar(10) NOT NULL COMMENT '用户名',
  `password` varchar(20) NOT NULL COMMENT '密码',
  `role` varchar(10) NOT NULL COMMENT '角色\n',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `account_user_id_uindex` (`user_id`),
  UNIQUE KEY `account_user_name_uindex` (`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='账户密码表';

-- 正在导出表  dmygo.account 的数据：~5 rows (大约)
DELETE FROM `account`;
INSERT INTO `account` (`user_id`, `user_name`, `password`, `role`) VALUES
	(46, 'admin', 'abc123456', 'admin'),
	(47, 'worker01', 'cau1234', 'worker'),
	(48, 'worker02', 'cau1234', 'worker'),
	(49, 'customer01', 'cau12345', 'customer'),
	(50, 'customer02', 'cau12345', 'customer'),
	(63, 'worker03', 'cau1234', 'customer');

-- 导出  表 dmygo.field 结构
CREATE TABLE IF NOT EXISTS `field` (
  `field_id` int NOT NULL AUTO_INCREMENT COMMENT '地块id\n',
  `field_name` varchar(20) NOT NULL COMMENT '地块名称',
  `field_pos` varchar(20) NOT NULL COMMENT '地块位置',
  `field_size` varchar(20) NOT NULL COMMENT '地块大小',
  `field_class` varchar(20) NOT NULL COMMENT '地块类别\n',
  `field_outcome` varchar(20) NOT NULL COMMENT '地块产出\n',
  PRIMARY KEY (`field_id`),
  UNIQUE KEY `field_field_id_uindex` (`field_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='设施信息表';

-- 正在导出表  dmygo.field 的数据：~7 rows (大约)
DELETE FROM `field`;
INSERT INTO `field` (`field_id`, `field_name`, `field_pos`, `field_size`, `field_class`, `field_outcome`) VALUES
	(1, '农田01', '东', '100*1000', '农田', '小麦'),
	(2, '农田02', '东', '100*200', '农田', '小麦'),
	(3, '鱼塘01', '南', '100*200', '鱼塘', '鲫鱼'),
	(4, '鱼塘02', '南', '100*100', '鱼塘', '鲈鱼'),
	(5, '果园01', '西', '100*200', '果园', '苹果'),
	(6, '果园03', '南', '100*100', '果园', '苹果'),
	(7, '菜园01', '南', '200*100', '菜园', '小白菜');

-- 导出  表 dmygo.goods_info 结构
CREATE TABLE IF NOT EXISTS `goods_info` (
  `product_id` int NOT NULL COMMENT '产品id\n',
  `goods_quantity` int NOT NULL DEFAULT '0' COMMENT '商品数量',
  `goods_price` int NOT NULL DEFAULT '0' COMMENT '商品价格\n',
  `goods_state` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否上架',
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `goods_info_product_id_uindex` (`product_id`),
  CONSTRAINT `goods_info_product_info_product_id_fk` FOREIGN KEY (`product_id`) REFERENCES `product_info` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  dmygo.goods_info 的数据：~7 rows (大约)
DELETE FROM `goods_info`;
INSERT INTO `goods_info` (`product_id`, `goods_quantity`, `goods_price`, `goods_state`) VALUES
	(1, 223, 21, 1),
	(2, 5245, 32, 1),
	(3, 2529, 6, 1),
	(4, 7341, 25, 1),
	(5, 324, 20, 0),
	(6, 4123, 5, 1),
	(7, 0, 0, 0);

-- 导出  表 dmygo.order 结构
CREATE TABLE IF NOT EXISTS `order` (
  `order_id` int NOT NULL AUTO_INCREMENT COMMENT '订单id\n',
  `product_id` int NOT NULL COMMENT '产品id\n',
  `user_id` int NOT NULL COMMENT '用户id',
  `product_quantity` int DEFAULT NULL COMMENT '产品数量\n',
  PRIMARY KEY (`order_id`),
  UNIQUE KEY `order_order_id_uindex` (`order_id`),
  KEY `order_account_user_id_fk` (`user_id`),
  KEY `order_goods_info_product_id_fk` (`product_id`),
  CONSTRAINT `order_account_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `account` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `order_goods_info_product_id_fk` FOREIGN KEY (`product_id`) REFERENCES `goods_info` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  dmygo.order 的数据：~0 rows (大约)
DELETE FROM `order`;

-- 导出  表 dmygo.product_info 结构
CREATE TABLE IF NOT EXISTS `product_info` (
  `product_id` int NOT NULL AUTO_INCREMENT COMMENT '产品id',
  `product_class` varchar(20) NOT NULL COMMENT '产品类别',
  `product_name` varchar(20) NOT NULL COMMENT '产品名称',
  `product_price` int NOT NULL DEFAULT '0' COMMENT '产品价格\n',
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `product_info_product_id_uindex` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='产品类别';

-- 正在导出表  dmygo.product_info 的数据：~7 rows (大约)
DELETE FROM `product_info`;
INSERT INTO `product_info` (`product_id`, `product_class`, `product_name`, `product_price`) VALUES
	(1, '主食', '小麦', 3),
	(2, '水果', '苹果', 8),
	(3, '水果', '梨', 6),
	(4, '鱼', '鲈鱼', 25),
	(5, '鱼', '鲫鱼', 20),
	(6, '蔬菜', '小白菜', 10),
	(7, '蔬菜', '茼蒿', 12);

-- 导出  表 dmygo.product_storage 结构
CREATE TABLE IF NOT EXISTS `product_storage` (
  `product_id` int NOT NULL COMMENT '产品id\n',
  `field_id` int NOT NULL COMMENT '设施id',
  `product_quantity` int DEFAULT NULL COMMENT '存放数量',
  `product_state` varchar(20) NOT NULL COMMENT '产品状态',
  PRIMARY KEY (`product_id`,`field_id`),
  KEY `product_storage___fk_field` (`field_id`),
  CONSTRAINT `product_storage___fk_field` FOREIGN KEY (`field_id`) REFERENCES `field` (`field_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `product_storage___fk_product` FOREIGN KEY (`product_id`) REFERENCES `product_info` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='产品存放表';

-- 正在导出表  dmygo.product_storage 的数据：~7 rows (大约)
DELETE FROM `product_storage`;
INSERT INTO `product_storage` (`product_id`, `field_id`, `product_quantity`, `product_state`) VALUES
	(1, 1, 3000, '0'),
	(1, 2, 5000, '1'),
	(2, 5, 4000, '1'),
	(3, 4, 200, '1'),
	(3, 6, 600, '0'),
	(4, 3, 4000, '0'),
	(5, 4, 200, '1');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
