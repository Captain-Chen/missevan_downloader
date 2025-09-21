# MissEvan Downloader | 猫耳FM广播剧下载工具

## What is this?
A tool that can be used to download all of your favorite radio dramas from MissEvan/猫耳FM. 

### Features
* Fast concurrent downloads using a single session
* Can handle large audio files without using a lot of memory
* Infers the file extension from the HTTP response header

## How to install (on Windows)
1. Clone the project:  
`git clone https://github.com/Captain-Chen/missevan_downloader.git`
2. Install the dependencies: `python -m pip install -r requirements.txt`
3. Decide whether you want to run the script directly or compile as a standlone executable.
    * To run the script directly: `python missevan_downloader.py`  
    * To compile as a standalone executable:
        * Install PyInstaller: `python -m pip install pyinstaller`
        * Run: `pyinstaller missevan_downloader.py --onefile --windowed && cd dist`
        * Run `missevan_downloader.exe` inside the `dist` folder and follow the prompts. You may run this executable from anywhere on your machine.

## How to use (on Windows)
> [!TIP]
> **Optional but recommended step:**  
> Some radio dramas are paid and require you to own them in order to download.  
> * If you have a registered account on MissEvan/猫耳FM:
>    * Create a `token.txt` file in the same folder as `missevan_downloader.py` or the bundled application.
>  * Locate and copy your token from your browser:  
>  `Developer Tools > Application > Storage > Cookies > https://www.missevan.com > token > somelongvalue`
>  * Paste your token value into `token.txt` and save.

> [!IMPORTANT]
> **DO NOT SHARE YOUR TOKEN WITH ANYONE ELSE**

1. Run the script directly: `python missevan_downloader.py` or the bundled executable.
2. Enter the url of the drama or episode.  
e.g. `https://www.missevan.com/mdrama/drama/{someId}`  
`https://www.missevan.com/sound/player?id={someId}`
3. The program will look for the corresponding audio files and download them into the `dl` folder. If the file cannot be downloaded it will be skipped.
4. If the downloads fail, your token may be incorrect or expired. Replace the value inside `token.txt` with the new token value.

*Note:* Code may be unoptimized and contain bugs.

### Dependencies & Requirements
Requires Python **v3.7+**
* [asyncio](https://docs.python.org/3/library/asyncio.html)
* [aiohttp](https://docs.aiohttp.org/en/stable/)
* [aiofiles](https://pypi.org/project/aiofiles/)
* [validators](https://validators.readthedocs.io/en/latest/)
