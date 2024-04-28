import pandas as pd
import requests, zipfile, io
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns

# 10 últimos anos 
anos = [str(i) for i in range(2013,2023)]

## Extração e tratamento dos dados
# Criação dos dataframes
colunas = ["Media mulheres","Media homens"]
medias_ES = pd.DataFrame(index=anos,columns=colunas)
medias_BR = pd.DataFrame(index=anos,columns=colunas)


for ano in anos:
    #Extração dos dados do site do inep - Censo da Educação Superior
    file_url = f"https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_{ano}.zip"
    r = requests.get(file_url,verify=False)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("dados_ed_superior/")

    if ano == "2022":
        dados = pd.read_csv(f"dados_ed_superior/microdados_educaç╞o_superior_{ano}/dados/MICRODADOS_CADASTRO_CURSOS_{ano}.CSV", sep=";",encoding='latin-1',on_bad_lines='warn')
    else:
        
        dados = pd.read_csv(f"dados_ed_superior/Microdados do Censo da Educaç╞o Superior {ano}/dados/MICRODADOS_CADASTRO_CURSOS_{ano}.CSV", sep=";",encoding='latin-1',on_bad_lines='warn')    
    
    # Código 0713: Eletricidade e energia
    dados_eletricidade_energia = dados.loc[dados["CO_CINE_AREA_DETALHADA"]==713] 
    # Código 0714: Eletrônica e automação
    dados_eletronica_automacao = dados.loc[dados["CO_CINE_AREA_DETALHADA"]==714]
    dados_eletrica = pd.merge(dados_eletricidade_energia,dados_eletronica_automacao,how="outer")

    dados_eletrica_brasil = dados_eletrica

    for local in ["Brasil","ES"]:
        
        if (local == "ES"):
            dados_eletrica = dados_eletrica.loc[dados_eletrica["SG_UF"]=="ES"]
        else:
            dados_eletrica = dados_eletrica_brasil
    
        dados_eletrica = dados_eletrica.dropna(subset = "QT_ING")
        dados_eletrica = dados_eletrica.loc[dados_eletrica["QT_ING"]!=0]

        dados_eletrica["PORC_ING_FEM"] = dados_eletrica["QT_ING_FEM"].div(dados_eletrica["QT_ING"], fill_value=-1)
        dados_eletrica["PORC_ING_MASC"] = dados_eletrica["QT_ING_MASC"].div(dados_eletrica["QT_ING"], fill_value=-1)

        if (local == "ES"):
            medias_ES.at[ano,"Media mulheres"] = dados_eletrica["PORC_ING_FEM"].mean()
            medias_ES.at[ano,"Media homens"] = dados_eletrica["PORC_ING_MASC"].mean()
        else:
            medias_BR.at[ano,"Media mulheres"] = dados_eletrica["PORC_ING_FEM"].mean()
            medias_BR.at[ano,"Media homens"] = dados_eletrica["PORC_ING_MASC"].mean()

    #Extração dos dados do site do inep - Enem
    file_url = f"https://download.inep.gov.br/microdados/microdados_enem_{ano}.zip"
    r = requests.get(file_url,verify=False)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"dados_enem/microdados_enem_{ano}")
    
    if ano == "2016":
        dados = pd.read_csv(f"dados_enem/microdados_enem_{ano}/DADOS/microdados_enem_{ano}.csv",sep=";",encoding='latin-1',on_bad_lines='warn',usecols=["TP_SEXO","SG_UF_ESC"])
    else:
        dados = pd.read_csv(f"dados_enem/microdados_enem_{ano}/DADOS/MICRODADOS_ENEM_{ano}.csv",sep=";",encoding='latin-1',on_bad_lines='warn',usecols=["TP_SEXO","SG_UF_ESC"])

    dados_ES = dados.loc[dados["SG_UF_ESC"]=="ES"]
    medias_BR.at[ano,"ENEM"]=len(dados.loc[dados["TP_SEXO"]=="F"])/len(dados)
    medias_ES.at[ano,"ENEM"]=len(dados_ES.loc[dados_ES["TP_SEXO"]=="F"])/len(dados_ES)

medias_ES = medias_ES.rename_axis('Ano').reset_index()
medias_BR = medias_BR.rename_axis('Ano').reset_index()

## Criação dos gráficos
# Multiplicar todos os números por 100
medias_ES["Media mulheres"] *= 100
medias_ES["Media homens"] *= 100
medias_ES["ENEM"] *= 100
medias_BR["Media mulheres"] *= 100
medias_BR["Media homens"] *= 100
medias_BR["ENEM"] *= 100

medias_ES.to_csv("media_ES.csv")
medias_BR.to_csv("media_BR.csv")

def plot_grafico(df):
    # Definir o estilo "darkgrid"
    sns.set_style("darkgrid")

    # Criar uma figura e eixos com tamanho maior
    fig, ax = plt.subplots(figsize=(10, 4))

    # Definir a largura das barras
    largura_barras = 0.7

    # Plotar as barras empilhadas para as médias de mulheres e homens
    bar_plot = df[['Media mulheres', 'Media homens']].plot(kind='bar', stacked=True, ax=ax, cmap="viridis",width=largura_barras)

    # Adicionar os dados do ENEM como linhas no mesmo eixo
    df['ENEM'].plot(kind='line', color='black', ax=ax, label='Mulheres no ENEM', marker='o')

    # Adicionar os valores das porcentagens nas barras
    for p in bar_plot.patches[:len(df)]:
        ax.annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    # Adicionar os valores das porcentagens nos marcadores da linha do ENEM
    for i, txt in enumerate(df['ENEM']):
        ax.annotate(f"{txt:.2f}%", (df.index[i], txt), textcoords="offset points", xytext=(0,10), ha='center')

    # Definir os rótulos e títulos
    ax.set_ylabel('Média Mulheres e Homens / Porcentagem do ENEM')
    ax.set_xlabel('Ano')
    #plt.title('Mulheres e Homens Ingressantes na Área da Eng. Elétrica vs Mulheres no ENEM \n Espírito Santo')

    # Definir os anos como rótulos do eixo x
    ax.set_xticklabels(df['Ano'])

    # Adicionar legenda com os textos personalizados
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=['Mulheres no ENEM', 'Homens na Eng. Elétrica', 'Mulheres na Elétrica'], bbox_to_anchor=(0.5, 1.15),loc='upper center',ncol = 3)

    # Mostrar o gráfico
    #plt.show()

    return fig,ax

plot_grafico(medias_ES)
plt.savefig('grafico_ES.png')
plt.show()

plot_grafico(medias_BR)
plt.savefig('grafico_BR.png')
plt.show()