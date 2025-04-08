@echo off
chcp 1254 >nul
setlocal enabledelayedexpansion
mode con cols=80 lines=35
title Pip-Boy 3000 - Corel Kontrol Terminali
color 0A

:: Ses fonksiyonları
call :yukleBeepFonksiyonu

:: Başlangıç ekranı
cls
echo.
echo.
echo      ██████╗ ██╗██████╗       ██████╗  ██████╗ ██╗   ██╗
echo      ██╔══██╗██║██╔══██╗      ██╔══██╗██╔═══██╗╚██╗ ██╔╝
echo      ██████╔╝██║██████╔╝█████╗██████╔╝██║   ██║ ╚████╔╝ 
echo      ██╔═══╝ ██║██╔═══╝ ╚════╝██╔══██╗██║   ██║  ╚██╔╝  
echo      ██║     ██║██║           ██████╔╝╚██████╔╝   ██║   
echo      ╚═╝     ╚═╝╚═╝           ╚═════╝  ╚═════╝    ╚═╝   
echo.
echo           ██████╗ ██████╗ ██████╗ ███████╗██╗     
echo          ██╔════╝██╔═══██╗██╔══██╗██╔════╝██║     
echo          ██║     ██║   ██║██████╔╝█████╗  ██║     
echo          ██║     ██║   ██║██╔══██╗██╔══╝  ██║     
echo          ╚██████╗╚██████╔╝██║  ██║███████╗███████╗
echo           ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
echo.
echo               ***** VAULT-TEC KONTROL SİSTEMİ *****
echo.
echo          Sistem başlatılıyor...
call :beep 700 100
ping -n 1 127.0.0.1 >nul
call :beep 900 100
ping -n 2 127.0.0.1 >nul
call :beep 500 100
ping -n 1 127.0.0.1 >nul
call :beep 1000 200
echo          Hoş geldiniz, %username%!
ping -n 3 127.0.0.1 >nul

:anamenu
cls
call :beep 500 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                   PIP-BOY 3000 - COREL KONTROL SİSTEMİ                     ║
echo ╠════════════════════════════════════════════════════════════════════════════╣
echo ║                                                                            ║
echo ║ [1] ► Corel uygulamasını sonlandır                                         ║
echo ║                                                                            ║
echo ║ [2] ► Corel kullanıcı verilerini temizle                                   ║
echo ║                                                                            ║
echo ║ [3] ► Tam sistem bakımı (Kapat ve verileri temizle)                        ║
echo ║                                                                            ║
echo ║ [4] ► Yedekleme yap ve sonra temizle                                       ║
echo ║                                                                            ║
echo ║ [5] ► Corel internet erişimi yönetimi                                      ║
echo ║                                                                            ║
echo ║ [6] ► Sistem bilgilerini görüntüle                                         ║
echo ║                                                                            ║
echo ║ [7] ► Çıkış                                                                ║
echo ║                                                                            ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo ►► VAULT-TEC DİKKAT: Lütfen bir seçenek seçin.
set /p secim="►► Seçiminiz (1-7): "
call :beep 800 50

if "%secim%"=="1" goto kapat
if "%secim%"=="2" goto verisil
if "%secim%"=="3" goto tamtemizlik
if "%secim%"=="4" goto yedekle
if "%secim%"=="5" goto internetyonet
if "%secim%"=="6" goto sistembilgi
if "%secim%"=="7" goto cikis

call :beep 300 200
echo.
echo !! GEÇERSİZ SEÇİM !! Lütfen 1-7 arasında bir numara girin.
echo.
ping -n 3 127.0.0.1 >nul
goto anamenu

:kapat
cls
call :beep 600 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                          UYGULAMA SONLANDIRMA                              ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo  ► Corel Draw uygulaması aranıyor ve sonlandırılıyor...
echo.
call :beep 500 50
call :beep 600 50
call :beep 700 50
taskkill /IM "CorelDrw.exe" /F
if %errorlevel% equ 0 (
    call :beep 900 100
    echo  ✓ Corel Draw başarıyla sonlandırıldı.
    echo.
    echo  █ █ █ █ █ █ █ █ █ █ █ █ █ 100%% TAMAMLANDI █ █ █ █ █ █ █ █ █ █ █ █ █
) else (
    call :beep 300 200
    echo  ! Corel Draw zaten çalışmıyor veya sonlandırılamadı.
    echo.
    echo  █ █ █ █ █                   40%% BAŞARISIZ █ █ █ █ █ 
)
echo.
echo  ► İşlem tamamlandı. Devam etmek için ENTER tuşuna basın...
pause >nul
goto anamenu

:verisil
cls
call :beep 600 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                    COREL VERİ TEMİZLEME İŞLEMİ                             ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo  !!! UYARI: Bu işlem tüm Corel kullanıcı verilerinizi silecektir !!!
echo.
echo  █ Bu işlem geri alınamaz ve aşağıdaki verileri siler:
echo    ├─ Kullanıcı ayarları
echo    ├─ Çalışma alanı düzenleri
echo    ├─ Özelleştirilmiş kısayollar
echo    └─ Program tercihleri
echo.
set /p onay="  ► İşlemi onaylıyor musunuz? (E/H): "
if /i "%onay%"=="E" (
    echo.
    echo  ► Corel kullanıcı verileri siliniyor...
    call :beep 500 50
    call :beep 600 50
    call :beep 700 50
    if exist "C:\Users\%username%\AppData\Roaming\Corel" (
        rmdir /S /Q "C:\Users\%username%\AppData\Roaming\Corel"
        call :beep 900 100
        echo.
        echo  ✓ Corel kullanıcı verileri başarıyla silindi.
        echo.
        echo  █ █ █ █ █ █ █ █ █ █ █ █ █ 100%% TAMAMLANDI █ █ █ █ █ █ █ █ █ █ █ █ █
    ) else (
        call :beep 300 200
        echo.
        echo  ! Corel kullanıcı verileri bulunamadı.
        echo  ! Silme işlemi gerçekleştirilemedi.
        echo.
        echo  █ █ █ █ █                  40%% BAŞARISIZ █ █ █ █ █
    )
) else (
    call :beep 300 200
    echo.
    echo  ! İşlem iptal edildi.
)
echo.
echo  ► Ana menüye dönmek için ENTER tuşuna basın...
pause >nul
goto anamenu

:tamtemizlik
cls
call :beep 600 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                         TAM SİSTEM BAKIMI                                  ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo  !!! UYARI !!! 
echo  Bu işlem Corel Draw'ı kapatacak ve tüm verilerinizi temizleyecektir.
echo.
set /p onay="  ► İşlemi onaylıyor musunuz? (E/H): "
if /i "%onay%"=="E" (
    echo.
    echo  ► Tam bakım işlemi başlatılıyor...
    echo.
    echo  [1/2] Corel Draw sonlandırılıyor...
    call :beep 500 50
    taskkill /IM "CorelDrw.exe" /F
    if %errorlevel% equ 0 (
        echo  ✓ Corel Draw başarıyla sonlandırıldı.
    ) else (
        echo  ! Corel Draw zaten çalışmıyor veya sonlandırılamadı.
    )
    
    echo.
    echo  [2/2] Corel kullanıcı verileri temizleniyor...
    call :beep 600 50
    if exist "C:\Users\%username%\AppData\Roaming\Corel" (
        rmdir /S /Q "C:\Users\%username%\AppData\Roaming\Corel"
        call :beep 900 100
        echo  ✓ Corel kullanıcı verileri başarıyla silindi.
        echo.
        echo  █ █ █ █ █ █ █ █ █ █ █ █ █ 100%% TAMAMLANDI █ █ █ █ █ █ █ █ █ █ █ █ █
    ) else (
        call :beep 300 200
        echo  ! Corel kullanıcı verileri bulunamadı.
        echo.
        echo  █ █ █ █ █ █ █ █ █ █ █      80%% TAMAMLANDI █ █ █ █ █ █ █ █ █ █ █
    )
) else (
    call :beep 300 200
    echo.
    echo  ! İşlem iptal edildi.
)
echo.
echo  ► Ana menüye dönmek için ENTER tuşuna basın...
pause >nul
goto anamenu

:yedekle
cls
call :beep 600 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                       VERİ YEDEKLEME VE TEMİZLEME                          ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

if not exist "C:\Users\%username%\AppData\Roaming\Corel" (
    call :beep 300 200
    echo  ! Yedeklenecek Corel kullanıcı verileri bulunamadı.
    echo.
    echo  ► Ana menüye dönmek için ENTER tuşuna basın...
    pause >nul
    goto anamenu
)

echo  ► Yedekleme ve temizleme işlemi başlatılıyor...
echo.

set tarih=%date:~10,4%%date:~7,2%%date:~4,2%
set zaman=%time:~0,2%%time:~3,2%
if "%zaman:~0,1%"==" " set zaman=0%zaman:~1,3%
set yedek_klasor=%userprofile%\Desktop\Corel_Yedek_%tarih%_%zaman%

echo  [1/4] Yedekleme klasörü oluşturuluyor...
call :beep 500 50
mkdir "%yedek_klasor%"
echo  ✓ Yedekleme klasörü oluşturuldu: %yedek_klasor%
echo.

echo  [2/4] Kullanıcı verileri yedekleniyor...
call :beep 600 50
xcopy "C:\Users\%username%\AppData\Roaming\Corel" "%yedek_klasor%" /E /I /H /Y >nul
echo  ✓ Veriler başarıyla yedeklendi.
echo.

echo  [3/4] Corel Draw sonlandırılıyor...
call :beep 700 50
taskkill /IM "CorelDrw.exe" /F >nul
echo  ✓ Corel Draw sonlandırıldı.
echo.

echo  [4/4] Corel kullanıcı verileri siliniyor...
call :beep 800 50
rmdir /S /Q "C:\Users\%username%\AppData\Roaming\Corel"
call :beep 900 100
echo  ✓ Corel kullanıcı verileri temizlendi.
echo.

echo  █ █ █ █ █ █ █ █ █ █ █ █ █ 100%% TAMAMLANDI █ █ █ █ █ █ █ █ █ █ █ █ █
echo.
echo  ✓ Yedekleme ve temizleme işlemi başarıyla tamamlandı!
echo  ✓ Yedek Konumu: %yedek_klasor%
echo.
echo  ► Ana menüye dönmek için ENTER tuşuna basın...
pause >nul
goto anamenu

:internetyonet
cls
call :beep 600 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                    COREL İNTERNET ERİŞİM YÖNETİMİ                          ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo  ► Lütfen yapmak istediğiniz işlemi seçin:
echo.
echo  [1] Corel ürünleri için gelen bağlantıları engelle
echo  [2] Corel ürünleri için giden bağlantıları engelle
echo  [3] Corel ürünleri için tüm internet erişimini engelle
echo  [4] Corel ürünleri için internet erişim engelini kaldır
echo  [5] Mevcut güvenlik duvarı kurallarını görüntüle
echo  [6] Ana menüye dön
echo.
set /p netsecim="► Seçiminizi girin (1-6): "
call :beep 800 50

if "%netsecim%"=="1" goto engellegelen
if "%netsecim%"=="2" goto engellegiden
if "%netsecim%"=="3" goto engelletum
if "%netsecim%"=="4" goto engelkaldir
if "%netsecim%"=="5" goto kuralliste
if "%netsecim%"=="6" goto anamenu

call :beep 300 200
echo.
echo  ! Geçersiz seçim! Lütfen tekrar deneyin.
echo.
ping -n 3 127.0.0.1 >nul
goto internetyonet

:engellegelen
cls
call :beep 600 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                         GELEN BAĞLANTILAR ENGELLEME                        ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo  ► Engellenecek Corel uygulamalarını seçin:
echo.
echo  [1] Sadece CorelDRAW
echo  [2] Tüm Corel uygulamaları
echo.
set /p corelapp="► Seçiminiz (1-2): "
call :beep 700 50

if "%corelapp%"=="1" (
    echo.
    echo  ► CorelDRAW için gelen bağlantılar engelleniyor...
    call :beep 500 50
    call :beep 600 50
    netsh advfirewall firewall add rule name="Corel Draw - Gelen Engelleme" dir=in action=block program="C:\Program Files\Corel\CorelDRAW Graphics Suite\Programs\CorelDrw.exe" enable=yes profile=any >nul
    call :beep 900 100
    echo  ✓ CorelDRAW için gelen bağlantılar engellendi.
    echo.
    echo  █ █ █ █ █ █ █ █ █ █ █ █ █ 100%% TAMAMLANDI █ █ █ █ █ █ █ █ █ █ █ █ █
) else if "%corelapp%"=="2" (
    echo.
    echo  ► Tüm Corel uygulamaları için gelen bağlantılar engelleniyor...
    call :beep 500 50
    call :beep 600 50
    netsh advfirewall firewall add rule name="Corel Uygulamaları - Gelen Engelleme" dir=in action=block program="C:\Program Files\Corel\CorelDRAW Graphics Suite\Programs\*.exe" enable=yes profile=any >nul
    call :beep 900 100
    echo  ✓ Tüm Corel uygulamaları için gelen bağlantılar engellendi.
    echo.
    echo  █ █ █ █ █ █ █ █ █ █ █ █ █ 100%% TAMAMLANDI █ █ █ █ █ █ █ █ █ █ █ █ █
) else (
    call :beep 300 200
    echo.
    echo  ! Geçersiz seçim!
)
echo.
echo  ► İnternet yönetim menüsüne dönmek için ENTER tuşuna basın...
pause >nul
goto internetyonet

:engellegiden
cls
call :beep 600 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                        GİDEN BAĞLANTILAR ENGELLEME                         ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo  ► Engellenecek Corel uygulamalarını seçin:
echo.
echo  [1] Sadece CorelDRAW
echo  [2] Tüm Corel uygulamaları
echo.
set /p corelapp="► Seçiminiz (1-2): "
call :beep 700 50

if "%corelapp%"=="1" (
    echo.
    echo  ► CorelDRAW için giden bağlantılar engelleniyor...
    call :beep 500 50
    call :beep 600 50
    netsh advfirewall firewall add rule name="Corel Draw - Giden Engelleme" dir=out action=block program="C:\Program Files\Corel\CorelDRAW Graphics Suite\Programs\CorelDrw.exe" enable=yes profile=any >nul
    call :beep 900 100
    echo  ✓ CorelDRAW için giden bağlantılar engellendi.
    echo.
    echo  █ █ █ █ █ █ █ █ █ █ █ █ █ 100%% TAMAMLANDI █ █ █ █ █ █ █ █ █ █ █ █ █
) else if "%corelapp%"=="2" (
    echo.
    echo  ► Tüm Corel uygulamaları için giden bağlantılar engelleniyor...
    call :beep 500 50
    call :beep 600 50
    netsh advfirewall firewall add rule name="Corel Uygulamaları - Giden Engelleme" dir=out action=block program="C:\Program Files\Corel\CorelDRAW Graphics Suite\Programs\*.exe" enable=yes profile=any >nul
    call :beep 900 100
    echo  ✓ Tüm Corel uygulamaları için giden bağlantılar engellendi.
    echo.
    echo  █ █ █ █ █ █ █ █ █ █ █ █ █ 100%% TAMAMLANDI █ █ █ █ █ █ █ █ █ █ █ █ █
) else (
    call :beep 300 200
    echo.
    echo  ! Geçersiz seçim!
)
echo.
echo  ► İnternet yönetim menüsüne dönmek için ENTER tuşuna basın...
pause >nul
goto internetyonet

:engelletum
cls
call :beep 600 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                      TÜM İNTERNET ERİŞİMİ ENGELLEME                        ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo  ► Engellenecek Corel uygulamalarını seçin:
echo.
echo  [1] Sadece CorelDRAW
echo  [2] Tüm Corel uygulamaları
echo.
set /p corelapp="► Seçiminiz (1-2): "
call :beep 700 50

if "%corelapp%"=="1" (
    echo.
    echo  ► CorelDRAW için tüm internet erişimi engelleniyor...
    call :beep 500 50
    netsh advfirewall firewall add rule name="Corel Draw - Gelen Engelleme" dir=in action=block program="C:\Program Files\Corel\CorelDRAW Graphics Suite\Programs\CorelDrw.exe" enable=yes profile=any >nul
    call :beep 600 50
    netsh advfirewall firewall add rule name="Corel Draw - Giden Engelleme" dir=out action=block program="C:\Program Files\Corel\CorelDRAW Graphics Suite\Programs\CorelDrw.exe" enable=yes profile=any >nul
    call :beep 900 100
    echo  ✓ CorelDRAW için tüm internet erişimi engellendi.
    echo.
    echo  █ █ █ █ █ █ █ █ █ █ █ █ █ 100%% TAMAMLANDI █ █ █ █ █ █ █ █ █ █ █ █ █
) else if "%corelapp%"=="2" (
    echo.
    echo  ► Tüm Corel uygulamaları için internet erişimi engelleniyor...
    call :beep 500 50
    netsh advfirewall firewall add rule name="Corel Uygulamaları - Gelen Engelleme" dir=in action=block program="C:\Program Files\Corel\CorelDRAW Graphics Suite\Programs\*.exe" enable=yes profile=any >nul
    call :beep 600 50
    netsh advfirewall firewall add rule name="Corel Uygulamaları - Giden Engelleme" dir=out action=block program="C:\Program Files\Corel\CorelDRAW Graphics Suite\Programs\*.exe" enable=yes profile=any >nul
    call :beep 900 100
    echo  ✓ Tüm Corel uygulamaları için internet erişimi engellendi.
    echo.
    echo  █ █ █ █ █ █ █ █ █ █ █ █ █ 100%% TAMAMLANDI █ █ █ █ █ █ █ █ █ █ █ █ █
) else (
    call :beep 300 200
    echo.
    echo  ! Geçersiz seçim!
)
echo.
echo  ► İnternet yönetim menüsüne dönmek için ENTER tuşuna basın...
pause >nul
goto internetyonet

:engelkaldir
cls
call :beep 600 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                       İNTERNET ENGELİ KALDIRMA                             ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo  ► Tüm Corel internet erişim engelleri kaldırılıyor...
call :beep 500 50
netsh advfirewall firewall delete rule name="Corel Draw - Gelen Engelleme" >nul
call :beep 600 50
netsh advfirewall firewall delete rule name="Corel Draw - Giden Engelleme" >nul
call :beep 700 50
netsh advfirewall firewall delete rule name="Corel Uygulamaları - Gelen Engelleme" >nul
call :beep 800 50
netsh advfirewall firewall delete rule name="Corel Uygulamaları - Giden Engelleme" >nul
call :beep 900 100
echo  ✓ Tüm Corel engelleme kuralları kaldırıldı.
echo.
echo  █ █ █ █ █ █ █ █ █ █ █ █ █ 100%% TAMAMLANDI █ █ █ █ █ █ █ █ █ █ █ █ █
echo.
echo  ► İnternet yönetim menüsüne dönmek için ENTER tuşuna basın...
pause >nul
goto internetyonet

:kuralliste
cls
call :beep 600 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                     GÜVENLİK DUVARI KURALLARI LİSTESİ                      ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo  ► Mevcut Corel güvenlik duvarı kuralları araştırılıyor...
echo.
call :beep 500 50
call :beep 600 50
call :beep 700 50
echo  ►► BULUNAN KURALLAR:
echo  ---------------------------------------------------------------------
netsh advfirewall firewall show rule name=all | findstr /i "Corel"
echo  ---------------------------------------------------------------------
echo.
call :beep 900 100
echo  ► İnternet yönetim menüsüne dönmek için ENTER tuşuna basın...
pause >nul
goto internetyonet

:sistembilgi
cls
call :beep 600 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                          SİSTEM BİLGİLERİ                                  ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo  ► Sistem bilgileri toplanıyor...
call :beep 500 50
call :beep 600 50
call :beep 700 50
echo.
echo  ► VAULT-TEC TEŞHİS SONUÇLARI:
echo  ---------------------------------------------------------------------
echo  Kullanıcı Adı      : %username%
echo  Bilgisayar Adı     : %computername%
echo  İşletim Sistemi    : %os%
echo  Tarih              : %date%
echo  Zaman              : %time%
echo  ---------------------------------------------------------------------
echo.

echo  ► COREL ÜRÜN BİLGİLERİ:
echo  ---------------------------------------------------------------------
if exist "C:\Program Files\Corel\CorelDRAW Graphics Suite\Programs\CorelDrw.exe" (
    echo  Corel Draw Durumu  : Yüklü
) else (
    echo  Corel Draw Durumu  : Yüklü Değil
)

if exist "C:\Users\%username%\AppData\Roaming\Corel" (
    echo  Kullanıcı Verileri : Mevcut
    echo  Veri Konumu        : C:\Users\%username%\AppData\Roaming\Corel
) else (
    echo  Kullanıcı Verileri : Mevcut Değil
)
echo  ---------------------------------------------------------------------
echo.
call :beep 900 100
echo  ► Ana menüye dönmek için ENTER tuşuna basın...
pause >nul
goto anamenu

:cikis
cls
call :beep 600 50
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                           VAULT-TEC ÇIKIŞ                                  ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo  ► Sistemden çıkılıyor...
echo.
call :beep 500 50
call :beep 400 50
call :beep 300 50
echo  ✓ Pip-Boy 3000 Corel Kontrol Terminali kapatılıyor
echo.
echo  VAULT-TEC: İyi günler dileriz %username%!
call :beep 200 200
ping -n 3 127.0.0.1 >nul
exit

:: Fonksiyonlar
:yukleBeepFonksiyonu
(
echo WScript.CreateObject("WScript.Shell").Run "cmd /c exit 7",0 ^
) >"%temp%\silent.vbs"
(
echo Function Beep(^freq,duration^)
echo CreateObject("^"SAPI.SpVoice^"^").speak Chr^(^(^(freq/10^)^)+34^),2
echo WScript.Sleep duration
echo End Function
echo Beep WScript.Arguments^(0^),WScript.Arguments^(1^)
) >"%temp%\beep.vbs"
goto :eof

:beep
if "%1"=="" (
    cscript //nologo "%temp%\silent.vbs"
) else (
    cscript //nologo "%temp%\beep.vbs" %1 %2
)
goto :eof
