{{
    config (
        materialized = 'view'
    )
}}

SELECT 
    {{ dbt_utils.star(from=ref('transaction_with_line')) }}
    , {{ dbt_utils.star(from=ref('dim_item'), except = var("scd_excluded_col_name") ) }}
    , {{ dbt_utils.star(from=ref('dim_bu'), except = var("scd_excluded_col_name") ) }}

FROM {{ ref("fact_all_transactions_with_line") }} t

{# Scope of the dataset #}
WHERE t.transaction_type IN ( {{ var("sales_scope_type") | join(', ') }} )