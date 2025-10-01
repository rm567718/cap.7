#NOME:RAIMUNDA NAYARA MENDES DOS SANTOS, RM:rm567718, FASE:2, CAPITULO:7
required_packages <- c("readxl", "dplyr", "ggplot2", "e1071")
missing_packages <- required_packages[!sapply(required_packages, requireNamespace, quietly = TRUE)]

if (length(missing_packages) > 0) {
  cat("Instalando pacotes faltantes:", paste(missing_packages, collapse = ", "), "\n")
  install.packages(missing_packages)


}

suppressPackageStartupMessages({
  library(readxl)
  library(dplyr)
  library(ggplot2)
  library(e1071)
})

cat("✓ Todas as bibliotecas carregadas com sucesso!\n")

if (!file.exists("base_agro.xlsx")) {
  stop("\n❌ ERRO: Arquivo 'base_agro.xlsx' não encontrado!\n",
       "   Verifique se o arquivo está no diretório de trabalho atual: ", getwd())
}

available_sheets <- readxl::excel_sheets("base_agro.xlsx")
if (!"Sheet1" %in% available_sheets) {
  stop("\n❌ ERRO: Planilha 'Sheet1' não encontrada!\n",
       "   Planilhas disponíveis: ", paste(available_sheets, collapse = ", "))
}

cat("📁 Carregando dados...\n")
dados <- read_xlsx("base_agro.xlsx", sheet = "Sheet1")
cat("✓ Dados carregados!\n")

if (nrow(dados) == 0) {
  stop("\  ERRO: A planilha 'Sheet1' está vazia!\n",
       "   Verifique se os dados foram inseridos corretamente.")
}

cat("\n✓ Dados carregados com sucesso!")
cat("\n  - Número de observações:", nrow(dados))
cat("\n  - Número de variáveis:", ncol(dados))
cat("\n  - Colunas:", paste(names(dados), collapse = ", "), "\n\n")
dados$Nivel_Tecnologia <- factor(dados$Nivel_Tecnologia,
                                 levels = c("Baixo", "Médio", "Alto"),
                                 ordered = TRUE)

if (!"Produtividade_t_ha" %in% names(dados)) {
  stop("\n ERRO: Coluna 'Produtividade_t_ha' não encontrada!\n",
       "   Colunas disponíveis: ", paste(names(dados), collapse = ", "))
}

x <- dados$Produtividade_t_ha

if (all(is.na(x))) {
  stop("\n ERRO: Todos os valores de produtividade são NA!\n",
       "   Verifique a qualidade dos dados na coluna 'Produtividade_t_ha'.")
}

na_count <- sum(is.na(x))
total_count <- length(x)
valid_count <- total_count - na_count

if (na_count > 0) {
  na_percent <- round((na_count / total_count) * 100, 1)
  cat(" Aviso:", na_count, "valores NA encontrados em Produtividade_t_ha")
  cat(" (", na_percent, "% dos dados)\n")
}

cat("ℹ Dados válidos para análise:", valid_count, "de", total_count, "observações\n\n")
media   <- mean(x, na.rm = TRUE)
mediana <- median(x, na.rm = TRUE)
cat("📊 Calculando estatísticas descritivas...\n")
moda <- tryCatch({
  x_clean <- x[!is.na(x)]
  if (length(x_clean) == 0) {
    NA
  } else {
    if (length(x_clean) > 10000) {
      sample_size <- min(5000, length(x_clean))
      x_sample <- sample(x_clean, sample_size)
      freq_table <- table(round(x_sample, 1))
    } else {
      freq_table <- table(round(x_clean, 1))
    }
    as.numeric(names(sort(freq_table, decreasing = TRUE)[1]))
  }
}, error = function(e) NA)

variancia <- var(x, na.rm = TRUE)
desvio    <- sd(x, na.rm = TRUE)
amplitude <- diff(range(x, na.rm = TRUE))
iqr_val   <- IQR(x, na.rm = TRUE)
cv <- ifelse(media != 0 && !is.na(media), (desvio / media) * 100, NA_real_)

quartis   <- quantile(x, probs = c(.25, .5, .75), na.rm = TRUE, names = TRUE)
decis     <- quantile(x, probs = seq(0.1, 0.9, by = 0.1), na.rm = TRUE, names = TRUE)

cat("===== TENDÊNCIA CENTRAL =====\n")
moda_texto <- ifelse(is.na(moda), "Não calculável", sprintf("%.1f", moda))
cat(sprintf("Média: %.3f | Mediana: %.3f | Moda(~1 casa): %s\n\n", media, mediana, moda_texto))
cat("===== DISPERSÃO =====\n")
cv_texto <- ifelse(is.na(cv), "Não calculável", sprintf("%.1f%%", cv))
cat(sprintf("Variância: %.3f | Desvio: %.3f | Amplitude: %.3f | IQR: %.3f | CV: %s\n\n",
            variancia, desvio, amplitude, iqr_val, cv_texto))
cat("===== QUARTIS =====\n")
print(quartis)
cat("\n===== DÉCIS =====\n")
print(decis)

print(ggplot(dados, aes(x = Produtividade_t_ha)) +
        geom_histogram(aes(y = after_stat(density)), bins = 12, alpha = 0.7,
                       fill = "lightblue", color = "black") +
        geom_density(linewidth = 1, color = "red") +
        labs(title = "Produtividade (t/ha) — Histograma e Densidade",
             x = "t/ha", y = "Densidade") +
        theme_minimal())

print(ggplot(dados, aes(x = Cultura, y = Produtividade_t_ha)) +
        geom_boxplot(fill = "lightgreen", alpha = 0.7) +
        labs(title = "Produtividade por Cultura", x = "Cultura", y = "t/ha") +
        theme_minimal() +
        theme(axis.text.x = element_text(angle = 45, hjust = 1)))

if (!"Cultura" %in% names(dados)) {
  stop("\n ERRO: Coluna 'Cultura' não encontrada!\n",
       "   Colunas disponíveis: ", paste(names(dados), collapse = ", "))
}

if (all(is.na(dados$Cultura))) {
  stop("\n ERRO: Todos os valores de Cultura são NA!\n",
       "   Verifique a qualidade dos dados na coluna 'Cultura'.")
}

cat("📊 Calculando frequências de cultura...\n")
tab_cultura <- dados %>% 
  filter(!is.na(Cultura)) %>%
  count(Cultura, name = "frequencia", sort = TRUE) %>%
  mutate(proporcao = frequencia / sum(frequencia),
         percentual = round(proporcao * 100, 1))

if (nrow(tab_cultura) > 10) {
  cat(" Aviso: Muitas categorias de cultura (", nrow(tab_cultura), "). Considere agrupar categorias menos frequentes.\n")
}

cat("\n===== TABELA DE FREQUÊNCIAS - CULTURA =====\n")
print(tab_cultura)

print(ggplot(tab_cultura, aes(x = Cultura, y = frequencia)) +
        geom_col(fill = "steelblue", alpha = 0.8) +
        geom_text(aes(label = frequencia), vjust = -0.3) +
        labs(title = "Frequências de Cultura", x = "Cultura", y = "Contagem") +
        theme_minimal() +
        theme(axis.text.x = element_text(angle = 45, hjust = 1)))

print(ggplot(tab_cultura, aes(x = Cultura, y = proporcao)) +
        geom_col(fill = "orange", alpha = 0.8) +
        geom_text(aes(label = paste0(percentual, "%")), vjust = -0.3) +
        scale_y_continuous(labels = function(x) paste0(x*100, "%")) +
        labs(title = "Proporções de Cultura", x = "Cultura", y = "Proporção") +
        theme_minimal() +
        theme(axis.text.x = element_text(angle = 45, hjust = 1)))

if ("dados_reais_conab" %in% readxl::excel_sheets("base_agro.xlsx")) {
  tryCatch({
    cat("📁 Carregando dados CONAB...\n")
    dados_reais <- read_xlsx("base_agro.xlsx", sheet = "dados_reais_conab")
    cat("✓ Dados CONAB carregados!\n")
    
    if (nrow(dados_reais) == 0) {
      cat("\nAviso: A planilha 'dados_reais_conab' está vazia.\n")
    } else {
      dados_reais$Nivel_Tecnologia <- factor(dados_reais$Nivel_Tecnologia,
                                           levels = c("Baixo", "Médio", "Alto"),
                                           ordered = TRUE)
      cat("\n===== RESUMO (CONAB - nacional) =====\n")
      required_cols <- c("Cultura", "Subtipo", "Produtividade_t_ha")
      missing_cols <- setdiff(required_cols, names(dados_reais))
      if (length(missing_cols) > 0) {
        cat("\nAviso: Colunas faltando nos dados CONAB:", paste(missing_cols, collapse = ", "), "\n")
      } else {
        print(dados_reais %>% group_by(Cultura, Subtipo) %>%
                summarise(n = n(),
                          media_prod = mean(Produtividade_t_ha, na.rm = TRUE),
                          dp = sd(Produtividade_t_ha, na.rm = TRUE),
                          .groups = "drop"))
      }
      
      feijao_data <- dados_reais %>% filter(Cultura == "Feijão")
      if (nrow(feijao_data) > 0) {
        print(ggplot(feijao_data, aes(x = Subtipo, y = Produtividade_t_ha)) +
                geom_boxplot(fill = "lightcoral", alpha = 0.7) +
                labs(title = "Feijão (Brasil) — categorias CONAB (nacional)",
                     x = "Subtipo", y = "t/ha") +
                theme_minimal() +
                theme(axis.text.x = element_text(angle = 45, hjust = 1)))
      } else {
        cat("\nAviso: Não há dados de feijão nos dados CONAB.\n")
      }
    }
  }, error = function(e) {
    cat("\nErro ao processar dados CONAB:", e$message, "\n")
  })
} else {
  cat("\nPlanilha 'dados_reais_conab' não encontrada.\n")
}
sheets <- readxl::excel_sheets("base_agro.xlsx")
if ("feijao_CE_placeholder" %in% sheets && "dados_reais_conab" %in% sheets) {
  tryCatch({
    cat("📁 Carregando dados para comparação CE vs Brasil...\n")
    ce <- read_xlsx("base_agro.xlsx", sheet = "feijao_CE_placeholder")
    br <- read_xlsx("base_agro.xlsx", sheet = "dados_reais_conab") %>%
      filter(Cultura == "Feijão") %>%
      mutate(Chave = paste0(Subtipo)) %>%
      group_by(Chave) %>%
      summarise(Prod_BR = mean(Produtividade_t_ha, na.rm = TRUE), .groups = "drop")
    
    ce <- ce %>%
      mutate(Chave = paste0(Tipo)) %>%
      group_by(Chave, Safra, Tipo) %>%
      summarise(Prod_CE = mean(Produtividade_t_ha, na.rm = TRUE), .groups = "drop")
    
    comp <- left_join(ce, br, by = "Chave") %>%
      mutate(
        Dif_abs = Prod_CE - Prod_BR,
        Dif_perc = ifelse(!is.na(Prod_BR) & Prod_BR != 0, 
                         100 * (Prod_CE / Prod_BR - 1), 
                         NA_real_)
      )
    print(comp)
    if (nrow(comp) > 0 && any(!is.na(comp$Prod_CE))) {
      print(ggplot(comp, aes(x = Tipo)) +
              geom_col(aes(y = Prod_CE), position = position_dodge(width = 0.6),
                       width = 0.5, fill = "lightblue", alpha = 0.8) +
              geom_point(aes(y = Prod_BR), size = 3, color = "red") +
              labs(title = "Feijão — Ceará (placeholder) vs Brasil (CONAB)",
                   subtitle = "Colunas: CE (t/ha). Pontos: Brasil (t/ha) — valores nacionais por subtipo",
                   x = "Tipo", y = "t/ha") +
              theme_minimal() +
              theme(axis.text.x = element_text(angle = 45, hjust = 1)))
    } else {
      cat("\nAviso: Não há dados suficientes para gerar o gráfico de comparação.\n")
    }
  }, error = function(e) {
    cat("\nErro ao processar comparação CE vs Brasil:", e$message, "\n")
  })
} else {
  cat("\nPlanilhas necessárias para comparação CE vs Brasil não encontradas.\n")
}

cat("\n", rep("=", 50), "\n")
cat("ANÁLISE CONCLUÍDA COM SUCESSO!\n")
cat("Data/Hora:", format(Sys.time(), "%d/%m/%Y %H:%M:%S"), "\n")
cat("Diretório de trabalho:", getwd(), "\n")
cat("Versão do R:", R.version.string, "\n")
cat(rep("=", 50), "\n")

rm(list = c("x", "na_count", "total_count", "valid_count", "required_packages", "missing_packages"))
if (exists("available_sheets")) rm(available_sheets)
if (exists("required_cols")) rm(required_cols)
if (exists("missing_cols")) rm(missing_cols)
if (exists("feijao_data")) rm(feijao_data)
if (exists("sheets")) rm(sheets)
if (exists("ce")) rm(ce)
if (exists("br")) rm(br)
if (exists("comp")) rm(comp)

cat("✓ Variáveis temporárias removidas da memória.\n")