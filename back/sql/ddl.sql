CREATE SCHEMA `bolero`;

DROP TABLE if exists `composer_openopus`;
CREATE TABLE `composer_openopus`
(
    `composer_id`   int(10) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `name`          varchar(191) COLLATE utf8mb4_unicode_ci                 DEFAULT NULL,
    `complete_name` varchar(191) COLLATE utf8mb4_unicode_ci                 DEFAULT NULL,
    `portrait`      varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
    `birth`         date                                    NOT NULL,
    `death`         date                                                    DEFAULT NULL,
    `epoch`         varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
    `country`       varchar(191) COLLATE utf8mb4_unicode_ci                 DEFAULT NULL,
    `recommended`   tinyint(1) UNSIGNED                                     DEFAULT '0',
    `popular`       tinyint(1) UNSIGNED                     NOT NULL        DEFAULT '0'
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

DROP TABLE if exists `work_openopus`;
CREATE TABLE `work_openopus`
(
    `work_id`     int(10) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `composer_id` int(10) UNSIGNED                        NOT NULL,
    `title`       varchar(191) COLLATE utf8mb4_unicode_ci          DEFAULT NULL,
    `subtitle`    varchar(512) COLLATE utf8mb4_unicode_ci          DEFAULT NULL,
    `searchterms` varchar(1024) COLLATE utf8mb4_unicode_ci         DEFAULT NULL,
    `genre`       varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
    `year`        date                                             DEFAULT NULL,
    `recommended` tinyint(1) UNSIGNED                     NOT NULL DEFAULT '0',
    `popular`     tinyint(1) UNSIGNED                     NOT NULL DEFAULT '0'
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

DROP TABLE if exists `composer`;
CREATE TABLE `composer`
(
    `composer_id`   int(10) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `name`          varchar(191) COLLATE utf8mb4_unicode_ci                 DEFAULT NULL,
    `complete_name` varchar(191) COLLATE utf8mb4_unicode_ci                 DEFAULT NULL,
    `portrait`      varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
    `birth`         date                                    NOT NULL,
    `death`         date                                                    DEFAULT NULL,
    `epoch`         varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
    `nationality`   varchar(191) COLLATE utf8mb4_unicode_ci                 DEFAULT NULL,
    `recommended`   tinyint(1) UNSIGNED                                     DEFAULT '0',
    `popular`       tinyint(1) UNSIGNED                     NOT NULL        DEFAULT '0'
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;

DROP TABLE if exists `work`;
CREATE TABLE `work`
(
    `work_id`     int(10) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    `composer_id` int(10) UNSIGNED NOT NULL,
    `title`       varchar(191) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `subtitle`    varchar(512) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `searchterms` varchar(1024) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `genre`       varchar(191) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `recommended` tinyint(1) UNSIGNED                      DEFAULT '0',
    `popular`     tinyint(1) UNSIGNED                      DEFAULT '0',
    `number`      int(10) UNSIGNED                         DEFAULT NULL,
    `tonality`    varchar(191) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `opus`        int(10) UNSIGNED                         DEFAULT NULL,
    `opus_no`     int(10) UNSIGNED                         DEFAULT NULL,
    `catalog_abr` varchar(191) COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
    `catalog_no`  int(10) UNSIGNED                         DEFAULT NULL,
    `nickname`    varchar(191) COLLATE utf8mb4_unicode_ci  DEFAULT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
