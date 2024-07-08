
![COMFY-UI (4)](https://github.com/daxcay/ImageDuplicateFinder/assets/164315771/39d8151a-b234-4fd5-b65d-2291a96585ff)

# Image Duplicate Finder

![image](https://img.shields.io/badge/version-1.1.0-green) ![image](https://img.shields.io/badge/last_update-July_2024-green)

**Image Duplicate Finder** is a python and flask based webapp designed to efficiently identify duplicate images within a dataset. This project utilizes advanced image processing and machine learning techniques to compare and detect duplicates.

Youtube video tutorial: [https://www.youtube.com/watch?v=u90vtRh4Fr8](https://youtu.be/-v9X4CBX81A)

## Installation

  #### Requirements
  
  - Latest Python (😅)
  - Git (https://git-scm.com/downloads)
  - Virtual environment package `virtualenv`: To install open CMD and write `pip install virtualenv`    
  - Clone repository into a folder: `git clone https://github.com/daxcay/ImageDuplicateFinder`

  #### Execution

  Go to the cloned repository folder: 

  - **For Windows**: open `run_window.bat` and allow app to run. (as its downloaded from internet it will ask for it)
  - **Linux & MacOS**: open shell/terminal and give execute permission like this: `chmod +x run_linux_mac.sh` and execute it like this: `./run_linux_mac.sh`

  #### Initial run
  - When running for the first time the program will install Flask, numpy, Pillow, scikit-learn, tensorflow.  
  - Updates will take place automatically.
  - If all goes well a browser windows will open with this address `http://127.0.0.1:5501`

  ![image](https://github.com/daxcay/ImageDuplicateFinder/assets/164315771/19919300-bfbb-4d45-8b72-dba08e4a0510)

## Usage

- ### Image path

    Got to your image folder and copy it as a path and paste it in the input box.

    > **Note**: Make sure images names have no spaces.
  
- ### Setting Euclidean Similarity Threshold

    A **lower** value indicates higher similarity between the images.

    - 0 (exactly same)
    - 0.5 (similar enough)
    - 1.0 (different)

> **Note:** if you notice too many false positives (different images flagged as duplicates), lower the `Euclidean Similarity Threshold` and/or raise the `Cosine Similarity Threshold`.
    
- ### Setting Cosine Similarity Threshold
  
    A **higher** value indicates higher similarity between the images.

    - 0 (different)
    - 0.5 (similar enough)
    - 1 (exactly same)

> **Note:** if you notice too many false negatives (missed duplicates), raise the `Euclidean Similarity Threshold` and/or lower the `Cosine Similarity Threshold`.

- ### Best Setting
    - Euclidean Similarity Threshold = **0.5**
    - Cosine Similarity Threshold = **0.9**

After a successful run, you will see a page to select images for deletion. By default, all the duplicate images are selected for deletion, but check the selected images for any incorrect selection. Press "delete selected" to delete all the duplicate files. Finally, open the image directory. Images are now duplicate-free. A backup folder is created with all the original files (with duplicates) in case anything goes wrong.

## Credits

### Raf Stahelin - Testing and Feedback

### Daxton Caylor - ComfyUI Node Developer 
  - ### Contact
     - **Twitter**: @daxcay27
     - **Email** - daxtoncaylor@gmail.com
     - **Discord** - daxtoncaylor
     - **DiscordServer**: https://discord.gg/Z44Zjpurjp
    
  - ### Support
     - **Buy me a coffee**: https://buymeacoffee.com/daxtoncaylor
     - **Support me on paypal**: https://paypal.me/daxtoncaylor
