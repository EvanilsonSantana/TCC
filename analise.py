import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

#conexão com o Drive
from google.colab import drive
drive.mount('/content/gdrive')

codacy = pd.read_excel('/content/gdrive/MyDrive/TCC/Experimento/Vulnerabilidades_Reportadas/Codacy.xlsx')
sonar = pd.read_excel('/content/gdrive/MyDrive/TCC/Experimento/Vulnerabilidades_Reportadas/Sonarqube.xlsx')
asst = pd.read_excel('/content/gdrive/MyDrive/TCC/Experimento/Vulnerabilidades_Reportadas/ASST.xlsx')
appscan = pd.read_excel('/content/gdrive/MyDrive/TCC/Experimento/Vulnerabilidades_Reportadas/AppScan.xlsx')
deepsource = pd.read_excel('/content/gdrive/MyDrive/TCC/Experimento/Vulnerabilidades_Reportadas/Deepsource.xlsx')
snyk = pd.read_excel('/content/gdrive/MyDrive/TCC/Experimento/Vulnerabilidades_Reportadas/Snyk.xlsx')



df_codacy = pd.DataFrame(codacy)
df_sonar = pd.DataFrame(sonar)
df_asst = pd.DataFrame(asst)
df_appscan = pd.DataFrame(appscan)
df_deepsource = pd.DataFrame(deepsource)
df_snyk = pd.DataFrame(snyk)

datasets = [df_codacy, df_sonar, df_asst, df_appscan, df_deepsource, df_snyk]
nomes_datasets = ['Codacy', 'Sonar', 'ASST', 'AppScan', 'DeepSource', 'Snyk']

"""# Datasets"""

df_codacy

"""# Analise dos dados"""

df_codacy.info()

"""### Validação da Classificação"""

def verificar_datasets(df1, df2, nome_df1, nome_df2):
    num_nao_correspondentes = 0
    for index, row1 in df1.iterrows():
        for index2, row2 in df2.iterrows():
            if row1['caminho_do_arquivo'] == row2['caminho_do_arquivo'] and row1['linha'] == row2['linha']:
                if row1['verdadeiro_positivo'] != row2['verdadeiro_positivo']:
                    print("Valores não correspondentes encontrados:")
                    print(f"{nome_df1}: {row1}")
                    print(f"{nome_df2}: {row2}")
                    print()
                    num_nao_correspondentes += 1
                    break
    print(f"Total de não correspondentes entre {nome_df1} e {nome_df2}: {num_nao_correspondentes}")

# Iteração sobre todas as combinações de datasets
for i, df1 in enumerate(datasets):
    for j, df2 in enumerate(datasets):
        if i < j:  # Para evitar duplicações e comparações consigo mesmo
            verificar_datasets(df1, df2, nomes_datasets[i], nomes_datasets[j])

"""### Validação das colunas FP e TP"""

def check_values(datasets, nomes_datasets):
    for nome_df, df in zip(nomes_datasets, datasets):
        both_one = (df['verdadeiro_positivo'] == 1) & (df['falso_positivo'] == 1)
        both_zero = (df['verdadeiro_positivo'] == 0) & (df['falso_positivo'] == 0)

        print(f"\nDataset '{nome_df}':")

        if any(both_one):
            print("Linhas onde 'verdadeiro_positivo' e 'falso_positivo' são ambos 1:",
                  df[both_one].index)
        else:
            print("Não existem linhas onde 'verdadeiro_positivo' e 'falso_positivo' são ambos 1.")

        if any(both_zero):
            print("Linhas onde 'verdadeiro_positivo' e 'falso_positivo' são ambos 0:",
                  df[both_zero].index)
        else:
            print("Não existem linhas onde 'verdadeiro_positivo' e 'falso_positivo' são ambos 0.")


check_values(datasets, nomes_datasets)

"""# Análise dos Resultados"""

def plot_results(datasets):
    for i, df in enumerate(datasets):
        sum_true_positive = df['verdadeiro_positivo'].sum()
        sum_false_positive = df['falso_positivo'].sum()

        labels = ['Verdadeiros Positivos', 'Falsos Positivos']
        values = [sum_true_positive, sum_false_positive]

        plt.figure(figsize=(8, 8))
        plt.bar(labels, values, color=['green', 'red'])
        plt.xlabel('Tipo de Resultado')
        plt.ylabel('Quantidade')
        plt.title(f'Análise de Resultados de Vulnerabilidades - Dataset {i+1}: {datasets[i].name}')
        plt.ylim(0, max(max(values) + 10, 10))  # Adiciona um pouco de espaço acima da maior barra ou define mínimo como 10

        # Adiciona valores acima de cada barra
        for j in range(len(values)):
            plt.text(j, values[j] + 1, str(values[j]), ha='center', va='bottom')

        # Mostra o gráfico
        plt.show()


# Atribuindo um nome para cada dataframe
df_codacy.name = 'Codacy'
df_sonar.name = 'Sonar'
df_asst.name = 'ASST'
df_appscan.name = 'AppScan'
df_deepsource.name = 'DeepSource'
df_snyk.name = 'Snyk'

# Chamando a função para plotar os resultados para os 6 datasets
plot_results(datasets)

"""### Precisão e taxa de falsos descobertos"""

def calcular_precisao(df):
    verdadeiros_positivos = df['verdadeiro_positivo'].sum()
    falsos_positivos = df['falso_positivo'].sum()

    precisao = (verdadeiros_positivos / (verdadeiros_positivos + falsos_positivos)) * 100 if (verdadeiros_positivos + falsos_positivos) > 0 else 0
    return precisao

def calcular_fdr(df):
    verdadeiros_positivos = df['verdadeiro_positivo'].sum()
    falsos_positivos = df['falso_positivo'].sum()

    fdr = (falsos_positivos / (verdadeiros_positivos + falsos_positivos)) * 100 if (verdadeiros_positivos + falsos_positivos) > 0 else 0
    return fdr

# Calcular e mostrar a precisão e a taxa de falsos descobertos para cada conjunto de dados
precisoes = []
fdrs = []
for df, nome_df in zip(datasets, nomes_datasets):
    precisao = calcular_precisao(df)
    fdr = calcular_fdr(df)
    precisoes.append(precisao)  # Adicionando a precisão calculada à lista
    fdrs.append(fdr)            # Adicionando a FDR calculada à lista
    print(f'Precisão para {nome_df}: {precisao:.2f}%')
    print(f'Taxa de Falsos Descobertos para {nome_df}: {fdr:.2f}%')


# Configurações das cores das barras
colors = '#007acc'
fdr_color = '#d35400'

# Configuração do gráfico
fig, ax = plt.subplots(figsize=(12, 7))

# Largura das barras
bar_width = 0.4

# Posições das barras
r1 = range(len(precisoes))
r2 = [x + bar_width for x in r1]

# Criando as barras para precisão e FDR
bars1 = ax.bar(r1, precisoes, color=colors, width=bar_width, edgecolor='grey', label='Precisão', alpha=0.7)
bars2 = ax.bar(r2, fdrs, color=fdr_color, width=bar_width, edgecolor='grey', label='Taxa de Falsos Descobertos (FDR)', alpha=0.7)

# Adicionando o título e os rótulos dos eixos
ax.set_title('Precisão e Taxa de Falsos Descobertos das Ferramentas de Análise Estática de Código')
ax.set_xlabel('Ferramentas')
ax.set_ylabel('Percentual (%)')
ax.set_xticks([r + bar_width/2 for r in range(len(precisoes))])
ax.set_xticklabels(nomes_datasets)

# Adicionando valores sobre as barras para melhor visualização
for bar in bars1:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', fontweight='bold')

for bar in bars2:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', fontweight='bold')

# Adicionando a legenda
ax.legend()

# Mostrando o gráfico
plt.tight_layout()
plt.show()

"""# Apenas a Precisão"""

# Configurações das cores das barras
colors = ['#007acc', '#f7b731', '#eb3b5a', '#20bf6b', '#8854d0', '#fed330']

# Criando o gráfico de barras
plt.figure(figsize=(10, 6))
bars = plt.bar(nomes_datasets, precisoes, color=colors, alpha=0.7)

# Adicionando o título e os rótulos dos eixos
plt.title('Precisão das Ferramentas de Análise Estática de Código')
plt.xlabel('Ferramentas')
plt.ylabel('Precisão (%)')

# Adicionando valores de precisão sobre cada barra para melhor visualização
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', fontweight='bold')

# Mostrando o gráfico
plt.tight_layout()
plt.show()
