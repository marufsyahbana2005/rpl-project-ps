@echo off
title Exito Playbox - Live Demo Server
echo ======================================================
echo    MEMULAI SERVER LIVE DEMO - EXITO PLAYBOX
echo ======================================================
echo.
echo [*] Membuka peramban di http://127.0.0.1:5000/login ...
start http://127.0.0.1:5000/login
echo [*] Menjalankan server aplikasi Flask...
echo [*] Tekan Ctrl + C di jendela ini untuk mematikan server.
echo.
python app.py
pause
