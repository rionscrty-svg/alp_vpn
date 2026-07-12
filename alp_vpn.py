import os
import sys
import time
import socket
import subprocess
import requests
from alp_core import get_current_ip, renew_tor_ip, get_detailed_ip_info, set_tor_exit_node, change_mac_address, activate_kill_switch, deactivate_kill_switch, connect_wireguard, disconnect_wireguard, secure_dns_start, secure_dns_stop, connect_warp, disconnect_warp, configure_multihop_circuit

def print_banner():
    # Terminal için ANSI Renk Kodları
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    banner = f"""{CYAN}{BOLD}
       ___    __    ____  _    ______  _  __
      /   |  / /   / __ \| |  / / __ \/ |/ /
     / /| | / /   / /_/ /| | / / /_/ /    / 
    / ___ |/ /___/ ____/ | |/ / ____/ /|  /  
   /_/  |_/_____/_/      |___/_/   /_/ |_/   
    {RESET}
    {YELLOW}[+] Gelişmiş Linux Ağ Gizlilik ve Güvenlik Kalkanı{RESET}
    {RED}[*] Geliştirici : Rion{RESET}
    {RED}[*] Versiyon    : 1.1.0 (Akıllı Zırh Sürümü){RESET}
 {GREEN}==================================================={RESET}
    """
    print(banner)

def clear_screen():
    subprocess.run(["clear"])

def clean_iptables_armor():
    """Çöp Toplayıcı: Modlar arası geçişte arkada kalan iptables kilitlerini temizler."""
    subprocess.run(["sudo", "iptables", "-F"], capture_output=True)
    subprocess.run(["sudo", "iptables", "-X"], capture_output=True)
    subprocess.run(["sudo", "iptables", "-P", "INPUT", "ACCEPT"], capture_output=True)
    subprocess.run(["sudo", "iptables", "-P", "OUTPUT", "ACCEPT"], capture_output=True)
    subprocess.run(["sudo", "iptables", "-P", "FORWARD", "ACCEPT"], capture_output=True)

def check_tor_service():
    print("[*] Tor bağlantısı kontrol ediliyor (Port 9050)...")
    try:
        with socket.create_connection(("127.0.0.1", 9050), timeout=2):
            print("[+] Tor servisi aktif ve yanıt veriyor.\n")
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        print("[-] HATA: Tor servisi yanıt vermiyor veya kapalı!")
        print("[-] Lütfen terminale 'sudo systemctl start tor' yazarak servisi başlatın.")
        sys.exit(1)

def verify_connection():
    print("[*] Tor ağı üzerinden internete çıkış doğrulanıyor (Biraz sürebilir)...")
    
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    
    for deneme in range(1, 4):
        try:
            response = requests.get("https://check.torproject.org/", proxies=proxies, timeout=15)
            if "Congratulations" in response.text:
                print("[+] BAŞARILI! Tor ağı üzerinden internete bağlısın.\n")
                return 
        except requests.exceptions.Timeout:
            print(f"[*] Deneme {deneme}/3 zaman aşımına uğradı. Tor devreleri kuruluyor, bekleniyor...")
            time.sleep(5) 
        except Exception as e:
            print(f"[-] HATA: İnternet bağlantısı kurulamadı. Sebep: {e}")
            sys.exit(1)
            
    print("[-] HATA: Tor ağına bağlanılamadı! Ağınız yeni değişmiş olabilir.")
    print("[-] ÇÖZÜM: Lütfen terminale 'sudo systemctl restart tor' yazıp programı tekrar açın.")
    sys.exit(1)

def print_menu():
    print("1) Ghost Mode (Rastgele Ülke - 30s de bir IP değişir)")
    print("2) Custom Tor Profile (Süreyi Sen Seç)")
    print("3) Location Changer (Hedef Ülke Seçimi)")
    print("4) Mac Adresi Gizleme (Ağ yöneticisinden gizlenme / MAC Spoofing)")
    print("5) Custom Wireguard Node (Özel Sunucu / kendi wireguardın)")
    print("6) High Speed Mode (Cloudflare Warp)")
    print("7) Multi-Hop (Sıçrama)")
    print("8) Çıkış \n")
    print("\033[92m" + "="*50 + "\033[0m")

def main():
    interface = ""
    while True:
        clear_screen()
        print_banner()
        print_menu()
        secim = input("Seçiminiz [1-8]: ")

        if secim == '1':
            set_tor_exit_node(None)
            print("\n[+] Ghost Mode Aktif Ediliyor...")
            
            print("\033[93m[!] ÖNEMLİ UYARI: Eğer az önce MAC adresinizi değiştirdiyseniz,")
            print("    ağın tam oturması için 15-20 saniye beklemeniz önerilir.\033[0m\n")
            
            interface = input("[*] Kill Switch koruması için ağ arayüzünüzü yazın (örn: enp7s0): ").strip()

            secure_dns_start()
            
            print("[!] Durdurmak ve menüye dönmek için CTRL+C'ye basın.\n")
            try:
                while True:
                    proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                    try:
                        requests.get("https://check.torproject.org/", proxies=proxies, timeout=12)
                        print(f"[*] Aktif Kimlik: {get_detailed_ip_info()}")
                        time.sleep(30)
                        renew_tor_ip()
                        # HATA ÇÖZÜMÜ: Tor IP değiştirdikten sonra yeni devre kurması için 4 saniye nefes payı
                        time.sleep(4) 
                    except Exception as e:
                        print(f"\n\033[91m[-] Bağlantı sarsıntısı: {e}. Akıllı Zırh devreye giriyor...\033[0m")
                        if interface:
                            print("[*] Veri sızıntısını önlemek için 'Tor-Only' IPTables kalkanı çekiliyor...")
                            
                            # SADECE IPTABLES İLE AĞI KİLİTLİYORUZ, NM RESTART YOK!
                            subprocess.run(["sudo", "iptables", "-F"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-P", "OUTPUT", "DROP"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-P", "INPUT", "DROP"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-o", "lo", "-j", "ACCEPT"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-i", "lo", "-j", "ACCEPT"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-p", "udp", "--dport", "67", "--sport", "68", "-j", "ACCEPT"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "udp", "--dport", "68", "--sport", "67", "-j", "ACCEPT"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-m", "owner", "--uid-owner", "toranon", "-j", "ACCEPT"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"], capture_output=True)
                            
                            secure_dns_stop()
                            
                            print("[*] Fiziksel ağ koparılmadan Tor servisi sıfırlanıyor...")
                            subprocess.run(["sudo", "systemctl", "restart", "tor"])
                            
                            print("\033[93m[*] Korumalı kalkan içinde Tor'un devreyi kurması bekleniyor (15 Saniye)...\033[0m")
                            time.sleep(15) 
                            
                            print("[*] Güvenli DNS ve Ana Kill Switch kuralları YENİDEN KİLİTLENİYOR...")
                            secure_dns_start()
                            activate_kill_switch(interface)
                            
                            print("\033[92m[+] Zırh aktif. Sistem %100 sızıntısız şekilde onarıldı.\033[0m\n")
                        else:
                            print("\n\033[91m[!] UYARI: Ağ arayüzü girilmediği için Kill Switch tetiklenemedi!\033[0m\n")
                            break
            except KeyboardInterrupt:
                print("\n\n[-] Ghost Mode durduruldu. Menüye dönülüyor...")
                time.sleep(1)
            finally:
                secure_dns_stop()
                clean_iptables_armor() # Çıkarken arkada kalan kuralları temizle
                if interface:
                    deactivate_kill_switch(interface)
                print("[*] Ghost Mode kapatıldı, ağ ve DNS ayarları normale döndürüldü.")
                time.sleep(1)
                
        elif secim == '2':
            set_tor_exit_node(None) 
            sure = input("\nKaç saniyede bir IP değişsin? (Örn: 45): ")
            interface = input("[*] Kill Switch koruması için ağ arayüzünüzü yazın (örn: enp7s0): ").strip()
            secure_dns_start()
            
            if sure.isdigit():
                sure = int(sure)
                print(f"\n[+] Custom Tor Modu Aktif ({sure} saniyede bir)")
                print("[!] Durdurmak için CTRL+C'ye basın.\n")
                
                proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                
                try:
                    while True:
                        baglanti_koptu = False
                        try:
                            requests.get("https://check.torproject.org/", proxies=proxies, timeout=8)
                        except Exception:
                            baglanti_koptu = True
                            
                        if baglanti_koptu:
                            print("\n\033[91m[-] Tor bağlantısı koptu! Akıllı Zırh devreye giriyor...\033[0m")
                            if interface:
                                activate_kill_switch(interface)
                                print("[*] Sistem Tor devresini tamir ediyor. (Ağ kapatılmıyor, sadece kilitleniyor)...")
                                subprocess.run(["sudo", "systemctl", "restart", "tor"], capture_output=True)
                                time.sleep(15) 
                                deactivate_kill_switch(interface)
                                print("\033[92m[+] Tamir denemesi bitti. Tünel test ediliyor...\033[0m\n")
                                continue 
                            else:
                                print("\033[91m[!] Ağ arayüzü girilmediği için Kill Switch çalışamadı. Çıkılıyor...\033[0m")
                                break
                                
                        print(f"[*] Aktif Kimlik: {get_detailed_ip_info()}")
                        time.sleep(sure)
                        
                        if not renew_tor_ip():
                            print("[-] Tor IP yenileme başarısız. Bir sonraki döngüde tamir edilecek...")
                        else:
                            time.sleep(4) # IP değiştikten sonra Tor'un oturmasını bekle
                            
                except KeyboardInterrupt:
                    print("\n[*] Çıkış sinyali alındı...")
                    time.sleep(1)
                finally:
                    secure_dns_stop()
                    clean_iptables_armor()
                    if interface:
                        deactivate_kill_switch(interface)
                    print("\n[-] Custom mod durduruldu. Menüye dönülüyor...")
                    time.sleep(1)
            else:
                print("\n[!] Lütfen geçerli bir rakam girin!")
                time.sleep(2)

        elif secim == '3':
            secure_dns_start()
            print("\n=== HEDEF ÜLKE SEÇİMİ ===")
            print("Popüler Kodlar: de (Almanya), us (Amerika), fr (Fransa), nl (Hollanda)")
            ulke = input("Bağlanmak istediğiniz ülke kodu (örn: de): ").strip()
            interface = input("[*] Kill Switch koruması için ağ arayüzünüzü yazın (örn: enp7s0): ").strip()
            
            if len(ulke) == 2 and ulke.isalpha():
                set_tor_exit_node(ulke) 
                print(f"\n[+] Bağlantı [{ulke.upper()}] ülkesine tünellendi.")
                print("[!] Normal menüye dönmek için CTRL+C'ye basın.\n")
                
                try:
                    while True:
                        proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                        
                        try:
                            requests.get("https://check.torproject.org/", proxies=proxies, timeout=10)
                            print(f"[*] Aktif Kimlik: {get_detailed_ip_info()}")
                            time.sleep(15) 
                            
                        except Exception as e:
                            print(f"\n\033[91m[-] Bağlantı koptu: {e}. Akıllı onarım başlatılıyor...\033[0m")
                            if interface:
                                print("[*] Sızıntıyı önlemek için IPTables Zırhı çekiliyor...")
                                
                                subprocess.run(["sudo", "iptables", "-F"], capture_output=True)
                                subprocess.run(["sudo", "iptables", "-P", "OUTPUT", "DROP"], capture_output=True)
                                subprocess.run(["sudo", "iptables", "-P", "INPUT", "DROP"], capture_output=True)
                                subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-o", "lo", "-j", "ACCEPT"], capture_output=True)
                                subprocess.run(["sudo", "iptables", "-A", "INPUT", "-i", "lo", "-j", "ACCEPT"], capture_output=True)
                                subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-p", "udp", "--dport", "67", "--sport", "68", "-j", "ACCEPT"], capture_output=True)
                                subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "udp", "--dport", "68", "--sport", "67", "-j", "ACCEPT"], capture_output=True)
                                subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-m", "owner", "--uid-owner", "toranon", "-j", "ACCEPT"], capture_output=True)
                                subprocess.run(["sudo", "iptables", "-A", "INPUT", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"], capture_output=True)
                                
                                secure_dns_stop()
                                
                                print("[*] Tor servisi yeniden başlatılıyor (Ağ kesilmeden)...")
                                subprocess.run(["sudo", "systemctl", "restart", "tor"])
                                
                                print("\033[93m[*] Korumalı hat üzerinden ağ haritası indiriliyor (15 Saniye)...\033[0m")
                                time.sleep(15) 
                                
                                set_tor_exit_node(ulke)
                                print(f"[*] Ülke kilidi tekrar [{ulke.upper()}] olarak ayarlandı.")
                                
                                secure_dns_start()
                                activate_kill_switch(interface)
                                print("\033[92m[+] Onarım sızıntısız tamamlandı!\033[0m\n")
                            else:
                                print("\n\033[91m[!] Ağ arayüzü girilmediği için koruma başlatılamadı!\033[0m\n")
                                break
                                
                except KeyboardInterrupt:
                    set_tor_exit_node(None)
                    print("\n\n[-] Ülke kısıtlaması kaldırıldı. Menüye dönülüyor...")
                    time.sleep(1)
                finally:
                    secure_dns_stop()
                    clean_iptables_armor()
                    if interface:
                        deactivate_kill_switch(interface)
                    print("[+] Zırh ve DNS SIZINTI ÖNLEME KAPATILDI")
                    time.sleep(1)

            else:
                print("\n[!] Geçersiz ülke kodu! (Lütfen 'us' veya 'de' gibi 2 harfli kod girin)")
                time.sleep(2)

        elif secim == '4':
            print("\n=== MAC ADRESİ GİZLEME ===")
            print("Örnek ağ isimleri: eth0 (Kablolu), wlan0 (Kablosuz), wlp3s0 vb.")
            interface = input("Gizlemek istediğiniz ağ arayüzünü yazın: ").strip()
            
            if interface:
                change_mac_address(interface)
                time.sleep(3)
            else:
                print("[-] Geçersiz giriş!")
                time.sleep(2)

        elif secim == '5':
            print("\n=== CUSTOM WIREGUARD NODE ===")
            print("[*] Kendi WireGuard (.conf) sunucunuza bağlanın.")
            print("1) Kendi .conf dosyanızla bağlanın")
            print("2) Aktif bağlantıyı kapat")
            print("3) Ana Menüye Dön")
            
            wg_secim = input("\nSeçiminiz [1-3]: ").strip()
            
            if wg_secim == '1':
                conf_path = input("\n[?] Lütfen .conf dosyasının tam yolunu girin (örn: /home/kali/benim_vpn.conf): ").strip()
                if os.path.exists(conf_path):
                    set_tor_exit_node(None) 
                    clean_iptables_armor() # Çakışmaları önlemek için zırhı temizle
                    if connect_wireguard(conf_path):
                        input("\nKapatmak / Menüye dönmek için Enter'a basın...")
                        disconnect_wireguard(conf_path)
                        time.sleep(2)
                else:
                    print(f"[-] HATA: '{conf_path}' bulunamadı. Yolu doğru yazdığınızdan emin olun!")
                    time.sleep(2)
                    
            elif wg_secim == '2':
                conf_path = input("\n[?] Kapatılacak .conf dosyasının tam yolunu girin: ").strip()
                if os.path.exists(conf_path):
                    disconnect_wireguard(conf_path)
                else:
                    print("[-] Dosya bulunamadığı için işlem yapılamadı.")
                time.sleep(2)
                
            elif wg_secim == '3':
                print("[*] Ana menüye dönülüyor...")
                time.sleep(1)
            else:
                print("[-] Geçersiz seçim!")
                time.sleep(2)

        elif secim == '6':
            print("\n\033[93m" + "="*55)
            print("        HIGH SPEED MODE (CLOUDFLARE WARP)")
            print("="*55 + "\033[0m")
            print("\033[91m[!] GİZLİLİK UYARISI:\033[0m")
            print("Bu mod, maksimum hız ve sansür atlatmak için tasarlanmıştır.")
            print("Trafiğiniz Cloudflare'in devasa ağına (1.1.1.1) tünellenir.")
            print("Hükümet/ISS engellerini aşarsınız ancak %100 No-Log garanti edilmez.\n")
            
            print("\033[93m[!] MAC UYARISI: Eğer az önce MAC adresi değiştirdiyseniz (Seçenek 4),")
            print("    WARP'ın bağlanması için modemin size yeni IP vermesi gerekir.\033[0m\n")
            
            print("1) Şartları kabul et ve Jet Hızında Bağlan")
            print("2) Aktif WARP Bağlantısını Durdur")
            print("3) Ana Menüye Dön")
            
            warp_secim = input("\nSeçiminiz [1-3]: ").strip()
            
            if warp_secim == '1':
                set_tor_exit_node(None)
                subprocess.run(["sudo", "systemctl", "stop", "tor"]) 
                
                # ÇÖP TOPLAYICI DEVREDE: WARP'ın bağlanmasını engelleyen hayalet Kill Switch kuralları siliniyor.
                print("[*] Sistemin eski kilitleri ve zırh kuralları temizleniyor...")
                clean_iptables_armor()
                if interface:
                    deactivate_kill_switch(interface)
                
                if connect_warp():
                    print("\n[*] Tünel oturtuluyor, yeni IP bilgisi alınıyor (Lütfen bekleyin)...")
                    time.sleep(5) 
                    
                    print(f"[*] YENİ WARP KİMLİĞİNİZ: {get_current_ip()}\n")
                    print("\033[93m[!] İnternetiniz şu an jet hızında! Programdan çıkmadan önce mutlaka durdurun (Seçenek 2).\033[0m")
                    
                    input("\nMenüye dönmek / Kapatmak için Enter'a basın...")
                    disconnect_warp()
                    subprocess.run(["sudo", "systemctl", "start", "tor"]) 
                else:
                    input("\n[-] HATA YAKALANDI: Lütfen üstteki hata mesajını okuyun ve menüye dönmek için Enter'a basın...")
                    
            elif warp_secim == '2':
                disconnect_warp()
                subprocess.run(["sudo", "systemctl", "start", "tor"]) 
                time.sleep(2)
                
            elif warp_secim == '3':
                print("[*] Ana menüye dönülüyor...")
                time.sleep(1)
            
        elif secim == '7':
            print("\n\033[93m" + "="*55)
            print("        MULTI-HOP (GELİŞMİŞ ZİNCİRLEME)")
            print("="*55 + "\033[0m")
            print("[*] Trafiğinizi belirlediğiniz iki ülke üzerinden geçirir.")
            print("\033[91m[!] Multi-Hop un ne olduğundan emin değilseniz kullanmamanız önerilir.\n\033[0m")
            
            giris = input("Giriş Düğümü Ülke Kodu (örn: de) [Boş geçilebilir]: ").strip()
            cikis = input("Çıkış Düğümü Ülke Kodu (örn: us) [Boş geçilebilir]: ").strip()
            
            print("\n[*] İstihbarat Ağı Koruması (Orta Düğümler İçin):")
            print("0) Kapalı (Daha Hızlı)")
            print("1) Five Eyes (ABD, İng, Kan, Avus, Yeni Zelanda) Engelle")
            print("2) Fourteen Eyes (Ekstra 9 Avrupa Ülkesi) Engelle")
            spy_secim = input("Seçiminiz [0-2]: ").strip()
            
            spy_level = int(spy_secim) if spy_secim in ['0', '1', '2'] else 0
            
            interface = input("\n[*] Kill Switch koruması için ağ arayüzünüzü yazın (örn: enp7s0): ").strip()
            
            secure_dns_start()
            print("\n[*] Multi-Hop ağı örülüyor, lütfen bekleyin...")
            
            configure_multihop_circuit(giris if giris else None, cikis if cikis else None, True, spy_level)
            
            print("\n[!] Durdurmak ve menüye dönmek için CTRL+C'ye basın.\n")
            try:
                while True:
                    proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                    try:
                        requests.get("https://check.torproject.org/", proxies=proxies, timeout=15)
                        print(f"[*] Multi-Hop Kimliği: {get_detailed_ip_info()}")
                        time.sleep(30) 
                        
                    except Exception as e:
                        print(f"\n\033[91m[-] Zincir koptu: {e}. Akıllı zırh ile onarım başlatılıyor...\033[0m")
                        if interface:
                            print("[*] Sızıntıyı önlemek için anında kalkan çekiliyor...")
                            
                            subprocess.run(["sudo", "iptables", "-F"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-P", "OUTPUT", "DROP"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-P", "INPUT", "DROP"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-o", "lo", "-j", "ACCEPT"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-i", "lo", "-j", "ACCEPT"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-p", "udp", "--dport", "67", "--sport", "68", "-j", "ACCEPT"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "udp", "--dport", "68", "--sport", "67", "-j", "ACCEPT"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-m", "owner", "--uid-owner", "toranon", "-j", "ACCEPT"], capture_output=True)
                            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"], capture_output=True)
                            
                            secure_dns_stop()
                            
                            print("[*] Ağ bağlantısı kapatılmadan Tor resetleniyor...")
                            subprocess.run(["sudo", "systemctl", "restart", "tor"])
                            
                            print("\033[93m[*] Korumalı hat üzerinden ağ haritası indiriliyor (20 Saniye)...\033[0m")
                            time.sleep(20) 
                            
                            print("[*] Multi-Hop zinciri yeniden inşa ediliyor...")
                            configure_multihop_circuit(giris if giris else None, cikis if cikis else None, True, spy_level)
                            
                            secure_dns_start()
                            activate_kill_switch(interface)
                            print("\033[92m[+] Onarım sızıntısız tamamlandı! Zincir aktif.\033[0m\n")
                        else:
                            print("\n\033[91m[!] UYARI: Ağ arayüzü girilmediği için Kill Switch tetiklenemedi!\033[0m\n")
                            break
            except KeyboardInterrupt:
                print("\n\n[-] Multi-Hop durduruldu. Tor ayarları sıfırlanıyor...")
                configure_multihop_circuit(None, None, False, 0)
                time.sleep(1)
            finally:
                secure_dns_stop()
                clean_iptables_armor()
                if interface:
                    deactivate_kill_switch(interface)
                print("[*] Ağ ve DNS ayarları normale döndürüldü. Menüye dönülüyor...")
                time.sleep(1)
        
        elif secim == '8':
            print("\n[-] Zırh ve kilitler temizleniyor...")
            clean_iptables_armor()
            print("[-] ALP VPN kapatılıyor. Güvenli günler...")
            sys.exit(0) 
            
        else:
            print("\n\033[93m[!] Geçersiz seçim! Lütfen 1-8 arasında bir sayı girin.\033[0m")
            time.sleep(1)
            continue

if __name__ == "__main__":
    clear_screen()
    check_tor_service()
    verify_connection()
    time.sleep(1) 
    clear_screen()
    print_banner()
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[-] Program zorla kapatıldı. Güvenlik zırhları temizleniyor...")
        clean_iptables_armor()
        sys.exit(0)