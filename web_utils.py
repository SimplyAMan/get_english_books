import urllib.request
import os
import re
import sys
import math


def progressbar(prefix="", size=60):
    count = 100

    def _show(_i):
        x = int(size * _i / count)
        # sys.stdout.write("%s[%s%s] %i/%i\r" %
        #                  (prefix, "#" * x, "." * (size - x), _i, count))
        sys.stdout.write("%s[%s%s] %i\r" %
                         (prefix, "#" * x, "." * (size - x), _i))
        sys.stdout.flush()

    _show(0)
    for i, item in enumerate(range(100)):
        yield item
        _show(i + 1)
    sys.stdout.write("\n")
    sys.stdout.flush()


def check_file_exists(
        url,
        path):
    webFile = urllib.request.urlopen(url)
    web_file_name = re.findall(
        "filename=\"(\S+)\"", webFile.getheader('Content-Disposition'))[0]
    web_file_size = int(webFile.getheader('Content-Length'))
    try:
        local_file_name = os.path.join(path, web_file_name)
        local_file_size = os.path.getsize(local_file_name)
        if web_file_size != local_file_size:
            file_exists = False
        else:
            file_exists = True
    except OSError as e:
        print('file doesn\'t exists')
        file_exists = False
    if not file_exists:
        # print(file_exists)
        print('need to download file ' + web_file_name)
    return file_exists


def download_file(
        file_url,
        dest_path):
    if not check_file_exists(file_url, dest_path):
        # print(file_url)
        webFile = urllib.request.urlopen(file_url)
        localFileName = re.findall(
            "filename=\"(\S+)\"", webFile.getheader('Content-Disposition'))[0]
        web_file_size = int(webFile.getheader('Content-Length'))
        # print(localFileName)

        localFile = open(os.path.join(dest_path, localFileName), 'wb')

        # chunk_size = 1024 * 256
        chunk_size = math.ceil(web_file_size / 100)
        # i = 1
        # while 1:
        # range_size = web_file_size // chunk_size
        print("Download " + localFileName + ':')
        for i in progressbar('', 40):
            chunk = webFile.read(chunk_size)
            localFile.write(chunk)
            # sys.stdout.write("\r{0}".format(i))
            # i += 1
            if not chunk:
                break

        localFile.close()
        webFile.close()

if __name__ == "__main__":
    url = r'http://english-e-reader.net/download?link=brave-new-world-aldous-huxley&format=mp3'
    download_file(url, 'Test\\')
