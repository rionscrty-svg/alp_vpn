import os
import sys
import time
import alp_core
import socket
import subprocess
import requests
from alp_core import get_current_ip, renew_tor_ip, get_detailed_ip_info, set_tor_exit_node, change_mac_address, activate_kill_switch, deactivate_kill_switch, connect_wireguard, disconnect_wireguard, secure_dns_start, secure_dns_stop, connect_warp, disconnect_warp, configure_multihop_circuit


LANG = "tr"
T = {}

TRANSLATIONS = {
    "tr": {
        "banner_subtitle": "[+] Gelişmiş Linux Ağ Gizlilik ve Güvenlik Kalkanı",
        "banner_dev": "[*] Geliştirici : Rion",
        "banner_ver": "[*] Versiyon    : 1.1.0",
        "check_tor": "[*] Tor bağlantısı kontrol ediliyor (Port 9050)...",
        "tor_active": "[+] Tor servisi aktif ve yanıt veriyor.\n",
        "tor_error": "[-] HATA: Tor servisi yanıt vermiyor veya kapalı!\n[-] Lütfen terminale 'sudo systemctl start tor' yazarak servisi başlatın.",
        "verify_conn": "[*] Tor ağı üzerinden internete çıkış doğrulanıyor (Biraz sürebilir)...",
        "conn_success": "[+] BAŞARILI! Tor ağı üzerinden internete bağlısın.\n",
        "retry_msg": "[*] Deneme {deneme}/3 zaman aşımına uğradı. Tor devreleri kuruluyor, bekleniyor...",
        "conn_err": "[-] HATA: İnternet bağlantısı kurulamadı. Sebep: {e}",
        "conn_fail_err1": "[-] HATA: Tor ağına bağlanılamadı! Ağınız yeni değişmiş olabilir.",
        "conn_fail_err2": "[-] ÇÖZÜM: Lütfen terminale 'sudo systemctl restart tor' yazıp programı tekrar açın.",
        "menu_title": "=== ALP VPN MENÜ ===",
        "menu_1": "1) Ghost Mode (Rastgele Ülke - 30s de bir IP değişir)",
        "menu_2": "2) Custom Tor Profile (Süreyi Sen Seç)",
        "menu_3": "3) Location Changer (Hedef Ülke Seçimi)",
        "menu_4": "4) Mac Adresi Gizleme (Ağ yöneticisinden gizlenme / MAC Spoofing)",
        "menu_5": "5) Custom Wireguard Node (Özel Sunucu / kendi wireguardın)",
        "menu_6": "6) High Speed Mode (Cloudflare Warp)",
        "menu_7": "7) Multi-Hop (Sıçrama)",
        "menu_8": "8) Çıkış \n",
        "menu_prompt": "Seçiminiz [1-8]: ",
        "ghost_active": "\n[+] Ghost Mode Aktif Ediliyor...",
        "ghost_mac_warn": "[!] ÖNEMLİ UYARI: Eğer az önce MAC adresinizi değiştirdiyseniz,\n    ağın tam oturması için 15-20 saniye beklemeniz önerilir.\n",
        "interface_prompt": "[*] Kill Switch koruması için ağ arayüzünüzü yazın (enp7s0 , eth0 , wlp2s0 , wlan0 , enp3s0 vb.): ",
        "ctrl_c_msg": "[!] Durdurmak ve menüye dönmek için CTRL+C'ye basın.\n",
        "active_identity": "[*] Aktif Kimlik: {info}",
        "conn_shake_msg": "\n[-] Bağlantı sarsıntısı: {e}. Akıllı Zırh devreye giriyor...",
        "iptables_shield_msg": "[*] Veri sızıntısını önlemek için 'Tor-Only' IPTables kalkanı çekiliyor...",
        "tor_reset_msg": "[*] Fiziksel ağ koparılmadan Tor servisi sıfırlanıyor...",
        "wait_circuit": "[*] Korumalı kalkan içinde Tor'un devreyi kurması bekleniyor (15 Saniye)...",
        "relock_rules": "[*] Güvenli DNS ve Ana Kill Switch kuralları YENİDEN KİLİTLENİYOR...",
        "repair_success": "[+] Zırh aktif. Sistem %100 sızıntısız şekilde onarıldı.\n",
        "no_interface_warn": "\n[!] UYARI: Ağ arayüzü girilmediği için Kill Switch tetiklenemedi!\n",
        "ghost_stopping": "\n\n[-] Ghost Mode durduruldu. Menüye dönülüyor...",
        "ghost_closed": "[*] Ghost Mode kapatıldı, ağ ve DNS ayarları normale döndürüldü.",
        "custom_sec_prompt": "\nKaç saniyede bir IP değişsin? (Örn: 45): ",
        "custom_active": "\n[+] Custom Tor Modu Aktif ({sure} saniyede bir)",
        "ctrl_c_stop": "[!] Durdurmak için CTRL+C'ye basın.\n",
        "tor_lost_msg": "\n[-] Tor bağlantısı koptu! Akıllı Zırh devreye giriyor...",
        "repairing_msg": "[*] Sistem Tor devresini tamir ediyor. (Ağ kapatılmıyor, sadece kilitleniyor)...",
        "repair_test_msg": "[+] Tamir denemesi bitti. Tünel test ediliyor...\n",
        "no_interface_exit": "[!] Ağ arayüzü girilmediği için Kill Switch çalışamadı. Çıkılıyor...",
        "renew_fail": "[-] Tor IP yenileme başarısız. Bir sonraki döngüde tamir edilecek...",
        "exit_signal": "\n[*] Çıkış sinyali alındı...",
        "custom_stopping": "\n[-] Custom mod durduruldu. Menüye dönülüyor...",
        "invalid_num": "\n[!] Lütfen geçerli bir rakam girin!",
        "loc_title": "\n=== HEDEF ÜLKE SEÇİMİ ===",
        "loc_popular": "Popüler Kodlar: de (Almanya), us (Amerika), fr (Fransa), nl (Hollanda)",
        "loc_prompt": "Bağlanmak istediğiniz ülke kodu (örn: de): ",
        "tunnel_success": "\n[+] Bağlantı [{ulke}] ülkesine tünellendi.",
        "loc_lost": "\n[-] Bağlantı koptu: {e}. Akıllı onarım başlatılıyor...",
        "iptables_armor": "[*] Sızıntıyı önlemek için IPTables Zırhı çekiliyor...",
        "tor_restart_clean": "[*] Tor servisi yeniden başlatılıyor (Ağ kesilmeden)...",
        "wait_map": "[*] Korumalı hat üzerinden ağ haritası indiriliyor (15 Saniye)...",
        "relock_loc": "[*] Ülke kilidi tekrar [{ulke}] olarak ayarlandı.",
        "repair_done": "[+] Onarım sızıntısız tamamlandı!\n",
        "no_interface_protect": "\n[!] Ağ arayüzü girilmediği için koruma başlatılamadı!\n",
        "loc_removed": "\n\n[-] Ülke kısıtlaması kaldırıldı. Menüye dönülüyor...",
        "armor_closed": "[+] Zırh ve DNS SIZINTI ÖNLEME KAPATILDI",
        "invalid_country": "\n[!] Geçersiz ülke kodu! (Lütfen 'us' veya 'de' gibi 2 harfli kod girin)",
        "mac_title": "\n=== MAC ADRESİ GİZLEME ===",
        "mac_example": "Örnek ağ isimleri: eth0 (Kablolu), wlan0 (Kablosuz), wlp3s0 vb.",
        "mac_prompt": "Gizlemek istediğiniz ağ arayüzünü yazın: ",
        "invalid_input": "[-] Geçersiz giriş!",
        "wg_title": "\n=== CUSTOM WIREGUARD NODE ===",
        "wg_info": "[*] Kendi WireGuard (.conf) sunucunuza bağlanın.",
        "wg_opt1": "1) Kendi .conf dosyanızla bağlanın",
        "wg_opt2": "2) Aktif bağlantıyı kapat",
        "wg_opt3": "3) Ana Menüye Dön",
        "wg_prompt": "\nSeçiminiz [1-3]: ",
        "wg_conf_prompt": "\n[?] Lütfen .conf dosyasının tam yolunu girin (örn: /home/kali/benim_vpn.conf): ",
        "wg_close_prompt": "\nKapatmak / Menüye dönmek için Enter'a basın...",
        "wg_not_found": "[-] HATA: '{path}' bulunamadı. Yolu doğru yazdığınızdan emin olun!",
        "wg_close_path_prompt": "\n[?] Kapatılacak .conf dosyasının tam yolunu girin: ",
        "wg_not_found_action": "[-] Dosya bulunamadığı için işlem yapılamadı.",
        "returning_main": "[*] Ana menüye dönülüyor...",
        "invalid_choice": "[-] Geçersiz seçim!",
        "warp_title": "        HIGH SPEED MODE (CLOUDFLARE WARP)",
        "warp_privacy_warn": "[!] GİZLİLİK UYARISI:",
        "warp_privacy_desc": "Bu mod, maksimum hız ve sansür atlatmak için tasarlanmıştır.\nTrafiğiniz Cloudflare'in devasa ağına (1.1.1.1) tünellenir.\nGerçek ip adresinizi görünür.\nHükümet/ISS engellerini aşarsınız ancak %100 No-Log garanti edilmez.\n",
        "warp_mac_warn": "[!] MAC UYARISI: Eğer az önce MAC adresi değiştirdiyseniz (Seçenek 4),\n    WARP'ın bağlanması için modemin size yeni IP vermesi gerekir.\n",
        "warp_opt1": "1) Şartları kabul et ve Jet Hızında Bağlan",
        "warp_opt2": "2) Aktif WARP Bağlantısını Durdur",
        "warp_opt3": "3) Ana Menüye Dön",
        "warp_prompt": "\nSeçiminiz [1-3]: ",
        "clearing_locks": "[*] Sistemin eski kilitleri ve zırh kuralları temizleniyor...",
        "warp_wait": "\n[*] Tünel oturtuluyor, yeni IP bilgisi alınıyor (Lütfen bekleyin)...",
        "warp_new_identity": "[*] YENİ WARP KİMLİĞİNİZ: {ip}\n",
        "warp_speed_warn": "[!] İnternetiniz şu an jet hızında! Programdan çıkmadan önce mutlaka durdurun (Seçenek 2).",
        "warp_close_prompt": "\nMenüye dönmek / Kapatmak için Enter'a basın...",
        "warp_err_caught": "\n[-] HATA YAKALANDI: Lütfen üstteki hata mesajını okuyun ve menüye dönmek için Enter'a basın...",
        "mh_title": "        MULTI-HOP (GELİŞMİŞ ZİNCİRLEME)",
        "mh_desc": "[*] Trafiğinizi belirlediğiniz iki ülke üzerinden geçirir.",
        "mh_warn": "[!] Multi-Hop'un ne olduğundan emin değilseniz kullanmamanız önerilir.\n",
        "mh_in_prompt": "Giriş Düğümü Ülke Kodu (örn: de) [Boş geçilebilir]: ",
        "mh_out_prompt": "Çıkış Düğümü Ülke Kodu (örn: us) [Boş geçilebilir]: ",
        "mh_intel_title": "\n[*] İstihbarat Ağı Koruması (Orta Düğümler İçin):",
        "mh_intel_0": "0) Kapalı (Daha Hızlı)",
        "mh_intel_1": "1) Five Eyes (ABD, İng, Kan, Avus, Yeni Zelanda) Engelle",
        "mh_intel_2": "2) Fourteen Eyes (Ekstra 9 Avrupa Ülkesi) Engelle",
        "mh_intel_prompt": "Seçiminiz [0-2]: ",
        "mh_building": "\n[*] Multi-Hop ağı örülüyor, lütfen bekleyin...",
        "mh_identity": "[*] Multi-Hop Kimliği: {info}",
        "mh_broken": "\n[-] Zincir koptu: {e}. Akıllı zırh ile onarım başlatılıyor...",
        "mh_shield": "[*] Sızıntıyı önlemek için anında kalkan çekiliyor...",
        "mh_tor_reset": "[*] Ağ bağlantısı kapatılmadan Tor resetleniyor...",
        "mh_wait_map": "[*] Korumalı hat üzerinden ağ haritası indiriliyor (20 Saniye)...",
        "mh_rebuilding": "[*] Multi-Hop zinciri yeniden inşa ediliyor...",
        "mh_stopping": "\n\n[-] Multi-Hop durduruldu. Tor ayarları sıfırlanıyor...",
        "mh_closed": "[*] Ağ ve DNS ayarları normale döndürüldü. Menüye dönülüyor...",
        "exit_clearing": "\n[-] Zırh ve kilitler temizleniyor...",
        "exit_closing": "[-] ALP VPN kapatılıyor. Güvenli günler...",
        "invalid_choice_range": "\n[!] Geçersiz seçim! Lütfen 1-8 arasında bir sayı girin.",
        "forced_exit": "\n\n[-] Program zorla kapatıldı. Güvenlik zırhları temizleniyor..."
    },
    "en": {
        "banner_subtitle": "[+] Advanced Linux Network Privacy & Security Shield",
        "banner_dev": "[*] Developer   : Rion",
        "banner_ver": "[*] Version     : 1.1.0 ",
        "check_tor": "[*] Checking Tor connection (Port 9050)...",
        "tor_active": "[+] Tor service is active and responding.\n",
        "tor_error": "[-] ERROR: Tor service is not responding or stopped!\n[-] Please start the service by typing 'sudo systemctl start tor' in the terminal.",
        "verify_conn": "[*] Verifying internet connection through Tor (This may take a moment)...",
        "conn_success": "[+] SUCCESS! You are connected to the internet through the Tor network.\n",
        "retry_msg": "[*] Attempt {deneme}/3 timed out. Tor circuits are being established, waiting...",
        "conn_err": "[-] ERROR: Internet connection could not be established. Reason: {e}",
        "conn_fail_err1": "[-] ERROR: Failed to connect to the Tor network! Your network may have changed.",
        "conn_fail_err2": "[-] SOLUTION: Please type 'sudo systemctl restart tor' in your terminal and restart the program.",
        "menu_title": "=== ALP VPN MENU ===",
        "menu_1": "1) Ghost Mode (Random Country - IP changes every 30s)",
        "menu_2": "2) Custom Tor Profile (Choose custom rotation interval)",
        "menu_3": "3) Location Changer (Select target country)",
        "menu_4": "4) Hide MAC Address (Network manager camouflage / MAC Spoofing)",
        "menu_5": "5) Custom Wireguard Node (Private Server / your own WireGuard configuration)",
        "menu_6": "6) High Speed Mode (Cloudflare Warp)",
        "menu_7": "7) Multi-Hop (Chaining)",
        "menu_8": "8) Exit \n",
        "menu_prompt": "Your Choice [1-8]: ",
        "ghost_active": "\n[+] Activating Ghost Mode...",
        "ghost_mac_warn": "[!] IMPORTANT WARNING: If you have just changed your MAC address,\n    it is recommended to wait 15-20 seconds for the network to settle.\n",
        "interface_prompt": "[*] Enter your network interface for Kill Switch protection (enp7s0, eth0, wlp2s0, wlan0, enp3s0 etc.): ",
        "ctrl_c_msg": "[!] Press CTRL+C to stop and return to the main menu.\n",
        "active_identity": "[*] Active Identity: {info}",
        "conn_shake_msg": "\n[-] Connection instability: {e}. Smart Armor is deploying...",
        "iptables_shield_msg": "[*] Deploying 'Tor-Only' IPTables shield to prevent data leaks...",
        "tor_reset_msg": "[*] Resetting Tor service without disconnecting physical network...",
        "wait_circuit": "[*] Waiting for Tor to establish circuit inside the protective shield (15 Seconds)...",
        "relock_rules": "[*] RE-LOCKING Secure DNS and Main Kill Switch rules...",
        "repair_success": "[+] Shield active. System successfully repaired with 100% leak protection.\n",
        "no_interface_warn": "\n[!] WARNING: Kill Switch could not be triggered because no network interface was provided!\n",
        "ghost_stopping": "\n\n[-] Ghost Mode stopped. Returning to menu...",
        "ghost_closed": "[*] Ghost Mode closed, network and DNS settings restored to normal.",
        "custom_sec_prompt": "\nHow many seconds between IP changes? (e.g., 45): ",
        "custom_active": "\n[+] Custom Tor Mode Active (every {sure} seconds)",
        "ctrl_c_stop": "[!] Press CTRL+C to stop.\n",
        "tor_lost_msg": "\n[-] Tor connection lost! Smart Armor is deploying...",
        "repairing_msg": "[*] System is repairing Tor circuit. (Network is locked, not disconnected)...",
        "repair_test_msg": "[+] Repair attempt finished. Testing tunnel...\n",
        "no_interface_exit": "[!] Kill Switch could not run because no network interface was provided. Exiting...",
        "renew_fail": "[-] Tor IP renewal failed. Will be repaired on the next loop...",
        "exit_signal": "\n[*] Exit signal received...",
        "custom_stopping": "\n[-] Custom mode stopped. Returning to menu...",
        "invalid_num": "\n[!] Please enter a valid number!",
        "loc_title": "\n=== TARGET COUNTRY SELECTION ===",
        "loc_popular": "Popular Codes: de (Germany), us (United States), fr (France), nl (Netherlands)",
        "loc_prompt": "Country code you want to connect to (e.g., de): ",
        "tunnel_success": "\n[+] Connection tunneled to country [{ulke}].",
        "loc_lost": "\n[-] Connection lost: {e}. Smart repair initiated...",
        "iptables_armor": "[*] Deploying IPTables Shield to prevent leaks...",
        "tor_restart_clean": "[*] Restarting Tor service (without network interruption)...",
        "wait_map": "[*] Downloading network map over protected line (15 Seconds)...",
        "relock_loc": "[*] Country lock set back to [{ulke}].",
        "repair_done": "[+] Repair completed without leaks!\n",
        "no_interface_protect": "\n[!] Protection could not be started because no network interface was provided!\n",
        "loc_removed": "\n\n[-] Country restrictions removed. Returning to menu...",
        "armor_closed": "[+] Shield and DNS LEAK PREVENTION CLOSED",
        "invalid_country": "\n[!] Invalid country code! (Please enter a 2-letter code like 'us' or 'de')",
        "mac_title": "\n=== MAC ADDRESS SPOOFING ===",
        "mac_example": "Example network names: eth0 (Wired), wlan0 (Wireless), wlp3s0 etc.",
        "mac_prompt": "Enter the network interface you want to hide: ",
        "invalid_input": "[-] Invalid input!",
        "wg_title": "\n=== CUSTOM WIREGUARD NODE ===",
        "wg_info": "[*] Connect to your own WireGuard (.conf) server.",
        "wg_opt1": "1) Connect with your own .conf file",
        "wg_opt2": "2) Close the active connection",
        "wg_opt3": "3) Return to Main Menu",
        "wg_prompt": "\nYour Choice [1-3]: ",
        "wg_conf_prompt": "\n[?] Please enter the full path to the .conf file (e.g., /home/kali/my_vpn.conf): ",
        "wg_close_prompt": "\nPress Enter to close / return to menu...",
        "wg_not_found": "[-] ERROR: '{path}' not found. Make sure you typed the path correctly!",
        "wg_close_path_prompt": "\n[?] Enter the full path of the .conf file to be closed: ",
        "wg_not_found_action": "[-] Action could not be performed because the file was not found.",
        "returning_main": "[*] Returning to main menu...",
        "invalid_choice": "[-] Invalid choice!",
        "warp_title": "        HIGH SPEED MODE (CLOUDFLARE WARP)",
        "warp_privacy_warn": "[!] PRIVACY WARNING:",
        "warp_privacy_desc": "This mode is designed for maximum speed and bypassing censorship.\nYour traffic is tunneled into Cloudflare's massive network (1.1.1.1).\nYour real IP address is visible.\nYou bypass government/ISP blocks, but 100% No-Log is not guaranteed.\n",
        "warp_mac_warn": "[!] MAC WARNING: If you just changed your MAC address (Option 4),\n    the modem needs to assign you a new IP for WARP to connect.\n",
        "warp_opt1": "1) Accept conditions and Connect with Jet Speed",
        "warp_opt2": "2) Stop Active WARP Connection",
        "warp_opt3": "3) Return to Main Menu",
        "warp_prompt": "\nYour Choice [1-3]: ",
        "clearing_locks": "[*] Clearing system's old locks and shield rules...",
        "warp_wait": "\n[*] Fitting tunnel, retrieving new IP info (Please wait)...",
        "warp_new_identity": "[*] YOUR NEW WARP IDENTITY: {ip}\n",
        "warp_speed_warn": "[!] Your internet is now blazing fast! Make sure to stop it before exiting the program (Option 2).",
        "warp_close_prompt": "\nPress Enter to return to menu / close...",
        "warp_err_caught": "\n[-] ERROR CAUGHT: Please read the error message above and press Enter to return to menu...",
        "mh_title": "        MULTI-HOP (ADVANCED CHAINING)",
        "mh_desc": "[*] Routes your traffic through two custom countries.",
        "mh_warn": "[!] If you are not sure what Multi-Hop is, it is recommended not to use it.\n",
        "mh_in_prompt": "Entry Node Country Code (e.g., de) [Can be left blank]: ",
        "mh_out_prompt": "Exit Node Country Code (e.g., us) [Can be left blank]: ",
        "mh_intel_title": "\n[*] Intelligence Network Protection (For Middle Nodes):",
        "mh_intel_0": "0) Disabled (Faster)",
        "mh_intel_1": "1) Block Five Eyes (US, UK, CA, AU, NZ)",
        "mh_intel_2": "2) Block Fourteen Eyes (Extra 9 European Countries)",
        "mh_intel_prompt": "Your Choice [0-2]: ",
        "mh_building": "\n[*] Building Multi-Hop network, please wait...",
        "mh_identity": "[*] Multi-Hop Identity: {info}",
        "mh_broken": "\n[-] Chain broken: {e}. Initiating repair with smart shield...",
        "mh_shield": "[*] Deploying immediate shield to prevent leaks...",
        "mh_tor_reset": "[*] Resetting Tor without shutting down physical network connection...",
        "mh_wait_map": "[*] Downloading network map over protected line (20 Seconds)...",
        "mh_rebuilding": "[*] Rebuilding Multi-Hop chain...",
        "mh_stopping": "\n\n[-] Multi-Hop stopped. Resetting Tor settings...",
        "mh_closed": "[*] Network and DNS settings restored to normal. Returning to menu...",
        "exit_clearing": "\n[-] Clearing shields and locks...",
        "exit_closing": "[-] ALP VPN is closing. Have a safe day...",
        "invalid_choice_range": "\n[!] Invalid choice! Please enter a number between 1-8.",
        "forced_exit": "\n\n[-] Program force closed. Clearing security shields..."
    }
}

def select_language():
    global T, LANG
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    print(f"\n{CYAN}{BOLD}=== SELECT LANGUAGE / DİL SEÇİNÜ ==={RESET}")
    print("1) English")
    print("2) Türkçe")
    secim = input("Choice / Seçim [1-2]: ").strip()
    if secim == "1":
        LANG = "en"
        T = TRANSLATIONS["en"]
    else:
        LANG = "tr"
        T = TRANSLATIONS["tr"]

    alp_core.set_language(LANG)
def print_banner():
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
    /_/  |_/_____/_/      |___/_/    /_/ |_/   
     {RESET}
    {YELLOW}{T["banner_subtitle"]}{RESET}
    {RED}{T["banner_dev"]}{RESET}
    {RED}{T["banner_ver"]}{RESET}
 {GREEN}==================================================={RESET}
    """
    print(banner)

def clear_screen():
    subprocess.run(["clear"])

def clean_iptables_armor():
    subprocess.run(["sudo", "iptables", "-F"], capture_output=True)
    subprocess.run(["sudo", "iptables", "-X"], capture_output=True)
    subprocess.run(["sudo", "iptables", "-P", "INPUT", "ACCEPT"], capture_output=True)
    subprocess.run(["sudo", "iptables", "-P", "OUTPUT", "ACCEPT"], capture_output=True)
    subprocess.run(["sudo", "iptables", "-P", "FORWARD", "ACCEPT"], capture_output=True)

def check_tor_service():
    print(T["check_tor"])
    try:
        with socket.create_connection(("127.0.0.1", 9050), timeout=2):
            print(T["tor_active"])
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        print(T["tor_error"])
        sys.exit(1)

def verify_connection():
    print(T["verify_conn"])
    
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    
    for deneme in range(1, 4):
        try:
            response = requests.get("https://check.torproject.org/", proxies=proxies, timeout=15)
            if "Congratulations" in response.text:
                print(T["conn_success"])
                return 
        except requests.exceptions.Timeout:
            print(T["retry_msg"].format(deneme=deneme))
            time.sleep(5) 
        except Exception as e:
            print(T["conn_err"].format(e=e))
            sys.exit(1)
            
    print(T["conn_fail_err1"])
    print(T["conn_fail_err2"])
    sys.exit(1)

def print_menu():
    print(T["menu_title"])
    print(T["menu_1"])
    print(T["menu_2"])
    print(T["menu_3"])
    print(T["menu_4"])
    print(T["menu_5"])
    print(T["menu_6"])
    print(T["menu_7"])
    print(T["menu_8"])
    print("\033[92m" + "="*50 + "\033[0m")

def main():
    interface = ""
    while True:
        clear_screen()
        print_banner()
        print_menu()
        secim = input(T["menu_prompt"])

        if secim == '1':
            set_tor_exit_node(None)
            print(T["ghost_active"])
            print(f"\033[93m{T['ghost_mac_warn']}\033[0m")
            
            interface = input(T["interface_prompt"]).strip()

            secure_dns_start()
            
            print(T["ctrl_c_msg"])
            try:
                while True:
                    proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                    try:
                        requests.get("https://check.torproject.org/", proxies=proxies, timeout=12)
                        print(T["active_identity"].format(info=get_detailed_ip_info()))
                        time.sleep(30)
                        renew_tor_ip()
                        time.sleep(4) 
                    except Exception as e:
                        print(f"\n\033[91m{T['conn_shake_msg'].format(e=e)}\033[0m")
                        if interface:
                            print(T["iptables_shield_msg"])
                            
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
                            
                            print(T["tor_reset_msg"])
                            subprocess.run(["sudo", "systemctl", "restart", "tor"])
                            
                            print(f"\033[93m{T['wait_circuit']}\033[0m")
                            time.sleep(15) 
                            
                            print(T["relock_rules"])
                            secure_dns_start()
                            activate_kill_switch(interface)
                            
                            print(f"\033[92m{T['repair_success']}\033[0m")
                        else:
                            print(f"\n\033[91m{T['no_interface_warn']}\033[0m")
                            break
            except KeyboardInterrupt:
                print(T["ghost_stopping"])
                time.sleep(1)
            finally:
                secure_dns_stop()
                clean_iptables_armor()
                if interface:
                    deactivate_kill_switch(interface)
                print(T["ghost_closed"])
                time.sleep(1)
                
        elif secim == '2':
            set_tor_exit_node(None) 
            sure = input(T["custom_sec_prompt"])
            interface = input(T["interface_prompt"]).strip()
            secure_dns_start()
            
            if sure.isdigit():
                sure = int(sure)
                print(T["custom_active"].format(sure=sure))
                print(T["ctrl_c_stop"])
                
                proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                
                try:
                    while True:
                        baglanti_koptu = False
                        try:
                            requests.get("https://check.torproject.org/", proxies=proxies, timeout=8)
                        except Exception:
                            baglanti_koptu = True
                            
                        if baglanti_koptu:
                            print(f"\n\033[91m{T['tor_lost_msg']}\033[0m")
                            if interface:
                                activate_kill_switch(interface)
                                print(T["repairing_msg"])
                                subprocess.run(["sudo", "systemctl", "restart", "tor"], capture_output=True)
                                time.sleep(15) 
                                deactivate_kill_switch(interface)
                                print(f"\033[92m{T['repair_test_msg']}\033[0m")
                                continue 
                            else:
                                print(f"\033[91m{T['no_interface_exit']}\033[0m")
                                break
                                
                        print(T["active_identity"].format(info=get_detailed_ip_info()))
                        time.sleep(sure)
                        
                        if not renew_tor_ip():
                            print(T["renew_fail"])
                        else:
                            time.sleep(4)
                            
                except KeyboardInterrupt:
                    print(T["exit_signal"])
                    time.sleep(1)
                finally:
                    secure_dns_stop()
                    clean_iptables_armor()
                    if interface:
                        deactivate_kill_switch(interface)
                    print(T["custom_stopping"])
                    time.sleep(1)
            else:
                print(T["invalid_num"])
                time.sleep(2)

        elif secim == '3':
            secure_dns_start()
            print(T["loc_title"])
            print(T["loc_popular"])
            ulke = input(T["loc_prompt"]).strip()
            interface = input(T["interface_prompt"]).strip()
            
            if len(ulke) == 2 and ulke.isalpha():
                set_tor_exit_node(ulke) 
                print(T["tunnel_success"].format(ulke=ulke.upper()))
                print(T["ctrl_c_msg"])
                
                try:
                    while True:
                        proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                        
                        try:
                            requests.get("https://check.torproject.org/", proxies=proxies, timeout=10)
                            print(T["active_identity"].format(info=get_detailed_ip_info()))
                            time.sleep(15) 
                            
                        except Exception as e:
                            print(f"\n\033[91m{T['loc_lost'].format(e=e)}\033[0m")
                            if interface:
                                print(T["iptables_armor"])
                                
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
                                
                                print(T["tor_restart_clean"])
                                subprocess.run(["sudo", "systemctl", "restart", "tor"])
                                
                                print(f"\033[93m{T['wait_map']}\033[0m")
                                time.sleep(15) 
                                
                                set_tor_exit_node(ulke)
                                print(T["relock_loc"].format(ulke=ulke.upper()))
                                
                                secure_dns_start()
                                activate_kill_switch(interface)
                                print(f"\033[92m{T['repair_done']}\033[0m")
                            else:
                                print(f"\n\033[91m{T['no_interface_protect']}\033[0m")
                                break
                                
                except KeyboardInterrupt:
                    set_tor_exit_node(None)
                    print(T["loc_removed"])
                    time.sleep(1)
                finally:
                    secure_dns_stop()
                    clean_iptables_armor()
                    if interface:
                        deactivate_kill_switch(interface)
                    print(T["armor_closed"])
                    time.sleep(1)

            else:
                print(T["invalid_country"])
                time.sleep(2)

        elif secim == '4':
            print(T["mac_title"])
            print(T["mac_example"])
            interface = input(T["mac_prompt"]).strip()
            
            if interface:
                change_mac_address(interface)
                time.sleep(3)
            else:
                print(T["invalid_input"])
                time.sleep(2)

        elif secim == '5':
            print(T["wg_title"])
            print(T["wg_info"])
            print(T["wg_opt1"])
            print(T["wg_opt2"])
            print(T["wg_opt3"])
            
            wg_secim = input(T["wg_prompt"]).strip()
            
            if wg_secim == '1':
                conf_path = input(T["wg_conf_prompt"]).strip()
                if os.path.exists(conf_path):
                    set_tor_exit_node(None) 
                    clean_iptables_armor() 
                    if connect_wireguard(conf_path):
                        input(T["wg_close_prompt"])
                        disconnect_wireguard(conf_path)
                        time.sleep(2)
                else:
                    print(T["wg_not_found"].format(path=conf_path))
                    time.sleep(2)
                    
            elif wg_secim == '2':
                conf_path = input(T["wg_close_path_prompt"]).strip()
                if os.path.exists(conf_path):
                    disconnect_wireguard(conf_path)
                else:
                    print(T["wg_not_found_action"])
                time.sleep(2)
                
            elif wg_secim == '3':
                print(T["returning_main"])
                time.sleep(1)
            else:
                print(T["invalid_choice"])
                time.sleep(2)

        elif secim == '6':
            print("\n\033[93m" + "="*55)
            print(T["warp_title"])
            print("="*55 + "\033[0m")
            print(f"\033[91m{T['warp_privacy_warn']}\033[0m")
            print(T["warp_privacy_desc"])
            
            print(f"\033[93m{T['warp_mac_warn']}\033[0m")
            
            print(T["warp_opt1"])
            print(T["warp_opt2"])
            print(T["warp_opt3"])
            
            warp_secim = input(T["warp_prompt"]).strip()
            
            if warp_secim == '1':
                set_tor_exit_node(None)
                subprocess.run(["sudo", "systemctl", "stop", "tor"]) 
                
                print(T["clearing_locks"])
                clean_iptables_armor()
                if interface:
                    deactivate_kill_switch(interface)
                
                if connect_warp():
                    print(T["warp_wait"])
                    time.sleep(5) 
                    
                    print(T["warp_new_identity"].format(ip=get_current_ip()))
                    print(f"\033[93m{T['warp_speed_warn']}\033[0m")
                    
                    input(T["warp_close_prompt"])
                    disconnect_warp()
                    subprocess.run(["sudo", "systemctl", "start", "tor"]) 
                else:
                    input(T["warp_err_caught"])
                    
            elif warp_secim == '2':
                disconnect_warp()
                subprocess.run(["sudo", "systemctl", "start", "tor"]) 
                time.sleep(2)
                
            elif warp_secim == '3':
                print(T["returning_main"])
                time.sleep(1)
            
        elif secim == '7':
            print("\n\033[93m" + "="*55)
            print(T["mh_title"])
            print("="*55 + "\033[0m")
            print(T["mh_desc"])
            print(f"\033[91m{T['mh_warn']}\033[0m")
            
            giris = input(T["mh_in_prompt"]).strip()
            cikis = input(T["mh_out_prompt"]).strip()
            
            print(T["mh_intel_title"])
            print(T["mh_intel_0"])
            print(T["mh_intel_1"])
            print(T["mh_intel_2"])
            spy_secim = input(T["mh_intel_prompt"]).strip()
            
            spy_level = int(spy_secim) if spy_secim in ['0', '1', '2'] else 0
            
            interface = input(T["interface_prompt"]).strip()
            
            secure_dns_start()
            print(T["mh_building"])
            
            configure_multihop_circuit(giris if giris else None, cikis if cikis else None, True, spy_level)
            
            print(T["ctrl_c_msg"])
            try:
                while True:
                    proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                    try:
                        requests.get("https://check.torproject.org/", proxies=proxies, timeout=15)
                        print(T["mh_identity"].format(info=get_detailed_ip_info()))
                        time.sleep(30) 
                        
                    except Exception as e:
                        print(f"\n\033[91m{T['mh_broken'].format(e=e)}\033[0m")
                        if interface:
                            print(T["mh_shield"])
                            
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
                            
                            print(T["mh_tor_reset"])
                            subprocess.run(["sudo", "systemctl", "restart", "tor"])
                            
                            print(f"\033[93m{T['mh_wait_map']}\033[0m")
                            time.sleep(20) 
                            
                            print(T["mh_rebuilding"])
                            configure_multihop_circuit(giris if giris else None, cikis if cikis else None, True, spy_level)
                            
                            secure_dns_start()
                            activate_kill_switch(interface)
                            print(f"\033[92m{T['repair_done']}\033[0m")
                        else:
                            print(f"\n\033[91m{T['no_interface_warn']}\033[0m")
                            break
            except KeyboardInterrupt:
                print(T["mh_stopping"])
                configure_multihop_circuit(None, None, False, 0)
                time.sleep(1)
            finally:
                secure_dns_stop()
                clean_iptables_armor()
                if interface:
                    deactivate_kill_switch(interface)
                print(T["mh_closed"])
                time.sleep(1)
        
        elif secim == '8':
            print(T["exit_clearing"])
            clean_iptables_armor()
            print(T["exit_closing"])
            sys.exit(0) 
            
        else:
            print(f"\033[93m{T['invalid_choice_range']}\033[0m")
            time.sleep(1)
            continue

if __name__ == "__main__":
    clear_screen()
    select_language()
    clear_screen()
    check_tor_service()
    verify_connection()
    time.sleep(1) 
    clear_screen()
    print_banner()
    try:
        main()
    except KeyboardInterrupt:
        print(T["forced_exit"])
        clean_iptables_armor()
        sys.exit(0)