import json
import urllib3
import os
import subprocess
import boto3
from botocore.exceptions import ClientError


OUTPUT_DIR = "/tmp"  # AWS Lambda has write permissions in /tmp
FORMATS = {
    "low": "bestvideo[height<=240][ext=mp4]+bestaudio[ext=mp4]",
    "medium": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=mp4]",
    "high": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=mp4]"}
os.makedirs(OUTPUT_DIR, exist_ok=True)

s3 = boto3.client('s3')
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


def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    encoded_data = json.dumps(data).encode('utf-8')
    http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})


def send_video(chat_id, file_path):
    file_name = os.path.basename(file_path)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"

    with open(file_path, 'rb') as video:
        video_data = video.read()  # Lire tout le fichier en bytes
        
    http.request(
        'POST',
        url,
        fields={
            "chat_id": str(chat_id),
            "video": (file_name, video_data, "video/mp4")})  # Nom du fichier, données, type MIME


def download_video(url, resolution):
    
    format = FORMATS.get(resolution, FORMATS["medium"])
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
                print("*** No mp4 file found")
                return None
    else:
        print("*** Error downloading")
        return None


def lambda_handler(event, context):
    print(f"*** Event : {event}")
    body = json.loads(event['body'])
    print(f"*** Body : {body}")
    try:
        chat_id = body['message']['chat']['id']
        message_text = body['message']['text']
    except KeyError:
        chat_id = body['edited_message']['chat']['id']
        message_text = body['edited_message']['text']

    # Get the Telegram bot token from Secrets Manager
    global BOT_TOKEN
    BOT_TOKEN = get_secret_bot_token()
    print(f"*** Bot Token : {BOT_TOKEN}")

    # Assert there is 2 parts
    parts = message_text.split()
    if len(parts) != 2:
        msg = f"Please send the URL followed by the resolution ({', '.join(FORMATS.keys())}). Example: https://youtu.be/example high"
        send_message(chat_id, msg)
        return {'statusCode': 200, 'body': json.dumps('Invalid input')}
    url, resolution = parts[0], parts[1]
    print(f"*** URL : {url}")
    print(f"*** resolution : {resolution}")

    # Assert resolution is one of the allowed values
    if resolution not in FORMATS.keys():
        msg = f"Invalid resolution. Please choose from {', '.join(FORMATS.keys())}."
        send_message(chat_id, msg)
        print(f"*** Invalid resolution : {resolution}")
        return {'statusCode': 200, 'body': json.dumps('Invalid resolution')}

    # Download the video
    send_message(chat_id, "Downloading video, please wait...")
    file_path = download_video(url, resolution)
    print(f"*** File Path : {file_path}")
    if file_path:
        file_name = os.path.basename(file_path)
        msg = f"""Sending "{file_name}" at {resolution} resolution..."""
        send_message(chat_id, msg)
        send_video(chat_id, file_path)
        os.remove(file_path)  # Clean up after sending
    else:
        send_message(chat_id, "Failed to download the video. Please try again.")
    
    return {'statusCode': 200, 'body': json.dumps('Message processed successfully')}
