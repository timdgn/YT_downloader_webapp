import json
import urllib3
import os
import subprocess
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
OUTPUT_DIR = "/tmp"  # AWS Lambda has write permissions in /tmp
os.makedirs(OUTPUT_DIR, exist_ok=True)

http = urllib3.PoolManager()

def get_secret_bot_token():
    secret_name = "Telegram-bot-token"
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)
    except ClientError as e:
        raise e

    # Convert SecretString to a dictionary
    secret_string = get_secret_value_response['SecretString']
    secret = json.loads(secret_string)  # Parse the JSON string

    return secret['bot_token']

def send_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    encoded_data = json.dumps(data).encode('utf-8')
    http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})

def send_video(bot_token, chat_id, file_path):
    file_name = os.path.basename(file_path)
    url = f"https://api.telegram.org/bot{bot_token}/sendVideo"

    with open(file_path, 'rb') as video:
        video_data = video.read()  # Lire tout le fichier en bytes
        
    http.request(
        'POST',
        url,
        fields={
            "chat_id": str(chat_id),
            "video": (file_name, video_data, "video/mp4")})  # Nom du fichier, données, type MIME

def get_format_id(resolution):
    formats = {"low": "18", "medium": "22", "high": "137+140", "very high": "313+140"}
    return formats.get(resolution, "18")

def download_video(url, resolution):
    
    format_id = get_format_id(resolution)
    yt_dlp_path = "/opt/bin/yt-dlp"
    cookie_file = "/tmp/cookie.txt"
    output_path = "/tmp/%(title)s.%(ext)s"
    
    s3_bucket = "yt-cookie"
    s3_key = "www.youtube.com_cookies.txt"
    s3.download_file(s3_bucket, s3_key, cookie_file)
    
    command = [
        yt_dlp_path,
        "--cookies", cookie_file,
        "-o", output_path,
        url
    ]

    print("*** Executing command:", " ".join(command))

    process = subprocess.run(command, capture_output=True, text=True)
    print(process.stdout)

    if process.returncode == 0:    
        print("*** Download successful")
        for file in os.listdir("/tmp"):
            if file.endswith(".mp4"):
                return f"/tmp/{file}"
    else:
        print("*** Error downloading")
        return None

def lambda_handler(event, context):
    body = json.loads(event['body'])
    print(f"*** Body : {body}")
    chat_id = body['message']['chat']['id']
    message_text = body['message']['text']

    # Get the Telegram bot token from Secrets Manager
    bot_token = get_secret_bot_token()
    print(f"*** Bot Token : {bot_token}")

    # Assert there is 2 parts
    parts = message_text.split()
    if len(parts) < 2:
        msg = "Please send the URL followed by the quality (low, medium, high, very high). Example: https://youtu.be/example high"
        send_message(bot_token, chat_id, msg)
        return {'statusCode': 200, 'body': json.dumps('Invalid input')}
    url, quality = parts[0], " ".join(parts[1:])
    print(f"*** URL : {url}")
    print(f"*** Quality : {quality}")

    # Assert quality is one of the allowed values
    allowed_qualities = ["low", "medium", "high", "very high"]
    if quality not in allowed_qualities:
        msg = "Invalid quality. Please choose from low, medium, high, or very high."
        send_message(bot_token, chat_id, msg)
        print(f"*** Invalid quality : {quality}")
        return {'statusCode': 200, 'body': json.dumps('Invalid quality')}

    # Download the video
    send_message(bot_token, chat_id, "Downloading video, please wait...")
    file_path = download_video(url, quality)
    print(f"*** File Path : {file_path}")
    if file_path:
        send_video(bot_token, chat_id, file_path)
        os.remove(file_path)  # Clean up after sending
    else:
        send_message(bot_token, chat_id, "Failed to download the video. Please try again.")
    
    return {'statusCode': 200, 'body': json.dumps('Message processed successfully')}
