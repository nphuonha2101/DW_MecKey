/*
 Navicat Premium Dump SQL

 Source Server         : MySQL 8.4.3
 Source Server Type    : MySQL
 Source Server Version : 80403 (8.4.3)
 Source Host           : localhost:3306
 Source Schema         : control_db

 Target Server Type    : MySQL
 Target Server Version : 80403 (8.4.3)
 File Encoding         : 65001

 Date: 05/11/2024 23:16:59
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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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

-- ----------------------------
-- Procedure structure for LoadCSVFile
-- ----------------------------
DROP PROCEDURE IF EXISTS `LoadCSVFile`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `LoadCSVFile`(
    IN file_path VARCHAR(255),
    IN table_name VARCHAR(64),
    IN fields_terminated CHAR(1),
    IN lines_terminated CHAR(1)
)
BEGIN
    SET @load_query = CONCAT(
        "LOAD DATA INFILE '",
        file_path,
        "' INTO TABLE ",
        table_name,
        " FIELDS TERMINATED BY '",
        fields_terminated,
        "' LINES TERMINATED BY '",
        lines_terminated,
        "' IGNORE 1 LINES;"
    );
    
    -- Kiểm tra quyền FILE
    SET @have_file_privilege = 0;
    SELECT COUNT(*) INTO @have_file_privilege 
    FROM information_schema.user_privileges 
    WHERE grantee LIKE CONCAT("'", CURRENT_USER, "'") 
    AND PRIVILEGE_TYPE = 'FILE';
    
    -- Kiểm tra sự tồn tại của bảng
    SET @table_exists = 0;
    SELECT COUNT(*) INTO @table_exists 
    FROM information_schema.tables 
    WHERE table_schema = DATABASE() 
    AND table_name = table_name;
    
    -- Kiểm tra file có tồn tại
    SET @file_exists = 0;
    SELECT COUNT(*) INTO @file_exists 
    FROM information_schema.files 
    WHERE file_name = file_path;
    
    -- Xử lý các điều kiện lỗi
    IF @have_file_privilege = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User không có quyền FILE';
    ELSEIF @table_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Bảng không tồn tại';
    ELSEIF @file_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'File không tồn tại hoặc không thể truy cập';
    ELSE
        -- Thực thi câu lệnh LOAD DATA
        PREPARE stmt FROM @load_query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        -- Trả về số dòng đã được import
        SELECT COUNT(*) AS imported_rows FROM table_name;
    END IF;
    
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
