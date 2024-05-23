# IoTDataHub


## Gereksinimler

1. docker-compose
2. make (Komutları manuel olarak girmek istemezseniz)

## Çalıştırın
```
make up
```

Bu komut RabbitMQ, Clickhouse veritabanı ve uygulamamızın iki bileşeni iot_device_simulator ile iot_tcp_server yapılandırmalarını tamamlar docker ile çalıştırır.


## Kullanım

Herhangi bir tetikleme gerektirmez.
Cihaz simulatörü hemen dummy konum bilgilerini tcp sunucumuza göndermeye başlayacak.
Tcp sunucumuz mesajları yakalayacak ve mesajın geçerliliğini kontrol edecek.Ardından mesaj RabbitMQ kuyruğuna yazılacak.

#### Kuyruktaki mesajları direk olarak Clickhouse veritabanı consume etmektedir.

Veritabanında rabbitmq engine kullanan bir köprü tablo oluşturuldu.Tablomuz kuyruğa bağlanarak mesajları otomatik olarak çeker.Mesajı sütunlarına ayırarak doğru ve hızlı biçimde mergetree engine kullanan iot_locations tablosuna yazar.




[RabbitMQ Screenshot](https://drive.google.com/uc?export=view&id=1u01WPTGA2JIEMPpbSSsDKVgB2baZyreK)

[Clickhouse Screenshot](https://drive.google.com/file/d/1xeiYoU0b8wcSX6t_pPTmph3_Il71gtWe/view?usp=drive_link)
