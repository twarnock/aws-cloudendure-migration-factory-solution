#########################################################################################
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.                    #
# SPDX-License-Identifier: MIT-0                                                        #
#                                                                                       #
# Permission is hereby granted, free of charge, to any person obtaining a copy of this  #
# software and associated documentation files (the "Software"), to deal in the Software #
# without restriction, including without limitation the rights to use, copy, modify,    #
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to    #
# permit persons to whom the Software is furnished to do so.                            #
#                                                                                       #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,   #
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A         #
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT    #
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION     #
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE        #
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                #
#########################################################################################

import json
import boto3
import os

def lambda_handler(event, context):

    try:
        body = json.loads(event['body'])    
        userid = body['username']
        password = body['password']
        client = boto3.client('cognito-idp')
        response = client.initiate_auth(
            ClientId=os.environ['clientId'],
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': userid,
                'PASSWORD': password
            }
        )
    except Exception as e:
        if "NotAuthorizedException" in str(e) or "UserNotFoundException" in str(e):
            return {'headers': {'Access-Control-Allow-Origin': '*'},
                    'statusCode': 400,
                    'body': 'Incorrect username or password'
                  }
    return {'headers': {'Access-Control-Allow-Origin': '*'},
        'statusCode': 200,
        'body': json.dumps(response['AuthenticationResult']['IdToken'])
    }

