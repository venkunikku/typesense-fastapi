# to create a local env

Tested in `Python 3.13`

## create a virtual environment.

Directly under the code root folder run 

```
python -m venv fastapi-typesense
```
## To activate the env on the command line
1. Go into the root of the folder.
2. Run below command to activate.
```
fastapi-typesense\Scripts\activate.bat # on windows
fastapi-typesens/Scripts/activate # on linux
pip install -r requirements.txt
```
## To run local server
1. cd into src folder and then run below command
```
uvicorn main:app --reload --port 8020
```
