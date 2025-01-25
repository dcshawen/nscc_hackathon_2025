CREATE TABLE Users (
	id INT IDENTITY (1,1),
	username NVARCHAR (50) UNIQUE NOT NULL,
	password_hash NVARCHAR (255) NOT NULL,
	CONSTRAINT PK_Users PRIMARY KEY (id)
);

Select * from Users;