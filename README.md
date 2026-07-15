# ALP VPN 🛡️

🌍 **[English](#english)** | 🇹🇷 **[Türkçe](#türkçe)**

---

<a id="english"></a>
## 🇬🇧 English

### Disclaimer
**This software is developed purely for educational and cybersecurity research purposes.**

All legal responsibilities that may arise during the use of Alp VPN belong entirely to the end user. The developer (**Rion**) cannot be held responsible for the use of this software in illegal activities, cyber attacks, unauthorized access, or any action that violates local laws.

By downloading and using the software, you accept all risks and legal consequences.

> **Remember:** No system is 100% secure. Always comply with local laws and ethical rules while protecting your privacy.

### About Alp VPN
Alp VPN is an advanced anonymity tool developed for Linux systems that provides high-level privacy. Unlike a standard VPN, it combines the Tor network, a software-based Kill Switch, iptables-based leak protection, and MAC address manipulation into a single terminal interface.

**Developer:** Rion

### Installation
Open your terminal and run the following commands sequentially:

```bash
git clone [https://github.com/rionscrty-svg/alp_vpn.git](https://github.com/rionscrty-svg/alp_vpn.git)
cd alp_vpn
sudo bash setup.sh
sudo resolvconf -u
sudo python3 alp_vpn.py