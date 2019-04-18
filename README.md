# Scrapbook
Final project for COMP 353 Databases course. This is the base for a website and database to manage family events, communication, and memories.




SQL FOR DATABASES
First, create 'Scrapbook' database, then run these within that database.

CREATE TABLE `Scrapbook`.`Posts` ( `postID` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                                  `title` VARCHAR(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL , 
                                  `date_posted` DATETIME NOT NULL , 
                                  `content` TEXT CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL , 
                                  `owner_id` INT(11) NOT NULL));
CREATE TABLE `Scrapbook`.`User` ( `userID` INT(11) NOT NULL AUTO_INCREMENT,
                                 `username` VARCHAR(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ,
                                 `email` VARCHAR(120) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL , 
                                 `image_file` VARCHAR(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ,
                                 `password` VARCHAR(60) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ,
                                 PRIMARY KEY (`userID`));
                                 
CREATE TABLE `Scrapbook`.`Contact Information` ( `ContactID` INT NOT NULL , `UserID` INT NOT NULL , `City` TEXT NULL ,
                                               `Address` TEXT NOT NULL , `Primary_Phone` INT NOT NULL , `Secondary_Phone` INT                                                 NULL DEFAULT NULL , `Contact_Email` INT NOT NULL , PRIMARY KEY (`ContactID`))                                                 ENGINE = InnoDB;
                                  


Link to Web Design Moqup: https://app.moqups.com/TrCU9LFVj5/view
Link to ER Diagram: https://www.lucidchart.com/invitations/accept/58507afc-eedb-4688-a786-958c22bf9cf7
