## Sorumluluk Reddi 

**Bu yazılım tamamen eğitim ve siber güvenlik araştırmaları amacıyla geliştirilmiştir.**

Alp VPN'in kullanımı sırasında doğabilecek her türlü yasal sorumluluk tamamen son kullanıcıya aittir. Geliştirici (**Rion**), bu yazılımın yasa dışı faaliyetlerde, siber saldırılarda, yetkisiz erişimlerde veya yerel yasaları ihlal eden herhangi bir eylemde kullanılmasından sorumlu tutulamaz. 

Yazılımı indirerek ve kullanarak tüm riskleri ve hukuki sonuçları kabul etmiş sayılırsınız.

> **Unutmayın:** Hiçbir sistem %100 güvenli değildir. Gizliliğinizi korurken her zaman yerel yasalara ve etik kurallara uyun.

# Alp VPN 
Alp VPN, Linux sistemler için geliştirilmiş, üst düzey gizlilik sağlayan gelişmiş bir anonimlik aracıdır. Standart bir VPN'den farklı olarak Tor ağını, donanımsal Kill Switch'i, iptables tabanlı sızıntı korumasını ve MAC adresi manipülasyonunu tek bir terminal arayüzünde birleştirir.

**Geliştirici:** Rion

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
 * Custom Wireguard Node (Özel Sunucu / kendi wireguardın)  >> eğer işletim sisteminizi kapsayan bir güvenlik istiyorsanız bunu seçmelisiniz <<  
 * High Speed Mode (Cloudflare Warp)
 * Multi-Hop (Sıçrama)
 * **!! Not !! Tor ağı tarayıcınızda çalılışmaya ayarlanmıştır terminalden kullanılan araçlarla veya ek açılan uygulamalarla etkileşime girmez ( amacı dns ve killswitch ile veri sızıntısı olmaksızın internette gezinmek.)**
##  Kurulum

Terminali açın ve aşağıdaki komutları sırasıyla çalıştırın:

```bash
git clone [https://github.com/KULLANICI_ADIN/alp_vpn.git](https://github.com/KULLANICI_ADIN/alp_vpn.git)
cd alp_vpn
sudo bash setup.sh


---------------iletişim plartformlarım------------------
.--------------------------------------------------------.
instagram : https://www.instagram.com/rion.security/
github : 
youtube :
linkedin : 
tiktok : 
.-------------------------------------------------------.
