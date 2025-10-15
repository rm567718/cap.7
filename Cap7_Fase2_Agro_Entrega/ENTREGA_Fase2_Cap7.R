
# ================================================================
# 📦 ENTREGA — Fase 2 | Capítulo 7
# Projeto: Sistema de Análise de Dados do Agronegócio (arquivo único)
# Autora: Raimunda Nayara Mendes dos Santos (RM: 567718)
# Instruções de uso:
#   • Requisitos: R instalado (os pacotes serão instalados automaticamente)
#   • Execução no R/RStudio: source("ENTREGA_Fase2_Cap7_Raimunda_Nayara_567718.R")
#   • Execução via terminal: Rscript ENTREGA_Fase2_Cap7_Raimunda_Nayara_567718.R
# Saídas geradas:
#   • relatorios/estatisticas_geral.csv
#   • relatorios/estatisticas_por_cultura.csv
#   • relatorios/graficos/*.png
#   • relatorios/relatorio_agro.html
# Observação: O script cria uma base sintética (base_agro.xlsx) se não existir.
# ================================================================

# -------------------------------
# 0) Função para garantir pacotes
# -------------------------------
ensure_packages <- function(pkgs) {
  to_install <- pkgs[!pkgs %in% rownames(installed.packages())]
  if (length(to_install) > 0) {
    message("Instalando pacotes: ", paste(to_install, collapse = ", "))
    install.packages(to_install, repos = "https://cloud.r-project.org")
  }
  invisible(lapply(pkgs, require, character.only = TRUE))
}

ensure_packages(c(
  "tidyverse","readxl","openxlsx","e1071","ggplot2",
  "rmarkdown","knitr","scales"
))

# -------------------------------
# 1) Configurações do projeto
# -------------------------------
config <- list(
  autora   = "Raimunda Nayara Mendes dos Santos",
  rm       = "567718",
  fase     = 2,
  capitulo = 7,
  base_xlsx = "base_agro.xlsx",
  saida_dir = "relatorios",
  graficos_dir = file.path("relatorios","graficos"),
  relatorio_rmd = file.path("relatorios","relatorio_agro.Rmd"),
  relatorio_html = file.path("relatorios","relatorio_agro.html")
)

dir.create(config$saida_dir, showWarnings = FALSE, recursive = TRUE)
dir.create(config$graficos_dir, showWarnings = FALSE, recursive = TRUE)

# -------------------------------
# 2) Criar base de exemplo se não existir
# -------------------------------
if (!file.exists(config$base_xlsx)) {
  set.seed(42)
  n <- 40
  cultura <- sample(c("Arroz","Feijão"), size = n, replace = TRUE, prob = c(0.5,0.5))
  subtipo <- ifelse(cultura == "Feijão",
                    sample(c("Preto","Caupi","Cores"), size = n, replace = TRUE),
                    NA_character_)
  produtividade <- round(rnorm(n, mean = ifelse(cultura=="Arroz", 4.8, 3.2), sd = 0.8), 2)
  produtividade[produtividade < 0] <- runif(sum(produtividade < 0), 0.5, 1.0)

  dados <- tibble::tibble(
    Safra = sample(2019:2024, n, replace = TRUE),
    Regiao = sample(c("Brasil","Ceará"), n, replace = TRUE, prob = c(0.7,0.3)),
    Cultura = cultura,
    Subtipo = subtipo,
    Produtividade_t_ha = produtividade,
    Nivel_Tecnologico = sample(c("Baixo","Médio","Alto"), n, replace = TRUE)
  )

  openxlsx::write.xlsx(dados, config$base_xlsx)
  message("Base de exemplo criada: ", config$base_xlsx)
}

# -------------------------------
# 3) Leitura e validação
# -------------------------------
dados <- readxl::read_excel(config$base_xlsx)

mensagens_validacao <- list()

# Tipos básicos
esperados <- c("Safra","Regiao","Cultura","Subtipo","Produtividade_t_ha","Nivel_Tecnologico")
faltantes <- setdiff(esperados, names(dados))
if (length(faltantes) > 0) {
  stop("Colunas faltando na base: ", paste(faltantes, collapse = ", "))
}

# Regras simples
if (any(is.na(dados$Produtividade_t_ha))) {
  mensagens_validacao <- c(mensagens_validacao, "Há valores NA em Produtividade_t_ha — serão removidos.")
}
if (any(dados$Produtividade_t_ha < 0 | dados$Produtividade_t_ha > 20, na.rm = TRUE)) {
  mensagens_validacao <- c(mensagens_validacao, "Há produtividades fora do intervalo [0,20] t/ha — serão capadas.")
}

# Limpeza
dados <- dados |>
  dplyr::mutate(
    Produtividade_t_ha = pmin(pmax(Produtividade_t_ha, 0), 20),
    Cultura = factor(Cultura, levels = c("Arroz","Feijão"))
  ) |>
  dplyr::filter(!is.na(Produtividade_t_ha))

# Salvar mensagens de validação
if (length(mensagens_validacao) > 0) {
  writeLines(mensagens_validacao, con = file.path(config$saida_dir, "validacao.log"))
}

# -------------------------------
# 4) Estatísticas descritivas
# -------------------------------
library(e1071)

desc_geral <- dados |>
  dplyr::summarise(
    n = dplyr::n(),
    media = mean(Produtividade_t_ha),
    mediana = median(Produtividade_t_ha),
    dp = sd(Produtividade_t_ha),
    minimo = min(Produtividade_t_ha),
    maximo = max(Produtividade_t_ha),
    assimetria = e1071::skewness(Produtividade_t_ha),
    curtose = e1071::kurtosis(Produtividade_t_ha)
  )

desc_por_cultura <- dados |>
  dplyr::group_by(Cultura) |>
  dplyr::summarise(
    n = dplyr::n(),
    media = mean(Produtividade_t_ha),
    mediana = median(Produtividade_t_ha),
    dp = sd(Produtividade_t_ha),
    minimo = min(Produtividade_t_ha),
    maximo = max(Produtividade_t_ha),
    .groups = "drop"
  )

readr::write_csv(desc_geral, file.path(config$saida_dir, "estatisticas_geral.csv"))
readr::write_csv(desc_por_cultura, file.path(config$saida_dir, "estatisticas_por_cultura.csv"))

# -------------------------------
# 5) Gráficos
# -------------------------------
library(ggplot2)

p1 <- ggplot(dados, aes(x = Produtividade_t_ha)) +
  geom_histogram(aes(y=..density..), bins = 12) +
  geom_density(linewidth = 1) +
  labs(title = "Produtividade (t/ha) — Histograma e Densidade",
       x = "t/ha", y = "Densidade")

p2 <- ggplot(dados, aes(x = Cultura, y = Produtividade_t_ha)) +
  geom_boxplot() +
  labs(title = "Produtividade por Cultura",
       x = "Cultura", y = "t/ha")

freq <- dados |>
  dplyr::count(Cultura) |>
  dplyr::mutate(prop = n / sum(n))

p3 <- ggplot(freq, aes(x = Cultura, y = n)) +
  geom_col() +
  geom_text(aes(label = scales::percent(prop, accuracy = 0.1)), vjust = -0.5) +
  labs(title = "Frequências e Proporções por Cultura", x = "Cultura", y = "Contagem")

dados_feijao <- dplyr::filter(dados, Cultura == "Feijão" & !is.na(Subtipo))
if (nrow(dados_feijao) > 0) {
  p4 <- ggplot(dados_feijao, aes(x = Subtipo, y = Produtividade_t_ha)) +
    stat_summary(fun = mean, geom = "col") +
    labs(title = "Feijão — Produtividade média por subtipo (CONAB)", x = "Subtipo", y = "t/ha")
} else {
  p4 <- ggplot() + labs(title = "Sem dados de subtipos de Feijão disponíveis")
}

ggsave(file.path(config$graficos_dir, "hist_densidade.png"), p1, width = 8, height = 5, dpi = 120)
ggsave(file.path(config$graficos_dir, "boxplot_cultura.png"), p2, width = 8, height = 5, dpi = 120)
ggsave(file.path(config$graficos_dir, "frequencias_cultura.png"), p3, width = 8, height = 5, dpi = 120)
ggsave(file.path(config$graficos_dir, "feijao_subtipos.png"), p4, width = 8, height = 5, dpi = 120)

# -------------------------------
# 6) Gerar RMarkdown e HTML
# -------------------------------
rmd_conteudo <- '---
title: "Relatório do Agronegócio — Capítulo 7"
author: "Raimunda Nayara Mendes dos Santos (RM: 567718)"
date: "`r format(Sys.Date(), \"%d/%m/%Y\")`"
output:
  html_document:
    toc: true
    toc_depth: 3
    theme: flatly
    df_print: paged
---

## Visão Geral

**Fase 2 — Capítulo 7.** Este relatório apresenta validação, estatísticas descritivas e visualizações de produtividade agrícola (CONAB/IBGE como referência).

## Estatísticas

```{r}
desc_geral <- readr::read_csv("relatorios/estatisticas_geral.csv", show_col_types = FALSE)
desc_por_cultura <- readr::read_csv("relatorios/estatisticas_por_cultura.csv", show_col_types = FALSE)

desc_geral
desc_por_cultura
```

## Gráficos

### Histograma + Densidade
![](graficos/hist_densidade.png)

### Produtividade por Cultura
![](graficos/boxplot_cultura.png)

### Frequências por Cultura (com proporções)
![](graficos/frequencias_cultura.png)

### Feijão — Subtipos (média)
![](graficos/feijao_subtipos.png)
'

writeLines(rmd_conteudo, con = config$relatorio_rmd)

# Tenta renderizar o HTML (se o rmarkdown estiver OK)
try({
  rmarkdown::render(input = config$relatorio_rmd, output_file = basename(config$relatorio_html), output_dir = config$saida_dir, quiet = TRUE)
  message("Relatório HTML gerado em: ", config$relatorio_html)
}, silent = TRUE)

message("✅ Execução concluída. Arquivos gerados em: ", normalizePath(config$saida_dir))
