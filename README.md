
# IoT - logger
![](https://image.flaticon.com/icons/png/512/1998/1998618.png =40x40)
![](https://image.flaticon.com/icons/png/512/1998/1998618.png=40x40)
![](https://image.flaticon.com/icons/png/512/1998/1998618.png)

IoT logger is an IoT architecture for gathering informations about IoT sensors. It is based on RabbitMQ queues and works with Nuclio.

### What is RabbitMQ
From the [RabbitMQ](https://www.rabbitmq.com/) home page:
> RabbitMQ is the most widely deployed open source message broker.

### What is Nuclio
From  the [Nuclio](https://nuclio.io/) home page:
> Nuclio is an open source and managed serverless platform used to minimize development and maintenance overhead and automate the deployment of data-science based applications

## ![](https://image.flaticon.com/icons/png/512/4987/4987493.png =40x40) Architecture

## :rocket: Installation
The project is composed of 5 parts

* front-end (React.js)
* middleware (Python)
* IoT sensors (Python)
* RabbitMQ
* Nuclio

You can install all this components inside docker using the ```docker-compose.yml``` file provided

# IoT logger

```docker
cd iot-logger
docker build -t iot-logger .
```

```docker
docker run -v C:\Users\Mario\Desktop\Mario\ServerlessComputing\iot-project\iot-logger:/logger -dp 5000:5000 -dp 4444:4444 --name iot-logger -it iot-logger
```

# IoT sensors
```docker
cd ..
cd iot-sensors
docker build -t iot-sensors .
```


```docker
docker run -v C:\Users\Mario\Desktop\Mario\ServerlessComputing\iot-project\iot-sensors:/sensors -d --name iot-sensors -it iot-sensors
```

# IoT frontend

```docker
cd ..
cd iot-front-end
docker run -v C:\Users\Mario\Desktop\Mario\ServerlessComputing\iot-project\iot-front-end\build:/usr/local/apache2/htdocs/ -dp 80:80 --name iot-frontend httpd:2.4
```

# Docker compose

```bash
docker-compose up --build -d
```
