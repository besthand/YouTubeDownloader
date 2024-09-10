# YouTubeDownloader
要執行這個程式，你需要進行以下步驟，包括設置執行環境並執行程式。以下是完整的步驟：

### 1. **安裝 Python**
   - 如果尚未安裝 Python，可以從 [Python 官方網站](https://www.python.org/downloads/) 下載並安裝適合你的版本（推薦使用 Python 3.x）。
   - **注意**：安裝時請勾選「Add Python to PATH」，以便在命令提示字元（CMD）中直接使用 Python 指令。

### 2. **安裝所需套件**
   - 打開命令提示字元（CMD）或 PowerShell（Windows），或者終端機（Mac/Linux），並執行以下命令來安裝 `pytubefix` 以及你將用來處理影片與音訊合併的 `ffmpeg`：
   
   ```bash
   pip install pytubefix
   ```

   - 安裝 `ffmpeg`：  
     1. 你可以從 [FFmpeg 官方網站](https://ffmpeg.org/download.html) 下載並安裝適合你的平台的 FFmpeg 版本。
     2. 安裝後，將 `ffmpeg` 的路徑加入到系統的環境變數（PATH）中，以便可以在命令列直接使用 `ffmpeg` 指令。


### 3. **執行 Python 程式**

   - 打開命令提示字元（CMD）或終端機，並導航到你儲存 `ytdownloader.py` 的資料夾。例如，如果檔案儲存在 `C:\Users\你的帳號\Documents` 資料夾，可以使用以下指令切換到該目錄：
   
   ```bash
   cd C:\Users\你的帳號\Documents
   ```

   - 確保 FFmpeg 已經設定完成，並可以在命令提示字元中執行 `ffmpeg` 命令。你可以在 CMD 中輸入以下命令來檢查 FFmpeg 是否正確安裝：

   ```bash
   ffmpeg -version
   ```

   如果 FFmpeg 正常運行，你會看到版本資訊。

   - 之後，執行 Python 程式：

   ```bash
   python ytdownloader.py
   ```

   - 程式會提示你輸入 YouTube 影片網址。貼上 YouTube 影片網址並按下 Enter。

### 4. **下載並合併影片**
   - 程式會自動下載最高畫質的影片和音訊，並將其合併。
   - 所有處理過程中的檔案會儲存在以影片名稱命名的資料夾中，合併後的檔案也會以影片名稱命名並存放在同一資料夾中。
   - 如果影片名稱中有作業系統不支援的字元，這些字元會被自動替換為 `"-"`。

### 5. **確認結果**
   - 最終合併的影片檔案會以 `影片名稱.mp4` 命名，並儲存在與影片名稱相同的資料夾中。你可以打開該資料夾來檢視下載與合併的影片。

### 注意事項：
1. **ffmpeg 安裝**：若未正確安裝或設定 `ffmpeg`，合併過程可能無法順利進行。
2. **影片地區限制或登入要求**：某些 YouTube 影片可能有地區限制或需要登入觀看，這會影響下載。

