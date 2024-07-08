
# ImageDuplicateFinder

![image](https://img.shields.io/badge/version-1.1.0-green) ![image](https://img.shields.io/badge/last_update-July_2024-green)

**ImageDuplicateFinder** is a python and flask based webapp designed to efficiently identify duplicate images within a dataset. This project utilizes advanced image processing and machine learning techniques to compare and detect duplicates.

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
  
  - ### Setting Euclidean Similarity Threshold (`esimilarity_threshold`)
  
    It Measures the Euclidean distance between the feature vectors of two images. A lower Euclidean distance indicates higher similarity between the images.
      
    - **Best Setting**: Lower values (e.g., 0.1) are more strict, identifying images as duplicates only if they are very similar. This minimizes false positives but may miss some duplicates.
    - **Worst Setting**: Higher values (e.g., 1.0) are more lenient, allowing for more variance between images to be considered duplicates. This can increase false positives.
    
  - ### Setting Cosine Similarity Threshold (`csimilarity_threshold`)
  
    It Measures the cosine similarity between the feature vectors of two images. A higher cosine similarity (closer to 1) indicates higher similarity between the images.
      
    - **Best Setting**: Higher values (e.g., 0.95) are more strict, identifying images as duplicates only if they are very similar. This minimizes false positives but may miss some duplicates.
    - **Worst Setting**: Lower values (e.g., 0.7) are more lenient, allowing for more variance between images to be considered duplicates. This can increase false positives.

  - ### Default Values
  
    - `esimilarity_threshold=0.5`: This is a moderate setting, balancing between false positives and false negatives.
    - `csimilarity_threshold=0.9`: This is a high setting, ensuring that only very similar images are considered duplicates.
  
  - ### Impact of Settings
  
    - **Strict Settings (Lower `esimilarity_threshold` and Higher `csimilarity_threshold`)**:
      - **Pros**: Reduces false positives, ensuring that only very similar images are flagged as duplicates.
      - **Cons**: May miss some duplicates that have slight variations.
        
    - **Lenient Settings (Higher `esimilarity_threshold` and Lower `csimilarity_threshold`)**:
      - **Pros**: Captures more potential duplicates, including those with slight variations.
      - **Cons**: Increases the risk of false positives, flagging non-duplicate images as duplicates.
  
  - ### Recommendations
  
    - **Best Settings for Most Use Cases**: 
      - `esimilarity_threshold=0.5` (moderate strictness)
      - `csimilarity_threshold=0.9` (high strictness)
    
    - **Adjustments**: 
      - If you notice too many false positives, lower the `esimilarity_threshold` and/or raise the `csimilarity_threshold`.
      - If you notice too many false negatives (missed duplicates), raise the `esimilarity_threshold` and/or lower the `csimilarity_threshold`.

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
