- Create an EC2 Instance
- 
- Create a Key pair and download it and save it in the project directory
	Key-pair = Kafka-stock-market-
	Instance name = Kafka-stock-market-

- To connect EC2 instance to local terminal
	- Navigate to key pair folder
	- chmod 400 key-pair-name   //if getting some error
	- ssh -i "kafka-stock-market.pem" ec2-user@ec2-13-60-55-149.eu-north-1.compute.amazonaws.com 	(get it from EC2/Instances/Instance ID/Connect/SSH Client)

- Download required Dependencies
	- Download Apache Kafka into our EC2 instance (kafka 3.8.0 Scala 2.12)
		- wget https://downloads.apache.org/kafka/3.8.0/kafka_2.12-3.8.0.tgz	
	- Extract the tar file
		- tar -xvf kafka_2.12-3.8.0.tgz
	- Apache Kafka works on JVM
		- sudo yum install -y java-1.8.0
		- java -version

- Start Zoo Keeper
	- Navigate to uncompressed kafka folder
	- cd kafka_2.12-3.8.0
	- bin/zookeeper-server-start.sh config/zookeeper.properties

- Alocate memory to kafkaesque server (only ones)
	- Now open a new terminal and navigate to the project directory and paste ssh key and get connected to the EC2 instance/machine
	- Allocate defined memory to kafka server
		- export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"

- Start Kafka server
	- Navigate to kafka and start kafka
		- cd kafka_2.12-3.8.0
		- bin/kafka-server-start.sh config/server.properties
	(By this point we have both zookeeper and kafka server running)

- We can observe that our kafka server is running at a private IP DNS, so we can't access private DNS unless we are in the same network 
	.'.([2024-09-26 05:33:08,767] INFO Registered broker 0 at path /brokers/ids/0 with addresses: PLAINTEXT://ip-172-31-44-223.eu-north-1.compute.internal:9092, czxid (broker epoch): 25 (kafka.zk.KafkaZkClient))
	- change Private IP DNS to Public IP DNS
		- press CTRL+C to both terminals to terminate
		- sudo nano config/server.properties (for changing ADVERTISED_LISTNERS to public IP of EC2 Instance)
			- change "your.host.name" in "advertised.listeners=PLAINTEXT://your.host.name:9092" to Public IPv4 in EC2 instance (13.60.55.149) -----> "advertised.listeners=PLAINTEXT://13.60.55.149:9092"
		- Now again start the zookeeper and kafka server
			- Now our kafka server is running in Public IP DNS
				.'.([2024-09-26 06:01:16,063] INFO Registered broker 0 at path /brokers/ids/0 with addresses: PLAINTEXT://13.60.55.149:9092, czxid (broker epoch): 46 (kafka.zk.KafkaZkClient))

- Give Security Permissions (Not a good Practice)
	- EC2 > instances > Instance ID > Security > Security Groups > Edit Inbound Rules > Add Rule
		- change Type as "All Traffic"
		- change Source as "Anywhere IPv4"
		- Save Rules

- Open a new third Terminal and connect to EC2 server and connect to kafka server
	- 1. Here we will create the topic 
	- 2. Create Producer and Consumer

- Create topic
	- bin/kafka-topics.sh --create --topic demo_test_1 --bootstrap-server 13.60.55.149:9092 --replication-factor 1 --partitions 1  .'.(change Public IP)

- Create Producer
	- bin/kafka-console-producer.sh --topic demo_test_1 --bootstrap-server 13.60.55.149:9092

- Create Consumer 
	- Open fourth terminal
	- use ssh
	- cd kafka_2.12-3.8.0
	- bin/kafka-console-consumer.sh --topic demo_test_1 --bootstrap-server 13.60.55.149:9092

- Now whatever data is produced by producer is reflected at the consumer end

- Create Bucket
	- Amazon S3 > Buckets > Create Bucket > name your bucket
	- S3 Bucket is a Object Storage
	- Now we want to Upload data from our producer to S3 Bucket

- Get AWS Access Key and private key
	- IAM > users > Create User/Add User

- Download and install AWS CLI
- Open terminal and type "aws configure"
	- Enter Access Key ID from civ file
	- Enter Secret Access Key from csv file
	- Enter region or just hit enter

- Upload data to S3 in the form of Events


