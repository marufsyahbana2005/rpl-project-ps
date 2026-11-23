# git-push.ps1 — Skrip PowerShell Manajemen Git Cepat
# Repositori: marufsyahbana2005/rpl-project-ps

function Tampilkan-Header {
    Clear-Host
    Write-Host "======================================================" -ForegroundColor Cyan
    Write-Host "       MENU OPERASIONAL GIT — EXITO PLAYBOX           " -ForegroundColor Yellow
    Write-Host "   Repositori: https://github.com/marufsyahbana2005/rpl-project-ps" -ForegroundColor Gray
    Write-Host "======================================================" -ForegroundColor Cyan
}

function Jalankan-QuickPush {
    Tampilkan-Header
    $currentBranch = (git branch --show-current).Trim()
    if (-not $currentBranch) { $currentBranch = "main" }
    
    Write-Host "`n[*] Status perubahan saat ini (git status -s):" -ForegroundColor Green
    git status -s

    $pesan = Read-Host "`nMasukkan pesan commit (Tekan Enter untuk 'update: sinkronisasi kode')"
    if ([string]::IsNullOrWhiteSpace($pesan)) {
        $pesan = "update: sinkronisasi kode"
    }

    Write-Host "`n[*] Melakukan git add . ..." -ForegroundColor Green
    git add .

    Write-Host "[*] Melakukan git commit -m `"$pesan`" ..." -ForegroundColor Green
    git commit -m "$pesan"

    Write-Host "[*] Mengirim perubahan ke GitHub (git push origin $currentBranch) ..." -ForegroundColor Green
    git push origin $currentBranch

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[SUKSES] Berhasil di-push ke cabang $currentBranch di GitHub!" -ForegroundColor Green
    } else {
        Write-Host "`n[GALAT] Gagal melakukan git push. Periksa koneksi atau branch." -ForegroundColor Red
    }
}

function Jalankan-Pull {
    Tampilkan-Header
    $currentBranch = (git branch --show-current).Trim()
    if (-not $currentBranch) { $currentBranch = "main" }
    
    Write-Host "`n[*] Menarik pembaruan dari GitHub (git pull origin $currentBranch) ..." -ForegroundColor Cyan
    git pull origin $currentBranch
}

function Jalankan-Status {
    Tampilkan-Header
    Write-Host "`n[*] Status Lengkap Repositori (git status):" -ForegroundColor Cyan
    git status
}

function Jalankan-Log {
    Tampilkan-Header
    Write-Host "`n[*] 10 Riwayat Commit Terakhir (git log):" -ForegroundColor Cyan
    git log --oneline --graph --decorate -n 10
}

# Alur Utama Jika Ada Argumen Pesan Commit Langsung: .\git-push.ps1 "pesan commit"
if ($args.Count -gt 0) {
    $pesanArg = $args -join " "
    $currentBranch = (git branch --show-current).Trim()
    if (-not $currentBranch) { $currentBranch = "main" }
    
    Write-Host "[*] Melakukan Auto Add, Commit, dan Push..." -ForegroundColor Cyan
    git add .
    git commit -m "$pesanArg"
    git push origin $currentBranch
    exit $LASTEXITCODE
}

# Menu Interaktif
do {
    Tampilkan-Header
    $curBranch = (git branch --show-current).Trim()
    Write-Host "Cabang Aktif Saat Ini : $curBranch" -ForegroundColor Magenta
    Write-Host "------------------------------------------------------" -ForegroundColor Gray
    Write-Host "1. Quick Push (Add All + Commit + Push ke GitHub)" -ForegroundColor Green
    Write-Host "2. Git Pull (Tarik update terbaru dari GitHub)" -ForegroundColor Yellow
    Write-Host "3. Git Status (Cek berkas yang diubah)" -ForegroundColor White
    Write-Host "4. Git Log (Lihat riwayat commit terbaru)" -ForegroundColor White
    Write-Host "0. Keluar" -ForegroundColor Gray
    Write-Host "------------------------------------------------------" -ForegroundColor Gray
    
    $pilihan = Read-Host "Pilih menu [1-4 / 0]"
    switch ($pilihan) {
        "1" { Jalankan-QuickPush; Pause }
        "2" { Jalankan-Pull; Pause }
        "3" { Jalankan-Status; Pause }
        "4" { Jalankan-Log; Pause }
        "0" { Write-Host "`nSelesai. Sampai jumpa!" -ForegroundColor Green; break }
        Default { Write-Host "`nPilihan tidak valid!" -ForegroundColor Red; Start-Sleep -Seconds 1 }
    }
} while ($pilihan -ne "0")
