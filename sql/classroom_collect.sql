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

 Date: 04/09/2023 22:44:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for classroom_collect
-- ----------------------------
DROP TABLE IF EXISTS `classroom_collect`;
CREATE TABLE `classroom_collect`  (
  `classroom` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `collect` smallint(5) UNSIGNED NOT NULL DEFAULT 0,
  UNIQUE INDEX `classroom`(`classroom`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
