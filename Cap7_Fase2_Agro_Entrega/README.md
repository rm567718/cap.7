# 🌾 Sistema de Análise de Dados do Agronegócio

## 📋 Sobre o Projeto

Este projeto desenvolve uma solução completa para análise de dados do agronegócio brasileiro, focando em produtividade agrícola, sustentabilidade e inovação tecnológica. A ferramenta permite análise estatística avançada, visualizações interativas e relatórios automatizados para tomada de decisão no setor agrícola.

## 🎯 Objetivos

- **Análise Estatística**: Estatísticas descritivas completas de produtividade agrícola
- **Validação de Dados**: Sistema robusto de validação e limpeza de dados
- **Visualizações**: Gráficos interativos e informativos para análise visual
- **Comparação Regional**: Análise comparativa entre diferentes regiões do Brasil
- **Relatórios**: Geração automática de relatórios em HTML
- **Inovação**: Implementação de técnicas de análise preditiva e machine learning

## 🚀 Funcionalidades Principais

### 1. **Validação Inteligente de Dados**
- Verificação automática de tipos de dados
- Detecção e tratamento de valores ausentes
- Validação de intervalos e consistência
- Limpeza automática de dados inconsistentes

### 2. **Análise Estatística Avançada**
- Estatísticas descritivas completas (média, mediana, moda, desvio padrão)
- Análise de distribuição e tendências
- Cálculo de quartis e decis
- Análise de correlações entre variáveis

### 3. **Visualizações Interativas**
- Histogramas com curvas de densidade
- Boxplots para análise por categoria
- Gráficos de barras para frequências
- Gráficos comparativos regionais

### 4. **Análise Comparativa**
- Comparação entre diferentes culturas
- Análise regional (Ceará vs Brasil)
- Comparação temporal por safra
- Benchmarking de produtividade

### 5. **Relatórios Automatizados**
- Geração de relatórios em HTML
- Exportação de gráficos em alta resolução
- Sumários executivos automáticos
- Dados para tomada de decisão

## 📊 Dados Analisados

### Variáveis Principais
- **Produtividade (t/ha)**: Produtividade por hectare
- **Cultura**: Tipo de cultura agrícola
- **Nível Tecnológico**: Baixo, Médio, Alto
- **Região**: Localização geográfica
- **Safra**: Período de cultivo

### Fontes de Dados
- **CONAB**: Dados oficiais de produtividade nacional
- **Dados Regionais**: Informações específicas do Ceará
- **Dados Simulados**: Para demonstração e testes

## 🛠️ Tecnologias Utilizadas

- **R**: Linguagem principal para análise estatística
- **ggplot2**: Visualizações avançadas
- **dplyr**: Manipulação de dados
- **readxl**: Leitura de arquivos Excel
- **e1071**: Análise estatística avançada
- **rmarkdown**: Geração de relatórios

## 📁 Estrutura do Projeto

```
cap.7/
├── README.md                 # Documentação principal
├── analise_agro.R           # Script principal de análise
├── validacao_dados.R        # Script de validação
├── relatorio_agro.Rmd       # Template de relatório
├── base_agro.xlsx           # Base de dados principal
├── funcoes_auxiliares.R     # Funções auxiliares
├── config.R                 # Configurações do sistema
└── relatorios/              # Pasta para relatórios gerados
    ├── relatorio_YYYYMMDD.html
    └── graficos/
```

## 🚀 Como Usar

### 1. **Instalação de Dependências**

#### Para Python:
```bash
# Opção 1: Usar o instalador automático
python install_deps.py

# Opção 2: Usar o arquivo batch (Windows)
install_dependencies.bat

# Opção 3: Usar o PowerShell (Windows)
powershell -ExecutionPolicy Bypass -File install_dependencies.ps1

# Opção 4: Instalação manual
pip install pandas numpy matplotlib seaborn openpyxl scipy

# Opção 5: Usar requirements.txt
pip install -r requirements.txt
```

#### Para R:
```r
# Execute o script principal - as dependências serão instaladas automaticamente
source("ENTREGA_Fase2_Cap7.R")
```

### 2. **Verificação de Dependências**
```bash
# Verificar se todas as dependências estão instaladas
python main.py --deps
```

### 3. **Troubleshooting - Erro de Importação**

#### Erro de matplotlib.pyplot:
```
❌ Não foi possível resolver a importação "matplotlib.pyplot"
```

**Soluções:**

1. **Instalar matplotlib:**
   ```bash
   pip install matplotlib
   ```

2. **Reinstalar matplotlib:**
   ```bash
   pip uninstall matplotlib -y
   pip install matplotlib --force-reinstall
   ```

3. **Usar ambiente virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install matplotlib seaborn pandas numpy
   ```

4. **Verificar instalação:**
   ```bash
   python -c "import matplotlib.pyplot as plt; print('matplotlib OK')"
   ```

#### Erro de pandas:
```
❌ pandas não encontrado: cannot import name 'NaT' from 'pandas._libs'
```

**Soluções:**

1. **Reinstalar pandas:**
   ```bash
   pip uninstall pandas -y
   pip install pandas --force-reinstall
   ```

2. **Instalar versão específica:**
   ```bash
   pip install pandas==2.0.3 numpy==1.24.3
   ```

3. **Verificar Python path:**
   ```bash
   python -c "import sys; print(sys.path)"
   ```

### 2. **Validação de Dados**
```r
# Valide seus dados antes da análise
source("validacao_dados.R")
validar_dados("base_agro.xlsx")
```

### 3. **Análise Completa**
```r
# Execute a análise completa
source("analise_agro.R")
```

### 4. **Geração de Relatório**
```r
# Gere relatório em HTML
rmarkdown::render("relatorio_agro.Rmd")
```

## 📈 Inovações Implementadas

### 1. **Sistema de Validação Inteligente**
- Detecção automática de outliers
- Validação de consistência temporal
- Verificação de integridade referencial

### 2. **Análise Preditiva**
- Modelos de regressão para previsão de produtividade
- Análise de tendências sazonais
- Identificação de padrões de crescimento

### 3. **Interface Interativa**
- Menu de opções para diferentes análises
- Validação em tempo real de entradas do usuário
- Feedback visual durante processamento

### 4. **Relatórios Dinâmicos**
- Relatórios adaptativos baseados nos dados
- Gráficos interativos com plotly
- Exportação em múltiplos formatos

## 🔧 Configurações

### Personalização de Análises
```r
# Configure parâmetros no arquivo config.R
source("config.R")

# Ajuste configurações
config$graficos$tema <- "minimal"
config$relatorio$formato <- "html"
config$validacao$tolerancia_na <- 0.1
```

## 📊 Exemplos de Uso

### Análise de Produtividade por Cultura
```r
# Análise específica de uma cultura
analisar_cultura("Soja", dados)
```

### Comparação Regional
```r
# Compare produtividade entre regiões
comparar_regioes("Ceará", "Brasil", dados)
```

### Análise Temporal
```r
# Analise tendências ao longo do tempo
analisar_tendencias(dados, periodo = "anual")
```

## 🎯 Aplicações no Agronegócio

### 1. **Tomada de Decisão**
- Identificação de culturas mais produtivas
- Análise de viabilidade econômica
- Planejamento de safras

### 2. **Gestão de Recursos**
- Otimização do uso de insumos
- Análise de eficiência tecnológica
- Planejamento de investimentos

### 3. **Sustentabilidade**
- Análise de impacto ambiental
- Monitoramento de práticas sustentáveis
- Relatórios de conformidade

### 4. **Inovação Tecnológica**
- Avaliação de novas tecnologias
- Análise de ROI de investimentos
- Benchmarking tecnológico

## 📚 Referências

- **BOLFE, E. L. et al.** Agricultura digital: pesquisa, desenvolvimento e inovação nas cadeias produtivas. 2020.
- **EMBRAPA.** Visão de futuro. 2022.
- **FAO.** FAOSTAT. 2022.
- **CONAB.** Dados de preços de produtos agrícolas.
- **SERASA EXPERIAN.** Soluções para agro.

## 👥 Contribuições

Este projeto foi desenvolvido como parte do Capítulo 7 do curso, focando em:
- Análise estatística aplicada ao agronegócio
- Desenvolvimento de soluções inovadoras
- Aplicação de tecnologias digitais na agricultura
- Sustentabilidade e eficiência produtiva

## 📞 Suporte

Para dúvidas ou sugestões sobre o projeto, consulte:
- Documentação técnica nos arquivos de código
- Comentários inline no código R
- Exemplos de uso nos scripts de demonstração

---

**Desenvolvido por:** Raimunda Nayara Mendes dos Santos  
**RM:** 567718  
**Fase:** 2  
**Capítulo:** 7  

*Sistema de Análise de Dados do Agronegócio - Versão 1.0*
