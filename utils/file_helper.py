import os
from .ImageType import ImageType
from typing import List
import glob

def create_folder(folder: str):
    """
    This function creates a folder if it does not exist.

    Parameters:
    folder (str): The path of the folder to be created.

    Returns:
    None
    """
    if not os.path.isdir(folder):
        os.makedirs(folder)


def get_all_files(dir: str, type: ImageType) -> List[str]:
    """
    Get all files with the given extension in the given directory.
    
    Parameters
    ----------
    ext : str
        The extension of the files to get.
    dir : str
        The directory to search.
    
    Returns
    -------
    List[str]
        A list of filenames with the given extension in the given directory.
    """
    if type == ImageType.All:
        return [f for t in type.value for f in glob.glob(f'{dir}/*.{t}')]
    return glob.glob(f'{dir}/*.{type.value}')
