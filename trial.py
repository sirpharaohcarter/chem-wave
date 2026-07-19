import requests
import pandas as pd
 
compounds = ["caffeine", "aspirin", "ibuprofen"]
data_list = []

for chemical in compounds: 
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical}/property/MolecularWeight,XLogP/JSON"
    response = requests.get(url).json()
     
    props = response['PropertyTable']['Properties'][0]
    data_list.append({
        "Name": chemical,
        "MW": props.get("MolecularWeight"),
        "LogP": props.get("XLogP")
    })
 
df = pd.DataFrame(data_list)
print(df)