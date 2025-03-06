import os
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

# Function to search for a song on YouTube
def search_youtube(query):
    results = YoutubeSearch(query, max_results=1).to_dict()
    if results:
        return 'https://www.youtube.com' + results[0]['url_suffix']
    return None

# Function to download the YouTube video as an mp3
def download_youtube(url, output_dir='downloads'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'ffmpeg_location': r'C:\ffmpeg\bin',  # Full path to ffmpeg and ffprobe
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Function to process the text file and handle downloading
def download_songs_from_txt(file_path):
    # Ensure the downloads directory exists
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    downloaded_count = 0  # Counter for downloaded songs

    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                # Extracting the song title from each line (splitting by ' – ')
                song_title = line.split(' – ')[0]
                print(f"Searching for: {song_title}")
                
                # Search the song on YouTube
                url = search_youtube(song_title)
                if url:
                    print(f"Found on YouTube: {url}")
                    # Download the song
                    download_youtube(url)
                    downloaded_count += 1  # Increment the counter
                else:
                    print(f"Could not find: {song_title}")

    print(f"\nTotal songs downloaded: {downloaded_count}")  # Print the total count

if __name__ == "__main__":
    # Path to your text file containing the list of songs
    file_path = 'list.txt'
    download_songs_from_txt(file_path)
