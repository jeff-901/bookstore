use bookstore;

DROP TABLE IF EXISTS `discount`;
DROP TABLE IF EXISTS `review`;
DROP TABLE IF EXISTS `cart_item`;
DROP TABLE IF EXISTS `order_item`;
DROP TABLE IF EXISTS `order`;
DROP TABLE IF EXISTS `book`;
DROP TABLE IF EXISTS `user`;

CREATE TABLE `user`(
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `role` INT NOT NULL,
    `first_name` VARCHAR(128) NOT NULL,
	`last_name` VARCHAR(128) NOT NULL,
    `email` VARCHAR(256) NOT NULL,
    `phone` VARCHAR(64) NOT NULL,
    `gender` VARCHAR(32) NOT NULL,
    `password` VARCHAR(256) NOT NULL,
    `address` VARCHAR(256),
	CONSTRAINT `user_pk` PRIMARY KEY (`user_id`),
    UNIQUE (`email`, `phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `order` (
    `order_id` INT NOT NULL AUTO_INCREMENT, 
    `user_id` INT NOT NULL,
    `total_price` INT NOT NULL,
    `time` DATETIME(3) NOT NULL,
	PRIMARY KEY (`order_id`),
    FOREIGN KEY(`user_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `book` (
    `book_id` INT NOT NULL,
    `ISBN` VARCHAR(32) NOT NULL, 
    `name` VARCHAR(256) NOT NULL,
    `author` VARCHAR(64) NOT NULL,
    `author_original` VARCHAR(64),
    `translator` VARCHAR(64),
    `publishing_house` VARCHAR(64),
    `publishing_date` DATETIME(3),
    `price` INT NOT NULL,
	PRIMARY KEY (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `order_item` (
    `order_id` INT NOT NULL, 
    `book_id` INT NOT NULL,
    `number` INT NOT NULL,
    `price` INT NOT NULL,
    CONSTRAINT `order_item_pk` PRIMARY KEY (`order_id`, `book_id`),
    FOREIGN KEY(`order_id`) REFERENCES `order` (`order_id`) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(`book_id`) REFERENCES `book` (`book_id`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `cart_item` (
    `user_id` INT NOT NULL, 
    `book_id` INT NOT NULL,
    `number` INT NOT NULL,
    CONSTRAINT `cart_pk` PRIMARY KEY (`user_id`, `book_id`),
    FOREIGN KEY(`user_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(`book_id`) REFERENCES `book` (`book_id`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `discount` (
    `book_id` INT NOT NULL,
    `discount_price` INT NOT NULL, 
    `expire_date` DATETIME(3),
    PRIMARY KEY (`book_id`),
    FOREIGN KEY(`book_id`) REFERENCES `book` (`book_id`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `review` (
    `review_id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `book_id` INT NOT NULL,
    `comment` VARCHAR(2048) NOT NULL,
    `create_time` DATETIME(3) NOT NULL,
    `last_modified` DATETIME(3) NOT NULL,
    PRIMARY KEY (`review_id`),
    FOREIGN KEY(`user_id`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(`book_id`) REFERENCES `book` (`book_id`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;