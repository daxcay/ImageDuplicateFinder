
# ImageDuplicateFinder

ImageDuplicateFinder is a Python and Flask based webapp designed to efficiently identify duplicate images within a dataset. This project utilizes advanced image processing and machine learning techniques to compare and detect duplicates.

## Features

- **Robust Duplicate Detection**: Leverages deep learning models to find exact and near-duplicate images.
- **Scalable**: Efficiently handles large datasets with minimal performance overhead.
- **Extensible**: Easy to integrate with other applications using Flask.
- **Visualization**: Provides visual confirmation of detected duplicates.


## Run Locally

Clone the project

```bash
  git clone https://github.com/daxcay/ImageDuplicateFinder
```

Make sure **venv** is installed

```
pip install virtualenv
```

## Go to the project directory.

- ### Windows

Open run_windows.bat

- ### Linux & MacOS

Open a terminal and give execute permission like this

```
chmod +x run_linux_mac.sh
```

Execute the script

```
./run_linux_mac.sh
```

## Installation

When you run the above scripts it creates a virtual environment and installs every requirement automatically.

If all goes well you will see a browser window gets open to this address: 

```
http://127.0.0.1:5501
```
![image](https://github.com/daxcay/ImageDuplicateFinder/assets/164315771/3e8bac40-6779-42ba-a474-3293b6479443)

## Usage

- **Image Folder Preparation**: Make a folder and place all the image files in top level. make sure no other subfolder is present.
- **Copy Folder Path**: ok now copy this folder as path.
- **Paste Folder Path**: paste folder in the input and press submit.
- After successfull run you will see a page to select image for deletion.
- By default all the duplicate imges are selected for deletion but check the selected images for any incorrect selection.
- Press deleted selected to delete all the duplicate files.
- Finally, open the image directory. Images are now duplicate free.
- A backup folder is created with all the original files (with duplicates) in case anything goes wrong. 


# CREDITS

◉ Daxton Caylor - ComfyUI Node Developer 
- Discord - daxtoncaylor
- Email - daxtoncaylor@gmail.com
- Discord server: https://discord.gg/Z44Zjpurjp
- Commission Status:  🟢 **Open** 🟢

# Support ❤️
- Buy me a coffee: https://buymeacoffee.com/daxtoncaylor
- If you like to suppport me you can donate me on paypal: https://paypal.me/daxtoncaylor
