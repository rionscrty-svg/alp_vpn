# Alp VPN 🛡️

🌍 **[English](#english)** | 🇹🇷 **[Türkçe](#türkçe)**

---

<a id="türkçe"></a>
## 🇹🇷 Türkçe

### Sorumluluk Reddi 

**Bu yazılım tamamen eğitim ve siber güvenlik araştırmaları amacıyla geliştirilmiştir.**

Alp VPN'in kullanımı sırasında doğabilecek her türlü yasal sorumluluk tamamen son kullanıcıya aittir. Geliştirici (**Rion**), bu yazılımın yasa dışı faaliyetlerde, siber saldırılarda, yetkisiz erişimlerde veya yerel yasaları ihlal eden herhangi bir eylemde kullanılmasından sorumlu tutulamaz. 

Yazılımı indirerek ve kullanarak tüm riskleri ve hukuki sonuçları kabul etmiş sayılırsınız.

> **Unutmayın:** Hiçbir sistem %100 güvenli değildir. Gizliliğinizi korurken her zaman yerel yasalara ve etik kurallara uyun.

# Alp VPN 
Alp VPN, Linux sistemler için geliştirilmiş, üst düzey gizlilik sağlayan gelişmiş bir anonimlik aracıdır. Standart bir VPN'den farklı olarak Tor ağını, donanımsal Kill Switch'i, iptables tabanlı sızıntı korumasını ve MAC adresi manipülasyonunu tek bir terminal arayüzünde birleştirir.

**Geliştirici:** Rion

## Kurulum

Terminali açın ve aşağıdaki komutları sırasıyla çalıştırın:

```bash
git clone https://github.com/rionscrty-svg/alp_vpn.git
cd alp_vpn
sudo bash setup.sh
sudo resolvconf -u
sudo python3 alp_vpn.py
```

## Neden ALP VPN? (Yeni: Akıllı Zırh Teknolojisi)

Eski nesil güvenlik araçları bağlantı koptuğunda ağ kartınızı tamamen kapatarak donanımı yorar ve sistemi dondururdu. ALP VPN, baştan aşağı yenilenen **Akıllı Zırh (IPTables Kill Switch)** mimarisiyle çalışır:

* **Milisaniyelik Tepki:** Tor ağı veya VPN bağlantısı koptuğu anda, ağ donanımınız kapatılmadan sadece `iptables` üzerinden tüm trafik kilitlenir. Gerçek IP adresiniz bir milimetre bile dışarı sızamaz.
* **Geniş Linux Uyumluluğu:** Debian/Kali (`debian-tor`) ve Fedora/RedHat (`toranon`) sistemlerinin tamamında kullanıcı izinlerini otomatik tanır ve sorunsuz çalışır.
* **Sıfır Donanım Yıpranması:** Ağ yöneticisini (NetworkManager) sürekli yeniden başlatmaya gerek kalmaz, saatlerce Ghost Mode'da açık kalsa bile sisteminiz şişmez.
* **DNS Sızıntı Koruması:** `chattr` kilitleriyle DNS adresiniz `resolv.conf` üzerinden fiziksel olarak mühürlenir.

## Özellikler
- **Ghost Mode:** Sürekli ve otomatik değişen Tor kimlikleri.
- **Akıllı Kill-Switch:** Bağlantı koptuğunda "Connection Refused" mekanizmasıyla veriyi içeride tutar.
- **Cloudflare WARP Entegrasyonu:** Dinamik WireGuard tünellemesi ile hızlı anonimlik.
- **Kesin MAC Gizleme:** İnternet çıkışından önce ağ yöneticisini resetleyerek fiziksel kimliği (MAC) maskeler.

## İçindeki seçenekler 

 * Ghost Mode (Rastgele Ülke - 30s de bir IP değişir)
 * Custom Tor Profile (Süreyi Sen Seç)
 * Location Changer (Hedef Ülke Seçimi)
 * Mac Adresi Gizleme (Ağ yöneticisinden gizlenme / MAC Spoofing)
 * Custom Wireguard Node (Özel Sunucu / kendi wireguardın)   
 * High Speed Mode (Cloudflare Warp)
 * Multi-Hop (Sıçrama)
 * **!! Not !! Tor ağı tarayıcınızda çalışmaya ayarlanmıştır terminalden kullanılan araçlarla veya ek açılan uygulamalarla etkileşime girmez ( amacı dns ve killswitch ile veri sızıntısı olmaksızın internette gezinmek.).Tor ağını kullanırken FoxyProxy kullanılması tavsiye edilir**

## İletişim
* instagram : [https://www.instagram.com/rion.security/](https://www.instagram.com/rion.security/)
* github : 
* youtube :
* linkedin : 
* tiktok : https://www.tiktok.com/@rion.security

---

<a id="english"></a>
## 🇬🇧 English

### Disclaimer 

**This software is developed purely for educational and cybersecurity research purposes.**

All legal responsibilities that may arise during the use of Alp VPN belong entirely to the end user. The developer (**Rion**) cannot be held responsible for the use of this software in illegal activities, cyber attacks, unauthorized access, or any action that violates local laws. 

By downloading and using the software, you accept all risks and legal consequences.

> **Remember:** No system is 100% secure. Always comply with local laws and ethical rules while protecting your privacy.

# Alp VPN 
Alp VPN is an advanced anonymity tool developed for Linux systems that provides high-level privacy. Unlike a standard VPN, it combines the Tor network, hardware Kill Switch, iptables-based leak protection, and MAC address manipulation in a single terminal interface.

**Developer:** Rion

## Installation

Open the terminal and run the following commands sequentially:

```bash
git clone https://github.com/rionscrty-svg/alp_vpn.git
cd alp_vpn
sudo bash setup.sh
sudo resolvconf -u
sudo python3 alp_vpn.py
```

## Why ALP VPN? (New: Smart Armor Technology)

Older generation security tools would completely shut down your network card when the connection dropped, straining the hardware and freezing the system. ALP VPN operates with a completely revamped **Smart Armor (IPTables Kill Switch)** architecture:

* **Millisecond Response:** The moment the Tor network or VPN connection drops, all traffic is locked via `iptables` without shutting down your network hardware. Your real IP address cannot leak even a millimeter.
* **Broad Linux Compatibility:** Automatically recognizes user permissions and works flawlessly across all Debian/Kali (`debian-tor`) and Fedora/RedHat (`toranon`) systems.
* **Zero Hardware Wear:** No need to constantly restart the network manager (NetworkManager), your system won't bloat even if left open in Ghost Mode for hours.
* **DNS Leak Protection:** Your DNS address is physically sealed via `resolv.conf` with `chattr` locks.

## Features
- **Ghost Mode:** Continuous and automatically changing Tor identities.
- **Smart Kill-Switch:** Keeps data inside using a "Connection Refused" mechanism when the connection drops.
- **Cloudflare WARP Integration:** Fast anonymity with dynamic WireGuard tunneling.
- **Absolute MAC Spoofing:** Masks the physical identity (MAC) by resetting the network manager before internet egress.

## Included options 

 * Ghost Mode (Random Country - IP changes every 30s)
 * Custom Tor Profile (You Choose the Time)
 * Location Changer (Target Country Selection)
 * Mac Address Hiding (Hiding from network manager / MAC Spoofing)
 * Custom Wireguard Node (Private Server / your own wireguard)   
 * High Speed Mode (Cloudflare Warp)
 * Multi-Hop (Bounce)
 * **!! Note !! The Tor network is configured to work in your browser it does not interact with tools used from the terminal or additional opened applications (its purpose is to browse the internet without data leaks with dns and killswitch.). It is recommended to use FoxyProxy while using the Tor network**

## Contact
* instagram : [https://www.instagram.com/rion.security/](https://www.instagram.com/rion.security/)
* github : 
* youtube :
* linkedin : 
* tiktok : https://www.tiktok.com/@rion.security
