#!/bin/bash

# 1. Sudo Kontrolü
if [ "$EUID" -ne 0 ]; then
  echo "[-] HATA: Lütfen bu scripti 'sudo bash setup.sh' şeklinde çalıştırın!"
  exit 1
fi

# 2. Sistem Bilgileri
. /etc/os-release
echo "[*] İşletim Sistemi Tespit Edildi: $NAME"

# 3. Paket Yöneticisi ve Paket İsimlerini Tanımla
case "$ID" in
    arch|manjaro|endeavouros)
        PKG_MGR="pacman -Sy --noconfirm"
        TOR_GROUP="tor"
        # Arch Linux'ta python paket isimleri 'python-' ile başlar.
        PACKAGES="tor python-stem python-requests python-pysocks macchanger wireguard-tools iptables e2fsprogs curl"
        ;;
    fedora|rhel|centos|almalinux|rocky)
        PKG_MGR="dnf install -y"
        TOR_GROUP="tor"
        IS_FEDORA=true
        PACKAGES="tor python3-stem python3-requests python3-pysocks macchanger wireguard-tools iptables e2fsprogs curl"
        ;;
   debian|ubuntu|kali|linuxmint|pop|zorin|elementary|devuan)
        echo "[*] Paket listeleri güncelleniyor..."
        apt-get update -y > /dev/null 2>&1
        PKG_MGR="apt-get install -y"
        TOR_GROUP="debian-tor"
        # openresolv paketi listenin sonuna eklendi
        PACKAGES="tor python3-stem python3-requests python3-socks macchanger wireguard-tools iptables e2fsprogs curl openresolv"
        ;;
    *)
        echo "[-] Desteklenmeyen dağıtım: $ID"
        exit 1
        ;;
esac

# 4. Kurulum Döngüsü (Toplu Yükleme)
echo -e "\n[*] Gerekli sistem paketleri indiriliyor..."
for pkg in $PACKAGES; do
    echo "[+] '$pkg' paketi kuruluyor..."
    $PKG_MGR $pkg > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "[-] HATA: '$pkg' paketi kurulamadı. İnternet bağlantınızı kontrol edin."
        exit 1
    fi
done

# 5. Tor Ayarlarını Yaz
echo "[+] Tor yapılandırma dosyası güncelleniyor..."
sudo bash -c 'cat <<EOF > /etc/tor/torrc
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
RunAsDaemon 1
EOF'

# 6. Servisi Çalıştır
echo "[+] Tor servisi başlatılıyor..."
systemctl enable --now tor
systemctl restart tor

# 7. Güvenlik Ayarları (Sadece SELinux aktifse ve kural tanımlıysa çalıştır)
if [ "$IS_FEDORA" = true ] && command -v selinuxenabled >/dev/null && selinuxenabled 2>/dev/null; then
    echo "[+] SELinux güvenlik kuralları kontrol ediliyor..."
    
    # Sadece 'tor_can_network_connect' boole'u sistemde varsa çalıştır
    if getsebool tor_can_network_connect &>/dev/null; then
        echo "[+] Kural bulundu, uygulanıyor..."
        sudo setsebool -P tor_can_network_connect 1
    else
        echo "[!] Uyarı: 'tor_can_network_connect' kuralı şu an sistemde bulunamadı, kurulum devam ediyor."
    fi
fi

# 8. Kullanıcıyı Yetkilendir (Daha güvenli yöntem)
# Önce grubun oluşması için 2 saniye bekle
sleep 2 

if [ -n "$SUDO_USER" ]; then
    # Tor grubunu bulmaya çalış (debian-tor veya tor olabilir)
    TARGET_GROUP=$(getent group | grep -E '^(tor|debian-tor)' | cut -d: -f1 | head -n 1)
    
    if [ -n "$TARGET_GROUP" ]; then
        usermod -aG "$TARGET_GROUP" "$SUDO_USER"
        echo "[+] Kullanıcı '$SUDO_USER', '$TARGET_GROUP' grubuna eklendi."
    else
        echo "[!] Uyarı: Tor grubu otomatik bulunamadı. Lütfen manuel kontrol edin."
    fi
else
    echo "[!] Sudo kullanıcısı tespit edilemedi."
fi

# 9. Dosya İzinleri
echo "[+] Dosya çalıştırma izinleri ayarlanıyor..."
chmod +x alp_vpn.py alp_core.py 2>/dev/null

echo "----------------------------------------------------"
echo -e "\e[92m[+] KURULUM BAŞARILI!!!!\e[0m"
echo "[!] Tor grubu değişikliklerinin aktif olması için LÜTFEN oturumu kapatıp açın (veya sistemi yeniden başlatın)."
echo "[*] Programı başlatmak için komutunuz: sudo python3 alp_vpn.py"
echo "----------------------------------------------------"