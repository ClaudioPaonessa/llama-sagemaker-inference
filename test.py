import boto3
import json

session = boto3.Session()
# Create a low-level client representing Amazon SageMaker Runtime
sagemaker_runtime = session.client("sagemaker-runtime", region_name="eu-central-1")

# The name of the endpoint. The name must be unique within an AWS Region in your AWS account. 
endpoint_name='app-endpoint'

input = {"text": "Say yes or no!", "token_count": 8}

# After you deploy a model into production using SageMaker hosting 
# services, your client applications use this API to get inferences 
# from the model hosted at the specified endpoint.
response = sagemaker_runtime.invoke_endpoint(
                            EndpointName=endpoint_name, 
                            Body=json.dumps(input), ContentType='application/json'
                            )

# Optional - Print the response body and decode it so it is human read-able.
print(response['Body'].read().decode('utf-8'))