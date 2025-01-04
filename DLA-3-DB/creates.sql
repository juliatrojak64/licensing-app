--CREATE DATABASE DriversLicenseSystem;

-- Use the database
USE DriversLicenseSystem;


-- Users table
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    Phone NVARCHAR(15),
    Address NVARCHAR(MAX),
    DateOfBirth DATE,
    CreatedAt DATETIME DEFAULT GETDATE()
);

-- Licenses table
CREATE TABLE Licenses (
    LicenseID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL,
    LicenseStage NVARCHAR(50) CHECK (LicenseStage IN ('Registration', 'Verification', 'Learning', 'Exam', 'Licensed')),
    IssuedDate DATE,
    ExpiryDate DATE,
    Status NVARCHAR(50) CHECK (Status IN ('Pending', 'In Progress', 'Completed')),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Exams table
CREATE TABLE Exams (
    ExamID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL,
    ExamDate DATE NOT NULL,
    Score INT,
    Result NVARCHAR(50) CHECK (Result IN ('Passed', 'Failed', 'Pending')),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Lessons table
CREATE TABLE Lessons (
    LessonID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL,
    LessonDate DATE NOT NULL,
    InstructorName NVARCHAR(100),
    LessonNotes NVARCHAR(MAX),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Progress table
CREATE TABLE Progress (
    ProgressID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL,
    ModuleName NVARCHAR(100) NOT NULL,
    CompletionStatus NVARCHAR(50) CHECK (CompletionStatus IN ('Not Started', 'In Progress', 'Completed')),
    CompletionDate DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);