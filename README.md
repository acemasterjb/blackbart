# Black Bart
*Bartholomew Roberts,  aka Black Bart, was a Welsh pirate and the most successful pirate of the Golden Age of Piracy.*

This repo scrapes exchange rate data from the central bank websites of various Caricom (Caribbean Community) countries.

## Installation
**1) Set up your venv**

**... with conda**
```bash
cd ~/to/folder/you/cloned/to
conda create -p ./venv -python 3.8.5
conda activate ./venv
```

**... with vanilla python**
```bash
python3 -m venv ./venv
```
then activate

windows:
```powershell
venv\Scripts\activate.bat
```

linux/macOS:
```bash
source ./venv/bin/activate
```

**2) Set up your dependencies**
```bash
pip3 pip install -r requirements.txt
```

**3) Run the server**
```bash
uvicorn main:app --reload
```

`--reload` means that your server will reload when you make changes to `main.py`
