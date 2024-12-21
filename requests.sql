select load_dev_plugin('cryptopricingplugin','devManifest.json');
DROP TABLE IF EXISTS TempCrypto;
DROP TABLE IF EXISTS Wallet;
CREATE TABLE TempCrypto AS
SELECT * FROM cryptopricingplugin_cryptoValueTable;
CREATE TABLE Wallet AS
WITH FilteredData AS (
    SELECT 
        Currency AS Devise, 
        SUM(Amount) AS TotalAmount 
    FROM notion_database
    WHERE Description NOT IN ('Crypto Earn Allocation', 'Crypto Earn Withdrawal', 'DPoS staking payment', 'Defi Purchase')
    GROUP BY Currency
    UNION ALL
    SELECT 
        toCurrency AS Devise, 
        SUM(toAmount) AS TotalAmount 
    FROM notion_database
    WHERE Description NOT IN ('Crypto Earn Allocation', 'Crypto Earn Withdrawal', 'DPoS staking payment', 'Defi Purchase')
    GROUP BY toCurrency
),
ConsolidatedData AS (
    SELECT 
        Devise, 
        SUM(TotalAmount) AS FinalAmount
    FROM FilteredData
    GROUP BY Devise
)
SELECT 
    ConsolidatedData.Devise AS Currency, 
    ConsolidatedData.FinalAmount AS Quantity,
    TempCrypto.Value AS UnitValue,
    (ConsolidatedData.FinalAmount * TempCrypto.Value) AS TotalValue
FROM ConsolidatedData
LEFT JOIN TempCrypto
ON TRIM(LOWER(ConsolidatedData.Devise)) = TRIM(LOWER(TempCrypto.Currency))
WHERE ConsolidatedData.FinalAmount > 0.000001;
.mode csv
.output Wallet.csv
SELECT * FROM Wallet;
.output stdout;