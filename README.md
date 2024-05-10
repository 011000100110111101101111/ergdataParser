# Setup

## Create virtual env

Create the virtual env

```
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

(Optional) Add packages to develop further

```
# Since we created the virtual env, we can now use python instead of python3
python -m pip install <package>
# Update stored packages (requirments.txt)
python -m pip freeze > requirements.txt
```

Deactivate the virtual env

```
deactivate
```

## Usage

Download all your rowerg data from logbook as csv files and put in the same directory as this program. Then just run the program, it has a basic interface for options. It will move all used folders to *used-reports* after it is complete, and append PROCESSED to the end.
