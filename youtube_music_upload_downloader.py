from pathlib import Path
from ytmusicapi import YTMusic, OAuthCredentials
import os
import urllib.request
import re
import unicodedata


def normalize(name, replacement="_", max_length=255):
  # Normalize unicode (é → e)
  name = unicodedata.normalize("NFKD", name)
  name = name.encode("ascii", "ignore").decode("ascii")

  # Remove or replace forbidden characters
  name = re.sub(r"[<>:\"/\\|?*'\x00-\x1F]", replacement, name)

  # Replace spaces and repeated replacements
  name = re.sub(r'\s+', ' ', name).strip()
  name = re.sub(f"{re.escape(replacement)}+", replacement, name)

  # Optional: limit length
  name = name[:max_length].rstrip(" .")

  return name


ytmusic = YTMusic("browser.json")

# get all songs
print("loading all songs ...")
songs= ytmusic.get_library_upload_songs(None)

# get all albums
albums = ytmusic.get_library_upload_albums(None)

# loop over albums
for album in albums:
  print("-- " + normalize(album['title']))
  # define album directory name
  album_dir = "Albums/" + normalize(album['title'])
  # define thumbnail/artwork to choose
  album_thumbnail = album['thumbnails'][-1]['url']

  # create album directory
  Path(album_dir).mkdir(parents=True, exist_ok=True)
  # download thumbnail/artwork
  urllib.request.urlretrieve(album_thumbnail, album_dir + "/thumbnail.png")

  # get details for current album
  album_current = ytmusic.get_library_upload_album(album['browseId'])
  # set tracknumber in current album to 0
  track_number = 0
  # loop through current album tracks
  for track in album_current['tracks']:
    # increase track number by 1
    track_number += 1
    # set file path to music file
    print("--    " + f"{track_number:02d}" + " - " + normalize(track['title']) + " - " + track['videoId'] + ".m4a")
    file_path = album_dir + "/" + f"{track_number:02d}" + " - " + normalize(track['title']) + " - " + track['videoId'] + ".m4a"

    # download music file if it does not exist
    if not Path(file_path).is_file():
      dl_command = "yt-dlp --cookies cookie.txt 'https://music.youtube.com/watch?v=" + track['videoId'] + "' -o '" + file_path + "' -f 141"
      os.system(dl_command)

    # get details of song to get artist reliably (often not available in album data)
    artist = next(a["artists"][0]["name"] for a in songs if a["videoId"] == track['videoId'])
    tag_command = "AtomicParsley '" + file_path + "' --title \"" + track['title'] + "\" --artist \"" + artist + "\" --album \"" + album['title'] + "\" --tracknum '" + str(track_number) + "' --artwork '" + album_dir + "/thumbnail.png' --overWrite"
    os.system(tag_command)
