# FIAP - Faculdade de Informática e Administração Paulista

FIAP - Faculdade de Informática e Administração Paulista 

# Análise Estatística de Dados do Agronegócio

## Grupo de Desenvolvimento

## Integrantes:

* Everton Marinho Souza (RM: 568137)
* Julia Gutierres Fernandes Souza (RM: 568296)
* Matheus Ribeiro Martelletti (RM: 566767)
* Raimunda Nayara Mendes dos Santos (RM: 567718)

## Professores:

### Tutor(a)

* Sabrina Otoni

### Coordenador(a)

* ANDRÉ GODOI CHIOVATO

## Descrição

Este projeto desenvolve uma solução completa para análise estatística de dados do agronegócio brasileiro, focando em produtividade agrícola com base em dados da CONAB e IBGE. A ferramenta permite análise estatística avançada, visualizações interativas e relatórios automatizados para tomada de decisão no setor agrícola.

O projeto atende aos requisitos do Capítulo 7, incluindo:

- Criação de base de dados Excel com 40 linhas e 6 colunas
- Análise de variáveis quantitativas (discreta e contínua) e qualitativas (nominal e ordinal)
- Estatísticas descritivas completas (medidas de tendência central, dispersão e separatrizes)
- Análise gráfica com histogramas, boxplots e gráficos de frequências
- Geração automática de relatórios em HTML

As variáveis analisadas incluem Safra (quantitativa discreta), Produtividade_t_ha (quantitativa contínua), Cultura (qualitativa nominal) e Nivel_Tecnologico (qualitativa ordinal), proporcionando uma visão abrangente da produtividade agrícola brasileira.

## Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

* **.github**: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.
* **assets**: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.
* **config**: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.
* **document**: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.
* **scripts**: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.
* **src**: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.
* **README.md**: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## Como executar o código

### Pré-requisitos

- R instalado (versão 3.8 ou superior)
- RStudio (opcional, mas recomendado)

### Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone [URL_DO_REPOSITORIO]
   cd Cap7_Fase2_Agro_Entrega
   ```

2. **Execute o script principal:**
   ```bash
   Rscript src/ENTREGA_Fase2_Cap7.R
   ```

   Ou no R/RStudio:
   ```r
   source("src/ENTREGA_Fase2_Cap7.R")
   ```

### O que o script faz automaticamente:

1. Instala dependências R necessárias (tidyverse, ggplot2, e1071, etc.)
2. Cria base de dados (`src/base_agro.xlsx`) se não existir
3. Valida e limpa os dados
4. Calcula estatísticas descritivas completas
5. Gera gráficos (histograma, boxplot, frequências)
6. Exporta resultados em CSV e HTML na pasta `document/relatorios/`

### Arquivos Gerados

Após a execução, os seguintes arquivos serão criados em `document/relatorios/`:

- `estatisticas_geral.csv` - Estatísticas descritivas gerais
- `estatisticas_por_cultura.csv` - Estatísticas por cultura
- `relatorio_agro.Rmd` - Relatório RMarkdown
- `relatorio_agro.html` - Relatório HTML final
- `graficos/` - Pasta com todos os gráficos gerados

## Histórico de lançamentos

* 1.0.0 - 15/10/2024 - Versão inicial com análise completa do agronegócio

## Licença

MODELO GIT FIAP por Fiap está licenciado sobre Attribution 4.0 International.