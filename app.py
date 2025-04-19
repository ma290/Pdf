import gradio as gr
import os
import yt_dlp
import requests
import shutil

# 🔒 Replace with your own bot token
BOT_TOKEN = "1701760957:AAHYs626-DnndxSeS9N_7y1_2V3Vn071Yck"

def get_chat_id():
    # Get the chat_id dynamically from the bot interactions
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        updates = response.json().get("result", [])
        if updates:
            chat_id = updates[-1]['message']['chat']['id']
            return chat_id
    return None

def send_to_telegram(video_path: str, chat_id: int):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    with open(video_path, 'rb') as video:
        response = requests.post(url, data={'chat_id': chat_id}, files={'video': video})
    return response.ok, response.text

def download_and_upload(channel_url: str):
    # Get the chat_id dynamically
    chat_id = get_chat_id()
    if chat_id is None:
        return "❌ Could not retrieve chat ID. Please make sure you've interacted with the bot."

    output_dir = "downloads"

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'ignoreerrors': True,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': False,
        'noplaylist': False,
        'extract_flat': False,
        'noprogress': True,
    }

    try:
        # Initialize yt-dlp downloader and get the video list from the channel
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(channel_url, download=False)
            video_urls = [entry['url'] for entry in info_dict['entries']]  # Get all video URLs

        status_log = ""

        for video_url in video_urls:
            # Download one video at a time
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                video_file = ydl.prepare_filename(info_dict)

            # Upload the video to Telegram chat
            status_log += f"📤 Uploading: {video_file}...\n"
            success, response = send_to_telegram(video_file, chat_id)

            if success:
                status_log += "✅ Uploaded successfully.\n"
                os.remove(video_file)  # Delete after upload
                status_log += "🗑️ Deleted after upload.\n\n"
            else:
                status_log += f"❌ Upload failed. Error: {response}\n\n"

        return status_log

    except Exception as e:
        return f"❌ Error: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("## 📥 YouTube Channel to Telegram Bot Uploader")
    channel_input = gr.Textbox(label="Enter YouTube Channel URL")
    download_button = gr.Button("Start Download + Upload")
    status_box = gr.Textbox(label="Status Log", lines=15)

    download_button.click(
        download_and_upload,
        inputs=channel_input,
        outputs=status_box
    )

demo.launch(share=True, debug=True)
