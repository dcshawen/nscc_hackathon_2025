--DROP DATABASE TimeSheet;

CREATE DATABASE TimeSheet;

GO

USE TimeSheet;

GO

CREATE TABLE EmployeeDetail (
    EmpName NVARCHAR (255),
    WNumber NVARCHAR (50),
    Fund INT,
    Dept NVARCHAR (50),
    Program NVARCHAR (50),
    Account INT,
    Project NVARCHAR (50),
    HourlyPay DECIMAL (10,2),
    PayStartDt DATE,
    PayEndDt DATE,
    WeekNo INT,
    SplDt DATE,
    HrWorked DECIMAL (5,2),
    OtherInfo TEXT,
    PRIMARY KEY (WNumber, HourlyPay)
);


INSERT INTO EmployeeDetail (EmpName, WNumber, Fund, Dept, Program, Account, Project, HourlyPay, PayStartDt, PayEndDt, WeekNo, SplDt, HrWorked, OtherInfo)
VALUES
('Emily Green', 'W0463702', 12476, 'Admissions', 'Bachelor of Arts (BA)', 12345, 'Alpha', 25.00, '2025-01-01', '2025-01-07', 1, '2025-01-05', 40, 'Info1'),
('James Carter', 'W0530918', 35921, 'Student Affairs', 'Bachelor of Science (BS)', 67890, 'Beta', 30.00, '2025-01-08', '2025-01-14', 2, '2025-01-12', 38, 'Info2'),
('Olivia Harris', 'W0655427', 84309, 'Career Services', 'Bachelor of Business Administration (BBA)', 11223, 'Gamma', 22.50, '2025-01-15', '2025-01-21', 3, '2025-01-19', 42, 'Info3'),
('Daniel Scott', 'W0783461', 47685, 'Financial Aid', 'Master of Education (M.Ed.)', 44556, 'Delta', 28.75, '2025-01-22', '2025-01-28', 4, '2025-01-26', 36, 'Info4'),
('Sophia Mitchell', 'W0362849', 52410, 'Alumni Relations', 'Doctor of Philosophy (Ph.D.)', 77889, 'Epsilon', 35.00, '2025-01-29', '2025-02-04', 5, '2025-02-02', 44, 'Info5'),
('Alexander Morgan', 'W0479765', 19834, 'Campus Security', 'Associate of Science (AS)', 99001, 'Zeta', 27.00, '2025-02-05', '2025-02-11', 6, '2025-02-09', 40, 'Info6'),
('Charlotte Turner', 'W0675214', 76593, 'Facilities Management', 'Master of Fine Arts (MFA)', 22334, 'Eta', 31.50, '2025-02-12', '2025-02-18', 7, '2025-02-16', 39, 'Info7');


SELECT * FROM EmployeeDetail;