import json
import hmac
import hashlib
import base64
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def lambda_handler(event, context):
    logger.info('Event: {}'.format(json.dumps(event)))
    try:
        if not 'sub' in event or len(event['sub']) == 0:
            raise Exception('Parameter \'sub\' is required.')
        if not 'clientId' in event or len(event['clientId']) == 0:
            raise Exception('Parameter \'clientId\' is required.')
        if not 'clientSecret' in event or len(event['clientSecret']) == 0:
            raise Exception('Parameter \'clientSecret\' is required.')
    except Exception as e:
        logger.error('Error: {}'.format(e))
        error_msg = {
            'message': str(e)
        }
        return {
            'statusCode': 502,
            'body': json.dumps(error_msg)
        }
    sub_payload = '{}{}'.format(event['sub'], event['clientId'])
    digest = hmac.new(event['clientSecret'].encode(
        'UTF-8'),
        msg = sub_payload.encode('UTF-8'),
        digestmod = hashlib.sha256
    ).digest()
    secret_hash = base64.b64encode(digest).decode()
    logger.info('Secret Hash: {}'.format(secret_hash))
    return {
        'statusCode': 200,
        'body': {
            'secretHash': secret_hash
        }
    }
