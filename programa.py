import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path("games_case_output")
OUT.mkdir(exist_ok=True)

def rotulo_decada(ano):
    if 1990 <= ano <= 1999:
        return "Anos 90"
    if 2000 <= ano <= 2009:
        return "Anos 2000"
    if 2010 <= ano <= 2016:
        return "Anos 2010"
    return "Outro"

def main():
    df = pd.read_excel("base de dados.xlsx")
    df.to_csv("vgsales.csv", index=False)
    df = pd.read_csv("vgsales.csv")

    df.rename(columns={
        'Vendas Globais (milhões)': 'Vendas_Global',
        'Gênero': 'Genero'
    }, inplace=True)

    #Limpeza
    faltantes = df['Ano'].isna().sum()
    df = df.dropna(subset=['Ano']).copy()
    df['Ano'] = df['Ano'].astype(int)

    #Análise descritiva
    vendas_por_genero = df.groupby('Genero')['Vendas_Global'].sum().sort_values(ascending=False)
    genero_mais_vendido = vendas_por_genero.idxmax()
    vendas_genero_top = vendas_por_genero.max()

    contagem_plataformas = df['Plataforma'].value_counts()
    plataforma_mais_lancamentos = contagem_plataformas.idxmax()
    qtd_jogos_plataforma = contagem_plataformas.max()

    # Décadas
    df['Decada'] = df['Ano'].apply(rotulo_decada)

    #Gráfico 1
    top5 = vendas_por_genero.head(5)
    plt.figure(figsize=(8,5))
    top5.plot(kind='bar', color='skyblue')
    plt.ylabel("Vendas Globais (milhões)")
    plt.title("Top 5 Gêneros por Vendas Globais")
    plt.tight_layout()
    plt.savefig(OUT / "top5_generos_bar.png")
    plt.close()

    #Gráfico 2
    jogos_por_ano = df.groupby('Ano').size().sort_index()
    plt.figure(figsize=(10,5))
    jogos_por_ano.plot(kind='line', marker='o', color='orange')
    plt.ylabel("Número de Jogos")
    plt.xlabel("Ano")
    plt.title("Total de Jogos Lançados por Ano")
    plt.tight_layout()
    plt.savefig(OUT / "jogos_por_ano_line.png")
    plt.close()

    #Salvar base limpa
    df.to_csv(OUT / "vgsales_limpo.csv", index=False)
    
    resumo = {
        "Valores faltantes em 'Ano' antes da limpeza": int(faltantes),
        "Gênero mais vendido": genero_mais_vendido,
        "Vendas (milhões)": float(round(vendas_genero_top, 2)),
        "Plataforma com mais lançamentos": plataforma_mais_lancamentos,
        "Qtde de jogos na plataforma": int(qtd_jogos_plataforma),
        "Observação": (
        "Observa-se que a maior concentração de lançamentos ocorreu nos anos 2000, "
        "e que os gêneros Action e Sports se destacam em vendas globais, "
        "indicando forte preferência do mercado por esses tipos de jogos."
    )
    }
    print("\nResumo da Análise:")
    for k, v in resumo.items():
        print(f"- {k}: {v}")

if __name__ == "__main__":
    main()
