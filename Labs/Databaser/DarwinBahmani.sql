use everyloop 

SELECT 
    [Spacecraft], 
    [Launch date], 
    [Carrier rocket], 
    [Operator], 
    [Mission type]
INTO SuccessfulMissions
FROM MoonMissions
WHERE [Outcome] = 'Successful';
GO

UPDATE SuccessfulMissions
SET [Operator] = LTRIM(RTRIM([Operator]));
GO 

UPDATE SuccessfulMissions
SET [Spacecraft] = LEFT([Spacecraft], CHARINDEX('(', [Spacecraft]) - 1)
WHERE [Spacecraft] LIKE '%(%';
GO

SELECT [Operator],[Mission type], COUNT(*) AS [Mission count]
FROM SuccessfulMissions
GROUP BY [Operator], [Mission type]
HAVING COUNT(*) > 1 
ORDER BY [Operator], [Mission type]
GO

SELECT 
    [FirstName] + ' ' + [LastName] AS [Name],
    *,
    CASE 
        WHEN CAST(SUBSTRING([ID], LEN([ID]) - 1, 1) AS INT) % 2 = 0 THEN 'Female'
        ELSE 'Male'
    END AS [Gender]
INTO NewUsers
FROM Users;
GO

SELECT 
    UserName, 
    COUNT(*) AS Occurrences
FROM NewUsers
GROUP BY UserName
HAVING COUNT(*) > 1;
GO

#chatgpt
ALTER TABLE NewUsers
ALTER COLUMN UserName VARCHAR(100);
#
GO


WITH RankedDuplicates AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY UserName ORDER BY ID) AS rn
    FROM NewUsers
)

UPDATE RankedDuplicates
SET UserName = 
    CASE 
        WHEN rn = 1 THEN UserName
        ELSE UserName + '_' + CAST(rn - 1 AS VARCHAR)
    END;
GO



DELETE FROM NewUsers
WHERE 
    Gender = 'Female' 
    AND CAST(LEFT(ID, 2) AS INT) < 70;
GO
 


SELECT 
    products.Id AS Id,
    products.ProductName AS Product,
    suppliers.CompanyName AS Supplier,
    categories.CategoryName AS Category
FROM company.products AS products
JOIN company.suppliers AS suppliers ON products.SupplierId = suppliers.Id
JOIN company.categories AS categories ON products.CategoryId = categories.Id;
GO

SELECT 
    regions.RegionDescription AS Region,
    COUNT(DISTINCT employees.Id) AS [Number of Employees]
FROM company.employees
JOIN company.employee_territory ON employees.Id = employee_territory.EmployeeId
JOIN company.territories ON employee_territory.TerritoryId = territories.Id
JOIN company.regions ON territories.RegionId = regions.Id
GROUP BY regions.RegionDescription;
GO




