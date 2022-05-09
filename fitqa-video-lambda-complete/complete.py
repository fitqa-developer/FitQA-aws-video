import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs = boto3.resource('sqs', )
queue = sqs.get_queue_by_name(QueueName=os.environ['QueueName'])

def handler(event, context):
  status_code = 200

  detail = event['detail']
  status = detail['status']
  metadata = detail['userMetadata']

  output = {}
  output['status'] = "SUCCESS" if status != "ERROR" else "ERROR"
  output['time'] = event['time']
  output['key'] = extract_key(metadata)

  try:
    output['files'] = extract_output(event['detail']['outputGroupDetails'])

    # Send a message.
    body = json.dumps(output, indent=4)
    response = queue.send_message(MessageBody=body)
    print(response)

  except Exception as e:
    logger.error('Exception: %s', e)
    status_code = 500
    raise
  finally:
    return {
      'statusCode': status_code,
      'body': json.dumps(output, indent=4, sort_keys=True, default=str),
      'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    }

def extract_key(metadata: dict[str, str]) -> str:
  file_name = metadata['input']
  return file_name.split('/')[-1]

def extract_output(output_detail):
  output = []
  for group in output_detail:
    if group['type'] == 'HLS_GROUP':
      continue

    detail = group['outputDetails'][0]
    file_path = detail['outputFilePaths'][0]
    file_type = 'image' if file_path.endswith('.jpg') else 'video'
    output.append({
      'type': file_type,
      'url': convert_public_url(file_path),
      'width': detail['videoDetails']['widthInPx'],
      'height': detail['videoDetails']['heightInPx'],
    })
  return output


def convert_public_url(path: str):
  return path.replace("s3://fitqa-video-dest",
                      "https://fitqa-video-dest.s3.ap-northeast-2.amazonaws.com")
