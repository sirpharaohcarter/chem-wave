from chemwave import ChemWave

from chemwave import ChemWave

wave = ChemWave()

# Test 1: Batch lookup by CIDs
print("🌊 Batch querying by CIDs...")
cids = [2244, 702]
cid_results = wave.batch_get_compounds(cids, namespace="cid")
print(f"Retrieved {len(cid_results)} compounds by CID.")

# Test 2: Batch lookup by Names
print("\n🌊 Batch querying by Names...")
names = ["aspirin", "caffeine", "water"]
name_results = wave.batch_get_compounds(names, namespace="name")
for item in name_results:
    print(f"• {item.get('IUPACName')}: {item.get('MolecularFormula')}")

# Test 3: Batch lookup by SMILES
print("\n🌊 Batch querying by SMILES...")
smiles_list = ["CCO", "O"]  # Ethanol, Water
smiles_results = wave.batch_get_compounds(smiles_list, namespace="smiles")
for item in smiles_results:
    print(f"• CID {item.get('CID')}: Weight={item.get('MolecularWeight')}")


#previous tests (just for record, some may be faulty)

'''

wave = ChemWave()

# Aspirin SMILES: CC(=O)OC1=CC=CC=C1C(=O)O
aspirin_smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"

print("🌊 Querying compound properties using SMILES...")
aspirin_data = wave.get_compound(aspirin_smiles, namespace="smiles")

print(f"IUPAC Name: {aspirin_data.get('IUPACName')}")
print(f"Molecular Weight: {aspirin_data.get('MolecularWeight')}")


wave = ChemWave()

print("🌊 Testing batch_get_compounds()...")

# Aspirin (2244), Ethanol (702), Water (962)
test_cids = [2244, 702, 962]

results = wave.batch_get_compounds(test_cids)

for compound in results:
    print(f"• CID {compound.get('CID')}: Formula={compound.get('MolecularFormula')}, Weight={compound.get('MolecularWeight')}")


wave = ChemWave()

print("🌊 Testing smiles_to_cid()...")

# Ethanol
ethanol_cid = wave.smiles_to_cid("CCO")
print(f"Ethanol ('CCO') CID: {ethanol_cid}")

# Aspirin
aspirin_cid = wave.smiles_to_cid("CC(=O)OC1=CC=CC=C1C(=O)O")
print(f"Aspirin SMILES CID: {aspirin_cid}")

# invalid
invalid_cid = wave.smiles_to_cid("NOT_A_SMILES_STRING")
print(f"Invalid SMILES CID: {invalid_cid}")


wave = ChemWave()

print("🌊 Testing get_compound('caffeine')...")
caffeine_data = wave.get_compound("caffeine")
print(caffeine_data)

print("\n🌊 Testing custom property lookup for 'aspirin'...")
aspirin_data = wave.get_compound("aspirin", properties=["MolecularFormula", "MolecularWeight"])
print(aspirin_data)

print("🌊 Testing POST request via _make_request...")
endpoint = "compound/smiles/cids/JSON"
payload = {"smiles": "CCO"}  # Ethanol SMILES

# Send as a POST request!
raw_response = wave._make_request(endpoint, method="POST", payload=payload)
print(raw_response)
'''