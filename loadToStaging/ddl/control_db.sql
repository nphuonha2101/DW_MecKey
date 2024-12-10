/*
 Navicat Premium Dump SQL

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80403 (8.4.3)
 Source Host           : localhost:3307
 Source Schema         : control_db

 Target Server Type    : MySQL
 Target Server Version : 80403 (8.4.3)
 File Encoding         : 65001

 Date: 07/12/2024 23:14:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for file_config
-- ----------------------------
DROP TABLE IF EXISTS `file_config`;
CREATE TABLE `file_config`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `feed_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `source_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `folder_data_path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `feed_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `transform_proc_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `load_proc_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `num_pages` int NULL DEFAULT 1,
  `staging_raw_table_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `file_delimiter` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `line_terminator` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `start_page` int NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of file_config
-- ----------------------------
INSERT INTO `file_config` VALUES (1, 'Akko Mechanic Keyboard', 'https://akkogear.com.vn/danh-muc/ban-phim/page/', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads', 'akko_feed', 'InsertToAkkoTransformed', 'LoadAkkoTransformed', 19, 'raw_akko', ',', '\\n', 2);
INSERT INTO `file_config` VALUES (2, 'CellphoneS Mechanic Keyboards', 'https://api.cellphones.com.vn/v2/graphql/query', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads', 'cps_feed', 'transform_cellphones', 'load_cellphones_transformed', 19, 'raw_cps', ',', '\\n', 1);

-- ----------------------------
-- Table structure for file_log
-- ----------------------------
DROP TABLE IF EXISTS `file_log`;
CREATE TABLE `file_log`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_config` int NULL DEFAULT NULL,
  `status` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `file_path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `is_active` bit(1) NULL DEFAULT b'1',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 223 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of file_log
-- ----------------------------
INSERT INTO `file_log` VALUES (1, 1, 'RE', '2024-11-18 14:58:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241118_145836.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (2, 1, 'EX', '2024-11-18 14:58:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241118_145836.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (3, 1, 'SE', '2024-11-18 15:00:16', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241118_145836.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (4, 1, 'RP', '2024-11-18 15:00:16', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241118_145836.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (5, 1, 'PX', '2024-11-18 15:00:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241118_145836.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (6, 1, 'SP', '2024-11-18 15:00:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241118_145836.csv', 'Successful process', b'0');
INSERT INTO `file_log` VALUES (7, 1, 'RT', '2024-11-18 15:00:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241118_145836.csv', 'Ready transform', b'0');
INSERT INTO `file_log` VALUES (8, 1, 'ST', '2024-11-18 15:01:17', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241118_145836.csv', 'Successful transform', b'0');
INSERT INTO `file_log` VALUES (9, 1, 'RL', '2024-11-18 15:01:17', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241118_145836.csv', 'Ready load', b'1');
INSERT INTO `file_log` VALUES (10, 2, 'RE', '2024-11-22 16:18:37', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_161837.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (11, 2, 'EX', '2024-11-22 16:18:37', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_161837.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (12, 2, 'FE', '2024-11-22 16:18:37', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_161837.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (13, 2, 'RE', '2024-11-22 16:20:41', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_162041.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (14, 2, 'EX', '2024-11-22 16:20:41', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_162041.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (15, 2, 'FE', '2024-11-22 16:20:41', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_162041.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (16, 2, 'RE', '2024-11-22 16:22:51', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_162251.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (17, 2, 'EX', '2024-11-22 16:22:51', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_162251.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (18, 2, 'FE', '2024-11-22 16:22:51', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_162251.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (19, 2, 'RE', '2024-11-22 16:26:14', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_162614.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (20, 2, 'EX', '2024-11-22 16:26:14', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_162614.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (21, 2, 'FE', '2024-11-22 16:26:14', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_162614.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (22, 2, 'RE', '2024-11-22 16:29:48', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_162948.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (23, 2, 'EX', '2024-11-22 16:29:48', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_162948.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (24, 2, 'FE', '2024-11-22 16:29:48', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_162948.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (25, 2, 'RE', '2024-11-22 16:32:47', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_163247.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (26, 2, 'EX', '2024-11-22 16:32:47', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_163247.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (27, 2, 'FE', '2024-11-22 16:32:47', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_163247.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (28, 2, 'RE', '2024-11-22 16:41:21', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_164121.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (29, 2, 'EX', '2024-11-22 16:41:21', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_164121.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (30, 2, 'FE', '2024-11-22 16:41:21', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_164121.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (31, 2, 'RE', '2024-11-22 16:43:51', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_164351.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (32, 2, 'EX', '2024-11-22 16:43:51', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_164351.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (33, 2, 'FE', '2024-11-22 16:43:52', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_164351.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (34, 2, 'RE', '2024-11-22 16:48:49', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_164849.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (35, 2, 'EX', '2024-11-22 16:48:49', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_164849.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (36, 2, 'FE', '2024-11-22 16:48:49', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_164849.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (37, 2, 'RE', '2024-11-22 16:57:39', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_165739.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (38, 2, 'EX', '2024-11-22 16:57:39', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_165739.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (39, 2, 'FE', '2024-11-22 16:57:39', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_165739.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (40, 2, 'RE', '2024-11-22 17:00:30', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170030.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (41, 2, 'EX', '2024-11-22 17:00:30', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170030.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (42, 2, 'FE', '2024-11-22 17:00:30', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170030.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (43, 2, 'RE', '2024-11-22 17:02:43', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170243.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (44, 2, 'EX', '2024-11-22 17:02:43', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170243.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (45, 2, 'FE', '2024-11-22 17:02:44', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170243.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (46, 2, 'RE', '2024-11-22 17:04:40', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170440.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (47, 2, 'EX', '2024-11-22 17:04:40', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170440.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (48, 2, 'FE', '2024-11-22 17:04:40', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170440.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (49, 2, 'RE', '2024-11-22 17:05:38', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170538.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (50, 2, 'EX', '2024-11-22 17:05:38', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170538.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (51, 2, 'FE', '2024-11-22 17:05:38', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170538.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (52, 2, 'RE', '2024-11-22 17:07:37', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170737.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (53, 2, 'EX', '2024-11-22 17:07:37', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170737.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (54, 2, 'SE', '2024-11-22 17:07:59', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170737.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (55, 2, 'RP', '2024-11-22 17:07:59', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170737.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (56, 2, 'RE', '2024-11-22 17:11:20', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171120.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (57, 2, 'EX', '2024-11-22 17:11:20', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171120.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (58, 2, 'FE', '2024-11-22 17:11:20', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171120.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (59, 2, 'RE', '2024-11-22 17:14:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (60, 2, 'EX', '2024-11-22 17:14:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (61, 2, 'SE', '2024-11-22 17:15:03', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (62, 2, 'RP', '2024-11-22 17:15:03', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (63, 2, 'RE', '2024-11-22 17:16:03', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171603.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (64, 2, 'EX', '2024-11-22 17:16:03', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171603.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (65, 2, 'SE', '2024-11-22 17:16:29', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171603.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (66, 2, 'RP', '2024-11-22 17:16:29', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171603.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (67, 2, 'RE', '2024-11-22 17:25:25', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_172525.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (68, 2, 'EX', '2024-11-22 17:25:25', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_172525.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (69, 2, 'SE', '2024-11-22 17:25:51', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_172525.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (70, 2, 'RP', '2024-11-22 17:25:51', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_172525.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (71, 2, 'RE', '2024-11-22 17:32:25', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_173225.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (72, 2, 'EX', '2024-11-22 17:32:25', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_173225.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (73, 2, 'SE', '2024-11-22 17:32:48', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_173225.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (74, 2, 'RP', '2024-11-22 17:32:48', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_173225.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (75, 2, 'RE', '2024-11-23 14:18:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_141836.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (76, 2, 'EX', '2024-11-23 14:18:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_141836.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (77, 2, 'FE', '2024-11-23 14:18:37', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_141836.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (78, 2, 'RE', '2024-11-23 12:29:23', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_122923.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (79, 2, 'EX', '2024-11-23 12:29:23', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_122923.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (80, 2, 'FE', '2024-11-23 12:29:24', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_122923.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (81, 2, 'RE', '2024-11-23 12:32:08', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123208.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (82, 2, 'EX', '2024-11-23 12:32:08', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123208.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (83, 2, 'FE', '2024-11-23 12:32:08', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123208.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (84, 2, 'RE', '2024-11-23 12:38:22', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (85, 2, 'EX', '2024-11-23 12:38:22', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (86, 2, 'SE', '2024-11-23 12:38:47', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (87, 2, 'RP', '2024-11-23 12:38:47', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (88, 2, 'RE', '2024-12-01 20:09:33', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241201_200933.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (89, 2, 'EX', '2024-12-01 20:09:33', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241201_200933.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (90, 2, 'SE', '2024-12-01 20:09:58', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241201_200933.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (91, 2, 'RP', '2024-12-01 20:09:58', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241201_200933.csv', 'Ready process', b'1');
INSERT INTO `file_log` VALUES (92, 2, 'RE', '2024-12-04 19:58:42', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241204_195842.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (93, 2, 'EX', '2024-12-04 19:58:43', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241204_195842.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (94, 2, 'SE', '2024-12-04 19:59:09', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241204_195842.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (95, 2, 'RP', '2024-12-04 19:59:09', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241204_195842.csv', 'Ready process', b'1');
INSERT INTO `file_log` VALUES (96, 1, 'RE', '2024-12-05 02:19:20', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_021920.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (97, 1, 'EX', '2024-12-05 02:19:20', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_021920.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (98, 1, 'SE', '2024-12-05 02:20:07', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_021920.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (99, 1, 'RP', '2024-12-05 02:20:07', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_021920.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (100, 1, 'RE', '2024-12-05 02:20:07', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_022007.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (101, 1, 'EX', '2024-12-05 02:20:07', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_022007.csv', 'Extracting', b'1');
INSERT INTO `file_log` VALUES (102, 1, 'RE', '2024-12-05 07:24:55', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072455.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (103, 1, 'EX', '2024-12-05 07:24:55', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072455.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (104, 1, 'SE', '2024-12-05 07:25:41', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072455.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (105, 1, 'RP', '2024-12-05 07:25:41', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072455.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (106, 1, 'RE', '2024-12-05 07:28:15', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072815.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (107, 1, 'EX', '2024-12-05 07:28:15', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072815.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (108, 1, 'SE', '2024-12-05 07:29:00', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072815.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (109, 1, 'RP', '2024-12-05 07:29:00', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072815.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (110, 1, 'RE', '2024-12-05 07:29:00', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072900.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (111, 1, 'EX', '2024-12-05 07:29:00', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072900.csv', 'Extracting', b'1');
INSERT INTO `file_log` VALUES (112, 1, 'RE', '2024-12-05 07:29:49', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072949.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (113, 1, 'EX', '2024-12-05 07:29:49', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072949.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (114, 1, 'SE', '2024-12-05 07:30:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072949.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (115, 1, 'RP', '2024-12-05 07:30:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072949.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (116, 1, 'RE', '2024-12-05 07:30:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073036.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (117, 1, 'EX', '2024-12-05 07:30:36', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073036.csv', 'Extracting', b'1');
INSERT INTO `file_log` VALUES (118, 1, 'RE', '2024-12-05 07:32:29', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073229.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (119, 1, 'EX', '2024-12-05 07:32:29', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073229.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (120, 1, 'SE', '2024-12-05 07:33:17', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073229.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (121, 1, 'RP', '2024-12-05 07:33:17', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073229.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (122, 1, 'RE', '2024-12-05 07:38:21', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073821.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (123, 1, 'EX', '2024-12-05 07:38:21', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073821.csv', 'Extracting', b'1');
INSERT INTO `file_log` VALUES (124, 1, 'RE', '2024-12-05 07:38:23', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073823.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (125, 1, 'EX', '2024-12-05 07:38:23', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073823.csv', 'Extracting', b'1');
INSERT INTO `file_log` VALUES (126, 1, 'RE', '2024-12-05 07:38:24', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073824.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (127, 1, 'EX', '2024-12-05 07:38:24', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073824.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (128, 1, 'RE', '2024-12-05 07:38:24', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073824.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (129, 1, 'EX', '2024-12-05 07:38:24', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073824.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (130, 1, 'RE', '2024-12-05 07:38:24', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073824.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (131, 1, 'EX', '2024-12-05 07:38:24', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073824.csv', 'Extracting', b'1');
INSERT INTO `file_log` VALUES (132, 1, 'RE', '2024-12-05 07:38:25', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073825.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (133, 1, 'EX', '2024-12-05 07:38:25', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073825.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (134, 1, 'RE', '2024-12-05 07:38:25', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073825.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (135, 1, 'EX', '2024-12-05 07:38:25', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073825.csv', 'Extracting', b'1');
INSERT INTO `file_log` VALUES (136, 1, 'RE', '2024-12-05 07:38:26', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073826.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (137, 1, 'EX', '2024-12-05 07:38:26', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073826.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (138, 1, 'RE', '2024-12-05 07:38:26', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073826.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (139, 1, 'EX', '2024-12-05 07:38:26', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073826.csv', 'Extracting', b'1');
INSERT INTO `file_log` VALUES (140, 1, 'RE', '2024-12-05 07:38:29', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073829.csv', 'Ready extract', b'1');
INSERT INTO `file_log` VALUES (141, 1, 'RE', '2024-12-05 07:38:30', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073830.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (142, 1, 'EX', '2024-12-05 07:38:30', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073830.csv', 'Extracting', b'1');
INSERT INTO `file_log` VALUES (143, 1, 'RE', '2024-12-05 07:38:38', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073838.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (144, 1, 'EX', '2024-12-05 07:38:38', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073838.csv', 'Extracting', b'1');
INSERT INTO `file_log` VALUES (145, 1, 'RE', '2024-12-05 07:40:26', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_074026.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (146, 1, 'EX', '2024-12-05 07:40:26', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_074026.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (147, 1, 'SE', '2024-12-05 07:41:13', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_074026.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (148, 1, 'RP', '2024-12-05 07:41:13', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_074026.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (149, 2, 'RE', '2024-12-05 07:42:26', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241205_074226.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (150, 2, 'EX', '2024-12-05 07:42:26', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241205_074226.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (151, 2, 'SE', '2024-12-05 07:43:45', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241205_074226.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (152, 2, 'RP', '2024-12-05 07:43:45', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241205_074226.csv', 'Ready process', b'1');
INSERT INTO `file_log` VALUES (153, 2, 'RE', '2024-12-05 07:45:50', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241205_074550.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (154, 2, 'EX', '2024-12-05 07:45:50', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241205_074550.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (155, 2, 'SE', '2024-12-05 07:47:11', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241205_074550.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (156, 2, 'RP', '2024-12-05 07:47:11', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241205_074550.csv', 'Ready process', b'1');
INSERT INTO `file_log` VALUES (157, 1, 'RE', '2024-12-06 12:34:29', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241206_123429.csv', 'Ready extract', b'0');
INSERT INTO `file_log` VALUES (158, 1, 'EX', '2024-12-06 12:34:29', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241206_123429.csv', 'Extracting', b'0');
INSERT INTO `file_log` VALUES (159, 1, 'SE', '2024-12-06 12:36:57', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241206_123429.csv', 'Successful extract', b'0');
INSERT INTO `file_log` VALUES (160, 1, 'RP', '2024-12-06 12:36:57', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241206_123429.csv', 'Ready process', b'0');
INSERT INTO `file_log` VALUES (161, 1, 'PX', '2024-12-06 20:07:31', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_021920.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (162, 1, 'FE', '2024-12-06 20:07:31', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_021920.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (163, 1, 'PX', '2024-12-06 20:07:35', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072455.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (164, 1, 'FE', '2024-12-06 20:07:35', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072455.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (165, 1, 'PX', '2024-12-06 20:07:37', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072815.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (166, 1, 'FE', '2024-12-06 20:07:37', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072815.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (167, 1, 'PX', '2024-12-06 20:07:38', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072949.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (168, 1, 'FE', '2024-12-06 20:07:38', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_072949.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (169, 1, 'PX', '2024-12-06 20:08:24', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073229.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (170, 1, 'FE', '2024-12-06 20:08:24', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_073229.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (171, 1, 'PX', '2024-12-06 20:09:47', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_074026.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (172, 1, 'FE', '2024-12-06 20:09:47', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241205_074026.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (173, 1, 'PX', '2024-12-06 20:11:01', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241206_123429.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (174, 1, 'RL', '2024-12-06 20:11:01', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/akko_20241206_123429.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (175, 2, 'PX', '2024-12-06 20:14:15', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170737.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (176, 2, 'FE', '2024-12-06 20:14:17', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_170737.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (177, 2, 'PX', '2024-12-06 20:15:27', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (178, 2, 'RT', '2024-12-06 20:15:32', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Failed extract', b'0');
INSERT INTO `file_log` VALUES (179, 2, 'PX', '2024-12-06 20:17:00', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171603.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (180, 2, 'FE', '2024-12-06 20:17:00', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171603.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (181, 2, 'PX', '2024-12-06 20:44:19', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_172525.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (182, 2, 'FE', '2024-12-06 20:44:19', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_172525.csv', 'Failed extract', b'1');
INSERT INTO `file_log` VALUES (183, 2, 'RT', '2024-12-06 23:12:30', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Ready transform', b'0');
INSERT INTO `file_log` VALUES (184, 2, 'TX', '2024-12-06 23:12:30', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Transforming', b'0');
INSERT INTO `file_log` VALUES (185, 2, 'RT', '2024-12-06 23:12:30', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Failed transform', b'0');
INSERT INTO `file_log` VALUES (186, 2, 'RT', '2024-12-06 23:15:08', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Ready transform', b'0');
INSERT INTO `file_log` VALUES (187, 2, 'TX', '2024-12-06 23:15:08', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Transforming', b'0');
INSERT INTO `file_log` VALUES (188, 2, 'FT', '2024-12-06 23:15:08', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Failed transform', b'0');
INSERT INTO `file_log` VALUES (189, 2, 'RT', '2024-12-07 03:40:07', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Ready transform', b'0');
INSERT INTO `file_log` VALUES (190, 2, 'TX', '2024-12-07 03:40:07', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Transforming', b'0');
INSERT INTO `file_log` VALUES (191, 2, 'FT', '2024-12-07 03:40:07', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Failed transform', b'0');
INSERT INTO `file_log` VALUES (192, 2, 'RT', '2024-12-07 03:41:57', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Ready transform', b'0');
INSERT INTO `file_log` VALUES (193, 2, 'TX', '2024-12-07 03:41:57', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Transforming', b'0');
INSERT INTO `file_log` VALUES (194, 2, 'ST', '2024-12-07 03:41:57', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Successful transform', b'0');
INSERT INTO `file_log` VALUES (195, 2, 'RL', '2024-12-07 03:41:57', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_171436.csv', 'Ready load', b'1');
INSERT INTO `file_log` VALUES (196, 2, 'PX', '2024-12-07 03:53:18', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_173225.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (197, 2, 'FP', '2024-12-07 03:53:18', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241122_173225.csv', 'Failed process', b'1');
INSERT INTO `file_log` VALUES (198, 2, 'PX', '2024-12-07 01:00:39', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (199, 2, 'SP', '2024-12-07 01:00:39', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Successful process', b'0');
INSERT INTO `file_log` VALUES (200, 2, 'RT', '2024-12-07 01:00:39', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Ready transform', b'0');
INSERT INTO `file_log` VALUES (201, 2, 'PX', '2024-12-07 01:08:22', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (202, 2, 'PX', '2024-12-07 01:10:39', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (203, 2, 'PX', '2024-12-07 01:11:46', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Processing', b'0');
INSERT INTO `file_log` VALUES (204, 2, 'SP', '2024-12-07 01:11:46', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Successful process', b'0');
INSERT INTO `file_log` VALUES (205, 2, 'RT', '2024-12-07 01:11:46', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Ready transform', b'0');
INSERT INTO `file_log` VALUES (206, 2, 'RT', '2024-12-07 01:23:41', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Ready transform', b'0');
INSERT INTO `file_log` VALUES (207, 2, 'TX', '2024-12-07 01:23:41', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Transforming', b'0');
INSERT INTO `file_log` VALUES (208, 2, 'ST', '2024-12-07 01:23:41', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Successful transform', b'0');
INSERT INTO `file_log` VALUES (209, 2, 'RL', '2024-12-07 01:23:41', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Ready load', b'0');
INSERT INTO `file_log` VALUES (210, 2, 'RT', '2024-12-07 01:23:44', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Ready transform', b'0');
INSERT INTO `file_log` VALUES (211, 2, 'TX', '2024-12-07 01:23:44', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Transforming', b'0');
INSERT INTO `file_log` VALUES (212, 2, 'ST', '2024-12-07 01:23:44', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Successful transform', b'0');
INSERT INTO `file_log` VALUES (213, 2, 'RL', '2024-12-07 01:23:44', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Ready load', b'0');
INSERT INTO `file_log` VALUES (214, 2, 'RT', '2024-12-07 01:24:48', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Ready transform', b'0');
INSERT INTO `file_log` VALUES (215, 2, 'TX', '2024-12-07 01:24:49', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Transforming', b'0');
INSERT INTO `file_log` VALUES (216, 2, 'FT', '2024-12-07 01:24:49', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Failed transform', b'0');
INSERT INTO `file_log` VALUES (217, 2, 'RT', '2024-12-07 01:28:06', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Ready transform', b'0');
INSERT INTO `file_log` VALUES (218, 2, 'TX', '2024-12-07 01:28:06', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Transforming', b'0');
INSERT INTO `file_log` VALUES (219, 2, 'FT', '2024-12-07 01:28:07', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Failed transform', b'0');
INSERT INTO `file_log` VALUES (220, 2, 'RT', '2024-12-07 01:28:09', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Ready transform', b'0');
INSERT INTO `file_log` VALUES (221, 2, 'TX', '2024-12-07 01:28:09', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Transforming', b'0');
INSERT INTO `file_log` VALUES (222, 2, 'FT', '2024-12-07 01:28:09', 'D:/ProgramData/MySQL/MySQL Server 8.4.3/Uploads/cps_20241123_123822.csv', 'Failed transform', b'1');

-- ----------------------------
-- Procedure structure for InsertFileLog
-- ----------------------------
DROP PROCEDURE IF EXISTS `InsertFileLog`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `InsertFileLog`(IN id_config INT, IN status VARCHAR(2), IN file_path TEXT, IN description VARCHAR(255))
BEGIN
  DECLARE inserted_id BIGINT;
  
  START TRANSACTION;
  BEGIN
    DECLARE EXIT HANDLER for SQLEXCEPTION
    BEGIN
      ROLLBACK;
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Có lỗi xảy ra';
    END;
    
    INSERT INTO file_log(id_config, `status`, file_path, description)
    VALUES(id_config, status, file_path, description);
    
    SET inserted_id = (SELECT LAST_INSERT_ID());
    
    UPDATE file_log SET is_active = 0 WHERE file_log.id != inserted_id AND file_log.id_config = id_config AND file_log.file_path = file_path;
    
    
    COMMIT;
  END;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
