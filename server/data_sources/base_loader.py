from abc import ABC, abstractmethod
from typing import List, Dict

class BaseLoader(ABC):
    @abstractmethod
    async def load(self) -> List[Dict]:
      
     pass
