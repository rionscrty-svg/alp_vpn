#!/bin/bash

# Renk Tanımlamaları
CYAN='\033[0;96m'
GREEN='\033[0;92m'
RED='\033[0;91m'
YELLOW='\033[0;93m'
NC='\033[0m' # Renk sıfırlama

# 1. Sudo Kontrolü (Her iki dilde de hata verir ki kullanıcı anlasın)
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[-] ERROR: Please run this script with 'sudo bash setup.sh'!${NC}"
  echo -e "${RED}[-] HATA: Lütfen bu scripti 'sudo bash setup.sh' şeklinde çalıştırın!${NC}"
  exit 1
fi

clear

# 2. Dil Seçimi Menüsü
echo -e "${CYAN}=== ALP VPN SETUP / KURULUM ===${NC}"
echo "1) English"
echo "2) Türkçe"
read -p "Choice / Seçim [1-2]: " lang_choice

if [ "$lang_choice" == "1" ]; then
    L_OS_DETECT="[*] Detected OS:"
    L_PKG_UPDATE="[*] Updating package lists..."
    L_UNSUPPORTED="[-] Unsupported distribution:"
    L_DOWNLOADING="\n[*] Downloading required system packages..."
    L_INSTALLING="[+] Installing package:"
    L_PKG_ERR="[-] ERROR: Failed to install package. Check your internet connection:"
    L_TOR_CFG="[+] Updating Tor configuration file..."
    L_CLEAN_ORPHAN="[+] Cleaning up potential orphan Tor processes in the background..."
    L_START_TOR="[+] Starting Tor service..."
    L_WAIT_TOR="[*] Waiting for Tor service to be ready..."
    L_TOR_SUCCESS="[+] Tor service successfully activated and listening!"
    L_TOR_WARN="[!] Warning: Tor started but ports are not responding yet. Please check 'sudo systemctl status tor'."
    L_SELINUX_CHECK="[+] Checking SELinux security rules..."
    L_SELINUX_APPLY="[+] Rule found, applying..."
    L_SELINUX_WARN="[!] Warning: 'tor_can_network_connect' rule not found on the system, continuing setup."
    L_USER_GROUP_1="[+] User"
    L_USER_GROUP_2="added to group"
    L_GROUP_WARN="[!] Warning: Tor group could not be found automatically. Please check manually."
    L_SUDO_WARN="[!] Sudo user could not be detected."
    L_CHMOD="[+] Setting file execution permissions..."
    L_SUCCESS="[+] SETUP SUCCESSFUL!!!!"
    L_REBOOT="[!] PLEASE log out and log back in (or reboot) for Tor group changes to take effect."
    L_RUN="[*] Command to start the program: sudo python3 alp_vpn.py"
else
    L_OS_DETECT="[*] İşletim Sistemi Tespit Edildi:"
    L_PKG_UPDATE="[*] Paket listeleri güncelleniyor..."
    L_UNSUPPORTED="[-] Desteklenmeyen dağıtım:"
    L_DOWNLOADING="\n[*] Gerekli sistem paketleri indiriliyor..."
    L_INSTALLING="[+] Paketi kuruluyor:"
    L_PKG_ERR="[-] HATA: Paket kurulamadı. İnternet bağlantınızı kontrol edin:"
    L_TOR_CFG="[+] Tor yapılandırma dosyası güncelleniyor..."
    L_CLEAN_ORPHAN="[+] Arka plandaki olası yetim Tor süreçleri temizleniyor..."
    L_START_TOR="[+] Tor servisi başlatılıyor..."
    L_WAIT_TOR="[*] Tor servisinin hazır olması bekleniyor..."
    L_TOR_SUCCESS="[+] Tor servisi başarıyla aktif edildi ve dinleniyor!"
    L_TOR_WARN="[!] Uyarı: Tor servisi başlatıldı ancak portlar henüz yanıt vermiyor. Lütfen 'sudo systemctl status tor' komutunu kontrol edin."
    L_SELINUX_CHECK="[+] SELinux güvenlik kuralları kontrol ediliyor..."
    L_SELINUX_APPLY="[+] Kural bulundu, uygulanıyor..."
    L_SELINUX_WARN="[!] Uyarı: 'tor_can_network_connect' kuralı şu an sistemde bulunamadı, kurulum devam ediyor."
    L_USER_GROUP_1="[+] Kullanıcı"
    L_USER_GROUP_2="grubuna eklendi."
    L_GROUP_WARN="[!] Uyarı: Tor grubu otomatik bulunamadı. Lütfen manuel kontrol edin."
    L_SUDO_WARN="[!] Sudo kullanıcısı tespit edilemedi."
    L_CHMOD="[+] Dosya çalıştırma izinleri ayarlanıyor..."
    L_SUCCESS="[+] KURULUM BAŞARILI!!!!"
    L_REBOOT="[!] Tor grubu değişikliklerinin aktif olması için LÜTFEN oturumu kapatıp açın (veya sistemi yeniden başlatın)."
    L_RUN="[*] Programı başlatmak için komutunuz: sudo python3 alp_vpn.py"
fi

# 3. Sistem Bilgileri
. /etc/os-release
echo -e "${CYAN}${L_OS_DETECT} ${NAME}${NC}"

# 4. Paket Yöneticisi ve Paket İsimlerini Tanımla
case "$ID" in
    arch|manjaro|endeavouros)
        PKG_MGR="pacman -Sy --noconfirm"
        TOR_GROUP="tor"
        PACKAGES="tor python-stem python-requests python-pysocks macchanger wireguard-tools iptables e2fsprogs curl"
        ;;
    fedora|rhel|centos|almalinux|rocky)
        PKG_MGR="dnf install -y"
        TOR_GROUP="tor"
        IS_FEDORA=true
        PACKAGES="tor python3-stem python3-requests python3-pysocks macchanger wireguard-tools iptables e2fsprogs curl"
        ;;
    debian|ubuntu|kali|linuxmint|pop|zorin|elementary|devuan)
        echo -e "${CYAN}${L_PKG_UPDATE}${NC}"
        apt-get update -y > /dev/null 2>&1
        PKG_MGR="apt-get install -y"
        TOR_GROUP="debian-tor"
        PACKAGES="tor python3-stem python3-requests python3-socks macchanger wireguard-tools iptables e2fsprogs curl openresolv"
        ;;
    *)
        echo -e "${RED}${L_UNSUPPORTED} $ID${NC}"
        exit 1
        ;;
esac

# 5. Kurulum Döngüsü (Toplu Yükleme)
echo -e "${CYAN}${L_DOWNLOADING}${NC}"
for pkg in $PACKAGES; do
    echo -e "${CYAN}${L_INSTALLING} '$pkg'...${NC}"
    $PKG_MGR $pkg > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${RED}${L_PKG_ERR} '$pkg'${NC}"
        exit 1
    fi
done

# 6. Tor Ayarlarını Yaz
echo -e "${CYAN}${L_TOR_CFG}${NC}"
sudo bash -c 'cat <<EOF > /etc/tor/torrc
SocksPort 127.0.0.1:9050
ControlPort 127.0.0.1:9051
CookieAuthentication 1
CookieAuthFileGroupReadable 1
EOF'

# 7. Servisi Çalıştır (Port çakışmaları ve servis engelleri temizleniyor)
echo -e "${CYAN}${L_CLEAN_ORPHAN}${NC}"
killall -q -9 tor 2>/dev/null 

echo -e "${CYAN}${L_START_TOR}${NC}"
systemctl unmask tor 2>/dev/null
systemctl unmask tor@default 2>/dev/null
systemctl daemon-reload

systemctl enable tor >/dev/null 2>&1
systemctl restart tor

# Portların aktifleşmesi için kısa bir süre bekle ve doğrulama yap
echo -e "${YELLOW}${L_WAIT_TOR}${NC}"
TOR_ACTIVE=false
for i in {1..5}; do
    if ss -antp 2>/dev/null | grep -E "9050|9051" >/dev/null; then
        TOR_ACTIVE=true
        break
    fi
    sleep 1
done

if [ "$TOR_ACTIVE" = true ]; then
    echo -e "${GREEN}${L_TOR_SUCCESS}${NC}"
else
    echo -e "${RED}${L_TOR_WARN}${NC}"
fi

# 8. Güvenlik Ayarları (Sadece SELinux aktifse)
if [ "$IS_FEDORA" = true ] && command -v selinuxenabled >/dev/null && selinuxenabled 2>/dev/null; then
    echo -e "${CYAN}${L_SELINUX_CHECK}${NC}"
    if getsebool tor_can_network_connect &>/dev/null; then
        echo -e "${GREEN}${L_SELINUX_APPLY}${NC}"
        sudo setsebool -P tor_can_network_connect 1
    else
        echo -e "${YELLOW}${L_SELINUX_WARN}${NC}"
    fi
fi

# 9. Kullanıcıyı Yetkilendir (Daha güvenli yöntem)
sleep 2 

if [ -n "$SUDO_USER" ]; then
    TARGET_GROUP=$(getent group | grep -E '^(tor|debian-tor)' | cut -d: -f1 | head -n 1)
    
    if [ -n "$TARGET_GROUP" ]; then
        usermod -aG "$TARGET_GROUP" "$SUDO_USER"
        echo -e "${GREEN}${L_USER_GROUP_1} '$SUDO_USER' ${L_USER_GROUP_2} '$TARGET_GROUP'${NC}"
    else
        echo -e "${YELLOW}${L_GROUP_WARN}${NC}"
    fi
else
    echo -e "${YELLOW}${L_SUDO_WARN}${NC}"
fi

# 10. Dosya İzinleri
echo -e "${CYAN}${L_CHMOD}${NC}"
chmod +x alp_vpn.py alp_core.py 2>/dev/null

# 11. Bitiş Ekranı
echo "----------------------------------------------------"
echo -e "${GREEN}${L_SUCCESS}${NC}"
echo -e "${YELLOW}${L_REBOOT}${NC}"
echo -e "${CYAN}${L_RUN}${NC}"
echo "----------------------------------------------------"