# Installation

## Install Nuclio
```bash
docker run -p 8070:8070 -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp --name nuclio nuclio/dashboard:stable-amd64
```

Install RabbitMQ
## x86_64 processors
```bash
docker run -p 9000:15672  -p 1883:1883 -p 5672:5672 --name rabbitMQ cyrilix/rabbitmq-mqtt
```

# Installation on ARM processors

Uou can install RabbitMQ on ARM processors like raspberry
## Install RabbitMQ
Start rabbitMQ
```bash
docker run -p 9000:15672 -p 1883:1883 -p 5672:5672 -d --name rabbitMQ arm32v7/rabbitmq:3.6-management
```