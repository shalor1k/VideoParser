# Video Parser

A Python tool to scrape video metadata (titles and URLs) from YouTube, VK, and RuTube channels or playlists and save them into an Excel file (`videos.xlsx`). The tool identifies duplicate videos across platforms by normalizing titles and merges their links into a single entry.

## Features
- **Supported Platforms**: YouTube, VK (vkvideo.ru), RuTube.
- **Output**: Saves video titles and URLs to `videos.xlsx` with columns:
  - `Название видео` (Video Title)
  - `Кто в видео?` (Who is in the video?)
  - `YouTube link`, `VK link`, `RuTube link`, `Сайт link` (Website link)
  - `Инфа`, `Инфа_1`, `Инфа_2`, `Инфа_3` (Additional info fields, empty by default)
- **Duplicate Handling**: Merges videos with similar titles (case-insensitive, ignoring punctuation) into one row with links from all platforms.
- **Two Versions**:
  - `parser.py`: Verbose mode with detailed logs (channel IDs, video titles, URLs, metadata).
  - `parser_percentages.py`: Minimalist mode with progress bars, execution time, and only essential error messages.

## Prerequisites
- **Python**: 3.8 or higher
- **Dependencies**:
  ```bash
  pip install -U yt-dlp scrapetube pandas openpyxl tqdm
  ```
  - `yt-dlp`: For scraping video metadata from YouTube, VK, and RuTube.
  - `scrapetube`: For fetching YouTube channel videos.
  - `pandas` and `openpyxl`: For creating and saving Excel files.
  - `tqdm` (for `parser_percentages.py`): For progress bars.
- **Cookies** (optional): A `cookies.txt` file with cookies for `youtube.com`, `vkvideo.ru`, and `rutube.ru` to bypass restrictions. Export cookies using browser extensions like "Get cookies.txt".

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/video-parser.git
   cd video-parser
   ```
2. Install dependencies:
   ```bash
   pip install -U yt-dlp scrapetube pandas openpyxl tqdm
   ```
3. (Optional) Place `cookies.txt` in the same directory as the scripts to handle authenticated requests.

## Usage
1. **Run the script**:
   - For verbose output with detailed logs:
     ```bash
     python parser.py
     ```
   - For minimal output with progress bars and execution time:
     ```bash
     python parser_percentages.py
     ```
2. **Input**:
   - Enter comma-separated URLs for YouTube, VK, or RuTube channels/playlists when prompted:
     ```
     Enter URLs separated by commas (YouTube, VK, Rutube): https://youtube.com/@garchenmoscow,https://vkvideo.ru/@garchenmoscow/all,https://rutube.ru/channel/31787118/videos/
     ```
3. **Output**:
   - The script generates `videos.xlsx` in the working directory with video metadata.
   - Example output for `parser_percentages.py`:
     ```
     Enter URLs separated by commas (YouTube, VK, Rutube): https://youtube.com/@garchenmoscow,https://vkvideo.ru/@garchenmoscow/all,https://rutube.ru/channel/31787118/videos/
     Parsing YouTube: 100%|██████████████████████████| 53/53 [00:05<00:00, 10.00video/s]
     Parsing VK: 100%|██████████████████████████████| 353/353 [23:20<00:00, 3.97s/video]
     Parsing RuTube: 100%|██████████████████████████| 269/269 [17:50<00:00, 3.98s/video]
     ✅ Saved 500 unique videos to videos.xlsx
     File videos.xlsx exists, size: 12345 bytes
     Total execution time: 00:41:15
     Done! Check videos.xlsx for video links.
     ```

## Scripts
- **`parser.py`**:
  - Outputs detailed logs for debugging, including channel IDs, video titles, URLs, and metadata extraction status.
  - Useful for developers or when troubleshooting issues.
  - Example log snippet:
    ```
    Extracted channel_id: UCno-vdHYIBiEjJyuCF2rpJg
    0: Название: Друбпон Лама Палкьи. Совет практикующим
    0: URL: https://youtube.com/watch?v=b5p_nIuePWI
    ```

- **`parser_percentages.py`**:
  - Displays progress bars for each platform using `tqdm`.
  - Shows only critical errors (e.g., `❌ Error fetching videos`) and skipped videos (e.g., `⚠️ Failed to process VK video 4/353`).
  - Reports total execution time in `HH:MM:SS` format.
  - Ideal for end-users who want a clean interface.

## Building Executable
To create a standalone `.exe` file for Windows:
1. Install PyInstaller:
   ```bash
   pip install -U pyinstaller
   ```
2. Run PyInstaller for either script:
   ```bash
   pyinstaller --onefile --add-data "cookies.txt;." --hidden-import yt_dlp --hidden-import scrapetube --hidden-import pandas --hidden-import openpyxl --hidden-import tqdm parser_percentages.py
   ```
3. Find `parser_percentages.exe` in the `dist` folder.
4. Ensure `cookies.txt` is in the same directory as the `.exe` (if used).

## Notes
- **Cookies**: Some platforms (e.g., VK, RuTube) may require cookies to bypass rate limits or access restrictions. Use a browser extension to export cookies to `cookies.txt`.
- **Network Issues**: If you encounter `ConnectionResetError`, try:
  - Using a VPN to bypass regional restrictions.
  - Increasing `time.sleep(2)` in `parse_vk` or `parse_rutube` in the script.
  - Adding a proxy to `base_opts` in the script:
    ```python
    base_opts['proxy'] = 'http://your_proxy:port'
    ```
- **Excel File**: Ensure the working directory has write permissions to create `videos.xlsx`. Alternatively, specify a full path:
  ```python
  output_file = 'C:/path/to/videos.xlsx'
  ```
- **Performance**: Parsing VK and RuTube may take longer due to API rate limits and `time.sleep(1.5)` delays to avoid bans.

## Troubleshooting
- **Module Not Found**: Ensure all dependencies are installed in the active Python environment.
- **Empty Excel File**: Check write permissions or if `openpyxl` is installed (`pip show openpyxl`).
- **Connection Errors**: Verify `cookies.txt` or use a VPN/proxy.
- **Progress Bars Not Showing**: Run the script in a terminal (e.g., Command Prompt, PowerShell) instead of an IDE.

## License
MIT License

## Contributing
Feel free to open issues or submit pull requests for improvements or bug fixes.
