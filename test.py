from chemwave import ChemWave

wave = ChemWave()

# We test our internal helper manually just to verify it works!
# Querying PubChem for water's molecular weight in JSON format
endpoint = "compound/name/water/property/MolecularWeight/JSON"

print("🌊 Sending raw request to PubChem...")
data = wave._make_request(endpoint)

print("Response received from PubChem:")
print(data)