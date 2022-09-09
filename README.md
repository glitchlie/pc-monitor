# pc-monitor
Simple client-server application for transmitting PC hardware data.
Currently in development.

Web application is hosted on Flask. Client and server connect through sockets. Redis is used for caching and transmitted data is passed to RabbitMQ.
