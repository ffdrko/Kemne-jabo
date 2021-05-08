CREATE DATABASE IF NOT EXISTS kemne_jabo;

USE kemne_jabo;

DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS mediums;
DROP TABLE IF EXISTS taken_by;
DROP TABLE IF EXISTS information;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS location;

CREATE TABLE IF NOT EXISTS location
(
    location_id 	BIGINT PRIMARY KEY AUTO_INCREMENT,
    street 		VARCHAR(300) NOT NULL,
    house 		INT NOT NULL,
    thana 		VARCHAR(100) NOT NULL,
    district 		VARCHAR(100) NOT NULL,
    postal_code 	INT NOT NULL
);

CREATE TABLE IF NOT EXISTS users
(
    user_id 		BIGINT PRIMARY KEY AUTO_INCREMENT,
    email 		VARCHAR(300) NOT NULL UNIQUE,
    pass 		VARCHAR(100) NOT NULL, 
    first_name 		VARCHAR(300) NOT NULL,
    last_name 		VARCHAR(300) NOT NULL,
    phone 		BIGINT NOT NULL UNIQUE,
    question 		VARCHAR(500) NOT NULL,
    answer 		VARCHAR(500) NOT NULL,
    hint 		VARCHAR(500) NOT NULL,
    can_withdraw 	BOOLEAN DEFAULT 0,
    points 		BIGINT DEFAULT 0,
    money 		INT DEFAULT 0,
    location_id 	BIGINT NOT NULL,
			FOREIGN KEY address (location_id)
			REFERENCES location (location_id)
			ON DELETE CASCADE
			ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS information
(
    information_id 	BIGINT PRIMARY KEY AUTO_INCREMENT,
    start_pos 		VARCHAR(300) NOT NULL, 
    destination 	VARCHAR(300) NOT NULL,
    positive_review 	BIGINT DEFAULT 0,
    negative_review 	BIGINT DEFAULT 0,
    on_query 		BOOLEAN DEFAULT 1,
    user_id 		BIGINT NOT NULL,
			FOREIGN KEY fk_user (user_id)
			REFERENCES users (user_id)
			ON DELETE CASCADE
			ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS mediums
(
    medium_id 		BIGINT PRIMARY KEY AUTO_INCREMENT,
    transport		VARCHAR(200) NOT NULL,
    lower_range		INT NOT NULL,
    higher_range 	INT NOT NULL,
    information_id 	BIGINT NOT NULL,
			FOREIGN KEY fk_info (information_id)
			REFERENCES information (information_id)
			ON DELETE CASCADE
			ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS taken_by
(
    search_id 		BIGINT PRIMARY KEY AUTO_INCREMENT,
    is_useful 		BOOLEAN DEFAULT 0,
    information_id 	BIGINT NOT NULL,
			FOREIGN KEY fk_info (information_id)
			REFERENCES information (information_id)
			ON DELETE CASCADE
			ON UPDATE NO ACTION,
    user_id 		BIGINT NOT NULL,
			FOREIGN KEY fk_user (user_id)
			REFERENCES users (user_id)
			ON DELETE CASCADE
			ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS reports
(
    report_id 	BIGINT PRIMARY KEY AUTO_INCREMENT,
    message 	VARCHAR(2500) NOT NULL,
    feedback 	VARCHAR(2500) NOT NULL, 
    is_FAQ 	BOOLEAN DEFAULT 0,
    user_id 	BIGINT NOT NULL,
		FOREIGN KEY fk_user (user_id)
		REFERENCES users (user_id)
		ON DELETE CASCADE
		ON UPDATE NO ACTION
);