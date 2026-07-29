import time
import requests


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