

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for app_info
-- ----------------------------
DROP TABLE IF EXISTS `app_info`;
CREATE TABLE `app_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '应用ID',
  `name` varchar(255) DEFAULT NULL COMMENT '应用名称',
  `type` varchar(100) DEFAULT NULL,
  `domain` varchar(250) DEFAULT NULL,
  `platform` varchar(50) DEFAULT NULL,
  `assets_id` int(11) DEFAULT NULL COMMENT '资产ID',
  `sub_category_id` int(11) DEFAULT NULL COMMENT 'dist_id',
  `main_category_id` int(11) DEFAULT NULL COMMENT '主类ID',
  `inner_ip` varchar(160) DEFAULT NULL,
  `public_ip` varchar(160) DEFAULT NULL COMMENT '管理IP',
  `db_type` varchar(100) DEFAULT NULL,
  `port` int(11) DEFAULT NULL COMMENT '端口(mysql)',
  `oper_user` varchar(16) DEFAULT NULL COMMENT '操作员',
  `update_date` date DEFAULT NULL COMMENT '更新时间',
  `is_monitor` smallint(1) DEFAULT '0' COMMENT '0：不纳入监控 1：纳入监控   ',
  `is_del` smallint(1) DEFAULT '0' COMMENT '1：删除  0：使用 ',
  PRIMARY KEY (`id`),
  KEY `inner_ip` (`inner_ip`) USING BTREE,
  KEY `ip` (`public_ip`) USING BTREE,
  KEY `type` (`type`) USING BTREE,
  KEY `sub_category_id` (`sub_category_id`) USING BTREE,
  KEY `main_category_id` (`main_category_id`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=2671 DEFAULT CHARSET=utf8 COMMENT='应用表';

-- ----------------------------
-- Table structure for assets
-- ----------------------------
DROP TABLE IF EXISTS `assets`;
CREATE TABLE `assets` (
  `id` int(5) NOT NULL AUTO_INCREMENT COMMENT '资产ID',
  `hostname` varchar(50) DEFAULT NULL,
  `wxsn` varchar(250) DEFAULT NULL COMMENT '唯一代号',
  `platform` varchar(50) DEFAULT NULL,
  `main_category_id` int(5) DEFAULT NULL,
  `idc_id` int(11) DEFAULT NULL COMMENT 'IDC_ID',
  `public_ip` char(15) DEFAULT NULL COMMENT '管理IP',
  `pwd` varchar(255) DEFAULT NULL,
  `inner_ip` char(15) DEFAULT NULL COMMENT '内网ip',
  `ips` varchar(200) DEFAULT NULL COMMENT '所有IP列表',
  `ipmi_ip` varchar(15) DEFAULT NULL COMMENT 'IPMIIP',
  `sn` varchar(20) DEFAULT NULL COMMENT '生产编号',
  `rack` varchar(15) DEFAULT NULL COMMENT '机柜',
  `os` varchar(200) DEFAULT NULL COMMENT '操作系统',
  `setting` varchar(50) DEFAULT NULL COMMENT '手写配置',
  `settings` varchar(50) DEFAULT NULL COMMENT '真实配置',
  `brand` varchar(50) DEFAULT NULL COMMENT '品牌',
  `manager` varchar(30) DEFAULT NULL COMMENT '负责人',
  `flag` tinyint(1) DEFAULT NULL COMMENT '状态:0=报废, 1=正常, 2=故障, 3=待用',
  `virtual` int(11) DEFAULT NULL COMMENT '0：实体；-1：虚拟机宿主。如果是虚拟机则填写对应主机ID',
  `type` tinyint(1) DEFAULT NULL COMMENT '设备类型 1=服务器;2=交换机;3=存储;4=其它;',
  `oper_user` varchar(16) DEFAULT NULL COMMENT '操作人',
  `update_date` datetime DEFAULT NULL COMMENT '更新时间',
  `is_manage` int(1) DEFAULT '0' COMMENT '0:未管理 1:纳入管理',
  `vlan` tinyint(3) DEFAULT NULL COMMENT '1=外网,2=内网,100=内外网',
  `purchase_date` datetime DEFAULT NULL COMMENT '购买日期',
  `price` decimal(9,2) DEFAULT NULL COMMENT '价格',
  `children` varchar(255) DEFAULT NULL,
  `del_info` int(1) DEFAULT '1' COMMENT '0=删除',
  `memo` text,
  PRIMARY KEY (`id`),
  KEY `idc_id` (`idc_id`) USING BTREE,
  KEY `public_ip` (`public_ip`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=298 DEFAULT CHARSET=utf8 COMMENT='资产信息';

-- ----------------------------
-- Table structure for data_config
-- ----------------------------
DROP TABLE IF EXISTS `data_config`;
CREATE TABLE `data_config` (
  `id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `type` tinyint(4) DEFAULT NULL,
  `name` varchar(255) COLLATE latin1_german1_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;

-- ----------------------------
-- Table structure for domain
-- ----------------------------
DROP TABLE IF EXISTS `domain`;
CREATE TABLE `domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(255) DEFAULT NULL,
  `ip` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for employee
-- ----------------------------
DROP TABLE IF EXISTS `employee`;
CREATE TABLE `employee` (
  `uid` int(5) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `username` varchar(10) DEFAULT NULL COMMENT '姓名',
  `spell` varchar(32) DEFAULT NULL COMMENT '拼音名',
  `pid` int(5) DEFAULT '0' COMMENT '大部门ID',
  `did` int(5) DEFAULT NULL COMMENT '小部门ID',
  `jober` varchar(32) DEFAULT NULL COMMENT '职位',
  `Email` varchar(250) DEFAULT NULL COMMENT '邮箱',
  `password` varchar(64) DEFAULT NULL COMMENT '邮箱密码',
  `Mobile` varchar(12) DEFAULT NULL COMMENT '手机',
  `Phone` varchar(12) DEFAULT NULL COMMENT '电话/分机',
  `IP` varchar(15) DEFAULT NULL COMMENT 'IP',
  `MAC` varchar(17) DEFAULT NULL COMMENT 'MAC',
  `OS` varchar(20) DEFAULT NULL COMMENT '电脑系统',
  `indate` date DEFAULT NULL COMMENT '入职日期',
  `outdate` date DEFAULT NULL COMMENT '离职日期',
  `del_info` smallint(1) DEFAULT NULL COMMENT '1：为正常 0：为删除',
  `update_date` date DEFAULT NULL,
  `oper_user` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=895 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for idc
-- ----------------------------
DROP TABLE IF EXISTS `idc`;
CREATE TABLE `idc` (
  `id` smallint(6) NOT NULL AUTO_INCREMENT COMMENT 'idcid',
  `area` enum('双线','网通','电信') DEFAULT NULL COMMENT 'IDC区域',
  `name` varchar(50) DEFAULT NULL COMMENT '机房名称',
  `prefix` varchar(50) DEFAULT NULL COMMENT '别名',
  `ip_range` varchar(255) DEFAULT NULL COMMENT 'ip范围',
  `mask` varchar(15) DEFAULT NULL COMMENT '掩码',
  `gateway` varchar(15) DEFAULT NULL COMMENT '网关',
  `switch` varchar(15) DEFAULT NULL COMMENT '交换机IP',
  `contact` varchar(255) DEFAULT NULL COMMENT '联系方式',
  `total_server` smallint(6) DEFAULT NULL COMMENT '总服务器数量',
  `total_online` smallint(6) DEFAULT NULL COMMENT '线上服务器数量',
  `total_server_bak` smallint(6) DEFAULT NULL COMMENT '备机服务器数量',
  `band_width` int(11) DEFAULT NULL COMMENT '带宽',
  `is_monitor` tinyint(1) DEFAULT NULL COMMENT '监控',
  `status` tinyint(1) DEFAULT NULL COMMENT '状态',
  `is_del` tinyint(1) DEFAULT '0' COMMENT '1:删除 0:使用',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COMMENT='IDC信息';

-- ----------------------------
-- Table structure for main_category
-- ----------------------------
DROP TABLE IF EXISTS `main_category`;
CREATE TABLE `main_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主分类',
  `prefix` varchar(100) NOT NULL COMMENT '拼音简称',
  `name` varchar(100) NOT NULL COMMENT '主类名一般指游戏名',
  `app_type` varchar(250) DEFAULT NULL,
  `type` binary(1) NOT NULL DEFAULT '1' COMMENT '分类 1:游戏 0:非游戏',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '游戏运营状态  -1:停运 0:未开放 1:运营',
  `is_monitor` binary(1) NOT NULL DEFAULT '0' COMMENT '0：不纳入监控 1：纳入监控',
  `is_rebot` binary(1) NOT NULL DEFAULT '0' COMMENT '1：采集 0：不采集数据',
  `is_del` binary(1) NOT NULL DEFAULT '0' COMMENT '1:删除 0：使用',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8 COMMENT='主分类';

-- ----------------------------
-- Table structure for platform
-- ----------------------------
DROP TABLE IF EXISTS `platform`;
CREATE TABLE `platform` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `main_category_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `prefix` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for sub_category
-- ----------------------------
DROP TABLE IF EXISTS `sub_category`;
CREATE TABLE `sub_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '二级分类ID',
  `main_category_id` int(11) NOT NULL COMMENT '父类ID',
  `name` varchar(50) NOT NULL COMMENT '二级分类名 一般指游戏区组',
  `prefix` varchar(32) NOT NULL COMMENT '拼音简称',
  `platform` varchar(50) DEFAULT NULL COMMENT 'IDCID',
  `status` tinyint(1) DEFAULT '1' COMMENT '区组运营状态 -1:停运  0：未对外开放,1：对外开放',
  `stage` tinyint(4) DEFAULT '3' COMMENT '-1:停运 0:未对外开放 1：内测  2：公测  3：正式',
  `is_monitor` binary(1) DEFAULT '0' COMMENT '0：不纳入监控 1：纳入监控',
  `is_rebot` binary(1) DEFAULT '0' COMMENT '0：不采集数据 1：采集数据',
  `open_date` datetime DEFAULT NULL COMMENT '开服日期',
  `close_date` datetime DEFAULT NULL COMMENT '关服、合服日期',
  `sub_category_id` int(11) DEFAULT NULL COMMENT '合服目标区组',
  `is_del` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1：删除  0：使用',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=819 DEFAULT CHARSET=utf8 COMMENT='二级分类（区组）';
