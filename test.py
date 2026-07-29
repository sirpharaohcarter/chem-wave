from chemwave import ChemWave

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

'''
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