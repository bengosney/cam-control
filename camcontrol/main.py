import time
from datetime import datetime

import scapy.all as scapy
from pytapo import Tapo

from .config import camIPS, camPassword, camUsername, ipRange, macs

arp_req_frame = scapy.ARP(pdst=ipRange)
broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
frame = broadcast_frame / arp_req_frame


def checkForPhones():
    answered_list = scapy.srp(frame, timeout=1, verbose=False)[0]
    return all(a[1].hwsrc not in macs for a in answered_list)


def logLine(line):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    print(f"{date_time:}: {line}")


def main(sleepTime=30):
    logLine(f"Checking for {macs}")
    previous = None

    while True:
        logLine("Checking phones")
        detectMotion = checkForPhones()

        if detectMotion != previous:
            logLine(f"Possible change to {detectMotion}, checking again")
            if checkForPhones() != previous:
                logLine(f"Setting motion detection to {detectMotion}")
                for camIP in camIPS:
                    tapo = Tapo(camIP, camUsername, camPassword)
                    tapo.setMotionDetection(detectMotion)

                previous = detectMotion

        logLine("Sleeping...")
        time.sleep(sleepTime)


if __name__ == "__main__":
    main()
