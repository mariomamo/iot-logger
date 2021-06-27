
# <img src="https://image.flaticon.com/icons/png/512/1998/1998618.png" width="40" height="40" /> IoT - logger :robot:

IoT logger is an IoT architecture for gathering informations about IoT sensors. It is based on RabbitMQ queues and works with Nuclio.

### What is RabbitMQ
From the [RabbitMQ](https://www.rabbitmq.com/) home page:
> RabbitMQ is the most widely deployed open source message broker.

### What is Nuclio
From  the [Nuclio](https://nuclio.io/) home page:
> Nuclio is an open source and managed serverless platform used to minimize development and maintenance overhead and automate the deployment of data-science based applications

## <img src="https://image.flaticon.com/icons/png/512/4987/4987493.png" width="40" height="40"/> Architecture

The architecture is composed by some sensors that send informations about their status on a queue (```iot/web/sensors```). When a new message is incoming on this queue a nuclio function is triggered. This function send an HTTP request to a middleware written in <b>python</b> (```http://<service_url>:<service_port>/iot/logger/sendlog```).<br>
The middleware is in communication with a UI web based made in <b>React.js</b> by a <b>socket-io</b> connection.<br>
With this GUI we can read the status of all sensors connected and we can change their status. When we send a message from GUI to middleware this message will be send on another queue (```iot/sensor/{sensor_id}```).<br>
Each sensor is connected to their queue by own <b>sensor_id</b>.

<img src="readme\architecture.png"/>

## :rocket: Installation
The project is composed of 5 parts

* RabbitMQ
* Nuclio
* front-end (React.js)
* middleware (Python)
* IoT sensors (Python)

You can install this components one by one with ```dockerfile```, or you can use a ```docker-compose.yml``` file provided.
First of all clone the project and follow the instructions below

```git
git clone https://github.com/mariomamo/iot-project
```

## :gear: Some configuration before starting

Before starting you need to modify some configurations files.<br>
:one: Change IP address in front-end web app
Go to ```\iot-project\iot-front-end\compiled``` and edit ```index.html``` file. You can find a div with "root" id, you need to change the IP address in url property with yours.

```html
<div id="root" url="http://<INSERT_YOUR_IP_ADDRESS_HERE>" port="5000"></div>
```
If you want you can change also the port, but it is useless, you can map this port on another port of docker.

:two: Change the IP addresses in ```application.yaml``` inside python files
Go to ```iot-project\iot-logger``` and edit ```application.yml``` file.
You have to write your local IP address in ```topic_url``` property.

```yml
name: 'IoT-Logger'  
socket_io_port: 5000  
receive_topic_name: 'sensors/logs'  
send_topic_name: 'iot/sensors'  
topic_url: '192.168.1.59'  
rest_port: 4444
```

:warning: If you  want to change the port remember to change ```socket_io_port``` also :warning:<br>
:warning: ```rest_port``` is the port used for REST API. :warning:<br>
:warning: If you want to change this port remember to change the port inside nuclio script also :warning:

Go to ```iot-project\iot-logger``` and edit ```application.yml``` file.

```yml
sensors:  
  - chat_id: "1"  
    name: 'Car'  
    sensor_type: "car"  
    image: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Circle-icons-car.svg/1200px-Circle-icons-car.svg.png'  
    receive_topic_name: 'iot/sensors'  
    send_topic_name: 'iot/web/sensors'  
    topic_url: '192.168.1.59'  
  - chat_id: "2"  
    name: 'My house'  
    sensor_type: "home"  
    image: 'https://media.istockphoto.com/vectors/smart-home-vector-icon-with-airwaves-isolated-on-white-background-vector-id1186712143?k=6&m=1186712143&s=170667a&w=0&h=zZoIDzrMKXkUERFYeuSnYhiuSxZ22IcXT0RPIanZxG0='  
    receive_topic_name: 'iot/sensors'  
    send_topic_name: 'iot/web/sensors'  
    topic_url: '192.168.1.59'  
  - chat_id: "3"  
    name: 'Bed room air conditioner'  
    sensor_type: "air-conditioner"  
    image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfe3ft1wqiQUu1Kra38EezbmQTljHkFPSPzA&usqp=CAU'  
    receive_topic_name: 'iot/sensors'  
    send_topic_name: 'iot/web/sensors'  
    topic_url: '192.168.1.59'
```

You can simply add a new sensor adding a new element in the sensors array. You just have to add the required informations.
Actually there are only three types of sensors supported

* car
* home
* air-conditioner

Other sensor types will be ignored.
Also in this case you need to change the current IP in ```topic_url``` with yours. Each sensor can have different ```topic_url```.

:warning: You can of coure change all the topics, but remember to keep these topics name coherents :warning:

## :whale: docker-compose

you just have to type these commands

```docker-compose
docker-compose up --build -d
```

* <b>build</b>: rebuild images if they are already builded before
* <b>d</b>: execute in background. When the docker-compose will setted up you will not see the docker logs console

 <img src="readme\docker-compose.png" />

After this operation some containers (iot-logger and iot-logger) can fail. This is because rabbitMQ container is not ready. You can simply avoid this by restarting failing containers.

 <img src="readme\container_fail.png" />

## :whale2: dockerfile
### :one: RabbitMQ
In some cases you need to deploy only some parts of this projects for load balancing or availability purpose. So you can also use dockerfile instead of docker-compose.

Open your terminal and copy/paste this line

```shell
docker run -p 9000:15672 -p 1883:1883 -p 5672:5672 cyrilix/rabbitmq-mqtt
```

:heavy_check_mark: It is also available for ARM processors
```bash
docker run -p 9000:15672 -p 1883:1883 -p 5672:5672 arm32v7/rabbitmq
```

### :two: Nuclio
Open your terminal and copy/paste this line

```bash
docker run -p 8070:8070 -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp nuclio/dashboard:stable-amd64
```

:x: It is not available for ARM processors

### :three: IoT logger

Go to ```iot-logger``` folder
:warning: Check the directory where you are. You should be in ```iot-project``` folder :warning:

```bash
cd iot-logger
```

Build the image

```bash
docker build -t iot-logger .
```
Run container

```bash
docker run -v <path_where_you_cloned_project>\iot-project\iot-logger:/logger -dp 5000:5000 -dp 4444:4444 --name iot-logger -it iot-logger
```

### :four: IoT sensors
Go to ```iot-logger``` folder
:warning: Check the directory where you are. You should be in ```iot-project``` folder :warning:

```bash
cd iot-logger
```
Build the image

```docker
docker build -t iot-logger .
```
Run container

```docker
docker run -v <path_where_you_cloned_project>\iot-project\iot-logger:/sensors -d --name iot-logger -it iot-logger
```

### :five: IoT frontend
Go to ```iot-front-end``` folder
:warning: Check the directory where you are. You should be in ```iot-project``` folder :warning:

```bash
cd iot-front-end
```
In questo caso non abbiamo bisogno di un dockerfile
Run docker
```bash
docker run -v <path_where_you_cloned_project>\iot-project\iot-front-end\compiled:/usr/local/apache2/htdocs/ -dp 80:80 --name iot-frontend httpd:2.4
```

## :gear: Nuclio configuration
Once you have installed the project you need to configure it.
Go to ```iot-project/nuclio-function/loggerconsumer.yaml``` and write your local ip address at line <b>17</b>

```yml
triggers:
    MyMQTTTriggher:
      class: ""
      kind: rabbit-mq
      url: "amqp://guest:guest@<INSERT_YOUR_LOCA_IP_ADDRESS_HERE>:5672"
      attributes:
        exchangeName: """"
        queueName: iot/web/sensors
        topics:
          - '""'
```

Open [Nuclio control panel](http://localhost:8070/), create a new project and import the function you have just modified.
In the next window you should change the existing IP addres at line <b>25</b> with yours.

```python
response = requests.get("http://<INSERT_YOUR_LOCA_IP_ADDRESS_HERE>:4444/iot/logger/sendlog", headers=headers, json=payload)
```

Now you can deploy your function. When your function has been deployed go to [IoT logger webapp](http://localhost/) and restart ```iot-logger``` container. When ```iot-logger``` will be restarted it will send some information to the ```iot-logger``` and you will se these informations on the webapp. Now you can send commands to devices and you can read their responses.
Enjoy :)