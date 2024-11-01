from pytubefix import YouTube
from pytubefix.cli import on_progress
import platform
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

        # 設定 CRF 和預設
        crf_value = 18  # 調整此值以改變品質

        # 獲取原始影片和音訊的大小（以byte為單位）
        original_size = os.path.getsize(video_file_path) + os.path.getsize(audio_file_path)

        # 計算目標檔案大小（120% 的原始大小）
        target_size = original_size * 1.2

        # 獲取影片的長度（秒）
        duration = yt.length

        # 計算平均比特率（Kbps）
        average_bitrate = (target_size * 8) / (duration * 1024)


        # 根據顯示卡類型選擇編碼器
        gpu_type = get_gpu_type()

        if gpu_type == 'nvidia':
            video_encoder = 'hevc_nvenc'
            print("使用 NVIDIA 編碼器")
        elif gpu_type == 'amd':
            video_encoder = 'hevc_amf'
            print("使用 AMD 編碼器")
        else:
            video_encoder = 'libx265'  # 預設使用軟體編碼
            print("使用軟體編碼")

        # 使用 ffmpeg 合併影片與音訊，並將結果輸出到資料夾中
        output_file_path = os.path.join(video_title, f"{video_title}.mp4")
        command = f'ffmpeg -i "{audio_file_path}" -i "{video_file_path}" -c:v {video_encoder} -b:v {average_bitrate}k -c:a copy "{output_file_path}"'
        print(f"合併命令: {command}")
        subprocess.run(command, shell=True)

        # 清除暫存檔案（影片流和音訊流）
        os.remove(video_file_path)
        os.remove(audio_file_path)

        print(f"影片與音訊已合併完成: {output_file_path}") 
    except Exception as e:
        print(f"發生錯誤: {e}")

def get_gpu_type():
    try:
        system = platform.system().lower()

        if system == 'windows':
            # 使用 wmic 指令在 Windows 上取得顯示卡資訊
            result = subprocess.run(['wmic', 'path', 'win32_videocontroller', 'get', 'name'], stdout=subprocess.PIPE, text=True)
        elif system == 'linux':
            # 使用 lspci 指令在 Linux 上取得顯示卡資訊
            result = subprocess.run(['lspci'], stdout=subprocess.PIPE, text=True)
        else:
            print("不支援的作業系統")
            return 'unknown'

        output = result.stdout.lower()

        if 'nvidia' in output:
            return 'nvidia'
        elif 'amd' in output or 'advanced micro devices' in output:
            return 'amd'
        else:
            return 'unknown'
    except Exception as e:
        print(f"無法檢測顯示卡類型: {e}")
        return 'unknown'

if __name__ == "__main__":
    video_url = input("請輸入 YouTube 影片網址: ")
    download_and_merge(video_url)