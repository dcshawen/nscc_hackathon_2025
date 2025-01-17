/*DROP DATABASE EMPTIMESHEET

ALTER DATABASE EMPTIMESHEET SET SINGLE_USER WITH ROLLBACK IMMEDIATE; 
GO*/


CREATE DATABASE EMPTIMESHEET;

GO

USE EMPTIMESHEET;

GO

--DROP TABLE EMP_DETAIL;

-- EMP_USER Table
CREATE TABLE EMP_USER (
    Emp_W_Id NVARCHAR(25) NOT NULL,
	Emp_Pswd_hash NVARCHAR (255) NOT NULL,
	Emp_Portal INT NOT NULL DEFAULT 1,
	PRIMARY KEY (Emp_W_Id),				 
);
					
-- EMP_DETAIL Table
CREATE TABLE EMP_DETAIL (
    TyS_Id INT IDENTITY(1,1),             
    Emp_W_Id_FK NVARCHAR(25) NOT NULL,
	Emp_Name NVARCHAR (50) NOT NULL,
    Emp_Program NVARCHAR(25),             
    Emp_Dept NVARCHAR(25),                
    Emp_Fund NVARCHAR(25),                
    Emp_Acct NVARCHAR(25),                
    Emp_Proj NVARCHAR(25),                
    PRIMARY KEY (TyS_Id),			      
);

ALTER TABLE EMP_DETAIL 
ADD CONSTRAINT Emp_W_Id_FK_EMP_DETAIL FOREIGN KEY (Emp_W_ID_FK) REFERENCES EMP_USER(Emp_W_ID);


INSERT INTO EMP_USER (Emp_W_Id, Emp_Pswd_hash, Emp_Portal) 
VALUES 
    ('W000001', '!@#%$!#^$%&%*^*^#^@', 1);

-- Insert data into EMP_DETAIL table
INSERT INTO EMP_DETAIL (Emp_W_Id_FK, Emp_Name, Emp_Program, Emp_Dept, Emp_Fund, Emp_Acct, Emp_Proj)
VALUES 
    ('W000001', 'Alice Johnson', 'ProgramA', 'DeptA', 'FundA', 'AcctA', 'ProjA'),
    ('W000002', 'Bob Smith', 'ProgramB', 'DeptB', 'FundB', 'AcctB', 'ProjB'),
    ('W000002', 'Charlie Davis', 'ProgramB', 'DeptC', 'FundC', 'AcctC', 'ProjC'),
    ('W000004', 'Diana Garcia', 'ProgramD', 'DeptD', 'FundD', 'AcctD', 'ProjD'),
    ('W000005', 'Evan Martinez', 'ProgramE', 'DeptE', 'FundE', 'AcctE', 'ProjE');


SELECT * FROM EMP_USER;
SELECT * FROM EMP_DETAIL;

