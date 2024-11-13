import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import LambdaCallback
import csv

# Função de callback para imprimir informações sobre o número de amostras
def on_epoch_end(epoch, logs):
    print(f"\nÉpoca {epoch + 1}:")
    print(f"Número de amostras no treino: {X_train.shape[0]}")
    print(f"Número de amostras no teste: {X_test.shape[0]}")

# Carregar dados dos arquivos CSV com número máximo de campos
csv_file_benign = 'api_calls_2b.csv'
csv_file_malign = 'api_calls_2m.csv'

# Determinar o número máximo de colunas entre os arquivos
num_cols_benign = pd.read_csv(csv_file_benign, encoding='ISO-8859-1', sep=';', quoting=csv.QUOTE_NONE, on_bad_lines='skip').shape[1]
num_cols_malign = pd.read_csv(csv_file_malign, encoding='ISO-8859-1', sep=';', quoting=csv.QUOTE_NONE, on_bad_lines='skip').shape[1]
max_num_cols = max(num_cols_benign, num_cols_malign)

# Carregar os dados com o número máximo de colunas, preenchendo faltantes com NaN
data_benign = pd.read_csv(csv_file_benign, encoding='ISO-8859-1', sep=';', names=range(max_num_cols), quoting=csv.QUOTE_NONE, on_bad_lines='warn')
data_malign = pd.read_csv(csv_file_malign, encoding='ISO-8859-1', sep=';', names=range(max_num_cols), quoting=csv.QUOTE_NONE, on_bad_lines='warn')

# Adicionar coluna de classe ("benigno" ou "maligno")
data_benign['classe'] = 'benigno'
data_malign['classe'] = 'maligno'

# Remover a coluna "Nome do Arquivo" de cada dataset, caso exista
if 'Nome do Arquivo' in data_benign.columns:
    data_benign = data_benign.drop(columns=['Nome do Arquivo'])
if 'Nome do Arquivo' in data_malign.columns:
    data_malign = data_malign.drop(columns=['Nome do Arquivo'])

# Realizar undersampling nos dados benignos para igualar o número de amostras malignas
data_benign_downsampled = resample(data_benign, replace=False, n_samples=len(data_malign), random_state=42)

# Concatenar os datasets balanceados
data_full = pd.concat([data_benign_downsampled, data_malign], axis=0)

# Separar entradas (X) e rótulos (y) do dataset
X = data_full.iloc[:, :-1]  # Excluir a última coluna (classe)
y = data_full.iloc[:, -1]   # Última coluna, que contém as classes

# Converter colunas para numéricas e preencher valores faltantes com 0.0
X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

# Converter rótulos de texto para valores numéricos
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Garantir que os dados estejam no formato correto
X = X.astype(np.float32)
y = y.astype(np.int32)

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Converter rótulos para formato categórico (detecção binária)
y_train = to_categorical(y_train, num_classes=2)
y_test = to_categorical(y_test, num_classes=2)

# Criar e compilar o modelo MLP
model = Sequential()
model.add(Dense(1024, activation='sigmoid', input_shape=(X_train.shape[1],)))
model.add(Dropout(0.1))
model.add(Dense(1024, activation='relu'))
model.add(Dense(2, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Definir o callback e treinar o modelo
print_callback = LambdaCallback(on_epoch_end=on_epoch_end)
model.fit(X_train, y_train, batch_size=32, epochs=50, validation_data=(X_test, y_test), callbacks=[print_callback])

# Avaliação e relatório
from sklearn.metrics import classification_report, confusion_matrix

y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_test_classes = np.argmax(y_test, axis=1)

report = classification_report(y_test_classes, y_pred_classes, target_names=['benigno', 'maligno'])
print("\nRelatório de Classificação:\n", report)

conf_matrix = confusion_matrix(y_test_classes, y_pred_classes)
print("Matriz de Confusão:\n", conf_matrix)

# Salvar o modelo
model.save('MLP_API.h5')
print("Modelo salvo como 'MLP_API.h5'")
