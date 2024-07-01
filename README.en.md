**EN** | [Português](README.md)

# Fashion Retail Packing Optimization 📦
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-3918/)

## About The Project 📖
This project addresses a practical Bin Packing Problem (BPP) posed by Lojas Renner S.A., a fashion and lifestyle ecosystem that includes Renner, Camicado, Youcom, Realize CFI, and Repassa. Over the years, Renner has established itself as one of the largest and most traditional department store chains in Brazil, known for its wide market presence and strong e-commerce operations. The company offers a diverse range of products, including clothing, footwear, accessories, and home items. The goal of this project is to use the First Fit Decreasing (FFD) heuristic to optimize the packing of items into boxes, considering specific constraints such as volume, weight, and other logistical factors in the fashion sector. Throughout the project, we had the valuable collaboration of Guilherme Freitas Coelho, who provided support from the initial understanding of the problem to the adaptation of constraints, aiming for a better approximation to the real situations faced by the sector.

## Features 🌟
- **First Fit Decreasing Heuristic Implementation**: Uses FFD to efficiently solve the bin packing problem under complex constraints specific to fashion retail.
- **Comparison with Exact Modeling Approaches**: Assesses the performance of FFD compared to traditional exact modeling techniques, demonstrating its effectiveness in providing competitive solutions quickly.

## Getting Started 🚀
To get a local copy up and running, follow these simple steps:

### Prerequisites 📋
- Python 3.9+
- Pandas
- NumPy
- Additional dependencies in `requirements.txt`

### Installation
1. Clone the repository
   ```sh
   git clone https://github.com/CandaPin/Resolucao_Problemas.git
   ```
2. Install the necessary packages
   ```sh
   pip install -r requirements.txt
   ```

## Usage 💡
To use the project, you need to set up some files according to the specific needs of the packing process. Inside the `configs/` folder, you must add a file named `FirstFitDecreasingConfig.json`. This file should follow the format below, with paths replaced by generic values that correspond to the structure of your project:

```json
{
    "sources": {
        "BackLogOrders": {
            "from": "xlsx",
            "path": "<path_to_order_file>",
            "sheetName": "Sheet1"
        },
        "BoxTypes": {
            "from": "xlsx",
            "path": "<path_to_box_file>",
            "sheetName": "Box Types"
        }
    },
    "outputs": {
        "results": {
            "type": "csv",
            "path": "<path_to_save_results>"
        },
        "leftOver": {
            "type": "csv",
            "path": "<path_to_save_leftovers>"
        }
    }
}
```

**TODO:** Detail use case later

## Results 📊
| Model | Number of Items | Total Volume of Items [mm³] | Solution (number of boxes) | Execution Time [s] | GAP (%) | Lower Bound |
|-------|-----------------|-----------------------------|---------------------------|-------------------|---------|-------------|
| FFD         | 604             | 1,494,112,291               | 20                        | <0.01             | 0.00%   | 20          |
| Exact Model | 604             | 1,494,112,291               | 20                        | 2.7               | 0.00%   | 20          |
| FFD         | 1,021           | 3,066,413,006               | 45                        | 0.1               | 8.89%   | 41          |
| Exact Model | 1,021           | 3,066,413,006               | 41                        | 14.3              | 0.00%   | 41          |
| FFD         | 1,660           | 9,408,168,918               | 97                        | 0.5               | 1.03%   | 96          |
| Exact Model | 1,660           | 9,408,168,918               | 96                        | 6.9               | 0.00%   | 96          |
| FFD         | 2,290           | 9,012,843,586               | 124                       | 0.4               | 7.26%   | 115         |
| Exact Model | 2,290           | 9,012,843,586               | 118                       | 600               | 2.54%   | 115         |
| FFD         | 3,085           | 12,390,885,045              | 175                       | 0.6               | 8.00%   | 161         |
| Exact Model | 3,085           | 12,390,885,045              | 165                       | 900               | 2.42%   | 161         |
| FFD         | 4,032           | 17,791,897,922              | 241                       | 1.3               | 2.07%   | 236         |
| Exact Model | 4,032           | 17,791,897,922              | 238                       | 600               | 0.84%   | 236         |
| FFD         | 5,496           | 23,263,872,349              | 309                       | 1.8               | 1.29%   | 305         |
| Exact Model | 5,496           | 23,263,872,349              | 309                       | 600               | 1.29%   | 305         |
| FFD         | 7,589           | 30,081,014,981              | 395                       | 3.2               | 1.77%   | 388         |
| Exact Model | 7,589           | 30,081,014,981              | 393                       | 900               | 1.27%   | 388         |
| FFD         | 8,739           | 41,264,636,031              | 551                       | 5.7               | 0.73%   | 547         |
| Exact Model | 8,739           | 41,264,636,031              | 560                       | 900               | 2.32%   | 547         |
| FFD         | 9,312           | 35,353,480,220              | 464                       | 4.3               | 1.08%   | 459         |
| Exact Model | 9,312           | 35,353,480,220              | 501                       | 900               | 8.38%   | 459         |

