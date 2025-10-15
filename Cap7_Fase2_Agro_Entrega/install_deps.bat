@echo off
echo ===============================================
echo     INSTALADOR DE DEPENDENCIAS - CAP. 7
echo ===============================================
echo.

echo Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.7+ e tente novamente.
    pause
    exit /b 1
)

echo.
echo Atualizando pip...
python -m pip install --upgrade pip

echo.
echo Instalando dependencias essenciais...
python -m pip install pandas numpy matplotlib seaborn openpyxl scipy

echo.
echo Testando instalacao...
python -c "import pandas, numpy, matplotlib, seaborn; print('Todas as dependencias instaladas com sucesso!')"

if %errorlevel% equ 0 (
    echo.
    echo ===============================================
    echo     INSTALACAO CONCLUIDA COM SUCESSO!
    echo ===============================================
    echo.
    echo Voce pode agora executar:
    echo   python main.py --mode rapido
    echo   python main.py --mode completo
) else (
    echo.
    echo ===============================================
    echo     ERRO NA INSTALACAO!
    echo ===============================================
    echo.
    echo Tente executar manualmente:
    echo   pip install pandas numpy matplotlib seaborn openpyxl
)

echo.
pause