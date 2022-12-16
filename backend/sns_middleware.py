import boto3
import json

class sns_middleware():
    def __init__(self):
        self.sns_client = boto3.client('sns', 'us-east-1',
                           aws_secret_access_key='EUbgOf1q+30p/dSOH6piXQcTGL6LUfAoJHjHdLKg',
                           aws_access_key_id='AKIASTUKBQHD67W3Z6DA')


    def register_notification(self, request, respone):
        print(respone.status_code)
        if respone.status_code == 200:

            data = request.get_json()
            username = data['username']
            email = data['email']
            file = {'username': username,
                    'email': email
                    }

            r = self.sns_client.publish(
                TopicArn='arn:aws:sns:us-east-1:179604390343:test',
                Message=json.dumps(file),

            )

            print(r)