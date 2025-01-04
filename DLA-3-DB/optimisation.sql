-- Use the database
USE DriversLicenseSystem;

-- 1. Add Indexes to Frequently Queried Columns
CREATE NONCLUSTERED INDEX idx_Users_Email ON Users (Email);
CREATE NONCLUSTERED INDEX idx_Licenses_UserID ON Licenses (UserID);
CREATE NONCLUSTERED INDEX idx_Exams_ExamDate ON Exams (ExamDate);

-- 2. Update Statistics
EXEC sp_updatestats;

-- 3. Rebuild or Reorganize Fragmented Indexes
-- Detect and handle indexes with high fragmentation (>30%)
DECLARE @TableName NVARCHAR(MAX), @IndexName NVARCHAR(MAX);

DECLARE IndexCursor CURSOR FOR
SELECT 
    OBJECT_NAME(object_id) AS TableName, 
    name AS IndexName
FROM sys.indexes
WHERE OBJECT_ID IN (
    SELECT object_id
    FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'DETAILED')
    WHERE avg_fragmentation_in_percent > 30
);

OPEN IndexCursor;

FETCH NEXT FROM IndexCursor INTO @TableName, @IndexName;

WHILE @@FETCH_STATUS = 0
BEGIN
    PRINT 'Rebuilding index ' + @IndexName + ' on table ' + @TableName;
    EXEC ('ALTER INDEX [' + @IndexName + '] ON [' + @TableName + '] REBUILD');
    FETCH NEXT FROM IndexCursor INTO @TableName, @IndexName;
END;

CLOSE IndexCursor;
DEALLOCATE IndexCursor;
