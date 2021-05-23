CREATE DATABASE IF NOT EXISTS kemne_jabo;

USE kemne_jabo;

DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS mediums;
DROP TABLE IF EXISTS taken_by;
DROP TABLE IF EXISTS information;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS admins;

CREATE TABLE IF NOT EXISTS users
(
	user_id 		BIGINT PRIMARY KEY AUTO_INCREMENT,
    email 			VARCHAR(300) NOT NULL UNIQUE,
    pass 			VARCHAR(100) NOT NULL, 
    first_name 		VARCHAR(300) NOT NULL,
    last_name 		VARCHAR(300) NOT NULL,
    phone 			VARCHAR(11) NOT NULL UNIQUE,
    question 		VARCHAR(500) NOT NULL,
    answer 			VARCHAR(500) NOT NULL,
    hint 			VARCHAR(500) NOT NULL,
    can_withdraw 	BOOLEAN DEFAULT 0,
    points 			BIGINT DEFAULT 0,
    money 			INT DEFAULT 0,
    street 			VARCHAR(300) NOT NULL,
    house 			VARCHAR(300) NOT NULL,
    thana 			VARCHAR(100) NOT NULL,
    district 		VARCHAR(100) NOT NULL,
    postal_code 	VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS information
(
	information_id 		BIGINT PRIMARY KEY AUTO_INCREMENT,
    start_pos 			VARCHAR(300) NOT NULL, 
    destination 		VARCHAR(300) NOT NULL,
    positive_review 	BIGINT DEFAULT 0,
    negative_review 	BIGINT DEFAULT 0,
    on_query 			BOOLEAN DEFAULT 1,
    user_id 			BIGINT NOT NULL,
						FOREIGN KEY fk_user (user_id)
						REFERENCES users (user_id)
						ON DELETE CASCADE
						ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS mediums
(
	medium_id 			BIGINT PRIMARY KEY AUTO_INCREMENT,
    transport			VARCHAR(200) NOT NULL,
    lower_range			INT NOT NULL,
    higher_range 		INT NOT NULL,
    information_id 		BIGINT NOT NULL,
						FOREIGN KEY fk_info (information_id)
						REFERENCES information (information_id)
						ON DELETE CASCADE
						ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS taken_by
(
	search_id 			BIGINT PRIMARY KEY AUTO_INCREMENT,
    is_useful 			BOOLEAN DEFAULT 0,
    information_id 		BIGINT NOT NULL,
						FOREIGN KEY fk_info (information_id)
						REFERENCES information (information_id)
						ON DELETE CASCADE
						ON UPDATE NO ACTION,
	user_id 			BIGINT NOT NULL,
						FOREIGN KEY fk_user (user_id)
						REFERENCES users (user_id)
						ON DELETE CASCADE
						ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS reports
(
	report_id 	BIGINT PRIMARY KEY AUTO_INCREMENT,
    message 	VARCHAR(2500) NOT NULL,
    feedback 	VARCHAR(2500), 
    is_FAQ 		BOOLEAN DEFAULT 0,
    is_ans 		BOOLEAN DEFAULT 0,
    user_id 	BIGINT NOT NULL,
				FOREIGN KEY fk_user (user_id)
				REFERENCES users (user_id)
				ON DELETE CASCADE
				ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS admins
(
	email VARCHAR(300) PRIMARY KEY NOT NULL UNIQUE,
    pass VARCHAR(100) NOT NULL
);

INSERT INTO users VALUES (NULL, 'example@gmail.com', 'pass_word', 'no_fname', 'no_lname', '01234567891', 'no_ques', 'no_ans', 'no_hint', 0, 0, 0, 'no_street', 'no_house', 'no_thana', 'no_district', '0000');
INSERT INTO admins VALUES ('justchillbro1234@gmail.com', 'admin1234');
INSERT INTO reports VALUES (NULL, 'How do I register?', 'Please go to sign up and fill out all the informations to register', 1, 1, 1);
INSERT INTO reports VALUES (NULL, 'How do I login?', 'Please go to login and put your email and password to login. If it says account does not exist, please go to sign up and fill out all the informations to register', 1, 1, 1);
INSERT INTO reports VALUES (NULL, 'What do I do if I forget my password?', 'Please go to login and then click on forgot my password. Then answer your security question and set a new password', 1, 1, 1); 