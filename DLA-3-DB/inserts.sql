USE DriversLicenseSystem;

-- Sample data insertion
INSERT INTO Users (Name, Email, Phone, Address, DateOfBirth)
VALUES 
(N'John Doe', N'john.doe@example.com', N'1234567890', N'123 Elm Street, Cityville', '1990-05-15'),
(N'Jane Smith', N'jane.smith@example.com', N'0987654321', N'456 Oak Avenue, Townsville', '1985-09-25');

INSERT INTO Licenses (UserID, LicenseStage, IssuedDate, ExpiryDate, Status)
VALUES
(1, N'Learning', '2025-01-01', '2030-01-01', N'In Progress'),
(2, N'Registration', NULL, NULL, N'Pending');

INSERT INTO Exams (UserID, ExamDate, Score, Result)
VALUES
(1, '2025-02-01', 85, N'Passed'),
(2, '2025-03-01', NULL, N'Pending');

INSERT INTO Lessons (UserID, LessonDate, InstructorName, LessonNotes)
VALUES
(1, '2025-01-15', N'Instructor A', N'Basics of driving.'),
(1, '2025-01-22', N'Instructor B', N'Advanced turns and parking.');

INSERT INTO Progress (UserID, ModuleName, CompletionStatus, CompletionDate)
VALUES
(1, N'Traffic Rules', N'Completed', '2025-01-10'),
(2, N'Driving Basics', N'In Progress', NULL);