# youtube_music_upload_downloader
Download you previously uploaded audio tracks from YouTube Music

This little python script just exists because I lost access to my local music library and needed to download the files I uploaded myself to YouTube Music in the past.  
The only official way to do this I could find is to use Google Takeout to export all your uploads.  
Unfortunately basically all tags, folders and everything that makes sense out of a big music library is not available there anymore. At this was the case for me.  
There are applications like MusicBrainz Picard that can help you to get some metadata in your files again. For me this just worked like 50% of the time.  

Is this script super fancy and state of the art? 100% no!  
Did it help me to get my library back? 100% yes!  

## Dependencies
Just tested on Linux (Fedora). MacOS might also work. I guess Windows not....
### Python programms/libraries installed via pip
- yt-dlp (could be that you need to add ~/.local/bin to your PATH variable)
- ytmusicapi
### OS packages
- AtomicParsley

## Usage
Prepare browser.json for ytmusicapi and cookie.txt for yt-dlp. The ones here in the repo are just examples. You have to put in your real cookie values.  
Look at the documentations on how to do this:
- https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html
- https://docs.cyotek.com/cyowcopy/1.10/netscapecookieformat.html

Then your simply run the python programm:
```
python youtube_music_upload_downloader.py
```
Files will be downloaded to the current folder under `Albums` and will be put into a separate subdirectory for every album.
