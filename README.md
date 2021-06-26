
# ![](https://image.flaticon.com/icons/png/512/1998/1998618.png =40x40) IoT - logger

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
