import pandas as pd
import boto3
import json
from time import sleep

# Initialize AWS SNS client
sns = boto3.client('sns', 
                   aws_access_key_id='your aws access key', 
                   aws_secret_access_key='your aws secret access key', 
                   region_name='eu-central-1')  

# Replace with your SNS topic ARN
topic_arn = 'your sns topic arn'


# Function to publish messages to SNS
def publish_message(message):
    response = sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps({'default': json.dumps(message)}), 
        MessageStructure='json'
    )
    print(f'Message published: {response}')

if __name__ == '__main__':
    # Example static messages
    publish_message({'name': 'Rudra Dutt'})
    publish_message({'Department': 'Computer Science and Engineering'})

    # Read from CSV and publish messages
    df = pd.read_csv("indexProcessed.csv")  # Ensure your CSV file is in the same directory
    
    for index, row in df.iterrows():
        publish_message(row.to_dict())
        sleep(1)  # Optional: Sleep to avoid overwhelming the SNS
