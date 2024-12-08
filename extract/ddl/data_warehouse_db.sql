/*
 Navicat Premium Dump SQL

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80403 (8.4.3)
 Source Host           : localhost:3307
 Source Schema         : data_warehouse_db

 Target Server Type    : MySQL
 Target Server Version : 80403 (8.4.3)
 File Encoding         : 65001

 Date: 07/12/2024 23:17:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for date_dim
-- ----------------------------
DROP TABLE IF EXISTS `date_dim`;
CREATE TABLE `date_dim`  (
  `id` int NOT NULL,
  `date` date NULL DEFAULT NULL,
  `weekday_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `month` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `year` int NULL DEFAULT NULL,
  `day` int NULL DEFAULT NULL,
  `day_of_year` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for keyboard
-- ----------------------------
DROP TABLE IF EXISTS `keyboard`;
CREATE TABLE `keyboard`  (
  `SKU` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `name` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  `image` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `model` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `mode` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `switch` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `keycap` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `size` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `weight` decimal(10, 2) NULL DEFAULT NULL,
  `accessory` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `manufacturer` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `source` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `is_active` bit(1) NULL DEFAULT NULL,
  `date` datetime NULL DEFAULT NULL,
  `expired_date` datetime NULL DEFAULT '9999-12-31 00:00:00',
  `id` bigint NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `SKU`(`SKU` ASC) USING BTREE,
  UNIQUE INDEX `SKU_2`(`SKU` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for keyboard_price_fact
-- ----------------------------
DROP TABLE IF EXISTS `keyboard_price_fact`;
CREATE TABLE `keyboard_price_fact`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `SKU` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  `id_date_dim` bigint NULL DEFAULT NULL,
  `source` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for temp_insert_keyboard_dim
-- ----------------------------
DROP TABLE IF EXISTS `temp_insert_keyboard_dim`;
CREATE TABLE `temp_insert_keyboard_dim`  (
  `SKU` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `image` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  `model` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `mode` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `switch` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `keycap` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `size` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `weight` decimal(10, 2) NULL DEFAULT NULL,
  `accessory` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `date` datetime NULL DEFAULT NULL,
  `manufacturer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `source` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`SKU`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for temp_keyboard_dim_exists
-- ----------------------------
DROP TABLE IF EXISTS `temp_keyboard_dim_exists`;
CREATE TABLE `temp_keyboard_dim_exists`  (
  `SKU` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `image` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  `model` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `mode` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `switch` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `keycap` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `size` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `weight` decimal(10, 2) NULL DEFAULT NULL,
  `accessory` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `date` datetime NULL DEFAULT NULL,
  `manufacturer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `source` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`SKU`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for temp_keyboard_dim_not_exists
-- ----------------------------
DROP TABLE IF EXISTS `temp_keyboard_dim_not_exists`;
CREATE TABLE `temp_keyboard_dim_not_exists`  (
  `SKU` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `image` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  `model` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `mode` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `switch` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `keycap` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `size` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `weight` decimal(10, 2) NULL DEFAULT NULL,
  `accessory` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `date` datetime NULL DEFAULT NULL,
  `manufacturer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `source` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`SKU`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Function structure for check_difference
-- ----------------------------
DROP FUNCTION IF EXISTS `check_difference`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `check_difference`(
    p_SKU VARCHAR(255)
) RETURNS tinyint(1)
    READS SQL DATA
BEGIN
    DECLARE diff_found tinyint(1) DEFAULT 0;

    SELECT 
        CASE 
            WHEN temp_exists.name != keyboard_dim.name OR
                 temp_exists.image != keyboard_dim.image OR
                 temp_exists.price != keyboard_dim.price OR
                 temp_exists.model != keyboard_dim.model OR
                 temp_exists.mode != keyboard_dim.mode OR
                 temp_exists.switch != keyboard_dim.switch OR
                 temp_exists.keycap != keyboard_dim.keycap OR
                 temp_exists.size != keyboard_dim.size OR
                 temp_exists.weight != keyboard_dim.weight OR
                 temp_exists.accessory != keyboard_dim.accessory OR
                 temp_exists.manufacturer != keyboard_dim.manufacturer
            THEN 1
            ELSE 0
        END INTO diff_found
    FROM temp_keyboard_dim_exists AS temp_exists
    JOIN keyboard AS keyboard_dim ON temp_exists.SKU = keyboard_dim.SKU
    WHERE temp_exists.SKU = p_SKU;

    RETURN diff_found;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for DeleteDuplicateFactRecord
-- ----------------------------
DROP PROCEDURE IF EXISTS `DeleteDuplicateFactRecord`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteDuplicateFactRecord`()
BEGIN
   
    DELETE t1
    FROM keyboard_price_fact t1
    INNER JOIN keyboard_price_fact t2 
    ON t1.id_date_dim = t2.id_date_dim
       AND t1.SKU = t2.SKU
       AND t1.id > t2.id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for HandleDuplicate
-- ----------------------------
DROP PROCEDURE IF EXISTS `HandleDuplicate`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `HandleDuplicate`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE keyboard_sku VARCHAR(255);
    
  
    DECLARE cur CURSOR FOR SELECT SKU FROM temp_keyboard_dim_exists;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET done = TRUE; 
    END;

    START TRANSACTION;
    
    TRUNCATE temp_keyboard_dim_exists;

    INSERT INTO temp_keyboard_dim_exists (SKU, name, image, price, model, mode, switch, keycap, size, weight, accessory, date, manufacturer, source) 
    SELECT SKU, name, image, price, model, mode, switch, keycap, size, weight, accessory, date, manufacturer, source
    FROM temp_insert_keyboard_dim 
    WHERE EXISTS (SELECT 1 FROM keyboard WHERE keyboard.SKU = temp_insert_keyboard_dim.SKU);

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO keyboard_sku;
        IF done THEN
            LEAVE read_loop;
        END IF;
               
        IF check_difference(keyboard_sku) THEN
            UPDATE keyboard
            SET expired_date = NOW(), is_active = 0
            WHERE SKU = keyboard_sku AND is_active = 1;

            CALL UpdateKeyboardRecords(keyboard_sku);
        END IF;

        -- Chèn vào bảng fact
        CALL InsertToFact(keyboard_sku, 'temp_keyboard_dim_exists');
    END LOOP;

    CLOSE cur;

    COMMIT;

END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for HandleNotDuplicate
-- ----------------------------
DROP PROCEDURE IF EXISTS `HandleNotDuplicate`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `HandleNotDuplicate`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE s_SKU VARCHAR(255);
    DECLARE s_name TEXT;
    DECLARE s_price DECIMAL(10, 2);
    DECLARE s_image TEXT;
    DECLARE s_model TEXT;
    DECLARE s_mode TEXT;
    DECLARE s_switch TEXT;
    DECLARE s_keycap TEXT;
    DECLARE s_size TEXT;
    DECLARE s_weight DECIMAL(10, 2);
    DECLARE s_accessory TEXT;
    DECLARE s_date DATETIME;
    DECLARE s_manufacturer TEXT;
    DECLARE s_source TEXT;

    DECLARE cur CURSOR FOR SELECT SKU, NAME, price, image, model, MODE, switch, keycap, size, weight, accessory, DATE, manufacturer, source FROM temp_keyboard_dim_not_exists;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    START TRANSACTION;
    
    TRUNCATE temp_keyboard_dim_not_exists;

    INSERT INTO temp_keyboard_dim_not_exists (SKU, NAME, image, price, model, MODE, switch, keycap, size, weight, accessory, DATE, manufacturer, source) 
    SELECT SKU, NAME, image, price, model, MODE, switch, keycap, size, weight, accessory, DATE, manufacturer, source 
    FROM temp_insert_keyboard_dim 
    WHERE NOT EXISTS (SELECT 1 FROM keyboard WHERE keyboard.SKU = temp_insert_keyboard_dim.SKU);

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO s_sku, s_name, s_price, s_image, s_model, s_mode, s_switch, s_keycap, s_size, s_weight, s_accessory, s_date, s_manufacturer, s_source;
        IF done THEN
            LEAVE read_loop;
        END IF;

        
        BEGIN
            DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
            BEGIN
                ROLLBACK;
                SELECT "ERROR TO INSERT FROM NOT EXITS TO KEYBOARD" as status;
                SET done = TRUE; 
            END;

            INSERT INTO keyboard (SKU, NAME, price, image, model, MODE, switch, keycap, size, weight, accessory, DATE, manufacturer, source, is_active) 
            VALUES(s_sku, s_name, s_price, s_image, s_model, s_mode, s_switch, s_keycap, s_size, s_weight, s_accessory, s_date, s_manufacturer, s_source, 1);
            
            -- Chèn vào bảng fact
            CALL InsertToFact(s_sku, 'temp_keyboard_dim_not_exists');
        END;

    END LOOP;

    CLOSE cur;

    COMMIT;

END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for InsertToFact
-- ----------------------------
DROP PROCEDURE IF EXISTS `InsertToFact`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `InsertToFact`(IN SKU VARCHAR(255), IN table_source_name VARCHAR(255))
BEGIN 
    DECLARE s_SKU VARCHAR(255);
    DECLARE s_price DECIMAL(10, 2); 
    DECLARE s_date DATETIME; 
    DECLARE s_source TEXT;
    DECLARE id_date_dim BIGINT;

    -- Kiểm tra xem bảng keyboard_price_fact đã tồn tại hay chưa
    IF NOT EXISTS (SELECT * FROM information_schema.tables WHERE table_schema = 'data_warehouse_db' AND table_name = 'keyboard_price_fact') THEN
        CREATE TABLE data_warehouse_db.keyboard_price_fact
        (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            SKU VARCHAR(255), 
            price DECIMAL(10, 2), 
            id_date_dim BIGINT,
            source TEXT
        );
    END IF; 

    -- Tạo câu truy vấn SELECT vào chuỗi
    SET @query = CONCAT('SELECT SKU, price, DATE, source FROM ', table_source_name, ' WHERE SKU = ?');
    PREPARE stmt FROM @query;
    SET @SKU = SKU; 
    EXECUTE stmt USING @SKU;

    -- Gán giá trị vào biến bằng cách sử dụng SELECT INTO
    SET @s_query = CONCAT('SELECT SKU, price, DATE, source INTO @s_SKU, @s_price, @s_date, @s_source FROM ', table_source_name, ' WHERE SKU = ?');
    PREPARE s_stmt FROM @s_query;
    EXECUTE s_stmt USING @SKU;

    -- Gán lại giá trị vào biến từ biến SQL
    SET s_SKU = @s_SKU;
    SET s_price = @s_price;
    SET s_date = @s_date;
    SET s_source = @s_source;

    -- Lấy id_date_dim
    SET id_date_dim = (SELECT id FROM date_dim WHERE date = s_date);
    
    -- Xem giá trị các biến
    SELECT s_SKU, s_price, id_date_dim, s_source;

    -- Chèn dữ liệu vào bảng keyboard_price_fact
--     IF NOT EXISTS (SELECT 1 FROM keyboard_price_fact WHERE SKU = s_SKU AND id_date_dim = id_date_dim) THEN
        INSERT INTO keyboard_price_fact (SKU, price, id_date_dim, source)
        VALUES(s_SKU, s_price, id_date_dim, s_source);
--     END IF;
    
    -- Giải phóng bộ nhớ cho câu lệnh chuẩn bị
    DEALLOCATE PREPARE stmt;
    DEALLOCATE PREPARE s_stmt;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for LoadAkkoTransformed
-- ----------------------------
DROP PROCEDURE IF EXISTS `LoadAkkoTransformed`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `LoadAkkoTransformed`()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Rollback nếu có lỗi
        ROLLBACK;
        DO RELEASE_LOCK('temp_insert_keyboard_dim_lock');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Procedure failed.';
    END;

    IF GET_LOCK('temp_insert_keyboard_dim_lock', 60) THEN
        START TRANSACTION;
        
        TRUNCATE temp_insert_keyboard_dim;

        INSERT INTO temp_insert_keyboard_dim (SKU, NAME, image, price, model, MODE, switch, keycap, size, weight, accessory, DATE, manufacturer, source) 
      SELECT
          SKU,
          NAME,
          image,
          price,
          model,
          MODE,
          switch,
          keycap,
          size,
          weight,
          accessory,
          DATE,
          manufacturer,
          source
      FROM
          data_staging_db.transformed_akko;
            
        -- Commit thay đổi
        COMMIT;
        
        CALL HandleDuplicate();
        CALL HandleNotDuplicate();
  
        CALL DeleteDuplicateFactRecord();
           
        -- Giải phóng khóa
        DO RELEASE_LOCK('temp_insert_keyboard_dim_lock');

    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Failed to acquire lock within timeout.';
    END IF;
    
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for load_cellphones_transformed
-- ----------------------------
DROP PROCEDURE IF EXISTS `load_cellphones_transformed`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `load_cellphones_transformed`()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Rollback nếu có lỗi
        ROLLBACK;
        DO RELEASE_LOCK('temp_insert_keyboard_dim_lock');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Procedure failed.';
    END;

    IF GET_LOCK('temp_insert_keyboard_dim_lock', 60) THEN
        START TRANSACTION;
        
        -- Làm sạch bảng
        TRUNCATE temp_insert_keyboard_dim;

        -- Chèn dữ liệu mới từ transformed_cellphones
        INSERT INTO temp_insert_keyboard_dim (SKU, NAME, image, price, model, MODE, switch, keycap, size, weight, accessory, DATE, manufacturer, source) 
        SELECT
            id,
            name,
            image,
            price,
            type,
            mode,
            switch,
            keycap,
            size,
            weight,
            accessory,
            date,
            manufacturer,
            source
        FROM
            data_staging_db.transformed_cellphones;
        
        -- Commit transaction
        COMMIT;
        
        CALL HandleDuplicate();
        CALL HandleNotDuplicate();
  
        CALL DeleteDuplicateFactRecord();

        -- Giải phóng khóa
        DO RELEASE_LOCK('temp_insert_keyboard_dim_lock');
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Failed to acquire lock within timeout.';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for UpdateKeyboardRecords
-- ----------------------------
DROP PROCEDURE IF EXISTS `UpdateKeyboardRecords`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateKeyboardRecords`(IN SKU VARCHAR(255))
BEGIN
     -- Insert dòng mới vào keyboard dim
     INSERT INTO keyboard (SKU, name, image, price, model, mode, switch, keycap, size, weight, accessory, manufacturer, date, is_active, source)
    SELECT SKU, name, image, price, model, mode, switch, keycap, size, weight, accessory, manufacturer, date, 1, source
    FROM temp_keyboard_dim_exists
    WHERE SKU = SKU;

END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
