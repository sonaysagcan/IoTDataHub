.PHONY: up clickhouse-set-schemas iot_tcp_server iot_device_simulator down restart logs

up:
	docker-compose up -d rabbitmq clickhouse
	$(MAKE) wait-clickhouse
	$(MAKE) clickhouse-set-schemas
	$(MAKE) iot_tcp_server iot_device_simulator

wait-clickhouse:
	@echo "Waiting for Database to start..."
	@sleep 20

clickhouse-set-schemas:
	docker-compose exec clickhouse bash -c "cat /opt/init.sql | clickhouse-client -m -n"

iot_tcp_server:
	docker-compose up -d iot_tcp_server

iot_device_simulator:
	docker-compose up -d iot_device_simulator

down:
	docker-compose down

restart: down up

logs:
	docker-compose logs -f