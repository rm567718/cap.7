#!/usr/bin/env python3
"""
Script de instalação de dependências para o projeto Capítulo 7
Sistema Integrado de Análise do Agronegócio
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Executa um comando e retorna se foi bem-sucedido"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Concluído")
            return True
        else:
            print(f"❌ {description} - Erro: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exceção: {e}")
        return False

def check_python_version():
    """Verifica a versão do Python"""
    print("🐍 Verificando versão do Python...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ é necessário")
        return False
    
    print("✅ Versão do Python compatível")
    return True

def install_package(package_name, description=None):
    """Instala um pacote Python"""
    if description is None:
        description = package_name
    
    print(f"📦 Instalando {description}...")
    
    # Comandos de instalação com diferentes estratégias
    commands = [
        f"pip install {package_name}",
        f"python -m pip install {package_name}",
        f"pip install --upgrade {package_name}",
        f"python -m pip install --upgrade --force-reinstall {package_name}"
    ]
    
    for i, command in enumerate(commands):
        if run_command(command, f"Tentativa {i+1}: {description}"):
            return True
    
    print(f"❌ Falha ao instalar {description}")
    return False

def test_import(package_name, import_statement=None):
    """Testa se um pacote pode ser importado"""
    if import_statement is None:
        import_statement = package_name
    
    try:
        exec(f"import {import_statement}")
        print(f"✅ {package_name} - Importação OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name} - Erro na importação: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🌾 INSTALADOR DE DEPENDÊNCIAS - CAPÍTULO 7")
    print("Sistema Integrado de Análise do Agronegócio")
    print("=" * 60)
    print()
    
    # Verificar Python
    if not check_python_version():
        print("\n❌ Versão do Python incompatível. Instale Python 3.7+")
        return False
    
    print()
    
    # Atualizar pip
    run_command("python -m pip install --upgrade pip", "Atualizando pip")
    print()
    
    # Lista de pacotes essenciais
    essential_packages = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("openpyxl", "openpyxl"),
        ("scipy", "scipy")
    ]
    
    # Instalar pacotes
    print("📦 INSTALANDO PACOTES ESSENCIAIS")
    print("-" * 40)
    
    failed_packages = []
    for package, import_name in essential_packages:
        if not install_package(package, package):
            failed_packages.append(package)
        print()
    
    # Testar importações
    print("🧪 TESTANDO IMPORTAÇÕES")
    print("-" * 40)
    
    import_failures = []
    for package, import_name in essential_packages:
        if not test_import(package, import_name):
            import_failures.append(package)
    
    # Resultado final
    print("\n" + "=" * 60)
    
    if not failed_packages and not import_failures:
        print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print()
        print("✅ Todos os pacotes foram instalados e testados")
        print()
        print("🚀 Você pode agora executar:")
        print("   python main.py --mode rapido")
        print("   python main.py --mode completo")
        print("   python main.py --deps  # Para verificar dependências")
        return True
    else:
        print("⚠️  INSTALAÇÃO COM PROBLEMAS")
        print()
        if failed_packages:
            print(f"❌ Pacotes que falharam na instalação: {', '.join(failed_packages)}")
        if import_failures:
            print(f"❌ Pacotes com erro de importação: {', '.join(import_failures)}")
        print()
        print("🔧 SOLUÇÕES RECOMENDADAS:")
        print("1. Execute manualmente:")
        print("   pip install --upgrade --force-reinstall pandas numpy matplotlib seaborn")
        print()
        print("2. Use ambiente virtual:")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate  # Windows")
        print("   pip install -r requirements.txt")
        print()
        print("3. Verifique conexão com internet")
        return False

if __name__ == "__main__":
    try:
        success = main()
        input("\nPressione Enter para sair...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("\nPressione Enter para sair...")
        sys.exit(1)