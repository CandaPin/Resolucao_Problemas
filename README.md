[English](README.en.md) | **PT**

# Otimização de Empacotamento no Varejo de Moda 📦
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-3918/)

## Sobre o Projeto 📖
Repositório destinado ao desenvolvimento do projeto proposto na disciplina "Resolução de Problemas via Modelagem Matemática", oferecida pela Unifesp, campus de São José dos Campos (https://sites.google.com/view/model-matematica/projetos).
Este projeto aborda um problema prático de Empacotamento Binário (Bin Packing Problem - BPP) proposto pela Companhia Lojas Renner S.A., um ecossistema de moda e estilo de vida que inclui Renner, Camicado, Youcom, Realize CFI e Repassa. Ao longo dos anos, a Renner consolidou-se como uma das maiores e mais tradicionais redes de lojas de departamento do Brasil, reconhecida por sua ampla presença no mercado e forte atuação no comércio eletrônico. A empresa oferece uma variedade de produtos, incluindo roupas, calçados, acessórios e itens para o lar. O objetivo deste projeto é utilizar a heurística First Fit Decreasing (FFD) para otimizar o empacotamento de itens em caixas, considerando restrições específicas como volume, peso e outros fatores logísticos do setor de moda. Durante o projeto, contamos com a valiosa colaboração de Guilherme Freitas Coelho, que ofereceu suporte desde a compreensão inicial do problema até a adaptação das restrições, visando uma melhor aproximação às situações reais enfrentadas pelo setor.

## Funcionalidades 🌟
- **Implementação da Heurística First Fit Decreasing**: Utiliza FFD para resolver de forma eficiente o problema de empacotamento binário sob restrições complexas específicas para o varejo de moda.
- **Comparação com Abordagens de Modelagem Exata**: Avalia o desempenho do FFD em comparação com técnicas de modelagem exata tradicionais, demonstrando sua eficácia em fornecer soluções competitivas de forma rápida.

## Primeiros Passos 🚀
Para obter uma cópia local e executá-la, siga estes passos simples:

### Pré-requisitos 📋
- Python 3.9+
- Pandas
- NumPy
- Demais dependências em `requirements.txt`

### Instalação
1. Clone o repositório
   ```sh
   git clone https://github.com/CandaPin/Resolucao_Problemas.git
   ```
2. Instale os pacotes necessários
   ```sh
   pip install -r requirements.txt
   ```

## Uso 💡
Para utilizar o projeto, é necessário configurar alguns arquivos de acordo com as necessidades específicas do processo de empacotamento. Dentro da pasta `configs/`, você deve adicionar um arquivo chamado `FirstFitDecreasingConfig.json`. Este arquivo deve seguir o formato abaixo, substituindo os caminhos por valores genéricos que correspondam à estrutura do seu projeto:

```json
{
    "sources": {
        "BackLogOrdens": {
            "from": "xlsx",
            "path": "<caminho_para_o_arquivo_de_ordens>",
            "sheetName": "Sheet1"
        },
        "TiposDeCaixa": {
            "from": "xlsx",
            "path": "<caminho_para_o_arquivo_de_caixas>",
            "sheetName": "Tipos de caixa"
        }
    },
    "outputs": {
        "results": {
            "type": "csv",
            "path": "<caminho_para_salvar_resultados>"
        },
        "leftOver": {
            "type": "csv",
            "path": "<caminho_para_salvar_sobras>"
        }
    }
}
```

**TODO:** Detalhar usecase depois

## Resultados 📊
| Modelo | Quantidade de itens | Volume total dos itens [mm³] | Solução (qtde caixas) | Tempo de execução [s] | GAP (%) | Limitante inferior |
|--------|---------------------|------------------------------|-----------------------|----------------------|---------|--------------------|
| FFD    | 604                 | 1.494.112.291                | 20                    | <0,01                | 0,00%   | 20                 |
| Exato  | 604                 | 1.494.112.291                | 20                    | 2,7                  | 0,00%   | 20                 |
| FFD    | 1.021               | 3.066.413.006                | 45                    | 0,1                  | 8,89%   | 41                 |
| Exato  | 1.021               | 3.066.413.006                | 41                    | 14,3                 | 0,00%   | 41                 |
| FFD    | 1.660               | 9.408.168.918                | 97                    | 0,5                  | 1,03%   | 96                 |
| Exato  | 1.660               | 9.408.168.918                | 96                    | 6,9                  | 0,00%   | 96                 |
| FFD    | 2.290               | 9.012.843.586                | 124                   | 0,4                  | 7,26%   | 115                |
| Exato  | 2.290               | 9.012.843.586                | 118                   | 600                  | 2,54%   | 115                |
| FFD    | 3.085               | 12.390.885.045               | 175                   | 0,6                  | 8,00%   | 161                |
| Exato  | 3.085               | 12.390.885.045               | 165                   | 900                  | 2,42%   | 161                |
| FFD    | 4.032               | 17.791.897.922               | 241                   | 1,3                  | 2,07%   | 236                |
| Exato  | 4.032               | 17.791.897.922               | 238                   | 600                  | 0,84%   | 236                |
| FFD    | 5.496               | 23.263.872.349               | 309                   | 1,8                  | 1,29%   | 305                |
| Exato  | 5.496               | 23.263.872.349               | 309                   | 600                  | 1,29%   | 305                |
| FFD    | 7.589               | 30.081.014.981               | 395                   | 3,2                  | 1,77%   | 388                |
| Exato  | 7.589               | 30.081.014.981               | 393                   | 900                  | 1,27%   | 388                |
| FFD    | 8.739               | 41.264.636.031               | 551                   | 5,7                  | 0,73%   | 547                |
| Exato  | 8.739               | 41.264.636.031               | 560                   | 900                  | 2,32%   | 547                |
| FFD    | 9.312               | 35.353.480.220               | 464                   | 4,3                  | 1,08%   | 459                |
| Exato  | 9.312               | 35.353.480.220               | 501                   | 900                  | 8,38%   | 459                |
