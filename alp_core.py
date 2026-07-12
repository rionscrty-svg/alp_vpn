import time
import requests
import subprocess
import shutil
import os
import stem.control
from stem import Signal
from stem.control import Controller

def dil_sec():
    print("--- ALP VPN ---")
    print("Select Language / Dil Seçin:")
    print("[1] English")
    print("[2] Türkçe")
    
    secim = input("Your choice / Seçiminiz [1-2]: ")
    return "EN" if secim == "1" else "TR"

DIL = dil_sec()

MSG = {
    "TR": {
        "dev": "Geliştirici: Rion",
        "privacy": "Gizlilik önemli!!!",
        "unknown_ip": "Bilinmeyen IP",
        "unknown_country": "Bilinmeyen Ülke",
        "unknown_city": "Bilinmeyen Şehir",
        "unknown_isp": "Bilinmeyen ISP",
        "loc_fail": "[-] Konum bilgisi alınamadı.",
        "ip_err": "[-] IP Sorgu Hatası:",
        "tor_new": "ALP VPN: Yeni Tor kimliği (IP) talep ediliyor...",
        "tor_lock": "[+] ALP VPN: Çıkış ülkesi [{}] olarak kilitlendi.",
        "tor_reset": "[+] ALP VPN: Ülke kısıtlaması kaldırıldı (Rastgele IP modu).",
        "tor_err": "[-] Ülke değiştirme hatası:",
        "mac_start": "\n[*] {} için MAC gizleme işlemi başlatılıyor...",
        "mac_down": "[*] Ağ bağlantısı kesiliyor...",
        "mac_gen": "[*] Yeni sahte MAC adresi üretiliyor...",
        "mac_restart": "[*] Ağ Yöneticisi yeniden başlatılıyor. İnternetin gelmesi 5-10 saniye sürebilir...",
        "mac_success": "\033[92m[+] BAŞARILI: {} fiziksel kimliği başarıyla gizlendi!\033[0m\n",
        "mac_no_tool": "[-] HATA: 'macchanger' aracı sistemde bulunamadı.",
        "mac_fail": "[-] HATA: İşlem başarısız oldu. Ağ adını ({}) doğru yazdığınızdan emin olun.",
        "ks_active": "\n\033[91m[!!!] ACİL DURUM: Bağlantı koptu! {} üzerinde Akıllı Zırh devreye giriyor...\033[0m",
        "ks_success": "\033[92m[+] Akıllı Kill Switch Aktif! Gerçek IP sızıntısı engellendi, ağ fiziksel olarak açık.\033[0m\n",
        "ks_err": "[-] Kill Switch tetikleme hatası:",
        "ks_deact": "[*] Akıllı Kill Switch ({}) kalkanı indiriliyor...",
        "ks_deact_suc": "\033[92m[+] Zırh kaldırıldı. Ağ trafiği normale döndü (Donanım kapatılmadı).\033[0m\n",
        "ks_deact_err": "[-] Kill Switch kaldırma hatası:",
        "wg_start": "\n[*] WireGuard VPN başlatılıyor ({})...",
        "wg_success": "\033[92m[+] BAŞARILI: Tünel Aktif! Tüm trafik WireGuard'a yönlendirildi.\033[0m",
        "wg_fail": "[-] HATA: WireGuard bağlantısı başlatılamadı!",
        "wg_stop": "\n[*] WireGuard VPN kapatılıyor ({})...",
        "wg_stop_suc": "\033[92m[+] BAŞARILI: Tünel Kapatıldı! Normal internete dönüldü.\033[0m",
        "wg_stop_fail": "[-] HATA: WireGuard bağlantısı kapatılamadı!",
        "warp_keys": "\n[*] Cloudflare WARP için kriptografik anahtarlar üretiliyor...",
        "warp_api_err": "[-] Cloudflare API Hatası: Sunucu {} kodu döndürdü.",
        "warp_suc": "\033[92m[+] BAŞARILI: Dinamik WARP Profili oluşturuldu! (alp_warp.conf)\033[0m",
        "warp_err": "[-] HATA: WARP tüneli oluşturulamadı ({})",
        "warp_not_found": "[-] HATA: Sistemde aktif bir ALP WARP bağlantısı algılanamadı.",
        "warp_forgotten": "\n[*] WARP tüneli açık unutulmuş! Otomatik olarak kapatılıyor...",
        "warp_clean": "[*] Ağ önbelleği ve rotalar temizleniyor (Lütfen bekleyin)...",
        "warp_clean_suc": "\033[92m[+] Ağ kalıntıları başarıyla temizlendi. Sistem normale döndü.\033[0m",
        "warp_clean_err": "[-] Ağ sıfırlanırken küçük bir sorun oluştu:",
        "dns_start": "[*] DNS Sızıntı Koruması Aktifleştiriliyor...",
        "dns_start_err": "[-] DNS başlatma hatası:",
        "dns_stop": "[*] DNS orijinal ayarlarına döndürüldü.",
        "multi_spy": "\033[93m[*] İstihbarat Koruması Aktif: {} ülkenin düğümleri bloklandı.\033[0m",
        "multi_hop": "\033[92m[+] MULTI-HOP YAPILANDIRILDI: Giriş:[{}] -> Çıkış:[{}]\033[0m",
        "multi_err": "\033[91m[-] Multi-Hop yapılandırma hatası: {}\033[0m",
        "test_title": "--- ALP VPN ÇEKİRDEK TESTİ ---",
        "test_curr": "Mevcut Detaylı Kimliğiniz:",
        "test_new": "Yeni Detaylı Kimliğiniz:"
    },
    "EN": {
        "dev": "Developer: Rion",
        "privacy": "Privacy matters!!!",
        "unknown_ip": "Unknown IP",
        "unknown_country": "Unknown Country",
        "unknown_city": "Unknown City",
        "unknown_isp": "Unknown ISP",
        "loc_fail": "[-] Failed to retrieve location info.",
        "ip_err": "[-] IP Query Error:",
        "tor_new": "ALP VPN: Requesting new Tor identity (IP)...",
        "tor_lock": "[+] ALP VPN: Exit node locked to [{}].",
        "tor_reset": "[+] ALP VPN: Country restriction lifted (Random IP mode).",
        "tor_err": "[-] Error changing country:",
        "mac_start": "\n[*] Starting MAC spoofing for {}...",
        "mac_down": "[*] Disconnecting network...",
        "mac_gen": "[*] Generating new fake MAC address...",
        "mac_restart": "[*] Restarting Network Manager. Internet may take 5-10 seconds to connect...",
        "mac_success": "\033[92m[+] SUCCESS: Physical identity for {} successfully hidden!\033[0m\n",
        "mac_no_tool": "[-] ERROR: 'macchanger' tool not found on the system.",
        "mac_fail": "[-] ERROR: Operation failed. Make sure the interface name ({}) is correct.",
        "ks_active": "\n\033[91m[!!!] EMERGENCY: Connection lost! Deploying Smart Armor on {}...\033[0m",
        "ks_success": "\033[92m[+] Smart Kill Switch Active! Real IP leak prevented, network physically open.\033[0m\n",
        "ks_err": "[-] Kill switch deployment error:",
        "ks_deact": "[*] Removing Smart Kill Switch ({}) armor...",
        "ks_deact_suc": "\033[92m[+] Armor removed. Network traffic returned to normal (Hardware not disabled).\033[0m\n",
        "ks_deact_err": "[-] Armor removal error:",
        "wg_start": "\n[*] Starting WireGuard VPN ({})...",
        "wg_success": "\033[92m[+] SUCCESS: Tunnel Active! All traffic routed through WireGuard.\033[0m",
        "wg_fail": "[-] ERROR: Failed to start WireGuard connection!",
        "wg_stop": "\n[*] Stopping WireGuard VPN ({})...",
        "wg_stop_suc": "\033[92m[+] SUCCESS: Tunnel Closed! Returned to normal internet.\033[0m",
        "wg_stop_fail": "[-] ERROR: Failed to close WireGuard connection!",
        "warp_keys": "\n[*] Generating cryptographic keys for Cloudflare WARP...",
        "warp_api_err": "[-] Cloudflare API Error: Server returned code {}.",
        "warp_suc": "\033[92m[+] SUCCESS: Dynamic WARP Profile created! (alp_warp.conf)\033[0m",
        "warp_err": "[-] ERROR: Failed to create WARP tunnel ({})",
        "warp_not_found": "[-] ERROR: No active ALP WARP connection detected on system.",
        "warp_forgotten": "\n[*] WARP tunnel left open! Closing automatically...",
        "warp_clean": "[*] Cleaning network cache and routes (Please wait)...",
        "warp_clean_suc": "\033[92m[+] Network remains successfully cleaned. System back to normal.\033[0m",
        "warp_clean_err": "[-] Minor issue while resetting network:",
        "dns_start": "[*] Activating DNS Leak Protection...",
        "dns_start_err": "[-] DNS activation error:",
        "dns_stop": "[*] DNS restored to original settings.",
        "multi_spy": "\033[93m[*] Intelligence Protection Active: Nodes from {} countries blocked.\033[0m",
        "multi_hop": "\033[92m[+] MULTI-HOP CONFIGURED: Entry:[{}] -> Exit:[{}]\033[0m",
        "multi_err": "\033[91m[-] Multi-Hop configuration error: {}\033[0m",
        "test_title": "--- ALP VPN CORE TEST ---",
        "test_curr": "Current Detailed Identity:",
        "test_new": "New Detailed Identity:"
    }
}
# =========================================================

print(MSG[DIL]["dev"])
print(MSG[DIL]["privacy"])

def get_current_ip():
    time.sleep(2)
    proxies = {'http': None, 'https': None} 
    try:
        response = requests.get('http://ip-api.com/json/', proxies=proxies, timeout=10)
        data = response.json() 
        
        if data.get('status') == 'success':
            ip = data.get('query', MSG[DIL]["unknown_ip"])
            ulke = data.get('country', MSG[DIL]["unknown_country"])
            sehir = data.get('city', MSG[DIL]["unknown_city"])
            isp = data.get('isp', MSG[DIL]["unknown_isp"])
            
            return f"\033[96m{ip}\033[0m ({ulke}, {sehir}) - ISP: {isp}"
        else:
            return MSG[DIL]["loc_fail"]
    except Exception as e:
        return f"{MSG[DIL]['ip_err']} {e}"

def get_detailed_ip_info():
    time.sleep(2)
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        response = requests.get('http://ip-api.com/json/', proxies=proxies, timeout=10)
        data = response.json() 
        
        if data.get('status') == 'success':
            ip = data.get('query', MSG[DIL]["unknown_ip"])
            ulke = data.get('country', MSG[DIL]["unknown_country"])
            sehir = data.get('city', MSG[DIL]["unknown_city"])
            isp = data.get('isp', MSG[DIL]["unknown_isp"])
            
            return f"\033[96m{ip}\033[0m ({ulke}, {sehir}) - ISP: {isp}"
        else:
            return MSG[DIL]["loc_fail"]
    except Exception as e:
        return f"{MSG[DIL]['ip_err']} {e}"

def renew_tor_ip():
    try:
        with stem.control.Controller.from_port(port=9051) as controller:
            controller.authenticate() 
            controller.signal(stem.Signal.NEWNYM)
            print(MSG[DIL]["tor_new"])
            return True
    except (stem.SocketError, Exception):
        return False

def set_tor_exit_node(country_code=None):
    try:
        with stem.control.Controller.from_port(port=9051) as controller:
            controller.authenticate()
            
            if country_code:
                formatted_code = f"{{{country_code.lower()}}}"
                controller.set_conf("ExitNodes", formatted_code)
                controller.set_conf("StrictNodes", "1")
                print(MSG[DIL]["tor_lock"].format(country_code.upper()))
            else:
                controller.reset_conf("ExitNodes")
                controller.reset_conf("StrictNodes")
                print(MSG[DIL]["tor_reset"])
                
            controller.signal(Signal.NEWNYM)
            time.sleep(5) 
    except Exception as e:
        print(f"{MSG[DIL]['tor_err']} {e}")
        
def change_mac_address(interface):
    print(MSG[DIL]["mac_start"].format(interface))
    try:
        print(MSG[DIL]["mac_down"])
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "down"], check=True)
        
        print(MSG[DIL]["mac_gen"])
        subprocess.run(["sudo", "macchanger", "-r", interface], check=True, stdout=subprocess.DEVNULL)
        
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], check=True)
        
        if shutil.which("systemctl"):
            print(MSG[DIL]["mac_restart"])
            subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], check=True)
            time.sleep(6) 
            
        print(MSG[DIL]["mac_success"].format(interface))
        
    except FileNotFoundError:
        print(MSG[DIL]["mac_no_tool"])
    except subprocess.CalledProcessError:
        print(MSG[DIL]["mac_fail"].format(interface))
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], stderr=subprocess.DEVNULL)
        if shutil.which("systemctl"):
            subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], stderr=subprocess.DEVNULL)

def activate_kill_switch(interface):
    print(MSG[DIL]["ks_active"].format(interface))
    try:
        subprocess.run(["sudo", "iptables", "-F"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "OUTPUT", "DROP"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "INPUT", "DROP"], capture_output=True)
        
        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-o", "lo", "-j", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-i", "lo", "-j", "ACCEPT"], capture_output=True)
        
        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-p", "udp", "--dport", "67", "--sport", "68", "-j", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "udp", "--dport", "68", "--sport", "67", "-j", "ACCEPT"], capture_output=True)
        
        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-m", "owner", "--uid-owner", "toranon", "-j", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-m", "owner", "--uid-owner", "debian-tor", "-j", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"], capture_output=True)

        print(MSG[DIL]["ks_success"])
    except Exception as e:
        print(f"{MSG[DIL]['ks_err']} {e}")

def deactivate_kill_switch(interface): 
    print(MSG[DIL]["ks_deact"].format(interface))
    try:
        subprocess.run(["sudo", "iptables", "-F"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-X"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "INPUT", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "OUTPUT", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "FORWARD", "ACCEPT"], capture_output=True)
        
        print(MSG[DIL]["ks_deact_suc"])
    except Exception as e:
        print(f"{MSG[DIL]['ks_deact_err']} {e}")

def connect_wireguard(config_path):
    print(MSG[DIL]["wg_start"].format(config_path))
    try:
        subprocess.run(["sudo", "wg-quick", "up", config_path], check=True)
        print(MSG[DIL]["wg_success"])
        secure_dns_start() 
        return True
    except subprocess.CalledProcessError:
        print(MSG[DIL]["wg_fail"])
        return False

def disconnect_wireguard(config_path):
    print(MSG[DIL]["wg_stop"].format(config_path))
    try:
        subprocess.run(["sudo", "wg-quick", "down", config_path], check=True)
        print(MSG[DIL]["wg_stop_suc"])
        secure_dns_stop()
        return True
    except subprocess.CalledProcessError:
        print(MSG[DIL]["wg_stop_fail"])
        return False

def connect_warp():
    print(MSG[DIL]["warp_keys"])
    try:
        privkey = subprocess.check_output(["wg", "genkey"]).decode("utf-8").strip()
        p = subprocess.Popen(["wg", "pubkey"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        pubkey, _ = p.communicate(input=privkey)
        pubkey = pubkey.strip()

        url = "https://api.cloudflareclient.com/v0a884/reg"
        headers = {
            "User-Agent": "okhttp/3.12.1",
            "CF-Client-Version": "a-6.11-3305",
            "Content-Type": "application/json"
        }
        payload = {
            "key": pubkey, "install_id": "", "fcm_token": "",
            "tos": "2024-01-01T00:00:00.000+00:00", "type": "Android", "locale": "en_US"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code != 200:
            print(MSG[DIL]["warp_api_err"].format(response.status_code))
            return False
            
        data = response.json()
        v4_addr = data["config"]["interface"]["addresses"]["v4"]
        v6_addr = data["config"]["interface"]["addresses"]["v6"]
        peer_pubkey = data["config"]["peers"][0]["public_key"]
        endpoint = data["config"]["peers"][0]["endpoint"]["host"]
        if ":" not in endpoint:
            endpoint += ":2408"

        config_path = os.path.abspath("alp_warp.conf")
        
        warp_config = f"""[Interface]
PrivateKey = {privkey}
Address = {v4_addr}/32
DNS = 1.1.1.1, 1.0.0.1
MTU = 1280

[Peer]
PublicKey = {peer_pubkey}
Endpoint = {endpoint}
AllowedIPs = 0.0.0.0/0
"""
        with open(config_path, "w") as f:
            f.write(warp_config)
            
        print(MSG[DIL]["warp_suc"])
        return connect_wireguard(config_path)

    except Exception as e:
        print(MSG[DIL]["warp_err"].format(e))
        return False

def disconnect_warp():
    config_path = os.path.abspath("alp_warp.conf")
    if os.path.exists(config_path):
        success = disconnect_wireguard(config_path)
        try:
            os.remove(config_path) 
        except:
            pass
        return success
    else:
        print(MSG[DIL]["warp_not_found"])
        return False

def is_warp_running():
    result = subprocess.run(['ip', 'link', 'show', 'alp_warp'], capture_output=True, text=True)
    return "alp_warp" in result.stdout

def stop_warp():
    if is_warp_running():
        print(MSG[DIL]["warp_forgotten"])
        disconnect_warp() 
        
        print(MSG[DIL]["warp_clean"])
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], capture_output=True)
            time.sleep(2) 
            print(MSG[DIL]["warp_clean_suc"])
        except Exception as e:
            print(f"{MSG[DIL]['warp_clean_err']} {e}")
            
    else:
        config_path = os.path.abspath("alp_warp.conf")
        if os.path.exists(config_path):
            try:
                os.remove(config_path) 
            except:
                pass

def secure_dns_start():
    try:
        print(MSG[DIL]["dns_start"])
        subprocess.run(["sudo", "chattr", "-i", "/etc/resolv.conf"], capture_output=True)
        subprocess.run(["sudo", "cp", "-a", "/etc/resolv.conf", "/etc/resolv.conf.alp_backup"], capture_output=True)
        subprocess.run(["sudo", "rm", "-f", "/etc/resolv.conf"], capture_output=True)
        
        dns_content = "nameserver 1.1.1.1\nnameserver 9.9.9.9\n"
        with open("/tmp/resolv.conf.tmp", "w") as f:
            f.write(dns_content)
            
        subprocess.run(["sudo", "mv", "/tmp/resolv.conf.tmp", "/etc/resolv.conf"], capture_output=True)
        res = subprocess.run(["sudo", "chattr", "+i", "/etc/resolv.conf"], capture_output=True)
        
        return res.returncode == 0
    except Exception as e:
        print(f"{MSG[DIL]['dns_start_err']} {e}")
        return False

def secure_dns_stop():
    try:
        subprocess.run(["sudo", "chattr", "-i", "/etc/resolv.conf"], capture_output=True)
        subprocess.run(["sudo", "rm", "-f", "/etc/resolv.conf"], capture_output=True)
        
        if os.path.exists("/etc/resolv.conf.alp_backup"):
            subprocess.run(["sudo", "mv", "/etc/resolv.conf.alp_backup", "/etc/resolv.conf"], capture_output=True)
        else:
            subprocess.run(["sudo", "ln", "-sf", "/run/systemd/resolve/stub-resolv.conf", "/etc/resolv.conf"], capture_output=True)
            
        print(MSG[DIL]["dns_stop"])
        return True
    except Exception as e:
        return False

def configure_multihop_circuit(entry_country=None, exit_country=None, strict=True, spy_protection_level=0):
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            
            if entry_country:
                controller.set_conf("EntryNodes", f"{{{entry_country.lower()}}}")
            else:
                controller.reset_conf("EntryNodes")
                
            if exit_country:
                controller.set_conf("ExitNodes", f"{{{exit_country.lower()}}}")
            else:
                controller.reset_conf("ExitNodes")
            
            if spy_protection_level > 0:
                five_eyes = ["US", "GB", "CA", "AU", "NZ"]
                fourteen_eyes = five_eyes + ["DK", "FR", "NL", "NO", "DE", "IT", "BE", "SE", "ES"]
                
                blacklist = list(fourteen_eyes) if spy_protection_level == 2 else list(five_eyes)
                
                if entry_country and entry_country.upper() in blacklist:
                    blacklist.remove(entry_country.upper())
                if exit_country and exit_country.upper() in blacklist:
                    blacklist.remove(exit_country.upper())
                    
                exclude_str = ",".join([f"{{{c.lower()}}}" for c in blacklist])
                controller.set_conf("ExcludeNodes", exclude_str)
                print(MSG[DIL]["multi_spy"].format(len(blacklist)))
            else:
                controller.reset_conf("ExcludeNodes")
                
            if strict and (entry_country or exit_country or spy_protection_level > 0):
                controller.set_conf("StrictNodes", "1")
            else:
                controller.set_conf("StrictNodes", "0")
                
            controller.signal(stem.Signal.NEWNYM)
            print(MSG[DIL]["multi_hop"].format(entry_country, exit_country))
            return True
            
    except Exception as e:
        print(MSG[DIL]["multi_err"].format(e))
        return False

if __name__ == "__main__":
    print(MSG[DIL]["test_title"])
    print(f"{MSG[DIL]['test_curr']} {get_detailed_ip_info()}")
    renew_tor_ip()
    print(f"{MSG[DIL]['test_new']} {get_detailed_ip_info()}")