def daily_query(today):
    query = f"""
    CREATE OR REPLACE VIEW persist_view AS 
    SELECT 
        o.number as order_number,
        ss.number as build_number,
        sa.firstname, 
        sa.lastname,
        sa.company,
        sa.address1,
        sa.address2,
        sa.city,
        sa.zipcode,
        sst.name AS state_name,
        o.email,
        ss.original_shipping_method_code,
        o.completed_at,
        sb.state AS scheduled,
        sb.delivery_date,
        sb.delivery_date_earliest,
        sb.pdf_url,
    (SELECT g.name 
    FROM spree_products g 
        JOIN spree_variants g_variants ON g.id = g_variants.product_id 
        WHERE g_variants.id = sb.gift_id 
        ORDER BY g.updated_at DESC 
        LIMIT 1) AS gift_name, 
    (SELECT g_variants.sku 
    FROM spree_products g 
        JOIN spree_variants g_variants ON g.id = g_variants.product_id 
        WHERE g_variants.id = sb.gift_id 
        ORDER BY g.updated_at DESC 
        LIMIT 1) AS gift_sku, 
        (SELECT a.name 
    FROM spree_products a 
        JOIN spree_variants a_variants ON a.id = a_variants.product_id 
        WHERE a_variants.id = sb.addon_id 
        ORDER BY a.updated_at DESC 
        LIMIT 1) AS addon_name, 
    (SELECT a_variants.sku 
    FROM spree_products a 
        JOIN spree_variants a_variants ON a.id = a_variants.product_id
        WHERE a_variants.id = sb.addon_id 
        ORDER BY a.updated_at DESC 
        LIMIT 1) AS addon_sku
    FROM  spree_orders o
    JOIN spree_builds sb ON o.id = sb.order_id
    JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
    JOIN spree_addresses sa ON ss.address_id = sa.id 
    JOIN spree_states sst ON sa.state_id = sst.id 
    WHERE 
        (o.completed_at >= '12-1-2023'::date
        AND o.completed_at < '{today}'::date
        AND sb.delivery_date_earliest is NULL
        AND ss.state = 'ready'
        AND sb.state='ready')
    OR
        (o.completed_at >= '08-23-2023'::date
        AND o.completed_at < '{today}'::date
        AND sb.delivery_date_earliest >= '2023-07-03'::date
        AND sb.delivery_date_earliest <= '{today}'
        AND ss.state = 'ready' 
        AND sb.state='ready')
    ORDER BY o.completed_at ASC;
    """
    return query

def target_order(order_number):
    query = f"""
    CREATE OR REPLACE VIEW persist_view AS 
    SELECT 
        o.number as order_number,
        ss.number as build_number,
        sa.firstname, 
        sa.lastname,
        sa.company,
        sa.address1,
        sa.address2,
        sa.city,
        sa.zipcode,
        sst.name AS state_name,
        o.email,
        ss.original_shipping_method_code,
        o.completed_at,
        sb.state AS scheduled,
        sb.delivery_date,
        sb.delivery_date_earliest,
        sb.pdf_url,
    (SELECT g.name 
    FROM spree_products g 
        JOIN spree_variants g_variants ON g.id = g_variants.product_id 
        WHERE g_variants.id = sb.gift_id 
        ORDER BY g.updated_at DESC 
        LIMIT 1) AS gift_name, 
    (SELECT g_variants.sku 
    FROM spree_products g 
        JOIN spree_variants g_variants ON g.id = g_variants.product_id 
        WHERE g_variants.id = sb.gift_id 
        ORDER BY g.updated_at DESC 
        LIMIT 1) AS gift_sku, 
        (SELECT a.name 
    FROM spree_products a 
        JOIN spree_variants a_variants ON a.id = a_variants.product_id 
        WHERE a_variants.id = sb.addon_id 
        ORDER BY a.updated_at DESC 
        LIMIT 1) AS addon_name, 
    (SELECT a_variants.sku 
    FROM spree_products a 
        JOIN spree_variants a_variants ON a.id = a_variants.product_id
        WHERE a_variants.id = sb.addon_id 
        ORDER BY a.updated_at DESC 
        LIMIT 1) AS addon_sku
    FROM  spree_orders o
    JOIN spree_builds sb ON o.id = sb.order_id
    JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
    JOIN spree_addresses sa ON ss.address_id = sa.id 
    JOIN spree_states sst ON sa.state_id = sst.id 
    WHERE o.number = '{order_number}'
        -- AND (sb.state = 'scheduled_v2' OR sb.state='ready')
        -- AND NOT sb.state = 'shipped'
        -- AND ss.state = 'ready'
    ORDER BY o.completed_at ASC;
    """
    return query

def target_build(build_number):
    query = f"""
    CREATE OR REPLACE VIEW persist_view AS 
    SELECT 
        o.number as order_number, 
        ss.number as build_number,
        sa.firstname, 
        sa.lastname,
        sa.company,
        sa.address1,
        sa.address2,
        sa.city,
        sa.zipcode,
        sst.name AS state_name,
        o.email,
        ss.original_shipping_method_code,
        o.completed_at,
        sb.state AS scheduled,
        sb.delivery_date,
        sb.delivery_date_earliest,
        sb.pdf_url,
    (SELECT g.name 
    FROM spree_products g 
        JOIN spree_variants g_variants ON g.id = g_variants.product_id 
        WHERE g_variants.id = sb.gift_id 
        ORDER BY g.updated_at DESC 
        LIMIT 1) AS gift_name, 
    (SELECT g_variants.sku 
    FROM spree_products g 
        JOIN spree_variants g_variants ON g.id = g_variants.product_id 
        WHERE g_variants.id = sb.gift_id 
        ORDER BY g.updated_at DESC 
        LIMIT 1) AS gift_sku, 
        (SELECT a.name 
    FROM spree_products a 
        JOIN spree_variants a_variants ON a.id = a_variants.product_id 
        WHERE a_variants.id = sb.addon_id 
        ORDER BY a.updated_at DESC 
        LIMIT 1) AS addon_name, 
    (SELECT a_variants.sku 
    FROM spree_products a 
        JOIN spree_variants a_variants ON a.id = a_variants.product_id
        WHERE a_variants.id = sb.addon_id 
        ORDER BY a.updated_at DESC 
        LIMIT 1) AS addon_sku
    FROM spree_orders o
    JOIN spree_builds sb ON o.id = sb.order_id
    JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
    JOIN spree_addresses sa ON ss.address_id = sa.id 
    JOIN spree_states sst ON sa.state_id = sst.id 
    WHERE ss.number = '{build_number}'
        -- AND (sb.state = 'scheduled_v2' OR sb.state='ready')
        -- AND NOT sb.state = 'shipped'
        -- AND ss.state = 'ready'
    ORDER BY o.completed_at ASC;
    """
    return query

def select_daily(today):
    query = f"""
    SELECT 
        o.number as order_number,
        ss.number as build_number,
        ss.state,
        o.completed_at,
        sb.state AS build_state
    FROM spree_orders o
        JOIN spree_builds sb ON o.id = sb.order_id
        JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
        JOIN spree_addresses sa ON ss.address_id = sa.id 
        JOIN spree_states sst ON sa.state_id = sst.id 
    WHERE o.completed_at >= '12-1-2023'::date
        AND o.completed_at < '{today}'::date
        AND sb.delivery_date_earliest is NULL
        AND ss.state = 'ready' 
        AND sb.state = 'ready';
    """
    return query
    

def update_daily(today):
    query = f"""
    UPDATE spree_shipments
    SET state = 'shipped'
    FROM spree_orders o
        JOIN spree_builds sb ON o.id = sb.order_id
        JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
        JOIN spree_addresses sa ON ss.address_id = sa.id 
    WHERE ss.id = spree_shipments.id
        AND o.completed_at >= '12-1-2023'::date
        AND o.completed_at < '{today}'::date
        AND sb.delivery_date_earliest is NULL
        AND ss.state = 'ready'
        AND sb.state = 'ready';
    """
    return query


def select_scheduled(today):
    query = f"""
    SELECT 
        o.number as order_number,
        ss.number as build_number,
        ss.state,
        o.completed_at,
        sb.delivery_date_earliest as earliest_delivery,
        sb.delivery_date as delivery_date,
        sb.state AS build_state
    FROM spree_orders o
        JOIN spree_builds sb ON o.id = sb.order_id
        JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
        JOIN spree_addresses sa ON ss.address_id = sa.id 
        JOIN spree_states sst ON sa.state_id = sst.id 
    WHERE o.completed_at >= '07-03-2023'::date
        AND sb.delivery_date_earliest >= '07-03-2023'::date
        AND sb.delivery_date_earliest <= '{today}'::date
        AND sb.state = 'ready' 
        AND ss.state = 'ready' 
    ORDER BY sb.delivery_date_earliest ASC;
    """
    return query


def update_scheduled(today):
    query = f"""
    UPDATE spree_shipments
    SET state = 'shipped'
    FROM spree_orders o
        JOIN spree_builds sb ON o.id = sb.order_id
        JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
        JOIN spree_addresses sa ON ss.address_id = sa.id 
        JOIN spree_states sst ON sa.state_id = sst.id
    WHERE ss.id = spree_shipments.id
        AND o.completed_at >= '07-03-2023'::date
        AND sb.delivery_date_earliest >= '07-03-2023'::date
        AND sb.delivery_date_earliest <= '{today}'::date
        AND sb.state = 'ready' 
        AND ss.state = 'ready'
    """
    return query


def select_target_order(order_number):
    query = f"""
    SELECT 
        o.number as order_number,
        ss.number as build_number,
        ss.state as shipment_state,
        sb.state AS build_state,  
        o.completed_at
    FROM spree_orders o
        JOIN spree_builds sb ON o.id = sb.order_id
        JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
    WHERE o.number = '{order_number}'
    """
    return query

def update_target_order(order_number):
    query = f"""
    UPDATE spree_shipments
    SET state = 'shipped'
    FROM spree_orders o
        JOIN spree_builds sb ON o.id = sb.order_id
        JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
    WHERE ss.id = spree_shipments.id
        AND o.number = '{order_number}'
    """
    return query

def select_target_build(build_number):
    query = f"""
    SELECT 
        o.number as order_number,
        ss.number as build_number,
        ss.state as shipment_state,
        sb.state AS build_state,  
        o.completed_at
    FROM spree_orders o
        JOIN spree_builds sb ON o.id = sb.order_id
        JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
    WHERE ss.number = '{build_number}'
    """
    return query

def update_target_build(build_number):
    query = f"""
    UPDATE spree_shipments
    SET state = 'shipped'
    FROM spree_orders o
        JOIN spree_builds sb ON o.id = sb.order_id
        JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
    WHERE ss.id = spree_shipments.id
        AND ss.number = '{build_number}'
    """
    return query