{{
    config (
        materialized = 'view'
    )
}}

SELECT transaction_nsid, MAX ( transaction_line_last_modified_date ) AS transaction_last_modified_date
FROM 
( 
    SELECT transaction_nsid, transaction_line_last_modified_date FROM [netsuite].[stg].[transactionline]
    UNION ALL
    SELECT transaction_nsid, transaction_last_modified_date      FROM [netsuite].[stg].[transaction]
) all_updates
GROUP BY transaction_nsid