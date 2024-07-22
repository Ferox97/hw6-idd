import json
import pandas as pd
import recordlinkage
from recordlinkage.index import Block

# Carica i dati dal file JSON unito
with open('merged_output.json', 'r') as file:
    data = json.load(file)

# Converti i dati in un DataFrame di pandas
df = pd.json_normalize(data)

# Visualizza le prime righe del DataFrame
print(df.head())

# Definizione delle strategie di blocking
# Prima strategia di blocking basata su 'name'
indexer1 = Block('name')

# Seconda strategia di blocking basata su 'name' e 'country'
indexer2 = Block(['name', 'country'])

# Generazione dei candidate links usando le strategie di blocking
candidate_links1 = indexer1.index(df)
candidate_links2 = indexer2.index(df)

# Creazione del comparatore di record
compare = recordlinkage.Compare()

# Aggiunta di regole di confronto solo se i campi esistono nei dati
if 'name' in df.columns:
    compare.exact('name', 'name', label='name')
if 'country' in df.columns:
    compare.exact('country', 'country', label='country')

# Calcolo del pairwise matching usando la prima strategia di blocking
features1 = compare.compute(candidate_links1, df)

# Calcolo del pairwise matching usando la seconda strategia di blocking
features2 = compare.compute(candidate_links2, df)

# Stampa dei risultati del pairwise matching
print("Pairwise matching results using the first blocking strategy (name):")
print(features1)

print("Pairwise matching results using the second blocking strategy (name and country):")
print(features2)

# Confronto dei risultati
matches1 = features1[features1.sum(axis=1) > 0]
matches2 = features2[features2.sum(axis=1) > 0]

print(f"Number of matches using the first blocking strategy (name): {len(matches1)}")
print(f"Number of matches using the second blocking strategy (name and country): {len(matches2)}")
