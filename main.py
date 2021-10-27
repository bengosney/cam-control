import time

import scapy.all as scapy
from pytapo import Tapo

from config import camIPS, camPassword, camUsername, ipRange, macs

arp_req_frame = scapy.ARP(pdst=ipRange)
broadcast_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
frame = broadcast_frame / arp_req_frame


def checkForPhones():
    answered_list = scapy.srp(frame, timeout=1, verbose=False)[0]
    return all(a[1].hwsrc not in macs for a in answered_list)


def main(sleepTime=30):
    print(f"Checking for {macs}")
    previous = None

    while True:
        print("Checking phones")
        detectMotion = checkForPhones()

        if detectMotion != previous:
            print("Possible change, checking again")
            if checkForPhones() != previous:
                print(f"Setting motion detection to {detectMotion}")
                for camIP in camIPS:
                    tapo = Tapo(camIP, camUsername, camPassword)
                    tapo.setMotionDetection(detectMotion)

                previous = detectMotion

        print("Sleeping...")
        time.sleep(sleepTime)


if __name__ == "__main__":
    main()
