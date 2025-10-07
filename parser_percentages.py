import yt_dlp
import scrapetube
import pandas as pd
import time
import re
import os
from tqdm import tqdm

# Функция для нормализации заголовков (удаление пробелов, пунктуации, регистра)
def normalize_title(title):
    title = re.sub(r'[^\w\s]', '', title.lower()).strip()
    return title

# Функция для форматирования времени в ЧЧ:ММ:СС
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Функция для определения платформы по URL
def detect_platform(url):
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'vkvideo.ru' in url or 'vk.com' in url:
        return 'vk'
    elif 'rutube.ru' in url:
        return 'rutube'
    return None

# Базовые настройки yt-dlp
base_opts = {
    'quiet': True,
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    },
    'cookiefile': 'cookies.txt',
    'retries': 3,
    'socket_timeout': 20,
    'no_warnings': True,
}

# Парсер YouTube
def parse_youtube(url):
    video_data = []
    ydl_opts = base_opts.copy()
    ydl_opts['extract_flat'] = True
    ydl_opts['http_headers']['Referer'] = 'https://youtube.com/'
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            channel_info = ydl.extract_info(url, download=False)
            channel_id = channel_info.get('channel_id', None)
            if not channel_id:
                print(f"❌ Could not extract channel_id for {url}")
                return video_data
        except Exception as e:
            print(f"❌ Error extracting channel_id for {url}: {e}")
            return video_data
    
    try:
        videos = list(scrapetube.get_channel(channel_id))  # Преобразуем в список для подсчёта
        total_videos = len(videos)
        for i, video in enumerate(tqdm(videos, desc="Parsing YouTube", unit="video")):
            try:
                title = video['title']['runs'][0]['text']
                video_url = f"https://youtube.com/watch?v={video['videoId']}"
                video_data.append({
                    'Название видео': title,
                    'normalized_title': normalize_title(title),
                    'YouTube link': video_url,
                    'VK link': '',
                    'RuTube link': '',
                    'Сайт link': '',
                    'Кто в видео?': '',
                    'Инфа': '',
                    'Инфа_1': '',
                    'Инфа_2': '',
                    'Инфа_3': ''
                })
                time.sleep(0.1)
            except Exception as e:
                print(f"⚠️ Failed to process YouTube video {i+1}/{total_videos}")
    except Exception as e:
        print(f"❌ Error fetching YouTube videos: {e}")
    
    return video_data

# Парсер VK
def parse_vk(url):
    video_data = []
    flat_opts = base_opts.copy()
    flat_opts['extract_flat'] = True
    flat_opts['http_headers']['Referer'] = 'https://vkvideo.ru/'
    flat_opts['extractor_args'] = {'vk': {'skip_auth': True}}
    
    with yt_dlp.YoutubeDL(flat_opts) as flat_ydl:
        try:
            playlist_info = flat_ydl.extract_info(url, download=False)
            total_videos = playlist_info.get('playlist_count', 0)
        except Exception as e:
            print(f"❌ VK playlist extraction error for {url}: {e}")
            return video_data
    
    if 'entries' in playlist_info:
        for i, entry in enumerate(tqdm(playlist_info['entries'], total=total_videos, desc="Parsing VK", unit="video")):
            if entry is None:
                print(f"⚠️ Skipping empty VK entry {i+1}/{total_videos}")
                continue
            
            video_id = entry.get('id', 'unknown')
            if '_' in video_id:
                owner_id, vid_id = video_id.split('_', 1)
                video_url = f"https://vkvideo.ru/video{owner_id}_{vid_id}"
            else:
                video_url = entry.get('url', 'No URL')
            
            title = entry.get('title', 'No title')
            
            try:
                full_opts = base_opts.copy()
                full_opts['extract_flat'] = False
                full_opts['http_headers']['Referer'] = 'https://vkvideo.ru/'
                full_opts['extractor_args'] = {'vk': {'skip_auth': True}}
                with yt_dlp.YoutubeDL(full_opts) as full_ydl:
                    full_entry = full_ydl.extract_info(entry['url'], download=False)
                    title = full_entry.get('title', title)
                    video_url = full_entry.get('webpage_url', video_url)
            except Exception as e:
                print(f"⚠️ Failed to process VK video {i+1}/{total_videos}")
            
            video_data.append({
                'Название видео': title,
                'normalized_title': normalize_title(title),
                'YouTube link': '',
                'VK link': video_url,
                'RuTube link': '',
                'Сайт link': '',
                'Кто в видео?': '',
                'Инфа': '',
                'Инфа_1': '',
                'Инфа_2': '',
                'Инфа_3': ''
            })
            time.sleep(1.5)
    
    return video_data

# Парсер Rutube
def parse_rutube(url):
    video_data = []
    flat_opts = base_opts.copy()
    flat_opts['extract_flat'] = True
    flat_opts['http_headers']['Referer'] = 'https://rutube.ru/'
    flat_opts['extractor_args'] = {'rutube': {'skip_auth': True}}
    
    with yt_dlp.YoutubeDL(flat_opts) as flat_ydl:
        try:
            playlist_info = flat_ydl.extract_info(url, download=False)
            total_videos = playlist_info.get('playlist_count', 0)
        except Exception as e:
            print(f"❌ Rutube playlist extraction error for {url}: {e}")
            return video_data
    
    if 'entries' in playlist_info:
        for i, entry in enumerate(tqdm(playlist_info['entries'], total=total_videos, desc="Parsing RuTube", unit="video")):
            if entry is None:
                print(f"⚠️ Skipping empty RuTube entry {i+1}/{total_videos}")
                continue
            
            video_id = entry.get('id', 'unknown')
            video_url = f"https://rutube.ru/video/{video_id}/"
            title = entry.get('title', 'No title')
            
            try:
                full_opts = base_opts.copy()
                full_opts['extract_flat'] = False
                full_opts['http_headers']['Referer'] = 'https://rutube.ru/'
                full_opts['extractor_args'] = {'rutube': {'skip_auth': True}}
                with yt_dlp.YoutubeDL(full_opts) as full_ydl:
                    full_entry = full_ydl.extract_info(entry['url'], download=False)
                    title = full_entry.get('title', title)
                    video_url = full_entry.get('webpage_url', video_url)
            except Exception as e:
                print(f"⚠️ Failed to process RuTube video {i+1}/{total_videos}")
            
            video_data.append({
                'Название видео': title,
                'normalized_title': normalize_title(title),
                'YouTube link': '',
                'VK link': '',
                'RuTube link': video_url,
                'Сайт link': '',
                'Кто в видео?': '',
                'Инфа': '',
                'Инфа_1': '',
                'Инфа_2': '',
                'Инфа_3': ''
            })
            time.sleep(1.5)
    
    return video_data

# Основная логика
start_time = time.time()

urls = input("Введите ссылки через запятую (YouTube, VK, Rutube): ").strip().split(',')
urls = [url.strip() for url in urls if url.strip()]

all_videos = []

for url in urls:
    platform = detect_platform(url)
    if not platform:
        print(f"❌ Unsupported platform for URL: {url}")
        continue
    
    if platform == 'youtube':
        all_videos.extend(parse_youtube(url))
    elif platform == 'vk':
        all_videos.extend(parse_vk(url))
    elif platform == 'rutube':
        all_videos.extend(parse_rutube(url))

# Объединение дубликатов по normalized_title
if all_videos:
    video_dict = {}
    for video in all_videos:
        norm_title = video['normalized_title']
        if norm_title in video_dict:
            video_dict[norm_title]['YouTube link'] = video_dict[norm_title]['YouTube link'] or video['YouTube link']
            video_dict[norm_title]['VK link'] = video_dict[norm_title]['VK link'] or video['VK link']
            video_dict[norm_title]['RuTube link'] = video_dict[norm_title]['RuTube link'] or video['RuTube link']
            video_dict[norm_title]['Название видео'] = video_dict[norm_title]['Название видео'] or video['Название видео']
        else:
            video_dict[norm_title] = video
    
    merged_videos = list(video_dict.values())
    
    for video in merged_videos:
        del video['normalized_title']
    
    output_file = 'videos.xlsx'
    try:
        df = pd.DataFrame(merged_videos, columns=[
            'Название видео', 'Кто в видео?', 'YouTube link', 'Инфа',
            'VK link', 'Инфа_1', 'RuTube link', 'Инфа_2',
            'Сайт link', 'Инфа_3'
        ])
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"✅ Saved {len(merged_videos)} unique videos to {output_file}")
        if os.path.exists(output_file):
            print(f"File {output_file} exists, size: {os.path.getsize(output_file)} bytes")
        else:
            print(f"❌ File {output_file} was not created")
    except Exception as e:
        print(f"❌ Error saving to XLSX: {e}")
else:
    print("❌ No video data to save.")

end_time = time.time()
execution_time = end_time - start_time
print(f"Total execution time: {format_time(execution_time)}")
input("Готово! Проверьте videos.xlsx — ссылки должны открывать видео для просмотра.")