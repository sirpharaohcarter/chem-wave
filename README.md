# chem-wave 🌊

*Chemistry coming at you in a wave! 🧪🌊*

A streamlined tool for accessing, querying, and retrieving chemical data from the PubChem database.

## Table of contents:

- [Features](#features)
- [Tutorial](#tutorial)
- [Supported Properties](#supported-properties)
- [Configuration](#configuration)
  
## Features

* **Quick Retrieval:** Fetch formulas, weights, and IUPAC names without fighting raw API responses.
* **Effortless ID Mapping:** Jump between common names, SMILES strings, and PubChem CIDs seamlessly.
* **Smart Batching:** Request properties for whole lists of compounds at once without getting rate-limited.
* **Friendly Error Handling:** Invalid inputs won't crash your script—ChemWave handles bad queries gracefully.

## Tutorial

Here is how you can use `ChemWave` to resolve compounds and fetch properties by **Name**, **CID**, or **SMILES**:

```python
from chemwave import ChemWave

# Initialize the client (default rate-limit delay is 0.25s)
wave = ChemWave()

```

#### 1. Look up CIDs directly using Name or SMILES
```python
caffeine_cid = wave.name_to_cid("caffeine")
ethanol_cid = wave.smiles_to_cid("CCO")

print(f"Caffeine CID: {caffeine_cid}")  # 2519
print(f"Ethanol CID: {ethanol_cid}")   # 702
```

#### 2. Fetch properties for a single compound (by Name, CID, or SMILES)
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
print(f"Caffeine Charge: {caffeine.get('Charge')}")
```

#### 3. Batch property retrieval (fetch multiple compounds in a single request!)
```python
names = ["aspirin", "caffeine", "water"]
batch_data = wave.batch_get_compounds(names, namespace="name")

for compound in batch_data:
    print(f"• {compound.get('IUPACName')}: {compound.get('MolecularFormula')}")
```

## Supported Properties

You can pass any valid PubChem PUG REST property into `properties=[...]`.

**Example Table:**

| Property Name | Example Output | Description |
| :--- | :--- | :--- |
| `MolecularFormula` | `"C9H8O4"` | Chemical formula |
| `MolecularWeight` | `180.16` | Molecular weight in g/mol |
| `IUPACName` | `"2-acetyloxybenzoic acid"` | Systematic chemical name |
| `CanonicalSMILES` | `"CC(=O)OC1=CC=CC=C1C(=O)O"` | Canonical SMILES structure |
| `InChIKey` | `"BSRRYWDWNJYHNS-UHFFFAOYSA-N"` | Unique 27-character structure hash |
| `Complexity` | `212` | Computed molecular complexity score |
| `TPSA` | `63.6` | Topological Polar Surface Area (Å²) |

## Configuration

`ChemWave` includes default rate-limiting to adhere to PubChem's API policies (max 5 requests per second).

```python
# Custom rate limit (e.g., 0.5s delay between requests)
wave = ChemWave(delay=0.5)

