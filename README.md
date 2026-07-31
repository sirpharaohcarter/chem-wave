# chem-wave 🌊

Chemistry coming at you in a wave! 🧪🌊

A streamlined tool for accessing, querying, and retrieving chemical data from the PubChem database.

### Table of contents:

- [Features](#features)
- [Tutorial](#tutorial)
- [Configuration](#configuration)
  
## Features

* **Quick Retrieval:** Fetch compound properties, IUPAC names, and chemical structures.
* **ID Mapping:** Easily convert between SMILES and PubChem CIDs.
* **Batch Operations:** Query multiple compounds simultaneously without hitting rate limits.

## Tutorial

Here is how you can use `ChemWave` to resolve compounds and fetch properties by **Name**, **CID**, or **SMILES**:

```python
from chemwave import ChemWave

# Initialize the client (default rate-limit delay is 0.25s)
wave = ChemWave()

```

### 1. Look up CIDs directly using Name or SMILES
```python
caffeine_cid = wave.name_to_cid("caffeine")
ethanol_cid = wave.smiles_to_cid("CCO")

print(f"Caffeine CID: {caffeine_cid}")  # 2519
print(f"Ethanol CID: {ethanol_cid}")   # 702
```

### 2. Fetch properties for a single compound (by Name, CID, or SMILES)
```python
# Base properties are: "MolecularFormula", "MolecularWeight", "IUPACName"
aspirin = wave.get_compound("aspirin")
print(f"Aspirin Formula: {aspirin.get('MolecularFormula')}")
print(f"Aspirin Weight: {aspirin.get('MolecularWeight')}")

# Extract multiple chosen properties
my_props = [
    "Complexity", 
    "Charge",
    "InChIKey"
]
caffeine = wave.get_compound("caffeine", properties = my_props)
print(f"Caffeine Charge: {caffeine.get('Charge')}"
```

### 3. Batch property retrieval (fetch multiple compounds in a single request!)
```python
names = ["aspirin", "caffeine", "water"]
batch_data = wave.batch_get_compounds(names, namespace="name")

for compound in batch_data:
    print(f"• {compound.get('IUPACName')}: {compound.get('MolecularFormula')}")
```
---
## Configuration

`ChemWave` includes default rate-limiting to adhere to PubChem's API policies (max 5 requests per second).

```python
# Custom rate limit (e.g., 0.5s delay between requests)
wave = ChemWave(delay=0.5)

