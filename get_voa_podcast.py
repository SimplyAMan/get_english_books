import logging
import feedparser
import urllib
import os
import Mp3Tag
import json


def get_log_name():
    return os.path.basename(__file__).split('.')[0] + '.log'


def get_config_name():
    return os.path.basename(__file__).split('.')[0] + '.json'

'''Function return file name by mp3 information'''


def get_filename(new_tags):
    filename = new_tags['path'] + '\\' + \
        new_tags['artist'] + '\\' + \
        new_tags['year'] + '\\' + \
        new_tags['album'] + '\\' + \
        new_tags['album'] + '_' + \
        new_tags['year'] + '_' +\
        new_tags['month'] + '_' +\
        new_tags['day'] + '.mp3'
    index = 1
    while os.path.exists(filename):
        tags = Mp3Tag.getTags(filename)
        if new_tags['artist'] != tags['artist'][0] \
                or new_tags['album'] != tags['album'][0] \
                or new_tags['title'] != tags['title'][0]:
            # if file with this name already exists but it's not this file than
            # create new file name
            filename = os.path.splitext(
                filename)[0] + '_' + str(index) + os.path.splitext(filename)[1]
            index += 1
        else:
            # if file with this name exists and it's this file than return
            # current file name
            break
    return filename

if __name__ == "__main__":
    logging.basicConfig(filename=get_log_name(), level=logging.INFO)
    logging.info('Started')

    with open(get_config_name()) as json_data_file:
        config = json.load(json_data_file)

    for voanews_podcast_url in config['urls']:
        logging.info('Process ' + voanews_podcast_url)
        feed = feedparser.parse(voanews_podcast_url)
        feed_title = feed['feed'].title
        author = feed['feed'].author
        image = feed['feed'].image.href

        for e in feed.entries:
            url = e.links[0]['href']
            webFile = urllib.request.urlopen(url)
            new_tags = dict(
                path=config['path'],
                year=str(e['published_parsed'].tm_year),
                month="{:0>2d}".format(e['published_parsed'].tm_mon),
                day="{:0>2d}".format(e['published_parsed'].tm_mday),
                artist=author,
                album=feed_title,
                title=e['title_detail']['value'],
                genre='podcast')
            mp3FileName = get_filename(new_tags)
            directory = os.path.dirname(mp3FileName)
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(mp3FileName):
                localFile = open(mp3FileName, 'wb')
                localFile.write(webFile.read())
                localFile.close()
                logging.info(mp3FileName + ' downloaded')
                Mp3Tag.setMp3Tag(mp3FileName, new_tags)
            webFile.close()
    print('complete downloads')
    logging.info('Finished')
