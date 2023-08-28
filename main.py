import cairosvg
import os
import glob
import re
import shutil
from collections import OrderedDict
import json
from PIL import Image


def match_png(png_file):
    """
    This function matches a png file and moves it to a folder.
    Move "./folder/image@1x.png", "./folder/image@2x.png" ... to the folder[./folder/image]

    Parameters:
    png_file (str): The file name of the png file.

    Returns:
    None
    """
    pattern = r"([^@]+)@.*\.png"

    match = re.match(pattern=pattern, string=png_file)
    if match:
        name = match.group(1)
        folder_name = name
        folder = os.path.join(os.curdir, folder_name)
        if not os.path.isdir(folder):
            os.makedirs(folder)

        shutil.move(png_file, folder)
        print(png_file)


def convert_svg(svg_file, width, height):
    """
    Converts a svg file to a png file
    
    Parameters
    ----------
    svg_file : str
        The svg file to be converted
    width : int
        The width of the output png file
    height : int
        The height of the output png file
    
    Returns
    -------
    None
    """
    
    file = os.path.splitext(svg_file)[0]
    for scale in [1, 2, 3]:
        png_file = file + f"@{scale}" + '.png'
        cairosvg.svg2png(url=svg_file, write_to=png_file,
                         output_width=width * scale, output_height=height * scale)


def match_scale(of: str) -> int:
    """
    Returns the scale from a string.

    Parameters
    ----------
    of : str
        The string to parse.

    Returns
    -------
    int
        The scale, or None if not found.
    """

    pattern = r'@(\d+)x'
    match = re.search(pattern=pattern, string=of)
    if match:
        scale = match.group(1)
        return int(scale)


def create_image_json(files: [str]) -> [dict]:
    """
    This function takes a list of files and returns a list of dictionaries
    with the filename, idiom and scale for each file.

    Parameters:
    files (list): A list of strings representing filenames

    Returns:
    list: A list of dictionaries containing the filename, idiom and scale
    """

    files = sorted(files)
    scales = []
    images = []
    for index, file in enumerate(files):
        scales.append(match_scale(file))
        images.append({
            "filename": file.split('/')[-1],
            "idiom": "universal",
            "scale": f"{index + 1}x"
        })
    images.sort(key=lambda x: float(x['scale'][:-1]))
    return images


def create_json(dir: str) -> OrderedDict:
    """
    This function creates a json file from a directory of images.

    Parameters:
    dir (str): The directory of images.

    Returns:
    OrderedDict: A dictionary containing the images and their corresponding information.
    """

    png_files = glob.glob(dir + '/*.png')
    images = create_image_json(png_files)
    data = OrderedDict()
    data['images'] = images
    data['info'] = {
        "author": "xcode",
        "version": "1"
    }
    return data


def create_json_file(folder: str):
    """
    This function creates images from a given folder.

    Parameters
    ----------
    folder : string
        The folder where the images are located.

    Returns
    -------
    None
    """

    with open(folder + '/Contents.json', 'w+') as f:
        print(folder + '/Contents.json')
        json.dump(create_json(dir=folder), sort_keys=True, fp=f)
        print(f"done: {folder}")


def list_dirs(folder: str):
    """
    Get a list of all directories in a given folder.

    Parameters
    ----------
    folder : str
        The path to the folder to search.

    Returns
    -------
    list
        A list of all the directories in the given folder.
    """
    dir_list = os.listdir(folder)
    dirs = []
    for name in dir_list:
        dir = os.path.join(folder, name)
        if os.path.isdir(dir):
            dirs.append(dir)
    return dirs


def rename_image_folder(folder):
    """
    Rename folders that end in .imageset

    Parameters
    ----------
    folder : str
        Folder name

    Returns
    -------
    str
        Folder name
    """
    pattern = r'(.+)-\w+\.imageset'
    match = re.match(pattern, folder)

    if match:
        new_name = re.sub(pattern, r'\1.imageset', folder)
        print(f"Renaming {folder} to {new_name}")
        return new_name

    return folder


def get_all_files(ext: str, dir: str) -> [str]:
    return glob.glob(f'{dir}/*.{ext}')


def resize_image(url: str, size: int = 96 / 3):
    pattern = r'(.+).png'
    match = re.match(pattern, url)
    if match:
        scales = [1, 2, 3]
        with open(url, 'rb') as i:
            origin_image = Image.open(i).convert('RGBA')

            image_file_name = match.group(1)
            image_folder = image_file_name + '.imageset'
            image_name = url.split('/')[-1].split('.')[0]
            create_folder(image_folder)
            for scale in scales:
                new_size = (int(size * scale), int(size * scale))
                new_img = Image.new('RGBA', new_size)
                resiezed_image = origin_image.resize(new_size, Image.BICUBIC)
                dest = image_folder + '/' + image_name + f'@{scale}.png'
                new_img.paste(resiezed_image)
                new_img.save(dest, format='PNG')
                print(f"{url} Saved to {dest}")


def create_folder(folder: str):
    if not os.path.isdir(folder):
        os.makedirs(folder)


if __name__ == '__main__':
    dir = './source'
    png_images = glob.glob(f"{dir}/*.png")
    for image in png_images:
        image_folders = dir + '/' + \
            image.split('/')[-1].split('.')[0] + '.imageset'
        create_json_file(folder=image_folders)
