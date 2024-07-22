import json
import pandas as pd
import os
import random
from itertools import combinations
from valentine import valentine_match
from valentine.algorithms import JaccardDistanceMatcher
from valentine.algorithms.jaccard_distance import StringDistanceFunction

# Funzione per leggere i file JSON
def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Funzione per normalizzare i JSON e convertirli in DataFrame
def json_to_dataframe(json_data):
    df = pd.json_normalize(json_data)
    # Ignora le colonne che contengono liste e converti tutte le altre colonne in stringhe
    for col in df.columns:
        if isinstance(df[col].iloc[0], list):
            df.drop(col, axis=1, inplace=True)
        else:
            df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, list) else str(x))
    return df

# Percorso della cartella contenente i file JSON
directory = 'sourcesJSON'

# Lettura e conversione dei file JSON in DataFrame
dataframes = {}
for file_name in os.listdir(directory):
    if file_name.endswith('.json'):
        print(f"Leggendo il file {file_name}...")
        file_path = os.path.join(directory, file_name)
        data = read_json(file_path)
        df = json_to_dataframe(data)
        dataframes[file_name] = df

print(f"\nTotale file JSON letti: {len(dataframes)}")

# Numero di coppie casuali da selezionare
num_random_pairs = 3  # Puoi cambiare questo numero secondo necessità

# Seleziona coppie casuali
all_possible_pairs = list(combinations(dataframes.items(), 2))
random_pairs = random.sample(all_possible_pairs, min(num_random_pairs, len(all_possible_pairs)))

# Inizializzazione dell'algoritmo di matching
matcher = JaccardDistanceMatcher(threshold_dist=0.8, distance_fun=StringDistanceFunction.Levenshtein)

# Confronto delle coppie casuali di DataFrame
all_matches = []
for (file1, df1), (file2, df2) in random_pairs:
    print(f"Confrontando {file1} e {file2}...")
    matches = valentine_match(df1, df2, matcher, file1, file2)
    all_matches.append((file1, file2, matches))

# Creazione dello schema mediato a partire dai matches
mediated_schema = {}

for file1, file2, matches in all_matches:
    for (col1, col2), score in matches.items():
        source_col = col1[1]  # col1 e col2 sono tuple del tipo ('table_name', 'column_name')
        mediated_schema[source_col] = 'string'  # Puoi migliorare il tipo di dato se necessario

# Aggiunta di eventuali campi non matchati
for df in dataframes.values():
    for col in df.columns:
        if col not in mediated_schema:
            mediated_schema[col] = 'string'

# Stampa dello schema mediato
print("\nSchema Mediato:")
print(json.dumps(mediated_schema, indent=2))

# Stampa dei risultati del matching con le metriche
print("\nRisultati del Matching:")
for file1, file2, matches in all_matches:
    print(f"Matches tra {file1} e {file2}:")
    for match, score in matches.items():
        print(f"  {match}: {score:.2f}")


