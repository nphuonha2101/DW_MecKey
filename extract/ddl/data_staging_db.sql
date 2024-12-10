/*
 Navicat Premium Dump SQL

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80403 (8.4.3)
 Source Host           : localhost:3307
 Source Schema         : data_staging_db

 Target Server Type    : MySQL
 Target Server Version : 80403 (8.4.3)
 File Encoding         : 65001

 Date: 07/12/2024 23:15:09
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for raw_akko
-- ----------------------------
DROP TABLE IF EXISTS `raw_akko`;
CREATE TABLE `raw_akko`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `price` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `image` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `model` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `mode` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `switch` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `keycap` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `size` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `weight` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `accessory` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 214 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for raw_cps
-- ----------------------------
DROP TABLE IF EXISTS `raw_cps`;
CREATE TABLE `raw_cps`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `keycap` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `type` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `number_of_keys` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `mode` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `led` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `battery` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `compatibility` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `size` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `image` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `manufacturer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `weight` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sku` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `price` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `discount_price` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `date` date NULL DEFAULT NULL,
  PRIMARY KEY (`id` DESC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 381 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for transformed_akko
-- ----------------------------
DROP TABLE IF EXISTS `transformed_akko`;
CREATE TABLE `transformed_akko`  (
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
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '_utf8mb4\\\'AKKO\\\'',
  `date` datetime NULL DEFAULT NULL,
  `manufacturer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`SKU`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for transformed_cellphones
-- ----------------------------
DROP TABLE IF EXISTS `transformed_cellphones`;
CREATE TABLE `transformed_cellphones`  (
  `sku` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `keycap` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `type` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `number_of_keys` int NULL DEFAULT NULL,
  `mode` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `led` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `battery` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `compatibility` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `size` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `image` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `manufacturer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `weight` decimal(10, 2) NULL DEFAULT NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  `discount_price` decimal(10, 2) NULL DEFAULT NULL,
  `date` date NULL DEFAULT NULL,
  `switch` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `accessory` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `source` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`sku`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Procedure structure for CreateTransformedAkko
-- ----------------------------
DROP PROCEDURE IF EXISTS `CreateTransformedAkko`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CreateTransformedAkko`()
BEGIN
    IF NOT EXISTS (
        SELECT * 
        FROM information_schema.TABLES 
        WHERE table_name = 'transformed_akko' 
        AND table_schema = 'data_staging_db'
    ) THEN
        CREATE TABLE transformed_akko (
            SKU VARCHAR(255) PRIMARY KEY,
            name TEXT,
            image TEXT,
            price DECIMAL(10, 2),
            model TEXT,
            mode TEXT,
            switch TEXT,
            keycap TEXT,
            size TEXT,
            weight DECIMAL(10, 2),
            accessory TEXT,
            source VARCHAR(255) DEFAULT('AKKO'),
            date DATETIME 
        );
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for InsertToAkkoTransformed
-- ----------------------------
DROP PROCEDURE IF EXISTS `InsertToAkkoTransformed`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `InsertToAkkoTransformed`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE src_name TEXT;
    DECLARE src_image TEXT;
    DECLARE src_price VARCHAR(255);
    DECLARE src_model TEXT;
    DECLARE src_mode TEXT;
    DECLARE src_switch TEXT;
    DECLARE src_keycap TEXT;
    DECLARE src_size VARCHAR(255);
    DECLARE src_weight VARCHAR(255);
    DECLARE src_accessory TEXT;
    DECLARE src_date DATE;
    DECLARE cleaned_weight DECIMAL(10, 2);
    DECLARE cleaned_price DECIMAL(10, 2);
    DECLARE generated_SKU VARCHAR(255);

    -- Định nghĩa CURSOR để lấy dữ liệu từ bảng raw_akko
    DECLARE cur CURSOR FOR 
    SELECT name, image, price, model, mode, switch, keycap, size, weight, accessory, date 
    FROM raw_akko;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    TRUNCATE transformed_akko;

    -- Mở CURSOR
    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO src_name, src_image, src_price, src_model, src_mode, src_switch, src_keycap, src_size, src_weight, src_accessory, src_date;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Làm sạch giá trị weight
        SET src_weight = REPLACE(REPLACE(REPLACE(LOWER(src_weight), 'kg', ''), 'nặng', ''), '~', '');

        IF src_weight = 'Unknown' OR src_weight = 'unknown' OR src_weight = '' THEN
            SET cleaned_weight = (SELECT AVG(weight) FROM transformed_akko WHERE weight IS NOT NULL);
        ELSE
            SET cleaned_weight = TRIM(REPLACE(src_weight, ' ', ''));
            -- Kiểm tra và chuyển đổi nếu có giá trị hợp lệ
            IF cleaned_weight REGEXP '^[0-9]+(\\.[0-9]+)?$' THEN
                SET cleaned_weight = CAST(cleaned_weight AS DECIMAL(10, 2));
            ELSE
                SET cleaned_weight = (SELECT AVG(weight) FROM transformed_akko WHERE weight IS NOT NULL);
            END IF;
        END IF;

        -- Làm sạch giá trị price
        IF src_price IS NOT NULL AND src_price REGEXP '^[0-9]+(\\.[0-9]+)?$' THEN
            SET cleaned_price = CAST(src_price AS DECIMAL(10, 2));
        ELSE
            SET cleaned_price = (SELECT AVG(price) FROM transformed_akko WHERE price IS NOT NULL);
        END IF;
        
        IF LOWER(src_name) = 'unknown' AND src_model IS NOT NULL THEN
          SET src_name = src_model;
        END IF;
        
        -- Chuyển ký tự nhân trong size
        SET src_size = REPLACE(REPLACE(REPLACE(src_size, ' ', ''), '*', 'x'), 'x', ' x ');

        
        -- Loại bỏ thẻ HTML
        SET src_switch = REGEXP_REPLACE(src_switch, '</?[^>]+>', '');
        SET src_mode = REGEXP_REPLACE(src_switch, '</?[^>]+>', '');
        SET src_model = REGEXP_REPLACE(src_switch, '</?[^>]+>', '');

        -- Tạo SKU
        SET generated_SKU = MD5(CONCAT(src_name, '-', src_model, '-', src_switch, '-', src_keycap));

        -- Chèn dữ liệu vào bảng đích
        INSERT INTO transformed_akko(name, image, price, model, mode, switch, keycap, size, weight, accessory, date, SKU, manufacturer)
        VALUES (src_name, src_image, cleaned_price, src_model, src_mode, src_switch, src_keycap, src_size, cleaned_weight, src_accessory, src_date, generated_SKU, 'AKKO');

    END LOOP;

    -- Đóng CURSOR
    CLOSE cur;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for transform_cellphones
-- ----------------------------
DROP PROCEDURE IF EXISTS `transform_cellphones`;
delimiter ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `transform_cellphones`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE src_name TEXT;
    DECLARE src_keycap TEXT;
    DECLARE src_type TEXT;
    DECLARE src_number_of_keys VARCHAR(255);
    DECLARE src_mode TEXT;
    DECLARE src_led TEXT;
    DECLARE src_battery TEXT;
    DECLARE src_compatibility TEXT;
    DECLARE src_size VARCHAR(255);
    DECLARE src_image TEXT;
    DECLARE src_manufacturer TEXT;
    DECLARE src_weight VARCHAR(255);
    DECLARE src_sku TEXT;
    DECLARE src_price VARCHAR(255);
    DECLARE src_discount_price VARCHAR(255);
    DECLARE src_date DATE;

    DECLARE cleaned_number_of_keys INT;
    DECLARE cleaned_weight DECIMAL(10, 2);
    DECLARE cleaned_price DECIMAL(10, 2);
    DECLARE cleaned_discount_price DECIMAL(10, 2);

	-- 	Biến lưu giá trị xuất hiện nhiều nhất
    DECLARE mode_price VARCHAR(255);
    DECLARE mode_discount_price VARCHAR(255);
    
	
    DECLARE cur CURSOR FOR
    SELECT name, keycap, type, number_of_keys, mode, led, battery, compatibility, size, image, manufacturer, weight, sku, price, discount_price, date
    FROM raw_cps
    WHERE name != 'N/A' AND image != 'N/A';

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Lấy ra giá trị xuất hiện nhiều nhất
    SELECT price INTO mode_price
    FROM raw_cps
    WHERE price != 'N/A'
    GROUP BY price
    ORDER BY COUNT(*) DESC
    LIMIT 1;
	
	SELECT discount_price INTO mode_discount_price
    FROM raw_cps
    WHERE discount_price != 'N/A'
    GROUP BY discount_price
    ORDER BY COUNT(*) DESC
    LIMIT 1;
 

	TRUNCATE transformed_cellphones;
	
    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO src_name, src_keycap, src_type, src_number_of_keys, src_mode, src_led, src_battery, src_compatibility, src_size, src_image, src_manufacturer, src_weight, src_sku, src_price, src_discount_price, src_date;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Thay giá trị N/A bằng giá trị xuất hiện nhiều nhất 
        SET src_price = CASE WHEN src_price = 'N/A' THEN mode_price ELSE src_price END;
        SET src_discount_price = CASE WHEN src_discount_price = 'N/A' THEN mode_discount_price ELSE src_discount_price END;
        

        -- Xử lý number_of_keys chỉ lấy số
        SET cleaned_number_of_keys =
		CASE
			WHEN src_number_of_keys = 'N/A' THEN NULL
			ELSE CAST(REGEXP_SUBSTR(TRIM(LOWER(src_number_of_keys)), '[0-9]+') AS UNSIGNED)
		END;


        -- Bỏ thẻ br ra khỏi battery
        SET src_battery =
		CASE
			WHEN src_battery = 'N/A' THEN src_battery
			ELSE REGEXP_REPLACE(src_battery, '</?[^>]+>', '')
		END;


        -- Xử lý weight chuyển về (kg)
        SET cleaned_weight = 
		CASE
			WHEN src_weight = 'N/A' THEN NULL
			WHEN src_weight LIKE '%kg%' 
			THEN CAST(SUBSTRING_INDEX(src_weight, ' ', 1) AS DECIMAL)
			WHEN src_weight LIKE '%g%' 
			THEN CAST(SUBSTRING_INDEX(src_weight, ' ', 1) AS DECIMAL) / 1000
			ELSE NULL
		END;


        -- Chuyển đổi price và discount_price
        SET cleaned_price =
		CASE
			WHEN src_price = 'N/A' THEN NULL
			ELSE CAST(src_price AS DECIMAL(10, 2))
		END;

		SET cleaned_discount_price =
		CASE
			WHEN src_discount_price = 'N/A' THEN NULL
			ELSE CAST(src_discount_price AS DECIMAL(10, 2))
		END;
    
        SET src_sku = MD5(CONCAT(src_name, '-', src_mode, '-', src_keycap, '-', src_manufacturer));
        
        INSERT INTO transformed_cellphones
        (sku, name, keycap, type, number_of_keys, mode, led, battery, compatibility, size, image, manufacturer, weight, price, discount_price, date, switch, accessory, source)
        VALUES
        (src_sku, src_name, src_keycap, src_type, cleaned_number_of_keys, src_mode, src_led, src_battery, src_compatibility, src_size, src_image, src_manufacturer, cleaned_weight, cleaned_price, cleaned_discount_price, src_date, 'N/A', 'N/A', 'Cellphone S');
    END LOOP;

    
    CLOSE cur;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table transformed_akko
-- ----------------------------
DROP TRIGGER IF EXISTS `before_insert_transformed_akko`;
delimiter ;;
CREATE TRIGGER `before_insert_transformed_akko` BEFORE INSERT ON `transformed_akko` FOR EACH ROW BEGIN
    -- Kiểm tra tên
    IF NEW.name IS NULL OR NEW.name = 'Unknown' OR NEW.name = 'unknown' THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Keyboard name must not be empty';
    END IF;

    -- Kiểm tra ngày
    IF NEW.date IS NOT NULL AND NEW.date < '1970-01-01' THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Date must be after 1970-01-01';
    END IF;

    -- Tạo SKU
    SET NEW.SKU = MD5(CONCAT(NEW.NAME, '-', NEW.model, '-', NEW.switch, '-', NEW.keycap, '-', NEW.source));
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
