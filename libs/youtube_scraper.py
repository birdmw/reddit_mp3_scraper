# 7/22/2017

from __future__ import unicode_literals

import pafy
import youtube_dl


def url_to_file(urls, settings):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': settings['preferredcodec'],
            'preferredquality': settings['preferredquality'],
        }],
    }

    less_urls = []
    for url in urls:
        with open(str('log.txt'), str('rb')) as log:
            log_urls = ''.join(log.readlines())
        if url not in log_urls:
            with open(str('log.txt'), str('a')) as log:
                log.write(url + "\n")
            try:
                duration = pafy.new(url).length
                if int(settings['min_song_len']) <= duration <= int(settings['max_song_len']):
                    less_urls.append(url)
            except:
                print "error grabbing", url
    print len(less_urls), "eligable songs"
    for i, url in enumerate(less_urls):
        print "[",i, "/", len(less_urls),"]", "=", 100*round(float(i)/float(len(less_urls)),3), "%"
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except:
            print "error getting", url


if __name__ == '__main__':
    test_urls = ['https://youtu.be/gP6FR0FbLoo', 'https://www.youtube.com/watch?v=Q7273Xl9XRU']
    url_to_file(urls=test_urls)
