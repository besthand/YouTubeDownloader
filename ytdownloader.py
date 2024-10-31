from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import re
import subprocess

def sanitize_filename(name):
    """
    移除所有非字母數字的字元
    """
    return re.sub(r'[^a-zA-Z0-9]', '', name)

def download_and_merge(url):
    try:
        # 創建 YouTube 物件
        yt = YouTube(url)
        
        # 取得影片標題，並將不合法字元替換為 "-"
        video_title = sanitize_filename(yt.title)
        
        # 建立以影片標題命名的資料夾
        if not os.path.exists(video_title):
            os.makedirs(video_title)
        
        # 取得最高畫質的影片流（無音訊）
        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        # 取得最高音質的音訊流
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()

        # 取得字幕流
        subtitle_stream = yt.captions.get('en')  # 使用適當的語言代碼

        # 下載影片流
        video_file_path = os.path.join(video_title, "video.mp4")
        video_stream.download(output_path=video_title, filename="video.mp4")
        print(f"影片下載完成: {video_file_path}")
        
        # 下載音訊流
        audio_file_path = os.path.join(video_title, "audio.mp4")
        audio_stream.download(output_path=video_title, filename="audio.mp4")
        print(f"音訊下載完成: {audio_file_path}")

        #下載字幕
        if subtitle_stream:
            subtitle_file_path = os.path.join(video_title, f"{video_title}.srt")
            
            # 下載字幕內容
            subtitle_content = subtitle_stream.generate_srt_captions()
            
            # 將字幕內容寫入檔案
            with open(subtitle_file_path, "w", encoding="utf-8") as subtitle_file:
                subtitle_file.write(subtitle_content)
            
            print(f"字幕下載完成: {subtitle_file_path}")
        else:
            print("找不到指定語言的字幕。")

        # 使用 ffmpeg 合併影片與音訊，並將結果輸出到資料夾中
        output_file_path = os.path.join(video_title, f"{video_title}.mp4")
        command = f'ffmpeg -i "{video_file_path}" -i "{audio_file_path}" -i "{subtitle_file_path}" -c copy "{output_file_path}"'
        print(f"合併命令: {command}")
        subprocess.run(command, shell=True)

        # 清除暫存檔案（影片流和音訊流）
        os.remove(video_file_path)
        os.remove(audio_file_path)

        print(f"影片與音訊已合併完成: {output_file_path}")
        
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    video_url = input("請輸入 YouTube 影片網址: ")
    download_and_merge(video_url)