CREATE DATABASE IF NOT EXISTS default;

USE default;

CREATE TABLE IF NOT EXISTS iot_locations (
    `device_uid` UInt32,
    `lat` Float64,
    `long` Float64,
    `created_at` Float64,
) Engine = MergeTree()
ORDER BY created_at;

CREATE TABLE IF NOT EXISTS clickhouse_rabbitmq_bridge
(
    `device_uid` UInt32,
    `lat` Float64,
    `long` Float64,
    `created_at` Float64,
) ENGINE = RabbitMQ SETTINGS
    rabbitmq_host_port = 'rabbitmq:5672',
    rabbitmq_exchange_name = 'iot_locations',
    rabbitmq_routing_key_list = 'iot_locations',
    rabbitmq_format = 'JSONEachRow',
    rabbitmq_exchange_type = 'direct',
    rabbitmq_num_consumers = 1,
    rabbitmq_routing_key_list = 'iot_locations'
    ;

CREATE MATERIALIZED VIEW IF NOT EXISTS iot_locations_view
TO iot_locations AS
SELECT
    device_uid as device_uid,
    lat AS lat,
    long AS long,
    created_at AS created_at
FROM clickhouse_rabbitmq_bridge;