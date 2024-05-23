import asyncio
import aio_pika
import json
from pydantic import BaseModel, ValidationError
from config import RABBITMQ_URL, TCP_SERVER_PORT, TCP_SERVER_HOST, LOCATION_Q,EXCHANGE_NAME,ROUTING_KEY,log

"""
    Tcp soketi dinler, 
    Gelen mesajı MessageModel ile karşılaştırır
    Geçerli mesajı RabbitMq kuyruğuna iletir.
    Mesajın gönderimini simule etmek için random mesaj üreten iot_device_simulator çalıştırılabilir.
"""

class MessageModel(BaseModel):
    device_uid: int
    lat: float
    long: float
    created_at: float


async def handle_message(reader, writer):
    try:
        data = await reader.readuntil(b'\n')
        message = json.loads(data.decode())
        message = MessageModel(**message)

        addr = writer.get_extra_info('peername')
        log.info(f"Iot_tcp_server received message from {addr}")

        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange(
                EXCHANGE_NAME, aio_pika.ExchangeType.DIRECT,durable=True
            )
            queue = await channel.declare_queue(LOCATION_Q)
            await queue.bind(exchange, ROUTING_KEY)
            await exchange.publish(
                aio_pika.Message(body=json.dumps(message.dict()).encode(),
                                 expiration=3600000),
                routing_key=ROUTING_KEY

            )
        writer.close()

    except ValidationError as e:
        log.error(f"handle_message ->Invalid message format {str(e)}")

    except asyncio.exceptions.IncompleteReadError as e:
        log.error(f"handle_message -> Failed to retrieve expected size data {str(e)}")

    except json.JSONDecodeError as e:
        log.error(f"handle_message -> JSON conversion error {str(e)}")

    except Exception as e:
        log.error(f"handle_message -> {str(e)}")


async def main():
    try:
        server = await asyncio.start_server(
            handle_message,
            host=TCP_SERVER_HOST,
            port=TCP_SERVER_PORT
        )
        log.info(f"Tcp server is listening {TCP_SERVER_HOST}:{TCP_SERVER_PORT}")

        async with server:
            await server.serve_forever()
    except Exception as e:
        log.error(f"{str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
