import time
import requests
from typing import List, Dict, Optional, Union

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


    def get_compound(self, identifier: Union[str, int], namespace: str = "name", properties: Optional[List[str]] = None) -> Dict:
        """
        Fetch property details for a single compound by Name, CID, or SMILES.
        
        :param identifier: Name (e.g. 'caffeine'), CID (e.g. 2244), or SMILES string.
        :param namespace: Lookup domain type: 'name', 'cid', or 'smiles' (Default: 'name')
        :param properties: List of property names to retrieve.
        """
        if namespace == "smiles":
            cid = self.smiles_to_cid(str(identifier))
            if not cid:
                return {}
            identifier = cid
            namespace = "cid"
        
        if properties is None:
            properties = ["MolecularFormula", "MolecularWeight", "IUPACName"]

        # string of props "MolecularFormula,MolecularWeight,IUPACName"
        prop_str = ",".join(properties)

        # 2. endpoint url eg. compound/name/caffeine/property/MolecularFormula,MolecularWeight/JSON
        endpoint = f"compound/{namespace}/{identifier}/property/{prop_str}/JSON"

        data = self._make_request(endpoint)

        # 4. Extract and return the dict
        try:
            return data["PropertyTable"]["Properties"][0]
        except (KeyError, IndexError):
            return {}

    def batch_get_compounds(self, identifiers: List[Union[str, int]], namespace: str = "cid", properties: Optional[List[str]] = None) -> List[Dict]:
        """
        Fetch properties for multiple compounds at once using their CIDs.
        
        :param cids: List of integer PubChem CIDs (e.g. [2244, 702, 962])
        :param properties: List of property names to retrieve
        :return: List of property dictionaries for each compound found
        """
        if not identifiers:
            return []

        # convert names / SMILES to cid for ease
        resolved_cids: List[int] = []

        if namespace == "cid":
            # confirm cids
            resolved_cids = [int(i) for i in identifiers]
        elif namespace == "name":
            for name in identifiers:
                cid = self.name_to_cid(str(name))
                if cid:
                    resolved_cids.append(cid)
        elif namespace == "smiles":
            for smiles in identifiers:
                cid = self.smiles_to_cid(str(smiles))
                if cid:
                    resolved_cids.append(cid)

        # if no valid cids
        if not resolved_cids:
            return []

        if properties is None:
            properties = ["MolecularFormula", "MolecularWeight", "IUPACName"]

        # bulk request
        cid_str = ",".join(map(str, resolved_cids))
        prop_str = ",".join(properties)
        endpoint = f"compound/cid/{cid_str}/property/{prop_str}/JSON"

        data = self._make_request(endpoint)

        if not data:
            return []

        # 4. Return the list of property dictionaries
        try:
            return data["PropertyTable"]["Properties"]
        except (KeyError, TypeError):
            return []
    
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

    def name_to_cid(self, name: str) -> Optional[int]:
        """
        Convert a compound's common or chemical name into its PubChem CID.
        
        :param name: Chemical or common name (e.g. 'caffeine', 'aspirin')
        :return: Integer CID if found, or None if invalid/not found.
        """
        endpoint = f"compound/name/{name}/cids/JSON"
        
        data = self._make_request(endpoint)
        
        if not data:
            return None
            
        try:
            cids = data["IdentifierList"]["CID"]
            return cids[0]
        except (KeyError, IndexError, TypeError):
            return None