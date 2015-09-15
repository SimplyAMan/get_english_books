__author__ = 'ahuryn'

import logging
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import mutagen.id3

def setMp3Tag(mp3File,tags):
    #print('tags in setMp3Tag: ',tags)
    try:
        audio = EasyID3(mp3File)
        audio = MP3(mp3File, ID3=EasyID3)
        try:
            audio.add_tags(ID3=EasyID3)
        except mutagen.id3.error:
            pass
        if 'artist' in tags:
            logging.info('Add ' + mp3File + ' tag ''artist'' ' + tags['artist'])
            audio['artist'] = tags['artist']
        if 'album' in tags:
            logging.info('Add ' + mp3File + ' tag ''album'' ' + tags['album'])
            audio['album'] = tags['album']
        if 'title' in tags:
            logging.info('Add ' + mp3File + ' tag ''title'' ' + tags['title'])
            audio['title'] = tags['title']
        if 'date' in tags:
            logging.info('Add ' + mp3File + ' tag ''date'' ' + tags['date'])
            audio['date'] = tags['date']
        if 'genre' in tags:
            logging.info('Add ' + mp3File + ' tag ''genre'' ' + tags['genre'])
            audio['genre'] = tags['genre']
        #audiofile['year'] = 2014
        audio.save()
    except FileNotFoundError:
        logging.error('File ' + mp3File + ' doesn''t exist')
        pass
    #audio.pprint()
    #print(audio)

def getMp3Tag(mp3File):
    #audiofile = EasyID3(mp3File)
    try:
        audio = MP3(mp3File, ID3=EasyID3)
        tags = dict()
        if 'artist' in audio:
            logging.info(mp3File + ' has tag ''artist'' ')# + audio['artist'])
            tags['artist'] =  audio['artist']
        if 'album' in audio:
            logging.info(mp3File + ' has tag ''album'' ')# + audio['album'])
            tags['album'] = audio['album']
        if 'title' in audio:
            logging.info(mp3File + ' has tag ''title'' ')# + audio['title'])
            tags['title'] = audio['title']
        if 'date' in audio:
            logging.info(mp3File + ' has tag ''date'' ')# + audio['date'])
            tags['date'] = audio['date']
        if 'genre' in audio:
            logging.info(mp3File + ' has tag ''genre'' ')# + audio['genre'])
            tags['genre'] = audio['genre']
    except FileNotFoundError:
        logging.error('File '+mp3File+' doesn''t exists')
        pass
    return tags

#----------------------------------------------------------------------
def getTags(path):
    #print(path)
    return EasyID3(path)
    #print ("Artist: ", m['artist'][0])
    #print ("Album: %s" % m['album'][0])
    #print ("Track: %s" % m['title'][0])
    #print ("Release Year: %s" % m['date'][0])
#----------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    filename = r'd:\Work\python_scripts\get_voa_podcast\test.mp3'
    tags = dict(artist='artist')
    print(getMp3Tag(r'd:\Library\English Teaching\Podcasts\VOA\2014\The Making of a Nation - Voice of America\The Making of a Nation - Voice of America_2014_11_17.mp3'))
    setMp3Tag(filename,tags)
    #print(getTags(filename))
    #getMutagenTags(filename)