@echo off
setlocal enabledelayedexpansion
title Git Quick Push - Exito Playbox (rpl-project-ps)

echo ======================================================
echo          GIT QUICK PUSH ^& SYNC AUTOMATION
echo      Repositori: marufsyahbana2005/rpl-project-ps
echo ======================================================
echo.

:: 1. Tampilkan status perubahan
echo [*] Memeriksa status perubahan berkas (git status)...
git status -s
echo.

:: 2. Tanya pesan commit
set "pesan="
set /p "pesan=Masukkan pesan commit (tekan Enter untuk default 'update: sinkronisasi kode'): "
if "%pesan%"=="" set "pesan=update: sinkronisasi kode"

:: 3. Dapatkan nama branch aktif saat ini
for /f "tokens=*" %%i in ('git branch --show-current') do set "branch=%%i"
if "%branch%"=="" set "branch=main"

echo.
echo [*] Menambahkan seluruh perubahan (git add .) ...
git add .

echo [*] Membuat commit dengan pesan: "%pesan%" ...
git commit -m "%pesan%"

echo [*] Mengirim ke GitHub (git push origin %branch%) ...
git push origin %branch%

if %errorlevel% equ 0 (
    echo.
    echo ======================================================
    echo [SUKSES] Perubahan berhasil di-push ke GitHub!
    echo Cabang: %branch%
    echo Repositori: https://github.com/marufsyahbana2005/rpl-project-ps
    echo ======================================================
) else (
    echo.
    echo [GALAT] Terjadi kegagalan saat git push. Silakan periksa koneksi internet atau hak akses.
)

echo.
pause
