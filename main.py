import cairosvg
import os
import shutil
from collections import OrderedDict
import json
from PIL import Image
from typing import List, Tuple, Dict
from utils import *
import typer

def create_image_folder(image_url: str) -> str:
    """Creates a folder for storing images.
    
    Args:
        image_url (str): The URL of the image.
    
    Returns:
        str: The path of the created folder.
    """
    
    dir = image_file_prefix(image_url) + '.imageset'
    create_folder(dir)
    return dir


def create_scaled_image_urls(image_url: str) -> List[Dict[str, str]]:
    """Creates a list of dictionaries containing scaled image URLs.
    
    Args:
        image_url (str): The URL of the original image.
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries, where each dictionary contains the scaled image URL and its corresponding scale factor.
    
    Example:
        >>> create_scaled_image_urls("https://example.com/image.png")
        [{'url': 'image@1x.png', 'scale': '1'}, {'url': 'image@2x.png', 'scale': '2'}, {'url': 'image@3x.png', 'scale': '3'}]
    """
    
    SCALES = [1, 2, 3]
    image_name = get_image_name(image_url)
    return [ {"url": f'{image_name}@{s}x.png', "scale": str(s)} for s in SCALES]

def get_image_name(image_url: str) -> str:
    """Get the name of an image from its URL.
    
    Args:
        image_url (str): The URL of the image.
    
    Returns:
        str: The name of the image without the file extension.
    
    Example:
        >>> get_image_name('https://example.com/images/image.jpg')
        'image'
    """
    
    return os.path.splitext(os.path.basename(image_url))[0]

def image_file_prefix(image_url: str) -> str:
    """Return the prefix of an image file.
    
    Args:
        image_url (str): The URL of the image file.
    
    Returns:
        str: The prefix of the image file.
    
    Example:
        >>> image_file_prefix('https://example.com/image.jpg')
        'https://example.com/image'
    """
    
    return os.path.splitext(image_url)[0]

def resize_image(image: Image.Image, new_size: Tuple[int, int]):
    """Resizes an image to a new size.
    
    Args:
        image (PIL.Image.Image): The image to be resized.
        new_size (Tuple[int, int]): The new size of the image.
    
    Returns:
        PIL.Image.Image: The resized image.
    
    Example:
        >>> from PIL import Image
        >>> image = Image.open('image.jpg')
        >>> new_size = (800, 600)
        >>> resized_image = resize_image(image, new_size)
    """
    
    new_img = Image.new('RGBA', new_size)
    resiezed_image = image.resize(new_size, Image.BICUBIC)
    new_img.paste(resiezed_image)
    return new_img

def move_png_image(png_file: str, dest: str):
    """Moves a PNG image file to a specified destination.
    
    Args:
        png_file (str): The path of the PNG image file to be moved.
        dest (str): The destination path where the PNG image file will be moved to.
    
    Raises:
        FileNotFoundError: If the source PNG image file does not exist.
        PermissionError: If the user does not have permission to move the PNG image file.
    """
    
    shutil.move(png_file, dest)


def convert_svg(svg_file: str, *size: int):
    """Converts an SVG file to PNG images of different sizes.
    
    Args:
        svg_file (str): The path to the SVG file.
        size (Tuple[int, int]): The desired width and height of the output images.
    
    Returns:
        None
    
    Raises:
        FileNotFoundError: If the SVG file does not exist.
        OSError: If there is an error creating the image folder or saving the PNG files.
    
    Example:
        convert_svg('path/to/file.svg', (100, 100))
    """
    if not size or len(size) == 0:
        with open(svg_file, 'rb') as i:
            size = Image.open(i, formats=['SVG']).size
    elif len(size) == 1:
        size = (size[0], size[0])
    file = image_file_prefix(svg_file)
    dir = create_image_folder(file + '.imageset')
    for scaled_image_url in create_scaled_image_urls(svg_file):
        png_file_name = scaled_image_url['url']
        scale = int(scaled_image_url['scale'])
        new_size = c_tuple(size) * scale
        png_file = os.path.join(dir, png_file_name)
        cairosvg.svg2png(url=svg_file, write_to= png_file, output_width= new_size[0], output_height= new_size[1])
        print_white(f'  - "{svg_file}" Saved to "{png_file}"')
    create_json_file(dir)
    


def create_image_json(files: List[str]) -> List[Dict[str, str]]:
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
    json_images = []
    for index, file in enumerate(files):
        scales.append(index + 1)
        json_images.append({
            "filename": file.split('/')[-1],
            "idiom": "universal",
            "scale": f"{index + 1}x"
        })
    json_images.sort(key=lambda x: float(x['scale'][:-1]))
    return json_images


def create_json(dir: str) -> OrderedDict:
    """This function creates a json file from a directory of images.

    Parameters:
    dir (str): The directory of images.

    Returns:
    OrderedDict: A dictionary containing the images and their corresponding information.
    """

    # png_files = glob.glob(dir + '/*.png')
    png_files = get_all_files(dir=dir, type=ImageType.PNG)
    images = create_image_json(png_files)
    data = OrderedDict()
    data['images'] = images
    data['info'] = {
        "author": "xcode",
        "version": "1"
    }
    return data


def create_json_file(folder: str):
    """Creates a JSON file named 'Contents.json' in the specified folder.
    
    Args:
        folder (str): The path of the folder where the JSON file will be created.
    
    Returns:
        None
    
    Raises:
        FileNotFoundError: If the specified folder does not exist.
    
    Example:
        create_json_file('/path/to/folder')
    """
    
    json_file = folder + '/Contents.json'
    with open(json_file, 'w+') as f:
        json.dump(create_json(dir=folder), sort_keys=True, fp=f)
        print_white(f"  - Contents.json was created to: {json_file}")




def create_images(url: str, *size: int):
    """Creates scaled images from the given URL.
    
    Args:
        url (str): The URL of the image file.
        *size (int): Variable length argument representing the desired size of the scaled images. If no size is provided, the original image size is used. If only one size is provided, the scaled images will have equal width and height.
    
    Returns:
        None
    
    Raises:
        FileNotFoundError: If the specified URL does not exist.
    
    Example:
        create_images('my-folder', 100, 200, 300)
    """
    
    with open(url, 'rb') as i:
        origin_image = Image.open(i).convert('RGBA')
        if not size or len(size) == 0:
            size = origin_image.size
        elif len(size) == 1:
            size = (size[0], size[0])
        dir = create_image_folder(url)
        scaled_image_urls = create_scaled_image_urls(url)
        for scaled_image_info in scaled_image_urls:
            new_size = c_tuple(size) * int(scaled_image_info['scale'])
            new_image = resize_image(origin_image, (new_size[0], new_size[1]))
            new_image_url = os.path.join(dir, scaled_image_info['url'])
            new_image.save(new_image_url, format='PNG')
            print_white(f'  - "{url}" Saved to "{new_image_url}"')
        create_json_file(dir)
      


def create_imageset(file: str, *size: int):
    """Create an image set based on the given file and sizes.
    
    Args:
        file (str): The path to the file.
        *size (int): Variable length argument representing the sizes of the images.
    
    Raises:
        FileNotFoundError: If the file does not exist or is not a regular file.
        ImageNotSupportError: If the file type is not supported.
    
    Example:
        create_imageset('image.png', 100, 200, 300)
    """
    

    if not (os.path.exists(file) and os.path.isfile(file)):
        raise FileNotFoundError
    _, ext = os.path.splitext(file)
    ext = ext[1:]

    if ext == ImageType.PNG.value:
        create_images(file, *size)
    elif ext == ImageType.SVG.value:
        convert_svg(file, *size)
    else:
        raise  ImageNotSupportError(message=f'File type is not supported. {ext}')
        
def create_imagesets(dir: str, type: ImageType, *size: int):
    """Creates image sets for all files in a given directory.
    
    Args:
        dir (str): The directory path where the files are located.
        type (ImageType): The type of image files to include in the image sets.
        *size (int): Variable length argument representing the sizes of the image sets.
    
    Raises:
        FileExistsError: If the directory does not exist or is not a directory.
    
    Returns:
        None
    
    Example:
        create_imagesets('/path/to/directory', ImageType.PNG, 100, 200, 300)
    """
    
    if not (os.path.exists(dir) and os.path.isdir(dir)) :
        raise FileExistsError
    print_cyan('Start converting...')
    all_files = get_all_files(dir=dir, type=type)
    for index, file in enumerate(all_files):
        print_white(f'⭕️ Start task for {file}')
        create_imageset(file, *size)
        print_green(f'✅({index + 1} / {len(all_files)}) Task completed for image {file}')
    print_cyan('All tasks done.')


app = typer.Typer()

@app.command()
def create(
    url: str = typer.Argument(default=None, help = ' The path of the image set, file or folder.', show_default=True, allow_dash=True), 
    format: str = typer.Option(default='all', help="""The format of the image set.  Only supports "svg" and "png".
                            Option list: [svg, png, all], when you choose "all", means both "svg" and "png".
                            If your path is a folder, you will need to specify the image format that you want to convert."""),
    size: List[int]  = typer.Option(default=None, help='The @1x size of the image set in pixel. If is None, will set the size to the size of the original image.')):
    if os.path.isdir(url):
        create_imagesets(url, parse_format(format), *size)
    elif os.path.isfile(url):
        create_imageset(url, *size)
    
def parse_format(format: str) -> ImageType:
    """Parses the given format string and returns the corresponding ImageType.
    
    Args:
        format (str): The format string to be parsed.
    
    Returns:
        ImageType: The corresponding ImageType based on the format string.
    """
    
    if format == 'all':
        return ImageType.All
    if format == ' png':
        return ImageType.PNG
    if format == 'svg':
        return ImageType.SVG
    return ImageType.PNG

if __name__ == '__main__':
    app()
