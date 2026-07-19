import time
import requests
import subprocess
import shutil
import os
import stem.control
from stem import Signal
from stem.control import Controller

CORE_LANG = "tr" 
CT = {
    "tr": {
        "dev": "Geliştirici: Rion",
        "privacy": "Gizlilik önemli!!!",
        "unk_ip": "Bilinmeyen IP",
        "unk_country": "Bilinmeyen Ülke",
        "unk_city": "Bilinmeyen Şehir",
        "unk_isp": "Bilinmeyen ISP",
        "ip_info": "\033[96m{ip}\033[0m ({ulke}, {sehir}) - ISP: {isp}",
        "loc_fail": "[-] Konum bilgisi alınamadı.",
        "ip_err": "[-] IP Sorgu Hatası: {e}",
        "req_ip": "ALP VPN: Yeni Tor kimliği (IP) talep ediliyor...",
        "torrc_err": "[-] torrc dosyası güncellenirken hata oluştu: {e}",
        "exit_locked": "[+] ALP VPN: Çıkış ülkesi [{country}] olarak kilitlendi.",
        "restr_removed": "[+] ALP VPN: Ülke kısıtlaması kaldırıldı (Rastgele IP modu).",
        "mac_start": "\n[*] {interface} için MAC gizleme işlemi başlatılıyor...",
        "mac_disconn": "[*] Ağ bağlantısı kesiliyor...",
        "mac_gen": "[*] Yeni sahte MAC adresi üretiliyor...",
        "mac_rest": "[*] Ağ Yöneticisi yeniden başlatılıyor. İnternetin gelmesi 5-10 saniye sürebilir...",
        "mac_succ": "\033[92m[+] BAŞARILI: {interface} fiziksel kimliği başarıyla gizlendi!\033[0m\n",
        "mac_not_found": "[-] HATA: 'macchanger' aracı sistemde bulunamadı.",
        "mac_fail": "[-] HATA: İşlem başarısız oldu. Ağ adını ({interface}) doğru yazdığınızdan emin olun.",
        "ks_emerg": "\n\033[91m[!!!] ACİL DURUM: Bağlantı koptu! {interface} üzerinde Akıllı Zırh devreye giriyor...\033[0m",
        "ks_act": "\033[92m[+] Akıllı Kill Switch Aktif! Gerçek IP sızıntısı engellendi, ağ fiziksel olarak açık.\033[0m\n",
        "ks_err": "[-] Kill Switch tetikleme hatası: {e}",
        "ks_deact_start": "[*] Akıllı Kill Switch ({interface}) kalkanı indiriliyor...",
        "ks_deact": "\033[92m[+] Zırh kaldırıldı. Ağ trafiği normale döndü (Donanım kapatılmadı).\033[0m\n",
        "ks_rm_err": "[-] Kill Switch kaldırma hatası: {e}",
        "wg_start": "\n[*] WireGuard VPN başlatılıyor ({path})...",
        "wg_act": "\033[92m[+] BAŞARILI: Tünel Aktif! Tüm trafik WireGuard'a yönlendirildi.\033[0m",
        "wg_err": "[-] HATA: WireGuard bağlantısı başlatılamadı!",
        "wg_stop": "\n[*] WireGuard VPN kapatılıyor ({path})...",
        "wg_stopped": "\033[92m[+] BAŞARILI: Tünel Kapatıldı! Normal internete dönüldü.\033[0m",
        "wg_stop_err": "[-] HATA: WireGuard bağlantısı kapatılamadı!",
        "warp_keys": "\n[*] Cloudflare WARP için kriptografik anahtarlar üretiliyor...",
        "warp_api_err": "[-] Cloudflare API Hatası: Sunucu {code} kodu döndürdü.",
        "warp_succ": "\033[92m[+] BAŞARILI: Dinamik WARP Profili oluşturuldu! (alp_warp.conf)\033[0m",
        "warp_err": "[-] HATA: WARP tüneli oluşturulamadı ({e})",
        "warp_not_found": "[-] HATA: Sistemde aktif bir ALP WARP bağlantısı algılanamadı.",
        "warp_forgot": "\n[*] WARP tüneli açık unutulmuş! Otomatik olarak kapatılıyor...",
        "net_clean": "[*] Ağ önbelleği ve rotalar temizleniyor (Lütfen bekleyin)...",
        "net_cleaned": "\033[92m[+] Ağ kalıntıları başarıyla temizlendi. Sistem normale döndü.\033[0m",
        "net_err": "[-] Ağ sıfırlanırken küçük bir sorun oluştu: {e}",
        "dns_start": "[*] DNS Sızıntı Koruması Aktifleştiriliyor...",
        "dns_err": "[-] DNS başlatma hatası: {e}",
        "dns_stop": "[*] DNS orijinal ayarlarına döndürüldü.",
        "mh_intel": "\033[93m[*] İstihbarat Koruması Aktif: {count} ülkenin düğümleri bloklandı.\033[0m",
        "mh_conf": "\033[92m[+] MULTI-HOP YAPILANDIRILDI: Giriş:[{entry}] -> Çıkış:[{exit}]\033[0m",
        "mh_err": "\033[91m[-] Multi-Hop yapılandırma hatası: {e}\033[0m",
        "test_title": "--- ALP VPN ÇEKİRDEK TESTİ ---",
        "test_cur": "Mevcut Detaylı Kimliğiniz: {info}",
        "test_new": "Yeni Detaylı Kimliğiniz: {info}"
    },
    "en": {
        "dev": "Developer: Rion",
        "privacy": "Privacy matters!!!",
        "unk_ip": "Unknown IP",
        "unk_country": "Unknown Country",
        "unk_city": "Unknown City",
        "unk_isp": "Unknown ISP",
        "ip_info": "\033[96m{ip}\033[0m ({ulke}, {sehir}) - ISP: {isp}",
        "loc_fail": "[-] Could not retrieve location information.",
        "ip_err": "[-] IP Query Error: {e}",
        "req_ip": "ALP VPN: Requesting new Tor identity (IP)...",
        "torrc_err": "[-] Error updating torrc file: {e}",
        "exit_locked": "[+] ALP VPN: Exit country locked to [{country}].",
        "restr_removed": "[+] ALP VPN: Country restriction removed (Random IP mode).",
        "mac_start": "\n[*] Starting MAC spoofing for {interface}...",
        "mac_disconn": "[*] Disconnecting network...",
        "mac_gen": "[*] Generating new fake MAC address...",
        "mac_rest": "[*] Restarting Network Manager. Internet may take 5-10 seconds to connect...",
        "mac_succ": "\033[92m[+] SUCCESS: Physical identity of {interface} successfully hidden!\033[0m\n",
        "mac_not_found": "[-] ERROR: 'macchanger' tool not found on the system.",
        "mac_fail": "[-] ERROR: Operation failed. Make sure you typed the network name ({interface}) correctly.",
        "ks_emerg": "\n\033[91m[!!!] EMERGENCY: Connection lost! Smart Armor deploying on {interface}...\033[0m",
        "ks_act": "\033[92m[+] Smart Kill Switch Active! Real IP leak prevented, hardware remains active.\033[0m\n",
        "ks_err": "[-] Kill Switch trigger error: {e}",
        "ks_deact_start": "[*] Lowering Smart Kill Switch ({interface}) shield...",
        "ks_deact": "\033[92m[+] Shield removed. Network traffic restored to normal (Hardware not disabled).\033[0m\n",
        "ks_rm_err": "[-] Kill Switch removal error: {e}",
        "wg_start": "\n[*] Starting WireGuard VPN ({path})...",
        "wg_act": "\033[92m[+] SUCCESS: Tunnel Active! All traffic routed to WireGuard.\033[0m",
        "wg_err": "[-] ERROR: Failed to start WireGuard connection!",
        "wg_stop": "\n[*] Stopping WireGuard VPN ({path})...",
        "wg_stopped": "\033[92m[+] SUCCESS: Tunnel Closed! Returned to normal internet.\033[0m",
        "wg_stop_err": "[-] ERROR: Failed to stop WireGuard connection!",
        "warp_keys": "\n[*] Generating cryptographic keys for Cloudflare WARP...",
        "warp_api_err": "[-] Cloudflare API Error: Server returned code {code}.",
        "warp_succ": "\033[92m[+] SUCCESS: Dynamic WARP Profile created! (alp_warp.conf)\033[0m",
        "warp_err": "[-] ERROR: Failed to create WARP tunnel ({e})",
        "warp_not_found": "[-] ERROR: No active ALP WARP connection detected on the system.",
        "warp_forgot": "\n[*] WARP tunnel left open! Closing automatically...",
        "net_clean": "[*] Clearing network cache and routes (Please wait)...",
        "net_cleaned": "\033[92m[+] Network residuals successfully cleared. System returned to normal.\033[0m",
        "net_err": "[-] Minor issue occurred while resetting network: {e}",
        "dns_start": "[*] Activating DNS Leak Protection...",
        "dns_err": "[-] DNS startup error: {e}",
        "dns_stop": "[*] DNS restored to original settings.",
        "mh_intel": "\033[93m[*] Intelligence Protection Active: Nodes of {count} countries blocked.\033[0m",
        "mh_conf": "\033[92m[+] MULTI-HOP CONFIGURED: Entry:[{entry}] -> Exit:[{exit}]\033[0m",
        "mh_err": "\033[91m[-] Multi-Hop configuration error: {e}\033[0m",
        "test_title": "--- ALP VPN CORE TEST ---",
        "test_cur": "Your Current Detailed Identity: {info}",
        "test_new": "Your New Detailed Identity: {info}"
    }
}

def set_language(lang_code):
    global CORE_LANG
    if lang_code in CT:
        CORE_LANG = lang_code

print(CT[CORE_LANG]["dev"])
print(CT[CORE_LANG]["privacy"])

def get_current_ip():
    time.sleep(2)
    proxies = {'http': None, 'https': None}
    try:
        response = requests.get('http://ip-api.com/json/', proxies=proxies, timeout=10)
        data = response.json() 
        
        if data.get('status') == 'success':
            ip = data.get('query', CT[CORE_LANG]["unk_ip"])
            ulke = data.get('country', CT[CORE_LANG]["unk_country"])
            sehir = data.get('city', CT[CORE_LANG]["unk_city"])
            isp = data.get('isp', CT[CORE_LANG]["unk_isp"])
            
            return CT[CORE_LANG]["ip_info"].format(ip=ip, ulke=ulke, sehir=sehir, isp=isp)
        else:
            return CT[CORE_LANG]["loc_fail"]
    except Exception as e:
        return CT[CORE_LANG]["ip_err"].format(e=e)

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
            ip = data.get('query', CT[CORE_LANG]["unk_ip"])
            ulke = data.get('country', CT[CORE_LANG]["unk_country"])
            sehir = data.get('city', CT[CORE_LANG]["unk_city"])
            isp = data.get('isp', CT[CORE_LANG]["unk_isp"])
            
            return CT[CORE_LANG]["ip_info"].format(ip=ip, ulke=ulke, sehir=sehir, isp=isp)
        else:
            return CT[CORE_LANG]["loc_fail"]
    except Exception as e:
        return CT[CORE_LANG]["ip_err"].format(e=e)

def renew_tor_ip():
    try:
        with stem.control.Controller.from_port(port=9051) as controller:
            controller.authenticate() 
            controller.signal(stem.Signal.NEWNYM)
            print(CT[CORE_LANG]["req_ip"])
            return True
    except (stem.SocketError, Exception):
        return False

def update_torrc_country(country_code=None):
    torrc_path = "/etc/tor/torrc"
    try:
        with open(torrc_path, "r") as f:
            lines = f.readlines()
        
        new_lines = [
            line for line in lines 
            if not line.strip().startswith("ExitNodes") and not line.strip().startswith("StrictNodes")
        ]
        
        if country_code:
            new_lines.append(f"ExitNodes {{{country_code.lower()}}}\n")
            new_lines.append("StrictNodes 1\n")
        
        with open(torrc_path, "w") as f:
            f.writelines(new_lines)
    except Exception as e:
        print(CT[CORE_LANG]["torrc_err"].format(e=e))

def set_tor_exit_node(country_code=None):
    update_torrc_country(country_code)
    
    try:
        import stem
        import stem.control
        with stem.control.Controller.from_port(port=9051) as controller:
            controller.authenticate()
            
            if country_code:
                formatted_code = f"{{{country_code.lower()}}}"
                controller.set_conf("ExitNodes", formatted_code)
                controller.set_conf("StrictNodes", "1")
                print(CT[CORE_LANG]["exit_locked"].format(country=country_code.upper()))
            else:
                controller.reset_conf("ExitNodes")
                controller.reset_conf("StrictNodes")
                print(CT[CORE_LANG]["restr_removed"])
                
            controller.signal(stem.Signal.NEWNYM)
            time.sleep(5) 
    except Exception:
        pass
        
def change_mac_address(interface):
    print(CT[CORE_LANG]["mac_start"].format(interface=interface))
    
    try:
        print(CT[CORE_LANG]["mac_disconn"])
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "down"], check=True)
        
        print(CT[CORE_LANG]["mac_gen"])
        subprocess.run(["sudo", "macchanger", "-r", interface], check=True, stdout=subprocess.DEVNULL)
        
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], check=True)
        
        if shutil.which("systemctl"):
            print(CT[CORE_LANG]["mac_rest"])
            subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], check=True)
            time.sleep(6) 
            
        print(CT[CORE_LANG]["mac_succ"].format(interface=interface))
        
    except FileNotFoundError:
        print(CT[CORE_LANG]["mac_not_found"])
    except subprocess.CalledProcessError:
        print(CT[CORE_LANG]["mac_fail"].format(interface=interface))
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], stderr=subprocess.DEVNULL)
        if shutil.which("systemctl"):
            subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], stderr=subprocess.DEVNULL)

def activate_kill_switch(interface):
    print(CT[CORE_LANG]["ks_emerg"].format(interface=interface))
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

        print(CT[CORE_LANG]["ks_act"])
    except Exception as e:
        print(CT[CORE_LANG]["ks_err"].format(e=e))

def deactivate_kill_switch(interface): 
    print(CT[CORE_LANG]["ks_deact_start"].format(interface=interface))
    try:
        subprocess.run(["sudo", "iptables", "-F"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-X"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "INPUT", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "OUTPUT", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "FORWARD", "ACCEPT"], capture_output=True)
        
        print(CT[CORE_LANG]["ks_deact"])
    except Exception as e:
        print(CT[CORE_LANG]["ks_rm_err"].format(e=e))

def connect_wireguard(config_path):
    print(CT[CORE_LANG]["wg_start"].format(path=config_path))
    try:
        subprocess.run(["sudo", "wg-quick", "up", config_path], check=True)
        print(CT[CORE_LANG]["wg_act"])
        secure_dns_start() 
        return True
    except subprocess.CalledProcessError:
        print(CT[CORE_LANG]["wg_err"])
        return False

def disconnect_wireguard(config_path):
    print(CT[CORE_LANG]["wg_stop"].format(path=config_path))
    try:
        subprocess.run(["sudo", "wg-quick", "down", config_path], check=True)
        print(CT[CORE_LANG]["wg_stopped"])
        secure_dns_stop()
        return True
    except subprocess.CalledProcessError:
        print(CT[CORE_LANG]["wg_stop_err"])
        return False

def connect_warp():
    print(CT[CORE_LANG]["warp_keys"])
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
            print(CT[CORE_LANG]["warp_api_err"].format(code=response.status_code))
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
            
        print(CT[CORE_LANG]["warp_succ"])
        return connect_wireguard(config_path)

    except Exception as e:
        print(CT[CORE_LANG]["warp_err"].format(e=e))
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
        print(CT[CORE_LANG]["warp_not_found"])
        return False

def is_warp_running():
    result = subprocess.run(['ip', 'link', 'show', 'alp_warp'], capture_output=True, text=True)
    return "alp_warp" in result.stdout

def stop_warp():
    if is_warp_running():
        print(CT[CORE_LANG]["warp_forgot"])
        disconnect_warp() 
        
        print(CT[CORE_LANG]["net_clean"])
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], capture_output=True)
            time.sleep(2) 
            print(CT[CORE_LANG]["net_cleaned"])
        except Exception as e:
            print(CT[CORE_LANG]["net_err"].format(e=e))
            
    else:
        config_path = os.path.abspath("alp_warp.conf")
        if os.path.exists(config_path):
            try:
                os.remove(config_path) 
            except:
                pass

def secure_dns_start():
    try:
        print(CT[CORE_LANG]["dns_start"])
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
        print(CT[CORE_LANG]["dns_err"].format(e=e))
        return False

def secure_dns_stop():
    try:
        subprocess.run(["sudo", "chattr", "-i", "/etc/resolv.conf"], capture_output=True)
        subprocess.run(["sudo", "rm", "-f", "/etc/resolv.conf"], capture_output=True)
        
        if os.path.exists("/etc/resolv.conf.alp_backup"):
            subprocess.run(["sudo", "mv", "/etc/resolv.conf.alp_backup", "/etc/resolv.conf"], capture_output=True)
        else:
            subprocess.run(["sudo", "ln", "-sf", "/run/systemd/resolve/stub-resolv.conf", "/etc/resolv.conf"], capture_output=True)
            
        print(CT[CORE_LANG]["dns_stop"])
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
                print(CT[CORE_LANG]["mh_intel"].format(count=len(blacklist)))
            else:
                controller.reset_conf("ExcludeNodes")
                
            if strict and (entry_country or exit_country or spy_protection_level > 0):
                controller.set_conf("StrictNodes", "1")
            else:
                controller.set_conf("StrictNodes", "0")
                
            controller.signal(stem.Signal.NEWNYM)
            print(CT[CORE_LANG]["mh_conf"].format(entry=entry_country, exit=exit_country))
            return True
            
    except Exception as e:
        print(CT[CORE_LANG]["mh_err"].format(e=e))
        return False

if __name__ == "__main__":
    print(CT[CORE_LANG]["test_title"])
    print(CT[CORE_LANG]["test_cur"].format(info=get_detailed_ip_info()))
    renew_tor_ip()
    print(CT[CORE_LANG]["test_new"].format(info=get_detailed_ip_info()))