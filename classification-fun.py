import json
import boto3
import base64



s3 = boto3.client('s3')
#runtime= boto3.client('runtime.sagemaker')
runtime = boto3.Session().client('sagemaker-runtime')

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2023-04-10-05-22-59-496"       ## TODO: fill in

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])  ## TODO: fill in)

    # Instantiate a Predictor
    predictor =  runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType='image/png', Body=image) ## TODO: fill in

    # For this model the IdentitySerializer needs to be "image/png"
    #predictor.serializer = IdentitySerializer("image/png")

    # Make a prediction:
    inferences =predictor['Body'].read().decode('utf-8') ## TODO: fill in

    # We return the data back to the Step Function
    event["inferences"] = [float(x) for x in inferences[1:-1].split(',')]
    return {
        'statusCode': 200,
        'body': {
            "image_data": event['body']['image_data'],
            "s3_bucket": event['body']['s3_bucket'],
            "s3_key": event['body']['s3_key'],
            "inferences": event['inferences'],}

    }
