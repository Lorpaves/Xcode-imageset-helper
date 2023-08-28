from enum import Enum 
from typing import List


def from_str(format: str) -> object:
    if format == 'all':
        return ImageType.All.value
    if format == ' png':
        return ImageType.PNG.value
    if format == 'svg':
        return ImageType.SVG.value
class ImageType(Enum):
    PNG = "png"
    SVG = "svg"
    All = [PNG, SVG]
    @classmethod
    def all(cls): 
        return [cls.PNG, cls.SVG]
    
        
    
  
