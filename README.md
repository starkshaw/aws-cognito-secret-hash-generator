# aws-cognito-secret-hash-generator
A Lambda function generates secret hash based on user sub, client ID, and client secret.

## Internal Dependencies

The following libraries are included in AWS Lambda Python runtimes:

- `json`
- `logging`
- `hmac`
- `hashlib`
- `base64`

## Example Lambda Event

```
{
  "sub": "",
  "clientId": "",
  "clientSecret": ""
}
```

All parameters are compulsory to calculate a secret hash.

`sub`: The subject claim of a user.
`clientId`: Cognito user pool app client ID.
`clientSecret`: Cognito user pool app client secret.

## Example Lambda Response

```
{
  "statusCode": 200,
  "body": {
    "secretHash": ""
  }
}
```

The `secretHash` key inside `body` stores the secret hash calculated based on `sub`, `clientId`, and `clientSecret`.

This Lambda function is minimum and will not verify if `sub` is actually an user inside a Cognito user pool with certain `clientId` with its corresponding `clientSecret`. Therefore, if any of the values are not correct, the secret hash will not pass the authentication request against Cognito user pool endpoint.

## Logging

If the Lambda function has the following permission, it will send diagnostic logs to CloudWatch log:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:<region>:<account-id>:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:<region>:<account-id>:log-group:/aws/lambda/<lambda-function-name>:*"
            ]
        }
    ]
}
```

Lambda function created as of today will automatically generate an execution role with this IAM policy attached.

### Notice

Since this Lambda function requires sensitive information such as the pair of client ID and client secret, the default logging level is set as `logging.ERROR`. Therefore, the function payload is not sent to CloudWatch automatically. Only the error message is forwarded to CloudWatch logs.