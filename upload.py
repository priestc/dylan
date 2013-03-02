import os
import sys
import StringIO
from subprocess import check_output, call
from boto.s3.connection import S3Connection
from boto.s3.key import Key

def get_duration_from_ogginfo(out):
    """
    Extract the number of seconds an ogg file is from the output of the
    ogginfo command. 
    """
    for line in out.split("\n"):
        if not line.strip().startswith("Playback length"):
            continue
        length = line[18:] # "5m:23.342s"

    minutes, seconds = length.split("m:")
    seconds = seconds[:-1]
    return int(minutes) * 60 + float(seconds)


if __name__ == '__main__':
    # usage: python upload.py *.flac bucket_name folder_name
    bucket_name = sys.argv[-2]
    folder = sys.argv[-1]
    if not folder.endswith("/"):
        folder += "/"

    conn = S3Connection()
    bucket = conn.get_bucket(bucket_name)
    files = sys.argv[1:-2]

    for f in files:
        delete = False
        if f.endswith(".flac"):
            upload_file = f[:-4] + "ogg"
            delete = True
            call(["oggenc", "-o%s" % upload_file, "-q5", f])
            out = check_output(["ogginfo", upload_file])
            duration = get_duration_from_ogginfo(out)
        elif f.endswith(".shn"):
            upload_file = f[:-3] + "ogg"
            intermediate = f[:-3] + "wav"
            call(["shorten", "-x", f]) # uncompress
            call(["oggenc", "-o%s" % upload_file, "-q5", intermediate])
            call(["shorten", intermediate]) # recompress
            out = check_output(["ogginfo", upload_file])
            duration = get_duration_from_ogginfo(out)
            delete = True
        elif f.endswith('.mp3'):
            upload_file = f
            delete = False
        elif f.endswith(".ogg"):
            upload_file = f
            delete = False
        else:
            print "skipping:", f
            continue

        key = Key(bucket)
        key.key = folder + upload_file
        key.set_metadata("X-Content-Duration", "%.2f" % duration)
        key.set_contents_from_filename(upload_file)
        key.set_acl('public-read')

        if delete:
            os.remove(upload_file)