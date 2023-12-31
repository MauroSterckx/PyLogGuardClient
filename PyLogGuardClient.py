import os
import json
import requests
from datetime import datetime

logPath = "/var/log/"
logFiles = ["auth.log", "syslog", "journal", "kern.log", "boot.log"]


def readlog(file):
    # check if bookmark exists
    bookmark = f"bookmark_{file}.txt"
    if os.path.exists(bookmark):
        with open(bookmark, "r") as f:
            lastRead = int(f.read())
    else:
        lastRead = 0

    # read log file
    try:
        with open(logPath + file, "r") as f:
            # skip lines already read in previous run
            for _ in range(lastRead):
                next(f)
            # read remaining lines
            for line in f:
                # send each line to server
                sendLog(line, file)

            # update bookmark
            with open(bookmark, "w") as bookmarkFile:
                bookmarkFile.write(str(lastRead + sum(1 for _ in f)))

    except Exception as e:
        print(e)
        # TODO send error to server


def sendLog(data, filename):
    # read server address from config file
    with open("API_data.json", "r") as f:
        api_data = json.load(f)
    server = api_data["server_ip"]

    # convert log data to json
    data_parts = data.split(" ")  # split data with spaces
    last_colon = data.rfind(":")  # find last colon in data

    logDate = f"{data_parts[0]} {data_parts[1]} : {data_parts[2]}"  # Month Day time
    logHost = data_parts[3]  # Hostname
    logType = filename  # Log type = filename
    log_Msg = data[
        last_colon + 1 :
    ].strip()  # Message = everything after last colon and strip whitepace in beginning

    log = {"date": logDate, "device": logHost, "type": logType, "msg": log_Msg}

    # send log to server
    res = requests.post(f"{server}/addTemp", json=log)

    if res.status_code == 200:
        print("Log sent successfully")
    else:
        print(res.text)


def sendOwnLog(data, logtype, hostname):
    with open("API_data.json", "r") as f:
        api_data = json.load(f)
    server = api_data["server_ip"]

    logDate = datetime.now().strftime("%b %d %H:%M:%S")
    logHost = hostname
    logType = logtype
    log_Msg = data

    log = {"date": logDate, "device": logHost, "type": logType, "msg": log_Msg}

    # send log to server
    res = requests.post(f"{server}/addTemp", json=log)

    if res.status_code == 200:
        print("Log sent successfully")
    else:
        print(res.text)


def checkLogs():
    for file in logFiles:
        readlog(file)


def serverReachable():
    # read server address from config file
    with open("API_data.json", "r") as f:
        api_data = json.load(f)
    server = api_data["server_ip"]

    try:
        # send a GET request to the server
        response = requests.get(server)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False


if __name__ == "__main__":
    if serverReachable():
        checkLogs()
    else:
        print("Server not reachable")
        # TODO send error to server + save log to file and send later
