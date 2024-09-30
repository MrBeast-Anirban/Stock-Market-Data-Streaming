import boto3
import json
import time
from s3fs import S3FileSystem
import uuid
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

# Initialize AWS clients
sqs = boto3.client('sqs', 
                   aws_access_key_id='your aws access key', 
                   aws_secret_access_key='your aws secret access key', 
                   region_name='eu-central-1')  # Update region if necessary

# Replace with your SQS queue URL
queue_url = 'your sqs queue url'  

# Initialize S3
s3 = S3FileSystem()

# Initialize Dash app
app = Dash(__name__)

# Initialize data lists for visualization
x_data = []  
y_data = []  

# Layout of the Dash app
app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])

# Callback to update the graph
@app.callback(
    Output('live-update-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)


def update_graph(n):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=2
    )

    messages = response.get('Messages', [])
    
    # Initialize lists for candlestick data
    dates = []
    opens = []
    highs = []
    lows = []
    closes = []

    for message in messages:
        message_body = json.loads(message['Body'])
        data = json.loads(message_body['Message'])  

        # Append to data lists
        dates.append(data['Date'])
        opens.append(data['Open'])
        highs.append(data['High'])
        lows.append(data['Low'])
        closes.append(data['Close'])

        # Store the message in S3
        unique_id = str(uuid.uuid4().int % 1000000).zfill(6)  
        s3_path = f"s3://sdebucket-miniproject/stock_market_{unique_id}.json"  
        with s3.open(s3_path, 'w') as file:
            json.dump(data, file)

        # Delete the message from the queue after processing
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )

    # Create a candlestick figure
    figure = go.Figure(data=[go.Candlestick(x=dates,
                                             open=opens,
                                             high=highs,
                                             low=lows,
                                             close=closes)])
    figure.update_layout(title='Real-Time Stock Market Candlestick Chart',
                         xaxis_title='Date',
                         yaxis_title='Price (USD)')

    return figure

if __name__ == '__main__':
    app.run_server(debug=True,port=8080) # Run the Dash app on port 8080