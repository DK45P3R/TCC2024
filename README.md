
# TCC2024 - Detecção de APKs Malignos com Machine Learning

Este projeto visa a detecção de aplicativos APK malignos através de técnicas de machine learning, utilizando dados de chamadas de API, opcodes e permissões. O repositório inclui código, modelos e conjuntos de dados para treinamento e avaliação.

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Uso](#uso)
- [Modelos e Dados](#modelos-e-dados)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Sobre o Projeto

Este projeto é desenvolvido como Trabalho de Conclusão de Curso (TCC) e explora o uso de algoritmos de machine learning para a detecção de ameaças em aplicativos Android (APKs). Usando dados relacionados a chamadas de API, opcodes e permissões, modelos de classificação foram treinados para distinguir entre aplicativos benignos e malignos.

## Funcionalidades

- **Classificação de APKs:** Identifica se um APK é benigno ou maligno com base em três categorias de dados.
- **Treinamento de Modelos:** Utiliza dados de chamadas de API, opcodes e permissões para treinar modelos específicos.
- **Avaliação de Modelos:** Avalia a precisão dos modelos em dados de teste.

## Estrutura do Projeto

A estrutura do repositório está organizada da seguinte forma:

```plaintext
TCC2024/
├── Andropytool/
│   ├── Extrair Características.txt
│   ├── Filtro de features.py
│   ├── Separador de features.py
│   ├── Separação_B_M.py
│   ├── Virus Total.txt
│   ├── criar csv 1.py
│   └── criar csv 2.py
├── Androzoo/
│   ├── Download.py
│   └── linha de código no promp.txt
├── Bases/
│   ├── api_calls_2b.csv
│   ├── api_calls_2m.csv
│   ├── opcodes_2b.csv
│   ├── opcodes_2m.csv
│   ├── permissions_2b.csv
│   └── permissions_2m.csv
├── Manipulando Json/
│   └── a.py
├── models/
│   ├── api_model.h5
│   ├── opcode_model.h5
│   ├── permissions_model.h5
│   ├── api_model.sav
│   ├── opcode_model.sav
│   └── permissions_model.sav
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   └── 03_model_training.ipynb
├── scripts/
│   ├── KNN.py
│   ├── MLP.py
│   └── Random_Forest.py
├── Equipe2_Adware
├── Permissions_Adware.csv
├── README.md
└── TCC.ipynb

```


### Pré-requisitos

- Python 3.9
- Gerenciador de pacotes `pip`

### Passo a Passo

Clone este repositório e instale as dependências:

```bash
# Clone este repositório
git clone https://github.com/DK45P3R/TCC2024.git

# Entre no diretório do projeto
cd TCC2024

# Instale as dependências
pip install -r requirements.txt
```

## Uso

Para treinar e avaliar os modelos de machine learning, siga as instruções abaixo.

### Treinamento do Modelo

Para treinar um modelo, execute:

```bash
python src/train_model.py --data_type api_calls  # ou "opcodes" ou "permissions"
```

### Avaliação do Modelo

Para avaliar um modelo existente, execute:

```bash
python src/evaluate_model.py --data_type api_calls  # ou "opcodes" ou "permissions"
```

## Modelos e Dados

Este projeto utiliza três tipos de dados para a classificação de APKs:

1. **API Calls:** `api_calls_2b.csv` e `api_calls_2m.csv`
2. **Opcodes:** `opcodes_2b.csv` e `opcodes_2m.csv`
3. **Permissions:** `permissions_2b.csv` e `permissions_2m.csv`

Os modelos treinados estão salvos no diretório `models/`, em formatos `.h5` para redes neurais e `.sav` para outros modelos.

## Tecnologias Utilizadas

- Python 3.9
- TensorFlow
- Scikit-learn
- Pandas
- NumPy


