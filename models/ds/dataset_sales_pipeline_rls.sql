{{
    config (
        materialized = 'view'
    )
}}

-- depends_on: {{ ref('prep_rls_normalize') }}
{{ model_generate_dataset_rls(ref("dataset_sales_pipeline"), "customer_bu_item") }}