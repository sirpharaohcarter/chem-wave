import time
import requests
from typing import List, Dict, Optional

class ChemWave:
    """
    ChemWave 🌊
    A client wrapper for the PubChem PUG REST API.
    """
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    def __init__(self, delay_seconds: float = 0.25):
        self.delay = delay_seconds
        
        self.session = requests.Session()

    def __repr__(self) -> str:
        return f"<ChemWave client (delay={self.delay}s)>"
    
    def _make_request(self, endpoint: str, method: str = "GET", payload: Optional[dict] = None):
        """
        Internal dispatcher handling HTTP GET/POST, rate limiting, and response parsing.
        
        :param endpoint: Relative API route (e.g., 'compound/smiles/cids/JSON')
        :param method: HTTP method ('GET' or 'POST')
        :param payload: Dictionary data to send in POST body (e.g., {'smiles': 'CCO'})
        """
        url = f"{self.base_url}/{endpoint}"

        try: 
            if method.upper() == "POST":
                response = self.session.post(url, data=payload)
            else:
                response = self.session.get(url)
            
            # errors
            response.raise_for_status()
        
            # rate limit
            time.sleep(self.delay)
        
            return response.json()
        
        except requests.exceptions.HTTPError as err:
            # Safely handle bad queries (e.g. 400 Bad Request, 404 Not Found)
            print(f"⚠️ [chem-wave] API request failed ({response.status_code}): {err}")
            return None


    def get_compound(self, name: str, properties: Optional[List[str]] = None) -> Dict:
        """
        Fetch property details for a compound by its common name.
        
        :param name: Common name of the compound (e.g., 'caffeine', 'aspirin')
        :param properties: List of properties to retrieve (defaults to common set if None)
        """
        if properties is None:
            properties = ["MolecularFormula", "MolecularWeight", "IUPACName"]

        # string of props "MolecularFormula,MolecularWeight,IUPACName"
        prop_str = ",".join(properties)

        # 2. endpoint url eg. compound/name/caffeine/property/MolecularFormula,MolecularWeight/JSON
        endpoint = f"compound/name/{name}/property/{prop_str}/JSON"

        data = self._make_request(endpoint)

        # 4. Extract and return the dict
        try:
            return data["PropertyTable"]["Properties"][0]
        except (KeyError, IndexError):
            return {}

    def smiles_to_cid(self, smiles: str) -> Optional[int]:
        """
        Convert a SMILES structure string into a PubChem Compound ID (CID).
        
        :param smiles: Chemical SMILES string (e.g., 'CCO' for Ethanol)
        :return: Integer CID if found, or None if invalid/not found.
        """
        endpoint = "compound/smiles/cids/JSON"
        payload = {"smiles": smiles}
        
        # 1. Send the POST request through our internal helper
        data = self._make_request(endpoint, method="POST", payload=payload)

        if not data:
            return None
        
        try:
            cids = data["IdentifierList"]["CID"]
            return cids[0]  # Return the CID
        except (KeyError, IndexError, TypeError):
            return None