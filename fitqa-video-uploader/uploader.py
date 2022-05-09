import base64
import cgi
import json
import logging
import os
from io import BytesIO

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from token_generator import random_character_with_prefix

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
  status_code = 200

  destinationBucket = os.environ['DestinationBucket']
  video_name = random_character_with_prefix("")
  params = parse_into_field_storage(event)

  resp_body = {'key': video_name}

  try:
    video_file = BytesIO(params['video'][0])
    upload_file(video_file, destinationBucket, video_name)
  except KeyError:
    status_code = 400
    resp_body = {'message': 'video parameter not found.'}

  return {
    "statusCode": status_code,
    "body": json.dumps(resp_body)
  }


def parse_into_field_storage(event):
  header = event['headers']
  body = event['body']
  is_base64_encoded = event['isBase64Encoded']

  if is_base64_encoded:
    body = base64.b64decode(body)
  body = BytesIO(body)

  _, pdict = cgi.parse_header(header['content-type'])
  pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
  pdict['CONTENT-LENGTH'] = bytes(header['content-length'], "utf-8")
  return cgi.parse_multipart(body, pdict)


def upload_file(file, destinationBucket: str, path: str):
  s3 = boto3.client('s3')
  try:
    s3.upload_fileobj(file, destinationBucket, path)
    logger.info("Upload successful")
  except ClientError as e:
    logger.error(e)
  except NoCredentialsError as e:
    logger.error(e)
