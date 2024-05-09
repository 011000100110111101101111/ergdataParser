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

## About
