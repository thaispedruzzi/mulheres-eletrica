# Análise do ingresso das mulheres nos cursos superiores das área de eletricidade, energia, eletrônica e automação

## Dados
### 1. Microdados do **Censo da Educação Superior** elaborado pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira | Inep

#### O que queremos descobrir a partir dessa base
1. *Percentual de ingressantes mulheres nos cursos de interesse (engenharia elétrica e correlatos) em cada ano, no Brasil*
2. *Percentual de ingressantes mulheres nos cursos de interesse (engenharia elétrica e correlatos) em cada ano, no Espírito Santo*

#### Sobre a base
- Onde obter: https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/censo-da-educacao-superior/resultados
- Anos analisados: 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021 e 2022
- Atributos utilizados:
  
| Nome da Variável       | Descrição da Variável                                                                                                            |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| SG_UF                  | Sigla da Unidade da Federação do local de oferta do curso                                                                        |
| CO_CINE_AREA_DETALHADA | Código de identificação da área detalhada, conforme adaptação da Classificação Internacional Normalizada da Educação Cine/Unesco |
| QT_ING                 | Quantidade de ingressantes                                                                                                       |
| QT_ING_FEM             | Quantidade de ingressantes do sexo feminino                                                                                      |
| QT_ING_MASC            | Quantidade de ingressantes do sexo masculino                                                                                     |

- Áreas detalhadas consideradas: 713 (Eletricidade e energia) e 714 (Eletrônica e automação)

### 2. Microdados do **Exame Nacional do Ensino Médio (ENEM)** elaborado pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira | Inep

#### O que queremos descobrir a partir dessa base
1. *Percentual de inscritas mulheres no ENEM em cada ano, no Brasil*
2. *Percentual de inscritas mulheres no ENEM em cada ano, no Espírito Santo*

#### Sobre a base
- Onde obter: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem
- Anos analisados: 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021 e 2022
- Atributos utilizados:

| Nome da Variável | Descrição                               |
|------------------|-----------------------------------------|
| SG_UF_ESC        | Sigla da Unidade da Federação da escola |
| TP_SEXO          | Sexo (F: feminino ou M: masculino)      |
   
## Tratamento dos dados
### Censo da educação superior
1. Filtro dos dados referentes às areas "eletricidade e energia" e "eletrônica e automação"
```python
# Código 0713: Eletricidade e energia
dados_eletricidade_energia = dados.loc[dados["CO_CINE_AREA_DETALHADA"]==713] 
# Código 0714: Eletrônica e automação
dados_eletronica_automacao = dados.loc[dados["CO_CINE_AREA_DETALHADA"]==714]
dados_eletrica = pd.merge(dados_eletricidade_energia,dados_eletronica_automacao,how="outer")
```
2. Eliminação de dados faltantes (NaN) e cursos com quantidade de ingressantes igual a zero
```python
dados_eletrica = dados_eletrica.dropna(subset = "QT_ING")
dados_eletrica = dados_eletrica.loc[dados_eletrica["QT_ING"]!=0]
```
4. Cálculo da porcentagem de mulheres e homens ingressantes nos cursos
```python
dados_eletrica["PORC_ING_FEM"] = dados_eletrica["QT_ING_FEM"].div(dados_eletrica["QT_ING"], fill_value=-1)
dados_eletrica["PORC_ING_MASC"] = dados_eletrica["QT_ING_MASC"].div(dados_eletrica["QT_ING"], fill_value=-1)
```
### ENEM
1. Cálculo da porcentagem de mulheres inscritas
```python
medias_BR.at[ano,"ENEM"]=len(dados.loc[dados["TP_SEXO"]=="F"])/len(dados)
medias_ES.at[ano,"ENEM"]=len(dados_ES.loc[dados_ES["TP_SEXO"]=="F"])/len(dados_ES)
```

## Resultados 
