<h3 align="center">xcode-imageset-helper


</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/Lorpaves/Xcode-imageset-helper/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/Lorpaves/Xcode-imageset-helper/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>


---

<p align="center"> xcode-imageset-helper is a command-line tool that simplify the steps of adding multiple images in XCode Asset
    <br> 
</p>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 About ](#-about-)
- [🏁 Getting Started ](#-getting-started-)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [🎈 Usage ](#-usage-)
- [🔧 Python API ](#-python-api-)

## 🧐 About <a name = "about"></a>

xcode-imageset-helper can convert multiple files into folders in XCode Asset format, you can directly drag and drop them into XCode. Support `svg` and `png` format.

## 🏁 Getting Started <a name = "getting_started"></a>

```bash
python main.py image.png

 # result
|—— image.png
|—— image.imageset # ==> generated folder
|    |—— image@1x.png
|    |—— image@2x.png
|    |—— image@3x.png
|    |—— Contents.json
```

### Prerequisites

- Python `3.11.4`


### Installing

A step by step series of examples that tell you how to use this tool.

**1. Clone this repository**

```
git clone https://github.com/Lorpaves/Xcode-imageset-helper.git
```

**2 How to install**

Using `pip`
```
cd Xcode-imageset-helper

pip install -r requirement.txt
```
---

Using `pipenv`
```
cd Xcode-imageset-helper

pip install pipenv

pipenv install

pipenv shell
```


## 🎈 Usage <a name="usage"></a>


**Show help**
```
python main.py --help 

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   file_path      [FILE_PATH]  The URL of the image set, file or folder. [default: None]                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --format                    TEXT     The format of the image set.  Only supports "svg" and "png". Option list: [svg, png, all], when you choose      │
│                                      "all", means both "svg" and "png". If your path is a folder, you will need to specify the image format that you │
│                                      want to convert.                                                                                                │
│                                      [default: all]                                                                                                  │
│ --size                      INTEGER  The @1x size of the image set in pixel. If is None, will set the size to the size of the original image.  │
│                                      [default: None]                                                                                                 │
│ --install-completion                 Install completion for the current shell.                                                                       │
│ --show-completion                    Show completion for the current shell, to copy it or customize the installation.                                │
│ --help                               Show this message and exit.                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

**Generate single file**
> Note: When generating a single file, there is no need to pass a format parameters
```
python main.py image.png 

python main.py image.png --size 24
```

---

**Generate multi-files by giving a direcotry path**
```
python main.py my-folder

python main.py my-folder --format png

python main.py my-folder --format svg

python main.py my-folder --format all --size 24
```


## 🔧 Python API <a name = "python api"></a>

``` bash
# Utils
|—— ImageNotSupportError.py # Error
|—— ImageType.py # Enum : Image type for converting original image. 
|—— c_tuple.py  # Tuple: For tuple calculation. c_tuple(1, 2) * 2 = (2, 4)
|—— file_helper.py  # A list of functions for file handling
|—— printer.py  # colorize text output
```

```bash
# main.py

# original image width andh height
create_imagesets('my-folder')

# same width and height
create_imagesets('my-folder', 100)

# different width and height
create_imagesets('my-folder', 100, 200)

# If you pass in multiple parameters, the height and width of the image only take the first and second, for the following example is (100, 200)
create_imagesets('my-folder', 100, 200, 300, 400)

# same as `create_images`
create_imageset('image.png')
```


