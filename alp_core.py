import time
import requests
import subprocess
import shutil
import os
import stem.control
from stem import Signal
from stem.control import Controller

print("Geliştirici: Rion")
print("Gizlilik önemli!!!")

# ESKİ FONKSİYON: Sadece ham IP adresini döner (WARP gibi tüm sistemi kaplayan ağlar için)
def get_current_ip():
    time.sleep(2)
    proxies = {'http': None, 'https': None} # Tor'u atla, sistemin ana ağından çık (WARP testleri için)
    try:
        response = requests.get('http://ip-api.com/json/', proxies=proxies, timeout=10)
        data = response.json() 
        
        if data.get('status') == 'success':
            ip = data.get('query', 'Bilinmeyen IP')
            ulke = data.get('country', 'Bilinmeyen Ülke')
            sehir = data.get('city', 'Bilinmeyen Şehir')
            isp = data.get('isp', 'Bilinmeyen ISP')
            
            return f"\033[96m{ip}\033[0m ({ulke}, {sehir}) - ISP: {isp}"
        else:
            return "[-] Konum bilgisi alınamadı."
    except Exception as e:
        return f"[-] IP Sorgu Hatası: {e}"

# YENİ FONKSİYON: IP'yi analiz edip konum bilgisi döner (SADECE TOR AĞI İÇİN)
def get_detailed_ip_info():
    time.sleep(2)
    # Sadece bu fonksiyon Tor portundan çıkar! (Ghost mode ve Custom Mode için)
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        response = requests.get('http://ip-api.com/json/', proxies=proxies, timeout=10)
        data = response.json() 
        
        if data.get('status') == 'success':
            ip = data.get('query', 'Bilinmeyen IP')
            ulke = data.get('country', 'Bilinmeyen Ülke')
            sehir = data.get('city', 'Bilinmeyen Şehir')
            isp = data.get('isp', 'Bilinmeyen ISP')
            
            return f"\033[96m{ip}\033[0m ({ulke}, {sehir}) - ISP: {isp}"
        else:
            return "[-] Konum bilgisi alınamadı."
    except Exception as e:
        return f"[-] IP Sorgu Hatası: {e}"

# IP DEĞİŞTİRME MOTORU
def renew_tor_ip():
    """Tor ağına yeni bir kimlik (IP) sinyali gönderir."""
    try:
        with stem.control.Controller.from_port(port=9051) as controller:
            controller.authenticate() 
            controller.signal(stem.Signal.NEWNYM)
            print("ALP VPN: Yeni Tor kimliği (IP) talep ediliyor...")
            return True
    except (stem.SocketError, Exception):
        return False

def set_tor_exit_node(country_code=None):
    """
    Tor çıkış düğümünü belirli bir ülkeye sabitler.
    Eğer None girilirse kısıtlamayı kaldırır (rastgele ülkeye döner).
    """
    try:
        with stem.control.Controller.from_port(port=9051) as controller:
            controller.authenticate()
            
            if country_code:
                formatted_code = f"{{{country_code.lower()}}}"
                controller.set_conf("ExitNodes", formatted_code)
                controller.set_conf("StrictNodes", "1")
                print(f"[+] ALP VPN: Çıkış ülkesi [{country_code.upper()}] olarak kilitlendi.")
            else:
                controller.reset_conf("ExitNodes")
                controller.reset_conf("StrictNodes")
                print("[+] ALP VPN: Ülke kısıtlaması kaldırıldı (Rastgele IP modu).")
                
            controller.signal(Signal.NEWNYM)
            time.sleep(5) # ZAMANLAMA 5 SANİYEYE ÇIKARILDI (Tor'un kilitleri tam kavraması için)
    except Exception as e:
        print(f"[-] Ülke değiştirme hatası: {e}")
        
def change_mac_address(interface):
    """Ağ yöneticisine reset atarak çalışan kesin MAC gizleme fonksiyonu."""
    print(f"\n[*] {interface} için MAC gizleme işlemi başlatılıyor...")
    
    try:
        print("[*] Ağ bağlantısı kesiliyor...")
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "down"], check=True)
        
        print("[*] Yeni sahte MAC adresi üretiliyor...")
        subprocess.run(["sudo", "macchanger", "-r", interface], check=True, stdout=subprocess.DEVNULL)
        
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], check=True)
        
        if shutil.which("systemctl"):
            print("[*] Ağ Yöneticisi yeniden başlatılıyor. İnternetin gelmesi 5-10 saniye sürebilir...")
            subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], check=True)
            time.sleep(6) 
            
        print(f"\033[92m[+] BAŞARILI: {interface} fiziksel kimliği başarıyla gizlendi!\033[0m\n")
        
    except FileNotFoundError:
        print("[-] HATA: 'macchanger' aracı sistemde bulunamadı.")
    except subprocess.CalledProcessError:
        print(f"[-] HATA: İşlem başarısız oldu. Ağ adını ({interface}) doğru yazdığınızdan emin olun.")
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], stderr=subprocess.DEVNULL)
        if shutil.which("systemctl"):
            subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], stderr=subprocess.DEVNULL)

# akıllı killswitch zırhı
def activate_kill_switch(interface):
    """Ağı fiziksel olarak kapatmak yerine IPTables ile anında kilitler (Akıllı Zırh)."""
    print(f"\n\033[91m[!!!] ACİL DURUM: Bağlantı koptu! {interface} üzerinde Akıllı Zırh devreye giriyor...\033[0m")
    try:
        # Eski kuralları temizle ve her şeyi yasakla
        subprocess.run(["sudo", "iptables", "-F"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "OUTPUT", "DROP"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "INPUT", "DROP"], capture_output=True)
        
        # 1. Localhost serbest
        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-o", "lo", "-j", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-i", "lo", "-j", "ACCEPT"], capture_output=True)
        
        # 2. DHCP İzni: Modemden IP alınabilmesi için UDP 67/68 serbest
        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-p", "udp", "--dport", "67", "--sport", "68", "-j", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "udp", "--dport", "68", "--sport", "67", "-j", "ACCEPT"], capture_output=True)
        
        # 3. Tor İzni (Hem Debian/Kali hem de Fedora için ikisini de ekliyoruz)
        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-m", "owner", "--uid-owner", "toranon", "-j", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-m", "owner", "--uid-owner", "debian-tor", "-j", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"], capture_output=True)

        print(f"\033[92m[+] Akıllı Kill Switch Aktif! Gerçek IP sızıntısı engellendi, ağ fiziksel olarak açık.\033[0m\n")
    except Exception as e:
        print(f"[-] Kill Switch tetikleme hatası: {e}")

def deactivate_kill_switch(interface): 
    """Akıllı zırhı (IPTables kilitlerini) kaldırır ve ağı serbest bırakır."""
    print(f"[*] Akıllı Kill Switch ({interface}) kalkanı indiriliyor...")
    try:
        subprocess.run(["sudo", "iptables", "-F"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-X"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "INPUT", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "OUTPUT", "ACCEPT"], capture_output=True)
        subprocess.run(["sudo", "iptables", "-P", "FORWARD", "ACCEPT"], capture_output=True)
        
        print(f"\033[92m[+] Zırh kaldırıldı. Ağ trafiği normale döndü (Donanım kapatılmadı).\033[0m\n")
    except Exception as e:
        print(f"[-] Kill Switch kaldırma hatası: {e}")

# hızlı internet wireguard için (kapatma)
def connect_wireguard(config_path):
    print(f"\n[*] WireGuard VPN başlatılıyor ({config_path})...")
    try:
        subprocess.run(["sudo", "wg-quick", "up", config_path], check=True)
        print("\033[92m[+] BAŞARILI: Tünel Aktif! Tüm trafik WireGuard'a yönlendirildi.\033[0m")
        secure_dns_start() 
        return True
    except subprocess.CalledProcessError:
        print("[-] HATA: WireGuard bağlantısı başlatılamadı!")
        return False

def disconnect_wireguard(config_path):
    print(f"\n[*] WireGuard VPN kapatılıyor ({config_path})...")
    try:
        subprocess.run(["sudo", "wg-quick", "down", config_path], check=True)
        print("\033[92m[+] BAŞARILI: Tünel Kapatıldı! Normal internete dönüldü.\033[0m")
        secure_dns_stop()
        return True
    except subprocess.CalledProcessError:
        print("[-] HATA: WireGuard bağlantısı kapatılamadı!")
        return False

# beyin takımı Cloudflare
def connect_warp():
    """Cloudflare API'sinden dinamik WireGuard profili üretir ve bağlanır."""
    print("\n[*] Cloudflare WARP için kriptografik anahtarlar üretiliyor...")
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
            print(f"[-] Cloudflare API Hatası: Sunucu {response.status_code} kodu döndürdü.")
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
            
        print("\033[92m[+] BAŞARILI: Dinamik WARP Profili oluşturuldu! (alp_warp.conf)\033[0m")
        return connect_wireguard(config_path)

    except Exception as e:
        print(f"[-] HATA: WARP tüneli oluşturulamadı ({e})")
        return False

def disconnect_warp():
    """Aktif WARP bağlantısını kapatır ve geçici profili siler."""
    config_path = os.path.abspath("alp_warp.conf")
    if os.path.exists(config_path):
        success = disconnect_wireguard(config_path)
        try:
            os.remove(config_path) 
        except:
            pass
        return success
    else:
        print("[-] HATA: Sistemde aktif bir ALP WARP bağlantısı algılanamadı.")
        return False

def is_warp_running():
    result = subprocess.run(['ip', 'link', 'show', 'alp_warp'], capture_output=True, text=True)
    return "alp_warp" in result.stdout

def stop_warp():
    """Kullanıcı aniden çıkış yaptığında (Ctrl+C veya Exit) tüneli güvenle kapatır ve ağı temizler."""
    if is_warp_running():
        print("\n[*] WARP tüneli açık unutulmuş! Otomatik olarak kapatılıyor...")
        disconnect_warp() 
        
        print("[*] Ağ önbelleği ve rotalar temizleniyor (Lütfen bekleyin)...")
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], capture_output=True)
            time.sleep(2) 
            print("\033[92m[+] Ağ kalıntıları başarıyla temizlendi. Sistem normale döndü.\033[0m")
        except Exception as e:
            print(f"[-] Ağ sıfırlanırken küçük bir sorun oluştu: {e}")
            
    else:
        config_path = os.path.abspath("alp_warp.conf")
        if os.path.exists(config_path):
            try:
                os.remove(config_path) 
            except:
                pass

def secure_dns_start():
    try:
        print("[*] DNS Sızıntı Koruması Aktifleştiriliyor...")
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
        print(f"[-] DNS başlatma hatası: {e}")
        return False

def secure_dns_stop():
    try:
        subprocess.run(["sudo", "chattr", "-i", "/etc/resolv.conf"], capture_output=True)
        subprocess.run(["sudo", "rm", "-f", "/etc/resolv.conf"], capture_output=True)
        
        if os.path.exists("/etc/resolv.conf.alp_backup"):
            subprocess.run(["sudo", "mv", "/etc/resolv.conf.alp_backup", "/etc/resolv.conf"], capture_output=True)
        else:
            subprocess.run(["sudo", "ln", "-sf", "/run/systemd/resolve/stub-resolv.conf", "/etc/resolv.conf"], capture_output=True)
            
        print("[*] DNS orijinal ayarlarına döndürüldü.")
        return True
    except Exception as e:
        return False

def configure_multihop_circuit(entry_country=None, exit_country=None, strict=True, spy_protection_level=0):
    """
    Tor düğümlerini yapılandırır ve opsiyonel olarak istihbarat ittifaklarını engeller.
    """
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
                print(f"\033[93m[*] İstihbarat Koruması Aktif: {len(blacklist)} ülkenin düğümleri bloklandı.\033[0m")
            else:
                controller.reset_conf("ExcludeNodes")
                
            if strict and (entry_country or exit_country or spy_protection_level > 0):
                controller.set_conf("StrictNodes", "1")
            else:
                controller.set_conf("StrictNodes", "0")
                
            controller.signal(stem.Signal.NEWNYM)
            print(f"\033[92m[+] MULTI-HOP YAPILANDIRILDI: Giriş:[{entry_country}] -> Çıkış:[{exit_country}]\033[0m")
            return True
            
    except Exception as e:
        print(f"\033[91m[-] Multi-Hop yapılandırma hatası: {e}\033[0m")
        return False

if __name__ == "__main__":
    print("--- ALP VPN ÇEKİRDEK TESTİ ---")
    print(f"Mevcut Detaylı Kimliğiniz: {get_detailed_ip_info()}")
    renew_tor_ip()
    print(f"Yeni Detaylı Kimliğiniz: {get_detailed_ip_info()}")