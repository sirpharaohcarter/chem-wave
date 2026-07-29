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
    
    def _make_request(self, endpoint: str) -> dict:
        """
        Internal helper to fetch data from PubChem safely.
        
        :param endpoint: The relative API path (e.g., 'compound/name/water/property/MolecularWeight/JSON')
        """
        url = f"{self.base_url}/{endpoint}"
        
        response = self.session.get(url)
        
        response.raise_for_status() #errors
        
        time.sleep(self.delay) #rate limiter
        
        return response.json()

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