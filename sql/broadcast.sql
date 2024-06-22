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

 Date: 23/06/2024 01:10:18
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for broadcast
-- ----------------------------
DROP TABLE IF EXISTS `broadcast`;
CREATE TABLE `broadcast`  (
  `message` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
