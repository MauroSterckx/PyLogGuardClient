import os

logPath = "/var/log/"
logFiles = ["auth.log", "syslog", "journal", "kern.log", "boot.log"]
bookmark = "bookmark.txt"


def readlog(file):
    # check if bookmark exists
    if os.path.exists(bookmark):
        with open(bookmark, "r") as f:
            lastRead = f.read()
    else:
        lastRead = 0

    # read log file
    try:
        with open(logPath + file, "r") as f:
            # skip lines already read in previous run
            for _ in range(lastRead):
                next(f)
            # read remaining lines
            data = f.read()

            # send data to server
            # TODO

            # update bookmark
            with open(bookmark, "w") as bookmarkFile:
                bookmarkFile.write(str(lastRead + data.count("\n")))

    except Exception as e:
        print(e)
