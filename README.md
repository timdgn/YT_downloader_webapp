# YouTube Video Downloader 🎞️

A streamlined web application built with Streamlit that allows you to download YouTube videos and playlists in various quality settings.

## Features ✨

- Download single or multiple YouTube videos
- Download entire YouTube playlists
- Select video quality (360p to 4K)
- User-friendly interface
- Progress tracking for downloads
- Support for multiple video formats

## Quality Options 🎥

- Low (360p)
- Medium (720p)
- High (1080p)
- Very High (4K)

## Installation 🚀

1. Clone this repository:
```bash
git clone https://github.com/timdgn/YT_downloader_webapp.git
```
```bash
cd YT_downloader_webapp
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage 💻

1. Start the application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Choose between downloading individual videos or playlists

4. For videos:
   - Enter one or more YouTube URLs (separated by spaces)
   - Select desired video quality
   - Click "Download Videos 🔥"

5. For playlists:
   - Enter the playlist URL
   - Select desired video quality
   - Click "Download Playlist 🔥"

## Notes 📝

- Downloaded videos will be saved in the `output` directory
- Internet connection is required for downloading videos
- Download speed depends on your internet connection and the selected video quality

# AWS Lambda and Telegram Bot

## Telegram Bot token

1. Create a new bot on Telegram
2. Get the bot token from the botfather
3. Add the token in your AWS Secret Manager
4. Adapt the lambda_function.py file to use the secret
5. Update the Lambda function Configuration > Permissions > Click on the Role name > Add permissions > Create inline policy > Add the read access policy for the secret

## API Gateway

1. Create a new HTTP API
2. Add a new integration with your Lambda function
3. Choose "Method" as ANY for simplicity, the "Resource path" like "/my_api", and "Integration target" as your Lambda function name
4. Keep Stage name ad "$default" and "Auto-deployed" selected
5. Get webhook info by using this url https://api.telegram.org/bot<BOT_TOKEN>/getWebhookInfo
6. Add webhook by using this url https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=<API_GATEWAY_URL>
7. (Optional) Delete webhook by using this url https://api.telegram.org/bot<BOT_TOKEN>/deleteWebhook

## Lambda Layer for yt-dlp

To create an AWS Lambda layer for yt-dlp, follow these steps:

1. Create a new directory for the layer:
   ```bash
   mkdir yt-dlp-layer && cd yt-dlp-layer
   ```

2. Create a `bin` directory inside it:
   ```bash
   mkdir -p bin
   ```

3. Download `yt-dlp`:
   ```bash
   curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o bin/yt-dlp
   ```

4. Make the downloaded file executable:
   ```bash
   chmod +x bin/yt-dlp
   ```

5. Zip the layer:
   ```bash
   zip -r yt-dlp-layer.zip bin
   ```

6. Upload the zip file to AWS Lambda as a new layer and assign it to your Lambda function.

## Cookies

Yt-dlp sometimes needs cookies to work

1. Export your youtube cookies with a Chrome extention like "Get cookies.txt LOCALLY"
2. Create a new bucket in your AWS account
3. Upload the youtube cookies .txt file to the bucket
4. Adapt the lambda_function.py file to use the bucket name and file key (i.e. the path in the bucket)
5. Update the Lambda function Configuration > Permissions > Click on the Role name > Add permissions > Create inline policy > Add the read access policy for the bucket

## Notes 📝

Debug using CloudWatch Log groups and Lambda function logs located in the Monitoring tab