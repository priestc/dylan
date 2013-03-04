import os
import sys
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

def get_duration_from_exiftool(out):
    """
    Parse the output of exiftool to get the duration in seconds.
    """
    for line in out.split("\n"):
        if line.startswith("Duration"):
            splitted = line.split(":")
            hours, minutes, seconds = splitted[1:4]
            if seconds.endswith("(approx)"):
                seconds = seconds[:-8]
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)

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
            out = check_output(["exiftool", f])
            duration = get_duration_from_exiftool(out)
        elif f.endswith(".wav"):
            upload_file = f[:-3] + "ogg"
            call(["oggenc", "-o%s" % upload_file, "-q5", f])
            out = check_output(["ogginfo", upload_file])
            duration = get_duration_from_ogginfo(out)
            delete = True
        elif f.endswith(".ogg"):
            upload_file = f
            delete = False
        else:
            print "skipping:", f
            continue

        call([
            "s3cmd", "put", "--acl-public",
            "--add-header=X-Content-Duration:%s" % duration, upload_file,
            "s3://%s/%s" % (bucket_name, folder)
        ])

        if delete:
            os.remove(upload_file)