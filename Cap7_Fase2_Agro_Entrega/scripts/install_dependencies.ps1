# PowerShell script para instalar dependências
# Execute como: powershell -ExecutionPolicy Bypass -File install_dependencies.ps1

Write-Host "===============================================" -ForegroundColor Green
Write-Host "    Instalador de Dependências - Cap. 7" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Verificar Python
Write-Host "Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERRO: Python não encontrado!" -ForegroundColor Red
    Write-Host "Instale Python 3.7+ e tente novamente." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""
Write-Host "Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""
Write-Host "Instalando dependências essenciais..." -ForegroundColor Yellow
$packages = @("pandas", "numpy", "matplotlib", "seaborn", "openpyxl")

foreach ($package in $packages) {
    Write-Host "Instalando $package..." -ForegroundColor Cyan
    python -m pip install $package
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ Aviso: Erro ao instalar $package" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Testando instalação..." -ForegroundColor Yellow
try {
    python -c "import pandas, numpy, matplotlib, seaborn; print('✅ Todas as dependências instaladas com sucesso!')"
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "===============================================" -ForegroundColor Green
        Write-Host "    INSTALAÇÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
        Write-Host "===============================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Você pode agora executar:" -ForegroundColor White
        Write-Host "  python main.py --mode rapido" -ForegroundColor Cyan
        Write-Host "  python main.py --mode completo" -ForegroundColor Cyan
    }
} catch {
    Write-Host ""
    Write-Host "===============================================" -ForegroundColor Red
    Write-Host "    ERRO NA INSTALAÇÃO!" -ForegroundColor Red
    Write-Host "===============================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Tente executar manualmente:" -ForegroundColor White
    Write-Host "  pip install pandas numpy matplotlib seaborn openpyxl" -ForegroundColor Cyan
}

Write-Host ""
Read-Host "Pressione Enter para sair"
