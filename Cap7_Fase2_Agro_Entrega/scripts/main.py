#!/usr/bin/env python3
"""
Sistema Integrado de Análise de Dados do Agronegócio
Projeto Capítulo 7 - Integração Python/R
Desenvolvido por: Raimunda Nayara Mendes dos Santos (RM: 567718)
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
import subprocess
import json
import argparse
import warnings
from pathlib import Path
import shutil
from typing import Optional, Any, Dict, List

# Try to import optional dependencies with fallbacks
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError as e:
    print(f"pandas não disponível: {e}")
    print("   Execute: pip install pandas")
    PANDAS_AVAILABLE = False
    pd = None  # type: ignore

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError as e:
    print(f"numpy não disponível: {e}")
    print("   Execute: pip install numpy")
    NUMPY_AVAILABLE = False
    np = None  # type: ignore

try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError as e:
    print(f"matplotlib não disponível: {e}")
    print("   Execute: pip install matplotlib")
    MATPLOTLIB_AVAILABLE = False
    plt = None  # type: ignore
except Exception as e:
    print(f"Erro inesperado ao importar matplotlib: {e}")
    MATPLOTLIB_AVAILABLE = False
    plt = None  # type: ignore

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError as e:
    print(f"seaborn não disponível: {e}")
    print("   Execute: pip install seaborn")
    SEABORN_AVAILABLE = False
    sns = None  # type: ignore

# Configurar matplotlib para português (se disponível)
if MATPLOTLIB_AVAILABLE:
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 16

# Suprimir warnings desnecessários
warnings.filterwarnings('ignore')

class AgroAnalysisSystem:
    """Sistema integrado de análise de dados do agronegócio"""
    
    def __init__(self, config_file=None, **kwargs):
        self.data = None
        self.config = self._load_config(config_file)
        
        # Aplicar configurações adicionais passadas via kwargs
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
        
        self.output_dir = Path("exportacoes")
        self.reports_dir = Path("relatorios")
        self.graphics_dir = self.reports_dir / "graficos"
        self.validation_messages = []
        
        # Criar diretórios necessários
        self._create_directories()
        
    def _load_config(self, config_file=None):
        """Carrega configurações do sistema"""
        default_config = {
            "autora": "Raimunda Nayara Mendes dos Santos",
            "rm": "567718",
            "fase": 2,
            "capitulo": 7,
            "data_file": "base_agro.xlsx",
            "output_format": "csv",
            "charts_format": "png",
            "language": "pt-BR",
            "r_script_path": "Rscript",
            "r_script_file": "ENTREGA_Fase2_Cap7.R",
            "chart_theme": "whitegrid",
            "chart_dpi": 120,
            "chart_size": (10, 6)
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    custom_config = json.load(f)
                    default_config.update(custom_config)
            except Exception as e:
                print(f"Erro ao carregar configuração personalizada: {e}")
                
        return default_config
    
    def _create_directories(self):
        """Cria diretórios necessários para o sistema"""
        directories = [self.output_dir, self.reports_dir, self.graphics_dir]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def check_dependencies(self):
        """Verifica e instala dependências necessárias"""
        required_packages = {
            "pandas": PANDAS_AVAILABLE,
            "numpy": NUMPY_AVAILABLE,
            "matplotlib": MATPLOTLIB_AVAILABLE,
            "seaborn": SEABORN_AVAILABLE
        }
        
        optional_packages = ["openpyxl", "plotly", "scikit-learn"]
        
        missing_packages = []
        for package, available in required_packages.items():
            if available:
                print(f"{package} disponível")
            else:
                missing_packages.append(package)
                print(f"{package} não encontrado")
        
        # Check optional packages
        for package in optional_packages:
            try:
                __import__(package)
                print(f"{package} disponível (opcional)")
            except ImportError:
                print(f"{package} não encontrado (opcional)")
        
        if missing_packages:
            print(f"\nPacotes essenciais faltantes: {', '.join(missing_packages)}")
            print("Execute: pip install pandas numpy matplotlib seaborn")
            print("Ou execute: pip install -r requirements.txt")
            return False
        
        print("\nTodas as dependências essenciais estão disponíveis!")
        return True
    
    def check_r_installation(self):
        """Verifica se R está instalado e acessível"""
        try:
            result = subprocess.run([self.config["r_script_path"], "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"R disponível: {result.stdout.split()[2]}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        print(f"R não encontrado em: {self.config['r_script_path']}")
        print("Instale R e certifique-se de que 'Rscript' está no PATH")
        return False
    
    def load_data(self, file_path=None):
        """Carrega dados do arquivo Excel"""
        if not PANDAS_AVAILABLE:
            print("pandas não disponível. Não é possível carregar dados.")
            print("   Execute: pip install pandas")
            return False
            
        if file_path is None:
            file_path = self.config["data_file"]
        
        try:
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                self.data = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path, encoding='utf-8')
            else:
                raise ValueError("Formato de arquivo não suportado. Use .xlsx, .xls ou .csv")
            
            print(f"Dados carregados: {len(self.data)} registros, {len(self.data.columns)} colunas")
            return True
            
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {file_path}")
            return False
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False
    
    def validate_data(self):
        """Valida e limpa os dados"""
        if self.data is None:
            print("Nenhum dado carregado para validação")
            return False
        
        self.validation_messages = []
        
        # Verificar colunas esperadas
        expected_columns = ["Safra", "Regiao", "Cultura", "Subtipo", "Produtividade_t_ha", "Nivel_Tecnologico"]
        missing_columns = [col for col in expected_columns if col not in self.data.columns]
        
        if missing_columns:
            self.validation_messages.append(f"Colunas faltando: {', '.join(missing_columns)}")
        
        # Validar produtividade
        if "Produtividade_t_ha" in self.data.columns:
            na_count = self.data["Produtividade_t_ha"].isna().sum()
            if na_count > 0:
                self.validation_messages.append(f"Valores NA em Produtividade_t_ha: {na_count}")
            
            invalid_values = self.data[
                (self.data["Produtividade_t_ha"] < 0) | 
                (self.data["Produtividade_t_ha"] > 20)
            ]
            
            if len(invalid_values) > 0:
                self.validation_messages.append(f"Produtividades fora do intervalo [0,20]: {len(invalid_values)} registros")
        
        # Limpeza dos dados
        self.data = self.data.copy()
        
        if "Produtividade_t_ha" in self.data.columns:
            # Remover valores NA e capar valores extremos
            self.data = self.data.dropna(subset=["Produtividade_t_ha"])
            self.data["Produtividade_t_ha"] = self.data["Produtividade_t_ha"].clip(0, 20)
        
        # Converter Cultura para categoria
        if "Cultura" in self.data.columns:
            self.data["Cultura"] = pd.Categorical(self.data["Cultura"])
        
        print(f"Validação concluída: {len(self.data)} registros válidos")
        if self.validation_messages:
            print("Mensagens de validação:")
            for msg in self.validation_messages:
                print(f"   - {msg}")
        
        return True
    
    def generate_statistics(self):
        """Gera estatísticas descritivas"""
        if self.data is None or "Produtividade_t_ha" not in self.data.columns:
            print("Dados não disponíveis para análise estatística")
            return False
        
        try:
            # Estatísticas gerais
            stats_general = {
                'n': len(self.data),
                'media': self.data["Produtividade_t_ha"].mean(),
                'mediana': self.data["Produtividade_t_ha"].median(),
                'desvio_padrao': self.data["Produtividade_t_ha"].std(),
                'minimo': self.data["Produtividade_t_ha"].min(),
                'maximo': self.data["Produtividade_t_ha"].max(),
                'q1': self.data["Produtividade_t_ha"].quantile(0.25),
                'q3': self.data["Produtividade_t_ha"].quantile(0.75)
            }
            
            # Estatísticas por cultura
            stats_by_culture = []
            if "Cultura" in self.data.columns:
                for cultura in self.data["Cultura"].unique():
                    cultura_data = self.data[self.data["Cultura"] == cultura]["Produtividade_t_ha"]
                    stats_by_culture.append({
                        'Cultura': cultura,
                        'n': len(cultura_data),
                        'media': cultura_data.mean(),
                        'mediana': cultura_data.median(),
                        'desvio_padrao': cultura_data.std(),
                        'minimo': cultura_data.min(),
                        'maximo': cultura_data.max()
                    })
            
            # Salvar estatísticas
            stats_general_df = pd.DataFrame([stats_general])
            stats_general_df.to_csv(self.reports_dir / "estatisticas_geral.csv", index=False)
            
            if stats_by_culture:
                stats_by_culture_df = pd.DataFrame(stats_by_culture)
                stats_by_culture_df.to_csv(self.reports_dir / "estatisticas_por_cultura.csv", index=False)
            
            print("Estatísticas descritivas geradas")
            return True
            
        except Exception as e:
            print(f" Erro ao gerar estatísticas: {e}")
            return False
    
    def create_visualizations(self):
        """Cria visualizações dos dados"""
        if not MATPLOTLIB_AVAILABLE or not SEABORN_AVAILABLE:
            print(" matplotlib ou seaborn não disponível para visualização")
            print("   Execute: pip install matplotlib seaborn")
            return False
            
        if self.data is None or "Produtividade_t_ha" not in self.data.columns:
            print(" Dados não disponíveis para visualização")
            return False
        
        try:
            # Configurar estilo
            plt.style.use('default')
            sns.set_theme(style=self.config["chart_theme"])
            
            # 1. Histograma com densidade
            plt.figure(figsize=self.config["chart_size"])
            plt.hist(self.data["Produtividade_t_ha"], bins=12, density=True, alpha=0.7, 
                    color='skyblue', edgecolor='black')
            
            # Adicionar curva de densidade
            try:
                from scipy import stats
                kde = stats.gaussian_kde(self.data["Produtividade_t_ha"])
                x_range = np.linspace(self.data["Produtividade_t_ha"].min(), 
                                    self.data["Produtividade_t_ha"].max(), 100)
                plt.plot(x_range, kde(x_range), 'r-', linewidth=2, label='Densidade')
            except ImportError:
                print("scipy não disponível para curva de densidade")
            
            plt.title("Produtividade (t/ha) — Histograma e Densidade", fontsize=14, fontweight='bold')
            plt.xlabel("Produtividade (t/ha)")
            plt.ylabel("Densidade")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(self.graphics_dir / "hist_densidade.png", dpi=self.config["chart_dpi"], bbox_inches='tight')
            plt.close()
            
            # 2. Boxplot por cultura
            if "Cultura" in self.data.columns:
                plt.figure(figsize=self.config["chart_size"])
                sns.boxplot(data=self.data, x="Cultura", y="Produtividade_t_ha")
                plt.title("Produtividade por Cultura", fontsize=14, fontweight='bold')
                plt.xlabel("Cultura")
                plt.ylabel("Produtividade (t/ha)")
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.savefig(self.graphics_dir / "boxplot_cultura.png", dpi=self.config["chart_dpi"], bbox_inches='tight')
                plt.close()
                
                # 3. Frequências por cultura
                plt.figure(figsize=self.config["chart_size"])
                culture_counts = self.data["Cultura"].value_counts()
                culture_props = self.data["Cultura"].value_counts(normalize=True)
                
                bars = plt.bar(culture_counts.index, culture_counts.values, color=['lightcoral', 'lightgreen'])
                plt.title("Frequências e Proporções por Cultura", fontsize=14, fontweight='bold')
                plt.xlabel("Cultura")
                plt.ylabel("Contagem")
                
                # Adicionar percentuais nas barras
                for i, (bar, prop) in enumerate(zip(bars, culture_props.values)):
                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                            f'{prop:.1%}', ha='center', va='bottom', fontweight='bold')
                
                plt.grid(True, alpha=0.3, axis='y')
                plt.tight_layout()
                plt.savefig(self.graphics_dir / "frequencias_cultura.png", dpi=self.config["chart_dpi"], bbox_inches='tight')
                plt.close()
            
            # 4. Análise de subtipos de feijão
            if "Subtipo" in self.data.columns and "Cultura" in self.data.columns:
                feijao_data = self.data[(self.data["Cultura"] == "Feijão") & 
                                      (self.data["Subtipo"].notna())]
                
                if len(feijao_data) > 0:
                    plt.figure(figsize=self.config["chart_size"])
                    subtipo_means = feijao_data.groupby("Subtipo")["Produtividade_t_ha"].mean()
                    
                    bars = plt.bar(subtipo_means.index, subtipo_means.values, 
                                  color=['gold', 'orange', 'darkorange'])
                    plt.title("Feijão — Produtividade média por subtipo", fontsize=14, fontweight='bold')
                    plt.xlabel("Subtipo")
                    plt.ylabel("Produtividade média (t/ha)")
                    
                    # Adicionar valores nas barras
                    for bar in bars:
                        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                                f'{bar.get_height():.2f}', ha='center', va='bottom', fontweight='bold')
                    
                    plt.grid(True, alpha=0.3, axis='y')
                    plt.tight_layout()
                    plt.savefig(self.graphics_dir / "feijao_subtipos.png", dpi=self.config["chart_dpi"], bbox_inches='tight')
                    plt.close()
            
            print("Visualizações geradas")
            return True
            
        except Exception as e:
            print(f"Erro ao criar visualizações: {e}")
            return False
    
    def run_r_analysis(self):
        """Executa análise R se disponível"""
        if not self.check_r_installation():
            print("Análise R não executada - R não disponível")
            return False
        
        r_script_path = self.config["r_script_file"]
        if not os.path.exists(r_script_path):
            print(f"Script R não encontrado: {r_script_path}")
            return False
        
        try:
            print("Executando análise R...")
            result = subprocess.run([self.config["r_script_path"], r_script_path], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("Análise R concluída com sucesso")
                if result.stdout:
                    print("Saída R:", result.stdout)
                return True
            else:
                print(f"Erro na execução R: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("Timeout na execução R (5 minutos)")
            return False
        except Exception as e:
            print(f"Erro ao executar R: {e}")
            return False
    
    def generate_report(self):
        """Gera relatório HTML"""
        try:
            html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório do Agronegócio - Capítulo 7</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c5530; text-align: center; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #388E3C; margin-top: 30px; }}
        h3 {{ color: #4CAF50; }}
        .info {{ background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .stats {{ background: #f0f8ff; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 5px; margin: 10px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .footer {{ text-align: center; margin-top: 40px; color: #666; font-style: italic; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Relatório do Agronegócio — Capítulo 7</h1>
        
        <div class="info">
            <h3>Informações do Projeto</h3>
            <p><strong>Autora:</strong> {self.config['autora']}</p>
            <p><strong>RM:</strong> {self.config['rm']}</p>
            <p><strong>Fase:</strong> {self.config['fase']}</p>
            <p><strong>Capítulo:</strong> {self.config['capitulo']}</p>
            <p><strong>Data de geração:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        </div>
        
        <h2>Visão Geral</h2>
        <p>Este relatório apresenta análise de dados do agronegócio brasileiro, incluindo validação de dados, 
        estatísticas descritivas e visualizações de produtividade agrícola.</p>
        
        <h2>📈 Estatísticas Descritivas</h2>
"""
            
            # Adicionar estatísticas se disponíveis
            stats_file = self.reports_dir / "estatisticas_geral.csv"
            if stats_file.exists():
                stats_df = pd.read_csv(stats_file)
                html_content += "<div class='stats'>\n"
                html_content += "<h3>Estatísticas Gerais</h3>\n"
                html_content += stats_df.to_html(index=False, classes='stats-table')
                html_content += "</div>\n"
            
            stats_by_culture_file = self.reports_dir / "estatisticas_por_cultura.csv"
            if stats_by_culture_file.exists():
                stats_by_culture_df = pd.read_csv(stats_by_culture_file)
                html_content += "<div class='stats'>\n"
                html_content += "<h3>Estatísticas por Cultura</h3>\n"
                html_content += stats_by_culture_df.to_html(index=False, classes='stats-table')
                html_content += "</div>\n"
            
            html_content += """
        <h2>Visualizações</h2>
        <p>Os gráficos abaixo mostram diferentes aspectos da produtividade agrícola:</p>
"""
            
            # Adicionar imagens dos gráficos
            graphics = [
                ("hist_densidade.png", "Histograma e Curva de Densidade da Produtividade"),
                ("boxplot_cultura.png", "Boxplot da Produtividade por Cultura"),
                ("frequencias_cultura.png", "Frequências e Proporções por Cultura"),
                ("feijao_subtipos.png", "Produtividade Média por Subtipo de Feijão")
            ]
            
            for graphic_file, title in graphics:
                graphic_path = self.graphics_dir / graphic_file
                if graphic_path.exists():
                    html_content += f"""
        <h3>{title}</h3>
        <img src="graficos/{graphic_file}" alt="{title}">
"""
            
            # Adicionar mensagens de validação se houver
            if self.validation_messages:
                html_content += """
        <h2>Mensagens de Validação</h2>
        <div class="info">
"""
                for msg in self.validation_messages:
                    html_content += f"            <p>• {msg}</p>\n"
                html_content += "        </div>\n"
            
            html_content += f"""
        <div class="footer">
            <p>Relatório gerado automaticamente pelo Sistema de Análise do Agronegócio</p>
            <p>Desenvolvido por {self.config['autora']} (RM: {self.config['rm']})</p>
        </div>
    </div>
</body>
</html>
"""
            
            # Salvar relatório
            report_path = self.reports_dir / "relatorio_agro.html"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Relatório HTML gerado: {report_path}")
            return True
            
        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")
            return False
    
    def run_quick_analysis(self):
        """Executa análise rápida"""
        print("Iniciando análise rápida...")
        
        if not self.load_data():
            return False
        
        if not self.validate_data():
            return False
        
        if not self.generate_statistics():
            return False
        
        if not self.create_visualizations():
            return False
        
        if not self.generate_report():
            return False
        
        print("Análise rápida concluída!")
        return True
    
    def run_complete_analysis(self):
        """Executa análise completa (Python + R)"""
        print("Iniciando análise completa...")
        
        # Análise Python
        if not self.run_quick_analysis():
            return False
        
        # Análise R
        self.run_r_analysis()
        
        print("Análise completa concluída!")
        return True
    
    def convert_csv_to_excel(self, csv_file, output_file=None):
        """Converte arquivo CSV para Excel"""
        if not PANDAS_AVAILABLE:
            print("pandas não disponível. Não é possível converter CSV.")
            print("   Execute: pip install pandas openpyxl")
            return False
            
        try:
            if output_file is None:
                output_file = self.config["data_file"]
            
            df = pd.read_csv(csv_file, encoding='utf-8')
            df.to_excel(output_file, index=False)
            print(f"CSV convertido para Excel: {output_file}")
            return True
            
        except Exception as e:
            print(f"Erro na conversão CSV: {e}")
            return False

def main():
    """Função principal do programa"""
    parser = argparse.ArgumentParser(
        description="Sistema Integrado de Análise do Agronegócio - Capítulo 7",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --mode rapido                    # Análise rápida (Python)
  python main.py --mode completo                  # Análise completa (Python + R)
  python main.py --from-csv dados.csv             # Converter CSV e analisar
  python main.py --saida resultados --mode rapido # Definir diretório de saída
        """
    )
    
    parser.add_argument('--mode', choices=['rapido', 'completo'], 
                       help='Modo de análise (rapido: Python, completo: Python+R)')
    parser.add_argument('--from-csv', metavar='ARQUIVO', 
                       help='Converter CSV para Excel antes da análise')
    parser.add_argument('--base', metavar='ARQUIVO', default='base_agro.xlsx',
                       help='Arquivo de dados Excel (padrão: base_agro.xlsx)')
    parser.add_argument('--saida', metavar='DIRETORIO', default='relatorios',
                       help='Diretório de saída (padrão: relatorios)')
    parser.add_argument('--rscript', metavar='CAMINHO', default='Rscript',
                       help='Caminho para Rscript (padrão: Rscript)')
    parser.add_argument('--config', metavar='ARQUIVO', 
                       help='Arquivo de configuração JSON')
    parser.add_argument('--all-in-one', action='store_true',
                       help='Atalho para análise completa')
    parser.add_argument('--deps', action='store_true',
                       help='Verificar apenas dependências')
    
    args = parser.parse_args()
    
    print("Sistema Integrado de Análise do Agronegócio")
    print("Projeto Capítulo 7 - Python/R Integration")
    print("Desenvolvido por: Raimunda Nayara Mendes dos Santos (RM: 567718)")
    print("=" * 60)
    
    # Configurar sistema
    config = {}
    if args.config:
        config['config_file'] = args.config
    if args.rscript != 'Rscript':
        config['r_script_path'] = args.rscript
    if args.base != 'base_agro.xlsx':
        config['data_file'] = args.base
    if args.saida != 'relatorios':
        config['reports_dir'] = args.saida
    
    sistema = AgroAnalysisSystem(**config)
    
    # Verificar dependências
    if not sistema.check_dependencies():
        sys.exit(1)
    
    if args.deps:
        print("\nVerificação de dependências concluída")
        return
    
    # Converter CSV se necessário
    if args.from_csv:
        if not sistema.convert_csv_to_excel(args.from_csv, args.base):
            sys.exit(1)
    
    # Determinar modo de análise
    mode = args.mode
    if args.all_in_one:
        mode = 'completo'
    
    if not mode:
        print("\nNenhum modo especificado. Use --mode rapido ou --mode completo")
        print("Use --help para ver todas as opções")
        sys.exit(1)
    
    # Executar análise
    success = False
    if mode == 'rapido':
        success = sistema.run_quick_analysis()
    elif mode == 'completo':
        success = sistema.run_complete_analysis()
    
    if success:
        print(f"\nAnálise concluída com sucesso!")
        print(f"Resultados salvos em: {sistema.reports_dir.absolute()}")
        print(f"Relatório HTML: {sistema.reports_dir / 'relatorio_agro.html'}")
    else:
        print("\nAnálise falhou. Verifique os erros acima.")
        sys.exit(1)

if __name__ == "__main__":
    main()

