/*
 Navicat Premium Data Transfer

 Source Server         : 腾讯云服务器
 Source Server Type    : MySQL
 Source Server Version : 50742
 Source Host           : 82.156.157.47:3306
 Source Schema         : user

 Target Server Type    : MySQL
 Target Server Version : 50742
 File Encoding         : 65001

 Date: 04/09/2023 22:43:50
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `number` smallint(19) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '序号',
  `openid` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户唯一标识',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户昵称',
  `bool_schedule` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '课表导入情况',
  `star_classroom_1` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '常去教室1',
  `star_classroom_2` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '常去教室2',
  `star_classroom_3` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '常去教室3',
  `bool_classroom` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '常去教室设置情况',
  `service_date` date NULL DEFAULT NULL COMMENT '用户注册日期',
  `time_ocr` tinyint(1) UNSIGNED NOT NULL DEFAULT 3 COMMENT '剩余识别次数',
  PRIMARY KEY (`number`) USING BTREE,
  UNIQUE INDEX `oonly_opid`(`openid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 133 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
