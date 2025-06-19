import os
import subprocess
import requests
import time

# Kalıcı depolama için özel klasör oluştur
PERSISTENT_DIR = "/home/user/persistent_data"
os.makedirs(PERSISTENT_DIR, exist_ok=True)
os.chmod(PERSISTENT_DIR, 0o777)

def setup_persistent_storage():
    """Kullanıcı verilerini kalıcı depolamaya bağlar"""
    home_dir = f"/home/{username}"
    persistent_links = {
        f"{home_dir}/.mozilla": f"{PERSISTENT_DIR}/.mozilla",
        f"{home_dir}/.config/google-chrome": f"{PERSISTENT_DIR}/.chrome",
        f"{home_dir}/.local/share/TelegramDesktop": f"{PERSISTENT_DIR}/.telegram",
        f"{home_dir}/.config/qBittorrent": f"{PERSISTENT_DIR}/.qbittorrent",
        f"{home_dir}/Desktop": f"{PERSISTENT_DIR}/Desktop"
    }
    
    for target, source in persistent_links.items():
        if not os.path.exists(source):
            os.makedirs(source, exist_ok=True)
        if os.path.exists(target):
            shutil.rmtree(target)
        os.symlink(source, target)
        print(f"Kalıcı bağlantı oluşturuldu: {target} → {source}")

def fix_network_issues():
    """Ağ bağlantı sorunlarını düzeltir"""
    # DNS ayarlarını düzelt
    os.system("sudo rm -f /etc/resolv.conf")
    os.system("sudo ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf")
    os.system("sudo systemctl restart systemd-resolved")
    
    # Temel ağ araçlarını yükle
    os.system("sudo apt install -y iputils-ping net-tools curl wget")
    
    # TCP optimizasyonları
    os.system("sudo sysctl -w net.ipv4.tcp_keepalive_time=60 net.ipv4.tcp_keepalive_intvl=60 net.ipv4.tcp_keepalive_probes=5")
    os.system("sudo sysctl -w net.core.rmem_max=12582912 net.core.wmem_max=12582912")
    
    print("Ağ sorunları düzeltildi ve optimizasyonlar uygulandı")

def is_internet_working():
    """İnternet bağlantısını kontrol eder"""
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return response.status_code == 200
    except:
        return False

def install_firefox_esr():
    """Firefox ESR kurulumu"""
    print("Firefox ESR kuruluyor...")
    os.system("sudo apt install -y firefox-esr")
    
    # Firefox için kalıcı depolama bağlantısı
    firefox_profile = f"{PERSISTENT_DIR}/.mozilla/firefox"
    os.makedirs(firefox_profile, exist_ok=True)
    os.system(f"rm -rf /home/{username}/.mozilla")
    os.system(f"ln -s {firefox_profile} /home/{username}/.mozilla")
    
    print("Firefox ESR başarıyla kuruldu!")

# Kullanıcı bilgileri
username = "user"
password = "root"
Pin = 123456
Autostart = True

# Kullanıcı oluştur
os.system(f"sudo useradd -m {username}")
os.system(f"echo '{username}:{password}' | sudo chpasswd")
os.system(f"sudo usermod -aG sudo {username}")
os.system("sudo sed -i 's/\/bin\/sh/\/bin\/bash/g' /etc/passwd")

# Ağ sorunlarını düzelt
fix_network_issues()

# CRD kodunu al
CRD_SSH_Code = input("Google CRD SSH Kodunu girin: ").strip()
if not CRD_SSH_Code:
    print("Hata: Geçerli bir CRD kodu girmediniz!")
    exit(1)

class EnhancedCRDSetup:
    def __init__(self, user):
        self.user = user
        self.start_time = time.time()
        
        print("\n" + "="*50)
        print("Gelişmiş CRD Kurulumu Başlatılıyor".center(50))
        print("="*50 + "\n")
        
        # Kurulum sırasını optimize et
        self.install_dependencies()
        self.install_crd()
        self.install_desktop_environment()
        self.install_google_chrome()
        install_firefox_esr()  # Firefox ESR kurulumu
        self.install_telegram()
        self.install_qbittorrent()
        self.changewall()
        self.finish_setup()
        
        self.print_success_message()

    def install_dependencies(self):
        """Gerekli bağımlılıkları yükler"""
        print("Temel bağımlılıklar kuruluyor...")
        os.system("sudo apt update -y")
        os.system("sudo apt install -y software-properties-common apt-transport-https ca-certificates")
        os.system("sudo apt --fix-broken install -y")
        print("Bağımlılıklar başarıyla kuruldu!")

    def install_crd(self):
        """Chrome Remote Desktop kurulumu"""
        print("Chrome Remote Desktop kuruluyor...")
        
        # Mevcut kurulumu temizle
        os.system("sudo apt purge -y chrome-remote-desktop")
        os.system("sudo rm -f /tmp/chrome-remote-desktop_current_amd64.deb")
        
        # En son sürümü indir ve kur
        os.system("wget https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb -O /tmp/crd.deb")
        os.system("sudo dpkg -i /tmp/crd.deb || sudo apt install -fy")
        
        # CRD servisini yapılandır
        os.system("sudo systemctl enable chrome-remote-desktop.service")
        print("Chrome Remote Desktop başarıyla kuruldu!")

    def install_desktop_environment(self):
        """XFCE masaüstü ortamını kurar"""
        print("XFCE Masaüstü Ortamı kuruluyor...")
        os.system("sudo DEBIAN_FRONTEND=noninteractive apt install -y xfce4 xfce4-goodies xserver-xorg-video-dummy")
        
        # CRD oturum yapılandırması
        os.system("sudo bash -c \"echo 'exec /etc/X11/Xsession /usr/bin/xfce4-session --disable-tcp-wrapper' > /etc/chrome-remote-desktop-session\"")
        
        # Gerekli servisleri başlat
        os.system("sudo apt install -y dbus-x11")
        os.system("sudo service dbus start")
        print("XFCE başarıyla kuruldu!")

    def install_google_chrome(self):
        """Google Chrome kurulumu"""
        print("Google Chrome kuruluyor...")
        os.system("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb")
        os.system("sudo dpkg -i /tmp/chrome.deb || sudo apt install -fy")
        print("Google Chrome başarıyla kuruldu!")

    def install_telegram(self):
        """Telegram Desktop kurulumu"""
        print("Telegram Desktop kuruluyor...")
        os.system("sudo apt install -y telegram-desktop")
        print("Telegram başarıyla kuruldu!")

    def install_qbittorrent(self):
        """qBittorrent kurulumu"""
        print("qBittorrent kuruluyor...")
        os.system("sudo apt install -y qbittorrent")
        print("qBittorrent başarıyla kuruldu!")

    def changewall(self):
        """Duvar kağıdını özelleştir"""
        print("Özel duvar kağıdı uygulanıyor...")
        wall_dir = f"/home/{self.user}/.local/share/xfce4/backdrops"
        os.makedirs(wall_dir, exist_ok=True)
        os.system(f"wget https://gitlab.com/chamod12/gcrd_deb_codesandbox.io_rdp/-/raw/main/walls/1920x1080.svg -O {wall_dir}/xfce-wall.svg")
        print("Duvar kağıdı başarıyla uygulandı!")

    def finish_setup(self):
        """Kurulumu tamamlar ve CRD'yi başlatır"""
        print("Kurulum tamamlanıyor...")
        
        # Kullanıcıyı CRD grubuna ekle
        os.system(f"sudo adduser {self.user} chrome-remote-desktop")
        
        # CRD oturumunu başlat
        command = f"{CRD_SSH_Code} --pin={Pin}"
        os.system(f"sudo -u {self.user} dbus-launch --exit-with-session {command}")
        
        # CRD servisini başlat
        os.system("sudo service chrome-remote-desktop start")
        
        # Kalıcı depolamayı ayarla
        setup_persistent_storage()

    def print_success_message(self):
        """Başarı mesajını ve erişim bilgilerini gösterir"""
        duration = int(time.time() - self.start_time)
        print("\n" + "="*50)
        print("KURULUM BAŞARIYLA TAMAMLANDI!".center(50))
        print("="*50)
        print(f"Süre: {duration} saniye")
        print(f"Kullanıcı Adı: {username}")
        print(f"Şifre: {password}")
        print(f"CRD PIN: {Pin}")
        print("-"*50)
        print("Firefox ESR ve Google Chrome kuruldu")
        print("Tüm veriler kalıcı depolamaya kaydedilecek")
        print("="*50)
        print("Bağlantı bilgileri hazır! Chrome Remote Desktop ile bağlanabilirsiniz.")

# Kurulumu başlat
try:
    if not is_internet_working():
        print("İnternet bağlantısı kontrol ediliyor...")
        fix_network_issues()
        time.sleep(3)
        
        if not is_internet_working():
            print("Hata: İnternet bağlantısı sağlanamadı!")
            exit(1)
    
    EnhancedCRDSetup(username)
except Exception as e:
    print(f"Kritik hata: {str(e)}")
    print("Lütfen konsol çıktısını kontrol edin ve tekrar deneyin")
